#!/usr/bin/env python

import os
import sys
import sqlite3
from stat import *
import MacOS
import hashlib

gExcludeList = set(['/private/var/FileWave', '/Volumes', '/private/tmp', '/dev/fd'])

gUseMD5 = True

class File:   
    def fromFile(self, path):
        s = os.lstat(path)
        
        self.md5 = ''
        self.rfmd5 = ''
        
        # Find resource fork size manually
        if S_ISREG(s[ST_MODE]):
            rf = MacOS.openrf(path, 'r')
            rf.seek(0, 2) #seeks to end of file
            self.rfSize = rf.tell()
            
            rfNumBytes = int(self.rfSize)
            
            if gUseMD5 and rfNumBytes > 0:
                rf.seek(0)
                h = hashlib.md5()
                h.update(rf.read(rfNumBytes))
                self.rfmd5 = h.hexdigest()
            
            rf.close()
        else:
            self.rfSize = 0
            
        # Find data md5
        if gUseMD5 and S_ISREG(s[ST_MODE]) and s[ST_SIZE] > 0:
            f = open(path, 'r')
            h = hashlib.md5()
            
            d = f.read(4096)
            while d:
                h.update(d)
                d = f.read(4096)
            
            #h.update(f.read())
            self.md5 = h.hexdigest()
        
        self.name = path
        self.mode = s[ST_MODE]
        self.uid = s[ST_UID]
        self.gid = s[ST_GID]
        self.size = s[ST_SIZE]
        self.creationDate = s[ST_CTIME]
        self.modificationDate = s[ST_MTIME]
        
        if S_ISLNK(s[ST_MODE]):
            self.linkPath = os.readlink(path)
        else:
            self.linkPath = ''
            
    def fromTuple(self, record):
        self.name = record[0]
        self.mode = record[1]
        self.uid = record[2]
        self.gid = record[3]
        self.size = record[4]
        self.rfSize = record[5]
        self.creationDate = record[6]
        self.modificationDate = record[7]
        self.linkPath = record[8]
        self.md5 = record[9]
        self.rfmd5 = record[10]
    
    # From a FW admin.sqlite record
    def fromFWTuple(self, fullPathName, record, isDir = False):
        self.name = fullPathName
        self.mode = record['unixMode']
        self.uid = record['unixOwnerID']
        self.gid = record['unixGroupID']
        
        if not isDir:
            self.size = record['dataForkSize']
            self.rfSize = record['resourceForkSize']
            self.creationDate = record['creationDate']
            self.modificationDate = record['modificationDate']
        else:
            self.size = 0
            self.rfSize = 0
            self.creationDate = record['dateCreated']
            self.modificationDate = record['dateModified']
        
    def findDiffs(self, f2):
        diffs = {}
        
        self._compare(f2, 'mode', diffs)
        self._compare(f2, 'uid', diffs)
        self._compare(f2, 'gid', diffs)
        self._compare(f2, 'size', diffs)
        self._compare(f2, 'rfSize', diffs)
        #self._compare(f2, 'creationDate', diffs)
        #self._compare(f2, 'modificationDate', diffs)
        self._compare(f2, 'linkPath', diffs)
        self._compare(f2, 'md5', diffs)
        self._compare(f2, 'rfmd5', diffs)
        
        if len(diffs):
            return diffs
        else:
            return None
    
    # When comparing records made from FW admin.sqlite
    def findDiffsFW(self, f2, isDir = False):
        diffs = {}
        
        self._compare(f2, 'mode', diffs)
        self._compare(f2, 'uid', diffs)
        self._compare(f2, 'gid', diffs)
        
        if not isDir:
            self._compare(f2, 'size', diffs)
            self._compare(f2, 'rfSize', diffs)
            #self._compare(f2, 'creationDate', diffs)
            #self._compare(f2, 'modificationDate', diffs)
        
        if len(diffs):
            return diffs
        else:
            return None
        
    def _compare(self, f2, attr, diffs):
        a = self.__dict__[attr]
        b = f2.__dict__[attr]
        
        if (a != b):
            diffs[attr] = (a, b)
        
class FileDB:
    def __init__(self, path):
        self.db = sqlite3.connect(path)
        
        self.createTables()
        
    def createTables(self):
        self.db.execute('''create table if not exists files (name text primary key, mode unsigned int, uid unsigned int,
                        gid unsigned int, size unsigned int, rfSize unsigned int, creationDate unisgned int, modificationDate unsigned int, linkPath text, md5 text, rfmd5 text, found unsigned int)''')
        self.db.commit()
    
    def insertFileToDB(self, file):
        f = file
        self.db.execute('insert into files values (?,?,?,?,?,?,?,?,?,?,?,0)', (f.name, f.mode, f.uid, f.gid, f.size, f.rfSize, f.creationDate, f.modificationDate, f.linkPath, f.md5, f.rfmd5))
        
    def getFileFromDB(self, name):
        c = self.db.cursor()
        c.execute('select * from files where name = ?', (name,))
        r = c.fetchone()
        
        if r:
            f = File()
            f.fromTuple(r)
            
            return f
        else:
            return None
    
    def resetFoundFiles(self):
        self.db.execute('update files set found = 0')

    def markFileFound(self, name):
        self.db.execute('update files set found = 1 where name = ?', (name,))
        
    def getFilesNotFound(self):
        c = self.db.cursor()
        c.execute('select name from files where found = 0 order by name asc')
        
        return c
    
    def commit(self):
        self.db.commit()
        
    def close(self):
        self.db.close()
        
def getRelName(path, basePath):
    if basePath == '/':
        return path
    else:
        return path[len(basePath):]
        
def scan(basePath, dbFile):
    db = FileDB(dbFile)
    
    for root, dirs, files in os.walk(basePath):
        if getRelName(root, basePath) in gExcludeList:
            dirs[:] = []
            print "Excluding", getRelName(root, basePath)
            continue
        
        for filename in dirs + files:
            fullName = os.path.join(root, filename)
            f = File()
            f.fromFile(fullName)
            f.name = getRelName(fullName, basePath)

            db.insertFileToDB(f)
            
    db.commit()
    
    db.close()
    
def compare(basePath, dbFile):
    db = FileDB(dbFile)
    db.resetFoundFiles()
    
    for root, dirs, files in os.walk(basePath):
        if getRelName(root, basePath) in gExcludeList:
            dirs[:] = []
            print "Excluding", getRelName(root, basePath)
            continue
        
        for filename in dirs + files:
            fullName = os.path.join(root, filename)
            
            f = File()
            f.fromFile(fullName)
            
            relName = getRelName(fullName, basePath)
            dbf = db.getFileFromDB(relName)
            
            if not dbf:
                print relName, "found on disk but not in DB"
                continue
            
            db.markFileFound(relName)
            
            # Compare
            diffs = dbf.findDiffs(f)
            if diffs:
                print relName, diffs
            
    db.commit()
    
    # List all files not marked in DB
    c = db.getFilesNotFound()
    for r in c:
        print r[0], "found in DB but not on disk"
    
    db.close()

def main():
    global gExcludeList
    
    if len(sys.argv) < 4:
        print "Usage: ./kmagic.py [scan|compare] <path> <db file>"
        sys.exit(1)
    
    mode = sys.argv[1]
    basePath = sys.argv[2]
    dbFile = sys.argv[3]
    
    if basePath[-1] == '/' and basePath != '/':
        basePath = basePath[:-1]
    
    if mode == "scan":
        scan(basePath, dbFile)
    elif mode == "compare":
        if not os.path.exists(dbFile):
            print "Database file does not exist:", dbFile
            sys.exit(2)
            
        compare(basePath, dbFile)
    else:
        print "Unknown mode: ", mode
        sys.exit(1)

if __name__ == "__main__":
    main()
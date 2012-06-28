from PyQt4.QtCore import QObject, pyqtSignal, Qt
from sqlalchemy.sql.expression import desc
from lib.path_info import PathInfo
from datetime import datetime
import simplejson as json
import base64
import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Binary
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker, relationship, backref
from lib.qt_database_wrapper import qtDatabaseWrapper, qtDatabaseConnection

import logging
logger = logging.getLogger(__name__)

Base = declarative_base()

class StopScanningException(Exception):
    pass

def ensure_unicode(s):
    if isinstance(s, unicode):
        return s
    return unicode(s, "utf-8")

class CheckedEntityMixin:
    """
    This mixin is used on the sql-alchemy classes that have a parent and children attribute, and the idea of being "checked" or not - it enables
    the subclasses to populate and propagate this checked state up & down the tree hierarchy.
    """
    def checkedState(self, default_state):
        """
        Works out what the checked state should be based on the immediate children check states - if all children are
        checked the same way, then the returned check state is the same as all the children.  If they are not, then its Qt.PartiallyChecked
        """
        states = set()
        for child in self.children:
            states.add(child.checked)
            if len(states) > 1:
                return Qt.PartiallyChecked

        if len(states) == 1:
            for value in states:
                return value

        return default_state

    def propagateCheckedStateToChildren(self, new_state = None):
        if new_state is None:
            new_state = self.checked
        for child in self.children:
            child.checked = new_state
            child.propagateCheckedStateToChildren(new_state)

    def propagateCurrentCheckedStateToParents(self):
        """Assuming the checked state of this item has changed, walk up the tree re-calculating the correct state for all parents"""
        parent = self.parent
        while parent is not None:
            new_state = parent.checkedState(parent.checked)
            if new_state != parent.checked:
                parent.checked = new_state
            parent = parent.parent

class GeneralInfo(Base):
    __tablename__ = "general_info"
    id = Column(Integer, primary_key=True)
    date_created = Column(DateTime)
    date_last_scanned = Column(DateTime)
    files_scanned = Column(Integer)
    files_merged = Column(Integer)
    reg_entry_scanned = Column(Integer)
    reg_entry_merged = Column(Integer)
    merge_complete = Column(Boolean)
    def __str__(self):
        return "Created:" + str(self.date_created) + ", Last Scanned:"\
                + str(self.date_last_scanned) + ", #files scanned:" + str(self.files_scanned)\
                + ", # files merged:" + str(self.files_merged)

class ScannedPath(Base):
    __tablename__ = "scanned_path"
    abs_path = Column(String(4096), primary_key=True)
    def __str__(self):
        return "ScannedPath: " + self.abs_path

# Note: I was considering using the inheritance options of SQLAlchemy to minimize the children/parent_key code duplication below,
# but decided that I wanted to be able to separate out the FileSystemSnapshot and FileSystemMerge objects - to the point where their data
# does NOT live in the same DB table - making it blindingly obvious where the data lives in case you need to debug it.

class FileSystemSnapshot(Base):
    __tablename__ = "file_system_snapshot"
    abs_path = Column(String(4096), primary_key=True)
    is_dir = Column(Boolean, index=True)
    path_info = Column(String(4096))
    parent_key = Column(String, ForeignKey('file_system_snapshot.abs_path'), index=True)
    children = relationship('FileSystemSnapshot', cascade="all", backref=backref("parent", remote_side=abs_path))
    def __str__(self):
        return u"FileSystemSnapshot: " + ensure_unicode(self.abs_path) + u" dir:" + unicode(self.is_dir)

class FileSystemMerge(Base, CheckedEntityMixin):
    __tablename__ = "file_system_merge"
    abs_path = Column(String(4096), primary_key=True)
    is_dir = Column(Boolean, index=True)
    path_info = Column(String(4096))
    checked = Column(Integer, index=True)
    flags = Column(Integer)
    parent_key = Column(String, ForeignKey('file_system_merge.abs_path'), index=True)
    children = relationship('FileSystemMerge', cascade="all", backref=backref("parent", remote_side=abs_path))

    def __str__(self):
        return u"FileSystemMerge: " + ensure_unicode(self.abs_path) + u" dir:" + unicode(self.is_dir) + u" checked:" + unicode(self.checked) + u" flags:" + unicode(self.flags)

class RegistryEntrySnapshot(Base):
    __tablename__ = "reg_entry_snapshot"
    key_name = Column(String(4096), primary_key=True)
    values = Column(Binary)
    parent_key = Column(Integer, ForeignKey('reg_entry_snapshot.key_name'), index=True)
    children = relationship('RegistryEntrySnapshot', cascade="all", backref=backref("parent", remote_side=key_name))
    def __str__(self):
        return u"RegistryEntryMerge: " + ensure_unicode(self.key_name) + u" checked:" + unicode(self.checked) + u" flags:" + unicode(self.flags)

class RegistryEntryMerge(Base, CheckedEntityMixin):
    __tablename__ = "reg_entry_merge"
    key_name = Column(String(4096), primary_key=True)
    values = Column(Binary)
    checked = Column(Integer, index=True)
    flags = Column(Integer)
    parent_key = Column(Integer, ForeignKey('reg_entry_merge.key_name'), index=True)
    children = relationship('RegistryEntryMerge', cascade="all", backref=backref("parent", remote_side=key_name))

    def __str__(self):
        return u"RegistryEntryMerge: " + ensure_unicode(self.key_name) + u" checked:" + unicode(self.checked) + u" flags:" + unicode(self.flags)

session_cache = dict()

def setup_alchemy_on(obj, filename, echo_sql=False):
    global session_cache

    try:
        engine = None
        maker = None
        session = None

        if filename in session_cache and False:
            engine, maker, session = session_cache[filename]
        else:
            engine = create_engine('sqlite:///{}'.format(filename), echo=echo_sql)
            maker = sessionmaker(bind=engine)
            session = maker()
            session_cache[filename] = (engine, maker, session)

        Base.metadata.create_all(engine)

        setattr(obj, 'engine', engine)
        setattr(obj, 'Session', maker)
    except Exception, e:
        logger.critical("failure setting up the alchemy session, error: {0}".format(e))
        raise

    return session

class PersistentScanningState(QObject):
    """
    this is "The Document", it encapsulates all of the data/state of the paths that we scanned.  Everything required to
    re-start the scanning process at some time in the future is stored here.

    The PersistentScanningState is both the path storage, and the comparison container.  The intent
    is to be able to combine two of them together in order to work out what has changed over time.

    The file_system_snapshot table contains a snapshot of the file system - its our 'pristine state', the file_system_merge table is
    almost a copy of the file_system_snapshot, its created when a 'merge scan' is made.  It contains the added/modified/deleted state.  The
    file_system_merge table can be re-created at any time by calling storeSecondScan - but you don't use it directly, instead
    use the ScanningController.

    Instead of exposing SQL here - almost all of the data manipulation is performed via the SQLAlchemy ORM which maps the Python
    classes to SQL (of various databases).  The ORM provides the ability to use table data as class instances - which
    in turn makes it easier to manage much of the storage complexity.
    """

    databaseChanged = pyqtSignal()
    scanningStateChanged = pyqtSignal(int)

    ITEM_ADDED = 1
    ITEM_MODIFIED = 2
    ITEM_UNCHANGED = 3
    ITEM_DELETED = 4
    ITEM_UNREADABLE = 5

    STATE_FILESYSTEM_SCANNING = 1
    STATE_REGISTRY_SCANNING = 2
    STATE_FILESYSTEM_ROLLBACK = 4
    STATE_REGISTRY_ROLLBACK = 5

    STATE_MERGESCAN_COPYING = 10
    STATE_MERGESCAN_SCANNING = 11
    STATE_MERGEREGISTRYSCAN_COPYING = 12
    STATE_MERGESCAN_UPDATE_INITIAL_STATE = 14
    STATE_MERGESCAN_ROLLBACK = 15

    def __init__(self, filename, echo_sql = False):
        super(PersistentScanningState, self).__init__()

        self.filename = filename
        self.isScanning = False
        logger.info("opened up persistent database at: {0}".format(self.filename))

        self.session = setup_alchemy_on(self, self.filename, echo_sql=echo_sql)

        self.info = self.session.query(GeneralInfo).get(1)
        if self.info is None:
            self.info = GeneralInfo()
            self.info.date_created = datetime.now()
            self.info.merge_complete = False
            self.info.files_scanned = 0
            self.info.files_merged = 0
            self.info.reg_entry_scanned = 0
            self.info.reg_entry_merged = 0
            self.session.add(self.info)
        self.session.commit()

        self.__changing_checked_state = 0

    def __del__(self):
        self.session.commit()

    def scanInfo(self):
        return self.info

    def clearMergeCompleteFlag(self):
        self.info.merge_complete = 0
        self.info.files_merged = 0
        self.info.reg_entry_merged = 0

    def fireDatabaseChangedEvent(self):
        self.databaseChanged.emit()

    def incChangingCheckedState(self):
        self.__changing_checked_state += 1
        return self.isChangingCheckedState()

    def decChangingCheckedState(self):
        self.__changing_checked_state -= 1
        return self.isChangingCheckedState()

    def isChangingCheckedState(self):
        return self.__changing_checked_state is not 0
    
    def storeSecondRegistryScan(self, reg_scanner):
        """ merge registry changes to : reg_entry_merge """
        self.isScanning = True
        RegistryEntryMerge.__table__.drop(bind=self.engine, checkfirst=True)
        RegistryEntryMerge.__table__.create(bind=self.engine)
        self.info.reg_entry_scanned = 0
        self.info.reg_entry_merged = 0
        self.session.commit() 
        self.scanningStateChanged.emit(PersistentScanningState.STATE_MERGEREGISTRYSCAN_COPYING)
        
        try:
            total_count = 0
            count_added = 0
            self.regListToAdd = []
            merge_count = 0
            
            for reg in reg_scanner.performScan():
                assert reg.key is not None
                registry = self.session.query(RegistryEntrySnapshot).get(reg.key)
                yield reg
                merge=True
                total_count += 1
                
                if "xxx" in reg.key:
                    print "this: ", reg.key, " values: ", reg.values
                if registry == None:
                    flags = PersistentScanningState.ITEM_ADDED
                    checked = Qt.Checked
                    #print "added: ", reg.key, "|| values: ", reg.values
                    
                else:
                    valuesScanned = reg.encodeRegValuesJson()
                    savedValues = registry.values
                    checked = Qt.Unchecked # initialize checked
                    if savedValues != valuesScanned:
                        flags = PersistentScanningState.ITEM_MODIFIED
                        checked = Qt.Checked
                        print "modified: ", reg.key
                    else:
                        merge=True # was False
                        flags = PersistentScanningState.ITEM_UNCHANGED
                        checked = Qt.Unchecked
                        
                        
                if merge == True:
                    #re = RegistryEntryMerge(key_name=reg.key, values=self.encodeRegValuesJson(reg.values), checked=checked, flags=flags, parent_key= reg.parentKey)
                    re = RegistryEntryMerge(key_name=reg.key, values= reg.encodeRegValuesJson(), checked=checked, flags=flags, parent_key= reg.parentKey)
                    self.session.add(re)
                    merge_count += 1
                    count_added += 1
                if count_added > 1000:
                    self.session.commit()
                    count_added = 0
            
            self.info.reg_entry_scanned = total_count
            self.info.reg_entry_merged = merge_count
            self.session.commit()

            # find the deleted keys:
            self.session.execute("INSERT into reg_entry_merge (key_name, checked, flags, parent_key) SELECT key_name, '0', '4', parent_key FROM reg_entry_snapshot WHERE key_name NOT IN (SELECT key_name FROM reg_entry_merge)")
            self.session.commit()
            
            self.__updateInitialCheckedState("registryScan")
        except:
            self.scanningStateChanged.emit(PersistentScanningState.STATE_REGISTRY_ROLLBACK)
            self.session.rollback()
        

        
    def storeRegistryEntrySnapshot(self, reg_scanner):
        self.isScanning = True
        RegistryEntrySnapshot.__table__.drop(bind=self.engine, checkfirst=True)
        RegistryEntrySnapshot.__table__.create(bind=self.engine)
        self.info.reg_entry_scanned = 0

        self.session.commit()
        
        try:
            self.scanningStateChanged.emit(PersistentScanningState.STATE_REGISTRY_SCANNING)
            total_count = 0
            count_added = 0
           
            for reg in reg_scanner.performScan():
                # reg is instance of : RegistryInfo
                assert reg.key is not None
                #print  "values: ", reg.values
                
                re = RegistryEntrySnapshot(key_name=reg.key, values=reg.encodeRegValuesJson(), parent_key= reg.parentKey)
                self.session.add(re)
                total_count += 1
                count_added += 1
                if count_added > 1000:
                    self.session.commit()
                    count_added = 0
                yield re

            self.info.reg_entry_scanned = total_count
            self.session.commit()

        except StopScanningException:
            self.scanningStateChanged.emit(PersistentScanningState.STATE_REGISTRY_ROLLBACK)
            self.session.rollback()
        
        self.isScanning = False
     

    def encodeRegValuesJson(self, values):
        encodedvalues = []
        x = ()
        for v in values:
            if isinstance(v[1], str): 
                x = (v[0], base64.b64encode(v[1]), v[2] )
            else: 
                x = v
        encodedvalues.append(x)
        obj = json.dumps(encodedvalues)
        return obj
    
    def storeFilesystemSnapshot(self, directory_scanner):
        self.isScanning = True

        FileSystemSnapshot.__table__.drop(bind=self.engine, checkfirst=True)
        FileSystemSnapshot.__table__.create(bind=self.engine)

        self.info.files_scanned = 0
        self.clearMergeCompleteFlag()

        self.session.commit()

        try:
            self.scanningStateChanged.emit(PersistentScanningState.STATE_FILESYSTEM_SCANNING)

            # for every item in the list stuff it into the table and we're done
            self.storePathsBeingScanned(directory_scanner.pathsForScanning())

            total_count = 0
            count_added = 0

            sp_info = [ PathInfo(p) for p in directory_scanner.pathsForScanning() ]
            for info in sp_info:
                assert info.abs_path is not None
                fs = FileSystemSnapshot(abs_path=ensure_unicode(info.abs_path), is_dir=info.is_dir, path_info=info.to_json(), parent_key=ensure_unicode(info.parentpath))
                self.session.add(fs)
                total_count += 1
                yield fs

            for info in directory_scanner.performScan():
                assert info.abs_path is not None
                fs = FileSystemSnapshot(abs_path=ensure_unicode(info.abs_path), is_dir=info.is_dir, path_info=info.to_json(), parent_key=ensure_unicode(info.parentpath))
                self.session.add(fs)
                total_count += 1
                count_added += 1
                if not self.isScanning:
                    raise StopScanningException()
                yield fs

                # just so we don't blow up the machine's RAM... commit each chunk now and then...
                if count_added > 1000:
                    self.session.commit()
                    count_added = 0

            self.info.files_scanned = total_count
            self.session.commit()
        except StopScanningException:
            self.scanningStateChanged.emit(PersistentScanningState.STATE_FILESYSTEM_ROLLBACK)
            self.session.rollback()

        self.isScanning = False

    def commonPrefix(self):
        return os.path.commonprefix(path for path, checked, flags in self.uniqueDirectories())

    def countUniqueDirectories(self):
        return self.session.query(FileSystemMerge.abs_path).filter(FileSystemMerge.is_dir==True).count()

    def uniqueDirectories(self):
        """Returns the abs_path, checked state and flags value for each of the directories, ordered by length(abs_path) ASC"""
        query = self.session.query(FileSystemMerge.abs_path, FileSystemMerge.checked, FileSystemMerge.flags).filter(FileSystemMerge.is_dir==True).order_by(func.length(FileSystemMerge.abs_path))
        for result in query:
            yield result.abs_path, result.checked, result.flags

    def storePathsBeingScanned(self, paths_to_scan):
        ScannedPath.__table__.drop(bind=self.engine, checkfirst=True)
        ScannedPath.__table__.create(bind=self.engine)
        
        for path in paths_to_scan:
            sp = ScannedPath(abs_path=ensure_unicode(path))
            self.session.add(sp)
        
        self.session.commit()

    def pathsBeingScanned(self):
        return self.session.query(ScannedPath).all()

    def roots(self):
        """Simply fetches all the root paths as FileSystemMerge instances, using the pathsBeingScanned call"""
        return [ self.session.query(FileSystemMerge).get(p.abs_path) for p in self.pathsBeingScanned() ]

    def __updateInitialCheckedState(self,model='SystemScan'):
        '''
        Find only the parent_keys for files that are checked, these are the files that have been changed - propagate the
        state of the parent keys up the hierarchy
        '''
        paths_done = set()
        if model == "SystemScan":
            # step1: find all the parent_key values for items that have changed...
            dirs = self.session.query(FileSystemMerge.parent_key).filter(FileSystemMerge.checked==Qt.Checked).group_by(FileSystemMerge.parent_key).order_by(desc(FileSystemMerge.parent_key))
            # step2: find all the FileSystemMerge instances for these parent keys
            parents = self.session.query(FileSystemMerge).filter(FileSystemMerge.abs_path.in_(dirs))
        else:
            parent_of_checked_keys = self.session.query(RegistryEntryMerge.parent_key).filter(RegistryEntryMerge.checked==Qt.Checked).group_by(RegistryEntryMerge.parent_key).order_by(desc(RegistryEntryMerge.parent_key))
            parents = self.session.query(RegistryEntryMerge).filter(RegistryEntryMerge.key_name.in_(parent_of_checked_keys))
  
        # the above two statements isolate only the added/modified parents, we then walk up the hierarchy calculating
        # the Checked state.  if any parent results in a Qt.PartiallyChecked state - then this is automatically propagated
        # instead of re-calculating the state from its children.

        for rec in parents:
            print "parent:::", rec
            parent_path = rec.parent_key
            checked = rec.checked
            #if parent_path in paths_done:
            #    continue
            #paths_done.add(parent_path)
            logger.debug("working out checked state for: {0}".format(parent_path))
            if not self.isScanning:
                raise StopScanningException()

            new_state = rec.checked
            try:
                new_state = rec.checkedState(rec.checked)
            except Exception, e:
                logger.critical("error checking state for parent path: {0}, error: {1}".format(parent_path, e))
                continue
            
            if model != "SystemScan":
                if rec.flags !=  PersistentScanningState.ITEM_MODIFIED:
                    rec.flags = PersistentScanningState.ITEM_MODIFIED
                    
            if new_state != rec.checked and rec.flags != PersistentScanningState.ITEM_UNCHANGED:
                rec.checked = new_state
                
                    

            # if its partially checked, propagate instantly all the way up the hierarchy
            if new_state == Qt.PartiallyChecked:
                while rec.parent is not None and not rec.parent_key in paths_done:
                    rec = rec.parent
                    rec.checked = Qt.PartiallyChecked
                    rec.flags  = PersistentScanningState.ITEM_MODIFIED
                    if model != "SystemScan":
                        paths_done.add(rec.key_name) 
                    else:
                        paths_done.add(rec.abs_path)

    def countScanningResults(self):
        '''Returns the number of files/directories that will be exported from the merge scan'''
        return self.session.query(FileSystemMerge.checked).filter(FileSystemMerge.checked == Qt.Checked).filter(FileSystemMerge.flags != PersistentScanningState.ITEM_DELETED).count()

    def iterateScanningResults(self):
        '''
        Like countScanningResults(), this finds all the items that have a Qt.Checked check state and have not been deleted, and returns
        them as FileSystemMerge instances.
        '''
        query = self.session.query(FileSystemMerge).filter(FileSystemMerge.checked == Qt.Checked).filter(FileSystemMerge.flags != PersistentScanningState.ITEM_DELETED)
        for file_system_merge in query:
            yield file_system_merge

    def iterateRegistrymergeResults(self):
        query = self.session.query(RegistryEntryMerge).filter(RegistryEntryMerge.checked == Qt.Checked) # we want the deleted registries
        for reg in query:
            yield reg
            
    def __prepareForMergeTable(self, push_add, path_info):
        abs_path = ensure_unicode(path_info.abs_path)
    
        # find the path we've just scanned in the merge table, work out if its been changed / added / deleted
        fs = self.session.query(FileSystemSnapshot).get(abs_path)
        json_text = path_info.to_json()
        parent_path = ensure_unicode(path_info.parentpath)

        # if it was not found, then its been added
        if fs is None:
            flags = PersistentScanningState.ITEM_ADDED
            checked = Qt.Checked
        else:
            fs_json_text = fs.path_info
            flags = PersistentScanningState.ITEM_MODIFIED if json_text != fs_json_text else PersistentScanningState.ITEM_UNCHANGED
            checked = Qt.Checked if flags == PersistentScanningState.ITEM_MODIFIED else Qt.Unchecked
            
            #print "this abs_path: %s" %  abs_path, flags
        #print "***** path: {0} flags: {1} checked: {2}".format(abs_path, flags, checked)
        push_add({'abs_path': abs_path,
                  'is_dir': 1 if path_info.is_dir else 0,
                  'path_info': json_text,
                  'flags': flags,
                  'checked': checked,
                  'parent_key': parent_path})

    def __flushAddQueueToDatabase(self):
        if len(self.add_list) == 0:
            return
        ins = FileSystemMerge.__table__.insert()
        self.session.connection().execute(ins, self.add_list)
        self.info.files_merged += len(self.add_list)
        self.add_list = []

 
        
    def storeSecondScan(self, directory_scanner):
        """
        Another scan is being performed, which needs to be integrated into the pre-scanned result set.  Each scan is
        checked against the existing database records, in order to create the added/modified/deleted flag.  This method
        returns a generator that punts out the very same object produced by the input generator - namely a PathInfo instance.
        """
        self.isScanning = True

        # take a copy of the file_system_snapshot table, first dump and re-create the file_system_merge table - the schema parts are
        # done using SQLAlchemy, but its way too slow for the rest of the work - which is done using the sqlite3 module
        # directly.
        FileSystemMerge.__table__.drop(bind=self.engine, checkfirst=True)
        FileSystemMerge.__table__.create(bind=self.engine)

        self.info.date_last_scanned = datetime.now()
        self.clearMergeCompleteFlag()

        self.scanningStateChanged.emit(PersistentScanningState.STATE_MERGESCAN_COPYING)

        self.add_list = []
        add_callable = lambda x: self.add_list.append(x)

        try:
            paths = [ PathInfo(p.abs_path) for p in self.pathsBeingScanned() ]

            # add each of the scan paths into the FileSystemMerge table, without marking them as modified etc
            for path_info in paths:
                self.__prepareForMergeTable(add_callable, path_info)
                yield path_info

            # now add each of the paths handed to us from the iterator, they are all PathInfo instances - and are converted into an 'INSERT'
            # for the FileSystemMerge table - which happens in batches to make use of executemany() - and bypass the ORM cos its a woof woof.
            for path_info in directory_scanner.performScan():
                self.__prepareForMergeTable(add_callable, path_info)

                if not self.isScanning:
                    raise StopScanningException()

                if len(self.add_list) > 1000:
                    self.__flushAddQueueToDatabase()

                yield path_info

            self.__flushAddQueueToDatabase()

            # to work out which records have been deleted, simply find the abs_path entries NOT in the FileSystemMerge table,
            # and copy them over as PersistentScanningState.ITEM_DELETED
            self.session.execute("INSERT into file_system_merge (abs_path, is_dir, path_info, flags, checked, parent_key) SELECT abs_path, is_dir, path_info, '4', '0', parent_key FROM file_system_snapshot WHERE abs_path NOT IN (SELECT abs_path FROM file_system_merge)")
            self.session.commit()

            self.scanningStateChanged.emit(PersistentScanningState.STATE_MERGESCAN_UPDATE_INITIAL_STATE)
            self.__updateInitialCheckedState()

            self.info.merge_complete = True
            self.session.commit()

        except StopScanningException:
            self.scanningStateChanged.emit(PersistentScanningState.STATE_MERGESCAN_ROLLBACK)

__author__ = 'john'

from fsevents import Observer, Stream
import pyfsevents, threading

def callback(thePath):
    print "the path changed is:" + str(thePath)
    
def callback2(thePath, recursive):
    print "the path changed is:" + str(thePath)

class FSEventsScanner:
    """
    Runs Ok, as long as you have MacFSEvents installed - but does not catch changes to the permissions nor uid/gid
    """
    def __init__(self):
        self.paths = []
        self.observer = Observer()
        self.stream = None

    def addPathToListenForChangesOn(self, thePath):
        print "added path:" + thePath
        self.paths.append(thePath)

    def startListening(self):
        self.observer.start()
        self.stream = Stream(callback, *self.paths, file_events=True)
        self.observer.schedule(self.stream)

class FSEventsScanner2:
    """
    Uses a different impl of Mac FS events, and only reports the top level directory - not so suitable
    """
    def __init__(self):
        self.paths = []

    def addPathToListenForChangesOn(self, thePath):
        self.paths.append(thePath)

    def startListening(self):
        for p in self.paths:
            pyfsevents.registerpath(p, callback2)
        pyfsevents.listen()

if __name__ == "__main__":
    f = FSEventsScanner()
    f.addPathToListenForChangesOn("/Users/john/Desktop")
    f.addPathToListenForChangesOn("/Users/john/Documents")
    f.startListening()
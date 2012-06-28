from PyQt4.Qt import *
from PyQt4.Qt import QObject
from lib.directory_scanner import DirectoryScanner
from lib.document_storage import DocumentStorage
from lib.persistent_scanning_state import PersistentScanningState, ensure_unicode
from lib.registry_scanner import RegistryScanner
class ScanningController(QObject):
    scanStarted = pyqtSignal(str)
    scanProgress = pyqtSignal(int, str)
    scanStateChanged = pyqtSignal(int)
    scanFinished = pyqtSignal(int)
    mergeCompleted = pyqtSignal()

    def __init__(self):
        super(QObject, self).__init__()
        self.document = None
        self.isScanning = True
        self.storage = None

    def stopScanning(self):
        self.isScanning = False
        if self.storage is not None:
            self.storage.isScanning = False

    def beginInitialScan(self, scan_paths, doc_name = None):
        # construct an initial scan, based on the selected items within the model...
        # workflow: scan to produce a persistent model, monitor/rescan, re-integrate changes into initial model (changed, deleted, added etc)
        scanner = DirectoryScanner()
        scanner.addPathsForScanning(scan_paths)

        # we want to store the results too - so build a storage device, its all being run via iterables
        # so its easy to chain these together.
        doc_path = DocumentStorage.getDocumentPathForName(doc_name, scan_paths)

        self.storage = PersistentScanningState(doc_path)
        self.storage.storePathsBeingScanned(scanner.paths_to_scan)
        self.storage.scanningStateChanged.connect(lambda x: self.scanStateChanged.emit(x))

        self.isScanning = True
        self.scanStarted.emit(doc_path)

        # this one line performs a recursive disk scan on multiple folders, obtains file/dir info, persists
        # this to the DB and then finally exposes [idx, f] so the UI can display progress.  Long live iterables... (and C++, you can die in a fire)
        total_found = 0
        for idx, f in enumerate(self.storage.storeFilesystemSnapshot(scanner)):
            total_found = idx
            if not (idx % 100):
                self.scanProgress.emit(idx, f.abs_path)
            if not self.isScanning:
                break
         
        
        registryScanner = RegistryScanner()
        totalRegistry = 0
        for idx ,r in enumerate(self.storage.storeRegistryEntrySnapshot(registryScanner)):
            totalRegistry = idx
            if not (idx % 100):
                self.scanProgress.emit(idx, r.key_name)
               
            if not self.isScanning:
                break
        
        self.stopScanning()

        # complete the scan...
        self.scanFinished.emit(total_found)

        self.storage = None

    def beginChangesScan(self, doc_name):
        """
        Find the selected item, and use the directories inside to perform a scan, the merge the results of that
        with the existing document - forming a set of objects that have been added/changed/removed
        """
        # now fetch the data model for that one to get the paths that need to be scanned
        self.storage = PersistentScanningState(DocumentStorage.documentFullPath(doc_name))
        #return self.__beginChangesScanWithDocument()
        self.__beginChangesScanWithDocument()

    def __beginChangesScanWithDocument(self):
        scan_paths = [ p.abs_path for p in self.storage.pathsBeingScanned() ]

        # kick off another scan
        scan = DirectoryScanner()
        scan.addPathsForScanning(scan_paths)

        self.scanStarted.emit(self.storage.filename)

        # now re-scan, we'll use a 'merge' facility from the persistent scanning state, it automatically
        # creates the required set of (added, modified, deleted) files.
        total_found = 0
        merge = self.storage.storeSecondScan(scan)
        for idx, f in enumerate(merge):
            total_found = idx
            #yield idx, f
            if not (idx % 100):
                self.scanProgress.emit(idx, ensure_unicode(f.abs_path))
            if not self.isScanning:
                break
        
        total_found = 0
        
        registryScanner = RegistryScanner()
        for idx, r in enumerate(self.storage.storeSecondRegistryScan(registryScanner)):
            total_found = idx
            if not (idx % 100):
                self.scanProgress.emit(idx, ensure_unicode(r.key))
            if not self.isScanning:
                break
            
        self.scanFinished.emit(total_found)

        self.mergeCompleted.emit()

        self.stopScanning()

        self.storage = None

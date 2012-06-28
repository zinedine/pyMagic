from PyQt4.Qt import *
from lib.scanning_controller import ScanningController

class ScanningControllerThread(QThread):
    scanStarted = pyqtSignal(str)
    scanProgress = pyqtSignal(int, str)
    scanFinished = pyqtSignal(int)
    scanStateChanged = pyqtSignal(int)
    mergeCompleted = pyqtSignal()

    def __init__(self, first_scan, doc_name):
        super(ScanningControllerThread, self).__init__()
        self.document_name = doc_name
        self.scan_paths = []
        self.first_scan = first_scan

    def stopScanning(self):
        self.scanner.stopScanning()
        self.wait()

    def run(self):
        # simply encapsulates the ScanningController, re-routing all its signals across the thread boundary
        self.scanner = ScanningController()
        self.scanner.scanStarted.connect(lambda x: self.scanStarted.emit(x))
        self.scanner.scanProgress.connect(lambda n, p: self.scanProgress.emit(n, p))
        self.scanner.scanFinished.connect(lambda x: self.scanFinished.emit(x))
        self.scanner.scanStateChanged.connect(lambda x: self.scanStateChanged.emit(x))
        self.scanner.mergeCompleted.connect(lambda: self.mergeCompleted.emit())

        if self.first_scan:
            self.scanner.beginInitialScan(self.scan_paths, self.document_name)
        else:
            #itr = self.scanner.beginChangesScan(self.document_name)
            self.scanner.beginChangesScan(self.document_name)
            #for x in itr:
            #    pass

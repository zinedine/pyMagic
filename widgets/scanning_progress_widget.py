
from PyQt4.Qt import *
from lib.persistent_scanning_state import PersistentScanningState
from lib.scanning_controller_thread import ScanningControllerThread
from ui.scanning_progress import Ui_ScanningProgress
from lib.document_storage import DocumentStorage
import logging
logger = logging.getLogger(__name__)

class ScanningProgressWidget(QWidget):
	def __init__(self, first_scan = True, parent = None):
		super(ScanningProgressWidget, self).__init__(parent)

		self.ui = Ui_ScanningProgress()
		self.ui.setupUi(self)
		self.scanner = None
		self.first_scan = first_scan

	def __del__(self):
		if self.scanner is not None:
			self.scanner.stopScanning()

	def beginScan(self, document_name, scan_paths, callableWhenDone = None):
		self.ui.labelProgressText.setText("")

		# kick off a scan of certain paths
		self.scanner = ScanningControllerThread(self.first_scan, document_name)
		self.scanner.scanStarted.connect(self.onScanStarted)
		self.scanner.scanProgress.connect(self.onScanProgress)
		self.scanner.scanFinished.connect(self.onScanFinished)
		self.scanner.scanStateChanged.connect(self.onScanStateChanged)

		if self.first_scan:
			self.scanner.scan_paths = scan_paths

		self.document_name = document_name
		self.scanner.finished.connect(self.onThreadFinished)

		if callableWhenDone is not None:
			self.scanner.finished.connect(callableWhenDone)

		logger.debug("ScanningProgressWidget - kicking off a scan")
		self.scanner.start()

	def cleanupScan(self):
		if self.scanner is not None:
			self.scanner.stopScanning()
			if self.first_scan:
				DocumentStorage.deleteDocumentNamed(self.document_name)
			logger.debug("Scanner stopped and was reset")
		self.scanner = None

	def onThreadFinished(self):
		self.scanner = None

	def cleanupPage(self):
		logger.debug("ScanningProgressWidget, cleanupPage")
		self.cleanupScan()

	def __setProgressText(self, normal_text, counter_text = ""):
		self.ui.labelProgressText.setText(normal_text)
		self.ui.labelProgressCount.setText(counter_text)

	def onScanStateChanged(self, new_state):
		if new_state == PersistentScanningState.STATE_FILESYSTEM_SCANNING:
			self.__setProgressText("Setting up the initial scan")
		elif new_state == PersistentScanningState.STATE_MERGESCAN_SCANNING:
			self.__setProgressText("Setting up the second scan")
		elif new_state == PersistentScanningState.STATE_MERGESCAN_COPYING:
			self.__setProgressText("Scanning and comparing paths...")
		elif new_state == PersistentScanningState.STATE_MERGESCAN_UPDATE_INITIAL_STATE:
			self.__setProgressText("Updating the initial checked state of the added / modified items")

	def onScanStarted(self, new_doc_name):
		pass

	def onScanFinished(self, total_found):
		t = "%d" % total_found
		self.ui.labelProgressText.setText(t)

	def onScanProgress(self, number_found, path_name):
		self.__setProgressText(path_name, format(number_found, ',d'))


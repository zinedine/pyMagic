
from PyQt4.Qt import *
from widgets.scanning_progress_widget import ScanningProgressWidget

class ScanningProgressWizpage(QWizardPage, ScanningProgressWidget):
	def __init__(self, first_scan = True):
		super(ScanningProgressWizpage, self).__init__(self)
		self.first_scan = first_scan

		self.setTitle("Scanning the disk...")
		self.setButtonText(QWizard.BackButton, "Cancel Scan")

	def initializePage(self):
		self.beginScan(self.wizard().documentName(), self.wizard().scanPaths())

	def onThreadFinished(self):
		super(ScanningProgressWizpage, self).onThreadFinished()
		self.completeChanged.emit()

	def cleanupPage(self):
		self.cleanupScan()
		super(ScanningProgressWizpage, self).cleanupPage()

	def onScanStarted(self, new_doc_name):
		self.completeChanged.emit()

	def onScanFinished(self, total_found):
		super(ScanningProgressWizpage, self).onScanFinished(total_found)
		self.completeChanged.emit()
		self.wizard().next()

	def isComplete(self):
		return self.scanner == None


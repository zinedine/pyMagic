
import sip
sip.setapi('QString', 2)

import sys
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QApplication, QHeaderView, QWidget
from lib.directory_scanner import DirectoryScanner
from lib.merge_scan_tree_model import MergeScanTreeModel, MergeScanMapper
from lib.persistent_scanning_state import PersistentScanningState
from lib.platform import Platform
from spike.CustomTreeWidget import Ui_CustomTreeWidget

class Widget(QWidget):
	def __init__(self, owner = None):
		super(Widget, self).__init__(owner)

		# make up a doc
		self.t = DirectoryScanner()
		if Platform.isMac:
			self.t.addPathsForScanning(['/Applications'])
		else:
			self.t.addPathsForScanning(['C:\\Program Files'])

		self.p = PersistentScanningState("demo.sqlite", echo_sql=False)

		self.initialScan()
		self.mergeScan()

		print "Info Is:", self.p.scanInfo()

		self.mapper = MergeScanMapper(self.p)

		self.ui = Ui_CustomTreeWidget()
		self.ui.setupUi(self)
		self.ui.treeView.setModel(MergeScanTreeModel(self.p, self.mapper, self.p.roots(), self))
		self.ui.treeView.expandToDepth(1)

		model = self.ui.treeView.model()
		header = self.ui.treeView.header()
		header.setResizeMode(MergeScanTreeModel.COL_CHECKED, QHeaderView.ResizeToContents)
		header.setResizeMode(MergeScanTreeModel.COL_PERMISSIONS, QHeaderView.ResizeToContents)

		self.ui.treeView.setAttribute(Qt.WA_MacShowFocusRect, False)

	def initialScan(self):
		for value in self.p.storeFilesystemSnapshot(self.t):
			pass

	def mergeScan(self):
		for value in self.p.storeSecondScan(self.t):
			pass

def run_ui(args):
	app = QApplication(sys.argv)
	wid = Widget()
	wid.show()
	wid.raise_()
	app.exec_()

if __name__ == "__main__":
	run_ui(sys.argv)

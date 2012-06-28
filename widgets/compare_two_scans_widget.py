import os

from lib.document_storage import DocumentStorage
from lib.merge_scan_tree_model import MergeScanTreeModel, MergeScanMapper
from lib.registry_merge_scan_tree_model import mergedRegistryTreeModel, MergedRegistryMapper
from lib.registry_scanner import HIVES
from lib.persistent_scanning_state import PersistentScanningState
from lib.platform import Platform
from lib.ui_helpers import ListWidgetDeleting, showInFinder
from ui import compare_two_scans

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QWizardPage, QMenu, QAction, QHeaderView, QDialog
from widgets.constants import WizardPage

from widgets.scanning_progress_widget import ScanningProgressWidget

import logging
logger = logging.getLogger(__name__)

class CompareTwoScansWidget(QWizardPage, ListWidgetDeleting):
	VIEW_MASK_ADDED = 1
	VIEW_MASK_MODIFIED = 2
	VIEW_MASK_REMOVED = 4
	VIEW_MASK_UNCHANGED = 8
	VIEW_MASK_ALL_CHECKED  = 16
	VIEW_MASK_ALL = 31
	VIEW_MASK_ONLY_CHECKED = 32
	VIEW_MASK_ONLY_UNCHECKED = 64

	def __init__(self):
		super(QWizardPage, self).__init__()
		super(ListWidgetDeleting, self).__init__()

		self.ui = compare_two_scans.Ui_compare_two_scans()
		self.ui.setupUi(self)

		self.actionShowInFinder = QAction("Show in Finder" if Platform.isMac else "Show in Explorer", self)
		self.actionShowInFinder.triggered.connect(self.__onShowInFinder)
		self.actionCheckSelected = QAction("Check all Selected", self)
		self.actionCheckSelected.triggered.connect(lambda: self.__onCheckSelectionViaContextMenu(Qt.Checked))
		self.actionUnCheckSelected = QAction("Uncheck all Selected", self)
		self.actionUnCheckSelected.triggered.connect(lambda: self.__onCheckSelectionViaContextMenu(Qt.Unchecked))

		self.menu = QMenu()
		self.menu.addAction(self.actionShowInFinder)
		self.menu.addSeparator()
		self.menu.addAction(self.actionCheckSelected)
		self.menu.addAction(self.actionUnCheckSelected)

		self.ui.checkBoxAdded.stateChanged.connect(self.__onStateFilteringChanged)
		self.ui.checkBoxChanged.stateChanged.connect(self.__onStateFilteringChanged)
		self.ui.checkBoxNotChanged.stateChanged.connect(self.__onStateFilteringChanged)
		self.ui.checkBoxRemoved.stateChanged.connect(self.__onStateFilteringChanged)
		self.ui.comboFiltering.currentIndexChanged.connect(self.__onStateFilteringChanged)

		# I added this because I was concerned that it took too many clicks on the checkbox to change its state
		#self.ui.tableView.setAttribute(Qt.WA_MacNoClickThrough, True)
		self.setTitle("Comparison and Package Preparation")

		self.ui.searchLineEdit.textChanged.connect(self.__onFilterTextChanged)
		self.ui.buttonRescan.clicked.connect(self.__onRescanClicked)

		# the current document name being shown
		self.document = None
		# the current path that is used to show a subset of the items in this document, this path is modified by
		# the user clicked in the 'tree widget' view.  The path is then added to an SQL expression filter that
		# is used to restrict the items shown in the table view.
		self.filter_abs_path = ''
		# the current filter text is stored here (so it can be re-applied), this text is a copy of whatever is
		# being typed into the search filter QLineEdit instance
		self.filter_text = ''
		# the current filter mask
		self.filter_mask = CompareTwoScansWidget.VIEW_MASK_ALL

		self.ui.treeView.customContextMenuRequested.connect(self.__onCustomContextMenu)

	def initializePage(self):
		name_of_file = self.wizard().documentName()
		self.__refreshResultsUsingDocument(PersistentScanningState(DocumentStorage.documentFullPath(name_of_file)))

		self.wizard().removePage(WizardPage.CREATE_NEW)
		self.wizard().removePage(WizardPage.FIRST_SCAN_PROGRESS)
		self.wizard().removePage(WizardPage.SECOND_SCAN_PROGRESS)
		self.wizard().removePage(WizardPage.SCANNING_COMPLETE_INSTALL_NOW)

		self.wizard().reinsertCreateScanPage()

	def __onCustomContextMenu(self, pos):
		indexes = self.ui.treeView.selectionModel().selectedRows()
		self.actionShowInFinder.setEnabled(len(indexes) == 1)
		self.menu.popup(self.ui.treeView.mapToGlobal(pos))

	def __onShowInFinder(self, action):
		indexes = self.ui.treeView.selectionModel().selectedRows()
		if len(indexes):
			first_index = indexes[0]
			ms = self.model.mergeScanForIndex(first_index)
			if ms is not None:
				showInFinder(ms.abs_path)

	def __onCheckSelectionViaContextMenu(self, check_state):
		"""
		This is called when the right-click contextual menu fires a check or uncheck selection event - we just modify
		the checked state of the selected rows
		"""
		indexes = self.ui.treeView.selectedIndexes()
		for idx in indexes:
			# find the object, and change its checked state
			ms = self.model.mergeScanForIndex(idx)
			if ms is not None and ms.checked != check_state:
				self.model.setCheckedStateForMergeScan(ms, check_state)

	def __onStateFilteringChanged(self, new_state):
		"""
		This filtering method is called when one of the state-type radio buttons is clicked.  The idea is to restrict the rows
		to those that match either the added/modified/deleted flags.
		"""
		new_mask = 0

		if self.ui.checkBoxAdded.checkState() == Qt.Checked:
			new_mask += CompareTwoScansWidget.VIEW_MASK_ADDED
		if self.ui.checkBoxChanged.checkState() == Qt.Checked:
			new_mask += CompareTwoScansWidget.VIEW_MASK_MODIFIED
		if self.ui.checkBoxRemoved.checkState() == Qt.Checked:
			new_mask += CompareTwoScansWidget.VIEW_MASK_REMOVED
		if self.ui.checkBoxNotChanged.checkState() == Qt.Checked:
			new_mask += CompareTwoScansWidget.VIEW_MASK_UNCHANGED

		if self.ui.comboFiltering.currentIndex() == 1:
			new_mask += CompareTwoScansWidget.VIEW_MASK_ONLY_CHECKED
		if self.ui.comboFiltering.currentIndex() == 2:
			new_mask += CompareTwoScansWidget.VIEW_MASK_ONLY_UNCHECKED

		self.filter_mask = new_mask
		self.__resetFilterCondition()

	def __rescanFinished(self):
		self.rescan_dlg.accept()
		self.rescan_dlg = None

	def __onRescanClicked(self):
		if not hasattr(self, 'document'):
			return

		# run a scan again in the background, throw up a dialog (modal) to keep track
		self.rescan_dlg = QDialog(self.wizard())
		self.rescan_dlg.setWindowFlags(Qt.Sheet)

		progress_widget = ScanningProgressWidget(False, parent = self.rescan_dlg)

		filename = self.document.filename

		scan_paths = [ p.abs_path for p in self.document.pathsBeingScanned() ]
		progress_widget.beginScan(filename, scan_paths, callableWhenDone=self.__rescanFinished)

		self.rescan_dlg.open()

	def __onFilterTextChanged(self, new_text):
		self.filter_text = new_text
		self.__resetFilterCondition()

	def __addToFlagsSet(self, flags_set, flag_value):
		if len(flags_set) > 0:
			flags_set += ", "
		flags_set += str(flag_value)
		return flags_set

	def __resetFilterCondition(self):
		if not hasattr(self, 'model'):
			return

		# build the entire condition, it is drive by the filter_abs_path (which may be null/zero len) and the filter_text

		flags_set = ""

		if self.filter_mask & CompareTwoScansWidget.VIEW_MASK_ADDED:
			flags_set = self.__addToFlagsSet(flags_set, PersistentScanningState.ITEM_ADDED)

		if self.filter_mask & CompareTwoScansWidget.VIEW_MASK_MODIFIED:
			flags_set = self.__addToFlagsSet(flags_set, PersistentScanningState.ITEM_MODIFIED)

		if self.filter_mask & CompareTwoScansWidget.VIEW_MASK_REMOVED:
			flags_set = self.__addToFlagsSet(flags_set, PersistentScanningState.ITEM_DELETED)

		if self.filter_mask & CompareTwoScansWidget.VIEW_MASK_UNCHANGED:
			flags_set = self.__addToFlagsSet(flags_set, PersistentScanningState.ITEM_UNCHANGED)

		filter = "is_dir = 'false' AND flags IN ({}) ".format(flags_set)
		#filter = " flags IN ({}) ".format(flags_set)

		if self.filter_mask & CompareTwoScansWidget.VIEW_MASK_ONLY_UNCHECKED:
			filter += "AND checked = {}".format(Qt.Unchecked)
		elif self.filter_mask & CompareTwoScansWidget.VIEW_MASK_ONLY_CHECKED:
			filter += "AND checked = {}".format(Qt.Checked)

		if len(self.filter_abs_path) > 0:
			filter += " AND abs_path LIKE '{}{}%'".format(self.filter_abs_path.encode("utf-8"), os.path.sep)

		if len(self.filter_text) > 0:
			filter += " AND (abs_path LIKE '%{}%' OR path_info LIKE '%{}%')".format(self.filter_text, self.filter_text)

		logger.debug("re-filtering text expression to: {0}".format(filter))
		#self.model.setFilter(filter)

	def __refreshResultsUsingDocument(self, doc):
		self.document = doc
		#self.document.databaseChanged.connect(self.__resetFilterCondition)
		
		mapper = MergeScanMapper(doc) 
		self.model = MergeScanTreeModel(doc, mapper, doc.roots(), self)
		self.ui.treeView.setModel(self.model)
		
		#self.model.checkStateChanged.connect(self.__onCheckSelectionHasChanged)

		registryMapper = MergedRegistryMapper(doc)
		self.registryModel = mergedRegistryTreeModel(doc, registryMapper, HIVES , self)
		self.ui.regView.setModel(self.registryModel)
		
		header = self.ui.treeView.header()
		header.setResizeMode(MergeScanTreeModel.COL_CHECKED, QHeaderView.ResizeToContents)
		header.setResizeMode(MergeScanTreeModel.COL_PERMISSIONS, QHeaderView.ResizeToContents)

#		# adjust column 0 in the table header
#		header = self.ui.treeView.header()
#		header.setSortIndicator(QueryModel.COL_ABSPATH, Qt.AscendingOrder)
#		model.setSort(PersistentScanningState.DBCOL_MERGE_ABS_PATH, Qt.AscendingOrder)
#
#		header.setResizeMode(QueryModel.COL_CHECKED, QHeaderView.Fixed)
#		header.setResizeMode(QueryModel.COL_ICON, QHeaderView.Fixed)
#		header.setResizeMode(QueryModel.COL_ABSPATH, QHeaderView.ResizeToContents)
#		header.resizeSection(QueryModel.COL_CHECKED, 45)
#		header.resizeSection(QueryModel.COL_ICON, 45)

		self.ui.treeView.setAttribute(Qt.WA_MacShowFocusRect, False)

		# clear existing search string
		self.ui.searchLineEdit.setText("")
		self.__resetFilterCondition()


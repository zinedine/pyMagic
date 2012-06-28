from PyQt4.QtCore import QSettings, Qt
from PyQt4.QtGui import QWidget, QDialogButtonBox, QStandardItemModel, QStandardItem, QItemSelectionModel, QMessageBox
import sys
from lib.exclusion_rules import ExclusionRules
from lib.platform import Platform
from lib.ui_helpers import ListWidgetDeleting
from ui.preferences import Ui_Preferences
import logging
logger = logging.getLogger(__name__)

class PreferencesWidget(QWidget, ListWidgetDeleting):
	def __init__(self, widget = None, exclusion_rules = None):
		super(PreferencesWidget, self).__init__(widget)
		self.ui = Ui_Preferences()
		self.ui.setupUi(self)

		if exclusion_rules == None:
			exclusion_rules = ExclusionRules()

		self.ui.buttonBox.clicked.connect(self.__onButtonClicked)
		self.ui.buttonBox.button(QDialogButtonBox.Ok).setText("Save")

		self.ui.addFileButton.clicked.connect(self.__onAddFile)
		self.ui.addDirButton.clicked.connect(self.__onAddDir)
		self.ui.addRegButton.clicked.connect(self.__onAddReg)

		self.ui.deleteFileButton.clicked.connect(lambda: self.__removeSelectedItems(self.ui.treeViewFiles))
		self.ui.deleteDirButton.clicked.connect(lambda: self.__removeSelectedItems(self.ui.treeViewDirs))
		self.ui.deleteRegButton.clicked.connect(lambda: self.__removeSelectedItems(self.ui.treeViewReg))
		self.ui.lblExpressionHintLink.linkActivated.connect(self.__onHelpLinkActivated)

		if not Platform.isWindows:
			self.ui.tabWidget.removeTab(2)

		self.rules = exclusion_rules

	def __onHelpLinkActivated(self, the_link):
		# ignore the link, show the help page
		logger.info("TODO: implement a QtHelp based document")
		
	def __loadRules(self, the_rules, tree_view):
		model = QStandardItemModel(self)
		for r in the_rules:
			item = QStandardItem(r)
			model.appendRow(item)
		model.setHeaderData(0, Qt.Horizontal, "Regular Expression")
		tree_view.setModel(model)

	def __saveRules(self, tree_view, set_method):
		temp_rules = []
		model = tree_view.model()

		for row in range(model.rowCount()):
			item = model.item(row)
			temp_rules.append(item.text())
		set_method(temp_rules)

	def __loadPreferences(self):
		# grab the list of each of the rules and populate the dialogs
		self.__loadRules(self.rules.fileExcludes(), self.ui.treeViewFiles)
		self.__loadRules(self.rules.dirExcludes(), self.ui.treeViewDirs)
		self.__loadRules(self.rules.registryExcludes(), self.ui.treeViewReg)
		settings = QSettings()
		curr_tab = settings.value("preferences_currtab", 0).toInt()
		self.ui.tabWidget.setCurrentIndex(curr_tab[0])
	
	def __savePreferences(self):
		self.__saveRules(self.ui.treeViewFiles, lambda x: self.rules.setFileExcludes(x))
		self.__saveRules(self.ui.treeViewDirs, lambda x: self.rules.setDirExcludes(x))
		if sys.platform.startswith("win"):
			self.__saveRules(self.ui.treeViewReg, lambda x: self.rules.setRegistryExcludes(x))

	def __removeSelectedItems(self, tree_view):
		toDelete = self.deleteSelectedTreeViewItems(tree_view, "Remove Rules?", "Are you sure you want to remove the selected rules?")
		for itemWidget in toDelete:
			pass

	def __addNewItemTo(self, tree_view, text):
		item = QStandardItem(text)
		tree_view.model().insertRow(0, item)
		tree_view.selectionModel().select(item.index(), QItemSelectionModel.Rows | QItemSelectionModel.Select)

	def __onAddFile(self):
		self.__addNewItemTo(self.ui.treeViewFiles, "<enter new file exclusion expression>")
	def __onAddDir(self):
		self.__addNewItemTo(self.ui.treeViewDirs, "<enter new directory exclusion expression>")
	def __onAddReg(self):
		self.__addNewItemTo(self.ui.treeViewReg, "<enter new registry exclusion expression>")

	def __restoreDefaults(self):
		res = QMessageBox.warning(self, "Restore all Defaults?", "Are you sure that you want to replace your existing expressions for files & directories with the defaults?", QMessageBox.Yes | QMessageBox.Cancel)
		if res == QMessageBox.StandardButton(QMessageBox.Yes):
			self.__loadRules(self.rules.defaultFileExclusionRules(), self.ui.treeViewFiles)
			self.__loadRules(self.rules.defaultDirExclusionRules(), self.ui.treeViewDirs)
			self.__loadRules(self.rules.defaultRegistryExclusionRules(), self.ui.treeViewReg)
			QMessageBox.information(self, "Restoration Complete", "The defaults have been restored")

	def __onButtonClicked(self, button):
		role = self.ui.buttonBox.buttonRole(button)
		if role == QDialogButtonBox.AcceptRole:
			# save preferences and fire close event
			self.__savePreferences()
		if role == QDialogButtonBox.ResetRole:
			self.__restoreDefaults()
			return
		self.close()

	def showEvent(self, evt):
		self.__loadPreferences()

	def closeEvent(self, evt):
		settings = QSettings()
		settings.setValue("preferences_currtab", self.ui.tabWidget.currentIndex())
		super(PreferencesWidget, self).closeEvent(evt)


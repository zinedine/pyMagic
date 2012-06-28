import os, sys
from PyQt4.QtCore import QObject, SIGNAL, Qt, QSettings
from PyQt4.QtGui import QWizardPage, QWizard, QColor, QFileDialog, QMessageBox

from lib.document_storage import DocumentStorage
from lib.platform import Platform
from lib.ui_helpers import ListWidgetDeleting, addNewListItemCalled
from ui.create_new_scan import Ui_CreateNewScan

mac_default_paths = [
	'/',
	'/Applications',
	'/Library',
	'/System',
	'/Users',
]

win_default_paths = [
	'C:\\',
	'C:\\Documents and Settings',
	'C:\\Program Files',
	'C:\\Program Files (x86)',
	'C:\\ProgramData',
	'C:\\Users',
]

def default_paths():
	if Platform.isWindows:
		# TODO: get all the retarded path names that are OS and language specific, throw them in this list and sort alpha
		return [ os.path.normpath(p) for p in win_default_paths ]
	return [ os.path.normpath(p) for p in mac_default_paths ]

class CreateNewScanWidget(QWizardPage, ListWidgetDeleting):
	def __init__(self):
		super(CreateNewScanWidget, self).__init__()

		self.ui = Ui_CreateNewScan()
		self.ui.setupUi(self)
		self.setTitle("Create Scan")
		self.setSubTitle("The list below shows the drives and directories that you can choose to scan.  You can select more than one drive or directory to include in this scan.")
		self.__loadListOfDocuments()

		# required fields
		self.registerField("scanPaths", self)

		self.ui.listWidget.setAttribute(Qt.WA_MacShowFocusRect, False)

		self.ui.addButton.clicked.connect(self.__onAddClicked)
		self.ui.removeButton.clicked.connect(self.__onRemoveClicked)
		self.ui.listWidget.itemSelectionChanged.connect(self.__onListSelectionChanged)

		# make it possible to validate the entered paths (whenever data is changed in the underlying model)
		QObject.connect(self.ui.listWidget.model(), SIGNAL("dataChanged(QModelIndex, QModelIndex)"), self.__validatePaths)
		self.ui.lineEditDocumentName.textChanged.connect(self.__slotDocumentNameChanged)

		self.__validatePaths()

		self.setButtonText(QWizard.NextButton, "Start Scan")

	def __del__(self):
		self.__saveSettings()

	def __validatePaths(self):
		"""
		Iterates all the items in the list and colour them based on their validity, e.g. missing or bad paths
		are coloured red, good paths the normal text colour.
		"""
		for item in self.ui.listWidget.findItems("*", Qt.MatchWildcard):
			path_name = item.data(Qt.DisplayRole).toString()
			if not os.path.exists(path_name):
				color = Qt.red
			else:
				color = Qt.black
			if path_name in default_paths():
				color = Qt.gray
			item.setData(Qt.ForegroundRole, QColor(color))
		self.__saveSettings()

	def __loadListOfDocuments(self):
		"""
		The UI doesn't contain any predefined items in the .ui file - these are based on the platform.  We load these,
		as well as the user-defined directories into the list.  The user-defined items are stored in the QSettings based
		storage.
		"""
		for value in default_paths():
			item = addNewListItemCalled([os.path.normpath(value)], self.ui.listWidget)
			item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
			t = item.font()
			t.setItalic(True)
			item.setFont(t)

		# load up state from storage...
		paths = QSettings().value("paths").toList()
		for value in paths:
			str = os.path.normpath(value.toString())
			if str not in default_paths():
				addNewListItemCalled([str], self.ui.listWidget, mutable=True)

	def __allPaths(self):
		return [item.data(Qt.DisplayRole).toString() for item in self.ui.listWidget.findItems("*", Qt.MatchWildcard)]

	def __saveSettings(self):
		"""
		Writes the current set of user-defined path names into QSettings based storage.
		"""
		the_paths = []
		for str in self.__allPaths():
			if str not in default_paths():
				the_paths.append(str)
		QSettings().setValue("paths", the_paths)

	def __onRemoveClicked(self):
		"""
		Removes the selected items from the view after confirmation
		"""
		results = self.deleteSelectedListWidgetItems(self.ui.listWidget, "Remove Items?", "Are you sure that you want to remove the selected items?")
		# force the iteration... removal from the list is our only goal.
		for item in results:
			pass

	def __onAddClicked(self):
		"""
		Creates a new item in the list and begins editing it.  The item is selected by choosing a directory using the
		file dialog.
		"""
		dir_name = QFileDialog.getExistingDirectory(self, "Select a directory")
		if dir_name is not None:
			theItem = addNewListItemCalled([dir_name], self.ui.listWidget, mutable=True)
			if theItem is not None:
				theItem.setSelected(True)

	def __slotDocumentNameChanged(self):
		self.completeChanged.emit()

	def __onListSelectionChanged(self):
		numSelected = len(self.ui.listWidget.selectedItems())
		if not numSelected:
			self.ui.status.setText("")
		else:
			self.ui.status.setText("%d path%s selected" % (numSelected, '' if numSelected <= 1 else 's'))

		self.ui.lineEditDocumentName.setText(DocumentStorage.getNewDocumentName(self.__scanPaths()))
		self.completeChanged.emit()

	def isComplete(self):
		done = len(self.ui.listWidget.selectedItems()) > 0 and len(self.ui.lineEditDocumentName.text()) > 0
		if done:
			self.wizard().setDocumentName(self.ui.lineEditDocumentName.text())
			self.setField("scanPaths", self.__scanPaths())
		return done

	def __scanPaths(self):
		scan_paths = []
		for item in self.ui.listWidget.selectedItems():
			value = item.data(Qt.DisplayRole).toString()
			if os.path.exists(value):
				scan_paths.append(value)
		return scan_paths

	def __problemPaths(self):
		problem_paths = []
		for item in self.ui.listWidget.selectedItems():
			value = item.data(Qt.DisplayRole).toString()
			if not os.path.exists(value):
				problem_paths.append(value)
		return problem_paths

	def validateCurrentPage(self):
		problem_paths = self.__problemPaths()
		if len(problem_paths) > 0:
			value = "The following paths do not exist on disk: %s\r\n\r\nPlease select only paths that exist and try again" % problem_paths
			QMessageBox.critical(self, "Paths Missing", value, QMessageBox.Cancel)
			return False

		return True


import os
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QWizardPage, QStandardItemModel, QStandardItem, QHeaderView
from lib.document_storage import DocumentStorage
from lib.persistent_scanning_state import PersistentScanningState
from lib.ui_helpers import ListWidgetDeleting
from ui.list_existing_scans import Ui_ListExistingScans
from PyQt4.QtCore import pyqtSignal
import logging
logger = logging.getLogger(__name__)

class ListOfExistingScanFilesWidget(QWizardPage, ListWidgetDeleting):
    loadScanFile = pyqtSignal(str)
    scanFileDeleted = pyqtSignal(str)

    def __init__(self):
        super(QWizardPage, self).__init__()
        super(ListWidgetDeleting, self).__init__()
        self.ui = Ui_ListExistingScans()
        self.ui.setupUi(self)
        self.setTitle("Fileset Magic Scans")
        self.setSubTitle("Below is a list of the previous scans you've made.")
        self.ui.treeView.setAttribute(Qt.WA_MacShowFocusRect, False)
        self.ui.treeView.doubleClicked.connect(self.__onListItemDoubleClicked)
        self.ui.deleteSelectedToolButton.clicked.connect(self.__deleteSelectedItems)

        self.registerField("secondScanComplete", self)

        self.document_name = None

    def __onListItemDoubleClicked(self, index):
        self.__onSelectionChanged(index, None)
        if self.isComplete():
            self.wizard().next()

    def __onSelectionChanged(self, current, previous):
        # find selected item - grab its document name
        name = current.data(Qt.DisplayRole).toString()
        logger.debug("selected: {0}".format(name))
        self.document_name = name
        self.completeChanged.emit()

    def initializePage(self):
        model = QStandardItemModel()

        # using a document model, we can obtain all the documents to list inside this view...
        all_docs = DocumentStorage.documents()
        for doc_filename in all_docs:
            # find out the last scan date, number of files, etc
            document = PersistentScanningState(doc_filename)
            logger.debug("found info: {0}".format(document.info))
            creation_date_str = str(document.info.date_created)
            last_date = str(document.info.date_last_scanned)
            num_scanned = "{0:,}".format(document.info.files_scanned)
            num_merged = "{0:,}".format(document.info.files_merged)
            is_merged = document.info.merge_complete
            if not is_merged:
                last_date_str = ""
            else:
                last_date_str = last_date

            doc = os.path.split(doc_filename)[1][:-len('.sqlite')]
            items = [
                QStandardItem(doc),
                QStandardItem(str(num_scanned)),
                QStandardItem(creation_date_str),
                QStandardItem(str(num_merged)),
                QStandardItem(last_date_str),
            ]

            items[1].setData(Qt.AlignRight, Qt.TextAlignmentRole)
            items[3].setData(Qt.AlignRight, Qt.TextAlignmentRole)

            model.invisibleRootItem().appendRow(items)

        self.ui.treeView.setModel(model)

        header = self.ui.treeView.header()

        model.setHeaderData(0, Qt.Horizontal, "Name")
        model.setHeaderData(1, Qt.Horizontal, "# First Scan")
        model.setHeaderData(2, Qt.Horizontal, "Date Created")
        model.setHeaderData(3, Qt.Horizontal, "# Second Scan")
        model.setHeaderData(4, Qt.Horizontal, "Date Scanned")

        header.setResizeMode(0, QHeaderView.ResizeToContents)
        header.setResizeMode(1, QHeaderView.ResizeToContents)
        header.setResizeMode(2, QHeaderView.ResizeToContents)
        header.setResizeMode(3, QHeaderView.ResizeToContents)
        header.setResizeMode(4, QHeaderView.ResizeToContents)

        self.ui.treeView.selectionModel().currentRowChanged.connect(self.__onSelectionChanged)

    def __deleteSelectedItems(self):
        toDelete = self.deleteSelectedTreeViewItems(self.ui.treeView, "Remove Scan Files?",
                                           "Are you sure you want to delete the selected scan files - this action cannot be undone")
        for rowItems in toDelete:
            for item in rowItems:
                name = item.data(Qt.DisplayRole).toString()
                logger.debug("going to delete: {0}".format(name))
                DocumentStorage.deleteDocumentNamed(name)
                self.scanFileDeleted.emit(name)
                break

        self.completeChanged.emit()

    def isComplete(self):
        done = self.document_name is not None
        if done:
            # if the second scan completed OK, we can skip the second scan
            fullpath_doc_name = DocumentStorage.documentFullPath(self.document_name)
            logger.debug("going with full path of document: {0}".format(fullpath_doc_name))
            persist_doc = PersistentScanningState(fullpath_doc_name)
            self.setField("secondScanComplete", persist_doc.info.merge_complete)
            self.wizard().setDocumentName(self.document_name)
            self.wizard().setWindowFilePath(fullpath_doc_name)
        return done


from lib.path_info import PathInfo
import os
from lib.platform import Platform
from PyQt4.QtCore import Qt, QVariant, QModelIndex, QAbstractItemModel, QDateTime
from PyQt4.QtGui import QWidget, QApplication, QHeaderView, QFileIconProvider, QFont, QColor
from lib.directory_scanner import DirectoryScanner
from lib.persistent_scanning_state import PersistentScanningState, FileSystemMerge
import sys

import logging
logger = logging.getLogger(__name__)

class MergeScanMapper(object):
    """Handles mapping an int to a FileSystemMerge instance, for use by the QModelIndex internalId() requirements"""
    INVALID_ID = -1

    def __init__(self, docu):
        super(MergeScanMapper, self).__init__()
        self.counter = 1
        self.ms_to_id = dict()
        self.id_to_ms = dict()
        self.document = docu

    def getMergeScanForId(self, id_value):
        if id_value in self.id_to_ms:
            return self.id_to_ms[id_value]
        logger.critical("No FileSystemMerge record for ID value: {}".format(id_value))
        return None

    def storeMergeScan(self, ms):
        if ms is None:
            logger.critical("Trying to store a None FileSystemMerge")
            return MergeScanTreeModel.INVALID_ID
        if ms in self.ms_to_id:
            return self.ms_to_id[ms]
        self.counter += 1
        self.ms_to_id[ms] = self.counter
        self.id_to_ms[self.counter] = ms
        return self.counter

    def getUniqueIDForPath(self, path_value):
        ms = self.document.session.query(FileSystemMerge).get(path_value)
        return self.storeMergeScan(ms)

class MergeScanTreeModel(QAbstractItemModel):
    COL_CHECKED = 0
    COL_NAME = 0
    COL_ICON = 0
    COL_CHANGE_TYPE = 1
    COL_SIZE = 2
    COL_PERMISSIONS = 3
    COL_DATE_MODIFIED = 4

    # make me larger if you add more columns...
    COL_MAX = 5

    IconProvider = QFileIconProvider()

    def __init__(self, docu, mapper, rootMergeScans, owner = None):
        super(MergeScanTreeModel, self).__init__(owner)
        self.document = docu
        self.mapper = mapper
        self.roots = rootMergeScans

    def flags(self, index):
        if not index.isValid():
            return 0
        ms = self.mapper.getMergeScanForId(index.internalId())
        if ms is None or ms.flags == PersistentScanningState.ITEM_DELETED:
            return Qt.ItemIsSelectable
        flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable
        if index.column() == MergeScanTreeModel.COL_CHECKED:
            flags |= Qt.ItemIsUserCheckable
        return flags

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if section == MergeScanTreeModel.COL_CHECKED or section == MergeScanTreeModel.COL_NAME:
                return "Path"
            elif section == MergeScanTreeModel.COL_SIZE:
                return "Size"
            elif section == MergeScanTreeModel.COL_PERMISSIONS:
                return "Permissions"
            elif section == MergeScanTreeModel.COL_CHANGE_TYPE:
                return "Change"
            elif section == MergeScanTreeModel.COL_DATE_MODIFIED:
                return "Modification Date"
        return QVariant()

    def mergeScanForIndex(self, index):
        """Public method that provides a FileSystemMerge object or None for any QModelIndex in the model"""
        return self.mapper.getMergeScanForId(index.internalId())

    def columnCount(self, parent):
        return MergeScanTreeModel.COL_MAX

    def hasChildren(self, parent):
        if not parent.isValid():
            return len(self.roots) > 0
        item = self.mapper.getMergeScanForId(parent.internalId())
        #logger.debug("hasChildren: ms {0}, # children: {1}".format(item, len(item.children)))
        return len(item.children) > 0

    def index(self, row, col, parent):
        if col >= MergeScanTreeModel.COL_MAX:
            return QModelIndex()
        if not parent.isValid():
            if row >= len(self.roots):
                logger.critical("index: row/col {0}/{1} asked for a row where the parent is not valid".format(row/col))
                return QModelIndex()
            id = self.mapper.getUniqueIDForPath(self.roots[row].abs_path)
        else:
            id = parent.internalId()
            child = self.mapper.getMergeScanForId(id)
            if row >= len(child.children):
                logger.critical("index: method requested row > child.children count")
                return QModelIndex()
            id = self.mapper.storeMergeScan(child.children[row])
        if id != MergeScanMapper.INVALID_ID:
            return self.createIndex(row, col, id)
        logger.critical("index: for row/col {0}/{1}, parent id {2} the internal id was invalid".format(row, col, parent.internalId()))
        return QModelIndex()

    def setCheckedStateForMergeScan(self, ms, value, emit_layout_events = True):
        # looks weird, but a layout changed emission causes the view to redraw without losing the selection state
        if emit_layout_events:
            self.layoutAboutToBeChanged.emit()

        ms.checked = value
        ms.propagateCheckedStateToChildren()
        ms.propagateCurrentCheckedStateToParents()

        if emit_layout_events:
            self.layoutChanged.emit()

    def setData(self, index, value, role):
        if role != Qt.CheckStateRole or not index.isValid() or index.column() != MergeScanTreeModel.COL_CHECKED:
            return False 
        id = index.internalId()
        ms = self.mapper.getMergeScanForId(id)
        if ms.flags == PersistentScanningState.ITEM_DELETED:
            return False
        if ms is not None:
            self.setCheckedStateForMergeScan(ms, value.toInt()[0])
            return True
        return False

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        ms = self.mapper.getMergeScanForId(index.internalId())
        if ms is None:
            logger.critical("data: wasn't able to get the FileSystemMerge for internal id {0}".format(index.internalId()))
            return QVariant()
        if role == Qt.CheckStateRole and index.column() == MergeScanTreeModel.COL_CHECKED:
            return ms.checked
        if role == Qt.DecorationRole and index.column() == MergeScanTreeModel.COL_ICON:
            return self.IconProvider.icon(QFileIconProvider.Folder) if ms.is_dir else None
        if role == Qt.TextColorRole:
            if ms.flags == PersistentScanningState.ITEM_DELETED:
                return QColor(Qt.red)
            return QVariant()
        if role == Qt.FontRole:
            font = QFont()
            info = PathInfo(ms.abs_path, ms.path_info)
            if info.is_symlink or ms.flags == PersistentScanningState.ITEM_UNREADABLE:
                font.setItalic(True)
            return font
        if role == Qt.DisplayRole:
            data = None
            if index.column() == MergeScanTreeModel.COL_NAME:
                data = os.path.basename(ms.abs_path)
                if "Sample" in data:
                    x = 0
            elif index.column() == MergeScanTreeModel.COL_CHANGE_TYPE:
                if ms.flags == PersistentScanningState.ITEM_ADDED:
                    data = "Added"
                elif ms.flags == PersistentScanningState.ITEM_DELETED:
                    data = "Deleted"
                elif ms.flags == PersistentScanningState.ITEM_MODIFIED:
                    data = "Modified"
                elif ms.flags == PersistentScanningState.ITEM_UNCHANGED:
                    data = ""
            elif index.column() == MergeScanTreeModel.COL_SIZE:
                data = PathInfo(ms.abs_path, ms.path_info).size_human_readable if not ms.is_dir else None
            elif index.column() == MergeScanTreeModel.COL_DATE_MODIFIED:
                value = QDateTime.fromTime_t(int(PathInfo(ms.abs_path, ms.path_info).modified_date))
                data = value.toString()
            elif index.column() == MergeScanTreeModel.COL_PERMISSIONS:
                info = PathInfo(ms.abs_path, ms.path_info)
                data = "{0}:{1} {2}".format(info.uid, info.gid, info.posix_perms_human_readable)
            return data
        return QVariant()

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()
        internal_id = index.internalId()
        ms = self.mapper.getMergeScanForId(internal_id)
        if ms is None:
            return QModelIndex()
        ms_parent = ms.parent
        if ms_parent is None:
            return QModelIndex()
        parent_id = self.mapper.storeMergeScan(ms_parent)
        grand_parent = ms_parent.parent
        if grand_parent is None:
            # which row number is this parent at in the top level?
            row = self.roots.index(ms_parent)
        else:
            self.mapper.storeMergeScan(grand_parent)
            row = grand_parent.children.index(ms_parent)
        return self.createIndex(row, 0, parent_id) 
    
    

    def rowCount(self, parent):
        if parent.isValid():
            item = self.mapper.getMergeScanForId(parent.internalId())
            return len(item.children)
        return len(self.roots)


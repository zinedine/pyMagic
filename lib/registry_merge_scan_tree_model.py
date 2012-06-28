

from lib.persistent_scanning_state import PersistentScanningState,  RegistryEntryMerge
from PyQt4.QtCore import Qt, QVariant, QModelIndex, QAbstractItemModel, QDateTime
from PyQt4.QtGui import QWidget, QApplication, QHeaderView, QFileIconProvider, QFont, QColor
#logger.critical("No FileSystemMerge record for ID value: {}".format(id_value))
from  lib.registry_info  import RegistryInfo


import logging
logger = logging.getLogger(__name__)

class MergedRegistryMapper(object):
    
    INVALID_ID = -1
    def __init__(self, storage ):
        super(MergedRegistryMapper, self).__init__()
        self.storage = storage
        self.mr_to_id = dict()
        self.id_to_mr = dict()
        self.count = 0 
        
    def storeMergedRegistry(self, mr):
        if mr is None:
            logger.critical("merged registry scan is null.")
            return self.INVALID_ID
        if mr in self.mr_to_id:
            return self.mr_to_id[mr]
        self.count += 1
        self.id_to_mr[self.count] = mr
        self.mr_to_id[mr] = self.count
        return self.count
    
    def getUniqueIDforMergeRegistry(self, key):
        # get mr from reading the DB
        mr = self.storage.session.query(RegistryEntryMerge).get(key)
        #if mr is None:
        #    logger.critical("key name {} does not exist in the database/RegistryEntryMerge table".format(key))
        #    return -1
        return self.storeMergedRegistry(mr)
    
    def getMergedRegistryforID(self, id):
        if id < 1:
            logger.critical("id {} is not valid".format(id))
        if not id in self.id_to_mr:
            logger.critical("registry merge with id {} does not exist".format(id))
            return None
        return self.id_to_mr[id]
    
    def updateMergeScan(self, mr):
        if mr is None:
            return False
        self.storage.session.add(mr)
        self.storage.session.commit() 
            
class mergedRegistryTreeModel(QAbstractItemModel):
    COL_CHECKED = 0
    COL_NAME = 0
    COL_CHANGE_TYPE = 1

    COL_MAX = 2

    def __init__(self, storage, mapper, hives,  owner = None):
        super(mergedRegistryTreeModel, self).__init__(owner)
        self.storage = storage
        self.mapper  = mapper
        self.hives = hives.keys()
        
    def parent(self, index):
        if not index.isValid():
            return QModelIndex()
        internal_id = index.internalId()
        mr = self.mapper.getMergedRegistryforID(internal_id)
        if mr is None:
            return QModelIndex()
        mrParent = mr.parent
        if mrParent is None:
            return QModelIndex()
        parent_id = self.mapper.storeMergedRegistry(mrParent)
        grand_parent = mrParent.parent
        if grand_parent is None:
            row = self.hives.index(mrParent.key_name)
        else:
            self.mapper.storeMergedRegistry(grand_parent)
            row = grand_parent.children.index(mrParent)
        return self.createIndex(row, 0, parent_id) 
        
    def columnCount(self, parent):
        return  mergedRegistryTreeModel.COL_MAX
       
    def rowCount(self, parent):
        if parent.isValid():
            item = self.mapper.getMergedRegistryforID(parent.internalId())
            return len(item.children)
        return len(self.hives)
    
    def hasChildren(self, parent):
        if not parent.isValid():
            return len(self.hives) > 0
        item = self.mapper.getMergedRegistryforID(parent.internalId()) 
        return len(item.children) > 0
    
    def data(self, index , role):
        if not index.isValid():
            return QVariant()
        mr = self.mapper.getMergedRegistryforID(index.internalId())
        #print "index internal: {} key: {}".format(index.internalId(), mr.key_name)
        if mr is None:
            logger.critical("data: wasn't able to get the RegistryEntryMerge for internal id {0}".format(index.internalId()))
            return QVariant()
        if role == Qt.CheckStateRole and index.column() == mergedRegistryTreeModel.COL_CHECKED:
            return mr.checked
        if role == Qt.TextColorRole:
            if mr.flags == PersistentScanningState.ITEM_DELETED:
                return QColor(Qt.red)
            return QVariant()
        # skipped Qt.FonteRole
        if role == Qt.DisplayRole:
            data = None
            if index.column() == mergedRegistryTreeModel.COL_NAME:
                #data = mr.key_name
                regInfo = RegistryInfo(mr.key_name, mr.values)
                data = regInfo.keyBaseName
            elif index.column() == mergedRegistryTreeModel.COL_CHANGE_TYPE:
                if mr.flags == PersistentScanningState.ITEM_ADDED:
                    data = "Added"
                elif mr.flags == PersistentScanningState.ITEM_DELETED:
                    data = "Deleted"
                elif mr.flags == PersistentScanningState.ITEM_MODIFIED:
                    data = "Modified"
                elif mr.flags == PersistentScanningState.ITEM_UNCHANGED:
                    data = "-"
            return data
        return QVariant() 
    
    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if section == mergedRegistryTreeModel.COL_CHECKED or section == mergedRegistryTreeModel.COL_NAME:
                return "key"
            elif section == mergedRegistryTreeModel.COL_CHANGE_TYPE:
                return "Change"
        return QVariant()
    
    def index(self, row, col, parent): 
        if col >= mergedRegistryTreeModel.COL_MAX:
            return QModelIndex()
        if not parent.isValid():
            if row > len(self.hives):
                logger.critical("index: row/col {0}/{1} asked for a row where the parent is not valid".format(row, col))
                return QModelIndex()
            
            id = self.mapper.getUniqueIDforMergeRegistry(self.hives[row]) 
        else:
            id = parent.internalId()
            parent_mr = self.mapper.getMergedRegistryforID(id)
            if row >= len(parent_mr.children):
                logger.critical("error... in index ")
                return QModelIndex()
            id = self.mapper.storeMergedRegistry(parent_mr.children[row])
        if id != MergedRegistryMapper.INVALID_ID:
            return self.createIndex(row, col, id)
        logger.critical("error .... index failed to get anything")
        return QModelIndex()
    
    def setData(self, index, value, role):
        if role != Qt.CheckStateRole and not index.isValid() and index.column != mergedRegistryTreeModel.COL_CHECKED:
            return False
        id = index.internalId()
        mr = self.mapper.getMergedRegistryforID(id)
        # msi is able to delete registry key, so leave the option to check deleted items
        #if mr.checked ==  PersistentScanningState.ITEM_DELETED:
        #    return False
        if mr is not None:
            self.setCheckedStateForRegistryMergeScan(mr, value.toInt()[0])
            return True
        return False
            
            
    def setCheckedStateForRegistryMergeScan(self, mr, value, emit_layout_events = True ):
        if  emit_layout_events:
            self.layoutAboutToBeChanged.emit()
        mr.checked = value
        mr.propagateCheckedStateToChildren()
        mr.propagateCurrentCheckedStateToParents()
        
        #here, save mr back to database
        #...
        self.mapper.updateMergeScan(mr)
        
        if emit_layout_events:
            self.layoutChanged.emit() 
        
            
    def flags(self, index):
        if not index.isValid():
            return 0
        mr = self.mapper.getMergedRegistryforID(index.internalId())
        if mr is None or mr.flags == PersistentScanningState.ITEM_DELETED:
            return Qt.ItemIsSelectable
        flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable
        if index.column() == mergedRegistryTreeModel.COL_CHECKED:
            flags |= Qt.ItemIsUserCheckable
        return flags

    
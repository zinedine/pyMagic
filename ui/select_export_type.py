# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\select_export_type.ui'
#
# Created: Thu Mar 15 18:08:30 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_SelectExportType(object):
    def setupUi(self, SelectExportType):
        SelectExportType.setObjectName(_fromUtf8("SelectExportType"))
        SelectExportType.resize(485, 265)
        self.gridLayout = QtGui.QGridLayout(SelectExportType)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(90, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(89, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 2, 1, 1)
        self.listExportTypes = QtGui.QTreeView(SelectExportType)
        self.listExportTypes.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.listExportTypes.setAlternatingRowColors(False)
        self.listExportTypes.setIconSize(QtCore.QSize(32, 32))
        self.listExportTypes.setRootIsDecorated(False)
        self.listExportTypes.setObjectName(_fromUtf8("listExportTypes"))
        self.listExportTypes.header().setVisible(False)
        self.gridLayout.addWidget(self.listExportTypes, 0, 1, 1, 1)

        self.retranslateUi(SelectExportType)
        QtCore.QMetaObject.connectSlotsByName(SelectExportType)

    def retranslateUi(self, SelectExportType):
        SelectExportType.setWindowTitle(QtGui.QApplication.translate("SelectExportType", "Form", None, QtGui.QApplication.UnicodeUTF8))


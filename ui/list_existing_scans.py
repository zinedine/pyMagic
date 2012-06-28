# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\list_existing_scans.ui'
#
# Created: Thu Mar 15 18:08:28 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_ListExistingScans(object):
    def setupUi(self, ListExistingScans):
        ListExistingScans.setObjectName(_fromUtf8("ListExistingScans"))
        ListExistingScans.resize(684, 373)
        ListExistingScans.setStyleSheet(_fromUtf8(""))
        self.gridLayout = QtGui.QGridLayout(ListExistingScans)
        self.gridLayout.setVerticalSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.buttonContainer = QtGui.QWidget(ListExistingScans)
        self.buttonContainer.setObjectName(_fromUtf8("buttonContainer"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.buttonContainer)
        self.horizontalLayout.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.horizontalLayout.setContentsMargins(0, -1, 0, -1)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.deleteSelectedToolButton = QtGui.QToolButton(self.buttonContainer)
        self.deleteSelectedToolButton.setMinimumSize(QtCore.QSize(25, 25))
        self.deleteSelectedToolButton.setMaximumSize(QtCore.QSize(25, 25))
        self.deleteSelectedToolButton.setProperty("styled", True)
        self.deleteSelectedToolButton.setObjectName(_fromUtf8("deleteSelectedToolButton"))
        self.horizontalLayout.addWidget(self.deleteSelectedToolButton)
        spacerItem = QtGui.QSpacerItem(69, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout.addWidget(self.buttonContainer, 1, 0, 1, 1)
        self.treeView = QtGui.QTreeView(ListExistingScans)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeView.sizePolicy().hasHeightForWidth())
        self.treeView.setSizePolicy(sizePolicy)
        self.treeView.setFrameShape(QtGui.QFrame.StyledPanel)
        self.treeView.setFrameShadow(QtGui.QFrame.Sunken)
        self.treeView.setLineWidth(1)
        self.treeView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.treeView.setAlternatingRowColors(True)
        self.treeView.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.treeView.setRootIsDecorated(False)
        self.treeView.setObjectName(_fromUtf8("treeView"))
        self.gridLayout.addWidget(self.treeView, 0, 0, 1, 1)

        self.retranslateUi(ListExistingScans)
        QtCore.QMetaObject.connectSlotsByName(ListExistingScans)

    def retranslateUi(self, ListExistingScans):
        ListExistingScans.setWindowTitle(QtGui.QApplication.translate("ListExistingScans", "Scan Documents", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteSelectedToolButton.setToolTip(QtGui.QApplication.translate("ListExistingScans", "Delete the selected scan documents", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteSelectedToolButton.setText(QtGui.QApplication.translate("ListExistingScans", "-", None, QtGui.QApplication.UnicodeUTF8))


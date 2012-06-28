# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\CustomTreeWidget.ui'
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

class Ui_CustomTreeWidget(object):
    def setupUi(self, CustomTreeWidget):
        CustomTreeWidget.setObjectName(_fromUtf8("CustomTreeWidget"))
        CustomTreeWidget.resize(906, 578)
        self.gridLayout = QtGui.QGridLayout(CustomTreeWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.splitter = QtGui.QSplitter(CustomTreeWidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.treeView = QtGui.QTreeView(self.splitter)
        self.treeView.setEditTriggers(QtGui.QAbstractItemView.AllEditTriggers)
        self.treeView.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.treeView.setIconSize(QtCore.QSize(16, 16))
        self.treeView.setUniformRowHeights(True)
        self.treeView.setHeaderHidden(False)
        self.treeView.setObjectName(_fromUtf8("treeView"))
        self.treeView.header().setVisible(True)
        self.treeView.header().setCascadingSectionResizes(True)
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)

        self.retranslateUi(CustomTreeWidget)
        QtCore.QMetaObject.connectSlotsByName(CustomTreeWidget)

    def retranslateUi(self, CustomTreeWidget):
        CustomTreeWidget.setWindowTitle(QtGui.QApplication.translate("CustomTreeWidget", "The Widget Testing Grounds", None, QtGui.QApplication.UnicodeUTF8))


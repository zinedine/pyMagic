# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\filesystem_tree_view.ui'
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

class Ui_FileSystemTree(object):
    def setupUi(self, FileSystemTree):
        FileSystemTree.setObjectName(_fromUtf8("FileSystemTree"))
        FileSystemTree.resize(194, 297)
        self.gridLayout = QtGui.QGridLayout(FileSystemTree)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.treeView = QtGui.QTreeView(FileSystemTree)
        self.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeView.setObjectName(_fromUtf8("treeView"))
        self.gridLayout.addWidget(self.treeView, 0, 0, 1, 1)

        self.retranslateUi(FileSystemTree)
        QtCore.QMetaObject.connectSlotsByName(FileSystemTree)

    def retranslateUi(self, FileSystemTree):
        FileSystemTree.setWindowTitle(QtGui.QApplication.translate("FileSystemTree", "List of Directories", None, QtGui.QApplication.UnicodeUTF8))


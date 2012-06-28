# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\create_new_scan.ui'
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

class Ui_CreateNewScan(object):
    def setupUi(self, CreateNewScan):
        CreateNewScan.setObjectName(_fromUtf8("CreateNewScan"))
        CreateNewScan.resize(732, 409)
        self.gridLayout = QtGui.QGridLayout(CreateNewScan)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.listWidget = QtGui.QListWidget(CreateNewScan)
        self.listWidget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.listWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.gridLayout.addWidget(self.listWidget, 0, 0, 1, 3)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.addButton = QtGui.QToolButton(CreateNewScan)
        self.addButton.setMinimumSize(QtCore.QSize(25, 22))
        self.addButton.setMaximumSize(QtCore.QSize(25, 22))
        self.addButton.setProperty("styled", True)
        self.addButton.setObjectName(_fromUtf8("addButton"))
        self.horizontalLayout.addWidget(self.addButton)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.removeButton = QtGui.QToolButton(CreateNewScan)
        self.removeButton.setMinimumSize(QtCore.QSize(25, 22))
        self.removeButton.setMaximumSize(QtCore.QSize(25, 22))
        self.removeButton.setProperty("styled", True)
        self.removeButton.setObjectName(_fromUtf8("removeButton"))
        self.horizontalLayout.addWidget(self.removeButton)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 3)
        self.label_2 = QtGui.QLabel(CreateNewScan)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 3, 0, 2, 2)
        self.lineEditDocumentName = QtGui.QLineEdit(CreateNewScan)
        self.lineEditDocumentName.setObjectName(_fromUtf8("lineEditDocumentName"))
        self.gridLayout.addWidget(self.lineEditDocumentName, 5, 0, 1, 1)
        self.status = QtGui.QLabel(CreateNewScan)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.status.sizePolicy().hasHeightForWidth())
        self.status.setSizePolicy(sizePolicy)
        self.status.setText(_fromUtf8(""))
        self.status.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.status.setObjectName(_fromUtf8("status"))
        self.gridLayout.addWidget(self.status, 5, 1, 1, 1)
        self.line = QtGui.QFrame(CreateNewScan)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 2, 0, 1, 3)

        self.retranslateUi(CreateNewScan)
        QtCore.QMetaObject.connectSlotsByName(CreateNewScan)

    def retranslateUi(self, CreateNewScan):
        CreateNewScan.setWindowTitle(QtGui.QApplication.translate("CreateNewScan", "Choose the directories to scan", None, QtGui.QApplication.UnicodeUTF8))
        self.addButton.setToolTip(QtGui.QApplication.translate("CreateNewScan", "Add a new directory to the list", None, QtGui.QApplication.UnicodeUTF8))
        self.addButton.setText(QtGui.QApplication.translate("CreateNewScan", "+", None, QtGui.QApplication.UnicodeUTF8))
        self.removeButton.setToolTip(QtGui.QApplication.translate("CreateNewScan", "Removes the selected directories from the list", None, QtGui.QApplication.UnicodeUTF8))
        self.removeButton.setText(QtGui.QApplication.translate("CreateNewScan", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("CreateNewScan", "Provide your new scan with a name, then start it by pressing the \'Start Scan\' button.", None, QtGui.QApplication.UnicodeUTF8))


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ScannerWindow.ui'
#
# Created: Thu Mar 15 18:08:29 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_ScannerWindow(object):
    def setupUi(self, ScannerWindow):
        ScannerWindow.setObjectName(_fromUtf8("ScannerWindow"))
        ScannerWindow.resize(1180, 472)
        ScannerWindow.setStyleSheet(_fromUtf8(""))
        self.centralwidget = QtGui.QWidget(ScannerWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout_4 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_4.setMargin(0)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(True)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.gridLayout_4.addWidget(self.tabWidget, 0, 0, 1, 1)
        ScannerWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(ScannerWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1180, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        self.menuWindow = QtGui.QMenu(self.menubar)
        self.menuWindow.setObjectName(_fromUtf8("menuWindow"))
        ScannerWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(ScannerWindow)
        self.statusbar.setStyleSheet(_fromUtf8(""))
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        ScannerWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(ScannerWindow)
        self.toolBar.setAllowedAreas(QtCore.Qt.BottomToolBarArea|QtCore.Qt.TopToolBarArea)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        ScannerWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionNew_Scan = QtGui.QAction(ScannerWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/FileSet Magic_32.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNew_Scan.setIcon(icon)
        self.actionNew_Scan.setIconVisibleInMenu(False)
        self.actionNew_Scan.setObjectName(_fromUtf8("actionNew_Scan"))
        self.actionAbout = QtGui.QAction(ScannerWindow)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.actionExport_as_Fileset_Package = QtGui.QAction(ScannerWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/Registry_32.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExport_as_Fileset_Package.setIcon(icon1)
        self.actionExport_as_Fileset_Package.setIconVisibleInMenu(False)
        self.actionExport_as_Fileset_Package.setObjectName(_fromUtf8("actionExport_as_Fileset_Package"))
        self.actionShow_Introduction = QtGui.QAction(ScannerWindow)
        self.actionShow_Introduction.setObjectName(_fromUtf8("actionShow_Introduction"))
        self.actionShow_Scan_Files = QtGui.QAction(ScannerWindow)
        self.actionShow_Scan_Files.setObjectName(_fromUtf8("actionShow_Scan_Files"))
        self.menuFile.addAction(self.actionNew_Scan)
        self.menuFile.addAction(self.actionExport_as_Fileset_Package)
        self.menuHelp.addAction(self.actionAbout)
        self.menuWindow.addAction(self.actionShow_Introduction)
        self.menuWindow.addAction(self.actionShow_Scan_Files)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuWindow.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.toolBar.addAction(self.actionNew_Scan)
        self.toolBar.addAction(self.actionExport_as_Fileset_Package)

        self.retranslateUi(ScannerWindow)
        QtCore.QMetaObject.connectSlotsByName(ScannerWindow)

    def retranslateUi(self, ScannerWindow):
        ScannerWindow.setWindowTitle(QtGui.QApplication.translate("ScannerWindow", "PyMagic - File Scanner", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("ScannerWindow", "Scan", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("ScannerWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menuWindow.setTitle(QtGui.QApplication.translate("ScannerWindow", "Window", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("ScannerWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew_Scan.setText(QtGui.QApplication.translate("ScannerWindow", "New Scan...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew_Scan.setShortcut(QtGui.QApplication.translate("ScannerWindow", "Ctrl+N", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setText(QtGui.QApplication.translate("ScannerWindow", "About...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExport_as_Fileset_Package.setText(QtGui.QApplication.translate("ScannerWindow", "Export as Fileset/Package...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExport_as_Fileset_Package.setIconText(QtGui.QApplication.translate("ScannerWindow", "Export", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExport_as_Fileset_Package.setToolTip(QtGui.QApplication.translate("ScannerWindow", "Export", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExport_as_Fileset_Package.setShortcut(QtGui.QApplication.translate("ScannerWindow", "Ctrl+E", None, QtGui.QApplication.UnicodeUTF8))
        self.actionShow_Introduction.setText(QtGui.QApplication.translate("ScannerWindow", "Show Introduction...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionShow_Scan_Files.setText(QtGui.QApplication.translate("ScannerWindow", "Show Scan Files...", None, QtGui.QApplication.UnicodeUTF8))

import ScannerWindow_rc

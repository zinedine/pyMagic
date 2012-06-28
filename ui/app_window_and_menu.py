# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\app_window_and_menu.ui'
#
# Created: Thu Mar 15 18:08:27 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuWindow = QtGui.QMenu(self.menubar)
        self.menuWindow.setObjectName(_fromUtf8("menuWindow"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen_Existing_Scan = QtGui.QAction(MainWindow)
        self.actionOpen_Existing_Scan.setObjectName(_fromUtf8("actionOpen_Existing_Scan"))
        self.actionPreferences = QtGui.QAction(MainWindow)
        self.actionPreferences.setMenuRole(QtGui.QAction.PreferencesRole)
        self.actionPreferences.setObjectName(_fromUtf8("actionPreferences"))
        self.actionShow_Log = QtGui.QAction(MainWindow)
        self.actionShow_Log.setObjectName(_fromUtf8("actionShow_Log"))
        self.actionSubmit_Bug_Report = QtGui.QAction(MainWindow)
        self.actionSubmit_Bug_Report.setObjectName(_fromUtf8("actionSubmit_Bug_Report"))
        self.menuFile.addAction(self.actionPreferences)
        self.menuWindow.addAction(self.actionShow_Log)
        self.menuWindow.addAction(self.actionSubmit_Bug_Report)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuWindow.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuWindow.setTitle(QtGui.QApplication.translate("MainWindow", "Window", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen_Existing_Scan.setText(QtGui.QApplication.translate("MainWindow", "Open Existing Scan...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPreferences.setText(QtGui.QApplication.translate("MainWindow", "Preferences...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionShow_Log.setText(QtGui.QApplication.translate("MainWindow", "Show Log...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionShow_Log.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Shift+L", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSubmit_Bug_Report.setText(QtGui.QApplication.translate("MainWindow", "Submit Bug Report...", None, QtGui.QApplication.UnicodeUTF8))


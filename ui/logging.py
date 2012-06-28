# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\logging.ui'
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

class Ui_LoggingWidget(object):
    def setupUi(self, LoggingWidget):
        LoggingWidget.setObjectName(_fromUtf8("LoggingWidget"))
        LoggingWidget.resize(1089, 575)
        self.gridLayout = QtGui.QGridLayout(LoggingWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.plainTextEdit = QtGui.QPlainTextEdit(LoggingWidget)
        self.plainTextEdit.setUndoRedoEnabled(False)
        self.plainTextEdit.setLineWrapMode(QtGui.QPlainTextEdit.NoWrap)
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setObjectName(_fromUtf8("plainTextEdit"))
        self.gridLayout.addWidget(self.plainTextEdit, 0, 0, 1, 3)
        self.buttonClearLog = QtGui.QPushButton(LoggingWidget)
        self.buttonClearLog.setObjectName(_fromUtf8("buttonClearLog"))
        self.gridLayout.addWidget(self.buttonClearLog, 1, 0, 1, 1)
        self.cbShowOnError = QtGui.QCheckBox(LoggingWidget)
        self.cbShowOnError.setChecked(True)
        self.cbShowOnError.setObjectName(_fromUtf8("cbShowOnError"))
        self.gridLayout.addWidget(self.cbShowOnError, 1, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(LoggingWidget)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 2, 1, 1)

        self.retranslateUi(LoggingWidget)
        QtCore.QMetaObject.connectSlotsByName(LoggingWidget)

    def retranslateUi(self, LoggingWidget):
        LoggingWidget.setWindowTitle(QtGui.QApplication.translate("LoggingWidget", "Logging", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonClearLog.setText(QtGui.QApplication.translate("LoggingWidget", "Clear Log", None, QtGui.QApplication.UnicodeUTF8))
        self.cbShowOnError.setText(QtGui.QApplication.translate("LoggingWidget", "Show this window when errors occur", None, QtGui.QApplication.UnicodeUTF8))


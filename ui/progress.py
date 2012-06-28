# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\progress.ui'
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

class Ui_Progress(object):
    def setupUi(self, Progress):
        Progress.setObjectName(_fromUtf8("Progress"))
        Progress.resize(565, 55)
        self.gridLayout = QtGui.QGridLayout(Progress)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(Progress)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.progressBar = QtGui.QProgressBar(Progress)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout.addWidget(self.progressBar, 0, 1, 1, 1)

        self.retranslateUi(Progress)
        QtCore.QMetaObject.connectSlotsByName(Progress)

    def retranslateUi(self, Progress):
        Progress.setWindowTitle(QtGui.QApplication.translate("Progress", "Progress", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Progress", "Loading:", None, QtGui.QApplication.UnicodeUTF8))


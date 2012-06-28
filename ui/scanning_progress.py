# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\scanning_progress.ui'
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

class Ui_ScanningProgress(object):
    def setupUi(self, ScanningProgress):
        ScanningProgress.setObjectName(_fromUtf8("ScanningProgress"))
        ScanningProgress.resize(752, 192)
        self.gridLayout = QtGui.QGridLayout(ScanningProgress)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(ScanningProgress)
        self.label.setWordWrap(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 3)
        self.progressBar = QtGui.QProgressBar(ScanningProgress)
        self.progressBar.setMaximum(0)
        self.progressBar.setProperty("value", -1)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout.addWidget(self.progressBar, 2, 0, 1, 3)
        self.labelFound = QtGui.QLabel(ScanningProgress)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelFound.sizePolicy().hasHeightForWidth())
        self.labelFound.setSizePolicy(sizePolicy)
        self.labelFound.setWordWrap(True)
        self.labelFound.setObjectName(_fromUtf8("labelFound"))
        self.gridLayout.addWidget(self.labelFound, 3, 0, 1, 1)
        self.labelProgressText = QtGui.QLabel(ScanningProgress)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelProgressText.sizePolicy().hasHeightForWidth())
        self.labelProgressText.setSizePolicy(sizePolicy)
        self.labelProgressText.setText(_fromUtf8(""))
        self.labelProgressText.setWordWrap(False)
        self.labelProgressText.setObjectName(_fromUtf8("labelProgressText"))
        self.gridLayout.addWidget(self.labelProgressText, 3, 1, 1, 2)
        spacerItem = QtGui.QSpacerItem(20, 34, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 5, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 53, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 0, 1, 1, 1)
        self.labelFound_2 = QtGui.QLabel(ScanningProgress)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelFound_2.sizePolicy().hasHeightForWidth())
        self.labelFound_2.setSizePolicy(sizePolicy)
        self.labelFound_2.setWordWrap(True)
        self.labelFound_2.setObjectName(_fromUtf8("labelFound_2"))
        self.gridLayout.addWidget(self.labelFound_2, 4, 0, 1, 1)
        self.labelProgressCount = QtGui.QLabel(ScanningProgress)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelProgressCount.sizePolicy().hasHeightForWidth())
        self.labelProgressCount.setSizePolicy(sizePolicy)
        self.labelProgressCount.setText(_fromUtf8(""))
        self.labelProgressCount.setWordWrap(False)
        self.labelProgressCount.setObjectName(_fromUtf8("labelProgressCount"))
        self.gridLayout.addWidget(self.labelProgressCount, 4, 1, 1, 2)

        self.retranslateUi(ScanningProgress)
        QtCore.QMetaObject.connectSlotsByName(ScanningProgress)

    def retranslateUi(self, ScanningProgress):
        ScanningProgress.setWindowTitle(QtGui.QApplication.translate("ScanningProgress", "Scanning...", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("ScanningProgress", "FilesetMagic is scanning the disk, this can take a number of minutes...", None, QtGui.QApplication.UnicodeUTF8))
        self.labelFound.setText(QtGui.QApplication.translate("ScanningProgress", "File:", None, QtGui.QApplication.UnicodeUTF8))
        self.labelFound_2.setText(QtGui.QApplication.translate("ScanningProgress", "Count:", None, QtGui.QApplication.UnicodeUTF8))


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\scanning_complete_install_now.ui'
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

class Ui_ScanningCompleteInstallNow(object):
    def setupUi(self, ScanningCompleteInstallNow):
        ScanningCompleteInstallNow.setObjectName(_fromUtf8("ScanningCompleteInstallNow"))
        ScanningCompleteInstallNow.resize(878, 462)
        self.gridLayout = QtGui.QGridLayout(ScanningCompleteInstallNow)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.labelInfo = QtGui.QLabel(ScanningCompleteInstallNow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelInfo.sizePolicy().hasHeightForWidth())
        self.labelInfo.setSizePolicy(sizePolicy)
        self.labelInfo.setWordWrap(True)
        self.labelInfo.setObjectName(_fromUtf8("labelInfo"))
        self.gridLayout.addWidget(self.labelInfo, 0, 0, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.labelDocumentName = QtGui.QLabel(ScanningCompleteInstallNow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelDocumentName.sizePolicy().hasHeightForWidth())
        self.labelDocumentName.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.labelDocumentName.setFont(font)
        self.labelDocumentName.setText(_fromUtf8(""))
        self.labelDocumentName.setAlignment(QtCore.Qt.AlignCenter)
        self.labelDocumentName.setObjectName(_fromUtf8("labelDocumentName"))
        self.horizontalLayout_3.addWidget(self.labelDocumentName)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.gridLayout.addLayout(self.horizontalLayout_3, 2, 0, 1, 1)
        self.label = QtGui.QLabel(ScanningCompleteInstallNow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setText(_fromUtf8(""))
        self.label.setPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/installer-mac.png")))
        self.label.setScaledContents(False)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 3, 0, 1, 1)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.label_2 = QtGui.QLabel(ScanningCompleteInstallNow)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.buttonFindChanges = QtGui.QPushButton(ScanningCompleteInstallNow)
        self.buttonFindChanges.setObjectName(_fromUtf8("buttonFindChanges"))
        self.horizontalLayout.addWidget(self.buttonFindChanges)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem5)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 5, 0, 1, 1)
        spacerItem6 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
        self.gridLayout.addItem(spacerItem6, 1, 0, 1, 1)
        spacerItem7 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
        self.gridLayout.addItem(spacerItem7, 4, 0, 1, 1)

        self.retranslateUi(ScanningCompleteInstallNow)
        QtCore.QMetaObject.connectSlotsByName(ScanningCompleteInstallNow)

    def retranslateUi(self, ScanningCompleteInstallNow):
        ScanningCompleteInstallNow.setWindowTitle(QtGui.QApplication.translate("ScanningCompleteInstallNow", "Scanning...", None, QtGui.QApplication.UnicodeUTF8))
        self.labelInfo.setText(QtGui.QApplication.translate("ScanningCompleteInstallNow", "You can install your software now.  Once you have installed, configured and tested your software - and you are ready to make a package/fileset from it - press the \"Find Changes\" button.\n"
"\n"
"If you quit Fileset Magic, you can easily complete the creation of your package/fileset by re-running the tool and selecting the following document:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("ScanningCompleteInstallNow", "When your software is installed - press the \"Find Changes...\" button below", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonFindChanges.setText(QtGui.QApplication.translate("ScanningCompleteInstallNow", "Find Changes...", None, QtGui.QApplication.UnicodeUTF8))

import scanning_complete_install_now_rc

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\PyMagicMSI\x\plugins\exporters\win_msi\ui_win_msi.ui'
#
# Created: Tue Dec 27 21:42:05 2011
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MSICreationPage(object):
    def setupUi(self, MSICreationPage):
        MSICreationPage.setObjectName(_fromUtf8("MSICreationPage"))
        MSICreationPage.resize(535, 276)
        MSICreationPage.setWindowTitle(QtGui.QApplication.translate("MSICreationPage", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.gridLayout_2 = QtGui.QGridLayout(MSICreationPage)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gbMSIWidget = QtGui.QGroupBox(MSICreationPage)
        self.gbMSIWidget.setTitle(QtGui.QApplication.translate("MSICreationPage", "create MSI:", None, QtGui.QApplication.UnicodeUTF8))
        self.gbMSIWidget.setObjectName(_fromUtf8("gbMSIWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gbMSIWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblProductName = QtGui.QLabel(self.gbMSIWidget)
        self.lblProductName.setText(QtGui.QApplication.translate("MSICreationPage", "Product Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.lblProductName.setObjectName(_fromUtf8("lblProductName"))
        self.gridLayout.addWidget(self.lblProductName, 0, 0, 1, 1)
        self.lineEditProductName = QtGui.QLineEdit(self.gbMSIWidget)
        self.lineEditProductName.setObjectName(_fromUtf8("lineEditProductName"))
        self.gridLayout.addWidget(self.lineEditProductName, 0, 1, 1, 2)
        self.lblManufacturer = QtGui.QLabel(self.gbMSIWidget)
        self.lblManufacturer.setText(QtGui.QApplication.translate("MSICreationPage", "Manufacturer:", None, QtGui.QApplication.UnicodeUTF8))
        self.lblManufacturer.setObjectName(_fromUtf8("lblManufacturer"))
        self.gridLayout.addWidget(self.lblManufacturer, 1, 0, 1, 1)
        self.lineEditManufacturer = QtGui.QLineEdit(self.gbMSIWidget)
        self.lineEditManufacturer.setObjectName(_fromUtf8("lineEditManufacturer"))
        self.gridLayout.addWidget(self.lineEditManufacturer, 1, 1, 1, 2)
        self.lblProductVersion = QtGui.QLabel(self.gbMSIWidget)
        self.lblProductVersion.setText(QtGui.QApplication.translate("MSICreationPage", "Product Version:", None, QtGui.QApplication.UnicodeUTF8))
        self.lblProductVersion.setObjectName(_fromUtf8("lblProductVersion"))
        self.gridLayout.addWidget(self.lblProductVersion, 2, 0, 1, 1)
        self.lineEditProductVersion = QtGui.QLineEdit(self.gbMSIWidget)
        self.lineEditProductVersion.setObjectName(_fromUtf8("lineEditProductVersion"))
        self.gridLayout.addWidget(self.lineEditProductVersion, 2, 1, 1, 2)
        self.lblLanguage = QtGui.QLabel(self.gbMSIWidget)
        self.lblLanguage.setText(QtGui.QApplication.translate("MSICreationPage", "Language:", None, QtGui.QApplication.UnicodeUTF8))
        self.lblLanguage.setObjectName(_fromUtf8("lblLanguage"))
        self.gridLayout.addWidget(self.lblLanguage, 3, 0, 1, 1)
        self.cbLanguage = QtGui.QComboBox(self.gbMSIWidget)
        self.cbLanguage.setObjectName(_fromUtf8("cbLanguage"))
        self.gridLayout.addWidget(self.cbLanguage, 3, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(335, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 3, 2, 1, 1)
        self.gridLayout_2.addWidget(self.gbMSIWidget, 0, 0, 1, 2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pbCreateMSI = QtGui.QPushButton(MSICreationPage)
        self.pbCreateMSI.setText(QtGui.QApplication.translate("MSICreationPage", "create MSI", None, QtGui.QApplication.UnicodeUTF8))
        self.pbCreateMSI.setObjectName(_fromUtf8("pbCreateMSI"))
        self.horizontalLayout.addWidget(self.pbCreateMSI)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 0, 1, 2)
        self.lblProgress = QtGui.QLabel(MSICreationPage)
        self.lblProgress.setText(QtGui.QApplication.translate("MSICreationPage", "Progress:", None, QtGui.QApplication.UnicodeUTF8))
        self.lblProgress.setObjectName(_fromUtf8("lblProgress"))
        self.gridLayout_2.addWidget(self.lblProgress, 2, 0, 1, 1)
        self.lblProgressInfo = QtGui.QLabel(MSICreationPage)
        self.lblProgressInfo.setText(_fromUtf8(""))
        self.lblProgressInfo.setObjectName(_fromUtf8("lblProgressInfo"))
        self.gridLayout_2.addWidget(self.lblProgressInfo, 2, 1, 1, 1)
        self.progressBar = QtGui.QProgressBar(MSICreationPage)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout_2.addWidget(self.progressBar, 3, 0, 1, 2)

        self.retranslateUi(MSICreationPage)
        QtCore.QMetaObject.connectSlotsByName(MSICreationPage)

    def retranslateUi(self, MSICreationPage):
        pass


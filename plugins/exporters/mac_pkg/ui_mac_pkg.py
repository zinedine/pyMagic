# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui_mac_pkg.ui'
#
# Created: Thu Nov 24 09:48:44 2011
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_PackageCreationPage(object):
    def setupUi(self, PackageCreationPage):
        PackageCreationPage.setObjectName(_fromUtf8("PackageCreationPage"))
        PackageCreationPage.resize(812, 448)
        self.gridLayout_3 = QtGui.QGridLayout(PackageCreationPage)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.gbSimple = QtGui.QGroupBox(PackageCreationPage)
        self.gbSimple.setFocusPolicy(QtCore.Qt.NoFocus)
        self.gbSimple.setCheckable(True)
        self.gbSimple.setObjectName(_fromUtf8("gbSimple"))
        self.gridLayout_2 = QtGui.QGridLayout(self.gbSimple)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.lblPackageName = QtGui.QLabel(self.gbSimple)
        self.lblPackageName.setObjectName(_fromUtf8("lblPackageName"))
        self.gridLayout_2.addWidget(self.lblPackageName, 0, 0, 1, 1)
        self.lblPackageIdent = QtGui.QLabel(self.gbSimple)
        self.lblPackageIdent.setObjectName(_fromUtf8("lblPackageIdent"))
        self.gridLayout_2.addWidget(self.lblPackageIdent, 1, 0, 1, 1)
        self.lineEditPackageIdent = QtGui.QLineEdit(self.gbSimple)
        self.lineEditPackageIdent.setObjectName(_fromUtf8("lineEditPackageIdent"))
        self.gridLayout_2.addWidget(self.lineEditPackageIdent, 1, 1, 1, 1)
        self.lblPackageVersion = QtGui.QLabel(self.gbSimple)
        self.lblPackageVersion.setObjectName(_fromUtf8("lblPackageVersion"))
        self.gridLayout_2.addWidget(self.lblPackageVersion, 2, 0, 1, 1)
        self.lineEditPackageVersion = QtGui.QLineEdit(self.gbSimple)
        self.lineEditPackageVersion.setObjectName(_fromUtf8("lineEditPackageVersion"))
        self.gridLayout_2.addWidget(self.lineEditPackageVersion, 2, 1, 1, 1)
        self.lblScriptsDir = QtGui.QLabel(self.gbSimple)
        self.lblScriptsDir.setObjectName(_fromUtf8("lblScriptsDir"))
        self.gridLayout_2.addWidget(self.lblScriptsDir, 3, 0, 1, 1)
        self.lineEditScriptsDirectory = QtGui.QLineEdit(self.gbSimple)
        self.lineEditScriptsDirectory.setText(_fromUtf8(""))
        self.lineEditScriptsDirectory.setDragEnabled(True)
        self.lineEditScriptsDirectory.setObjectName(_fromUtf8("lineEditScriptsDirectory"))
        self.gridLayout_2.addWidget(self.lineEditScriptsDirectory, 3, 1, 1, 1)
        self.pbScriptsDirectory = QtGui.QPushButton(self.gbSimple)
        self.pbScriptsDirectory.setObjectName(_fromUtf8("pbScriptsDirectory"))
        self.gridLayout_2.addWidget(self.pbScriptsDirectory, 3, 2, 1, 1)
        self.lblOutputDir = QtGui.QLabel(self.gbSimple)
        self.lblOutputDir.setObjectName(_fromUtf8("lblOutputDir"))
        self.gridLayout_2.addWidget(self.lblOutputDir, 4, 0, 1, 1)
        self.lineEditOutputDirectory = QtGui.QLineEdit(self.gbSimple)
        self.lineEditOutputDirectory.setStatusTip(_fromUtf8(""))
        self.lineEditOutputDirectory.setText(_fromUtf8(""))
        self.lineEditOutputDirectory.setDragEnabled(True)
        self.lineEditOutputDirectory.setObjectName(_fromUtf8("lineEditOutputDirectory"))
        self.gridLayout_2.addWidget(self.lineEditOutputDirectory, 4, 1, 1, 1)
        self.pbOutputDirectory = QtGui.QPushButton(self.gbSimple)
        self.pbOutputDirectory.setObjectName(_fromUtf8("pbOutputDirectory"))
        self.gridLayout_2.addWidget(self.pbOutputDirectory, 4, 2, 1, 1)
        self.lblOutputDir_2 = QtGui.QLabel(self.gbSimple)
        self.lblOutputDir_2.setObjectName(_fromUtf8("lblOutputDir_2"))
        self.gridLayout_2.addWidget(self.lblOutputDir_2, 5, 0, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.rbPermissionsPreserve = QtGui.QRadioButton(self.gbSimple)
        self.rbPermissionsPreserve.setChecked(True)
        self.rbPermissionsPreserve.setObjectName(_fromUtf8("rbPermissionsPreserve"))
        self.horizontalLayout_3.addWidget(self.rbPermissionsPreserve)
        self.rbPermissionsRecommended = QtGui.QRadioButton(self.gbSimple)
        self.rbPermissionsRecommended.setObjectName(_fromUtf8("rbPermissionsRecommended"))
        self.horizontalLayout_3.addWidget(self.rbPermissionsRecommended)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.gridLayout_2.addLayout(self.horizontalLayout_3, 5, 1, 1, 1)
        self.lineEditPackageName = QtGui.QLineEdit(self.gbSimple)
        self.lineEditPackageName.setText(_fromUtf8(""))
        self.lineEditPackageName.setObjectName(_fromUtf8("lineEditPackageName"))
        self.gridLayout_2.addWidget(self.lineEditPackageName, 0, 1, 1, 1)
        self.gridLayout_3.addWidget(self.gbSimple, 0, 0, 1, 2)
        self.gbCustom = QtGui.QGroupBox(PackageCreationPage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gbCustom.sizePolicy().hasHeightForWidth())
        self.gbCustom.setSizePolicy(sizePolicy)
        self.gbCustom.setFocusPolicy(QtCore.Qt.NoFocus)
        self.gbCustom.setFlat(False)
        self.gbCustom.setCheckable(True)
        self.gbCustom.setChecked(False)
        self.gbCustom.setObjectName(_fromUtf8("gbCustom"))
        self.gridLayout = QtGui.QGridLayout(self.gbCustom)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblOutputDirCustom = QtGui.QLabel(self.gbCustom)
        self.lblOutputDirCustom.setObjectName(_fromUtf8("lblOutputDirCustom"))
        self.gridLayout.addWidget(self.lblOutputDirCustom, 0, 0, 1, 1)
        self.lineEditOutputDirectoryCustom = QtGui.QLineEdit(self.gbCustom)
        self.lineEditOutputDirectoryCustom.setObjectName(_fromUtf8("lineEditOutputDirectoryCustom"))
        self.gridLayout.addWidget(self.lineEditOutputDirectoryCustom, 0, 1, 1, 1)
        self.pbOutputDirectoryCustom = QtGui.QPushButton(self.gbCustom)
        self.pbOutputDirectoryCustom.setObjectName(_fromUtf8("pbOutputDirectoryCustom"))
        self.gridLayout.addWidget(self.pbOutputDirectoryCustom, 0, 2, 1, 1)
        self.gridLayout_3.addWidget(self.gbCustom, 1, 0, 1, 2)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.pbCreatePackage = QtGui.QPushButton(PackageCreationPage)
        self.pbCreatePackage.setObjectName(_fromUtf8("pbCreatePackage"))
        self.horizontalLayout_2.addWidget(self.pbCreatePackage)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.gridLayout_3.addLayout(self.horizontalLayout_2, 2, 0, 1, 2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lblProgress = QtGui.QLabel(PackageCreationPage)
        self.lblProgress.setObjectName(_fromUtf8("lblProgress"))
        self.horizontalLayout.addWidget(self.lblProgress)
        self.lblProgressInfo = QtGui.QLabel(PackageCreationPage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblProgressInfo.sizePolicy().hasHeightForWidth())
        self.lblProgressInfo.setSizePolicy(sizePolicy)
        self.lblProgressInfo.setText(_fromUtf8(""))
        self.lblProgressInfo.setObjectName(_fromUtf8("lblProgressInfo"))
        self.horizontalLayout.addWidget(self.lblProgressInfo)
        self.gridLayout_3.addLayout(self.horizontalLayout, 4, 0, 1, 2)
        self.progress = QtGui.QProgressBar(PackageCreationPage)
        self.progress.setProperty(_fromUtf8("value"), 24)
        self.progress.setObjectName(_fromUtf8("progress"))
        self.gridLayout_3.addWidget(self.progress, 5, 0, 1, 2)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem3, 3, 0, 1, 1)

        self.retranslateUi(PackageCreationPage)
        QtCore.QMetaObject.connectSlotsByName(PackageCreationPage)
        PackageCreationPage.setTabOrder(self.lineEditPackageName, self.lineEditPackageIdent)
        PackageCreationPage.setTabOrder(self.lineEditPackageIdent, self.lineEditPackageVersion)
        PackageCreationPage.setTabOrder(self.lineEditPackageVersion, self.lineEditScriptsDirectory)
        PackageCreationPage.setTabOrder(self.lineEditScriptsDirectory, self.pbScriptsDirectory)
        PackageCreationPage.setTabOrder(self.pbScriptsDirectory, self.lineEditOutputDirectory)
        PackageCreationPage.setTabOrder(self.lineEditOutputDirectory, self.pbOutputDirectory)
        PackageCreationPage.setTabOrder(self.pbOutputDirectory, self.rbPermissionsPreserve)
        PackageCreationPage.setTabOrder(self.rbPermissionsPreserve, self.rbPermissionsRecommended)
        PackageCreationPage.setTabOrder(self.rbPermissionsRecommended, self.lineEditOutputDirectoryCustom)
        PackageCreationPage.setTabOrder(self.lineEditOutputDirectoryCustom, self.pbOutputDirectoryCustom)
        PackageCreationPage.setTabOrder(self.pbOutputDirectoryCustom, self.pbCreatePackage)

    def retranslateUi(self, PackageCreationPage):
        PackageCreationPage.setWindowTitle(QtGui.QApplication.translate("PackageCreationPage", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.gbSimple.setToolTip(QtGui.QApplication.translate("PackageCreationPage", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Lucida Grande\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Build a simple PKG</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">A Mac PKG will be built, containing all of the files you have marked for inclusion at the scanning stage. </p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">This feature only allows the creation of &quot;simple&quot; packages, e.g. there is no way to control more advanced packaging features like meta-packages or OS requirements - for those types of packages, use the &quot;Build a DSTROOT&quot; option instead.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.gbSimple.setTitle(QtGui.QApplication.translate("PackageCreationPage", "Build a simple PKG", None, QtGui.QApplication.UnicodeUTF8))
        self.lblPackageName.setText(QtGui.QApplication.translate("PackageCreationPage", "Package Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.lblPackageIdent.setText(QtGui.QApplication.translate("PackageCreationPage", "Package identifier:", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditPackageIdent.setToolTip(QtGui.QApplication.translate("PackageCreationPage", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Lucida Grande\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Specify a unique identifier for this package.</span> </p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The Mac OS X Installer recognizes a package as being an upgrade to an already-installed package only if the package identifiers match, so it is advisable to set a meaningful, consistent identifier when you build the package.  </p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">pkgbuild will infer an identifier when building a package from a single component, but will fail otherwise if the identifier has not been set.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditPackageIdent.setPlaceholderText(QtGui.QApplication.translate("PackageCreationPage", "e.g. com.yourcompany.product-name", None, QtGui.QApplication.UnicodeUTF8))
        self.lblPackageVersion.setText(QtGui.QApplication.translate("PackageCreationPage", "Package version:", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditPackageVersion.setToolTip(QtGui.QApplication.translate("PackageCreationPage", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Lucida Grande\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Specify a version for the package. </span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-weight:600;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Packages with the same identifier are compared using this version, to determine if the package is an upgrade or downgrade. </p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">If you don\'t specify a version, a default of zero is assumed, but this may prevent proper upgrade/downgrade checking.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditPackageVersion.setPlaceholderText(QtGui.QApplication.translate("PackageCreationPage", "e.g 1.0", None, QtGui.QApplication.UnicodeUTF8))
        self.lblScriptsDir.setText(QtGui.QApplication.translate("PackageCreationPage", "Scripts directory:", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditScriptsDirectory.setToolTip(QtGui.QApplication.translate("PackageCreationPage", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Lucida Grande\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Archive the entire contents of scripts-path as the package scripts.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">If this directory contains scripts named preinstall and/or postinstall, these will be run as the top-level scripts of the package. </p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Any other files under scripts-path will be used only if the top-level or component-specific scripts invoke them.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditScriptsDirectory.setPlaceholderText(QtGui.QApplication.translate("PackageCreationPage", "optional", None, QtGui.QApplication.UnicodeUTF8))
        self.pbScriptsDirectory.setText(QtGui.QApplication.translate("PackageCreationPage", "Choose...", None, QtGui.QApplication.UnicodeUTF8))
        self.lblOutputDir.setText(QtGui.QApplication.translate("PackageCreationPage", "Output directory:", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditOutputDirectory.setToolTip(QtGui.QApplication.translate("PackageCreationPage", "The path to which the package will be written.", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditOutputDirectory.setPlaceholderText(QtGui.QApplication.translate("PackageCreationPage", "~/Desktop", None, QtGui.QApplication.UnicodeUTF8))
        self.pbOutputDirectory.setText(QtGui.QApplication.translate("PackageCreationPage", "Choose...", None, QtGui.QApplication.UnicodeUTF8))
        self.lblOutputDir_2.setText(QtGui.QApplication.translate("PackageCreationPage", "Permissions:", None, QtGui.QApplication.UnicodeUTF8))
        self.rbPermissionsPreserve.setToolTip(QtGui.QApplication.translate("PackageCreationPage", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Lucida Grande\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Permissions: Preserve</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-weight:600;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">This is the default, the permissions of the files as found on the disk during the scan are preserved.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.rbPermissionsPreserve.setText(QtGui.QApplication.translate("PackageCreationPage", "Preserve", None, QtGui.QApplication.UnicodeUTF8))
        self.rbPermissionsRecommended.setToolTip(QtGui.QApplication.translate("PackageCreationPage", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Lucida Grande\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Permissions: Recommened</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-weight:600;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Generally the permissions will be set to root:wheel, which ensures that files installed in the system domain are root-owned, while files installed in the user home directory will be owned by that user.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.rbPermissionsRecommended.setText(QtGui.QApplication.translate("PackageCreationPage", "Recommended", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditPackageName.setToolTip(QtGui.QApplication.translate("PackageCreationPage", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Lucida Grande\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Specify a unique identifier for this package.</span> </p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The Mac OS X Installer recognizes a package as being an upgrade to an already-installed package only if the package identifiers match, so it is advisable to set a meaningful, consistent identifier when you build the package.  </p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">pkgbuild will infer an identifier when building a package from a single component, but will fail otherwise if the identifier has not been set.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditPackageName.setPlaceholderText(QtGui.QApplication.translate("PackageCreationPage", "My New Package", None, QtGui.QApplication.UnicodeUTF8))
        self.gbCustom.setToolTip(QtGui.QApplication.translate("PackageCreationPage", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Lucida Grande\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Build a DSTROOT</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">This option will write a DSTROOT to the output directory you specify - as well as writing a COMPONENT PROPERTY LIST, which you can then feed to pkgbuild using the --compoent-plist command line option.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">For more information check the pkgbuild man page.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.gbCustom.setTitle(QtGui.QApplication.translate("PackageCreationPage", "Build a DSTROOT for customized/advanced PKG creation", None, QtGui.QApplication.UnicodeUTF8))
        self.lblOutputDirCustom.setText(QtGui.QApplication.translate("PackageCreationPage", "Output directory:", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditOutputDirectoryCustom.setToolTip(QtGui.QApplication.translate("PackageCreationPage", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Lucida Grande\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Specify where you would like the DSTROOT directory to be created. </span> </p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">A DSTROOT directory will be created at the path you specify, containing a copy of all of the files that you have marked to include within the package. </p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">You can then use the Mac OS X package maker and your own custom command line and configuration with this directory.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditOutputDirectoryCustom.setPlaceholderText(QtGui.QApplication.translate("PackageCreationPage", "~/Desktop", None, QtGui.QApplication.UnicodeUTF8))
        self.pbOutputDirectoryCustom.setText(QtGui.QApplication.translate("PackageCreationPage", "Choose...", None, QtGui.QApplication.UnicodeUTF8))
        self.pbCreatePackage.setText(QtGui.QApplication.translate("PackageCreationPage", "Create Package", None, QtGui.QApplication.UnicodeUTF8))
        self.lblProgress.setText(QtGui.QApplication.translate("PackageCreationPage", "Progress:", None, QtGui.QApplication.UnicodeUTF8))


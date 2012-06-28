from PyQt4.QtCore import QRegExp, QDir, QFileInfo, QProcess, QUrl, QSettings, Qt
from PyQt4.QtGui import QIcon, QWidget, QFileDialog, QMessageBox, QApplication, QDesktopServices

import os
import shutil, string
import tempfile
from ui_mac_pkg import Ui_PackageCreationPage
from widgets.export_data_widget import ExportDataWidget
import logging
logger = logging.getLogger(__name__)

class PackageCreationWidget(QWidget):
	def __init__(self, parent):
		super(PackageCreationWidget, self).__init__(parent)
		self.ui = Ui_PackageCreationPage()
		self.ui.setupUi(self)

		self.document = None

		# the push buttons to specify directories...
		self.ui.pbOutputDirectory.released.connect(self.__onChooseSimpleOutputDirectory)
		self.ui.pbOutputDirectoryCustom.released.connect(self.__onChooseCustomOutputDirectory)
		self.ui.pbScriptsDirectory.released.connect(self.__onChooseScriptsDirectory)
		self.ui.pbCreatePackage.released.connect(self.__createPackage)

		self.ui.gbCustom.clicked.connect(lambda x: self.__onGroupBoxSelected(True, x))
		self.ui.gbSimple.clicked.connect(lambda x: self.__onGroupBoxSelected(False, x))

		self.ui.lineEditPackageName.textChanged.connect(self.__fieldsValid)
		self.ui.lineEditOutputDirectory.textChanged.connect(self.__fieldsValid)
		self.ui.lineEditOutputDirectoryCustom.textChanged.connect(self.__fieldsValid)
		self.ui.lineEditPackageIdent.textChanged.connect(self.__fieldsValid)
		self.ui.lineEditPackageVersion.textChanged.connect(self.__fieldsValid)
		self.ui.lineEditScriptsDirectory.textChanged.connect(self.__fieldsValid)
		self.ui.rbPermissionsPreserve.clicked.connect(self.__fieldsValid)
		self.ui.rbPermissionsRecommended.clicked.connect(self.__fieldsValid)

		self.ui.lblProgress.linkActivated.connect(self.__onLinkActivated)
		self.ui.lblProgressInfo.linkActivated.connect(self.__onLinkActivated)

		self.__loadFields()
		self.__fieldsValid()
		self.__setProgressHidden(True)

	def initializePageWithDocument(self, document):
		self.document = document

	def __onGroupBoxSelected(self, isCustom, ison):
		self.ui.gbCustom.blockSignals(True)
		self.ui.gbSimple.blockSignals(True)

		if not isCustom:
			ison = not ison
			
		self.ui.gbCustom.setChecked(ison)
		self.ui.gbSimple.setChecked(not ison)
		self.__fieldsValid()

		self.ui.gbCustom.blockSignals(False)
		self.ui.gbSimple.blockSignals(False)

	def __onChooseSimpleOutputDirectory(self):
		dir_name = QFileDialog.getExistingDirectory(self, "Choose Output Directory")
		if len(dir_name) > 0:
			self.ui.lineEditOutputDirectory.setText(dir_name)
		self.parent().changed()

	def __onChooseCustomOutputDirectory(self):
		dir_name = QFileDialog.getExistingDirectory(self, "Choose Custom Output Directory")
		if len(dir_name) > 0:
			self.ui.lineEditOutputDirectoryCustom.setText(dir_name)
		self.parent().changed()

	def __onChooseScriptsDirectory(self):
		dir_name = QFileDialog.getExistingDirectory(self, "Choose Scripts Directory")
		if len(dir_name) > 0:
			self.ui.lineEditScriptsDirectory.setText(dir_name)
		self.parent().changed()

	def __enableExportControls(self, enabled):
		self.ui.pbCreatePackage.setEnabled(enabled)

	def __fieldsValid(self):
		res = False
		res3 = len(self.__userSpecifiedDSTROOT()) > 0

		if self.ui.gbSimple.isChecked():
			res1 = len(self.ui.lineEditPackageIdent.text()) > 0 and len(self.ui.lineEditPackageVersion.text()) > 0
			res2 = len(self.ui.lineEditPackageName.text()) > 0
			res = res1 and res2 and res3
		else:
			res = res3

		self.__enableExportControls(res)
		self.__saveFields()

		return res

	def isComplete(self):
		if self.document == None:
			return False
		return self.__fieldsValid()

	def __userSpecifiedDSTROOT(self):
		res = None
		if self.ui.gbSimple.isChecked():
			res = self.ui.lineEditOutputDirectory.text()
			if res is None or len(res) == 0:
				res = self.ui.lineEditOutputDirectory.placeholderText()
		else:
			res = self.ui.lineEditOutputDirectoryCustom.text()
			if res is None or len(res) == 0:
				res = self.ui.lineEditOutputDirectoryCustom.placeholderText()
		return os.path.expandvars(os.path.expanduser(res))

	def __createPackage(self):
		# get the destination directory, if it does not exist - prompt and create it
		dstroot = self.__userSpecifiedDSTROOT()
		if not os.path.exists(dstroot):
			opt = QMessageBox.warning(self, "Destination Doesn't Exist", "The destination directory does not exist:\r\n{}\r\n\nDo you want to create it?".format(dstroot))
			if opt != QMessageBox.StandardButton(QMessageBox.Ok):
				return
			os.makedirs(dstroot)
			if not os.path.exists(dstroot):
				QMessageBox.error(self, "Failed to Create Directory", "There was a problem creating the directory:\r\n{}".format(dstroot))
				return

		# check if the scripts dir is specified, if it is, then it must exist
		scripts_dir = self.ui.lineEditScriptsDirectory.text()
		if len(scripts_dir) > 0:
			if not os.path.exists(scripts_dir):
				res = QMessageBox.warning(self,\
				                          "Scripts Directory",\
				                          "The scripts directory you specified does not exist - if you continue, the package will be created without scripting support\r\n\nDo you want to continue?",\
				                          buttons = QMessageBox.StandardButton(QMessageBox.Ok + QMessageBox.Cancel))
				if res != QMessageBox.StandardButton(QMessageBox.Ok):
					return

		total_items = self.document.countScanningResults()
		self.__prepareProgress("Copying data files ...", total_items)

		# create a new DSTROOT
		the_dir = os.path.join(dstroot, "DSTROOT")
		if not os.path.exists(the_dir):
			os.makedirs(the_dir)
		self.dstroot_path = tempfile.mkdtemp(dir=the_dir)
		self.package_name = self.ui.lineEditPackageName.text()

		# grab all the stuff we're supposed to export, and write it into a DSTROOT, then point
		# pkgbuild at it.
		# 1. construct a DSTROOT
		# 2. decide whether to run an analysis or create the pkg
		# 3. done.
		word = "DSTROOT creation"
		pkg_process = True

		if self.__createDSTRoot():
			if self.ui.gbSimple.isChecked():
				word = "creation"
				self.__prepareProgress("Constructing PKG...")
				pkg_process = self.__constructPackage()
			else:
				word = "analysis"
				self.__prepareProgress("Analyzing PKG...")
				pkg_process = self.__analyzePackage()

			html = "<a href='{}'>{}</href>".format(self.dstroot_path, self.dstroot_path)
			if pkg_process:
				pkg_result = "Package {} completed OK ({})".format(word, html)
			else:
				pkg_result = "Package {} failed to complete because of the packaging command failed (check logs)".format(word)
		else:
			pkg_result = "Package {} failed (check logs)".format(word)

		self.__finishProgress(pkg_result)

	def __runPackagingCommand(self, command_line):
		self.ui.pbCreatePackage.setEnabled(False)
		try:
			logger.info("going to run command: {0}".format(command_line))
			
			proc = QProcess()
			proc.startDetached(command_line)
			proc.waitForFinished(-1)

			# note: you are looking here, probably because the PKG command failed, but it wasn't caught - I've noticed that
			# the waitForFinished() will always return False (the command runs too quick on analysis for example?), and exitStatus()
			# isn't reliable when a failure occurs anyway.  Useless....
			if proc.exitStatus() != QProcess.NormalExit:
				QMessageBox.critical(self, "Packaging Error", "The packaging process failed to finish properly")
				return False
			return True
		finally:
			self.ui.pbCreatePackage.setEnabled(True)

	def __analyzePackage(self):
		path = self.dstroot_path
		plist = os.path.join(os.path.dirname(path), os.path.basename(path) + ".plist")
		cmd_line = "/usr/bin/pkgbuild --analyze --root {} {}".format(path, plist)

		return self.__runPackagingCommand(cmd_line)

	def __constructPackage(self):
		path = self.dstroot_path
		pkg = os.path.join(os.path.dirname(path), self.package_name + ".pkg")
		ident = self.ui.lineEditPackageIdent.text()
		ver = self.ui.lineEditPackageVersion.text()
		scripts = self.ui.lineEditScriptsDirectory.text()
		if len(scripts) > 0 and os.path.exists(scripts):
			cmd_line = "/usr/bin/pkgbuild --identifier {} --version {} --scripts \"{}\" --root \"{}\" \"{}\"".format(ident, ver, scripts, path, pkg)
		else:
			# this one doesn't spec the scripts path
			cmd_line = "/usr/bin/pkgbuild --identifier {} --version {} --root \"{}\" \"{}\"".format(ident, ver, path, pkg)

		return self.__runPackagingCommand(cmd_line)

	def __createDSTRoot(self):
		errors = []

		counter = 0
		for scan_record in self.document.iterateScanningResults():
			counter += 1

			source_path = scan_record.abs_path

			# goal: remove leading '/' so that join does the right thing
			final_dest = os.path.join(self.dstroot_path, source_path[1:])

			parent = os.path.split(final_dest)[0]
			if parent is not None and len(parent) > 0 and not os.path.exists(parent):
				os.makedirs(parent)

			self.__setProgress(counter, source_path)

			try:
				if os.path.islink(source_path):
					linkto = os.readlink(source_path)
					os.symlink(linkto, final_dest)
				elif os.path.isfile(source_path):
					shutil.copy2(source_path, final_dest)
				elif os.path.isdir(source_path):
					if not os.path.exists(final_dest):
						os.makedirs(final_dest)
					shutil.copystat(source_path, final_dest)
			except (IOError, os.error), why:
				errors.append((source_path, final_dest, str(why)))

		return len(errors) == 0

	def __setProgressHidden(self, hide):
		self.ui.progress.setHidden(hide)
		self.ui.lblProgress.setHidden(hide)
		self.ui.lblProgressInfo.setHidden(hide)

	def __prepareProgress(self, text, max_value = None):
		self.ui.progress.setMinimum(0)
		self.ui.progress.setMaximum(0)
		if max_value is not None:
			self.ui.progress.setMaximum(max_value)
		self.ui.lblProgressInfo.setText(text)
		self.ui.lblProgress.setText("Progress:")
		self.__setProgressHidden(False)

	def __setProgress(self, actual, source_path):
		self.ui.progress.setValue(actual)
		self.ui.lblProgressInfo.setText(source_path)
		QApplication.processEvents()

	def __finishProgress(self, text):
		self.__setProgressHidden(True)
		self.ui.lblProgress.setHidden(False)
		self.ui.lblProgress.setText(text)

	def __onLinkActivated(self, link_str):
		QDesktopServices.openUrl(QUrl.fromLocalFile(link_str))

	def __writeSettingsStr(self, settings, key, callable_str):
		if len(callable_str()) > 0:
			settings.setValue(key, callable_str())

	def __readSettingsStrToLineEdit(self, settings, key, line_edit):
		if settings.contains(key):
			value = settings.value(key, "").toString()
			line_edit.setText(value)

	def __saveFields(self):
		settings = QSettings()
		self.__writeSettingsStr(settings, "magic_plugin_pkg__package_name", lambda: self.ui.lineEditPackageName.text())
		self.__writeSettingsStr(settings, "magic_plugin_pkg__package_ident", lambda: self.ui.lineEditPackageIdent.text())
		self.__writeSettingsStr(settings, "magic_plugin_pkg__package_version", lambda: self.ui.lineEditPackageVersion.text())
		self.__writeSettingsStr(settings, "magic_plugin_pkg__scripts_directory", lambda: self.ui.lineEditScriptsDirectory.text())
		self.__writeSettingsStr(settings, "magic_plugin_pkg__output_directory", lambda: self.ui.lineEditOutputDirectory.text())
		self.__writeSettingsStr(settings, "magic_plugin_pkg__output_directory_custom", lambda: self.ui.lineEditOutputDirectoryCustom.text())

		if self.ui.gbSimple.isChecked():
			settings.setValue("magic_plugin_pkg__simple_or_custom", "simple")
		else:
			settings.setValue("magic_plugin_pkg__simple_or_custom", "custom")

		if self.ui.rbPermissionsPreserve.isChecked():
			settings.setValue("magic_plugin_pkg__permissions", "preserve")
		else:
			settings.setValue("magic_plugin_pkg__permissions", "recommended")

	def __loadFields(self):
		settings = QSettings()
		self.__readSettingsStrToLineEdit(settings, "magic_plugin_pkg__package_name", self.ui.lineEditPackageName)
		self.__readSettingsStrToLineEdit(settings, "magic_plugin_pkg__package_ident", self.ui.lineEditPackageIdent)
		self.__readSettingsStrToLineEdit(settings, "magic_plugin_pkg__package_version", self.ui.lineEditPackageVersion)
		self.__readSettingsStrToLineEdit(settings, "magic_plugin_pkg__scripts_directory", self.ui.lineEditScriptsDirectory)
		self.__readSettingsStrToLineEdit(settings, "magic_plugin_pkg__output_directory", self.ui.lineEditOutputDirectory)
		self.__readSettingsStrToLineEdit(settings, "magic_plugin_pkg__output_directory_custom", self.ui.lineEditOutputDirectoryCustom)

		value = settings.value("magic_plugin_pkg__permissions", "preserve")
		if value == "preserve":
			self.ui.rbPermissionsPreserve.setChecked(True)
		else:
			self.ui.rbPermissionsRecommended.setChecked(True)

		if settings.contains("magic_plugin_pkg__simple_or_custom"):
			if settings.value("magic_plugin_pkg__simple_or_custom").toString() == "simple":
				self.ui.gbSimple.setChecked(True)
				self.ui.gbCustom.setChecked(False)
			else:
				self.ui.gbCustom.setChecked(True)
				self.ui.gbSimple.setChecked(False)


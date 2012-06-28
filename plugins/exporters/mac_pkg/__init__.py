"""
This package exposes the ability to configure and create a Mac PKG from a merge_scan.
"""
from PyQt4.QtGui import QIcon
from plugins.exporters.mac_pkg.package_creation_widget import PackageCreationWidget
from resources_rc import *

def name():
	return "Mac Installer PKG"

def description():
	return "Creates a simple PKG, or a DSTROOT for customized Mac packages"

def icon():
	return QIcon(":/icons/package_icon.png")

def createExportUI(parent):
	return PackageCreationWidget(parent)

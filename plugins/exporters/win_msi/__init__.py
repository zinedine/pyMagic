
from PyQt4.QtGui import QIcon
from plugins.exporters.win_msi.msi_creation_widget import MSICreationWidget
from msiResources_rc import *

def name():
    return "msi package Installer"

def description():
    return "creates a msi package installer from a DSTRoot"

def icon():
    return QIcon(":/icons/msi_icon.gif") 

def template():
    return ":/files/pyMagicTemplateMSI.msi"

def createExportUI(parent):
    return MSICreationWidget(parent)

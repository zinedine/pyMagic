import sip
sip.setapi('QString', 2)

import sys, os
from PyQt4.QtCore import QCoreApplication

# VERY important, importing this module monkey patches Win32 os routines to have super-powers (like; can detect symlinks)
from lib.platform import Platform
import logging

# TIP: its important that the imports DO NOT happen before the Org/App name has been set up, otherwise the QSettings
# can potentially be instantiated *before* its defaults are ready
a = QCoreApplication(sys.argv)
a.setOrganizationName("FileWave")
a.setApplicationName("UnitTest")

#from test_build_tree_model import *
from test_directory_scanner import *
from test_document_storage import *
from test_path_info import *
from test_persistent_scanning_state import *
from test_exclusion_rules import *
from test_plugins import *
from tests.utils import start_figleaf, close_figleaf

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s, %(levelname)s: %(message)s',  datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    #fig_started = start_figleaf()

    # ERASE all settings.
    settings = QSettings()
    settings.clear()
    settings.sync()

    unittest.main(exit=False)

# NOT USING FIGLEAF - no point when "coverage" tool is so much better, see also: run.sh
#	if Platform.isMac:
#		if fig_started:
#			close_figleaf()
#			os.system("cd {} && {} figleaf2html.py -d html .unittest_coverage".format(os.getcwd(), sys.executable))
#			os.system("cd {} && open html/index.html".format(os.getcwd()))
#		else:
#			print "Figleaf coverage disabled; as it didn't start properly"

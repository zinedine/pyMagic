# this makes sure that QString's are converted to Python strings - so that routines expecting python
# strings don't blow up with type incompatibility issues - it must be the first line in the file.
import sip
sip.setapi('QString', 2)

# VERY important, importing this module monkey patches Win32 os routines to have super-powers (like; can detect symlinks)
from lib.platform import Platform

from widgets.logging_widget import LoggingWidget
from PyQt4.QtGui import QMainWindow, QApplication, QMessageBox
import sys

main_app = QApplication(sys.argv)

# these two don't look like they are used - but they are required so that the PyInstaller
# packaging properly picks up the dependencies to the modules (note: these are not used any longer - but its nice to know how to
# force refs to modules, right?)  ....   and I'm leaving it in cos it does no harm.
from PyQt4.QtSql import QSqlDatabase
from PyQt4.QtCore import QSettings

# so that the settings get a sane name throughout the program
main_app.setOrganizationName("FileWave")
main_app.setApplicationName("PyMagic")

from widgets.scan_wizard import ScanWizard
from ui.app_window_and_menu import Ui_MainWindow
from widgets.preferences_widget import PreferencesWidget

import os, sys

import logging
logger = logging.getLogger(__name__)

class DummyMainWindow(QMainWindow):
    def __init__(self, parent):
        super(DummyMainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

def submitBugReport():
    QMessageBox.information(None, "Prototype Idea", "Submit a bug report direct from the tool - it can collect the database (in compressed form), the current search expressions etc - allow you to enter a description of the problem, attach files and then get this to the right people at FileWave... \r\n\na good idea right?\n\nStay tuned...")

def run_app():
    # these addLibraryPath lines force the current runtime/exe directory to be part of the library
    # dll load path - making the resource system capable of loading libqsqlite.dylib and friends
    d = "qt4_plugins"
    d = os.path.join(os.path.dirname(sys.argv[0]), d)
    main_app.addLibraryPath(os.path.abspath(d))
    logger.debug("lib paths are now: {0}".format(main_app.libraryPaths()))
    logger.debug("app dir path is: {0}".format(main_app.applicationDirPath()))

    # the window is instantiated but NEVER SHOWN, only doing this so I have an easy way
    # of editing the QMenu items via the Designer
    dummy = DummyMainWindow(None)
    menubar = dummy.ui.menubar

    main_gui = ScanWizard()
    menubar.setParent(main_gui)

    dummy.ui.actionSubmit_Bug_Report.triggered.connect(lambda: submitBugReport())

    # logging window - hook up exception handler asap
    dummy.ui.actionShow_Log.triggered.connect(lambda: logging.show())

    # preferences window
    prefs = PreferencesWidget()
    dummy.ui.actionPreferences.triggered.connect(lambda: prefs.show())

    sheet = """
    QWidget#filterContainer {
        background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(120, 120, 120, 255), stop:1 rgba(120, 120, 120, 120))
    }

    QToolButton[styled="true"] {
        border: 1px solid #b0b0b0;
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                 stop: 0 #eeeeee, stop: 0.4 #ffffff,
                                 stop: 0.5 #e3e3e3, stop: 1.0 #efefef);
        color:#505050;
    }

    QToolButton[styled="true"]:hover {
        border: 1px solid gray;
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                 stop: 0 #eeeeee, stop: 0.4 #ffffff,
                                 stop: 0.5 #e3e3e3, stop: 1.0 #efefef);
        color: #505050;
    }

    QToolButton[styled="true"]:pressed {
        border: 1px solid gray;
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                 stop: 0 #dddddd, stop: 0.4 #eeeeee,
                                 stop: 0.5 #d3d3d3, stop: 1.0 #dfdfdf);
        color: #505050;
    }

    """

    if Platform.isMac:
        main_app.setStyleSheet(sheet)

    main_gui.show()
    main_gui.raise_()

    # delay load the exception hook, in case
    logging = LoggingWidget()
    logging.installExceptHook()

    main_app.exec_()

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s, %(levelname)s: %(message)s',  datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
    run_app()

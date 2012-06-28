from PyQt4.Qt import Qt
from PyQt4.QtCore import QSettings
from PyQt4.QtGui import QWidget
from ui.logging import Ui_LoggingWidget
import sys
import traceback
import datetime
import logging
logger = logging.getLogger(__name__)

class LoggingWidget(QWidget):
	def __init__(self, widget = None):
		super(LoggingWidget, self).__init__(widget)
		self.ui = Ui_LoggingWidget()
		self.ui.setupUi(self)
		self.ui.buttonClearLog.clicked.connect(self.__clearLog)
		self.ui.buttonBox.rejected.connect(self.close)

		settings = QSettings()
		is_checked = settings.value("show_error_log_when_exception_occurs", True).toBool()
		self.ui.cbShowOnError.setChecked(is_checked)
		self.ui.cbShowOnError.clicked.connect(self.__showFlagChanged)

		self.__clearLog()

	def installExceptHook(self):
		sys.excepthook = lambda t, v, tb: self.__exceptHook(t, v, tb)

	def __exceptHook(self, type, value, tb):
		the_time = datetime.datetime.now()
		time_str = the_time.strftime("%Y-%m-%d %H:%M:%S")

		message = time_str + ', exception:\n'
		message += ''.join(traceback.format_exception(type, value, tb))
		logger.critical(message)

		self.ui.plainTextEdit.appendPlainText(message)
		self.ui.plainTextEdit.appendPlainText("-----------------------------------------------------------------")

		if self.ui.cbShowOnError.isChecked():
			self.show()
			self.raise_()

	def __clearLog(self):
		self.ui.plainTextEdit.clear()

	def __showFlagChanged(self):
		settings = QSettings()
		settings.setValue("show_error_log_when_exception_occurs", self.ui.cbShowOnError.isChecked())


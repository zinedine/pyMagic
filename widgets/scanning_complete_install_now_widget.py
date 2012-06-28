
from PyQt4.Qt import *
from ui.scanning_complete_install_now import Ui_ScanningCompleteInstallNow
from widgets.constants import WizardPage
import logging
logger = logging.getLogger(__name__)

class ScanningCompleteInstallNowWidget(QWizardPage):
	def __init__(self):
		super(ScanningCompleteInstallNowWidget, self).__init__()

		self.ui = Ui_ScanningCompleteInstallNow()
		self.ui.setupUi(self)
		self.ui.buttonFindChanges.clicked.connect(self.__onFindChanges)
		self.scanner = None

		self.setTitle("The Initial Scan is Complete!")
		
		self.setButtonText(QWizard.NextButton, "Quit")

	def nextIdForWizard(self):
		if self.__find_changes and self.isComplete():
			return WizardPage.SECOND_SCAN_PROGRESS
		return -1

	def initializePage(self):
		self.ui.labelDocumentName.setText(self.wizard().documentName())
		self.__find_changes = False

		# REMOVE the first scanning progress page, we DO NOT want to go back to it when back() is pressed - and the
		# only way to stop QWizard from doing this is to remove the bloody thing entirely - if it aint there, it's hard to view it.
		# The create scan page will add it back in if required.
		self.wizard().removePage(WizardPage.FIRST_SCAN_PROGRESS)

	def __onFindChanges(self):
		logger.debug("would find changes")
		self.__find_changes = True
		if self.isComplete():
			self.wizard().next()

	def isComplete(self):
		return self.scanner is None


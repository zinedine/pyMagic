
# is the mother of all wizards used to control the program flow for all of the
# creation, selection etc.
from PyQt4.QtCore import Qt, QRect, QSettings, QPropertyAnimation, QEasingCurve
from PyQt4.QtGui import QWizard, QPixmap, QApplication
from plugins.exporters.plugin import ExporterPlugin
from widgets.constants import WizardPage
from widgets.compare_two_scans_widget import CompareTwoScansWidget
from widgets.create_new_scan_widget import CreateNewScanWidget
from widgets.export_data_widget import ExportDataWidget
from widgets.geometry_helper import GeometryHelper
from widgets.instructions_widget import InstructionsWidget
from widgets.list_existing_scans_widget import ListOfExistingScanFilesWidget
from widgets.scanning_complete_install_now_widget import ScanningCompleteInstallNowWidget
from widgets.scanning_progress_wizpage import ScanningProgressWizpage
from widgets.select_export_type_widget import SelectExportTypeWidget
import logging
logger = logging.getLogger(__name__)

class ScanningMode:
	SHOW_INTRO = 1
	CREATE_NEW = 2
	SELECT_EXISTING = 3

class ScanWizard(QWizard):
	def __init__(self, owner = None):
		super(ScanWizard, self).__init__(owner)

		self.__document_name = None

		#self.setOption(QWizard.NoBackButtonOnStartPage)
		self.setOptions(QWizard.NoDefaultButton | QWizard.NoBackButtonOnStartPage | QWizard.NoCancelButton)
		self.mode = ScanningMode.SHOW_INTRO
		self.geo = GeometryHelper()
		self.setOption(QWizard.HaveHelpButton, False)

		wavePixmap = QPixmap(":/icons/icons/wave.png")
		self.setPixmap(QWizard.BackgroundPixmap, wavePixmap.scaledToWidth(160, Qt.SmoothTransformation))

		# wizard pages
		self.introPage = InstructionsWidget()
		self.createNewScanPage = CreateNewScanWidget()
		self.firstScanProgressPage = ScanningProgressWizpage(True)
		self.secondScanProgressPage = ScanningProgressWizpage(False)
		self.scanningCompleteInstallNow = ScanningCompleteInstallNowWidget()
		self.listOfExistingScans = ListOfExistingScanFilesWidget()
		self.compareTwoScans = CompareTwoScansWidget()
		self.selectExportType = SelectExportTypeWidget()
		self.exportDataPage = ExportDataWidget()

		self.setPage(WizardPage.INTRO, self.introPage)
		self.setPage(WizardPage.CREATE_NEW, self.createNewScanPage)
		self.setPage(WizardPage.LIST_OF_EXISTING_SCANS, self.listOfExistingScans)
		self.setPage(WizardPage.COMPARE_TWO_SCANS, self.compareTwoScans)
		self.setPage(WizardPage.SELECT_EXPORT_TYPE, self.selectExportType)
		self.setPage(WizardPage.EXPORT_DATA, self.exportDataPage)

		self.introPage.beforeInstalling.connect(self.onNewScan)
		self.introPage.afterInstalling.connect(self.onSelectExistingScan)

		#self.__current_anim = None

		# hook 'next/continue' button, so if its hit on page 1 - we can quit
		self.button(QWizard.NextButton).clicked.connect(self.onNextButtonHit)
		self.currentIdChanged.connect(self.onPageChanged)

		#self.setWizardStyle(QWizard.ModernStyle)
		self.setStartId(WizardPage.INTRO)

	def reinsertFirstProgressPage(self):
		self.setPage(WizardPage.FIRST_SCAN_PROGRESS, self.firstScanProgressPage)

	def reinsertSecondProgressPage(self):
		self.setPage(WizardPage.SECOND_SCAN_PROGRESS, self.secondScanProgressPage)

	def reinsertScanCompletePage(self):
		self.setPage(WizardPage.SCANNING_COMPLETE_INSTALL_NOW, self.scanningCompleteInstallNow)

	def reinsertCreateScanPage(self):
		self.setPage(WizardPage.CREATE_NEW, self.createNewScanPage)

	def onPageChanged(self, new_page):
		logger.debug("the page has been changed to: {0}".format(new_page))
		logger.debug("")

		if new_page == WizardPage.CREATE_NEW:
			self.reinsertFirstProgressPage()
		if new_page == WizardPage.FIRST_SCAN_PROGRESS or new_page == WizardPage.SECOND_SCAN_PROGRESS or new_page == WizardPage.LIST_OF_EXISTING_SCANS:
			self.reinsertSecondProgressPage()
			self.reinsertScanCompletePage()
			self.setWindowFilePath("")

	@staticmethod
	def createAnimationFromToFor(widget, fromValue, toValue, duration, propName, curve = QEasingCurve.InOutCubic):
		anim = QPropertyAnimation(widget, propName)
		anim.setDuration(duration)
		anim.setStartValue(fromValue)
		anim.setEndValue(toValue)
		anim.setEasingCurve(curve)
		return anim

	@staticmethod
	def animatePropertyWidgetTo(widget, prop_name, end_value, animate = True):
		current_value = widget.property(prop_name)
		dur = 250
		if not animate:
			dur = 0

		anim = None
		if current_value != end_value:
			anim = ScanWizard.createAnimationFromToFor(widget, current_value, end_value, dur, prop_name)

		return anim

	def showEvent(self, evt):
		data = self.geo.load("mainWindow")
		if data is not None:
			self.restoreGeometry(data)
		else:
			self.setGeometry(QRect(40, 60, 700, 400))

	def closeEvent(self, evt):
		self.geo.save(self.saveGeometry(), "mainWindow")
		super(ScanWizard, self).closeEvent(evt)

	def onNewScan(self):
		self.mode = ScanningMode.CREATE_NEW
		self.next()

	def onSelectExistingScan(self):
		self.mode = ScanningMode.SELECT_EXISTING
		self.next()

	def onNextButtonHit(self):
		# cause app quit when no mode has been selected
		if self.mode == ScanningMode.SHOW_INTRO and self.currentId() == WizardPage.INTRO:
			QApplication.quit()

	def nextId(self):
		res = self._nextId()
		logger.debug("nextId called, current page: {0}, next page id: {1}".format(self.currentId(), res))
		return res
	
	def _nextId(self):
		c = self.currentId()

		if c == WizardPage.INTRO:
			if self.mode == ScanningMode.SHOW_INTRO:
				return WizardPage.INTRO
			if self.mode == ScanningMode.CREATE_NEW:
				return WizardPage.CREATE_NEW
			if self.mode == ScanningMode.SELECT_EXISTING:
				return WizardPage.LIST_OF_EXISTING_SCANS

		if c == WizardPage.CREATE_NEW:
			return WizardPage.FIRST_SCAN_PROGRESS

		if c == WizardPage.FIRST_SCAN_PROGRESS:
			return WizardPage.SCANNING_COMPLETE_INSTALL_NOW

		if c == WizardPage.SCANNING_COMPLETE_INSTALL_NOW:
			# no way to pass this point unless the widget allows it...
			return self.scanningCompleteInstallNow.nextIdForWizard()

		if c == WizardPage.LIST_OF_EXISTING_SCANS:
			isSecondDone = self.field("secondScanComplete").toBool()
			if isSecondDone:
				return WizardPage.COMPARE_TWO_SCANS
			return WizardPage.SECOND_SCAN_PROGRESS

		if c == WizardPage.SECOND_SCAN_PROGRESS:
			return WizardPage.COMPARE_TWO_SCANS

		if c == WizardPage.COMPARE_TWO_SCANS:
			return WizardPage.SELECT_EXPORT_TYPE

		if c == WizardPage.SELECT_EXPORT_TYPE:
			if len(ExporterPlugin.allExporterPlugins()) > 0:
				return WizardPage.EXPORT_DATA
			return -1

		if c == WizardPage.EXPORT_DATA:
			return self.exportDataPage.nextId()

		return -1

	def scanPaths(self):
		paths = [ path.toString() for path in self.field("scanPaths").toList() ]
		return paths

	def setDocumentName(self, value):
		self.__document_name = value

	def documentName(self):
		return self.__document_name


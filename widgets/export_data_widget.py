from PyQt4.QtGui import QWidget, QWizardPage, QGridLayout, QVBoxLayout, QLabel
from lib.document_storage import DocumentStorage
from lib.persistent_scanning_state import PersistentScanningState
from plugins.exporters.plugin import ExporterPlugin

class ExportDataWidget(QWizardPage):
	"""
	Wraps up whatever UI the plugin provides in a container QWidget (throwing away the old widget as required).
	There is no nextId() provided for widgets wrapped in this container - its the end of the road here.
	"""
	def __init__(self, parent = None):
		super(QWizardPage, self).__init__(parent)
		self.setTitle("Export Options")
		self.gridLayout = QGridLayout(self)
		self.plugin = None

	def nextId(self):
		# if no more pages, then return -1
		return -1

	def isComplete(self):
		if self.plugin is None:
			return False
		return self.plugin.ui.isComplete()

	def __createExportUI(self, document, parent):
		if self.plugin is None:
			raise Exception("self.plugin isn't set when __createExportUI was called")
		self.plugin.ui = self.plugin.createExportUI(parent)
		self.plugin.ui.initializePageWithDocument(document)
		return self.plugin.ui

	def changed(self):
		self.completeChanged.emit()

	def initializePage(self):
		"""
		Find and load the persistent document, create the export UI and insert it into the 'container'.  This
		method assumes that the wizard has a documentName set.
		"""

		self.container = QWidget(self)

		if self.plugin is not None:
			self.plugin.ui.setParent(None)
			self.gridLayout.removeWidget(self.plugin.ui)
			self.plugin.ui = None
			self.plugin = None

		name_of_file = self.wizard().documentName()
		document = PersistentScanningState(DocumentStorage.documentFullPath(name_of_file))

		self.plugin = self.__createPluginNamed(self.field("exportType").toString())
		ui = self.__createExportUI(document, self.container)
		self.gridLayout.addWidget(ui)

		self.changed()

	def __createPluginNamed(self, plugin_name):
		if ExporterPlugin.isValidPluginModule(plugin_name):
			plugin = ExporterPlugin(plugin_name)
			return plugin
		return None



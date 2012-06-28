from PyQt4.Qt import *
from lib.persistent_scanning_state import PersistentScanningState
from plugins.exporters.plugin import ExporterPlugin
from ui.select_export_type import Ui_SelectExportType
from widgets.constants import WizardPage
import logging
logger = logging.getLogger(__name__)

class SelectExportTypeWidget(QWizardPage):
	def __init__(self):
		super(QWizardPage, self).__init__()

		self.ui = Ui_SelectExportType()
		self.ui.setupUi(self)

		self.setTitle("Select Export Type")
		self.setSubTitle("Pick the type of export you'd like make from the list below.")

		self.registerField('exportType*', self.ui.listExportTypes)

		self.ui.listExportTypes.setAttribute(Qt.WA_MacShowFocusRect, False)
		self.ui.listExportTypes.doubleClicked.connect(self.__onListItemDoubleClicked)

		self.document_name = None

	def __onListItemDoubleClicked(self, itemWidget):
		if self.isComplete():
			self.wizard().next()

	def __onListItemSelectionChanged(self):
		self.completeChanged.emit()

	def __createStandardItemForPlugin(self, plugin, one_liner = None):
		item = None

		if one_liner is not None:
			item = QStandardItem(one_liner)
		elif plugin is not None:
			if plugin.icon is not None and plugin.name is not None:
				item = QStandardItem(plugin.icon, plugin.name)
			else:
				item = QStandardItem(plugin.name)
			item.setData(plugin.module, Qt.UserRole)
			item.setData(plugin.description, Qt.ToolTipRole)

		return item

	def initializePage(self):
		model = QStandardItemModel()
		rootItem = model.invisibleRootItem()

		# find all the appropriate plugins for export
		try:
			for plugin in ExporterPlugin.allExporterPlugins():
				item = self.__createStandardItemForPlugin(plugin)
				if item is not None:
					rootItem.appendRow(item)
		except Exception, e:
			logger.critical("during export, an exception occured: {0}".format(e))

		if model.rowCount() == 0:
			rootItem.appendRow(self.__createStandardItemForPlugin(None, "No exporter plugins found"))
			self.ui.listExportTypes.setSelectionMode(QAbstractItemView.NoSelection)

		# set the model first - then the selectionModel (order is important)
		self.ui.listExportTypes.setModel(model)
		self.ui.listExportTypes.selectionModel().selectionChanged.connect(self.__onListItemSelectionChanged)

		# select the item is there's only one in the model - makes it one step easier
		if model.rowCount() == 1:
			self.ui.listExportTypes.selectAll()

	def isComplete(self):
		done = self.ui.listExportTypes.selectionModel().hasSelection()
		if done:
			index = self.ui.listExportTypes.selectionModel().currentIndex()
			self.setField("exportType", index.data(Qt.UserRole).toString())
		return done

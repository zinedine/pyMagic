from lib.platform import Platform

class ExporterPlugin(object):
	def __init__(self, name = None):
		super(ExporterPlugin, self).__init__()
		self.__module = None
		self.__module_name = None
		if name is not None:
			self.__module = ExporterPlugin.loadPluginModuleNamed(name)
			self.__module_name = name

	@staticmethod
	def allExporterPlugins():
		try:
			if Platform.isMac:
				return [ ExporterPlugin("mac_pkg"), ]
			elif Platform.isWindows:
				return [ ExporterPlugin("win_msi") ]
			return []
		except Exception:
			return []

	@staticmethod
	def loadPluginModuleNamed(name):
		pkg_name = "plugins.exporters." + name
		return __import__(pkg_name, fromlist=["*"])

	@staticmethod
	def isValidPluginModule(name):
		return ExporterPlugin.loadPluginModuleNamed(name) is not None

	@property
	def name(self):
		return self.__module.name()

	@property
	def icon(self):
		return self.__module.icon()

	@property
	def description(self):
		return self.__module.description()

	@property
	def module(self):
		return self.__module_name

	def createExportUI(self, parent):
		return self.__module.createExportUI(parent)



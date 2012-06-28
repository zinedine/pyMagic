from PyQt4.QtCore import QSettings
from lib.platform import Platform

default_dir_excludes = {
	'win32':
		[
			r'.*RECYCLER.*',
			r'.*Recycled.*',
			r'.*security.*',
			r'.*System Volume Information.*',
			r'.*Temporary Internet Files.*',
			r'.*History.IE5.*',
			r'.*Prefetch.*',
			r'.*FileWaveInstallerLogFiles.*',
			r'.*Fileset WinMagic Assistant.*',
			r'.*Temp.*',
			r'.*i386.*',
			r'.*Crypto.*',
			r'.*Protect.*',
			r'.*Cabs.*',
			r'.*wbem.*',
			r'.*FWServer.*',
			r'.*SystemIndex.*',
            r'.*\$Recycle.Bin.*',
		],

	'darwin':
		[
			r'.*System Folder.*',
			r'.*.vol.*',
			r'/.Trashes.*',
			r'.*Network.*',
			r'.*TheFindByContentFolder.*',
			r'.*TheVolumeSettingsFolder.*',
			r'.*Cleanup At Startup.*',
			r'.*File Transfer Folder.*',
			r'.*Trash.*',
			r'/Volumes.*',
			r'.*automount.*',
			r'/cores.*',
			r'/tmp.*',
			r'.*FileWave',
			r'/var/log.*',
			r'/var/run.*',
			r'.*vm',
			r'/dev.*',
			r'/fwxserver.*',
			r'/.Trash.*',
			r'.*FileWave WinAdmin Snapshots.*',
			r'.*netinfo.*',
			r'/.fseventsd.*',
			r'/.Spotlight-V100.*',
			r'.*FileWaveAdmin.*',
			r'.*postfix.*',
			r'.*ARHelperJobs.*',
			r'/usr/local/filewave.*',
			r'/.MobileBackups.*',
		]
}

default_registry_excludes = {
	'win32':
		[
			r'.*SAM.*',
			r'.*SECURITY.*',
			r'.*HARDWARE.*',
			r'.*PendingFileRenameOperations.*',
			r'.*Cryptography.*',
			r'.*History.IE5.*',
			r'.*ControlSet001.*',
			r'.*ControlSet002.*',
			r'.*ControlSet003.*',
		]
}

default_file_excludes = {
	'win32':
		[
			r'.*pagefile.sys.*',
			r'.*NTUSER.DAT.*',
			r'.*ntuser.dat.log.*',
			r'.*software.*',
			r'.*software.log.*',
			r'.*theCatalog.*',
			r'.*newUserManifest.*',
			r'.*newDynamicUserManifest.*',
			r'.*FSWinMagic.ini.*',
            r'.*\$Recycle.Bin.*'
		],

	'darwin':
		[
			r'.*.DS_Store.*',
			r'.*AppleSharePDS.*',
			r'.*CheckForOSX.*',
			r'.*Desktop DB.*',
			r'.*Desktop DF.*',
			r'.*mach.*',
			r'.*mach.sym.*',
			r'.*.hotfiles.btree.*',
			r'.*.hidden.*',
			r'.*.vol.*',
			r'/dev.*',
			r'.*com.filewave.FileWaveAdmin.plist.*',
			r'.*.GlobalPreferences.plist.*',
			r'.*com.apple.finder.plist.*',
			r'.*net.*',
		]
}

class ExclusionRules(object):
	def __init__(self, settings = QSettings()):
		super(ExclusionRules, self).__init__()
		self.settings = settings

	@staticmethod
	def defaultFileExclusionRules():
		if Platform.isWindows:
			return default_file_excludes['win32']
		return default_file_excludes['darwin']

	@staticmethod
	def defaultDirExclusionRules():
		if Platform.isWindows:
			return default_dir_excludes['win32']
		return default_dir_excludes['darwin']

	@staticmethod
	def defaultRegistryExclusionRules():
		if Platform.isWindows:
			return default_registry_excludes['win32']
		return []

	def fileExcludes(self):
		return self.settings.value("file_exclusion_rules", ExclusionRules.defaultFileExclusionRules()).toStringList()

	def dirExcludes(self):
		return self.settings.value("dir_exclusion_rules", ExclusionRules.defaultDirExclusionRules()).toStringList()

	def registryExcludes(self):
		return self.settings.value("registry_exclusion_rules", ExclusionRules.defaultRegistryExclusionRules()).toStringList()

	def setFileExcludes(self, value):
		self.settings.setValue("file_exclusion_rules", value)

	def setDirExcludes(self, value):
		self.settings.setValue("dir_exclusion_rules", value)

	def setRegistryExcludes(self, value):
		self.settings.setValue("registry_exclusion_rules", value)

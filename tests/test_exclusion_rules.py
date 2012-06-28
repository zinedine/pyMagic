
import sys
from PyQt4.QtCore import QSettings
from lib.directory_scanner import DirectoryScanner
from lib.exclusion_rules import ExclusionRules

import unittest
from lib.platform import Platform

class TestExclusionRules(unittest.TestCase):
	def setUp(self):
		self.r = ExclusionRules(settings = QSettings())

	def test_can_store_changes_to_file_exclusions(self):
		new_rule = ".* last rule.*"

		# adds a new rule
		rules = self.r.fileExcludes()
		rules.append(new_rule)
		self.r.setFileExcludes(rules)

		self.assertEqual("FileWave", self.r.settings.organizationName())
		self.assertEqual("UnitTest", self.r.settings.applicationName())

		# fetch and test (the self.r rules are stored/read in default QSettings, unit test main sets this up)
		p = DirectoryScanner()
		self.assertTrue(new_rule in p.file_excludes)
		self.assertTrue(new_rule not in p.dir_excludes)

	def test_can_store_changes_to_dir_exclusions(self):
		new_rule = ".* dir rule.*"

		# adds a new rule
		rules = self.r.dirExcludes()
		rules.append(new_rule)
		self.r.setDirExcludes(rules)

		self.assertEqual("FileWave", self.r.settings.organizationName())
		self.assertEqual("UnitTest", self.r.settings.applicationName())

		# fetch and test (the self.r rules are stored/read in default QSettings, unit test main sets this up)
		p = DirectoryScanner()
		self.assertTrue(new_rule not in p.file_excludes)
		self.assertTrue(new_rule in p.dir_excludes)

	def test_exclusion_defaults(self):
		def_excludes = self.r.defaultFileExclusionRules()
		self.assertTrue(len(def_excludes) > 0)
		def_excludes = self.r.defaultDirExclusionRules()
		self.assertTrue(len(def_excludes) > 0)
		def_excludes = self.r.defaultRegistryExclusionRules()
		if Platform.isWindows:
			self.assertTrue(len(def_excludes) > 0)
		else:
			self.assertEqual(len(def_excludes), 0)


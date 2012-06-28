import sip
sip.setapi('QString', 2)

import unittest
from plugins.exporters.plugin import ExporterPlugin

class PlugTestCase(unittest.TestCase):
	"""
	Proves that the plugins system can load/introspect correctly
	"""
	def test_mac_pkg_plugin_can_be_found(self):
		plugin = ExporterPlugin("mac_pkg")
		self.assertIsNotNone(plugin)
		self.assertEqual(plugin.name, "Mac Installer PKG")
		self.assertEqual(plugin.module, "mac_pkg")

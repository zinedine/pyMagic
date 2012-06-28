import os
from PyQt4.Qt import Qt
import unittest
from lib.build_tree_model import FileSystemTreeModelBuilder
from lib.directory_scanner import DirectoryScanner
from lib.file_system_helper import FileSystemHelper
from lib.persistent_scanning_state import PersistentScanningState
from lib.platform import Platform
from tests.utils import DirectoryTreeBuilder

unittest.skipUnless(Platform.isMac, "tests skipped because they are for the mac")
class MacTestBuildTreeModel(unittest.TestCase):
	"""
	Tests how a tree model is built in different path/scan situations, and with different input data - esp. between
	the mac and windows implementations.
	"""
	def setUp(self):
		self.t = DirectoryScanner()
		self.builder = DirectoryTreeBuilder()

		# construct a known directory structure, suitable for testing - it includes files, directories, ACL's, etc

		self.contents_path = self.builder.make_dir("BB/TextEdit.app/Contents", 0755)
		self.builder.make_dir("BB/TextEdit.app/Contents/Resources", 0755)
		self.builder.make_dir("BB/TextEdit.app/Contents/Frameworks", 0755)
		self.builder.create_file("BB/TextEdit.app/Contents/Stupid.txt", 0755, 425)

		# produce a single scan of the fake file-system entries
		self.p = PersistentScanningState("tree-tests.sqlite")

		self.t.addPathsForScanning([self.builder.rootDir])
		self.initialScan()
		self.mergeScan()

	def initialScan(self):
		for value in self.p.storeFilesystemSnapshot(self.t.performScan()):
			pass
		self.assertTrue(self.p.numberOfScannedFiles() > 0)

	def mergeScan(self):
		for value in self.p.storeSecondScan(self.t.performScan()):
			pass
		self.assertTrue(self.p.numberOfMergedFiles() > 0)

	def test_simple_tree_model(self):
		# grab a fake scan of something we know the content of, e.g. one directory containing one file
		builder = FileSystemTreeModelBuilder(self.p)
		builder.buildModel()

		topLevel = builder.itemRootedAtPath(self.builder.rootDir)

		itemBB = builder.childOfItem(topLevel, "BB")
		self.assertTrue(itemBB is not None)
		self.assertEqual(itemBB.data().toString(), "BB")
		self.assertEqual(itemBB.rowCount(), 1)

		# fetch something that doesn't exist - should bring me back None
		self.assertEqual(None, builder.childOfItem(itemBB, "Not Here"))
		self.assertEqual(None, builder.itemRootedAtPath(os.path.join(self.builder.rootDir, "WOOT")))

		itemTextEdit = builder.childOfItem(itemBB, "TextEdit.app")
		self.assertTrue(itemTextEdit is not None)
		self.assertEqual(itemTextEdit.data().toString(), "TextEdit.app")
		self.assertEqual(itemTextEdit.rowCount(), 1)

		itemContents = builder.childOfItem(itemTextEdit, "Contents")
		self.assertTrue(itemContents is not None)
		self.assertEqual(itemContents.data().toString(), "Contents")
		self.assertEqual(itemContents.rowCount(), 2)

		# go grab both - they should be the frameworks and resources
		items = builder.childrenOfItem(itemContents, ["Resources", "Frameworks"])
		self.assertEqual(items["Resources"].data().toString(), "Resources")
		self.assertEqual(items["Frameworks"].data().toString(), "Frameworks")

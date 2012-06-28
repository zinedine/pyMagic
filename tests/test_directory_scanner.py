import re
from unittest.case import skipUnless, skip, TestCase, skipIf
from PyQt4.QtCore import Qt
from lib.directory_scanner import DirectoryScanner
from lib.file_system_helper import FileSystemHelper
from lib.persistent_scanning_state import PersistentScanningState, FileSystemMerge, FileSystemSnapshot
from lib.platform import Platform
from tests import utils

import os
import shutil
import unittest
import sys

from tests.utils import count_of, DirectoryTreeBuilder
import logging
logger = logging.getLogger(__name__)

@skipUnless(Platform.isMac, "this test is for Mac only")
class MacDirToolsTestCase(TestCase):
    def test_path_sep(self):
        self.assertEqual('/', os.path.sep)

    def test_drive_spec_and_path_splitting(self):
        """
        Checks that splitting out the drive paths works as expected
        """
        test_data = [
            ('/', [ '/' ], ),
            ('/Applications', [ '/', 'Applications'], ),
            ('/Users/john/something', [ '/', 'Users', 'john', 'something'] )
        ]

        for path, expected in test_data:
            parts = FileSystemHelper.splitPath(path)
            drive = parts[0]
            self.assertTrue(FileSystemHelper.isDriveSpec(drive), "this isn't a drive spec: {}".format(drive))
            self.assertEqual(len(parts), len(expected))
            self.assertEqual(parts, expected)

    def test_is_drive_spec_unicode(self):
        """Makes sure that both unicode and ASCII drive specs can be detected by the FileSystemHelper"""
        nonUnicodeDriveSpec = "/"
        unicodeDriveSpec = u"/"
        self.assertTrue(FileSystemHelper.isDriveSpec(nonUnicodeDriveSpec))
        self.assertTrue(FileSystemHelper.isDriveSpec(unicodeDriveSpec))


@skipUnless(Platform.isWindows, "this test is for Windows only")
class WinDirToolsTestCase(TestCase):
    def test_path_sep(self):
        self.assertEqual('\\', os.path.sep)

class ScanningTestCase(TestCase):
    def setUp(self):
        self.t = DirectoryScanner()

    def test_scanner_can_cope_with_scanning_a_bad_path(self):
        results = self.t.performScan(utils.bad_app_path())
        self.assertEqual(0, count_of(results))

    def test_scanner_with_crap_dir_expressions(self):
        self.t.dir_excludes += "this won't \\(compile - no way"
        self.assertRaises(re.error, lambda: self.t.performScan(utils.good_app_path()))

    def test_scanner_with_crap_file_expressions(self):
        self.t.file_excludes += "this won't \\(compile - no way"
        self.assertRaises(re.error, lambda: self.t.performScan(utils.good_app_path()))

    def test_scan_can_run_on_an_existing_path_and_find_some_files(self):
        count = count_of(self.t.performScan(utils.good_app_path()))
        logger.info("text edit.app contains {0} items".format(count))
        self.assertNotEqual(count, 0, "should not be None, text edit exists right?")

    def test_scan_with_exclusion_of_everything(self):
        self.t.dir_excludes.append(r'.*')
        self.t.file_excludes.append(r'.*')
        count = count_of(self.t.performScan(utils.good_app_path()))
        self.assertEqual(count, 0)

    @unittest.skipIf(Platform.isWindows, "testing exclusion of .DS_Store items makes no sense on Win32")
    def test_exclusion_of_dsstore_items(self):
        results = self.t.performScan(utils.good_app_path())
        logger.info("scanning for .DS_Store... hope we dont find it")
        self.assertFalse('.DS_Store' in [file.basename for file in results])

    def test_scan_with_exclusion_of_a_file(self):
        # scan the directory and store the number of files found there
        count_of_all = count_of(DirectoryScanner().performScan(utils.good_app_path()))
        self.assertTrue(count_of_all > 0)
        if Platform.isMac:
            self.t.file_excludes.append(r'.*/TextEdit.app/Contents/Info.plist$')
        else:
            self.t.file_excludes.append(r'.*python.exe$')
        count = count_of(self.t.performScan(utils.good_app_path()))
        self.assertEqual(count, count_of_all - 1)

class FindDifferencesTestCase(TestCase):
    def setUp(self):
        self.t = DirectoryScanner()
        self.builder = DirectoryTreeBuilder()

        # construct a known directory structure, suitable for testing - it includes files, directories, ACL's, etc

        self.contents_path = self.builder.make_dir("AA/TextEdit.app/Contents", 0755)
        self.builder.make_dir("AA/TextEdit.app/Contents/Resources", 0755)
        self.builder.make_dir("AA/TextEdit.app/Contents/Frameworks", 0755)

        self.dbName = "find-diffs.sqlite"
        self.removeDB()

        # produce a single scan of the fake file-system entries
        self.p = PersistentScanningState(self.dbName)

        self.t.addPathsForScanning([self.builder.rootDir])
        self.initialScan()

    def tearDown(self):
        self.p = None
        self.t = None
        self.builder = None

        self.removeDB()

    def removeDB(self):
        try:
            if os.path.exists(self.dbName):
                os.unlink(self.dbName)
        except Exception:
            logger.critical("all bets are off - could not delete {0}".format(self.dbName))

    def initialScan(self):
        for value in self.p.storeFilesystemSnapshot(self.t):
            pass
        self.assertTrue(self.p.scanInfo().files_scanned > 0)
        self.assertEqual(0, self.p.scanInfo().files_merged)

    def mergeScan(self):
        for value in self.p.storeSecondScan(self.t):
            pass
        self.assertTrue(self.p.scanInfo().files_merged > 0)

    def test_parent_child_relationships_in_file_system(self):
        # fetch the root FileSystemSnapshot object, grab its children
        path = FileSystemHelper.convertedPath('%AA/TextEdit.app/Contents')
        root = self.p.session.query(FileSystemSnapshot).filter(FileSystemSnapshot.abs_path.like(path)).one()
        self.assertTrue(root is not None)
        children = root.children
        for child in children:
            logger.info("{0}".format(child))

    def test_find_new_directory(self):
        self.builder.make_dir("AA/NewDirectory", 0777)
        self.mergeScan()
        ms = self.p.session.query(FileSystemMerge).filter(FileSystemMerge.abs_path.like('%NewDirectory')).one()
        logger.info("row, after add: {0}".format(ms.abs_path))
        self.assertEqual(Qt.Checked, ms.checked)
        self.assertEqual(PersistentScanningState.ITEM_ADDED, ms.flags)

        # now find AA, it should be partial because NewDirectory is well, new, and other stuff is marked as Qt.Unchecked
        fs_parent = self.p.session.query(FileSystemSnapshot).get(ms.parent.abs_path)
        self.assertTrue(fs_parent is not None)
        has_parent_changed = fs_parent.path_info != ms.parent.path_info
        if has_parent_changed:
            self.assertEqual(Qt.PartiallyChecked, ms.parent.checked)
            self.assertEqual(PersistentScanningState.ITEM_MODIFIED, ms.parent.flags)
        else:
            self.assertEqual(PersistentScanningState.ITEM_UNCHANGED, ms.parent.flags)

    def test_find_deleted_directory(self):
        self.builder.del_dir("AA/TextEdit.app/Contents/Frameworks")
        self.mergeScan()
        ms = self.p.session.query(FileSystemMerge).filter(FileSystemMerge.abs_path.like('%Frameworks')).one()
        self.assertTrue(ms.abs_path.endswith(FileSystemHelper.convertedPath("AA/TextEdit.app/Contents/Frameworks")))
        self.assertEqual(PersistentScanningState.ITEM_DELETED, ms.flags)
        self.assertEqual(Qt.Unchecked, ms.checked)

    @skipIf(Platform.isWindows, "POSIX tests cannot run on Windows")
    def test_modified_directory_owner(self):
        self.builder.change_posix("AA/TextEdit.app/Contents", 0500)
        self.mergeScan()

        query = self.p.session.query("ct", "flags", "checked").from_statement("SELECT count(*) as ct, flags, checked FROM file_system_merge WHERE abs_path LIKE '%Contents'").one()
        count = query.ct
        flags = query.flags
        checked = query.checked

        # even though the two folders UNDER this one are unchanged, the fact that this folder is modified takes precedence
        self.assertEqual(count, 1)
        self.assertEqual(flags, PersistentScanningState.ITEM_MODIFIED)
        self.assertEqual(checked, Qt.Checked)

    def test_root_scan_paths_are_in_persistent_document(self):
        paths = self.p.pathsBeingScanned()
        self.assertEqual(paths[0].abs_path, self.builder.rootDir)
        # run a merge scan to produce content in the FileSystemMerge table
        self.mergeScan()
        # and that this path is explicitly available from the FileSystemMerge model...
        root_path = self.p.session.query(FileSystemMerge).filter(FileSystemMerge.abs_path==self.builder.rootDir).one()
        self.assertTrue(root_path is not None)
        self.assertEqual(root_path.abs_path, self.builder.rootDir)

    def test_find_modified_directories_and_files(self):
        pass


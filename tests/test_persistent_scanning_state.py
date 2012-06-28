import os
import sip
from tests.utils import good_app_path

sip.setapi('QString', 2)

import unittest
from lib.directory_scanner import DirectoryScanner
from lib.document_storage import DocumentStorage
from lib.persistent_scanning_state import PersistentScanningState, FileSystemSnapshot
import logging
logger = logging.getLogger(__name__)

class PersistTestCase(unittest.TestCase):
    """
    Proves that the scan results can be persisted to a storage form, and re-constituted with the same data.
    """
    def setUp(self):
        self.p = PersistentScanningState("test.sqlite", echo_sql=False)

    def tearDown(self):
        del self.p
        os.remove("test.sqlite")

    def test_scan_is_stored(self):
        t = DirectoryScanner()
        t.addPathsForScanning([good_app_path()])
        # since its an iterable, force its execution
        for x in self.p.storeFilesystemSnapshot(t):
            pass

        # and the dir count contains something
        values = self.p.session.query(FileSystemSnapshot).all()
        self.assertTrue(len(values) > 0)

        self.assertTrue(DocumentStorage.deleteDocumentNamed('test.sqlite'))

    def test_scan_paths_being_scanned(self):
        self.p.storePathsBeingScanned(['one_path', 'two_path'])
        # open up the DB and check...
        paths = [ p.abs_path for p in self.p.pathsBeingScanned() ]
        logger.info("paths are: {0}".format(paths))
        self.assertTrue( "one_path" in paths )
        self.assertTrue( "two_path" in paths )

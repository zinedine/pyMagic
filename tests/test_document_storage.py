import sip
sip.setapi('QString', 2)

from unittest.case import skipUnless
from lib.platform import Platform
import os
import unittest
from lib.file_system_helper import FileSystemHelper
from lib.document_storage import DocumentStorage
import logging
logger = logging.getLogger(__name__)

class ModelTestCase(unittest.TestCase):
    def test_model_directory_can_be_created(self):
        # ensure a fake file is listed inside the data model directory
        f = open(DocumentStorage.documentFullPath('test.sqlite'), "w")
        f.write("something")
        f.close()
        all_docs = DocumentStorage.documents()
        for a_doc in all_docs:
            if 'test.sqlite' in a_doc:
                return
        raise SystemError("Failure - expected test.sqlite to be in these docs somewhere")

    @skipUnless(Platform.isWindows, "This is a C:\\ specific test")
    def test_cdrive_path_creates_sane_document_name(self):
        path = "c:\\"
        name = DocumentStorage.getNewDocumentName([path])
        self.assertTrue("c__" in name)
        
    def test_creating_name_by_using_scanpaths(self):
        name = DocumentStorage.getDocumentPathForName(None, ['/Something'])
        base, filename = os.path.split(name)
        self.assertTrue(filename.startswith("Something -"))
        self.assertTrue(filename.endswith(".sqlite"))

    def test_document_gives_new_filenames(self):
        new_name = DocumentStorage.getNewDocumentName(None)
        self.assertTrue('New Scan' in new_name)

    def test_document_gives_specific_filename(self):
        new_name = DocumentStorage.getDocumentPathForName("something", None)
        self.assertNotEqual(None, new_name)
        self.assertTrue(new_name.endswith("something.sqlite"))

    def test_list_external_disks_mac(self):
        exts = FileSystemHelper.attachedExternalDriveNames()
        logger.info("External disks are: {0}".format(exts))

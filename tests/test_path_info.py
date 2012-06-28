import sip
sip.setapi('QString', 2)

from unittest.case import skipUnless, skipIf
from lib.platform import Platform

import os
import random
import shutil
import unittest
from lib.path_info import PathInfo

class FileInfoTestCase(unittest.TestCase):
	def setUp(self):
		self.tmpDir = os.tmpnam()
		os.mkdir(self.tmpDir)
		# create a single file with zero content, owned by me
		self.tempFile1 = os.tempnam(self.tmpDir, "file1")
		self.tempFile2 = os.tempnam(self.tmpDir, "file2")

		if not Platform.isWindows:
			# create a symlink from file3 to file2
			self.tempFile3 = os.path.join(self.tmpDir, "file3")
			os.symlink(self.tempFile2, self.tempFile3)
		# ensure its exactly 2048 bytes
		with open(self.tempFile1, "wb") as f:
			for x in xrange(2048):
				f.write(str(random.randint(0, 1)))
		os.chmod(self.tempFile1, 0755)
		if not Platform.isWindows:
			os.chown(self.tempFile1, os.geteuid(), os.getegid())

	def tearDown(self):
		shutil.rmtree(self.tmpDir)

	@skipIf(Platform.isWindows, "its a symlink test which isn't supported on Win32 yet")
	def test_file3_exists_and_is_symlink(self):
		info = PathInfo(self.tempFile3)
		self.assertTrue(info.is_symlink)
		info = PathInfo(self.tempFile1)
		self.assertFalse(info.is_symlink)

	def test_properties_cannot_be_set(self):
		info = PathInfo(self.tempFile1)
		info.dirname = "something"

	def test_can_use_two_param_constructor(self):
		info = PathInfo(self.tempFile1)
		as_json = info.to_json()
		info2 = PathInfo(info.abs_path, as_json)
		self.assertEqual(info2.to_json(), as_json)
		self.assertFalse(info2.is_symlink)

	def test_permissions(self):
		info = PathInfo(self.tempFile1)
		self.assertEqual(info.dirname, os.path.dirname(self.tempFile1))
		self.assertEqual(info.basename, os.path.basename(self.tempFile1))
		self.assertEqual(info.size_bytes, 2048)

		if not Platform.isWindows:
			self.assertEqual(info.uid, os.geteuid())
			self.assertEqual(info.gid, os.getegid())
			self.assertEqual(info.posix_perms, 0755)
			self.assertNotEqual(info.posix_perms, 0711)

	@skipUnless(Platform.isWindows, "tests junctions on Win32")
	def test_junction_detection(self):
		# add more here as you see fit...
		paths = [ "C:\\ProgramData\Documents", "C:\\ProgramData\Desktop" ]
		for path in paths:
			is_symlink = PathInfo(path).is_symlink
			self.assertEqual(True, is_symlink)

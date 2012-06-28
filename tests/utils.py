import os
from random import random
import shutil
import sys
from lib.platform import Platform

if not Platform.isWindows:
	import pwd
	import grp

def count_of(iterable):
	count = 0
	for index, value in enumerate(iterable):
		count += 1
	return count

def bad_app_path():
	if Platform.isWindows:
		return "C:\\Program Files\\DoesNotExist.exe"
	else:
		return	"/Applications/TextEditThatDoesNotExist.app"

def good_app_path():
	if Platform.isWindows:
		return 'C:\\Python27'
	return "/Applications/TextEdit.app"


def close_figleaf():
	import figleaf
	print "Figleaf cleaning up"
	figleaf.stop()
	figleaf.write_coverage('.unittest_coverage', append=False)

def start_figleaf(close_at_exit = False):
	try:
		import figleaf

		if sys.gettrace() is None:
			if os.path.exists('.unittest_coverage'):
				os.unlink('.unittest_coverage')
			print "starting figleaf in directory:", os.getcwd()
			figleaf.start()

			if close_at_exit:
				import atexit
				atexit.register(close_figleaf)

			return True
	except Exception:
		pass

	return False


class DirectoryTreeBuilder:
	def __init__(self, temp_name = None):
		if temp_name is None:
			temp_name = os.path.realpath(os.tmpnam())

		self.rootDir = temp_name
		os.mkdir(self.rootDir)

		if not Platform.isWindows:
			self.user = os.environ['USER']
			self.uid = pwd.getpwnam(self.user)[2]
			self.gid = pwd.getpwnam(self.user)[3]
			self.group = grp.getgrgid(self.gid)[0]

	def __del__(self):
		shutil.rmtree(self.rootDir)

	def create_file(self, name, posixMode, byteSize):
		old_dir = os.getcwd()
		try:
			parent, just_the_file_name = os.path.split(name)
			self.make_dir(parent, posixMode)
			filename = os.path.join(self.rootDir, name)
			#print "filename is:", filename
			f = open(filename, mode="w")
			for b in xrange(byteSize):
				c = random() % 26
				f.write(str(c))
			f.close()
		except Exception, e:
			print "failed to create_file:", e
			raise
		finally:
			os.chdir(old_dir)

	def del_dir(self, name):
		old_dir = os.getcwd()
		try:
			os.chdir(self.rootDir)
			#print "deleting:", name
			if os.path.exists(name):
				shutil.rmtree(name)
		finally:
			os.chdir(old_dir)

	def make_dir(self, name, posixMode):
		old_dir = os.getcwd()
		try:
			os.chdir(self.rootDir)
			# name is always in unix format, split it out and rejoin with the OS format.
			if os.path.exists(name):
				return name
			os.makedirs(name, posixMode)
			if not Platform.isWindows:
				os.chown(name, self.uid, self.gid)
			return name
		finally:
			os.chdir(old_dir)

	def change_posix(self, name, perms):
		old_dir = os.getcwd()
		try:
			os.chdir(self.rootDir)
			os.chmod(name, perms)
		finally:
			os.chdir(old_dir)


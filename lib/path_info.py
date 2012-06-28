import json
import os
from posixpath import pathsep
from stat import S_IMODE, S_ISDIR, S_ISLNK
from lib.platform import Platform

import logging
logger = logging.getLogger(__name__)

if Platform.isWindows:
	import jaraco.windows.filesystem

class PathInfo:
	"""
	Encapsulates all the information for an item on disk at a certain point in time.

	The information here is stored in a database.
	While it would be possible to simply return a python object, I want to be able to unify
	the API that looks up permissions, ACL's etc across Mac/Linux and Win32 when the time comes
	and Python isn't going to do that for me.

	This class is used for both the directory and files that are encountered in a difference scan.
	"""
	def __init__(self, path, json_value = None):
		self.__abs_path = os.path.normpath(path)

		# forces caching of the info from disk, which is important because we are
		# building a snapshot - which should not exhibit 'lazy' behaviour
		self.__dict = dict()
		if json_value is None or len(json_value) == 0:
			self.__fetch_info()
		else:
			try:
				self.__dict.update(json.loads(json_value))
			except RuntimeError, e:
				logger.error("booom, for __abs_path: {0}, json value is: {1}".format(path, json_value))

	@staticmethod
	def humanReadableBytes(bytes):
		bytes = float(bytes)
		if bytes >= 1099511627776:
			terabytes = bytes / 1099511627776
			size = '%.2f T' % terabytes
		elif bytes >= 1073741824:
			gigabytes = bytes / 1073741824
			size = '%.2f G' % gigabytes
		elif bytes >= 1048576:
			megabytes = bytes / 1048576
			size = '%.2f M' % megabytes
		elif bytes >= 1024:
			kilobytes = bytes / 1024
			size = '%.2f K' % kilobytes
		else:
			size = '%.f b' % bytes
		return size

	def to_json(self):
		return json.dumps(self.__dict)

	@property
	def is_dir(self):
		return self.__dict['dir']

	@property
	def is_symlink(self):
		return self.__dict['sym_link']

	@property
	def exists(self):
		return self.__dict['exists']

	@property
	def abs_path(self):
		return self.__abs_path

	@property
	def parentpath(self):
		return os.path.split(self.__abs_path)[0]

	@property
	def basename(self):
		return os.path.basename(self.__abs_path)

	@property
	def dirname(self):
		return os.path.dirname(self.__abs_path).rstrip(pathsep)

	@property
	def size_human_readable(self):
		return PathInfo.humanReadableBytes(self.size_bytes)

	@property
	def size_bytes(self):
		return self.__dict['size']

	@property
	def gid(self):
		return self.__dict['gid']

	@property
	def uid(self):
		return self.__dict['uid']

	@property
	def modified_date(self):
		return self.__dict['mod_date']

	@property
	def posix_perms_human_readable(self):
		permsArray = [ "---", "--x", "-w-", "-wx", "r--", "r-x", "rw-", "rwx" ]
		result = "d" if self.is_dir else "-"
		perms = self.posix_perms
		for i in reversed(range(0, 3)):
			index = perms >> (i * 3) & 0x7
			result += permsArray[index]
		return result

	@property
	def posix_perms(self):
		return self.__dict['posix_perms']

	def __fetch_info(self):
		# lstat() does not follow sym links.
		try:
			info = os.lstat(self.__abs_path)
			is_symlink = True if S_ISLNK(info.st_mode) != 0 else False
			if Platform.isWindows:
				is_symlink = jaraco.windows.filesystem.is_reparse_point(self.__abs_path)
			dst_info = info
			if is_symlink:
				dst_info = os.stat(self.__abs_path)

			if info is not None:
				self.__dict.update({
					'exists': os.path.exists(self.__abs_path),
					'size': info.st_size,
					'r_size': 0,
					'gid': info.st_gid,
					'uid': info.st_uid,
					'posix_perms': S_IMODE(info.st_mode),
					'dir': S_ISDIR(dst_info.st_mode),
					'create_date': info.st_ctime,
					'mod_date': info.st_mtime,
					'sym_link': is_symlink
				})

				# if its a directory - collecting the size makes no sense, and in fact confuses the markup of checked/partially
				# modified scans - because changes to the posix perms can modify it?  at least unit tests show that - anyway, we've
				# got no present use for directories with a size attribute.
				if self.is_dir:
					self.__dict.update({'size': 0})
				else:
					# if its Mac, it might have the r_size and others
					if Platform.isMac and hasattr(info, 'r_size'):
						self.__dict.update({'r_size': info.r_size})
			else:
				self.setDefaults()

		except OSError, err:
			# lookup on fs failed, fill in a blank directory
			logger.warn("stat() on path '{0}' failed, using empty/blank defaults, error: {1}".format(self.__abs_path, err))
			self.setDefaults()

	def setDefaults(self):
		self.__dict.update({
			'exists': False,
			'size': 0,
			'r_size': 0,
			'gid': 0,
			'uid': 0,
			'posix_perms': 0,
			'dir': False,
			'create_date': 0,
			'mod_date': 0,
			'sym_link': False,
		})

	def __str__(self):
		return self.__abs_path + ", is_dir:" + self.is_dir + ", size:" + self.size_human_readable

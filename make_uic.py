
import sys, os, re
from lib.platform import Platform

def purge(dir, pattern):
	for f in os.listdir(dir):
		if re.search(pattern, f):
			the_file = os.path.join(dir, f)
			print "purged:", the_file
			os.remove(the_file)

def run_uic(path):
	print "running on path:", path
	purge(path, ".*.pyc")
	olddir = os.getcwd()
	os.chdir(path)
	for root, dirs, files in os.walk("."):
		for file in [file if file.endswith("ui") else None for file in files]:
			if file is not None:
				basename, ext = os.path.splitext(file)
				full_name = os.path.join(root, basename)
				print "pyuic4: {0}.py".format(full_name)
				os.system("pyuic4 {0}.ui > {0}.py".format(full_name))
		for file in [file if file.endswith("qrc") else None for file in files]:
			if file is not None:
				basename, ext = os.path.splitext(file)
				full_name = os.path.join(root, basename)
				print "pyrcc4: {0}_rc.py".format(full_name)
				os.system("pyrcc4 {0}.qrc > {0}_rc.py".format(full_name))
	os.chdir(olddir)

if __name__ == "__main__":
	run_uic("ui")
	run_uic("widgets")
	run_uic("spike")
	if Platform.isWindows:
		pass
	elif Platform.isMac:
		run_uic("plugins/exporters/mac_pkg")

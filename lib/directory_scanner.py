
import itertools
from lib.exclusion_rules import ExclusionRules
import os, sys
import re
from lib.file_system_helper import FileSystemHelper

from lib.path_info import PathInfo

import logging
logger = logging.getLogger(__name__)

class RuleCompilationError(re.error):
    errors = []

class DirectoryScanner(object):
    """
     The DirectoryScanner is responsible for scanning a series of paths on a disk and producing a bunch of
     PathInfo objects for each item found.

     Certain directories and files can be excluded from the scan by setting regular expressions that will exclude
     certain file or directory names from the scanner.  The defaults for these are defined in the default_dir_excludes,
     default_file_excludes and default_registry_excludes globals.

    """
    def __init__(self, exclusion_rules = None):
        if exclusion_rules is None:
            exclusion_rules = ExclusionRules()
        self.rules = exclusion_rules

        # this is the public set of posix style file patterns, e.g. *.txt
        self.dir_excludes = []
        self.file_excludes = []
        self.loadExclusionPreferences()

        # when a scan takes place, the dir_excludes are compiled into regex instances within _excludes
        self.__dir_excludes = []
        self.__file_excludes = []
        self.paths_to_scan = []

    def performScan(self, singlePathToScan = None):
        """
        Provides a generator that throws out FileInfo objs for files under the given directory that
        conform to the include/exclude rules of the directory scanner.
        """

        self.__prepareExpressions()
        if singlePathToScan is not None:
            self.addPathsForScanning([singlePathToScan])

        the_chain = []
        for path in self.paths_to_scan:
            logger.debug("checking path: {0}".format(path))
            if os.path.exists(path):
                the_chain.append(self.__scan(path))

        return itertools.chain(*the_chain)

    @staticmethod
    def compileExpression(exp):
        return re.compile(exp)

    def __prepareExpressions(self):
        """Compiles the expressions provided in exclusions into regular expression objects (faster)
        """
        self.__dir_excludes = []
        self.__file_excludes = []

        errors = []
        for r in self.dir_excludes:
            try:
                if r is None:
                    continue
                self.__dir_excludes.append(DirectoryScanner.compileExpression(r))
            except Exception, e:
                logger.warn("failure; dir expression '{0}' didn't compile, error: {1}, type of arg is: {2}".format(r, e, type(r)))
                errors += e

        for r in self.file_excludes:
            try:
                if r is None:
                    continue
                self.__file_excludes.append(DirectoryScanner.compileExpression(r))
            except Exception, e:
                logger.warn("failure; file expression '{0}' didn't compile, error: {1}, type of arg is: {2}".format(r, e, type(r)))
                errors += e

        if len(errors) > 0:
            e = RuleCompilationError()
            e.errors = errors
            raise e

    def __scan(self, dir_to_scan):
        """
        Runs the scan on a single path - making use of the pre-compiled _exclusions expressions - not for user-space,
        you should instead call performScan as that will prep the exclusion expressions, and concat the
        multiple paths into a single scan op.  The paths are scanned top-down, meaning deepest directories come last.
        """
        for root, dirs, files in os.walk(dir_to_scan):
            for file in files:
                abs_path = os.path.join(os.path.normpath(root), file)
                if self.fileExcluded(abs_path):
                    continue
                fs = self.getFileInformation(abs_path)
                yield fs

            for dir in dirs:
                abs_path = os.path.join(os.path.normpath(root), dir)
                if self.dirExcluded(abs_path):
                    continue
                fs = self.getFileInformation(abs_path)
                if fs.is_symlink:
                    dirs.remove(dir)
                yield fs

    def getFileInformation(self, abs_filename):
        return PathInfo(abs_filename)

    def __pathExcluded(self, exclusion_set, abs_path):
        # if the file path matches the exclusion list - we'll say that the file should not be included in the list
        for r in exclusion_set:
            match = r.match(abs_path)
            if match is not None:
                return True
        return False

    def fileExcluded(self, abs_path):
        return self.__pathExcluded(self.__file_excludes, abs_path)

    def dirExcluded(self, abs_path):
        return self.__pathExcluded(self.__dir_excludes, abs_path)

    def addPathsForScanning(self, scan_paths):
        new_paths = self.paths_to_scan + scan_paths
        self.paths_to_scan = [ os.path.normpath(p) for p in new_paths ]

    def pathsForScanning(self):
        return self.paths_to_scan

    def loadExclusionPreferences(self):
        self.file_excludes = self.rules.fileExcludes()
        self.dir_excludes = self.rules.dirExcludes()


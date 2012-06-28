import sip
from lib.registry_info import RegistryInfo

sip.setapi('QString', 2)

import itertools
from lib.directory_scanner import RuleCompilationError
from lib.exclusion_rules import ExclusionRules
import re

import logging
from lib.platform import Platform

logger = logging.getLogger(__name__)

if Platform.isWindows:
    import _winreg

HIVES = {
"HKEY_LOCAL_MACHINE" : _winreg.HKEY_LOCAL_MACHINE,
#"HKEY_CURRENT_USER" : _winreg.HKEY_CURRENT_USER,
#"HKEY_CLASSES_ROOT" : _winreg.HKEY_CLASSES_ROOT,
#"HKEY_USERS" : _winreg.HKEY_USERS,
#"HKEY_CURRENT_CONFIG" : _winreg.HKEY_CURRENT_CONFIG
}

class RegKey:
    def __init__ (self, name, key):
        self.name = name
        self.key = key
        self.__subkeys_and_values()

    def __str__ (self):
        return self.name + ", has {0} subkeys {1}, and {2} values: {3}".format(len(self.subkeys), self.subkeys, len(self.values), self.values)

    def __subkeys_and_values(self):
        # collect subkeys for this key
        self.subkeys = []
        i = 0
        while True:
            try:
                self.subkeys.append(_winreg.EnumKey(self.key, i))
                i += 1
            except EnvironmentError:
                break

        # collect values for this key
        self.values = []
        i = 0
        while True:
            try:
                self.values.append(_winreg.EnumValue(self.key, i))
                i += 1
            except EnvironmentError:
                break

def walk (top):
    """walk the registry starting from the key represented by
    top in the form HIVE\\key\\subkey\\..\\subkey and generating
    key, subkey_names, values at each level.

    key is a lightly wrapped registry key, including the name
    and the HKEY object.

    subkey_names are simply names of the subkeys of that key
    values are 3-tuples containing (name, data, data-type).

    See the documentation for _winreg.EnumValue for more details.
    """
    search_for = top
    if "\\" not in top:
        search_for += "\\"
    root, subkey = search_for.split ("\\", 1)
    key = _winreg.OpenKey (HIVES[root], subkey, 0, _winreg.KEY_READ)

    reg_key = RegKey(top, key)
    yield reg_key

    for subkey in reg_key.subkeys:
        try:
            for result in walk (top + "\\" + subkey):
                yield result
        except WindowsError:
            print "for name '{0}', subkey '{1}' could not be iterated".format(reg_key.name, subkey)

class RegistryScanner(object):
    """
    The RegistryScanner is responsible for scanning a registry entries and producing RegistryInfo objects.
    """
    def __init__(self, exclusion_rules = None):
        if exclusion_rules is None:
            exclusion_rules = ExclusionRules()
        self.rules = exclusion_rules

        # this is the public set of posix style exclusion patterns, e.g. *.txt
        self.excludes = []
        self.loadExclusionPreferences()

        # when a scan takes place, the excludes are compiled into regex instances within __excludes
        self.__excludes = []

        # default to scanning all HIVES
        self.__hives = HIVES.keys()

    def hivesToScan(self):
        return self.__hives

    def performScan(self):
        """
        Provides a generator that throws out RegistryInfo instances
        """

        self.__prepareExpressions()
        
        the_chain = []
        for hive in self.hivesToScan():
            the_chain.append(self.__scan(hive))

        return itertools.chain(*the_chain)

    @staticmethod
    def compileExpression(exp):
        return re.compile(exp)

    def __prepareExpressions(self):
        """Compiles the expressions provided in exclusions into regular expression objects (faster)
        """
        self.__excludes = []

        errors = []
        for r in self.excludes:
            try:
                if r is None:
                    continue
                self.__excludes.append(RegistryScanner.compileExpression(r))
            except Exception, e:
                logger.warn("failure; reg expression '{0}' didn't compile, error: {1}, type of arg is: {2}".format(r, e, type(r)))
                errors += e

        if len(errors) > 0:
            e = RuleCompilationError()
            e.errors = errors
            raise e

    def __scan(self, hive_or_path):
        """
        Scans a single HIVE
        """
        
        for reg_key in walk(hive_or_path):
            if self.pathExcluded(reg_key.name):
                continue
            info = RegistryInfo(reg_key.name, reg_key.values)
            yield info

    def __pathExcluded(self, exclusion_set, path):
        # if the path matches the exclusion list - we'll say that the it should not be included in the list
        for r in exclusion_set:
            match = r.match(path)
            if match is not None:
                return True
        return False

    def pathExcluded(self, path):
        return self.__pathExcluded(self.__excludes, path)

    def loadExclusionPreferences(self):
        self.excludes = self.rules.registryExcludes()
        
if __name__ == "__main__" and Platform.isWindows:
    s = RegistryScanner();
    for h in s.performScan():
        print h


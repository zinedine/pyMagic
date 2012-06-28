import msilib, msilib.schema, msilib.sequence, shutil, tempfile, os, os.path
from PyQt4.QtCore import QFile
from lib.registry_scanner import HIVES
from lib.registry_info import RegistryInfo
import itertools
import binascii as bin
import os
import _winreg
hives_string = " ".join(HIVES.keys())
                                    
# refer to registry tables article: 
#http://msdn.microsoft.com/en-us/library/windows/desktop/aa371168%28v=vs.85%29.aspx
#http://msdn.microsoft.com/en-us/library/windows/desktop/ms724884%28v=vs.85%29.aspx
# registry table -> root column values:
msidbRegistryRootClassesRoot = 0        #    HKEY_CLASSES_ROOT
msidbRegistryRootCurrentUser = 1        #    HKEY_CURRENT_USER
msidbRegistryRootLocalMachine = 2       #    HKEY_LOCAL_MACHINE
msidbRegistryRootUsers = 3              #    HKEY_USERS

# registry table -> value column
registry_value_prefix_REG_BINARY =      "#x"    #The value is interpreted and stored as a hexadecimal value (REG_BINARY)
registry_value_prefix_REG_EXPAND_SZ =   "#%"  #The value is interpreted and stored as an expandable string (REG_EXPAND_SZ).
registry_value_prefix_REG_DWORD =       "#"      # The value is interpreted and stored as an integer (REG_DWORD).

"""
REG_NONE = 0  not supported by msi
REG_SZ = 1
REG_EXPAND_SZ = 2
REG_BINARY = 3
REG_DWORD = 4
REG_DWORD_BIG_ENDIAN = 5
REG_DWORD_LITTLE_ENDIAN = 4
REG_LINK = 6    not supported by msi
REG_MULTI_SZ = 7
REG_RESOURCE_LIST = 8     not supported by msi
REG_FULL_RESOURCE_DESCRIPTOR = 9      not supported by msi
REG_RESOURCE_REQUIREMENTS_LIST = 10  not supported by msi
"""
#this type is not defined in _winreg module because it is not supported by WIndows Installer
# A 64-bit number.
REG_QWORD = 11  # skip all values with type == 11

# a list of non supported value types, skip if any
WINDOWS_INSTALLER_DOES_NOT_SUPPORT=[_winreg.REG_NONE, \
                                    _winreg.REG_LINK, \
                                    _winreg.REG_RESOURCE_LIST, \
                                    _winreg.REG_FULL_RESOURCE_DESCRIPTOR, \
                                    _winreg.REG_RESOURCE_REQUIREMENTS_LIST, \
                                    _winreg.REG_DWORD_BIG_ENDIAN, \
                                    REG_QWORD \
                                    ]
# a default value name with value not set
DefaultValueNameNotSet = '*'

class FileObject(object):
    def __init__(self,path):
        self.name = os.path.basename(path)
        self.path = os.path.abspath(path) 
        
class RegistryRecordGenerator():
    def __init__(self, RegistryInfo, component):
        self.keyName = RegistryInfo.key
        self.values = RegistryInfo.values  # values here is already decoded and in a list of tuples format.
        self.key = self.keyName[self.keyName.find("\\") + 1:]
        self.root = self.root()
        self.component = component
        
    def run(self):
        isDefaultValueSet = False
        for v in self.values:
            type = v[2]
            if type in WINDOWS_INSTALLER_DOES_NOT_SUPPORT:
                # it is better to log any skipped registry values, 
                continue
            if v[0] == '':
                # this is the default value, its presense means it has a value set
                # because _winreg.EnumValue will skip all default values that do not have values set
                isDefaultValueSet = True
                name = ''
            else:
                name = v[0] 
            
            if type == _winreg.REG_BINARY:
                value =  registry_value_prefix_REG_BINARY + bin.hexlify(v[1])
            elif type == _winreg.REG_DWORD or type == _winreg.REG_DWORD_LITTLE_ENDIAN:
                value = registry_value_prefix_REG_DWORD + str(v[1])
            elif type == _winreg.REG_EXPAND_SZ:
                value = registry_value_prefix_REG_EXPAND_SZ + str(v[1])
            elif type == _winreg.REG_MULTI_SZ:
                value = "[~]".join(v[1])
                #If the value contains the sequence tilde [~], 
                #then the value is interpreted as a Null-delimited list of strings (REG_MULTI_SZ). 
                #For example, to specify a list containing the three strings a, b and c, use "a[~]b[~]c".
            else:
                value = v[1] 
            
            registry  = "reg" + msilib.gen_uuid()[1:-1]
            record = (registry, self.root, self.key, name, value, self.component) 
            yield record
            
        if not isDefaultValueSet:
            name = DefaultValueNameNotSet
            value = ""
            registry  = "reg" + msilib.gen_uuid()[1:-1]
            record = (registry, self.root, self.key, name, value, self.component)
            yield record
    
    def root(self):
        if "HKEY_CLASSES_ROOT"      in self.keyName: return msidbRegistryRootClassesRoot
        elif "HKEY_CURRENT_USER"    in self.keyName: return msidbRegistryRootCurrentUser
        elif "HKEY_LOCAL_MACHINE"   in self.keyName: return msidbRegistryRootLocalMachine
        elif "HKEY_USERS"           in self.keyName: return msidbRegistryRootUsers
        else:
            return -1
   

class PyMagicMSICreator(object):
    def __init__(self, platform, msiFileName, productName, manufacturer, productVersion, language):
        self.platform = platform
        self.msiFile  = FileObject(msiFileName) 
        self.tempDir = tempfile.mkdtemp()
        self.productCode = msilib.gen_uuid()
        self.upgradeCode = msilib.gen_uuid()
        self.productVersion = productVersion
        self.manufacturer = manufacturer
        self.language = language
        self.productName = productName
        self.RegsitryComponent = "RegistryComponent"
        self.registryRecords = []
        
        self.template =  QFile(":/files/pyMagicTemplateMSI2.msi")
        self.template.open(QFile.ReadOnly) 
        data = self.template.readAll()
        self.templatePath = msiFileName
        x = QFile(self.templatePath)
        if  x.open(QFile.WriteOnly):
            print "opened file for write"
            x.write(data)
        else:
            print "could not open file for writing"
            
        x.close()
        self.template.close()
    

    def generate_msi(self, document, dstroot):
        """
        generate msi from a document, using systescanmerge and registryscanmerge 
        """
        self.database = msilib.OpenDatabase(self.msiFile.path, msilib.MSIDBOPEN_DIRECT)
        self.document = document
        
        propertyRecords = self.collectPropertyRecords() 
        table = "Property"
        msilib.add_data(self.database, table, propertyRecords)
        
        promptText = self.productName + " " + self.productVersion + " [1]"
        diskPrompt = [ ("DiskPrompt", promptText ) ]
        msilib.add_data(self.database, table, diskPrompt) 
        
        self.cabFile = msilib.CAB("files.cab")
        f = msilib.Feature(self.database, "defaultFeature", "Default Feature", "Everything", 0, directory="TARGETDIR")
        f.set_current()
        
        home =  dstroot[:3] # example home = "C:\"
        
        # this is the root directory object, a parent of all subdirs in the installation
        root = msilib.Directory(self.database, self.cabFile, None, home , "TARGETDIR", "SourceDir")
        
        self.__buildMSIHiarchy(dstroot, root)
        
        # create a component in "Component" table responsible for installing the registry keys
        root.start_component(component = self.RegsitryComponent, flags = 0)
        # RegsitryComponent is set to current component by default, we don't need that right now,
        root.component = None
        
        # Create and add registry records:
        self.createRegistryRecords()
        if len(self.registryRecords) != 0:
            # there are registry changes, enable and then add them to the installer
            actionsRecords = self.enableRegistryActions()
            table = "InstallExecuteSequence"
            msilib.add_data(self.database, table, actionsRecords)
            
            # now add self.registryRecords found by calling createRegistryRecords, to the msi. a list of tuples is the format.
            table = "Registry"
            msilib.add_data(self.database, table, self.registryRecords) 
            
        self.database.Commit()
        self.cabFile.commit(self.database)
        

    def __buildMSIHiarchy(self, dirPath, rootDirObj = None):
        """
        build the Installation hiarchy of Folders/files
        this will make changes to the following tables in the mis: Directory, Component, FeatureComponents, File 
        """
        for folder in  os.listdir(dirPath):
            path = os.path.join(dirPath,folder)
            if os.path.isdir(path):
                root = msilib.Directory(self.database, self.cabFile, rootDirObj, folder, folder , folder)
                self.__buildMSIHiarchy(path , root)
            elif os.path.isfile(path):
                rootDirObj.add_file(folder)
    
            
    def collectPropertyRecords(self):
        propertyRecords = [ ("ProductName",self.productName ),
                            ("ProductCode", self.productCode),
                            ("ProductVersion", self.productVersion),
                            ("Manufacturer", self.manufacturer),
                            ("ProductLanguage", self.language),
                            ("UpgradeCode", self.upgradeCode)
                          ]
        return propertyRecords
                 
    def createRegistryRecords(self):
        """
        create a list of tuples representing the win installer registry records
        each key may have more that one record, we create a record for each value in the format:
        (registry, rootKey, key, valueName, value, component)
        for more details: http://msdn.microsoft.com/en-us/library/windows/desktop/aa371168%28v=vs.85%29.aspx
        """
        for reg in self.document.iterateRegistrymergeResults():
            gen = RegistryRecordGenerator(RegistryInfo.from_json(reg.key_name, reg.values), self.RegsitryComponent)
            for idx, x in enumerate(gen.run()):
                self.registryRecords.append(x)
            #print "records list: ", self.registryRecords    
          
    def enableRegistryActions(self):
        #RemoveAddRegistry = [ ("RemoveRegistryValues", None, "2600"), ("WriteRegistryValues", None, "5000") ]
        RemoveAddRegistry = [ ("WriteRegistryValues", None, "5000") ]
        return RemoveAddRegistry     


 

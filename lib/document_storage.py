import os
from datetime import datetime
from string import replace
from PyQt4.Qt import QDesktopServices
from lib.platform import Platform

class DocumentStorage:
    """
    Handles the management of the storage location, finding the set of documents available (which are instances of PersistentScanningState
    """
    base_path = os.path.join(QDesktopServices.storageLocation(QDesktopServices.DocumentsLocation), "Filewave PyMagic")
    base_path = os.path.normpath(base_path)
    if not os.path.exists(base_path):
        os.mkdir(base_path)

    @classmethod
    def documents(self):
        """
        Finds all the .sqlite documents within the given path
        """
        all_files = os.listdir(self.base_path)
        all_sqlites = [ os.path.normpath(os.path.join(self.base_path, file)) for file in all_files if file.endswith('.sqlite')]
        return all_sqlites

    @classmethod
    def getDocumentPathForName(cls, doc_name, scan_paths):
        """
        Returns the full path for a given document name.  If the document name is blank then the name is generated
        based on the scan_paths value by calling getNewDocumentName()
        """
        if doc_name is None:
            doc_name = cls.getNewDocumentName(scan_paths)
        return cls.documentFullPath(doc_name)

    @classmethod
    def stripname(self, name):
        name = replace(name, ':', '_')
        name = replace(name, os.path.sep, '_')
        return name

    @classmethod
    def documentFullPath(self, param):
        """
        Returns the name of a document based on the path of the document directory
        """
        path = os.path.normpath(os.path.join(self.base_path, self.stripname(param)))
        if not path.endswith(".sqlite"):
            path += ".sqlite"

        return path

    @classmethod
    def deleteDocumentNamed(self, name):
        doc_name = self.documentFullPath(name)
        if os.path.exists(doc_name):
            os.unlink(doc_name)
        return not os.path.exists(doc_name)

    @classmethod
    def getNewDocumentName(cls, scan_paths):
        now = datetime.now()

        prefix = 'New Scan'
        if scan_paths is not None and len(scan_paths) == 1:
            prefix = os.path.basename(scan_paths[0])
            if Platform.isWindows and len(prefix) == 0:
                prefix = scan_paths[0]

        new_name = prefix + " - " + now.strftime("%Y %b %d - %H_%M_%S")
        return cls.stripname(new_name)

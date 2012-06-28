from PyQt4.QtCore import QRegExp, QDir, QFileInfo, QProcess, QUrl, QSettings, Qt
from PyQt4.QtGui import QIcon, QWidget, QFileDialog, QMessageBox, QApplication, QDesktopServices
from ui_win_msi import Ui_MSICreationPage
from pyMagicMSI import PyMagicMSICreator
from widgets.export_data_widget import ExportDataWidget
import tempfile, shutil
import os.path, os
import logging
logger = logging.getLogger(__name__)


class MSICreationWidget(QWidget):
    def __init__(self,parent):
        super(MSICreationWidget, self).__init__(parent)
        self.ui = Ui_MSICreationPage()
        self.ui.setupUi(self)
        
        self.document = None
        
        self.ui.lineEditProductName.textChanged.connect(self.__fieldsValidate)
        self.ui.lineEditManufacturer.textChanged.connect(self.__fieldsValidate)
        self.ui.lineEditProductVersion.textChanged.connect(self.__fieldsValidate)
        self.ui.pbCreateMSI.released.connect(self.__createMSI)
        
        self.ui.cbLanguage.addItem("-")
        self.ui.cbLanguage.addItem("English")
        self.ui.cbLanguage.addItem("French")
        self.ui.cbLanguage.addItem("German")
        self.ui.cbLanguage.activated[str].connect(self.__fieldsValidate)
        
        self.__enableExportControls(False)
        self.__loadFields()
        self.__fieldsValidate()
        self.__setProgressHidden(False)
        
    
    def __saveFields(self): 
        c = 0
    def isComplete(self):
        if self.document == None:
            return false
        return self.__fieldsValidate()
    
    def __prepareProgress(self, text, max = None):
        self.ui.progressBar.reset()
        self.ui.progressBar.setMaximum(0)
        self.ui.progressBar.setMinimum(0)
        if max is not None:
            self.ui.progressBar.setRange(0,max)
        self.ui.lblProgressInfo.setText(text)
        self.__setProgressHidden(False)
        
    def __setProgress(self, value, source_path):
        self.ui.progressBar.setValue(value)
        self.ui.lblProgressInfo.setText(source_path)
        QApplication.processEvents()

    def __finishProgress(self, text):
        self.__setProgressHidden(True)
        self.ui.lblProgress.setHidden(False)
        self.ui.lblProgress.setText(text)
                
    def initializePageWithDocument(self, document):
        self.document = document
        
    def __loadFields(self):
        return 0
        
    def __fieldsValidate(self):
        enabled =  [ self.ui.cbLanguage.currentText() != "-",
                        len(self.ui.lineEditManufacturer.text()) > 0,
                        len(self.ui.lineEditProductName.text())  > 0,
                        len(self.ui.lineEditProductVersion.text()) > 0 ]
        #remove this once done with testing
        enabled = [ True ]
        self.__enableExportControls(all(enabled)) 
        return all(enabled)
        
    def __enableExportControls(self, enabled):
        self.ui.pbCreateMSI.setEnabled(enabled)

        return True
        
    def __setProgressHidden(self, hide):
        self.ui.progressBar.setHidden(hide)
        self.ui.lblProgress.setHidden(hide)
        self.ui.lblProgressInfo.setHidden(hide)
        
    def languageCode(self, language):
       # for now return english only
       return "1033"  # assume english   

    def __createMSI(self):
        """   create the msi installer    """
        productName = self.ui.lineEditProductName.text()
        manufacturer = self.ui.lineEditManufacturer.text()
        productVersion = self.ui.lineEditProductVersion.text()
        language = self.ui.cbLanguage.currentText()
        
        total_system_items = self.document.countScanningResults()
        #total_registry_items = ? create the function
        self.__prepareProgress("creating msi Cabs", total_system_items)
        
        homeDrive = os.environ["userprofile"]
        dst_path = os.path.join(homeDrive, "DSTROOT")
        if not os.path.exists(dst_path):
            os.makedirs(dst_path) # or maybe makepath is better in this case
        self.dstroot_path = tempfile.mkdtemp(dir=dst_path)
        self.__createDSTRoot()
        platform = "x86"
        msiFileName = productName + productVersion + ".msi"
        # msi created is found at C:/pyMagicMSi/ , change it to get the path from USer : output directory
        msiFile = os.path.join(dst_path, msiFileName)
        msi = PyMagicMSICreator(platform, msiFile, productName, manufacturer, productVersion, self.languageCode(language))
        msi.generate_msi(self.document, os.path.abspath(self.dstroot_path))
        
        
        # for scan_record in self.document.iterateScanningResults():
        
        #msi.msi.generate_msi()   # generate: takes list of files and registries that we get from document
        # we need to construct the folder table:  child - parent structure from paths in document
        
    def __createDSTRoot(self):
        errors = []
        counter = 0 
        for scan_record in self.document.iterateScanningResults():
            counter += 1
            source_path = scan_record.abs_path
            final_dest = os.path.join(self.dstroot_path, source_path[3:])
            
            parent = os.path.split(final_dest)[0]
            if parent is not None and len(parent) > 0 and not os.path.exists(parent):
                os.makedirs(parent)
            self.__setProgress(counter, source_path)
            
            try:
                if os.path.islink(source_path):
                    linkto = os.readlink(source_path)
                    os.symlink(linkto,final_dest)
                elif os.path.isfile(source_path):
                    shutil.copy2(source_path, final_dest)
                elif os.path.isdir(source_path):
                    if not os.path.exists(final_dest):
                        os.makedirs(final_dest)
                    shutil.copystat(source_path, final_dest)
                    
            except ( IOError, os.error), why:
                errors.append((source_path, final_dest, str(why)))
                
        return len(errors) == 0
                
        
        
        
        
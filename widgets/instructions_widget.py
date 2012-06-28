
from PyQt4.Qt import *
from ui.Instructions import Ui_Instructions

class InstructionsWidget(QWizardPage):
    beforeInstalling = pyqtSignal()
    afterInstalling = pyqtSignal()

    def __init__(self, parent = None):
        super(InstructionsWidget, self).__init__(parent)
        self.ui = Ui_Instructions()
        self.ui.setupUi(self)
        
        self.ui.prepareForInstallButton.clicked.connect(self.beforeInstalling)
        self.ui.constructFilesetButton.clicked.connect(self.afterInstalling)

        self.setButtonText(QWizard.NextButton, "Quit")

    


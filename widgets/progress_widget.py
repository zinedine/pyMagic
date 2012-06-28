from ui.progress import Ui_Progress
from PyQt4.QtGui import QWidget

class ProgressWidget(QWidget):
	def __init__(self, widget = None):
		super(ProgressWidget, self).__init__(widget)
		self.ui = Ui_Progress()
		self.ui.setupUi(self)

	def setText(self, txt):
		self.ui.label.setText(txt)

	def setIndeterminate(self):
		self.ui.progressBar.setMinimum(0)
		self.ui.progressBar.setMaximum(0)
		self.ui.progressBar.setValue(0)

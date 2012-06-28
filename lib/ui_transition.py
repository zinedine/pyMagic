
from PyQt4.QtCore import QObject, pyqtSignal, QEasingCurve, QPropertyAnimation, QRect, QParallelAnimationGroup, QAbstractAnimation

class TransitionHandler(AnimatorBase):
	def __init__(self, parent = None):
		super(TransitionHandler, self).__init__(parent)


#	def animateChildWidgetToSizeMovingOutExistingChildWidget(self, stage, oldStage, newSize, animate = True):
#		stage.setGeometry(QRect(newSize.width(), 0, newSize.width(), newSize.height()))
#		stage.show()
#
#		self.grp = QParallelAnimationGroup()
#
#		# moves the old item out of the view
#		if oldStage is not None:
#			r = oldStage.geometry()
#			anim = AnimatorBase.animatePropertyWidgetTo(oldStage, "geometry", r.translated(-r.width(), 0))
#			if anim is not None:
#				self.grp.addAnimation(anim)
#
#		# moves the new item into the view.
#		anim = AnimatorBase.animatePropertyWidgetTo(stage, "geometry", QRect(0, 0, newSize.width(), newSize.height()))
#		if anim is not None:
#			self.grp.addAnimation(anim)
#
#		# does the UI need to resize to accomodate?
#		if newSize != self.toplevel.geometry().size():
#			anim = AnimatorBase.animatePropertyWidgetTo(self.toplevel, "size", newSize + self.toplevel.minimumSizeHint())
#			if anim is not None:
#				self.grp.addAnimation(anim)
#
#		self.startAnim(self.grp, "geometry")

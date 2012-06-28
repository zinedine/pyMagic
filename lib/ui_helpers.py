import cmd
import os
from PyQt4.Qt import *
from lib.platform import Platform
import logging
logger = logging.getLogger(__name__)

def addNewListItemCalled(data, theList, mutable=False):
	theList.addItems(data)

	lastRow = theList.model().rowCount()
	theItem = theList.item(lastRow - 1)
	if mutable:
		theItem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

	return theItem

def showInFinder(path_name):
	if Platform.isMac:
		# there doesn't seem to be a direct API to show the file in Finder, so Applescript to the rescue
		osa_command = """
		tell application "Finder"
			set mac_path to (POSIX file "{0}")
			reveal mac_path
			activate
		end tell
		""".format(path_name.encode("utf-8"))
		cmd = "osascript -e '{}'".format(osa_command)
	elif Platform.isWindows:
		cmd = "explorer.exe /select,{}".format(path_name.encode("utf-8"))

	if len(cmd) > 0:
		logger.info("command is: {0}".format(cmd))
		os.system(cmd)

class ListWidgetDeleting(object):
	def __init__(self):
		pass

	def deleteSelectedListWidgetItems(self, listWidget, title = "Remove Items?", text = "Are you sure that you want to remove the selected items?"):
		"""
		Removes the selected items from the listWidget after confirmation
		"""
		all_items = listWidget.selectedItems()
		res = QMessageBox.question(self, title, text, QMessageBox.Yes | QMessageBox.Cancel)
		if QMessageBox.StandardButton(QMessageBox.Yes) == res:
			# find the model objects, blow them away - we can do this via row number
			items = [listWidget.row(theItem) for theItem in all_items]
			items.sort()

			for rowNumber in reversed(items):
				yield listWidget.takeItem(rowNumber)

	def deleteSelectedTreeViewItems(self, treeView, title = "Remove Items?", text = "Are you sure that you want to remove the selected items?"):
		"""
		Removes the selected items from the view after confirmation
		"""
		all_items = treeView.selectionModel().selectedIndexes()
		res = QMessageBox.question(self, title, text, QMessageBox.Yes | QMessageBox.Cancel)
		if QMessageBox.StandardButton(QMessageBox.Yes) == res:
			# find the model objects, blow them away - we can do this via row number
			items = [item.row() for item in all_items]
			items.sort()

			for rowNumber in reversed(items):
				yield treeView.model().takeRow(rowNumber)

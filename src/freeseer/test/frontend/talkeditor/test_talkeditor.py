
import unittest


from PyQt4 import QtGui, QtTest, Qt


from freeseer.frontend.talkeditor.talkeditor import TalkEditorApp

class TestTalkEditorApp(unittest.TestCase):
	'''
	Test suite to verify the functionality of the TalkEditorApp class.

	Tests interact like an end user (using QtTest). Expect the app to be rendered.

	'''

	def setUp(self):
		'''
		Stardard init method: runs before each test_* method

		Initializes a QtGui.QApplication and TalkEditorApp object.
		TalkEditorApp.show() causes the UI to be rendered.
		'''

		self.app = QtGui.QApplication([])
		self.talk_editor = TalkEditorApp()
		self.talk_editor.show()


	def test_add_talk(self):
		''' 
		Tests a user creating a talk and adding it.
		'''

		QtTest.QTest.mouseClick(self.talk_editor.editorWidget.addButton, Qt.Qt.LeftButton)
		self.assertFalse(self.talk_editor.editorWidget.isVisible())	
		self.assertTrue(self.talk_editor.addTalkWidget.isVisible())

		mTitle = "This is a test"
		mPresenter = "Me, myself, and I"
		mEvent = "0 THIS St."
		mRoom = "Room 13"

		# populate talk data (date and time are prepopulated)
		self.talk_editor.addTalkWidget.titleLineEdit.setText(mTitle)
		self.talk_editor.addTalkWidget.presenterLineEdit.setText(mPresenter)
		self.talk_editor.addTalkWidget.eventLineEdit.setText(mEvent)
		self.talk_editor.addTalkWidget.roomLineEdit.setText(mRoom)

		# add in the talk
		QtTest.QTest.mouseClick(self.talk_editor.addTalkWidget.addButton, Qt.Qt.LeftButton)

		# find our talk (ensure it was added)
		found = False
		row_count = self.talk_editor.editorWidget.editor.model().rowCount() - 1
		while row_count >= 0 and not found: # should be at the end, but you never know
			if self.talk_editor.editorWidget.editor.model().index(row_count, 1).data() == mTitle and \
				self.talk_editor.editorWidget.editor.model().index(row_count, 2).data() == mPresenter and \
				self.talk_editor.editorWidget.editor.model().index(row_count, 5).data() == mEvent and \
				self.talk_editor.editorWidget.editor.model().index(row_count, 6).data() == mRoom:
				found = True
				# TODO: Select this row
			row_count -= 1

		self.assertTrue(found, "Couldn't find talk just inserted...")

		# now delete the talk we just created
		QtTest.QTest.mouseClick(self.talk_editor.editorWidget.removeButton, Qt.Qt.LeftButton);

	def test_add_talk_cancel(self):
		'''
		Tests a user creating a talk, but cancelling it instead of adding it.
		'''

		QtTest.QTest.mouseClick(self.talk_editor.editorWidget.addButton, Qt.Qt.LeftButton)
		self.assertFalse(self.talk_editor.editorWidget.isVisible())	
		self.assertTrue(self.talk_editor.addTalkWidget.isVisible())

		QtTest.QTest.mouseClick(self.talk_editor.addTalkWidget.cancelButton, Qt.Qt.LeftButton)
		self.assertFalse(self.talk_editor.addTalkWidget.isVisible())
		self.assertTrue(self.talk_editor.editorWidget.isVisible())

	def test_close_talkeditor(self):
		'''
		Tests the "close" button. 
		Although we close the app using this button after every test (in tearDown()), 
		we are not guarenteed a valid test case in tearDown().
		'''	

		QtTest.QTest.mouseClick(self.talk_editor.editorWidget.closeButton, Qt.Qt.LeftButton)
		self.assertFalse(self.talk_editor.editorWidget.isVisible())


	def test_clear_all_talks(self):
		'''
		Tests the "clear" button on the main window.
		'''

		if self.talk_editor.editorWidget.editor.model().rowCount() == 0:
			QtTest.QTest.mouseClick(self.talk_editor.editorWidget.addButton, Qt.Qt.LeftButton)
			mTitle = "This is a test"
			mPresenter = "Me, myself, and I"
			mEvent = "0 THIS St."
			mRoom = "Room 13"
			# populate talk data
			self.talk_editor.addTalkWidget.titleLineEdit.setText(mTitle)
			self.talk_editor.addTalkWidget.presenterLineEdit.setText(mPresenter)
			self.talk_editor.addTalkWidget.eventLineEdit.setText(mEvent)
			self.talk_editor.addTalkWidget.roomLineEdit.setText(mRoom)
		# date and time are prepopulated 

		# add in the talk
		QtTest.QTest.mouseClick(self.talk_editor.addTalkWidget.addButton, Qt.Qt.LeftButton)

		# we need at least 1 talk
		self.assertTrue(self.talk_editor.editorWidget.editor.model().rowCount() > 0)

		# TODO: 
		# ROADBLOCK: Clicking "clear" causes a pop-up confirmation box to appear.
		# It isn't clear how to get the test case to pause until the box has focus.

		# hit the clear button, hit no. No changes
		#QtTest.QTest.mouseClick(self.talk_editor.editorWidget.clearButton, Qt.Qt.LeftButton)
		# TODO: get the pop-up box's focus and click the button

		# hit the clear button, hit yes. Empty DB	
		#QtTest.QTest.mouseClick(self.talk_editor.editorWidget.clearButton, Qt.Qt.LeftButton)
		# TODO: get the pop-up box's focus and click the button

	def tearDown(self):
		'''
		Standard tear down method. Runs after each test_* method.

		This method closes the TalkEditorApp by clicking the "close" button
		'''

		QtTest.QTest.mouseClick(self.talk_editor.editorWidget.closeButton, Qt.Qt.LeftButton)

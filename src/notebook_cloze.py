# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo
# import all of the Qt GUI library
from aqt.qt import *
from anki.hooks import addHook

from aqt.qt import *

from PyQt4.QtGui import QWidget, QFileDialog

def testFunction():
    # get the number of cards in the current collection, which is stored in
    # the main window
    cardCount = mw.col.cardCount()
    # show a message box
    showInfo("yo what up")
    # showInfo("testing 123 " % cardCount)

def getFilename():
    w = QWidget()
    w.resize(320, 240)
    w.setWindowTitle("Hello World!")
    
    filename = QFileDialog.getOpenFileName(w, 'Open File', '/') 
    w.show()
    return filename

class NotebookEdit(object):
    def __init__(self, mw):
        showInfo("start gui")
        # QDialog.__init__(self, parent=None)
        filename = getFilename()
        showInfo(filename)

        w = QWidget()
        w.resize(320, 240)
        w.setWindowTitle("Hello World!")
        
        w.show()

class NotebookCloze(object):
    def __init__(self, ed):
        # showInfo("yo what up")
        mw.ncEditor = NotebookEdit(mw)

def onNCButton(ed):
    # showInfo('this should open the editor window')
    mw.notebookCloze = NotebookCloze(ed)

def onSetupEditorButtons(self):
    # showInfo('running notebook cloze')
    self._addButton("new notebook",
            lambda o=self: onNCButton(self),
            _("Alt-c"), _("Make new Notebook Cloze"),            canDisable=False)

addHook('setupEditorButtons', onSetupEditorButtons)


# create a new menu item, "test"
action = QAction("test", mw)

# set it to call testFunction when it's clicked
action.triggered.connect(testFunction)
# and add it to the tools menu
mw.form.menuTools.addAction(action)

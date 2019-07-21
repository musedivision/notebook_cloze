# import the main window object (mw) from aqt
from aqt import mw, deckchooser
# import the "show info" tool from utils.py
from aqt.utils import showInfo
# import all of the Qt GUI library
from aqt.qt import *
from anki.hooks import addHook
from anki.notes import Note
import logging, sys
from aqt.qt import *

from PyQt4.QtGui import QWidget, QFileDialog, QDialog, QListWidgetItem, QStandardItemModel, QStandardItem
from dialog import Dialog 
from process_notebook import readNotebook
import template

def testFunction():
    # get the number of cards in the current collection, which is stored in
    # the main window
    cardCount = mw.col.cardCount()
    # show a message box
    showInfo("yo what up")
    # showInfo("testing 123 " % cardCount)

def launchEditor():
    NotebookEdit()

class NotebookEdit(Dialog):
    def __init__(self):
        super(NotebookEdit, self).__init__()
        
        self.notebookFile.clicked.connect(self.getFilename)
        self.model = template.get_nbc_model(mw.col)

        self.deck_container = QWidget()
        self.deckChooser = deckchooser.DeckChooser(mw, self.deck_container, label=True)
        self.deckChooser.deck.setAutoDefault(False)
        self.did = self.deckChooser.selectedId()


    def getFilename(self):
        # w = QWidget() 
        # filename = QFileDialog.getOpenFileName(w, 'Open File') 
        # w.show()
        # self.filename = filename

        self.filename = '/Users/patricio/code/notebook_cloze/data/multi_cloze.ipynb'
        self.processNotebook()

    def processNotebook(self):
       output = readNotebook(self.filename) 
       answers,nbs = zip(*output)
       
       self.processed = { 'answers': answers, 'nbs':nbs, 'output':output } 

       answers = ['\n'.join(t) for t in answers ] 
       # cloze_txt = '\n'.join(output[0][0]) 
       self.answerList.addItems(answers)
    
    def addNote(self):
        # need deck id
        self.model['did'] = self.did
        # add data for all fields 
        # add tags to note
        note = Note(mw.col, self.model)


        # finally add to collection
        mw.col.addNote(note)
        

    def accept(self):
        instructions = self.instructionText.toPlainText()
        showInfo(str(self.did))
        

class NotebookCloze(object):
    def __init__(self, ed):
        # showInfo("yo what up")
        mw.ncEditor = NotebookEdit()
        mw.ncEditor.show()



def onNCButton(ed):
    # showInfo('this should open the editor window')
    mw.notebookCloze = NotebookCloze(ed)

def onSetupEditorButtons(self):
    # showInfo('running notebook cloze')
    btn = self._addButton("new notebook",
            lambda o=self: onNCButton(self),
            _("Alt-c"), _("Make new Notebook Cloze"),            canDisable=False)

    press_action = QAction(self.parentWindow, triggered=btn.animateClick)
    press_action.setShortcut(QKeySequence(_("Alt-n")))
    btn.addAction(press_action)

addHook('setupEditorButtons', onSetupEditorButtons)

#showInfo("addon properly loaded")

# create a new menu item, "test"
action = QAction("launch notebook cloze", mw)

# set it to call testFunction when it's clicked
action.triggered.connect(launchEditor)
# and add it to the tools menu
mw.form.menuTools.addAction(action)

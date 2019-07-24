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
from template import *
import os
import json
import string
import random
import unicodedata
from stat import S_IREAD, S_IRGRP, S_IROTH

randomString = lambda n: ''.join([random.choice(string.ascii_lowercase) for _ in range(n)])

def nbfile2url(nbpath):
    return 'http://alfred.local:8889/notebooks/anki/' + nbpath


def launchEditor():
    NotebookEdit()

def fieldDict(instr, a, n):
    return {
        NBC_FLDS['is']: instr,
        NBC_FLDS['lk']: n,
        NBC_FLDS['an']: a
        }

def makeFileReadOnly(fpath):
    os.chmod(fpath, S_IREAD|S_IRGRP|S_IROTH)


class NotebookEdit(Dialog):
    def __init__(self):
        super(NotebookEdit, self).__init__()
        
        self.notebookFile.clicked.connect(self.getFilename)
        self.model = get_nbc_model(mw.col)

        self.deck_container = QWidget()
        self.deckChooser = deckchooser.DeckChooser(mw, self.deck_container, label=True)
        self.deckChooser.deck.setAutoDefault(False)
        self.did = self.deckChooser.selectedId()

        # showInfo(str(self.model['flds']))
        self.media_path = mw.col.media.dir()


    def getFilename(self):
        w = QWidget() 
        self.filename = QFileDialog.getOpenFileName(w, 'Open File') 
        w.show()
    
        # self.filename = '/Users/patricio/code/notebook_cloze/data/multi_cloze.ipynb'
        self.processNotebook()

    def createNotebookLink(self, nb):
        # write read only notebook file
        # return link to file

        # will need to store the notebook file in ankis media folder
        # save returned path  
        fname = 'nbc_notebook_%s.ipynb' % randomString(10)

        nb_col_path = os.path.join(self.media_path, fname)
        with open(nb_col_path, 'w') as outfile:
            json.dump(nb, outfile)
            # tmpPath = tmpPath.decode('utf-8')       
            makeFileReadOnly(nb_col_path) 
            # nb_path = mw.col.media.writeData(tmpPath, nb)
            nb_url = nbfile2url(fname)
            return nb_url

    def processNotebook(self):
        output = readNotebook(self.filename)
        self.raw_input_nb = output
        self.displayCurrCloze()
    
    def displayCurrCloze(self):
        answers, _ = zip(*self.raw_input_nb)
        answers = ['\n'.join(t) for t in answers]
        self.answerList.addItems(answers)

    def createNotebooks(self):
        answers, nbs = zip(*self.raw_input_nb)
        answers = ['\n'.join(t) for t in answers]
        nbs = [self.createNotebookLink(nb) for nb in nbs]

        self.processed_nb = {'answers': answers, 'nbs':nbs}

        instr = self.instructionText.toPlainText()
        self.newCards = [fieldDict(instr, a, n) for a, n in zip(answers, nbs)]


    def createCardFields(self):
        # assumes notebook has already been processed
        proc = self.processed_nb
        instr = self.instructionText.toPlainText()
        multi_fields = [fieldDict(instr, a, n) for a, n in zip(proc['answers'], proc['nbs'])]
        self.newCards = multi_fields 

    def addNote(self, fields):
        flds = self.model['flds']
        self.model['did'] = self.did
        # add tags to note
        note = Note(mw.col, self.model)

        # add data for all fields 
        for i in flds:
            fname = i["name"]
            if fname in fields:
                note[fname] = fields[fname]
        # finally add to collection
        mw.col.addNote(note)
        

    def accept(self):
        # create card fields
        self.createNotebooks()
        self.createCardFields()
        numCards = len(self.newCards)
        for flds in self.newCards:
            self.addNote(flds)
        showInfo('Added %s cards' % str(numCards) )
        self.close()

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

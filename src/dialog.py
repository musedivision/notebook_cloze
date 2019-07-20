# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/dialog.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(400, 300)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.textEdit = QtGui.QTextEdit(Dialog)
        self.textEdit.setGeometry(QtCore.QRect(40, 50, 321, 79))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.answerList = QtGui.QListView(Dialog)
        self.answerList.setGeometry(QtCore.QRect(40, 190, 321, 41))
        self.answerList.setObjectName(_fromUtf8("answerList"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(40, 30, 281, 20))
        self.label.setObjectName(_fromUtf8("label"))
        self.notebookFile = QtGui.QPushButton(Dialog)
        self.notebookFile.setGeometry(QtCore.QRect(100, 150, 181, 32))
        self.notebookFile.setObjectName(_fromUtf8("notebookFile"))

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label.setText(_translate("Dialog", "instructions", None))
        self.notebookFile.setText(_translate("Dialog", "choose notebook", None))


class Dialog(QtGui.QDialog, Ui_Dialog):
    def __init__(self, parent=None, f=QtCore.Qt.WindowFlags()):
        QtGui.QDialog.__init__(self, parent, f)

        self.setupUi(self)


# -*- coding: utf-8 -*-
#Copyright 2015 Mathilde Daures, Anatalole Gesnouin
#---------------------------------------------------------------------
#This file is part of ExAM.

#ExAM is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#ExAM is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with ExAM.  If not, see <http://www.gnu.org/licenses/>.
#---------------------------------------------------------------------

__author__ = 'anatole'

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import os
import sys
import datetime


class ConcordanceDialog(QDialog):

    default_path = os.path.abspath(os.path.dirname(sys.argv[0])) + os.sep \
                   + "Ressources" + os.sep + "Concordance"
    time = datetime.date.today().isoformat()

    def __init__(self, parent=None):

        super(ConcordanceDialog, self).__init__(parent)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("This is how you should format your "
                                "entries (Patient_name or Phenotype) "
                                "to cross file "
                                ":"))
        layout.addWidget(QLabel("Entry"))
        self.line_ed = QLineEdit()
        self.list = QListWidget()
        layout.addWidget(self.line_ed)
        layout.addWidget(self.list)
        button_layout = QHBoxLayout()
        clear_button = QPushButton("C&lear")
        create_button = QPushButton("C&reate")
        cancel_button = QPushButton("&Cancel")
        clear_button.setAutoDefault(False)
        create_button.setAutoDefault(False)
        cancel_button.setAutoDefault(False)
        button_layout.addWidget(clear_button)
        button_layout.addWidget(create_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        self.setLayout(layout)
        self.connect(self.line_ed, SIGNAL("returnPressed()"), self.addToList)
        clear_button.connect(clear_button, SIGNAL("clicked()"), self.onClearClicked)
        create_button.connect(create_button, SIGNAL("clicked()"), self.onCreatecliked)
        cancel_button.connect(cancel_button, SIGNAL("clicked()"), self.onCancelClicked)

    def onCreatecliked(self):
        if os.access(self.default_path, os.W_OK):
            if self.list.count() != 0:
                f = open(os.path.join(self.default_path, self.time), "w")
                for i in range(self.list.count()):
                    f.write(str(self.list.item(i).text()) + os.linesep)
                self.done(1)
            else:
                bob = QMessageBox(self)
                bob.setText("You need to type in something to create a file !")
                bob.exec_()
        else:
            bob = QMessageBox(self)
            bob.setText("<p align='center'>For some reason you can't write in this directory :<br/>" + self.default_path
                        + "<br/>please change your directory's permissions</p>.")
            bob.exec_()

    def onCancelClicked(self):
        self.done(0)

    def onClearClicked(self):
        self.list.clear()

    def getNewFileName(self):
        return os.path.join(self.default_path, self.time)

    def addToList(self):
        if not self.list.findItems(self.line_ed.text(), Qt.MatchExactly):
            self.list.addItem(QListWidgetItem(self.line_ed.text()))
        self.line_ed.clear()
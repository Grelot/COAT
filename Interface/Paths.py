# -*- coding: utf-8 -*-
#Copyright 2015 Mathilde Daures, Anatole Gesnouin
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


class Paths1(QWidget):

    def __init__(self, name, default, path=os.path.abspath(os.sep)):
        super(Paths1, self).__init__()
        self.default = default
        lab = QLabel(name)
        lab.setFixedWidth(200)
        self.ed = QLineEdit()
        self.ed.setText(path)
        self.ed.setReadOnly(True)
        but = QPushButton("Browse")
        self.connect(but, SIGNAL("clicked()"), self.setPath)
        lay = QHBoxLayout()
        lay.addWidget(lab)
        lay.addWidget(self.ed)
        lay.addWidget(but)
        self.setLayout(lay)

    def setPath(self):
        tmp = QFileDialog.getOpenFileName(self, "Select file or Dir", ".")
        if tmp != "":
            self.ed.setText(tmp)

    def setDefault(self):
        self.ed.setText(self.default)


class Paths2(QWidget):

    def __init__(self, name, default, path=os.path.abspath(os.sep)):
        super(Paths2, self).__init__()
        self.default = default
        lab = QLabel(name)
        lab.setFixedWidth(200)
        self.ed = QLineEdit()
        self.ed.setText(path)
        self.ed.setReadOnly(True)
        but = QPushButton("Browse")
        self.connect(but, SIGNAL("clicked()"), self.setPath)
        lay = QHBoxLayout()
        lay.addWidget(lab)
        lay.addWidget(self.ed)
        lay.addWidget(but)
        self.setLayout(lay)

    def setPath(self):
        tmp = QFileDialog.getExistingDirectory(self, "Open Directory",
                                             ".",
                                             QFileDialog.ShowDirsOnly
                                             | QFileDialog.DontResolveSymlinks)
        if tmp != "":
            if tmp[-1] != os.sep:
                tmp += os.sep
            self.ed.setText(tmp)

    def setDefault(self):
        self.ed.setText(self.default)
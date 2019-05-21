# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from Paths import Paths1, Paths2
import os
import sys
import pickle

class AdvSettings(QtGui.QWidget):
    adv_save_file = os.path.abspath(os.path.dirname(sys.argv[0])) + os.sep + "SAVE/adv_set_save"
    bamFile_def = "/storage/bams/"
    samtools_def = "/GenAnalysis/src/samtools-1.3/"
    ref_hgtables_def = "/works/monodiab/pierre/covvar_v2/refFlat.txt"
    resultsDir_def = ""


    def __init__(self):
        super(AdvSettings, self).__init__()

        if not os.path.isfile(self.adv_save_file):
            self.resetAdvSettings()
        else:
            f = file(self.adv_save_file, "r")
            adv_save = pickle.load(f)
            f.close()
        '''
        save = {}

        save["bamdir"] = "test"
        save["samtls"] = "tessamtools"
        save["refhg"]  ="refhg"
        save["resdir"] = "resdede"
        '''

        self.advSetQVBox = QtGui.QVBoxLayout()
        self.advSetQVBox.setObjectName("advSetQVBox")
        self.bamFile = Paths2("bam files folder", self.bamFile_def, adv_save["bamdir"])
        self.samtools = Paths2("samtools folder", self.samtools_def, adv_save["samtls"])
        self.ref_hgtables = Paths1("hg tables reference file", self.ref_hgtables_def, adv_save["refhg"])
        self.res_path = Paths2("results folder", self.resultsDir_def, adv_save["resdir"])

        self.advSetQVBox.addWidget(self.bamFile)
        self.advSetQVBox.addWidget(self.samtools)
        self.advSetQVBox.addWidget(self.ref_hgtables)
        self.advSetQVBox.addWidget(self.res_path)

        #Buttons : OK, Cancel
        ok = QtGui.QPushButton("&Ok")
        ok.setObjectName("BUTTON")
        self.cancel = QtGui.QPushButton("&Cancel")
        self.cancel.setObjectName("BUTTON")
        self.connect(ok, QtCore.SIGNAL("clicked()"), self.onOkClicked)
        but_layout = QtGui.QHBoxLayout()
        but_layout.addWidget(self.cancel)
        but_layout.addWidget(ok)

        self.advSetQVBox.addLayout(but_layout)


        self.setLayout(self.advSetQVBox)

    def resetAdvSettings(self):
        adv_save = dict()
        adv_save["bamdir"] = self.bamFile_def
        adv_save["samtls"] = self.samtools_def
        adv_save["refhg"]  = self.ref_hgtables_def
        adv_save["resdir"] = self.resultsDir_def
        f = file(self.adv_save_file, "w")
        pickle.dump(adv_save, f, -1)
        f.close()


    def onOkClicked(self):
        adv_save = dict()
        adv_save["bamdir"] = self.bamFile.ed.text()
        adv_save["samtls"] = self.samtools.ed.text()
        adv_save["refhg"] = self.ref_hgtables.ed.text()
        adv_save["resdir"] = self.res_path.ed.text()
        f = file(self.adv_save_file, "w")
        pickle.dump(adv_save, f, -1)
        f.close()
        #self.filter_order.saveToFile()
        self.cancel.click()

    def onAdvSettingsClicked(self):
        f = file(self.adv_save_file, "r")
        adv_save = pickle.load(f)
        f.close()
        self.bamFile.ed.setText(adv_save["bamdir"])
        self.samtools.ed.setText(adv_save["samtls"])
        self.ref_hgtables.ed.setText(adv_save["refhg"])
        self.res_path.ed.setText(adv_save["resdir"])
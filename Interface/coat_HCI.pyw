# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from Wire import Coatwire
import sys
import os
import pickle
from AdvSettings import AdvSettings


def main(args):
    app = QtGui.QApplication(args)
    win = MainWindow()
    win.show()
    return app.exec_()


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






class MainWindow(QtGui.QMainWindow):
    coat_save_file = os.path.abspath(os.path.dirname(sys.argv[0])) + os.sep + "SAVE/coat_save"
    coordinates_def = "chr:start-end"
    geneName_def = "geneName"
    subjects_def = ""
    covThreshold_def = 5
    mapQual_def = 20

    def __init__(self):
        if not os.path.isfile(self.coat_save_file):
            self.adv_settings = AdvSettings()
            self.reset_main_coat()
        else:
            f = file(self.coat_save_file, "r")
            coat_save = pickle.load(f)
            f.close()

        QtGui.QMainWindow.__init__(self)
        self.setWindowTitle(_fromUtf8("COverage Analysis Tool"))
        self.setFixedSize(640, 820)

        #size of resolution screen
        #app_res = QtGui.QApplication([])
        '''
        screen_resolution = app.desktop().screenGeometry()
        width_screen, height_screen = screen_resolution.width(), screen_resolution.height()
        if int(width_screen) < 641 or int(height_screen) < 821:
            self.setFixedSize(480, 640)
        else:
            self.setFixedSize(640, 820)
        '''
        coat_widget = QtGui.QWidget()
        coat_main = QtGui.QVBoxLayout()

        #----------------------------------------------------------------------
        #advanced settings, save settings, reset

        self.box = QtGui.QGroupBox()
        self.box.setFixedWidth(600)
        settings_layout = QtGui.QVBoxLayout()
        path_group = QtGui.QWidget()
        path_lay = QtGui.QGridLayout()

        #advanced settings button
        self.advSetQPushButton = QtGui.QPushButton()
        self.advSetQPushButton.setObjectName(_fromUtf8("advSetQPushButton"))
        #save settings button
        self.saveQPushButton = QtGui.QPushButton()
        self.saveQPushButton.setObjectName(_fromUtf8("saveQPushButton"))
        #reset button
        self.resetQPushButton = QtGui.QPushButton()
        self.resetQPushButton.setObjectName(_fromUtf8("resetQPushButton"))

        path_lay.addWidget(self.advSetQPushButton, 0, 0, 2, 1)
        path_lay.addWidget(self.saveQPushButton, 0,1, 2, 1)
        path_lay.addWidget(self.resetQPushButton, 0,2, 2, 1)

        path_group.setLayout(path_lay)
        settings_layout.addWidget(path_group)
        self.box.setLayout(settings_layout)
        
        #----------------------------------------------------------------------
        #listOfsubjects

        self.box2 = QtGui.QGroupBox("Select subject :")
        self.box2.setFixedWidth(600)
        settings_layout2 = QtGui.QVBoxLayout()
        path_group2 = QtGui.QWidget()
        path_lay2 = QtGui.QGridLayout()

        self.subjectsQLineEdit = QtGui.QLineEdit()
        self.subjectsQLineEdit.setObjectName(_fromUtf8("subjectsQLineEdit"))
        self.subjectLabel = QtGui.QLabel(self.subjectsQLineEdit)

        path_lay2.addWidget(self.subjectsQLineEdit, 0, 0, 2, 1)
        path_lay2.addWidget(self.subjectLabel, 0,1, 2, 1)

        path_group2.setLayout(path_lay2)
        settings_layout2.addWidget(path_group2)
        self.box2.setLayout(settings_layout2)

        #----------------------------------------------------------------------
        #region

        self.box3 = QtGui.QGroupBox("Select region :")
        self.box3.setFixedWidth(600)
        settings_layout3 = QtGui.QVBoxLayout()
        path_group3 = QtGui.QWidget()
        path_lay3 = QtGui.QGridLayout()

        #coordinates chr start end
        self.coordinatesQRadioButton = QtGui.QRadioButton()
        self.coordinatesQRadioButton.setObjectName(_fromUtf8("coordinatesQRadioButton"))
        self.coordinateQLineEdit = QtGui.QLineEdit()
        self.coordinateQLineEdit.setObjectName(_fromUtf8("coordinateQLineEdit"))
        #gene name
        self.geneNameQRadioButton = QtGui.QRadioButton()
        self.geneNameQRadioButton.setObjectName(_fromUtf8("geneNameQRadioButton"))
        self.geneNameQLineEdit = QtGui.QLineEdit()
        self.geneNameQLineEdit.setObjectName(_fromUtf8("geneNameQLineEdit"))
        #label by default cds
        self.cdsOnlyLabel = QtGui.QLabel("[default] show coding DNA sequence (CDS)")
        #add UTR
        self.addUTRQCheckBox = QtGui.QCheckBox()
        self.addUTRQCheckBox.setObjectName(_fromUtf8("addUTRQCheckBox"))
        #add intronic region
        self.addIntronQCheckBox = QtGui.QCheckBox()
        self.addIntronQCheckBox.setObjectName(_fromUtf8("addIntronQCheckBox"))


        path_lay3.addWidget(self.coordinatesQRadioButton, 0, 0)
        path_lay3.addWidget(self.coordinateQLineEdit, 0,1)
        path_lay3.addWidget(self.geneNameQRadioButton, 1, 0)
        path_lay3.addWidget(self.geneNameQLineEdit, 1,1)
        path_lay3.addWidget(self.cdsOnlyLabel, 2, 1)
        path_lay3.addWidget(self.addUTRQCheckBox, 3,1)
        path_lay3.addWidget(self.addIntronQCheckBox, 4, 1)

        path_group3.setLayout(path_lay3)
        settings_layout3.addWidget(path_group3)
        self.box3.setLayout(settings_layout3)

        #----------------------------------------------------------------------
        #settings depth coverage threshold, quality threshold

        self.box4 = QtGui.QGroupBox("Select coverage thresholds :")
        self.box4.setFixedWidth(600)
        settings_layout4 = QtGui.QVBoxLayout()
        path_group4 = QtGui.QWidget()
        path_lay4 = QtGui.QGridLayout()

        self.covThresholdQSpinBox = QtGui.QSpinBox()
        self.covThresholdQSpinBox.setObjectName(_fromUtf8("covThresholdQSpinBox"))
        self.covThresholdLabel = QtGui.QLabel(self.covThresholdQSpinBox)
        self.covThresholdQSpinBox.setMaximum(9999)

        self.mapQualThresholdQSpinBox = QtGui.QSpinBox()
        self.mapQualThresholdQSpinBox.setObjectName(_fromUtf8("mapQualThresholdQSpinBox"))
        self.mapQualThresholdLabel = QtGui.QLabel(self.mapQualThresholdQSpinBox)
        self.mapQualThresholdQSpinBox.setMaximum(999)


        path_lay4.addWidget(self.covThresholdQSpinBox,0,0)
        path_lay4.addWidget(self.covThresholdLabel,0,1)
        path_lay4.addWidget(self.mapQualThresholdQSpinBox,1,0)
        path_lay4.addWidget(self.mapQualThresholdLabel,1,1)

        path_group4.setLayout(path_lay4)
        settings_layout4.addWidget(path_group4)
        self.box4.setLayout(settings_layout4)

        #----------------------------------------------------------------------
        #generate additional files

        self.box5 = QtGui.QGroupBox("Generate additional files :")
        self.box5.setFixedWidth(600)
        settings_layout5 = QtGui.QVBoxLayout()
        path_group5 = QtGui.QWidget()
        path_lay5 = QtGui.QGridLayout()

        #label by default uncovered file
        self.defaultuncovfileLabel = QtGui.QLabel("[default] uncovered regions file")
        self.coveredfileQCheckBox = QtGui.QCheckBox()
        self.coveredfileQCheckBox.setObjectName(_fromUtf8("coveredfileQCheckBox"))
        self.ucscfileQCheckBox = QtGui.QCheckBox()
        self.ucscfileQCheckBox.setObjectName(_fromUtf8("ucscfileQCheckBox"))



        path_lay5.addWidget(self.defaultuncovfileLabel,0,0)
        path_lay5.addWidget(self.coveredfileQCheckBox,1,0)
        path_lay5.addWidget(self.ucscfileQCheckBox,2,0)

        path_group5.setLayout(path_lay5)
        settings_layout5.addWidget(path_group5)
        self.box5.setLayout(settings_layout5)




        #----------------------------------------------------------------------
        #quit and launch

        self.box6 = QtGui.QGroupBox()
        self.box6.setFixedWidth(600)
        settings_layout6 = QtGui.QVBoxLayout()
        path_group6 = QtGui.QWidget()
        path_lay6 = QtGui.QGridLayout()


        self.covAnalysisQPushButton = QtGui.QPushButton()
        self.covAnalysisQPushButton.setObjectName(_fromUtf8("covAnalysisQPushButton"))
        self.quit_but = QtGui.QPushButton("&Quit")
        self.connect(self.quit_but, QtCore.SIGNAL("clicked()"), self, QtCore.SLOT("close()"))

        path_lay6.addWidget(self.quit_but,0,0)
        path_lay6.addWidget(self.covAnalysisQPushButton,0,1)

        path_group6.setLayout(path_lay6)
        settings_layout6.addWidget(path_group6)
        self.box6.setLayout(settings_layout6)

        #----------------------------------------------------------------------
        #NAMES

        self.subjectLabel.setText(QtGui.QApplication.translate("MainWindow","subjects", None))

        self.advSetQPushButton.setText(_translate("MainWindow", "advanced settings", None))
        self.resetQPushButton.setText(_translate("MainWindow", "reset", None))
        self.saveQPushButton.setText(_translate("MainWindow", "save settings", None))


        self.coordinatesQRadioButton.setText(_translate("MainWindow", "coordinates", None))
        self.geneNameQRadioButton.setText(_translate("MainWindow", "gene name", None))

        self.addUTRQCheckBox.setText(_translate("MainWindow", "add untranslated regions (UTR)", None))
        self.addIntronQCheckBox.setText(_translate("MainWindow", "add intronic regions", None))

        self.covThresholdLabel.setText(_translate("MainWindow", "coverage threshold", None))
        self.mapQualThresholdLabel.setText(_translate("MainWindow", "mapping quality threshold", None))

        self.coveredfileQCheckBox.setText(_translate("MainWindow", "covered regions file", None))
        self.ucscfileQCheckBox.setText(_translate("MainWindow", "UCSC custom track of uncovered regions (.GFF)", None))

        self.covAnalysisQPushButton.setText(_translate("MainWindow", "coverage checking", None))

        #----------------------------------------------------------------------
        #display widgets

        quit_but = QtGui.QPushButton("&Quit")
        quit_but.setObjectName("Quit")

        scroll = QtGui.QScrollArea()
        scroll_layout = QtGui.QVBoxLayout()
        scroll_container = QtGui.QWidget()
        scroll_layout.addWidget(self.box)
        scroll_layout.addWidget(self.box2)
        scroll_layout.addWidget(self.box3)
        scroll_layout.addWidget(self.box4)
        scroll_layout.addWidget(self.box5)
        scroll_layout.addWidget(self.box6)
        scroll_container.setLayout(scroll_layout)
        scroll.setWidget(scroll_container)


        #coat_main.addLayout(self.Widget_1_QHBox)
        #coat_main.addLayout(self.Widget_2_QHBox)
        #coat_main.addLayout(self.Widget_3a_QVBox)
        #coat_main.addLayout(self.Widget_3b_QVBox)
        #coat_main.addLayout(self.Widget_4_QVBox)
        #coat_main.addWidget(quit_but)

        coat_main.addWidget(scroll)
        coat_widget.setLayout(coat_main)





        self.adv_settings = AdvSettings()


        self.multiplex = QtGui.QStackedWidget()
        self.multiplex.addWidget(coat_widget)
        self.multiplex.addWidget(self.adv_settings)
        self.setCentralWidget(self.multiplex)

        self.connect(quit_but, QtCore.SIGNAL("clicked()"),self, QtCore.SLOT("close()"))        

        self.connect(self.advSetQPushButton, QtCore.SIGNAL("clicked()"),self.goToAdvSettings)

        self.adv_settings.connect(self.adv_settings.cancel, QtCore.SIGNAL("clicked()"),self.goToMenu)


        self.connect(self.resetQPushButton, QtCore.SIGNAL("clicked()"), self.onResetClicked)
        
        self.connect(self.saveQPushButton, QtCore.SIGNAL("clicked()"), self.onSaveClicked)

        #self.dialogTextBrowser = DialogueNameAnalysis(self)
        self.connect(self.covAnalysisQPushButton, QtCore.SIGNAL("clicked()"), self.onAnalysisClicked)
        #self.connect(self.covAnalysisQPushButton, QtCore.SIGNAL("clicked()"), self.dialogue_name_analysis)

        #download coat_save
        self.geneNameQLineEdit.setText(_translate("MainWindow", coat_save["gene"], None))
        self.coordinateQLineEdit.setText(_translate("MainWindow", coat_save["coo"], None))
        self.subjectsQLineEdit.setText(_translate("MainWindow", coat_save["subjects"], None))

        self.covThresholdQSpinBox.setValue(coat_save["covT"])
        self.mapQualThresholdQSpinBox.setValue(coat_save["mapQT"])
        self.coordinatesQRadioButton.setChecked(coat_save["modC"])
        self.geneNameQRadioButton.setChecked(coat_save["modG"])
        #self.cdsOnlyQCheckBox.setCheckState(coat_save["cds"])



    def goToAdvSettings(self):
        self.multiplex.setCurrentIndex(1)
        self.adv_settings.onAdvSettingsClicked()
        self.setWindowTitle("CoAT - Settings")


    def goToMenu(self):
        self.multiplex.setCurrentIndex(0)
        self.setWindowTitle("COverage Analysis Tool")


    def reset_main_coat(self):
        coat_save = dict()
        coat_save["coo"] = self.coordinates_def
        coat_save["gene"] = self.geneName_def

        coat_save["modC"] = True
        coat_save["modG"] = False
        coat_save["covT"] = self.covThreshold_def
        coat_save["mapQT"] = self.mapQual_def
        coat_save["subjects"] = self.subjects_def
        self.adv_settings.resetAdvSettings()
        f = file(self.coat_save_file, "w")
        pickle.dump(coat_save, f, -1)
        f.close()

        self.geneNameQLineEdit.setText(_translate("MainWindow", coat_save["gene"], None))
        self.coordinateQLineEdit.setText(_translate("MainWindow", coat_save["coo"], None))
        self.subjectsQLineEdit.setText(_translate("MainWindow", coat_save["subjects"], None))
        self.covThresholdQSpinBox.setValue(coat_save["covT"])
        self.mapQualThresholdQSpinBox.setValue(coat_save["mapQT"])
        self.coordinatesQRadioButton.setChecked(coat_save["modC"])
        self.geneNameQRadioButton.setChecked(coat_save["modG"])



    def onResetClicked(self):
        self.reset_main_coat()

    def onSaveClicked(self):
        self.adv_settings.onOkClicked()
        coordinates = self.coordinateQLineEdit.text()
        geneName = self.geneNameQLineEdit.text()
        subjects = self.subjectsQLineEdit.text()
        covT = self.covThresholdQSpinBox.text()
        mapQT = self.mapQualThresholdQSpinBox.text()
        coat_save = dict()
        coat_save["coo"] = str(coordinates)
        coat_save["gene"] = str(geneName)
        coat_save["subjects"] = str(subjects)
        coat_save["modC"] = self.coordinatesQRadioButton.isChecked()
        coat_save["modG"] = self.geneNameQRadioButton.isChecked()
        coat_save["covT"] = int(covT)
        coat_save["mapQT"] = int(mapQT)
        f = file(self.coat_save_file, "w")
        pickle.dump(coat_save, f, -1)
        f.close()




    def onAnalysisClicked(self):
        if self.coordinatesQRadioButton.isChecked():
            coordinate = str(self.coordinateQLineEdit.text())
            geneName = None
        else:
            geneName = str(self.geneNameQLineEdit.text())
            coordinate = None
        covT = self.covThresholdQSpinBox.text()
        mapQT = self.mapQualThresholdQSpinBox.text()
        subjects = self.subjectsQLineEdit.text()
        bamFile = self.adv_settings.bamFile.ed.text()
        samtools = self.adv_settings.samtools.ed.text()
        ref_hgtable = self.adv_settings.ref_hgtables.ed.text()
        resultsPath = self.adv_settings.res_path.ed.text()
        all_args = {}

        all_args["coordinate"] = coordinate
        all_args["geneName"] = geneName
        all_args["covT"] = int(covT)
        all_args["mapQT"] = int(mapQT)
        all_args["bamdir"] = str(bamFile)
        all_args["samtools"] = str(samtools)
        all_args["ref_hgtable"] = str(ref_hgtable)
        all_args["resdir"] = str(resultsPath)
        all_args["subjects"] = str(subjects)
        if self.addIntronQCheckBox.checkState():
            all_args["intron"] = True
        else:
            all_args["intron"] = None
        if self.addUTRQCheckBox.checkState():
            all_args["utr"] = True
        else:
            all_args["utr"] = None
        if self.coveredfileQCheckBox.checkState():
            all_args["uncov"] = True
        else:
            all_args["uncov"] = None
        if self.ucscfileQCheckBox.checkState():
            all_args["ucsc"] = True
        else:
            all_args["ucsc"] = None
        print all_args
        Coatwire(all_args)


if __name__ == "__main__":
    main(sys.argv)











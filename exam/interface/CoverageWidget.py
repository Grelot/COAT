from PyQt4.QtCore import *
from PyQt4.QtGui import *
import os
import sys
import pickle
from ConcordanceDialog import ConcordanceDialog
from Wire import Coatwire

class CoverageWidget(QWidget):
    save_file = os.path.abspath(os.path.dirname(sys.argv[0])) + os.sep + "Ressources" + os.sep + "Settings" + os.sep + "paths"
    def __init__(self):
        super(CoverageWidget, self).__init__()
        self.box = QGroupBox("Subjects to analyse :")
        self.box.setFixedWidth(820)
        settings_layout = QVBoxLayout()
        path_group = QWidget()
        path_lay = QGridLayout()

        #self.subjectsQLineEdit = QLineEdit()
        #self.subjectsQLineEdit.setObjectName("subjectsQLineEdit")
        index_lab = QLabel("<u><b>Subjects List File:</b></u>")
        path_lay.addWidget(index_lab, 1, 0, 2, 1)
        self.concordance_path = QLineEdit()
        self.concordance_path.setReadOnly(True)
        dir_button = QPushButton("Choose file")
        create_button = QPushButton("Create file")
        dir_button.connect(dir_button, SIGNAL("clicked()"), self.onConcordanceSearch)
        create_button.connect(create_button, SIGNAL("clicked()"), self.onCreateClicked)

        path_lay.addWidget(self.concordance_path, 1, 1, 2, 1)
        path_lay.addWidget(dir_button, 1, 2)
        path_lay.addWidget(create_button, 2, 2)

        #-------------
        #path_lay.addWidget(self.subjectsQLineEdit, 0, 1)
        path_group.setLayout(path_lay)
        settings_layout.addWidget(path_group)
        self.box.setLayout(settings_layout)

        self.box2 = QGroupBox("Region to analyse :")
        self.box2.setFixedWidth(820)
        settings_layout2 = QVBoxLayout()
        path_group2 = QWidget()
        path_lay2 = QGridLayout()

        self.coordinateOrGene = QButtonGroup()

        self.coordinatesQRadioButton = QRadioButton()
        self.coordinatesQRadioButton.setObjectName("coordinatesQRadioButton")
        self.coordinateOrGene.addButton(self.coordinatesQRadioButton)
        self.coordinateLabel = QLabel("<u><b>Coordinates</b></u>")
        self.coordinateQLineEdit = QLineEdit()
        self.coordinateQLineEdit.setObjectName("coordinateQLineEdit")
        path_lay2.addWidget(self.coordinatesQRadioButton,0,0)
        path_lay2.addWidget(self.coordinateLabel,0,1)
        path_lay2.addWidget(self.coordinateQLineEdit,0,2)

        self.geneNameQRadioButton = QRadioButton()
        self.geneNameQRadioButton.setObjectName("geneNameQRadioButton")
        self.coordinateOrGene.addButton(self.geneNameQRadioButton)
        self.geneNameLabel = QLabel("<u><b>Gene Name</b></u>")
        self.geneNameQLineEdit = QLineEdit()
        self.geneNameQLineEdit.setObjectName("geneNameQLineEdit")

        path_lay2.addWidget(self.geneNameQRadioButton,1,0)
        path_lay2.addWidget(self.geneNameLabel,1,1)
        path_lay2.addWidget(self.geneNameQLineEdit,1,2)

        self.geneNameQRadioButton.setChecked(True)

        path_group2.setLayout(path_lay2)
        settings_layout2.addWidget(path_group2)
        self.box2.setLayout(settings_layout2)

        #self.exonAllLabel = QLabel("<u><b>all gene exon regions</b></u>")
        #self.exonAllQRadioButton = QRadioButton()
        #self.exonAllQRadioButton.setObjectName("exonAllQRadioButton")
        #self.exonNumbLabel = QLabel("<u><b>gene exon number region</b></u>")
        #self.exonNumbQRadioButton = QRadioButton()
        #self.exonNumbQRadioButton.setObjectName("exonNumbQRadioButton")
        #self.exonNumbQSpinBox = QSpinBox()
        #self.exonNumbQSpinBox.setMinimum(1)
        #self.exonNumbQSpinBox.setObjectName("exonNumbQSpinBox")


        self.cdsOnlyLabel = QLabel("[default]")
        self.cdsOnlyLabel2 = QLabel("show coding DNA sequence (CDS)")
        self.cdsOnlyQCheckBox = QCheckBox()
        self.cdsOnlyQCheckBox.setObjectName("cdsOnlyQCheckBox")

        self.utrLabel = QLabel("<u><b>add untranslated regions (UTR)</b></u>")
        self.addUTRQCheckBox = QCheckBox()
        self.addUTRQCheckBox.setObjectName("addUTRQCheckBox")
        self.intronLabel = QLabel("<u><b>add intronic regions</b></u>")
        self.addIntronQCheckBox = QCheckBox()
        self.addIntronQCheckBox.setObjectName("addIntronQCheckBox")

        #path_lay2.addWidget(self.exonAllLabel,2,2)
        #path_lay2.addWidget(self.exonAllQRadioButton,2,1)
        #path_lay2.addWidget(self.exonNumbLabel,3,2)
        #path_lay2.addWidget(self.exonNumbQRadioButton,3,1)
        #path_lay2.addWidget(self.exonNumbQSpinBox,3,3)
        path_lay2.addWidget(self.cdsOnlyLabel,5,1)
        path_lay2.addWidget(self.cdsOnlyLabel2,5,2)
        #path_lay2.addWidget(self.cdsOnlyQCheckBox,5,1)
        path_lay2.addWidget(self.utrLabel,6,2)
        path_lay2.addWidget(self.addUTRQCheckBox,6,1)
        path_lay2.addWidget(self.intronLabel,7,2)
        path_lay2.addWidget(self.addIntronQCheckBox,7,1)


        self.cdsOnlyQCheckBox.setChecked(True)



        self.box3 = QGroupBox("Thresholds :")
        self.box3.setFixedWidth(820)
        settings_layout3 = QVBoxLayout()
        path_group3 = QWidget()
        path_lay3 = QGridLayout()

        self.covThresholdQSpinBox = QSpinBox()
        self.covThresholdQSpinBox.setObjectName("covThresholdQSpinBox")
        self.covThresholdQSpinBox.setRange(1, 500)
        self.covThresholdQSpinBox.setValue(5)
        self.covThresholdLabel = QLabel("<u><b>coverage depth</b></u>")

        self.mapQualThresholdQSpinBox = QSpinBox()
        self.mapQualThresholdQSpinBox.setObjectName("mapQualThresholdQSpinBox")
        self.mapQualThresholdQSpinBox.setRange(1, 254)
        self.mapQualThresholdQSpinBox.setValue(13)
        self.mapQualThresholdLabel = QLabel("<u><b>mapping quality</b></u>")


        path_lay3.addWidget(self.covThresholdQSpinBox, 0, 0)
        path_lay3.addWidget(self.covThresholdLabel, 0, 1)
        path_lay3.addWidget(self.mapQualThresholdQSpinBox, 1, 0)
        path_lay3.addWidget(self.mapQualThresholdLabel, 1, 1)

        path_group3.setLayout(path_lay3)
        settings_layout3.addWidget(path_group3)
        self.box3.setLayout(settings_layout3)

        self.box4 = QGroupBox("Generate additionnal files :")
        self.box4.setFixedWidth(820)
        settings_layout4 = QVBoxLayout()
        path_group4 = QWidget()
        path_lay4 = QGridLayout()

        self.outputNameQLineEdit = QLineEdit()
        self.outputNameQLineEdit.setObjectName("outputNameLineEdit")


        self.coverFileLabel = QLabel("<u><b>Covered regions file</b></u>")
        self.coverFileCheckBox = QCheckBox()
        self.coverFileCheckBox.setObjectName("coverFileCheckBox")
        self.ucscTrackLabel = QLabel("<u><b>UCSC Genome Browser track file of uncovered regions</b></u>")
        self.ucscTrackCheckBox = QCheckBox()
        self.ucscTrackCheckBox.setObjectName("ucscTrackCheckBox")

        path_lay4.addWidget(self.coverFileCheckBox, 0, 0)
        path_lay4.addWidget(self.coverFileLabel, 0, 1)
        path_lay4.addWidget(self.ucscTrackCheckBox, 1, 0)
        path_lay4.addWidget(self.ucscTrackLabel, 1, 1)

        path_group4.setLayout(path_lay4)
        settings_layout4.addWidget(path_group4)
        self.box4.setLayout(settings_layout4)

        scroll = QScrollArea()
        scroll_layout = QVBoxLayout()
        scroll_container = QWidget()
        scroll_layout.addWidget(self.box)
        scroll_layout.addWidget(self.box2)
        scroll_layout.addWidget(self.box3)
        scroll_layout.addWidget(self.box4)
        scroll_container.setLayout(scroll_layout)
        scroll.setWidget(scroll_container)


        ok = QPushButton("&Launch")
        ok.setObjectName("BUTTON")
        self.cancel = QPushButton("&Cancel")
        self.cancel.setObjectName("BUTTON")
        self.connect(ok, SIGNAL("clicked()"), self.onOkClicked)

        but_layout = QHBoxLayout()
        but_layout.addWidget(self.cancel)
        but_layout.addWidget(ok)


        lay = QVBoxLayout()
        lay.addWidget(scroll)
        lay.addLayout(but_layout)
        self.setLayout(lay)



    def onOkClicked(self):
        f = file(self.save_file, "r")
        save = pickle.load(f)
        f.close()
        resultsPath = save["res"]

        ref_hgtable = save["reference"]

        samtools = save["samtools"]
        bams_path = save["bams"]

        if self.coordinatesQRadioButton.isChecked():
            coordinate = str(self.coordinateQLineEdit.text())
            geneName = None
        else:
            geneName = str(self.geneNameQLineEdit.text())
            coordinate = None
        #exon = self.exonNumbQSpinBox.text()
        covT = self.covThresholdQSpinBox.text()
        mapQT = self.mapQualThresholdQSpinBox.text()
        subjectsFile = str(self.concordance_path.text())
        subjects = ""
        with open(subjectsFile, "r") as subFile:
            for subj in subFile.readlines():
                subjects += subj[:-1]
                subjects += ","
            subjects = subjects[:-1]
        all_args = {}
        #all_args["analysis"] = self.outputNameQLineEdit.text()
        all_args["coordinate"] = coordinate
        all_args["geneName"] = geneName
        #all_args["exon"] = exon
        all_args["covT"] = int(covT)
        all_args["mapQT"] = int(mapQT)
        all_args["bamdir"] = str(bams_path)
        all_args["samtools"] = str(samtools)
        all_args["ref_hgtable"] = str(ref_hgtable)
        all_args["resdir"] = str(resultsPath)
        all_args["subjects"] = str(subjects)
        if self.cdsOnlyQCheckBox.checkState():
            all_args["cds_only"] = True
        else:
            all_args["cds_only"] = None
        if self.addIntronQCheckBox.checkState():
            all_args["intron"] = True
        else:
            all_args["intron"] = None
        if self.addUTRQCheckBox.checkState():
            all_args["utr"] = True
        else:
            all_args["utr"] = None
        if self.ucscTrackCheckBox.checkState():
            all_args["ucscF"] = True
        else:
            all_args["ucscF"] = None
        if self.coverFileCheckBox.checkState():
            all_args["covF"] = True
        else:
            all_args["covF"] = None

        #if self.exonAllQRadioButton.isChecked():
        #    all_args["allEx"] = True
        #else:
        #    all_args["allEx"] = None
        #if self.exonNumbQRadioButton.isChecked():
        #    all_args["1Ex"] = True
        #else:
        #    all_args["1Ex"] = None
        #print all_args
        Coatwire(all_args)

    #concordance...
    def onConcordanceSearch(self):
        path = QFileDialog.getOpenFileName(self, "Find file")
        if path != "" and os.access(path, os.R_OK):
            self.concordance_path.setText(path)
        # return path
    def onConcordanceSearch2(self):
        path = QFileDialog.getOpenFileName(self, "Find file")
        if path != "" and os.access(path, os.R_OK):
            self.concordance_path2.setText(path)
        # return path

    def onCreateClicked(self):
        bob = ConcordanceDialog(self)
        tmp = bob.exec_()
        if tmp:
            self.concordance_path.setText(bob.getNewFileName())
    def onCreateClicked2(self):
        bob = ConcordanceDialog(self)
        tmp = bob.exec_()
        if tmp:
            self.concordance_path2.setText(bob.getNewFileName())
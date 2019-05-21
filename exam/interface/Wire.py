# -*- coding: utf-8 -*-
import os
import re
import sys
import subprocess


class Coatwire():


    def __init__(self, all_args):


        #mypath = os.path.dirname(sys.argv[0]).split("Interface")[0]
        #all_args["ref_hgtable"] = mypath + "/Coverage/refFlat.txt"


        print "CoAT process..."
        print "BAM Files directory : {0}".format(all_args["bamdir"])
        print "samtools directory : {0}".format(all_args["samtools"])

        print "ref hgtables : {0}".format(all_args["ref_hgtable"])
        print "results directory : {0}".format(all_args["resdir"])

        print "list of subjects : "
        for sub in all_args["subjects"].split(","):
            print sub

        if all_args["coordinate"]:
            print "coordinates : {0}".format(all_args["coordinate"])
            print "-"
        else:
            print "geneName : {0}".format(all_args["geneName"])
            #if all_args["1Ex"]:
            #    print "exon number : {0}".format(all_args["exon"])
            #    self.exon_input = str(all_args["exon"])
            #else:
            #    print "exon : ALL"
            #    self.exon_input = 0

        #print "done"
        #print "checking inputs"
        #check files input
        for a in (all_args["bamdir"], all_args["samtools"], all_args["resdir"]):
            if not self.check_is_dir(a):
                return
        if not self.check_is_file(all_args["ref_hgtable"]):
            return


        #==========================================================================
        #execute COAT ANALYSIS
        #==========================================================================

        mypath = os.path.realpath(__file__).split("Interface")[0]
        ##PEG:trouver le chemin complet du script execute
        ##PEG:le split sert a retrouver le nom dun autre script :p

        cmd = "python " + mypath + "/Coverage/coverageAnalysis.py"
        if all_args["geneName"]:
            #cmd += " --geneName {0}".format(all_args["geneName"])
            #cmd += " --exon {0}".format(self.exon_input)
            cmd += " --geneName {0}".format(all_args["geneName"])
            cmd += " --exon 0"
        else:
            cmd += " --position {0}".format(all_args["coordinate"])
        cmd += " --output {0}".format(all_args["resdir"])
        cmd += " --refPath {0}".format(all_args["ref_hgtable"])
        cmd += " --samtoolsPath {0}".format(all_args["samtools"])
        cmd += " --bamsPath {0}".format(all_args["bamdir"])
        cmd += " --subject {0}".format(all_args["subjects"])
        cmd += " --threshold {0}".format(all_args["covT"])
        cmd += " --mapQuality {0}".format(all_args["mapQT"])
        #cmd += " --htmlPage {0}".format(all_args["analysis"])
        #cmd += " --tableOutput {0}".format(all_args["analysis"])
        if all_args["cds_only"]:
            cmd += " --only_cds_regions"
        if all_args["utr"]:
            #cmd += " --only_cds_regions"
            cmd += " --add_utr_regions"
            #print "",
        if all_args["intron"]:
            cmd += " --add_intron_regions"
        if all_args["ucscF"]:
            cmd += " --track_no_cover_UCSC_output"
        if all_args["covF"]:
            cmd += " --cover_output"

        print cmd
        p1 = subprocess.Popen(cmd, shell=True, cwd="./",stderr=subprocess.PIPE)
        p1.wait()
        ph_out, ph_err = p1.communicate()
        #print ph_out
        #print "reported error"
        print ph_err
        #print p1.returncode
        print "CoAT end of program"
        return


    #==========================================================================
    #functions to check files input
    #==========================================================================
    def check_is_file(self, testFile):
        if os.path.isfile(testFile):
            return 1
        else:
            print "WARNING : path {0} is not a file".format(testFile)
            return None

    def check_is_dir(self, testDir):
        if os.path.isdir(testDir):
            return 1
        else:
            print "WARNING : Results path {0} is not a directory".format(testDir)
            return None

    def check_is_bamFile(self, bamFile):
        patternBamFile=re.compile("^.*\.bam$")
        if patternBamFile.match(bamFile):
            return 1
        else:
            return None




# -*- coding: utf-8 -*-
import os
import re
import sys
import subprocess


class Coatwire():


    def __init__(self, all_args):



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
            self.exon_input = 0

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
        cmd = "python " + mypath + "coverageAnalysis.py"
        cmd += " --output {0}".format(all_args["resdir"])
        if all_args["geneName"]:
            cmd += " --geneName {0}".format(all_args["geneName"])
        else:
            cmd += " --position {0}".format(all_args["coordinate"])
        cmd += " --cds_regions"
        if all_args["utr"]:
            cmd += " --add_utr_regions"
        if all_args["intron"]:
            cmd += " --add_intron_regions"
        cmd += " --bamsPath {0}".format(all_args["bamdir"])
        cmd += " --subject_list {0}".format(all_args["subjects"])
        cmd += " --coverage_threshold {0}".format(all_args["covT"])
        cmd += " --mapQuality_threshold {0}".format(all_args["mapQT"])
        if all_args["uncov"]:
            cmd += " --cover_output"
        if all_args["ucsc"]:
            cmd += " --track_no_cover_UCSC_output"
        cmd += " --refPath {0}".format(all_args["ref_hgtable"])
        cmd += " --samtoolsPath {0}".format(all_args["samtools"])



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




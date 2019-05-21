#================================================================================
#NOTICE
#================================================================================

'''


'''

#================================================================================
#MODULES
#================================================================================

import re
import sys
import subprocess
import argparse
import os.path
import getpass

#================================================================================
#CLASS
#================================================================================

class Subject:
    def __init__(self, name):
        self.name = name
        self.noCover = None
    def breadth_append(self, breadth):
        self.breadth = breadth
    def no_cover_file_append(self, noCover):
        self.noCover = noCover
    def depth_at_each_pos_file_append(self, depth_at_each_pos_outputFile):
        self.depth_at_each_pos = depth_at_each_pos_outputFile
    def plot_depth_append(self, plotDepth):
        self.plotDepth = plotDepth


class Region:
    def __init__(self,chr,start,end):
        self.chr = chr
        self.start = start
        self.end = end
        self.txNcExIn = {}
        self.dicOfSubject = {}
        self.utrStart = 0
        self.utrEnd = 0
    def chr_append(self, chr):
        self.chr = chr
    def start_append(self, start):
        self.start = start
    def end_append(self, end):
        self.end = end
    def gene_append(self, gene):
        self.gene = gene
    def txNcExIn_append(self, txNc, exIn):
        self.txNcExIn[txNc] = exIn
    def dicOfSubject_append(self,name):
        self.dicOfSubject[str(name)] = Subject(name)
    def utr_append(self, utrStart,utrEnd):
        self.utrStart = utrStart
        self.utrEnd = utrEnd



#================================================================================
#FUNCTIONS
#================================================================================

def remove_tmp_file(tmpFileName):
    '''
    remove the given temporary file with bash command rm
    '''
    command = "rm {0}".format(tmpFileName)
    subprocess.call(command, shell= True)
    return


def min_region(listOfRegions,what):
    min = 99999999999
    if what == "start":
        for region in listOfRegions:
            if region.start < min:
                min = region.start
    elif what == "end":
        for region in listOfRegions:
            if region.end < min:
                min = region.end
    else:
        print "error min_region"
    return min


def max_region(listOfRegions,what):
    max = 0
    if what == "start":
        for region in listOfRegions:
            if region.start > max:
                max = region.start
    elif what == "end":
        for region in listOfRegions:
            if region.end > max:
                max = region.end
    else:
        print "error min_region"
    return max


def convert_position_into_listOfRegions(position, ref_hgtable):
    '''
    from the position string CHR:FROM-TO or CHR:POS given in argument
    return a proper python list [CHR, FROM, TO] or [CHR, POS, POS+1]
    interrupt the program if the position string is no conform
    '''
    listOfRegions = []
    pattern1=re.compile("^chr.*[0-9]+-[0-9]+$")
    pattern2=re.compile("^chr.*[0-9]+$")
    if pattern1.match(position):
        posSplit = re.split(":|-", position)
        tmpChr = posSplit[0]
        tmpStart = int(posSplit[1])
        tmpEnd = int(posSplit[2])
    elif pattern2.match(position):
        posSplit = position.split(":")
        tmpChr = posSplit[0]
        tmpStart = int(posSplit[1])
        tmpEnd = tmpStart+1
    else:
        print "WARNING position format CHR:START-END or CHR:POSITION expected"
        sys.exit()
    #get features
    tmp_grep_chr = "tmp_grep_chr"
    command = "grep {0} {1} > {2}".format(tmpChr, ref_hgtable, tmp_grep_chr)
    subprocess.call(command, shell = True)
    with open(tmp_grep_chr, 'r') as ref_hg:
        in_tx = 0
        for ligne in ref_hg.readlines():
            splitLigne = ligne.split()
            txStart = int(splitLigne[4])
            txEnd = int(splitLigne[5])
            if(tmpEnd >= txStart and tmpStart <= txEnd):
                in_tx=1
                geneName = splitLigne[0]
                txName = splitLigne[1]
                exonAllStart = splitLigne[9].split(",")[:-1]
                exonAllEnd = splitLigne[10].split(",")[:-1]

                cdsStart = int(splitLigne[6])
                cdsEnd = int(splitLigne[7])
                txStrand = splitLigne[3]
                utr5Start = txStart
                utr5End = cdsStart-1
                utr3Start = cdsEnd+1
                utr3End = txEnd
                if txStrand != '-':
                    i=1
                else:
                    i=len(exonAllStart)
                if tmpEnd >= utr5Start and tmpStart <= utr5End:
                    #utr 5'
                    if txStrand != '-':
                        exIn = "utr_5"
                    else:
                        exIn = "utr_3"
                    if(utr5Start < tmpStart):
                        utr5Start = tmpStart
                    if(utr5End > tmpEnd):
                        utr5End = tmpEnd
                    region = Region(tmpChr, utr5Start, utr5End)
                    region.gene_append(geneName)
                    region.txNcExIn_append(txName, exIn)
                    listOfRegions.append(region)
                for s, e in zip(exonAllStart, exonAllEnd):
                    exonStart = int(s)
                    exonEnd = int(e)
                    #est dans exon
                    if(tmpEnd >= exonStart and tmpStart <= exonEnd):
                        utrStart = 0
                        utrEnd = 0
                        if (exonStart < cdsStart and exonEnd < cdsStart) or (exonStart > cdsEnd and exonEnd > cdsEnd):
                            exIn = "UTR"
                        elif exonStart < cdsStart:
                            exIn = "UTR"
                            utrStart = cdsStart
                            utrEnd = exonEnd
                        elif exonEnd > cdsEnd:
                            exIn = "UTR"
                            utrStart = exonStart
                            utrEnd = cdsEnd
                        else:
                            exIn = i
                        if(exonStart < tmpStart):
                            exonStart = tmpStart
                        if(exonEnd > tmpEnd):
                            exonEnd = tmpEnd
                        region = Region(tmpChr, exonStart, exonEnd)
                        region.gene_append(geneName)
                        region.txNcExIn_append(txName, exIn)
                        region.utr_append(utrStart,utrEnd)
                        listOfRegions.append(region)
                    #est dans intron
                    intronStart = exonEnd+1
                    if i < len(exonAllStart):
                        intronEnd = int(exonAllStart[i])-1
                        if (tmpEnd >= intronStart and tmpStart <= intronEnd):
                            if(intronStart < tmpStart):
                                intronStart = tmpStart
                            if(intronEnd > tmpEnd):
                                intronEnd = tmpEnd
                            exIn = "intron_{0}".format(i)
                            region = Region(tmpChr, intronStart, intronEnd)
                            region.gene_append(geneName)
                            region.txNcExIn_append(txName, exIn)
                            listOfRegions.append(region)
                    if txStrand != '-':
                        i+=1
                    else:
                        i-=1
                if tmpEnd >= utr3Start and tmpStart <= utr3End:
                    #utr 3'
                    if txStrand != '-':
                        exIn = "utr_3"
                    else:
                        exIn = "utr_5"
                    if(utr3Start < tmpStart):
                        utr3Start = tmpStart
                    if(utr3End > tmpEnd):
                        utr3End = tmpEnd
                    region = Region(tmpChr, utr3Start, utr3End)
                    region.gene_append(geneName)
                    region.txNcExIn_append(txName, exIn)
                    listOfRegions.append(region)
        NCListOfRegions = []
        geneName = "intergenic"
        if in_tx == 0:
            NCStart = tmpStart
            NCEnd = tmpEnd
            region = Region(tmpChr, NCStart, NCEnd)
            region.gene_append(geneName)
            region.txNcExIn_append("nc", "nc")
            NCListOfRegions.append(region)
        else:
            NCEnd = max_region(listOfRegions,"end")
            NCStart = min_region(listOfRegions,"start")
            if NCStart > tmpStart:
                region = Region(tmpChr, tmpStart, NCStart)
                region.gene_append(geneName)
                region.txNcExIn_append("nc", "nc")
                NCListOfRegions.append(region)
            for region in listOfRegions:
                NCListOfRegions.append(region)
            if NCEnd < tmpEnd:
                region = Region(tmpChr, NCEnd, tmpEnd)
                region.gene_append(geneName)
                region.txNcExIn_append("nc", "nc")
                NCListOfRegions.append(region)
    ref_hg.close()
    return NCListOfRegions


def convert_gene_into_region(geneName, ref_hgtable, cdsMode):
    tmp_grep_gen = "tmp_grep_gen"
    command = """grep "{0}\t" {1} > {2}""".format(geneName, ref_hgtable, tmp_grep_gen)
    subprocess.call(command, shell = True)
    listOfRegions = []
    with open(tmp_grep_gen, 'r') as ref_hg:
        for ligne in ref_hg.readlines():
            splitLigne = ligne.split()
            txChr = splitLigne[2]
            txName = splitLigne[1]
            txGene = splitLigne[0]
            txStart = int(splitLigne[4])
            txEnd = int(splitLigne[5])
            txStrand = splitLigne[3]


            exonAllStart = splitLigne[9].split(",")[:-1]
            exonAllEnd = splitLigne[10].split(",")[:-1]
            cdsStart = int(splitLigne[6])
            cdsEnd = int(splitLigne[7])

            if txStrand != '-':
                i=1
                first_utr=5
                last_utr=3
            else:
                i=len(exonAllStart)
                first_utr=5
                last_utr=3

            #premier intron ou region UTR
            exonStart = int(exonAllStart[0])
            if cdsStart < exonStart:
                region = Region(txChr, cdsStart, exonStart-1)
                region.gene_append(txGene)
                exIn = "intron:first"
                region.txNcExIn_append(txName, exIn)
                listOfRegions.append(region)
            for s, e in zip(exonAllStart, exonAllEnd):
                exonStart = int(s)
                exonEnd = int(e)
                if (exonStart < cdsStart and exonEnd < cdsStart) or (exonStart > cdsEnd and exonEnd > cdsEnd):
                    if cdsMode:
                        print "",
                    else:
                        if (exonStart < cdsStart):
                            exIn = "UTR{0}".format(last_utr)
                        else:
                            exIn = "UTR{0}".format(first_utr)
                        region = Region(txChr, exonStart,exonEnd)
                        region.gene_append(txGene)
                        region.txNcExIn_append(txName, exIn)
                        region.utr_append(exonStart,exonEnd)
                        listOfRegions.append(region)
                elif exonStart < cdsStart or exonEnd > cdsEnd:
                    if exonStart < cdsStart:
                        utrStart = exonStart
                        utrEnd = cdsStart
                    else:
                        utrStart = cdsEnd
                        utrEnd = exonEnd
                    if cdsMode:
                        if exonStart < cdsStart:
                            exonStart = cdsStart
                        else:
                            exonEnd = cdsEnd
                        exIn = i
                    else:
                        print "",
                        if (exonStart < cdsStart):
                            exIn = "UTR{0}".format(last_utr)#partly
                        else:
                            exIn = "UTR{0}".format(first_utr)#partly
                    region = Region(txChr, exonStart,exonEnd)
                    region.gene_append(txGene)
                    region.txNcExIn_append(txName, exIn)
                    region.utr_append(utrStart,utrEnd)
                    listOfRegions.append(region)
                else:
                    exIn = i
                    region = Region(txChr, exonStart,exonEnd)
                    region.gene_append(txGene)
                    region.txNcExIn_append(txName, exIn)
                    listOfRegions.append(region)
                if txStrand != '-':
                    i+=1
                else:
                    i-=1
            #dernier intron ou region UTR
            exonEnd = int(exonAllEnd[-1])
            if cdsEnd > exonEnd:
                region = Region(txChr, cdsStart, exonStart-1)
                region.gene_append(txGene)
                exIn = "intron_last".format(len(exonAllStart))
                region.txNcExIn_append(txName, exIn)
                listOfRegions.append(region)
    ref_hg.close()
    remove_tmp_file(tmp_grep_gen)
    return listOfRegions

def add_intron_to_listOfRegions(listOfRegions):
    intronListOfRegions = []
    test_utr = listOfRegions[0].txNcExIn.values()[0]
    if test_utr != "utr_3" and test_utr != "utr_5":
        test_utr = None
        base_j=1
    else:
        base_j=0
        test_utr = 1
    j = base_j
    i = 0
    prec_tx = listOfRegions[0].txNcExIn.keys()[0]
    for exon in listOfRegions[1:]:
        tx = exon.txNcExIn.keys()[0]
        ex_numb = exon.txNcExIn[tx]
        if tx != prec_tx:
            i+=1
            j = base_j
            prec_tx = tx
        else:
            exon_prec = listOfRegions[i]
            inChr = exon.chr
            inStart = exon_prec.end+1
            inEnd = exon.start-1
            inGene = exon.gene
            intron = Region(inChr, inStart, inEnd)
            intron.gene_append(inGene)
            intron.txNcExIn_append(tx, "intron_{0}".format(ex_numb))
            j+=1
            i+=1
            intronListOfRegions.append(exon_prec)
            if test_utr is None:
                intronListOfRegions.append(intron)
                intronListOfRegions.append(exon)
            else:
                if exon.txNcExIn[tx] != "utr_3" and exon.txNcExIn[tx] != "utr_5":
                    if exon_prec.txNcExIn[prec_tx] != "utr_3" and exon_prec.txNcExIn[prec_tx] != "utr_5":
                        intronListOfRegions.append(intron)
                else:
                    intronListOfRegions.append(exon)
    intronListOfRegions.append(listOfRegions[-1])
    return intronListOfRegions


def add_utr_to_listOfRegions(listOfRegions, ref_hgtable):
    tmp_grep_gen = "tmp_grep_gen"
    command = """grep "{0}\t" {1} > {2}""".format(geneName, ref_hgtable, tmp_grep_gen)
    subprocess.call(command, shell = True)
    utrListOfRegions = []
    with open(tmp_grep_gen, 'r') as ref_hg:
        for ligne in ref_hg.readlines():
            splitLigne = ligne.split()
            txChr = splitLigne[2]
            txName = splitLigne[1]
            txGene = splitLigne[0]
            txStart = int(splitLigne[4])
            txEnd = int(splitLigne[5])
            cdsStart = int(splitLigne[6])
            cdsEnd = int(splitLigne[7])
            txStrand = splitLigne[3]
            if txStrand != '-':
                utr5Start = txStart
                utr5End = cdsStart-1
                utr3Start = cdsEnd+1
                utr3End = txEnd
                utr3 = Region(txChr, utr3Start, utr3End)
                utr3.gene_append(txGene)
                utr3.txNcExIn_append(txName, "utr_3")
                utr5 = Region(txChr, utr5Start, utr5End)
                utr5.gene_append(txGene)
                utr5.txNcExIn_append(txName, "utr_5")
                utrListOfRegions.append(utr5)
                for exon in listOfRegions:
                    if exon.txNcExIn.keys()[0] == txName:
                        utrListOfRegions.append(exon)
                utrListOfRegions.append(utr3)
            else:
                utr5Start = cdsEnd+1
                utr5End = txEnd
                utr3Start = txStart
                utr3End = cdsStart-1
                utr3 = Region(txChr, utr3Start, utr3End)
                utr3.gene_append(txGene)
                utr3.txNcExIn_append(txName, "utr_3")
                utr5 = Region(txChr, utr5Start, utr5End)
                utr5.gene_append(txGene)
                utr5.txNcExIn_append(txName, "utr_5")
                utrListOfRegions.append(utr3)
                for exon in listOfRegions:
                    if exon.txNcExIn.keys()[0] == txName:
                        utrListOfRegions.append(exon)
                utrListOfRegions.append(utr5)
    ref_hg.close()
    return utrListOfRegions


def uniq_listOfRegions(listOfRegions):
    uniqListOfRegions = []
    for reg1 in listOfRegions:
        test = 0
        for reg2 in uniqListOfRegions:
            if reg1.start == reg2.start and reg1.end == reg2.end:
                test = 1
                for key,val in reg1.txNcExIn.items():
                    reg2.txNcExIn_append(key,val )
                break
            else:
                test = 0
        if test != 1:
            uniqListOfRegions.append(reg1)
    return(uniqListOfRegions)


def print_region(listOfRegions):
    for region in listOfRegions:
        print region.chr, region.start, region.end, region.gene,
        print "|",
        for key,val in region.txNcExIn.items():
            print key,val,
        print "|",
        for nameSubject, subject in region.dicOfSubject.items():
            print nameSubject, subject.breadth
        print ""
    return


#------------------------------------------------------------------------------

def execute_samtools_depth(samtools, bamFile, region, tmpSamDepthFile, mapQualThreshold):
    '''
    get samtools path and execute samtools depth on positions given by listOfPos and bamFile
    The samtools depth output is stocked in temporary file
    '''
    cmdBams = bamFile
    cmdRegion = "{0}:{1}-{2}".format(region.chr, region.start, region.end)
    command = "{0}samtools depth -Q {1} -r {2} {3} > {4} 2> /dev/null".format(samtools,mapQualThreshold ,cmdRegion, cmdBams, tmpSamDepthFile)
    #print command
    subprocess.call(command, shell = True)
    return


def no_cover_from_samtools_depth(region, subject, tmpSamDepthFile, resultsPath):
    no_cover_outputFile = resultsPath+"/no_cover_"+subject+"_"+region.gene+"_"+region.txNcExIn.keys()[0]+"_"+str(region.txNcExIn[region.txNcExIn.keys()[0]])+".cov-res"
    #print no_cover_outputFile
    region.dicOfSubject[subject].no_cover_file_append(no_cover_outputFile)
    with open(tmpSamDepthFile, 'r') as depthFile:
        with open(no_cover_outputFile, 'w') as outFile:
            header = "chr\tstart\tend\tgene\ttranscript\texon\n"
            outFile.write(header)
            read = depthFile.readlines()
            lengthRead = len(read)
            pos = region.start
            samPos = pos
            no_coverStart = 0
            no_coverEnd = 0
            i=0
            while pos <= region.end and no_coverEnd == 0:
                if i >= lengthRead:
                    if pos != no_coverEnd+1:
                        no_coverStart = samPos+1
                    no_coverEnd = region.end
                    break
                samPos = int(read[i].split()[1])
                depthPos = int(read[i].split()[2])
                testThresold = 0
                if depthPos <= thresholdCoverage:
                    testThresold = 1
                if samPos != pos:
                    if pos != no_coverEnd+1:
                        no_coverStart = pos
                    no_coverEnd = samPos
                    pos = samPos
                elif testThresold:
                    if pos != no_coverEnd+1:
                        no_coverStart = pos
                    no_coverEnd = samPos
                    i+=1
                    pos+=1
                else:
                    i+=1
                    pos+=1
            while pos <= region.end:
                if i >= lengthRead:
                    if pos != no_coverEnd+1:
                        #for tx in region.txNcExIn:
                        outFile.write("{0}\t".format(region.chr))
                        outFile.write("{0}\t".format(no_coverStart))
                        outFile.write("{0}\t".format(no_coverEnd))
                        outFile.write("{0}\t".format(region.gene))
                        outFile.write("{0}\t".format(region.txNcExIn.keys()[0]))
                        outFile.write("{0}\n".format(region.txNcExIn.values()[0]))
                        no_coverStart = samPos+1
                    no_coverEnd = region.end
                    break
                samPos = int(read[i].split()[1])
                depthPos = int(read[i].split()[2])
                testThresold = 0
                if depthPos <= thresholdCoverage:
                    testThresold = 1
                if samPos != pos:
                    if pos != no_coverEnd+1:
                        #for tx in region.txNcExIn:
                        outFile.write("{0}\t".format(region.chr))
                        outFile.write("{0}\t".format(no_coverStart))
                        outFile.write("{0}\t".format(no_coverEnd))
                        outFile.write("{0}\t".format(region.gene))
                        outFile.write("{0}\t".format(region.txNcExIn.keys()[0]))
                        outFile.write("{0}\n".format(region.txNcExIn.values()[0]))
                        no_coverStart = pos
                    no_coverEnd = samPos
                    pos = samPos
                elif testThresold:
                    if pos != no_coverEnd+1:
                        #for tx in region.txNcExIn:
                        outFile.write("{0}\t".format(region.chr))
                        outFile.write("{0}\t".format(no_coverStart))
                        outFile.write("{0}\t".format(no_coverEnd))
                        outFile.write("{0}\t".format(region.gene))
                        outFile.write("{0}\t".format(region.txNcExIn.keys()[0]))
                        outFile.write("{0}\n".format(region.txNcExIn.values()[0]))
                        no_coverStart = pos
                    no_coverEnd = samPos
                    i+=1
                    pos+=1
                else:
                    i+=1
                    pos+=1
            #for tx in region.txNcExIn:
            outFile.write("{0}\t".format(region.chr))
            outFile.write("{0}\t".format(no_coverStart))
            outFile.write("{0}\t".format(no_coverEnd))
            outFile.write("{0}\t".format(region.gene))
            outFile.write("{0}\t".format(region.txNcExIn.keys()[0]))
            outFile.write("{0}\n".format(region.txNcExIn.values()[0]))
        outFile.close()
    depthFile.close()
    subprocess.call("uniq {0} > tmp ; mv tmp {0}".format(no_cover_outputFile), shell=True)

    tmpFileName = resultsPath+"/no_cover_tmp"
    with open(no_cover_outputFile, 'r') as no_coverFile:
        with open(tmpFileName, 'w') as tmpFile:
            read = no_coverFile.readlines()
            header = read[0]
            tmpFile.write(header)
            lignes = read[1:]
            lenLignes = len(lignes)
            if lenLignes > 1:
                i = 1
                while i < lenLignes:
                    ligne1 = lignes[i-1].split()
                    ligne2 = lignes[i].split()
                    if int(ligne1[2]) == int(ligne2[1]):
                        tmpFile.write(
                            ligne1[0]+"\t"+
                            ligne1[1]+"\t"+
                            ligne2[2]+"\t"+
                            ligne1[3]+"\t"+
                            ligne1[4]+"\t"+
                            ligne1[5]+"\n"
                        )
                        i+=2
                    else:
                        tmpFile.write(lignes[i-1])
                        i+=1
            else:
                for ligne in lignes:
                    tmpFile.write(ligne)
        tmpFile.close()
    no_coverFile.close()
    subprocess.call("mv {0} {1}".format(tmpFileName, no_cover_outputFile),shell=True)
    return


def depth_at_each_pos_from_samtools_depth(tmpSamDepthFile, subject, region, resultsPath):
    depth_at_each_pos_outputFile = resultsPath+"/depth_at_each_pos_"+subject+"_"+region.gene+"_"+region.txNcExIn.keys()[0]+"_"+str(region.txNcExIn[region.txNcExIn.keys()[0]])+".cov-res"
    #print depth_at_each_pos_outputFile
    region.dicOfSubject[subject].depth_at_each_pos_file_append(depth_at_each_pos_outputFile)
    with open(tmpSamDepthFile, 'r') as depthFile:
        with open(depth_at_each_pos_outputFile, 'w') as outFile:
            read = depthFile.readlines()
            lengthRead = len(read)
            if lengthRead < 1:
                for zeropos in xrange(region.start, region.end+1):
                    outFile.write("{0}\t".format(region.chr))
                    outFile.write("{0}\t".format(zeropos))
                    outFile.write("{0}\n".format(0))
            else:
                i=0
                pos = region.start
                samPos = pos
                while pos <= region.end:
                    if i >= lengthRead:
                        for supPos in xrange(samPos, region.end):
                            outFile.write("{0}\t".format(region.chr))
                            outFile.write("{0}\t".format(supPos))
                            outFile.write("{0}\n".format(0))
                        break
                    samPos = int(read[i].split()[1])
                    if samPos != pos:
                        for supPos in xrange(pos, samPos):
                            outFile.write("{0}\t".format(region.chr))
                            outFile.write("{0}\t".format(supPos))
                            outFile.write("{0}\n".format(0))
                        pos = samPos
                    else:
                        depth = read[i].split()[2]
                        outFile.write("{0}\t".format(region.chr))
                        outFile.write("{0}\t".format(pos))
                        outFile.write("{0}\n".format(depth))
                        i+=1
                        pos+=1
        outFile.close()
    depthFile.close()
    return



def breadth_from_samtools_depth(listOfRegions, resultsPath, thresholdCoverage, samtools, subjectBams, mapQualThreshold):
    tmpSamDepthFile = "{0}/tmp_sam_depth".format(resultsPath)
    for region in listOfRegions:
        for s in subjectBams:
            execute_samtools_depth(samtools, subjectBams[s], region, tmpSamDepthFile, mapQualThreshold)
            with open(tmpSamDepthFile, 'r') as depthFile:
                read = depthFile.readlines()
                lengthRead = len(read)
                nbNoCoverPos = 0
                i=0
                pos = region.start
                samPos = pos
                while pos <= region.end:
                    if i >= lengthRead:
                        nbNoCoverPos+=(region.end-samPos+1)
                        break
                    samPos = int(read[i].split()[1])
                    depthPos = int(read[i].split()[2])
                    testThresold = 0
                    if depthPos <= thresholdCoverage:
                        testThresold = 1
                    if samPos != pos:
                        nbNoCoverPos+=(samPos-pos)
                        pos = samPos
                    elif testThresold:
                        nbNoCoverPos+=1
                        i+=1
                        pos+=1
                    else:
                        i+=1
                        pos+=1
                size = region.end-region.start+1
                if size < 1:
                    print size
                    print region.end
                    print region.start
                breadth = float(size-nbNoCoverPos)/float(size)
                breadth = round(breadth, 2)
                region.dicOfSubject_append(s)
                region.dicOfSubject[s].breadth_append(breadth)
                #no_cover
            depthFile.close()
            if breadth < 1:
                no_cover_from_samtools_depth(region, s, tmpSamDepthFile, resultsPath)
                depth_at_each_pos_from_samtools_depth(tmpSamDepthFile, s, region, resultsPath)
                #execute_plot_depth(region, thresholdCoverage, s, resultsPath)
            os.remove(tmpSamDepthFile)

    return


#------------------------------------------------------------------------------

def get_bamFile_from_subject_name(subjectName, bamsPath):
    command = "find {0} -name {1}*bam".format(bamsPath, subjectName)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=None)
    output = process.communicate()
    bamFile = str(output[0])[:-1]
    if output[1] is not None:
        print "WARNING : {0} is not in the subjects list".format(subjectName)
        sys.exit()
    return bamFile


def exon_from_listOfRegions(listOfRegions, exon):
    exonlistOfRegions = []
    for reg in listOfRegions:
        for key,val in reg.txNcExIn.items():
            if val == exon or val == (str(exon)+"u") or val == (str(exon)+"U"):
                exonlistOfRegions.append(reg)
    return exonlistOfRegions


def parse_exon_args(args_exon):
    if args_exon is None:
        return None
    try:
        exon = int(args_exon)
    except ValueError:
        print "WARNING : exon is not a number"
        sys.exit()
    if exon < 0:
        print "WARNING : exon is not a positive number"
        sys.exit()
    return exon


def check_is_file(testFile):
    if os.path.isfile(testFile):
        return 1
    else:
        print "WARNING : {0} is not a file".format(testFile)
        return None


def check_is_dir(testDir):
    if os.path.isdir(testDir):
        return 1
    else:
        print "WARNING : {0} is not a directory".format(testDir)
        return None


def check_is_bamFile(bamFile):
    patternBamFile=re.compile("^.*\.bam$")
    if patternBamFile.match(bamFile):
        return 1
    else:
        return None


#================================================================================
#ARGUMENTS
#================================================================================

parser = argparse.ArgumentParser(description='depth coverage')
parser.add_argument("-o","--output", type=str)
#select region
parser.add_argument("-p","--position",type=str)
parser.add_argument("-gene","--geneName",type=str)
parser.add_argument("-cds","--cds_regions", action='store_true')
parser.add_argument("-add_utr","--add_utr_regions", action='store_true')
parser.add_argument("-add_intron","--add_intron_regions", action='store_true')
#select subject
parser.add_argument("-bams","--bamsPath",type=str)
parser.add_argument("-subject","--subject_list",type=str)
#select coverage thresholds
parser.add_argument("-cov","--coverage_threshold", type=int, default=5)
parser.add_argument("-mapqual","--mapQuality_threshold", type=int, default=20)
#generate additional file(s)
parser.add_argument("-covout", "--cover_output", action='store_true')
parser.add_argument("-track", "--track_no_cover_UCSC_output", action='store_true')
#external
parser.add_argument("-ref","--refPath",type=str)
parser.add_argument("-samtools","--samtoolsPath",type=str)



#================================================================================
#MAIN
#================================================================================

args = parser.parse_args()
resultsPath = args.output
position = args.position
geneName = args.geneName

ref_hgtable = args.refPath
samtools = args.samtoolsPath

bamsPath = args.bamsPath

subject = args.subject_list
thresholdCoverage = args.coverage_threshold
utrAdd = args.add_utr_regions
intronAdd = args.add_intron_regions
cdsMode = args.cds_regions
mapQualThreshold = args.mapQuality_threshold
coverOutputMode = args.cover_output
trackNoCoverUCSC = args.track_no_cover_UCSC_output


print "Checking arguments..."
#--------------------------------------------------------------------------------
#CHECK ARGS
#--------------------------------------------------------------------------------

#check genome reference file
if check_is_file(ref_hgtable) is None:
    sys.exit()
#check samtools pathway
if check_is_dir(samtools) is None:
    sys.exit()
#check output pathway
if check_is_dir(resultsPath) is None:
    sys.exit()
#check BAMS pathway
if check_is_dir(bamsPath) is None:
    sys.exit()
if subject is not None:
    subjectBams = {}
    #removedSubject = []
    listOfSubject = []
    for s in subject.split(","):
        bamFile = get_bamFile_from_subject_name(s, bamsPath)
        if check_is_bamFile(bamFile) is not None:
            subjectBams[s]=bamFile
            listOfSubject.append(s)
        else:
            print "WARNING : No .BAM file found for the {0} subject in {1}".format(s,bamsPath)
            print "However the {0} subject has been remove from the list of subjects".format(s)
            #removedSubject.append(s)
else:
    print "WARNING : no subject argument"
    sys.exit()
#print subjectBams

print "Done"
print "Parsing reference..."

#--------------------------------------------------------------------------------
#PARSE QUERY GENOME POSITIONS
#--------------------------------------------------------------------------------
typeOfQuery = ""
if position:
    #region position
    typeOfQuery = "region {0}".format(position)
    listOfRegions = convert_position_into_listOfRegions(position, ref_hgtable)
elif geneName:
        typeOfQuery = "all CDS ONLY exonic regions in gene {0}".format(geneName)
        exon = None
        listOfRegions = convert_gene_into_region(geneName, ref_hgtable, cdsMode)
        if utrAdd:
            typeOfQuery = typeOfQuery + " and UTR regions"
            listOfRegions = add_utr_to_listOfRegions(listOfRegions, ref_hgtable)
        if intronAdd:
            typeOfQuery = typeOfQuery + " and intronic regions"
            listOfRegions = add_intron_to_listOfRegions(listOfRegions)
else:
    print "WARNING : no position/gene arguments"
    sys.exit()

listOfRegions = uniq_listOfRegions(listOfRegions)
#print_region(listOfRegions)

print "Done"
print "Coverage analysis..."

#--------------------------------------------------------------------------------
#COVERAGE DEPTH ANALYSIS
#--------------------------------------------------------------------------------


breadth_from_samtools_depth(listOfRegions, resultsPath, thresholdCoverage, samtools, subjectBams, mapQualThreshold)
#print_region(listOfRegions)

print "Done"
print "Generate results..."

#--------------------------------------------------------------------------------
#GENERATE TABLE RESULTS
#--------------------------------------------------------------------------------

tableOutput = str(resultsPath)+"/"+str(getpass.getuser())

if position:
    tableOutput += "_position_" + str(position)
else:
    tableOutput += "_gene_" + str(geneName)
if cdsMode:
    tableOutput += "_cds"
else:
    tableOutput += "_cds_add_utr"
if utrAdd:
    tableOutput += "_add_utr"
if intronAdd:
    tableOutput += "_add_intron"
tableOutput += "_cov_" + str(thresholdCoverage)
tableOutput += "_qual_" + str(mapQualThreshold)
if coverOutputMode:
    tableCoverOutput = tableOutput + "_covered.table"
tableOutput += "_uncovered.table"


with open(tableOutput,"w") as tableOutputFile:
    tableOutputFile.write("chrom\tuncovered_start\tuncovered_end\tsubject\tgene\ttranscript\texon_numb\tuncovered_length\n")
tableOutputFile.close()
listOfRegions.sort(key = lambda region : region.start, reverse = False)
for nameSubject in listOfSubject:
    for region in listOfRegions:
        subject = region.dicOfSubject[nameSubject]
        if subject.noCover is not None:
            region_no_cover = subject.noCover
            with open(region_no_cover, "r") as noCoverFile:
                #print "coucou"+nameSubject+subject.noCover
                read = noCoverFile.readlines()[1:]
                if len(read) > 0:
                    with open(tableOutput,"a") as tableOutputFile:
                        for ligne in read:
                            ligneSplit = ligne[:-1].split("\t")
                            chromosome = ligneSplit[0]
                            start = int(ligneSplit[1])
                            end = int(ligneSplit[2])
                            gene = ligneSplit[3]
                            tx = ligneSplit[4]
                            exon = ligneSplit[5]
                            if exon[-1] == "u":
                                #print start,end
                                #print region.utrStart,region.utrEnd
                                if end < region.utrStart:
                                    exon = exon[:-1]
                                elif start > region.utrEnd:
                                    exon = exon[:-1]
                                else:
                                    exon = exon
                            tableOutputFile.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\n".format(
                                chromosome,
                                start,
                                end,
                                nameSubject,
                                gene,
                                tx,
                                exon,
                                ((end-start)+1)
                            ))
                    tableOutputFile.close()
            noCoverFile.close()

subprocess.call("uniq {0} > tmp ; mv tmp {0}".format(tableOutput), shell=True)

#subprocess.call("rm {0}/*.pdf".format(resultsPath, htmlPage), shell=True)
print "Done"



if coverOutputMode:
    with open(tableCoverOutput,'w') as coverFile:
        coverFile.write("chrom\tcovered_start\tcovered_end\tsubject\tgene\ttranscript\texon_numb\tcovered_length\n")
        for nameSubject in listOfSubject:
            for region in listOfRegions:
                subject = region.dicOfSubject[nameSubject]
                if subject.noCover is not None:
                    region_no_cover = subject.noCover
                    with open(region_no_cover, "r") as noCoverFile:
                        read = noCoverFile.readlines()[1:]
                        lenRead = len(read)
                        if lenRead == 1:
                            ligne = read[0][:-1].split("\t")
                            chromosome = ligne[0]
                            gene = ligne[3]
                            tx = ligne[4]
                            exon = ligne[5]
                            if int(ligne[1]) > region.start:
                                start = region.start
                                end = ligne[1]
                                coverFile.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\n".format(
                                chromosome,
                                start,
                                end,
                                nameSubject,
                                gene,
                                tx,
                                exon,
                                ((int(end)-int(start))+1)
                                ))
                            if int(ligne[2]) < region.end:
                                start = ligne[2]
                                end = region.end
                                coverFile.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\n".format(
                                chromosome,
                                start,
                                end,
                                nameSubject,
                                gene,
                                tx,
                                exon,
                                ((int(end)-int(start))+1)
                                ))

                        if lenRead > 1:
                            for i in xrange(1,lenRead):
                                ligne1 = read[i-1][:-1].split("\t")
                                #print ligne1
                                ligne2 = read[i][:-1].split("\t")
                                chromosome = ligne1[0]
                                gene = ligne1[3]
                                tx = ligne1[4]
                                exon = ligne1[5]
                                #print exon
                                if int(ligne1[1]) > region.start:
                                    start = region.start
                                    end = ligne1[1]
                                    coverFile.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\n".format(
                                    chromosome,
                                    start,
                                    end,
                                    nameSubject,
                                    gene,
                                    tx,
                                    exon,
                                    ((int(end)-int(start))+1)
                                    ))
                                if int(ligne2[2]) < region.end:
                                    start = ligne2[2]
                                    end = region.end
                                    coverFile.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\n".format(
                                    chromosome,
                                    start,
                                    end,
                                    nameSubject,
                                    gene,
                                    tx,
                                    exon,
                                    ((int(end)-int(start))+1)
                                    ))
                                #par defaut
                                start = ligne1[2]
                                end = ligne2[1]
                                coverFile.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\n".format(
                                chromosome,
                                start,
                                end,
                                nameSubject,
                                gene,
                                tx,
                                exon,
                                ((int(end)-int(start))+1)
                                ))
                    noCoverFile.close()
                else:
                    for tx,ex in region.txNcExIn.items():
                        coverFile.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\n".format(
                        region.chr,
                        region.start,
                        region.end,
                        nameSubject,
                        region.gene,
                        tx,
                        ex,
                        ((int(region.end)-int(region.start))+1)
                        ))
    coverFile.close()

#subprocess.call("""(head -1 {0}; sed -n '2,$p' {0} | sort -k2 -k4) > tmp ; mv tmp {0}""".format(tableCoverOutput), shell=True)
print "Done"

if trackNoCoverUCSC:
    trackOutput = str(resultsPath)+"/"+str(getpass.getuser())
    if position:
        trackOutput += "_position_" + str(position)
    else:
        trackOutput += "_gene_" + str(geneName)
    if cdsMode:
        trackOutput += "_cds"
    else:
        trackOutput += "_cds_add_utr"
    #if utrAdd:
    #    trackOutput += "_add_utr"
    if intronAdd:
        trackOutput += "_add_intron"
    trackOutput += "_cov_" + str(thresholdCoverage)
    trackOutput += "_qual_" + str(mapQualThreshold)
    trackOutput += "_UCSC_track_uncovered.gff"
    with open(trackOutput,'w') as trackFile:
        with open(tableOutput,'r') as no_coverFile:
            read = no_coverFile.readlines()[1:]
            if len(read) > 0:
                infos = read[0][:-1].split()
                infos2 = read[-1].split()
                chromosome = infos[0]
                start = infos[1]
                end = infos2[2]
                gene = infos[4]
                trackFile.write(
                    "browser position {0}:{1}-{2}\n".format(
                        chromosome,
                        start,
                        end
                    )
                )
                trackFile.write("browser hide all \n")
                trackFile.write(
                    """track name=regulatory description="Uncovered regions in {0} (depth <= {1})" visibility=4 color=255,15,15\n""".format(gene,thresholdCoverage)
                )
                for ligne in read:
                    ligneSplit = ligne.split()
                    trackFile.write(
                        ligneSplit[0]+"\t"+
                        "ExAM"+"\t"+
                        "uncovered"+"\t"+
                        ligneSplit[1]+"\t"+
                        ligneSplit[2]+"\t"+
                        ".\t.\t.\t"+
                        ligneSplit[3]+"\n"
                    )
        no_coverFile.close()
    trackFile.close()



subprocess.call("rm -f {0}/*.cov-res".format(resultsPath), shell=True)
#================================================================================
#END
#================================================================================

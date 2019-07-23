<img src="https://github.com/Grelot/diabeteGenetics--COAT/blob/master/images/logo.png"  title="coat_logo">



[![EXAM SOURCEFORGE](https://sourceforge.net/sflogo.php?type=13&group_id=96355)](https://sourceforge.net/projects/exam-exome-analysis-and-mining/)

[![Project Status: Inactive – The project has reached a stable, usable state but is no longer being actively developed; support/maintenance will be provided as time allows.](https://www.repostatus.org/badges/latest/inactive.svg)](https://www.repostatus.org/#inactive) [![EXAM downloads](https://img.shields.io/sourceforge/dt/exam-exome-analysis-and-mining/..svg)](https://sourceforge.net/projects/exam-exome-analysis-and-mining/files/latest/download)


# CoverageAnalysisTool

Outputs a list of coding regions that are uncovered above a given threshold

# Overview

- COAT is a Python2 program developed in 2016 which aims to automatically find bad quality region of coding sequences in a set of individual exome sequencing data.

- It is a module integrated to the [EXome Analysis and Mining](https://sourceforge.net/projects/exam-exome-analysis-and-mining/).

- It includes a graphical interface.

- The output of this program is a spreadsheet with all the coding regions which are uncovered.
Supplementary annotation can be used for further analysis. Additional files can be
generated using `--cover_output` argument and/or `--track_no_cover_UCSC_output`.

# Input

## BAM files

BAM is a binary file format. SAM and BAM files contain the same information. These
files contain mapped reads sequence from Next Generation Sequencing.

# Installing COAT on LINUX

To use COAT, the following programs are necessary  :

* [python 2.6](https://www.python.org/download/releases/2.6/)
* [PyQt4](https://pypi.org/project/PyQt4/)
* [samtools 1.3](https://sourceforge.net/projects/samtools/files/samtools/1.3/)

The following files are necessary :

* BAM files folder
* reference sequence annotation file

## Programming language Python

Python (version 2.6.5 to version 2.7.8). To see which version of Python you have
installed, open a command prompt and run:

```
python --version
```

If you don’t have Python, type the following command to install python version 2.x:

```
sudo apt-get install python 2.6
```

## GUI toolkit PyQt4 

If you want to use COAT graphical interface, you will need to install the python module `PyQt4`

```
apt-cache search pyqt
sudo apt-get install python-qt4
```

## Samtools

To run COAT, you must have installed [samtools 1.3](https://sourceforge.net/projects/samtools/files/samtools/1.3/). If you have a previous version of samtools, COAT will not work, so download and install samtools 1.3. Unzip the downloaded file. Go into the newly created directory and compile the code by typing "make".

```
tar -xvjf samtools-1.3.tar.bz2
cd samtools-1.3/
make
```

## BAM

Store your BAM files into a dedicated folder. Prefix of BAM files name is used as subject identifier (see command-line argument `--subject_list`).

<img src="https://github.com/Grelot/diabeteGenetics--COAT/blob/master/images/bam_schema_folder.png"  title="bam_schema_folder">

Samtools folder must be specified (see command-line argument `--samtoolsPath`)
BAM files must be indexed. To generate Index of BAM files, use samtools line-commands:

```
samtools sort -T /tmp/aln.sorted -o aln.sorted.bam aln.bam
samtools index aln.sorted.bam
```

## Reference sequence annotation file

Reference annotated sequence is needed. This file contains gene	annotation of the genome reference you want to use. You can get file for h19 reference:
- http://hgdownload.cse.ucsc.edu/goldenPath/hg19/database/refFlat.txt.gz

# Command-line Arguments

This table summarizes the command-line arguments which are using by COAT. 

| complete flag argument | short flag |Default value | Summary |
| --- | --- | --- | --- |
| `--output` | `-o` | stdout | Output folder path. Will overwrite contents if file exists |
| `--position` | `-p` | NA | Interval positions in chromosome of the reference sequence FORMAT: _chr:start-end_ |
| `--geneName` | `-g` | NA | Select region of the gene. FORMAT: name of the gene according to reference |
| `--cds_regions` | `-cds` | TRUE | regions of exons which are not into UTR in the reference sequence |
| `--add_utr_regions` | `-add_utr` | FALSE | Add UTR to the selected region |
| `--add_intron_regions` | `-add_intron` | FALSE | Add intron regions to the selected region |
| `--bamsPath` | `-bams` | NA | BAM files folder |
| `--subject_list` | `-subject` | NA | Coma-separated list of prefix BAM files name(s) of selected subject in BAM files repertory |
| `--coverage_threshold` | `-cov` | 5 | The minimum coverage to be actually considered as _covered_ |
| `--mapQuality_threshold` | `-mapqual` | 20 | The minimum allowable mapping quality score to be counted for coverage |
| `--baseQuality_trehshold` | `-basequal` | 0 | The minimum allowable base quality score to be counted for coverage |
| `--cover_output` | `-covout` | FALSE | Output as a supplementary file the list of covered regions with annotation |
| `--track_no_cover_UCSC_output` | `-track` | FALSE | Output [UCSC Genome Brower custom track](https://genome.ucsc.edu/cgi-bin/hgGateway) which contains uncovered regions |
| `--refPath` | `-ref` | NA | Annotation file for reference _e.g._ hg19 |
| `--samtoolsPath` | `-samtools` | NA | Samtools 1.3 folder path |

# Example of command

```
python2 coverageAnalysis.py \
-gene GLIS3 \
-cds \
-add_utr \
-bams /storage/bams/ \
-subject family1_1,family1_3 \
-ref refFlat_hg19.txt \
-cov 15 \
-o coverage_check_results/
```

# Output

## List of uncovered/covered coding regions with annotation

| Chrom | Uncovered_start | Uncovered_end | subject | gene |transcript | Exon_numb | Uncovered_length |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Chr9 | 3937027 | 3937120 | Family1_1 | GLIS3 | NM_001042413 | 5 | 94 |
| Chr9 | 3937027 | 3937074 | Family1_3 | GLIS3 | NM_001042413 | 5 | 48 |

Each row is an uncovered region. 
- Chrom: chromosome.
- Uncovered_start: the reference start position of an uncovered region.
- Uncovered_end: the reference end position of an uncovered region.
- subject: the sequenced subject identifier.
- gene: name of the gene including the uncovered region.
- transcript: name of the transcript of the gene including the uncovered region.
- exon_numb: numb of the exon of the transcript of the gene including the uncovered region. This field can optionally mention UTR5’, UTR3’ and intron region.
- uncovered_length: number of nucleotides in the uncovered region.

## UCSC Genome browser custom track of uncovered region

<img src="https://github.com/Grelot/diabeteGenetics--COAT/blob/master/images/genome_browser_custom_track.png"  title="genome_browser_custom_track">

Visualising uncovered region on gene GLIS3 of the 2 subjects from family 1 with UCSC Genome Browser. Annotation from REFSEQ have been added. In red, uncovered region. 


# Interface

To run in graphical mode the program :
```
python2 Interface/coat_HCI.pyw
```

This command will display the following interface :

<img src="https://github.com/Grelot/diabeteGenetics--COAT/blob/master/images/coat_graphics.png"  title="coat_graphics">

______

## 1. Advanced settings, save settings and reset 
Click on Advanced settings to access advanced settings section.

* bam files folder: path of the folder in which your BAM files and BAM.bai files are stored.
* samtools folder: path of the folder in which samtools 1.3 is stored.
* Hg reference table file: path of the reference annotated sequence.
* Results folder: output folder path. Will overwrite contents if file exists. 

Save settings will save all your settings for the next time you will use COAT. Reset gives the default value for all settings.

## 2. Select subject 

Fill the fields with your coma-separated list of prefix BAM files name(s) of selected subject in BAM files folder.

## 3. Select region

Select the region to check by specify coordinates else or gene name. Coordinates refers to an interval positions in chromosome of the reference sequence (FORMAT: chr:start-end). By default, coverage check is running on CDS region. But you can add UTR and intron region by toggle the corresponding option.

## 4. Select coverage thresholds

3 thresholds are availables: 
- the minimum allowable coverage depth to be considered covered (default value = 5);
- the minimum allowable mapping quality score to be counted for coverage (default value = 20);
- the minimum allowable base quality score to be counted for coverage (default value = 0).

## 5. Generate additional files 

By default, output is a list of uncovered coding regions with annotation. You can add by toggle the corresponding option: a list of covered regions with annotation; an UCSC custom track which contains uncovered regions.

## 6. Launch and quit

When all your parameters are selected, click on launch coverage check to run COAT.







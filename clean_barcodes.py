#! /usr/bin/env python3

import sys, os

if len(sys.argv) != 4:
	sys.exit('---------------- clean_barcodes.py v. 0.2 - by Piotr Łukasik, 9 Feb 2024 ---------------\n\n'
	         'This script breaks up fasta files provided by ONTbarcoder based on results of BLAST searches against a custom database.\n'
	         'The script was designed to use as input a folder with de-multiplexed fasta files, representing noisy Nanopore COI sequences for different samples\n'
	         '(but it should also work with most other fasta files, for COI as otherwise, as long as you prepare the right database).'
	         'It also relies on a pre-prepared sequence database, where reads representing categories of interest have names starting with a defined prefix\n'
	         'It relies on NCBI blastN package in $PATH.\n'
	         'Within working directory, it creates folders representing categories, and outputs reads matching the categories there.\n\n'
	         'Usage: ./clean_barcodes.py <path_to_working_dir> <folder_with_input_fasta_files> <path_to_reference_db.fasta> \n')

Script, WorkingDir, InputDir, ReferenceDb = sys.argv

Categories = ['BEE', 'WOLBACHIA', 'STREPSIPTERA'] ### For now, pre-defined. In subsequent versions, they will be provided in a separate file.

percIdentThreshold = 90


###########################
### 0. Define functions ###

		# Imports a multifasta as a list of lists, where secondary lists consist of two
		# elements: heading and sequence. Takes the whole sequence name as heading
def ImportFastaAsList(fasta_file):
   FASTA = open(fasta_file, 'r')
   Seq_list = []
   Sequence = ''
   Seq_heading = ''
   for line in FASTA:   # Copying the sequence (potentially spread across multiple lines) to a single line
      if line.startswith('>'):
         if Sequence != '':   # Saves the existing Seq_heading and Sequence to a list before overwriting them
            Seq_list.append([Seq_heading, Sequence])
         Sequence = ''
         Seq_heading = line.strip().strip(">") # Takes the whole name as heading
      else:
         Sequence = Sequence + line.strip().upper()
   Seq_list.append([Seq_heading, Sequence.strip('')]) # Saves the final sequence (Seq_heading and Sequence) to a list

   FASTA.close()
   return(Seq_list)






#################################################################
### 1. Check the validity of reference dir and reference db, etc. ###

WorkingDir = str(WorkingDir)
if WorkingDir.endswith("/"):
    WorkingDir = WorkingDir[:-1]
    if not os.path.exists(WorkingDir):
        sys.exit('ERROR! Ensure that the path to the working directory is specified correctly!\n'
                 'Exiting......\n')


InputDir = str(InputDir)
if InputDir.endswith("/"):
    InputDir = InputDir[:-1]    
    if not os.path.exists(WorkingDir):
        sys.exit('ERROR! Ensure that the path to the directory with input fasta files is specified correctly!\n'
                 'Exiting......\n')

ReferenceDb = str(ReferenceDb)
if os.path.exists(ReferenceDb) and ReferenceDb.split(".")[-1] in ["fasta", "fa"]:
    if not os.path.exists("%s.ndb" % ReferenceDb):
        print("Reference fasta %s found, but not database files ... making blast db!" % ReferenceDb)
        os.system("makeblastdb -in %s -dbtype nucl" % ReferenceDb)
else:
	sys.exit('ERROR! Database file not found. Check the path that you provided!\n'
	         'Exiting......\n')





########################################################
### 2. Listing FASTA files in the directory provided ###

TargetDirContents = os.listdir(path=InputDir)
FASTA_list = []
for item in TargetDirContents:
    if item.split(".")[-1] in ["fa", "fasta"]:
        FASTA_list.append(item)

if len(FASTA_list) == 0:
    sys.exit('ERROR! No fasta files found in the input directory provided!\n'
	         'Exiting......\n')




####################################################################
### 3. Create sequence counting table, create output directories ###

SeqCounts = [['filename']]
''' Ultimately, SeqCounts should look like, 
[['filename', 'BEE', 'WOLBACHIA', 'unclassified', 'total'],
 ['File01.fa', 100, 10, 200, 210]]'''

for category in Categories:
    SeqCounts[0].append(category)
    
SeqCounts[0].append("unclassified")
SeqCounts[0].append("total")


# creating output folders for each of the categories
for category in Categories:
    if not os.path.exists("%s/%s" % (WorkingDir, category)):
        os.mkdir("%s/%s" % (WorkingDir, category))

if not os.path.exists("%s/unclassified" % WorkingDir):
    os.mkdir("%s/unclassified" % WorkingDir)

if not os.path.exists("%s/blastn_results" % WorkingDir):
    os.mkdir("%s/blastn_results" % WorkingDir)




###########################################
#### 4. Process individual FASTA files ####

Lib_count = len(FASTA_list)
print("Processing %s libraries in your directory ...")

Lib_no = 0
for FASTA in FASTA_list:
    Lib_no += 1
    print("Processing library %s / %s , %s .... " % (Lib_no, Lib_count, FASTA)) 

    if not os.path.exists("%s/blastn_results/%s.blastn" % (WorkingDir, FASTA)):    
        os.system("blastn -task megablast -db %s -query %s/%s -outfmt 6 -num_threads 8 -max_hsps 1 -max_target_seqs 1 -evalue 1e-10 -perc_identity 80 > %s/blastn_results/%s.blastn" % (ReferenceDb, InputDir, FASTA, WorkingDir, FASTA))
    
    BLASTN = open("%s/blastn_results/%s.blastn" % (WorkingDir, FASTA), "r")
    
    categoryCount = {}      # The dictionary will ultimately look like, {'BEE': 23}
    for category in Categories:
        categoryCount[category] = 0
    
    readClassify = {}      # The dictionary will ultimately look like, {'Read1': 'BEE', 'Read2': 'unclassified'}
    
    
    for line in BLASTN: # Which may look like:       662108_2_1_3	BEE_GBCHA58713|Bombus	98.091	419	3	4	1	414	239	657	0.0	707
        if not line.startswith("Warning"):
            LINE = line.split()
            seqID = LINE[0]
            topHitCategory = LINE[1].split("_")[0]
            percIdent = float(LINE[2])
            
            if topHitCategory in Categories and percIdent >= percIdentThreshold: 
                categoryCount[topHitCategory] += 1
                readClassify[seqID] = topHitCategory
            
            else:
                readClassify[seqID] = "unclassified"

    
    ### Importing FASTA file
    RAW_READS = ImportFastaAsList("%s/%s" % (InputDir, FASTA))
    
    
    ### Adding info on counts in different categories to SeqCounts 
    SeqCounts.append([FASTA])    
    countsAllCategories = 0
    for category in Categories:
        SeqCounts[-1].append(categoryCount[category])
        countsAllCategories += categoryCount[category]
    
    totalReadNo = len(RAW_READS)
    unclassifiedReadNo = totalReadNo - countsAllCategories
        
    SeqCounts[-1].append(unclassifiedReadNo)
    SeqCounts[-1].append(totalReadNo)
    
    
    
    SeqPile = {}               # The dictionary will ultimately look like, {'BEE': [['Read1': 'ACGT'],['Read2': 'CCGT']]}
    for category in Categories:
        SeqPile[category] = []
    SeqPile['unclassified'] = []
    
    
    for read in RAW_READS:
        if read[0] in readClassify.keys():    
            # read's category = readClassify[read[0]]
            SeqPile[readClassify[read[0]]].append(read)
        else:
            SeqPile['unclassified'].append(read)    
    
    BLASTN.close()
    
    for category in SeqPile.keys():
        if len(SeqPile[category]) > 0:
            OUTPUT_FASTA = open("%s/%s/%s_%s" % (WorkingDir, category, category, FASTA), "w")
        
            for read in SeqPile[category]:
                print(">", read[0], "\n", read[1], sep = '', file = OUTPUT_FASTA)
            OUTPUT_FASTA.close()






#######################################
###### 5. Print stats to stdout  ######

print("\nAnalysis complete :) \nNumbers of reads per category, per file:")

for row in SeqCounts:
    for item in row[:-1]:
        print(item, end="\t")
    print(row[-1])


#######################################
###             DONE :)             ###

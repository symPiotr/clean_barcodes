# Barcoding analysis Workflow - Illumina data - as implemented on the library comprising barcoded IBA and phorid samples
  
Steps:  
  
1. Raw data - nine libraries for different batches of samples - is at `/mnt/qnap/users/symbio/raw_data/illumina/amplicon_sequencing/20240430_NextSeq_batch21/BARCODES`
```
(base) piotr.lukasik@bug:~/raw_data/illumina/amplicon_sequencing/20240430_NextSeq_batch21/BARCODES$ ls
BARCODES_pool_01_R1.fq.gz  BARCODES_pool_02_R2.fq.gz  BARCODES_pool_04_R1.fq.gz  BARCODES_pool_05_R2.fq.gz  BARCODES_pool_07_R1.fq.gz  BARCODES_pool_08_R2.fq.gz
BARCODES_pool_01_R2.fq.gz  BARCODES_pool_03_R1.fq.gz  BARCODES_pool_04_R2.fq.gz  BARCODES_pool_06_R1.fq.gz  BARCODES_pool_07_R2.fq.gz  BARCODES_pool_09_R1.fq.gz
BARCODES_pool_02_R1.fq.gz  BARCODES_pool_03_R2.fq.gz  BARCODES_pool_05_R1.fq.gz  BARCODES_pool_06_R2.fq.gz  BARCODES_pool_08_R1.fq.gz  BARCODES_pool_09_R2.fq.gz
```  
  
2. On the cluster, I assemble forward and reverse reads using pear:
```
### Basic syntax:
pear -f BARCODES_R1.fq.gz -r BARCODES_R2.fq.gz -o BAR -j 16
  -f, --forward-fastq         <str>     Forward paired-end FASTQ file.
  -r, --reverse-fastq         <str>     Reverse paired-end FASTQ file.
  -o, --output                <str>     Output filename.
  -j, --threads               <int>     Number of threads to use

### Specific implementation - "for" loop executed within raw data folder, with output saved in specified folder in my home directory:
(base) piotr.lukasik@bug:~/raw_data/illumina/amplicon_sequencing/20240430_NextSeq_batch21/BARCODES$ for no in 1 2 3 4; do echo $no; pear -f BARCODES_pool_0"$no"_R1.fq.gz -r BARCODES_pool_0"$no"_R2.fq.gz -o ~/20240524_barcodes/BAR0"$no" -j 40; done 
```  
  
3. I download the `BAR0x.assembled.fastq` files to my Mac, using Cyberduck  
  
4. On my Mac, I run [ONTbarcoder v0.1.9](https://github.com/asrivathsan/ONTbarcoder) - initially, using the BAR02.assembled.fastq and the [demultiplexing file for BAR02](https://github.com/symPiotr/clean_barcodes/blob/main/BAR02_IBA_and_phorid_demultiplexing_sheet.txt) provided by Anna. Parameters:
```
Minimum Length: 400
Expected barcode length: 418
Window to select reads of during demultiplexing: 100
Build consensus based on reads subset by length: True
Build consensus based on reads subset by similarity: True
Fix barcodes based on MSA: True
Window to select reads of long length after demultiplexing: 50
Coverage used for barcode calling based on subsetting reads by lengths: [5, 25, 50, 100, 200, 500]
Coverage used for barcode calling in 2nd step, based on subsetting reads by similarity: 100
Genetic code: 5
```  
  
5. Inspect the `runsummary.xlsx` file in your output directory, and enjoy high success rate of barcode reconstruction :)  

6. Change directory to the `demultiplexed` folder in your output directory, and run [clean_demultiplexed.py](https://github.com/symPiotr/clean_barcodes/blob/main/clean_demultiplexed.py) on all *fa files:
```
$ cd BAR02
$ cd demultiplexed
$ for file in *fa; do clean_demultiplexed.py $file; done 
```  
  
7. Run [clean_barcodes.py](https://github.com/symPiotr/clean_barcodes/blob/main/clean_barcodes.py) on cleaned fasta files, using a pre-configured reference database. When processing barcoding libraries for diverse Swedish hoppers, not all of which closely matched references, I used a reference db [HOMO_WOLBACHIA_PIPUNCULIDAE.fasta](https://github.com/symPiotr/clean_barcodes/blob/main/HOMO_WOLBACHIA_PIPUNCULIDAE.fasta) to filter out human, parasitoid, and *Wolbachia/Rickettsia* reads, with the assumtion that the remaining reads are more likely to represent the hopper barcode.  
Note that the current version of the script does not use multiple processors - the searches do take a while!  
```
$ clean_barcodes.py 
---------------- clean_barcodes.py v. 0.2 - by Piotr Łukasik, 9 Feb 2024 ---------------

This script breaks up fasta files provided by ONTbarcoder based on results of BLAST searches against a custom database.
The script was designed to use as input a folder with de-multiplexed fasta files, representing noisy Nanopore COI sequences for different samples
(but it should also work with most other fasta files, for COI as otherwise, as long as you prepare the right database).It also relies on a pre-prepared sequence database, where reads representing categories of interest have names starting with a defined prefix
It relies on NCBI blastN package in $PATH.
Within working directory, it creates folders representing categories, and outputs reads matching the categories there.

Usage: ./clean_barcodes.py <path_to_working_dir> <folder_with_input_fasta_files> <path_to_reference_db.fasta> 

$ mkdir split
$ clean_barcodes.py split demultiplexed /Users/piotrlukasik/bioinfo/20240211_barcode_splitting/HOMO_WOLBACHIA_PIPUNCULIDAE.fasta
```  
  
8. Display stats --- file *000_splitting_summary.txt* in your output folder contains info on read number matched to each target.  
  
9. For each of the split folders that you care about (Unclassified, Pipunculidae, Wolbachia) run ONTbarcoder in "barcode reconstruction" mode.  
  
10. In Excel, combine the aforementioned *000_splitting_summary.txt* and *runsummary.xlsx* for each split folder
  
11. For the three datasets, consider using [mothur](https://mothur.org/), or another tool, to identify unique genotypes and cluster them into OTUs
```
### Identifying unique sequences
mothur "#unique.seqs(fasta=BAR.fasta, format=name)"

### Clustering
mothur "#dist.seqs(fasta=BAR.unique.fasta)"
mothur "#cluster(column=BAR.unique.dist, name=BAR.names, cutoff=0)"
mothur "#bin.seqs(list=BAR.unique.opti_mcc.list, fasta=BAR.fasta)"
   ### -> This should result in file BAR.unique.opti_mcc.0.fasta, with information on which zero-radius OTU (zOTU) each sequence is assigned to.
mothur "#cluster(column=BAR.unique.dist, name=BAR.names, cutoff=0.03)"
mothur "#bin.seqs(list=BAR.unique.opti_mcc.list, fasta=BAR.fasta)"
   ### -> This should result in file BAR.unique.opti_mcc.0.03.fasta, with information on which 97% OTU each sequence is assigned to.
``` 
    
12. Assign taxonomy to sequences. Perhaps using vsearch / sintax --- or perhaps by submitting batches of your sequences to BOLD
    ```
    vsearch --sintax Allbarcodes.fa -db /mnt/qnap/users/symbio/software/databases/MIDORI_with_tax_spikeins_endo_RDP.fasta -tabbedout otus2.tax -strand both -sintax_cutoff 0.8
    ```
  
13. Combine all resulting information in Excel!

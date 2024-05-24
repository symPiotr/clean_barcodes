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
  
3. I download the BAR0x.assembled.fastq files to my Mac, using Cyberduck  
  
4. On my Mac, I run [ONTbarcoder v0.1.9](https://github.com/asrivathsan/ONTbarcoder) using the assembled.fastq and the [demultiplexing file](file.txt) provided by Anna 

4. Copy BARCODES* data from /mnt/qnap/users/symbio/raw_data/illumina/metagenomics/20240130_NextSeq_batch20

5. Merge reads using pear
   pear -f BARCODES_R1.fastq.gz -r BARCODES_R2.fastq.gz -o BAR_20240130 -j 16

6. Run ONTbarcoder on BAR_20240130.assembled.fastq

..... Optional: consider running a specificity filter on demultiplexed data, similar to what I've implemented for bees, and redoing barcode reconstruction on symbiont-free data

... Ensure that in the demultiplexed fastq, Napisać skrypt do analiz NanopoCOI 
    E->A
    F->G
    Q->C
    P->T

4. Export Allbarcodes.fa

..... Consider using mothur to identify unique genotypes
    mothur "#unique.seqs(fasta=Allbarcodes.fa)"

..... Consider clustering unique genotypes into OTUs

5. Assign taxonomy to sequences
    vsearch --sintax Allbarcodes.fa -db /mnt/qnap/users/symbio/software/databases/MIDORI_with_tax_spikeins_endo_RDP.fasta -tabbedout otus2.tax -strand both -sintax_cutoff 0.8

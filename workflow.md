# Barcoding Workflow - Illumina data


Steps:

1. Copy BARCODES* data from /mnt/qnap/users/symbio/raw_data/illumina/metagenomics/20240130_NextSeq_batch20

2. Merge reads using pear
   pear -f BARCODES_R1.fastq.gz -r BARCODES_R2.fastq.gz -o BAR_20240130 -j 16

3. Run ONTbarcoder on BAR_20240130.assembled.fastq

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

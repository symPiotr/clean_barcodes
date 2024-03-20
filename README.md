# clean_demultiplexed, clean_barcodes
**clean_demultiplexed.py** and **clean_barcodes.py** are two scripts for cleaning ONTbarcoder-provided demultiplexed COI files through blastn searches against a custom sequence database.  


  
**clean_demultiplexed.py** converts FASTA files provided by ONTbarcoder into the format compatible with BLAST and clean_barcodes.py.    
**Specifically**, it converts sequences where special characters [EFQP] were used instead of [ACGT] as a way of indicating sequences in reverse orientation - as discussed in [https://github.com/asrivathsan/ONTbarcoder/issues/2](https://github.com/asrivathsan/ONTbarcoder/issues/2). Undetermined bases "N" remain unchanged.
Also, it replaces any characters ":" (colon) in sequence names, and removes any portion of sequence name after space.  
  
The script should be compatible with most versions of Python 3, with no additional dependencies.
  
Usage:  
`clean_demultiplexed.py sample123.fasta`  

Or for multiple fasta files that are in the same directory:  
`for file in *.fasta; do clean_demultiplexed.py $file; done`  
  
Alternatively, instead of using the script above, you could probably do something like,  
```
sed -i 's/E/A/g;s/F/G/g;s/P/T/g;s/Q/C/g' *.fasta  
sed -i 's/ /_/g;s/:/_/g;s/+/_/g' *.fasta
```   
   
   
The **clean_barcodes.py** script breaks up cleaned-up (as described above) demultiplexed fasta files, based on results of BLAST searches against a custom database.  
It relies on NCBI blastN package in PATH, and a customized database (see below) that sequences are *BLAST*-ed against. 
  
As input, the script uses a folder with de-multiplexed fasta files, representing demultiplexed sequences. It also relies on a pre-prepared sequence database, where reads representing categories of interest have names starting with a pre-defined prefixes. Categories you may want to pre-define when working with insect COI barcoding data are HOMO and WOLBACHIA. Then, you'll need to make a database combining human and Wolbachia COI sequences, and expect that your target reads (non-Wolbachia and non-human) will be sorted out as "Undetermined". 
```
$ head -4 HOMO_WOLBACHIA.fasta
>WOLBACHIA_GCA_947251965.1
atgagtgacgcaccaaagggcataaagcgttggttgttttccaccaac...
>HOMO_GBHUM009;tax=k:Chordata,p:Mammalia,c:Primates,o:Hominidae,f:Homo,g:Homo_sapiens,s:BOLD_ACX9869
GGGTCAACAAATCATAAAGATATTGGAACACTATATTTATTGTTTGGTGCATGAGCTGGAGTCT...
...
```
  
You may also consider adding to the database sequences of your study organism's parasitoids, or others... depending on your system, quality of available references for your group, and your research questions!  
    
Here, I have uploaded databases that you could use:
HOMO_WOLBACHIA.fasta  
HOMO_WOLBACHIA_BEE.fasta  
HOMO_WOLBACHIA_TACHINIDAE_CARABUS.fasta  
  ... all based on reference sequences for the above clades downloaded from BOLD database in November 2023. When using the script, you should specify the categories yourself in line XX of the script.  
  
Within working directory, the script creates folders representing pre-defined categories, outputs reads matching the categories in these folders, and prints statistics - the number of reads filtered out. You should then be able to run **ONTbarcoder** in barcode reconstruction mode using the contents any of these folders.
  
Usage:  

```
Usage: ./clean_barcodes.py <path_to_working_dir> <folder_with_input_fasta_files> <path_to_reference_db.fasta> \n')
E.g., clean_barcodes.py ~/barcodes_test ~/barcodes_test/input_fasta ~/barcodes_test/ref_db/HOMO_WOLBACHIA_BEE.fasta
```

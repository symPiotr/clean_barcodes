# clean_demultiplexed, clean_barcodes
clean_demultiplexed.py and clean_barcodes.py are two scripts for cleaning ONTbarcoder-provided demultiplexed COI files through blastn searches against a custom sequence database.
&nbsp;
&nbsp;
**clean_demultiplexed.py** converts FASTA files provided by ONTbarcoder into the format compatible with BLAST and clean_barcodes.py :)

Specifically, it converts sequences where special characters [EFQP] were used instead of [ACGT] as a way of indicating sequences in reverse orientation - as discussed in [https://github.com/asrivathsan/ONTbarcoder/issues/2](https://github.com/asrivathsan/ONTbarcoder/issues/2). Undetermnied bases "N" remain unchanged.
Also, it replaces any characters ":" (colon) in sequence names, and removes any portion of sequence name after space.

Usage: 
`clean_demultiplexed.py sample123.fasta`
`for file in *.fasta; do clean_demultiplexed.py $file; done`
&nbsp;
&nbsp;

The script breaks up fasta files provided by ONTbarcoder based on results of BLAST against a custom database.
As input, it uses a folder with de-multiplexed fasta files, representing noisy Nanopore COI sequences for different samples
It also relies on a pre-prepared sequence database, where reads representing categories of interest have names starting with a defined prefix

It relies on NCBI blastN package in PATH.
Within working directory, it creates folders representing categories, and outputs reads matching the categories there.


Usage: ./clean_barcodes.py <path_to_working_dir> <folder_with_input_fasta_files> <path_to_reference_db.fasta> \n')
E.g., clean_barcodes.py ~/barcodes_test ~/barcodes_test/input_fasta ~/barcodes_test/ref_db/BEE_COI_refs.fasta

# clean_barcodes
clean_barcodes.py is a tool for cleaning ONTbarcoder-provided demultiplexed COI files through blastn searches against a pre-defined sequence database.

The script breaks up fasta files provided by ONTbarcoder based on results of BLAST against a custom database.
As input, it uses a folder with de-multiplexed fasta files, representing noisy Nanopore COI sequences for different samples
It also relies on a pre-prepared sequence database, where reads representing categories of interest have names starting with a defined prefix

It relies on NCBI blastN package in PATH.
Within working directory, it creates folders representing categories, and outputs reads matching the categories there.


Usage: ./clean_barcodes.py <path_to_working_dir> <folder_with_input_fasta_files> <path_to_reference_db.fasta> \n')
E.g., clean_barcodes.py ~/barcodes_test ~/barcodes_test/input_fasta ~/barcodes_test/ref_db/BEE_COI_refs.fasta

#! /usr/bin/env python3

import sys, re

if len(sys.argv) != 2:
	sys.exit('---------------- clean_demultiplexed.py v. 0.2 - by Piotr Łukasik, 9 Feb 2024 ---------------\n\n'
	         'This script cleans a demultiplexed fasta file provided by ONTbarcoder, or provided by pear assembly of Illumina reads.\n'
	         'Usage: ./clean_demultiplexed.py <fasta_file> \n'
	         'Or in a loop: for file in *fasta; do clean_demultiplexed.py $file; done')
Script, Fasta = sys.argv


### Reads fasta, saves seqs in Sequence_list

FASTA = open(Fasta, 'r')

Sequence_list = []

Sequence = ''
for line in FASTA:   # Copying the sequence (potentially spread across multiple lines) to a single line
    if line.startswith('>'):
       if Sequence != '':   # Saves the existing Seq_heading and Sequence to a list before overwriting them
          Sequence_list.append([Seq_heading, Sequence])
          Sequence = ''
       Seq_heading = line.strip('\n')
       Seq_heading = re.sub(' .*', '', Seq_heading) # throws away any bits of sequence name after space
       Seq_heading = re.sub(':', '_', Seq_heading) # replaces colons with underscores
       
    else:
       Sequence = Sequence + line.strip('\n').upper()

Sequence_list.append([Seq_heading, Sequence]) # Saves the final sequence (Seq_heading and Sequence) to a list
       
FASTA.close()

### In Sequence_list, in all seqs, replaces PQFE characters na TCGA [see https://github.com/asrivathsan/ONTbarcoder/issues/2]

Repl_Dict = {'P': 'T', 'Q': 'C', 'F': 'G', 'E': 'A', 'N': 'N'}

for entry in Sequence_list:
    if entry[1][0] in ['A', 'C', 'G', 'T']:
        entry.append(entry[1])
    elif entry[1][0] in ['P', 'Q', 'F', 'E']:
        entry.append('')
        for nucl in entry[1]:
            entry[2] += Repl_Dict[nucl]

### In Sequence_list, in all seqs, replaces PQFE characters na TCGA

FASTA = open(Fasta, 'w')

for entry in Sequence_list:
    print(entry[0], '\n', entry[2], '\n', end = '', sep = '', file = FASTA)
    
FASTA.close()

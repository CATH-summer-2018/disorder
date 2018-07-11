#!/usr/bin/python

'''
From directory containing the collection of fasta files for each CATH SFAM,
create a folder for each sfam. Each folder contains one fasta file for each domain.
'''

import os

from Bio import SeqIO


def extract_fasta(inp_dir, out_dir):
    for file in os.listdir(inp_dir):
        sfam = file[22:-3]
        os.makedirs(out_dir + sfam)
        fasta_sequences = SeqIO.parse(open(inp_dir+file),'fasta')
        for fasta in fasta_sequences:
            name, seq = fasta.id[13:20], str(fasta.seq)
            with open(out_dir+sfam+"/"+name, 'w') as f:
                f.write(seq)

extract_fasta('./input/', './individual_fasta/')

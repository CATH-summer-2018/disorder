from Bio import SeqIO
import os
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

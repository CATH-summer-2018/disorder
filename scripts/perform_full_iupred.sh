#!/bin/bash

# Performs the iupred on all files in all folders.
# For each file does long and short iupred calculation, with respective naming

for f in individual_fasta/*/*; do
  ./iupred2a.py $f short > $f.short
  ./iupred2a.py $f long > $f.long
done

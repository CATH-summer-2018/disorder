#!/bin/bash
for f in individual_fasta/*/*; do
  ./iupred2a.py $f long > $f.results
done

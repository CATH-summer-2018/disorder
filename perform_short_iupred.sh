#!/bin/bash
for f in individual_fasta/*/*; do
  if [[ $f =~ .*"result".* ]]; then
    mv $f ${f: : -7}long
  else
    ./iupred2a.py $f short > $f.short
  fi
done

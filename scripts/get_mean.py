#!/usr/bin/python

'''
Uses the result of the perform_full_iupred.sh script as the input.
For each superfamily generate a pandas series that has a mean disorder of each domain.
Then write the series in the output file, separate for long and short.
'''

import os

import pandas as pd

def ser_from_dir(folder): #returns series of means from one sfam/folder
    short=pd.Series()
    long=pd.Series()
    for file in os.listdir(folder):
        if 'long' in file:
            df = pd.read_csv(folder+'/'+file, sep='\t')
            long[file[:7]] = df.DIS.mean()
        elif 'short' in file:
            df = pd.read_csv(folder+'/'+file, sep='\t')
            short[file[:7]] = df.DIS.mean()
    return short.sort_index(), long.sort_index()

def compile_disorders(directory): #performs previous function for all folders
    with open('long_results.tsv', 'w') as long:
        long.write('DOM    DIS\n')
    with open('short_results.tsv', 'w') as short:
        short.write('DOM    DI\n')
    for folder in os.listdir(directory):
        s, l = ser_from_dir('/'.join([directory,folder]))
        with open('long_results.tsv', 'a') as long:
            long.write(l.to_string())
        with open('short_results.tsv', 'a') as short:
            short.write(s.to_string())

compile_disorders('./individual_fasta')

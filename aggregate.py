#!/usr/bin/python

import os
import pandas as pd

def get_all_data(directory):
    s = pd.Series()
    for folder in os.listdir(directory):
        try:
            for file in os.listdir(folder):
                if 'result' not in file:
                    continue
                df = pd.read_csv(directory+folder+file, sep='\t')
                s[file] = df.DIS.mean()
        except:
            pass
    return s
get_all_data('./individual_fasta').to_csv('all_data.tsv', sep='\t')

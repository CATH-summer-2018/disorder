#!/usr/bin/python

import os
import pandas as pd

def get_all_data(directory):
    for folder in os.listdir(directory):
        s=pd.Series()
        try:
            for file in os.listdir(directory+'/'+folder):
                if 'result' not in file:
                    continue
                df = pd.read_csv(directory+'/'+folder+'/'+file, sep='\t')
                s[file[:7]] = df.DIS.mean()
        except Exception as e:
            print(e)
        with open('all_data.tsv', 'a+') as f:
            f.write(s.to_string() + '\n')
get_all_data('./individual_fasta')

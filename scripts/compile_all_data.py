#!/usr/bin/python
import pandas as pd

'''
Compiles the info about domains from CATH with calculated disorders,
and puts them into one big tsv
'''

def compile_all(long, short, info):
    df = pd.read_csv(info,
                     sep='\s+',
                     index_col=0)
    df['SHORT'] = pd.read_csv(short,
                              sep='\s\s+',
                              index_col=0)
    df['LONG'] = pd.read_csv(long,
                             sep='\s\s+',
                             index_col=0)
    df['SFAM'] = df['C'].astype(str)+'.'+df['A'].astype(str)+'.'+df['T'].astype(str)+'.'+df['H'].astype(str)

    df = df[['S35', 'S100', 'LEN', 'RES', 'SHORT', 'LONG', 'SFAM']]
    return df

compile_all(long='./long_results.tsv',
            short='./short_results.tsv',
           info='./cath-domain-list.txt').to_csv('./compiled.tsv', sep='\t')

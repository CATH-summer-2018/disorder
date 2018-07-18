#!/usr/bin/python
'''
Module for working with the disorder files generated by iupred
'''
import requests
import os
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import scipy
import seaborn as sns
import plotly
import plotly.graph_objs as go
import plotly.plotly as py
import py3Dmol

### PLOTS

def plt_scatter(s, col1, col2,
                col_cutoff=False, cutoff=False,
                savedname=False, title=False, marksize=15):
    '''
    Plots the scatter plot for 2 columns in the dataframe
    '''
    fig, ax = plt.subplots(figsize=(15,15))
    x = s.sort_values(by=col1)[col2].values
    y = s.sort_values(by=col1)[col1].values
    ax.set_xlim(min(x), max(x))
    ax.set_ylim(min(y), max(y))
    ax.set_xlabel(col2)
    ax.set_ylabel(col1)
    if col_cutoff:
        under = s[s[col_cutoff] < cutoff]
        over = s[s[col_cutoff] >= cutoff]
        x_under = under.sort_values(by=col1)[col2].values
        y_under = under.sort_values(by=col1)[col1].values
        x_over = over.sort_values(by=col1)[col2].values
        y_over = over.sort_values(by=col1)[col1].values
        ax.scatter(x_under, y_under, s=marksize, marker='x', c='#1E70AA')
        ax.scatter(x_over, y_over, s=marksize, marker='x', c='blue')
    else:
        ax.scatter(x, y, s=marksize, marker='.', c='#1E70AA')
    if title:
        plt.title(title)
    if savedname:
        plt.savefig(savedname, bbox_inches='tight')
    plt.show()

def plt_inter_scatter(s, col1, col2, savedname='./figs/tmp.html', show='jup',
                col_cutoff=False, cutoff=False, title=False, marksize=15):
    '''
    Plots the scatter plot for 2 columns in the dataframe
    '''
    x = s[col1]
    y = s[col2]
    trace=go.Scatter(
    x=x,
    y=y,
    mode = 'markers',
    marker=dict(size=5,
               color = 'rgba(0, 0, 255, .4)'),
               hoverinfo='text',
    text= 'ID: ' + s.index + '<br> ' + col1 + ': ' + x.round(3).astype(str) + '<br>'+ col2 + ': ' + y.round(3).astype(str),
    line=dict(width=2))

    data=[trace]
    layout = go.Layout(dict(hovermode='closest',
    title='Disorder scatterplot',
    xaxis= dict(
        title=col1,
        ticklen= 5,
        zeroline= False,
        gridwidth= 2,
    ),
    yaxis=dict(
        title=col2,
        ticklen= 5,
        gridwidth= 2,
    )))
    fig = go.Figure(data, layout)
    if show == 'jup':
        plotly.offline.iplot(fig)
    elif show == 'html':
        plotly.offline.plot(fig, filename=savedname)

def plt_regplot(s, col1, col2,
                savedname=False, title=False):
    '''
    Plots the scatter plot for 2 columns in the dataframe
    '''
    fig, ax = plt.subplots(figsize=(15,15))
    x = s.sort_values(by=col1)[col2].values
    y = s.sort_values(by=col1)[col1].values
    ax.set_xlim(min(x), max(x))
    ax.set_ylim(min(y), max(y))
    ax.set_xlabel(col2)
    ax.set_ylabel(col1)
    sns.regplot(x, y,
    scatter_kws={"s": 5},
    line_kws={'color':'blue'},
    marker='.',ci=None)
    if title:
        plt.title(title)
    if savedname:
        plt.savefig(savedname, bbox_inches='tight')
    plt.show()

def plot_heat(data, annot=False, savedname=False):
    '''
    Plots heatmap from the distance matrix
    '''
    fig, ax = plt.subplots(figsize=(30,30))
    mask = np.zeros_like(data)
    mask[np.triu_indices_from(mask)] = True
    sns.heatmap(data, mask=mask, annot=annot)
    if savedname:
        plt.savefig(savedname, bbox_inches='tight')
    plt.show()



### CLASSES

class Domain(object):
    '''
    Class for fetching stuff for a domain
    '''
    def __init__(self, df, domain):
        self.domain = domain
        self.long = pd.read_csv('./individual_fasta/'+df.loc[domain]['SFAM']+'/'+domain+'.long', sep='\t', index_col=0)
        self.short = pd.read_csv('./individual_fasta/'+df.loc[domain]['SFAM']+'/'+domain+'.short', sep='\t', index_col=0)

    def plot_disorder(self, method='both'):
        '''
        Plots the disorder for individual domain
        '''
        fig, ax = plt.subplots(figsize=(15,5))
        ax.plot([0, len(self.long)], [0.5,0.5], color='black', linewidth=0.7)
        ax.set_xlim(0, len(self.long))
        ax.set_ylim(0,1)
        if method == 'long':
            ax.plot(self.long.DIS)
        elif method == 'short':
            ax.plot(self.short.DIS)
        elif method == 'both':
            ax.plot(self.long.DIS, color='blue', label='LONG')
            ax.plot(self.short.DIS, color='orange', label='SHORT')
            plt.legend()
        else:
            print("Wrong method")
        plt.show()


    def show_structure(self):
        '''
        Uses py3Dmol and requests to fetch domain PDB and show it in jupyter
        '''
        view = py3Dmol.view()

        def adjust_looks(view):
            view.setStyle({'cartoon':{'colorscheme':'ssJmol'}})
            view.center()
            return view

        if (self.domain + '.pdb') in os.listdir('structures'):
            with open('./structures/'+self.domain+'.pdb') as file:
                view.addModel(file.read(), 'pdb')
                return adjust_looks(view)
        else:
            r = requests.get('http://www.cathdb.info/version/v4_2_0/api/rest/id/' + self.domain + '.pdb')
            with open('./structures/' + self.domain + '.pdb', 'w') as file:
                file.write(r.text)
            view = view.addModel(r.text, 'pdb')
            return adjust_looks(view)


class DomParser(object):
    '''
    Methods for quick work with domains DataFrame
    '''
    def __init__(self, df):
        self.df = df

    def get_sfam(self, sfam):
        return self.df[self.df['SFAM'] == sfam]


    def scrape_sfam(self, gr):
        '''
        Compiles information for each CATH superfamily rather than each domain
        '''
        dom_len = pd.Series()
        std_len = pd.Series()
        max_len = pd.Series()
        min_len = pd.Series()
        long = pd.Series()
        short = pd.Series()
        std_long = pd.Series()
        std_short = pd.Series()
        sample = pd.Series()
        for n, d in gr:
            short[n] = d.SHORT.mean()
            long[n] = d.LONG.mean()
            std_short[n] = d.SHORT.std().round(6)
            std_long[n] = d.LONG.std().round(6)
            dom_len[n] = d.LEN.mean().round(6)
            std_len[n] = d.LEN.std().round(6)
            min_len[n] = d.LEN.min()
            max_len[n] = d.LEN.max()
            sample[n] = d.SHORT.idxmax()
        size = self.df.SFAM.value_counts()
        sfam = pd.DataFrame({'SIZE' : size,
                             'STD_SHORT' : std_short,
                             'STD_LONG' : std_long,
                             'LEN' : dom_len,
                             'STD_LEN' : std_len,
                             'SHORT' : short,
                            'LONG':long,
                            'MAX_LEN' : max_len,
                            'MIN_LEN' : min_len,
                            'SAMPLE':sample})
        return sfam

    def compile_sfam(self):
        '''
        Runs scrape_sfam for each superfamily using groupby
        '''
        gr = self.df.groupby('SFAM')
        sfam = self.scrape_sfam(gr)
        sfam['DIS_DIFF'] = (sfam['LONG'] - sfam['SHORT']).abs().round(6)
        sfam['STD_LEN_PERC'] = sfam['STD_LEN_PERC'] = sfam['STD_LEN']/sfam['LEN']
        return sfam

    def plot_len_distr(self,sfam):
        fig, ax = plt.subplots(figsize=(10,10))
        data = self.get_sfam(sfam).LEN.values

        ax.hist(data,
                25,
                edgecolor='black')
        ax.set_xlim(0, max(data)*1.1)
        plt.xlabel('Length')
        plt.ylabel('Number of domains')
        plt.show()


### CALCULATIONS


def distance_matrix(df, sfam_id):
    '''
    Returns distance matrix for one sfam
    '''
    sfam = df[df.query_superfamily_id == sfam_id]
    cols = pd.concat([sfam.query_id, sfam.match_id]).unique()
    t = pd.DataFrame(index=cols)
    for item in cols:
        w = sfam[(sfam.query_id == item) | (sfam.match_id == item)]
        w['match'] = w.query_id.combine(w.match_id, lambda x, y: x if x != item else y)
        w.drop_duplicates(subset='match', keep='last', inplace=True)
        w.set_index('match', inplace=True)
        t[item] = w['ssap_score']
    return t

def normalised_SSAP(t):
    '''
    Returns normalised SSAP scores
    '''
    return (t.mean() - t.mean().mean()).abs().sort_values()


def all_SSAP(ssap, ind):
    '''
    Returns a dictionary with info for SSAP for SFAMs
    '''
    mean_SSAP = pd.Series()
    min_SSAP = pd.Series()
    mean_std_SSAP = pd.Series()
    for i in ind:
        t = distance_matrix(ssap, i).mean()
        mean_SSAP[i] = t.mean()
        min_SSAP[i] = t.min()
        mean_std_SSAP[i] = t.std()
    return pd.DataFrame({'MEAN_SSAP':mean_SSAP,
                        'MIN_SSAP':min_SSAP,
                        'MEAN_STD_SSAP':mean_std_SSAP})

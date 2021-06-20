from api import Phoenix
import numpy as np 
import pandas as pd
ph = Phoenix() 

def scores_benchmarker(xs): 
    return sum(xs) / len(xs)

def encode_result(s): 
    if s <= 2: 
        return 1
    elif s > 2: 
        return 0
    else: 
        return np.nan
        
q = open(r'queries/reporting/sq.sql','r+').read() 
df = ph.get_df(q) # q == df, q != df

df['result'] = df.result.apply(encode_result) 

bins = np.arange(0,1.1,.2) 
df['civis_partisan_bin']   = pd.cut(df.civis_partisan,  bins=bins)       
df['ts_partisan_bin']      = pd.cut(df.ts_partisan,     bins=bins)    
df['dnc_demsupport_bin']   = pd.cut(df.dnc_demsupport,  bins=bins) 
df['civis_ideology_bin']   = pd.cut(df.civis_ideology,  bins=bins) 
df['clarity_turnout_bin']  = pd.cut(df.clarity_turnout, bins=bins)    
df['ts_turnout_bin']       = pd.cut(df.ts_turnout,      bins=bins)    


support_bins = ['civis_partisan_bin', 'ts_partisan_bin', 'dnc_demsupport_bin', 'civis_ideology_bin']
turnout_bins = ['clarity_turnout_bin', 'ts_turnout_bin']

pfs = list()
for support in support_bins: 
    for turnout in turnout_bins: 

        pf = pd.pivot_table( df, 
                index=turnout, 
                columns=support, 
                values='result', 
                aggfunc=scores_benchmarker) 

        print(support.iloc[9,9], turnout.iloc[9,9], pf.iloc[9,9]) 
        print(pf)

        pfs.append(pf)

difs = list()
for af in pfs: 
    for bf in pfs: 
        #this is really why i want to do this in python
        #the equivalent work to do in sql: https://adatastory.wordpress.com/2015/01/27/hacking-linear-algebra-in-sql/
        af_bf = af - bf
        _b = bf.iloc[1:-2,1:-2] #20 & 30 only 

        cum_sum = _b.sum().sum()

        for i, r in af_bf.iterrows(): 
            print(i,r)
            print(af-bf.columns.name,' + ', af_bf.index.name, ' + ' ,i, ' + ' ,r.name)



import numpy as np
import pandas as pd

from fenv.api import Phoenix
import glob

ph = Phoenix()

def id_rate(df, df_ids, df_fm):
    fm = df_fm[df_fm.dist_sth == df.dist_sth]
    b = fm.base.values[0]
    t = fm.turnout.values[0]
    d = (t / 2) - b

    ids = df_ids[(df_ids.dist_sth == df.dist_sth) & ((df_ids.result == '1') | (df_ids.result == '2'))]
    ids = set(ids.vanid.values)

    return len(ids) / d


#ids
ids = open(r'../queries/phasing/canvassed.sql').read()
df_ids = ph.get_df(ids)

#targ 
targ = open(r'../queries/phasing/target.sql').read()
df_targ = ph.get_df(targ) #in a pivot table they are there
#field math 
field = open(r'../queries/phasing/fieldmath.sql').read()
df_fm = ph.get_df(field)

#main index
tiers = ph.get_df('select o1 from demspahdcc.commons.tiers union all select o2 from demspahdcc.commons.tiers')
df = pd.DataFrame({'dist_sth':tiers.o1.dropna().astype(int)})
df['id_total_rate'] = df.apply(id_rate, axis=1, args=(df_ids, df_fm))

df.sort_values('id_total_rate', ascending=False, inplace=True)
print(df)

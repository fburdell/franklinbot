
import pandas as pd 
import numpy as np
from api import Postgres
from api import Phoenix


#apis
ph = Phoenix()
po = Postgres('main')

#print options
pd.set_option('display.max_rows',500)
pd.set_option('display.max_columns',500)


df = pd.read_csv(r'outputs/zip_tv_compile.csv') #from compile...py
df = df.sort_values('dist_sys_voters_pen', ascending=False)

#voter frame
vf = df[['in_district', 'zone_int', 'zip_code', 'state', 'sys_code', 'sys_name', 'sys_media',
    'system_type', 'dist_sth', 
    'zip_l2_voters_in_zip',
    'dist_voters_indist_est', 'dist_sys_voters_pen', 'dist_voters_indist_rate']]

def update_local_zip_file(): 
    q = open(r'queries/zip_query.sql').read()
    print('getting bq')
    zf = ph.get_df(q)
    print('writing bq...')
    zf['zip_a'] = zf.zip_a.astype(int)
    zf.to_sql('zip_code_file_2_0_local', con=po.sa_con(), index=False, if_exists='replace')

zf = pd.read_sql('zip_code_file_2_0_local', con=po.sa_con()) 
zf = zf.drop('dist_sth', axis=1)
df = df.merge(zf, 
        left_on='zip_code',
        right_on='zip_a',
        how='left')

af = df 
af = af.groupby(['','',''])

print(df.info(verbose=True))
print('\n\n\n\n')
df = df[df.in_district == 'Y']
print(df.info(verbose=True))

agg_set_a = ['sys_code','sys_name','sys_type','dist_sth','in_district']
agg_set_b = ['sys_code','sys_name','sys_type']




























































































            

#ini attempt at sys voter waste 
def af():
    
    print(df.info(verbose=True))
    afs = list()
    for ix, hd in enumerate(df.dist_sth.unique()): 
        tf = df[df.dist_sth == hd]

        systems = zip(tf.sys_code.unique(), 
                tf.sys_name.unique())
        
        af = tf[['dist_sth','sys_code','sys_name','sys_media','zip_l2_voters_in_zip','dist_voters_indist_est','dist_sys_voters_pen']]
        af = af.groupby(['dist_sth','sys_code','sys_name','sys_media']).sum()
        af['dist_sys_voters_pen'] = round(af['dist_sys_voters_pen'], 0)

        #these figures need to accoutn for in/out district of zip code
        af['sys_voter_waste'] = round(af.zip_l2_voters_in_zip - af.dist_sys_voters_pen, 0)
        af['sys_voter_waste_perc'] = round(af.sys_voter_waste / af.zip_l2_voters_in_zip, 4) * 100
        af['sys_voter_satur_perc'] = round(100 - af.sys_voter_waste_perc, 2)


        af.rename(columns={'zip_l2_voters_in_zip':'sys_voters',
            'dist_voters_indist_est':'sys_voters_indist',
            'dist_sys_voters_pen':'sys_voters_satur'}, inplace=True)

        #af.to_csv(rf'outputs/af_{hd}.csv')
        afs.append(af)

    caf = pd.concat(afs)
    caf.sort_values('sys_voter_satur_perc', ascending=False, inplace=True) 
    caf.to_csv(rf'outputs/af_all.csv')

def bf():
    #describing the districts
    #not necessarily 

    #df = df[df.in_district == 'Y']

    df.rename(columns={'zip_l2_voters_in_zip':'sys_voters',
        'dist_voters_indist_est':'sys_voters_indist',
        'dist_sys_voters_pen':'sys_voters_satur'}, inplace=True)

    #df.drop_duplicates(['zip_code','dist_sth'], inplace=True)
    df.sys_voters_satur = round(df.sys_voters_satur, 0)

    zips = df.zip_code.unique()
    house_districts = df.dist_sth.unique()

    agg_set_a = ['sys_code','sys_name','sys_type','dist_sth']
    agg_set_b = ['sys_code','sys_name','sys_type']

    #pfa ==, = gfa
    #essentially makes dist_sth unique
    pfa = df.groupby(agg_set_a).agg(
            {'sys_voters_satur':[('sum',np.sum),('median',np.median)], 
            'sys_voters_indist':[('sum',np.sum)],
            'sys_voters':[('sum',np.sum)]
        }
    )

    #print(type(pfa.iloc[:,2].name)

    #pfa ==, = gfa
    gfa = pfa.reset_index(
            ).groupby(
                agg_set_b).agg(
                    #{'dist_sth':[('all of them',lambda x: ','.join(str(x)))],
                    {('sys_voters_indist','sum'):[('sum',np.sum)],
                    ('sys_voters_satur','sum'):[('sum',np.sum)]
                    }
            )

    #count dist_sth in each zone
    pfb = pfa.reset_index()
    pfb['dist_sth'] = pfb.dist_sth.astype(str)
    gfa_ = pfb.groupby(
            agg_set_b).agg(
                {'dist_sth':[('unique', lambda x: len(x.unique()))]
                }
            )

    gfa_.rename({'dist_sth':'count_dist_sth'}, axis=1, inplace=True)
    gfa = gfa.merge(gfa_, 
            left_index=True, 
            right_index=True, 
            how='right')

    #gfa.sort_values(('sys_voters_satur','sum'), ascending=False, inplace=True,)
    #gfa.reset_index(inplace=True)
    #gfa = gfa[(gfa.sys_type == 'interconnect') | (gfa.sys_type == 'superzone')]

    #print(gfa.info(verbose=True))
    print(gfa.head(10))


    #af['sys_voter_waste'] = round(af.zip_l2_voters_in_zip - af.dist_sys_voters_pen, 0)
    #af['sys_voter_waste_perc'] = round(af.sys_voter_waste / af.zip_l2_voters_in_zip, 4) * 100
    #af['sys_voter_satur_perc'] = round(100 - af.sys_voter_waste_perc, 2)

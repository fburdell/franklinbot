import pandas as pd 

from api import Postgres, Phoenix

pd.set_option('display.max_rows',500)
pd.set_option('display.max_columns',500)


class TV: 


    def __init__(self): 
        import pandas as pd 
        vfs = ['in_district', 'zone_int', 'zip_code', 'state', 'sys_code', 'sys_name', 'sys_media', 'system_type', 'dist_sth', 'zip_l2_voters_in_zip', 'dist_voters_indist_est', 'dist_sys_voters_pen', 'dist_voters_indist_rate']

        self.path_df = r'outputs/zip_tv_compile.csv'
        self.db = pd.read_csv(path_df)
        self.vf = df[vfs]
        

        

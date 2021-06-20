import openpyxl
import pandas as pd
import glob

pd.set_option('display.max_columns', 500)

bad_name = ['Map','Coverage Detail']


def system_type(sys): 
    if 'Interconnect' in sys: 
        return 'interconnect'
    elif 'DirecTV' in sys: 
        return 'directv'
    elif 'DISH' in sys: 
        return 'dish'
    elif 'Ad System' in sys: 
        return 'adsys'
    else: 
        return 'cable'

def sys_media(df): 
    if 'Interconnect' in df.sys_name: 
        return df.sys_media + 'Interconnect'
    else:
        return df.sys_media

def sys_type(df): 
    if 'Interconnect' in df.sys_media:
        return 'interconnect'
    if 'DirecTV' in df.sys_name: 
        return 'satellite'
    if 'DISH-' in df.sys_name: 
        return 'satellite'
    if 'Super Zone' in df.sys_name: 
        return 'superzone'
    else: 
        return 'cable'


paths = glob.glob(r'inputs/*.xlsx')

wb_list = []
for excel_path in paths: 
    print(f'accessing wb {excel_path}')

    wb = openpyxl.load_workbook(excel_path)

    names = wb.sheetnames
    names = [name for name in names if bad_name[0] not in name]
    names = [name for name in names if bad_name[1] not in name]
    
    wb_sheets = []
    for name in names: 
        print(f'\t cleaning sheet {name}')
        sheet_digit_pair = []
        for s in name.split(): 
            if s.isdigit(): 
                sheet_digit_pair.append(s)
            
        df = pd.read_excel(excel_path,
                sheet_name=name)
        #format df 
        df = df.replace(r'\n','',regex=True)
        df = df.fillna(r'_')

        #set columns
        df.columns = df.iloc[6,:]

        #set system type
        df['system_type'] = df.iloc[3,0]
        df[['sys_media','sys_name']] = df.system_type.str.split(r'/', expand=True)
        df[['sys_name','sys_code']] = df.sys_name.str.split('(', expand=True)
        df['sys_name'] = df.sys_name.str[:-5]
        df['sys_code'] = df.sys_code.str[:-1]

        df['sys_media'] = df.apply(sys_media, axis=1)
        df['sys_type'] = df.apply(sys_type, axis=1)

        df = df.iloc[7:-1,:] #drops the 'total' row at bottom of frame and garbage rows at top of frame
        
        #format columns
        df.columns = [x.lower() for x in df.columns.to_list()]
        df.columns = [x.replace(' ','_') for x in df.columns.to_list()]
        df.columns = [x.replace('(','') for x in df.columns.to_list()]
        df.columns = [x.replace(')','') for x in df.columns.to_list()]
        df = df.drop('_', axis=1)

        df['zone_int'] = sheet_digit_pair[0]
        df['dist_sth'] =  sheet_digit_pair[1]
        
        #write individual sheet to csv
        #df.to_csv(rf'{name}.csv', index=False) #writes index
        print(df.head(5))

        wb_sheets.append(df)
    for _ in wb_sheets: 
        wb_list.append(_)

print('concating...')
af = pd.concat(wb_list, axis=0)

"""
0   zip_code                                            43142 non-null  int64  
 1   in_district                                         43142 non-null  object 
 2   city                                                43142 non-null  object 
 3   state                                               43142 non-null  object 
 4   county                                              43142 non-null  object 
 5   countycablepenetrationnsi                           43142 non-null  float64
 6   rawcensus_hhin_zip                                  43142 non-null  int64  
 7   rawl2_votersin_zip                                  43142 non-null  int64  
 8   system_subscribersues                               43142 non-null  int64  
 9   total_censushh_in_zipstouchedby_system              43142 non-null  int64  
 10  systempenetrationofcensus_homes                     43142 non-null  float64
 11  percentage_ofdistrict_votersin_zip_codebased_on_l2  43142 non-null  float64
 12  estimateddistrict_votersin_zip_codebased_on_l2      43142 non-null  int64  
 13  systempenetrationof_l2_voters                       43142 non-null  float64
 14  estimatedsystem_censushh_in_zip                     23186 non-null  float64
 15  estimated_census_hh_in_districtbased_on_l2          43142 non-null  float64
 16  system_type                                         43142 non-null  object 
 17  zone_int                                            43142 non-null  int64  
 18  dist_sth                                            43142 non-null  int64  
 19  est._census_hh_in_district_based_on_l2              19956 non-null  float64
"""

af = af.rename(columns={'countycablepenetrationnsi':'county_pene_rate',
    'rawcensus_hhin_zip':'zip_census_hh_in_zip',
    'rawl2_votersin_zip':'zip_l2_voters_in_zip',
    'system_subscribersues':'sys_subscribers',
    'total_censushh_in_zipstouchedby_system':'sys_census_hh_zip_pene', #zip_census_hh_in_zip sum
    'systempenetrationofcensus_homes':'sys_census_hh_pene_rate', #sys_subscribers / sys_census_hh_zip_pene
    'percentage_ofdistrict_votersin_zip_codebased_on_l2':'dist_voters_indist_rate', #l2 provided
    'estimateddistrict_votersin_zip_codebased_on_l2':'dist_voters_indist_est', #zip_census_hh_in_zip * dist_voters_indist_rate
    'systempenetrationof_l2_voters':'dist_sys_voters_pen', #sys_census_hh_pene_rate * dist_voters_indist_est
    'estimatedsystem_censushh_in_zip':'distcen_hh_inzip', 
    'estimated_census_hh_in_districtbased_on_l2':'discen_hh_inzip',
    'est._census_hh_in_district_based_on_l2':'discen_hh_inzip_i',
    })

af['distcen_hh_indist'] = af['discen_hh_inzip'] + af['discen_hh_inzip_i']
af.drop(['discen_hh_inzip_i','discen_hh_inzip'], axis=1, inplace=True)

af.sort_index(axis=1, inplace=True)

print('writing...')
af.to_csv(r'outputs/zip_tv_compile.csv', index=False)


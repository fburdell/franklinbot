from api import Postgres

import numpy as np
import pandas as pd

class House:

    def __init__(self, district):
        self.district = district
        self.dos_prex = ['muniname', 'municode1', 'munidesc2', 'munidesc2', 'munidesc2']
        self.precincts = self.precincts()

    def gv(self):
        """general votes"""
        bo = Postgres('main')
        query = f"SELECT * FROM general_votes WHERE sthousedist = {self.district}"
        df = pd.read_sql_query(query, con=bo.pg_con())
        return df

    def pv(self):
        """primary votes"""
        bo = Postgres('main')
        query = f"SELECT * FROM primary_votes WHERE sthousedist = {self.district}"
        df = pd.read_sql_query(query, con=bo.pg_con())
        return df

    def pturn(self):
        """primary turnout counts"""
        df = self.pv()
        df = df.fillna("_")
        df = df[(df['officecode'] == "USP") | (df['officecode'] == "GOV")]
        # need to figure out how to calculate without reliance
        # on prez and gov years for off year elections
        # 2015 and 2017 are present in sql tables
        df = pd.pivot_table(df,
            index=['year','county', 'muniname', 'municode1', 'munidesc1', 'municode2', 'munidesc2'],
            columns=['officecode', 'party'],
            values='votecount',
            aggfunc=np.sum)
        df = df.groupby(level=1, axis=1).max()
        return df

    def dem_pturn(self):
        """primary turnout counts"""
        df = self.pv()
        df = df.fillna("_")
        df = df[df['party'] == "DEM"]
        df = df[(df['officecode'] == "USP") | (df['officecode'] == "GOV")]
        df = pd.pivot_table(df,
            index=['year','county', 'muniname', 'municode1', 'munidesc1', 'municode2', 'munidesc2'],
            columns=['lastname', 'officecode', 'party'],
            values='votecount',
            aggfunc=np.sum)
        df = df.groupby(level=1, axis=1).sum()
        df = df.max(axis=1)
        return df

    def gturn(self):
        """general turnout counts"""
        df = self.gv()
        df = df.fillna("_")
        df = pd.pivot_table(df,
            index=['year','county', 'muniname', 'municode1', 'munidesc1', 'municode2', 'munidesc2'],
            columns=['lastname', 'officecode', 'party'],
            values='votecount',
            aggfunc=np.sum)
        df = df.groupby(level=1, axis=1).sum()
        df = df.max(axis=1)
        return df

    def reg(self):
        """historical registration"""
        bo = Postgres('main')

        query = f"SELECT * FROM registration WHERE sthousedist = {self.district}"

        df = pd.read_sql_query(query, con=bo.pg_con())
        df.loc[:,"muniname":'munidesc2'] = df.loc[:,"muniname":'munidesc2'].fillna("_")

        ix = pd.MultiIndex.from_frame(df[['year', 'county', 'muniname', 'municode1', 'munidesc1', 'municode2', 'munidesc2']])
        df = df[['dem', 'rep', 'oth']]
        df.index = ix
        df = df.sum(axis=1)

        return df

    def partisan_reg(self):
        """historical registration"""
        bo = Postgres('main')

        query = f"SELECT * FROM registration WHERE sthousedist = {self.district}"

        df = pd.read_sql_query(query, con=bo.pg_con())
        df.loc[:,"muniname":'munidesc2'] = df.loc[:,"muniname":'munidesc2'].fillna("_")

        ix = pd.MultiIndex.from_frame(df[['year', 'county', 'muniname', 'municode1', 'munidesc1', 'municode2', 'munidesc2']])
        df = df[['dem', 'rep', 'oth']]
        df.index = ix
        return df


    def ex_reg(self):
        """historical registration"""
        bo = Postgres('main')

        query = f"SELECT * FROM registration WHERE sthousedist = {self.district}"

        df = pd.read_sql_query(query, con=bo.pg_con())
        df.loc[:,"muniname":'munidesc2'] = df.loc[:,"muniname":'munidesc2'].fillna("_")

        ix = pd.MultiIndex.from_frame(df[['year', 'county', 'muniname', 'municode1', 'munidesc1', 'municode2', 'munidesc2']])
        df = df[['dem', 'rep', 'oth']]
        df.index = ix

        return df

    def pturnp(self):
        """primaty turnout rate"""
        re = self.reg()
        pv = self.pturn()
        pv = pd.Series(pv.DEM)
        df = pv.div(re)
        return df

    def gturnp(self):
        """general turnout rate"""
        re = self.reg()
        gv = self.gturn()
        df = gv.div(re)
        df.rename('gturnp', inplace=True)
        df = df.loc[~df.index.duplicated(keep='last')]
        return df

    def pturnp_sums(self):
        re = self.reg()
        re = re.groupby(level=0).sum()
        pv = self.pturn()
        pv = pv.groupby(level=0).sum().iloc[:,0]


        df = pv.div(re)
        df.dropna(inplace=True)

        return df

    def gturnp_sums(self):
        """turnout generator"""
        re = self.reg()
        re = re.groupby(level=0).sum()
        gv = self.gturn()
        gv = gv.groupby(level=0).sum()
        gv.rename('gturnp_sum', inplace=True)
        print(gv)
        #df = df.loc[~df.index.duplicated(keep='last')]
        #df = df.dropna()
        return gv 

    def pvc(self):
        """primary vote counts"""
        df = self.pv()

        df = df[df.party == 'DEM']
        df = df.fillna('_')
        df = pd.pivot_table(df,
            index=['year','county', 'muniname', 'municode1', 'munidesc1', 'municode2', 'munidesc2'],
            columns=['officecode', 'lastname'],
            values='votecount',
            aggfunc=np.sum)

        return df

    def dem_ball(self):
        """general vote performance"""
        df = self.gv()

        df = df[(df['party'] == 'DEM') | (df['party'] == 'REP')]
        df = df.fillna("_")
        df = pd.pivot_table(df,
            index=['year','county', 'muniname', 'municode1', 'munidesc1', 'municode2', 'munidesc2'],
            columns=['officecode', 'party'],
            values='votecount',
            aggfunc=np.sum)

        dems = df.loc[:,(slice(None), 'DEM')]

        return dems
    

    def gvp(self):
        """general vote performance"""
        df = self.gv()

        df = df[(df['party'] == 'DEM') | (df['party'] == 'REP')]
        df = df.fillna("_")
        df = pd.pivot_table(df,
            index=['year','county', 'muniname', 'municode1', 'munidesc1', 'municode2', 'munidesc2'],
            columns=['officecode', 'party'],
            values='votecount',
            aggfunc=np.sum)

        dems = df.loc[:,(slice(None), 'DEM')]
        dems = dems.droplevel(level=1, axis=1)
        ballot = df.groupby(level=0, axis=1).sum()
        
        df = dems.div(ballot)

        return df

    def gvp_totals(self):
        df = self.gv()

        df = df[(df['party'] == 'DEM') | (df['party'] == 'REP')]
        df = df.fillna("_")
        df = pd.pivot_table(df,
            index=['year','county', 'muniname', 'municode1', 'munidesc1', 'municode2', 'munidesc2'],
            columns=['officecode', 'party'],
            values='votecount',
            aggfunc=np.sum)

        dems = df.loc[:,(slice(None), 'DEM')]
        ballot = df.groupby(level=0, axis=1).sum()

        dems = dems.groupby(level=0).sum()
        ballot = ballot.groupby(level=0).sum()

        df = dems.div(ballot)
        df = df.replace({0:np.nan})

        df = df.mean(axis=1)

        return df

    def ballotAverage(self):
        df = self.gvp()
        df = df.mean(axis=1)
        df.rename('ba', inplace=True)
        df = df.loc[~df.index.duplicated(keep='last')]
        return df

    def dpi(self):
        """historical dpi"""
        df = self.ballotAverage()
        df.rename('dpi', inplace=True)
        gf = df.groupby(level=[1,2,3,4,5,6], axis=0).apply(
            lambda x: x.ewm(span=3, adjust=False).mean())
        gf = gf[~gf.index.duplicated(keep='last')]
        return gf

    def zip_tpd(self):
        """zip turnout performance dpi"""
        dpi = self.dpi()
        bal = self.ballotAverage()
        tur = self.gturnp()
        df = pd.concat([dpi, bal, tur], axis=1)
        df = df.dropna()
        df = df[(df.dpi < 1) & (df.gturnp < 1) & (df.ba < 1)]
        return df

    def plot_dpi(self):
        s = self.gvp_totals()
        print(s)

        exp3 = s.ewm(span=3, adjust=False).mean()
        exp4 = s.ewm(span=4, adjust=False).mean()
        exp5 = s.ewm(span=5, adjust=False).mean()

        import matplotlib.pyplot as plt

        plt.plot(s.index, exp3*100, dashes=[3,3], label='3YR DPI (most accurate)')
        plt.plot(s.index, exp4*100, dashes=[9,9], label='4YR DPI')
        plt.plot(s.index, exp5*100, dashes=[27,27], label='5YR DPI')

        plt.grid(True)
        plt.xticks(range(2000,2022,2))
        plt.title(f"HD{self.district} Democratic Performance Index \n Over Time")
        plt.legend()

        plt.savefig(rf"G:\My Drive\frank\hdcc_frank\program\data\outputs\plot_dpi\{self.district}.png")
        plt.clf()

    def plot_tpd_dpi(self):
        df = self.zip_tpd()

        import seaborn as sns
        import matplotlib.pyplot as plt

        plt.axvline(.5)
        plt.axhline(.5)

        points = plt.scatter(df.gturnp, df.ba, c=df.dpi, cmap='coolwarm_r')

        cbar = plt.colorbar(points)
        cbar.set_label('DPI')

        sns.regplot(x='gturnp', y='ba', data=df,
            scatter=False, color=".1")

        plt.xlabel('Turnout % \nfor Precinct')
        plt.ylabel('Democratic Ballot Average % \nfor Precinct \nfor Year')
        plt.title(f'Legislative District {int(self.district)} \n \
        Precinct Turnout v. Precinct Democratic Averages & DPI')

        plt.tight_layout()

        plt.savefig(rf'G:\My Drive\frank\hdcc_frank\program\data\outputs\plot_turnbaadpi\{int(self.district)}.png')
        points.figure.clear()

    def plot_tpd_years(self):
        df = self.zip_tpd()

        import seaborn as sns
        import matplotlib.pyplot as plt
        df.reset_index(inplace=True)

        df = df[df.year >= 2008]

        plt.axvline(.5)
        plt.axhline(.5)

        ax = sns.lmplot(x='gturnp', y='ba', data=df,
            hue='year',
            legend=True,
            lowess=True)

        ax.fig.subplots_adjust(top=.9)

        ax.set(xlabel='Precinct Turnout %',
            ylabel='Precinct Ballot Average %',
            title=f'HD{int(self.district)} \n Turnout v Performance')

        ax.savefig(rf"G:\My Drive\frank\hdcc_frank\program\data\outputs\plot_turnbaa\{int(self.district)}.png")

    def plot_turnout(self):

        def poli_cat(s):
                midterm_years = [2002, 2006, 2010, 2014, 2018]
                presidential_years = [2000, 2004, 2008, 2012, 2016]
                if s['year'].astype('int') in presidential_years:
                    return 'Presidential'
                if s['year'].astype('int') in midterm_years:
                    return 'Midterm'
                else:
                    return 'If you are seeing this, Frank fucked up'

        turn = self.gturnp_sums()
        turn = pd.DataFrame(turn).reset_index()
        turn['Election Type'] = pd.DataFrame(turn).reset_index().apply(poli_cat, axis=1)

        import matplotlib.pyplot as plt
        import seaborn as sns

        ax = sns.lmplot(x='year', y='gturnp_sum', data=turn,
            col='Election Type',
            legend=True,
            lowess=True)

        ax.fig.subplots_adjust(top=.9)
        ax.set(xlabel='Year',
            ylabel='% Turnout',
            title=f"HD{int(self.district)} Turnout \n Over Time",
            xticks=np.arange(2000,2022,2))

        ax.savefig(rf'/home/frank/Insync/frank@pahdcc.com/Google Drive/frank/hdcc_frank/program/data/projects/env/outputs/plot_turnout/{self.district}.png')
        plt.close()

    def lr_turn_primary(self):
        presidential_years = [2000, 2004, 2008, 2012, 2016]

        t = self.pturnp_sums()
        t = t[t.index.isin(presidential_years)]
        t = t.ewm(span=3, adjust=False).mean()
        t = t.reset_index().values

        from sklearn.linear_model import LinearRegression
        import numpy as np

        x = t[:,0]
        y = t[:,1]
        z = np.array(2021)

        li = LinearRegression()

        li.fit(x[:,np.newaxis],y[:,np.newaxis])
        pred = li.predict(z.reshape(-1,1))

        return pred[0][0]

    def lr_turn_general(self):

        presidential_years = [2000, 2004, 2008, 2012, 2016]

        t = self.gturnp_sums()
        t = t[t.index.isin(presidential_years)]

        t = t.ewm(span=3, adjust=False).mean()
        t = t.reset_index().values

        from sklearn.linear_model import LinearRegression
        import numpy as np

        x = t[:,0]
        y = t[:,1]
        z = np.array(2020)

        li = LinearRegression()

        li.fit(x[:,np.newaxis],y[:,np.newaxis])
        pred = li.predict(z.reshape(-1,1))

        return pred[0][0]

    def primary_win(self):
        pred = self.lr_turn_primary()
        reg = self.reg()
        reg = reg.groupby(level=0).sum()
        reg = reg[reg.index==2018].values[0]

        return int(((reg*pred) / 2) + 1)

    def general_win(self):
        pred = self.lr_turn_general()
        reg = self.reg()
        reg = reg.groupby(level=0).sum()
        reg = reg[reg.index==2018].values[0]

        return int(((reg*pred) / 2) + 1)

    def precincts(self):
        gv = self.gvp()
        gv = gv.loc[2018]
        precincts = gv.index.unique()
        return precincts

    def campaign_dump_all(self, etype):

        etype = str(etype) + " "

        path = "G:\\My Drive\\2020 Cycle\\Campaigns\\"

        #zf = pd.read_csv(r'..\franksenv\temp\demographics.csv', index_col='HD')

        dist_int = int(self.district)
        dist_str = str(self.district)

        di = House(self.district)

        af = di.gv()
        af = af[af.year > 2010]
        af.to_csv(rf"{path}{etype}{dist_str}\Data\General Votes.csv", index=False)

        bf = di.pv()
        bf = bf[bf.year > 2010]
        bf.to_csv(rf"{path}{etype}{dist_str}\Data\Primary Votes.csv", index=False)

        reg = di.ex_reg()
        reg = reg.reset_index()
        reg = reg[reg.year > 2010]
        reg.to_csv(rf"{path}{etype}{dist_str}\Data\Registration.csv")

        dpi = di.zip_tpd()
        dpi = dpi.rename({'dpi':'DPI', 'gturnp':'General Turnout Rate', 'ba':'Ballot Average'})
        dpi = dpi.rename(columns={dpi.columns[0]:"DPI",
            dpi.columns[1]:"Ballot Average",
            dpi.columns[2]:"General Turnout Rate"})

        dpi.to_csv(rf"{path}{etype}{dist_str}\Data\DPI, Ballot Average, Turnout Rate.csv")


"""
#demographics portion of the export
#need demographics file again
        yf = zf[zf.index == dist_int]
        xf = (zf - zf.min()) / (zf.max() - zf.min())
        xf = xf[xf.index == dist_int]
        wf = pd.concat([yf, xf], axis=0)
        wf = wf.T
        wf = wf.rename(columns={wf.columns[0]:"Percent of District",
            wf.columns[1]:"Percentile of District"})
        wf = wf.rename(index={wf.index[0]:"<$50K/annum",
            wf.index[1]:"<>$50K100K/annum",
            wf.index[2]:"<>$100K200K/annum",
            wf.index[3]:">$200K/annum",
            })

        wf.to_csv(rf"{path}{etype}{dist_str}\Data\Demographics.csv")
"""

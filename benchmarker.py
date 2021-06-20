import datetime
import math
from api import Phoenix, Postgres
from franklinbot import FranklinBot 

import pandas as pd
import numpy as np


class Benchmarker(FranklinBot, Phoenix, Postgres): 

    def __init__(self, hd): 
        FranklinBot.__init__(self)
        Phoenix.__init__(self) 
        Postgres.__init__(self, 'main')

        self.db_main = Postgres('main')

        self.hd = hd

        self.field_nums = self.get_field_math() #dynamic_field_match.sql
        self.turnout = self.field_nums[0]
        self.base = self.field_nums[1]

        self.operations = self.get_all_attempts() #dynamic_get_all_attempts.sql
        self.survey_responses = self.operations[0]
        self.contacts = self.operations[1]

        self.phone_shift = 100
        self.text_shift = 250
        self.lit_shift = 70
        self.relational_shift = 25

        self.phone_contact = .1
        self.text_contact = .1
        self.lit_contact = 0
        self.relational_contact = .5

        self.passes = 1

        self.attach_file = f'outputs/HD{self.hd} {self.today} Target Checks.csv'
        self.attach_readme = f'README.md'

        self.attach_pers_work = f'outputs/HD{self.hd} {self.today} Persuasion Work.csv'
        self.attach_turn_work = f'outputs/HD{self.hd} {self.today} Turnout Work.csv'
        self.attach_field_report = f'outputs/HD{self.hd} {self.today} Field Report.txt'

        self.recipients = self.get_recipients()

        self.emails_master =  ['desks@pahdcc.com', 'friedman@dlcc.org', 'pereira@dlcc.org', 'dickinson@dlcc.org', 'pietrzyk@dlcc.org']
        self.emails_district = self.get_recipients()
        self.emails_all = self.emails_district + self.emails_master

    def target(self, target):
        #self.target = self.get_target()

        pass
        
    def get_recipients(self): 
         df = pd.read_sql(rf"select * from fmails where hd = '{self.hd}'", con=self.db_main.sa_con())
         return df.emails[0]

    def get_target(self, target): 
        #target='persuasion'|target='turnout'
        q = open('queries/dynamic_target.sql', 'r+').read()
        s = self.get_df(q.format(hd=self.hd, target=target))
        return s.vanid 

    def get_all_attempts(self):
        q = open('queries/dynamic_all_attempts.sql', 'r+').read()
        af = self.get_df(q.format(hd=self.hd))
        return af[af.type_contact == 'sr'], af[af.type_contact == 'co'] #survey response & contacts for all of 2020 in two frames

    def get_field_math(self): 
        q = open('queries/dynamic_field_math.sql', 'r+').read()
        df = self.get_df(q.format(hd=self.hd))
        return df.turnout[0], df.base[0]

    def get_win_number(self): 
        return (self.turnout * .5) + 1

    def get_wn(self): 
        return (self.turnout * .52)

    def get_uncanvassed_targets(self, target): 
        #vanids = self.target[~self.target.isin(self.operations)] 

        t = self.get_target(target) #full t 
        t = t[~t.isin(self.contacts.vanid)]
        t = t[~t.isin(self.survey_responses.vanid)]
        return t #series of vanids

    def get_ix_remainder(self, end, rem): 
        return [end - datetime.timedelta(days=x) for x in range(0,rem,7)]

    def get_ix_pers_rem(self): 
        return self.get_ix_remainder(self.persuasion_end,self.persuasion_remaining) 

    def get_ix_turn_rem(self): 
        return self.get_ix_remainder(self.turnout_end,self.turnout_remaining) 

    def get_ix_capture_rem(self): 
        return self.get_ix_remainder(self.capture_end,self.turnout_remaining) 

    def avg(self,s): 
        return [round(x * 1/len(s),2) for x in s]

    def get_ix_work_avg(self, rem): 
        ones = np.ones(len(rem))#looking for a self.get_ix_THING_rem() func
        return self.avg(ones)#returning avg work array (.2,.2,.2,.2,.2)

    def get_work_lin_space(self, ix_rem): 
        return np.linspace(1,len(ix_rem),len(ix_rem))
        
    def get_ix_work_lin_scale(self, s):
        for i in range(1,500): 
            sa = self.reducer_f(i, s)
            if sa.sum() < self.passes: 
                return sa
            else: 
                pass

    def reducer_f(self, i, s): 
        s = np.array([round(x/i,2) for x in s])
        #s[0] = s[1] #0th s usually ends at 0, set 0th to 1st val
        return s

    def set_work_frame(self, ix_phase_rem, t): #ie get_ix_pers_rem()

        
        if t == 'persuasion':
            dates = ix_phase_rem
            work = self.get_ix_work_lin_scale(
                    self.get_work_lin_space(
                        dates
                        )
                    )
            dates = dates[::-1]
            df = pd.DataFrame({'dates':dates,'work':work})
            pers_uncan = self.get_uncanvassed_targets('persuasion')
            df['persuasion_remaining'] = self.set_mode_work(pers_uncan, df.work)
            df['pers_shift_phone'] = self.set_mode_shifts(df.persuasion_remaining, self.phone_shift)
            df['pers_shift_text'] = self.set_mode_shifts(df.persuasion_remaining, self.text_shift)
            df['pers_shift_lit'] = self.set_mode_shifts(df.persuasion_remaining, self.lit_shift)
            df['pers_shift_relational'] = self.set_mode_shifts(df.persuasion_remaining, self.relational_shift)
            return df
        elif t == 'turnout': 
            dates = ix_phase_rem
            work = self.get_ix_work_lin_scale(
                    self.get_work_lin_space(
                        dates
                        )
                    )
            dates = dates[::-1]
            df = pd.DataFrame({'dates':dates,'work':work})
            turn_uncan = self.get_uncanvassed_targets('turnout')
            df['turnout_remaining'] = self.set_mode_work(turn_uncan, df.work)
            df['turn_shift_phone'] = self.set_mode_shifts(df.turnout_remaining, self.phone_shift)
            df['turn_shift_text'] = self.set_mode_shifts(df.turnout_remaining, self.text_shift)
            df['turn_shift_lit'] = self.set_mode_shifts(df.turnout_remaining, self.lit_shift)
            df['turn_shift_relational'] = self.set_mode_shifts(df.turnout_remaining, self.relational_shift)
            return df
        else: 
            'no t'


    def set_id_est(self, s_mode_goal, e_contact_rate): 
        return s_mode_goal * e_contact_rate

    def set_mode_work(self, uncanvassed, s_work):
        return [math.ceil(x) for x in (len(uncanvassed) * s_work)]

    def set_mode_shifts(self, s_work_goal, mode_shift): 
        return [math.ceil(x) for x in (s_work_goal / mode_shift)]

    def drop_benchmark_table(self): 
        q = open(r'queries/dynamic_drop_dist_benchmark.sql', 'r+').read()

        self.exe(q.format(hd=self.hd))


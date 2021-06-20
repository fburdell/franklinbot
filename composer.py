import math
from api import Phoenix, Postgres
from franklinbot import FranklinBot 
from benchmarker import Benchmarker

import datetime

import pandas as pd
import numpy as np

class Composer(Benchmarker):

    def __init__(self, hd):
        Benchmarker.__init__(self, hd)
    
    def name_space_example(self):
        return self.phone_shift

    def write_daily(self):

        def in_targ(canvassed, target):
            out = [x for x in canvassed if x not in target]
            inn = [x for x in canvassed if x in target]
            return [len(out), len(inn)]

        q_target = open(r'queries/dynamic_target.sql').read()
        vote_def = math.ceil(self.get_wn() - self.base)

        target = self.get_df(q_target.format(hd=self.hd))
        turnout = target[target.target == 't']
        persuasion = target[target.target == 'p']
    
        dvca = self.survey_responses.append(self.contacts)
        dvca['dt'] = [pd.to_datetime(x.replace(tzinfo=None)) for x in dvca.dt]
        week_prior = pd.to_datetime(self.week_prior)

        hdcc = dvca[(dvca.campaign == 'hdcc') & (dvca.dt > week_prior)]
        coord = dvca[(dvca.campaign == 'coord') & (dvca.dt > week_prior)]

        
        hdcc_t_out, hdcc_t_in = in_targ(set(hdcc.vanid.values), set(turnout.vanid.values))
        coord_t_out, coord_t_in = in_targ(set(coord.vanid.values), set(turnout.vanid.values))

        hdcc_p_out, hdcc_p_in = in_targ(set(hdcc.vanid.values), set(persuasion.vanid.values))
        coord_p_out, coord_p_in = in_targ(set(coord.vanid.values), set(persuasion.vanid.values))

        #rolling assessment in last week of work done
        inpers = hdcc_p_in + coord_p_in
        inturn = hdcc_t_in + coord_t_in
        inhdcc =  hdcc_p_in + hdcc_t_in 
        incoord =  coord_p_in + coord_t_in

        intarget =  inpers + inturn
        incampaign = inhdcc + incoord

        tp = len(turnout) + len(persuasion)

        report = f""",turnout_target_size,persuasion_target_size,total_attempts,in_turnout_attempts,in_persuasion_attempts 
HD{self.hd} Campaign,{len(turnout)},{len(persuasion)},{len(hdcc)},{hdcc_t_in},{hdcc_p_in}
Coordinated DVCA,na,na,{len(coord)},{coord_t_in},{coord_p_in}
Totals,na,na,{len(hdcc) + len(coord)},{inturn},{inpers}


HD{self.hd} Campaign Percents,na,na,,{   hdcc_t_in/ intarget}, {   hdcc_p_in/intarget }
Coordinated DVCA Percents,na,na,,{   coord_t_in/intarget },{   coord_p_in/intarget }
Total Percents,na,na,{ intarget/intarget},{ inturn/ intarget },{ inpers /intarget }
"""

        with open(rf'outputs/HD{self.hd} {self.today} Target Checks.csv', 'w') as f: 
            f.write(report)
            f.close()

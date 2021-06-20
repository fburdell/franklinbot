delete from demspahdcc.commons.hdcc_persuasion_unsurpressed_target where dist_sth = '030'; --drops yesterdays target from table

insert into demspahdcc.commons.hdcc_persuasion_unsurpressed_target (dist_sth, vanid) --puts todays target into table
   
select vf.dist_sth, targ.vanid --selects target for placement

from( --targ
--begin query

select * from ( --seg_a
select vanid
from demspahdcc.commons.voter_file
where 
  party = 'R'
  and ts_partisan_score > .4
  and ts_turnout_score > .5
) seg_a --gop scored

union all 

select * from ( --seg_b
select vanid
from demspahdcc.commons.voter_file
where 
  party = 'NPA'
  and ts_partisan_score > .1
  and ts_turnout_score > .5
) seg_b --npa scored

union all 

select * from (  --seg_c
select vanid
from demspahdcc.commons.voter_file
where 
  party = 'D'
  and ts_partisan_score < .8
  and ts_turnout_score > .5
) seg_c --conserv dem

union all 

select vanid from ( --seg_d
select vanid, dist_sth, p_2014, g_2014, p_2016,  g_2016, p_2018, g_2018 from ( 
select vanid as vanid, dist_sth, p_2014, g_2014, p_2016,  g_2016, p_2018, g_2018
from demspahdcc.commons.voter_file v
where 
  party = 'R' --add independents here
  and gender = 'F'
  and (p_2014 <> -1
  or p_2016 <> -1
  or p_2018 <> -1
  or g_2014 <> -1
  or g_2016 <> -1
  or g_2018 <> -1)
  ) seg_e_i
where
  ( p_2014 + g_2014 + p_2016 +  g_2016  ) < 2
  and ( p_2018 + g_2018) = 2 
) seg_d --f gop surge

union all 

select * from ( --seg_f
select vanid
from demspahdcc.commons.voter_file vf
left join democrats.blueprint_pa_numeric.scores_numeric sc on vf.personid = sc.person_id
where sc.civis_2020_partisanship > .1 and vf.clarity_turnout_score > .5
and vf.party <> 'D'
) seg_e --civis add

union all

select * from (  --seg_e
select vanid
from demspahdcc.commons.voter_file
where 
  ethnicity <> 'W'
  and party <> 'D'
  and ts_turnout_score is null
  and ts_partisan_score is null
) seg_f --unscored non white non dem

union all

select * from (  --seg_g
select vanid
from demspahdcc.commons.voter_file temp_vf
left join democrats.blueprint_pa.scores sc on temp_vf.personid = sc.person_id
where 
  party <> 'D'
  and gender = 'F'
  and ((ts_partisan_score is null) or
  (sc.civis_2020_partisanship is null))
) seg_g --unscored non-democratic women

--add in households with kids
--young child stuff 

--new independent registrations

--how do we add in old people

)targ

left join --allow for some flexibility and extra features when needed
    demspahdcc.commons.voter_file vf on targ.vanid = vf.vanid

where --suppressions and localization
  safe_cast(vf.dist_sth as int64) in (30) --check if hd in tiered hd

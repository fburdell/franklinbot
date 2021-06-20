delete from demspahdcc.commons.hdcc_persuasion_unsurpressed_target where dist_sth = '097';

insert into demspahdcc.commons.hdcc_persuasion_unsurpressed_target (dist_sth, vanid)

select vf.dist_sth, targ.vanid --selects target for placement

from( --targ

select vanid from ( --seg_d
select vanid, dist_sth, p_2014, g_2014, p_2016,  g_2016, p_2018, g_2018 from ( 
select vanid as vanid, dist_sth, p_2014, g_2014, p_2016,  g_2016, p_2018, g_2018
from demspahdcc.commons.voter_file v
where 
  party = 'R'
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
) seg_e --f gop surge

union all 

select * from (  --seg_e
select vanid
from demspahdcc.commons.voter_file
where 
  ethnicity <> 'W'
  and party <> 'D'
  and ts_turnout_score is null
  and ts_partisan_score is null
) seg_d --unscored non white non dem

union all 

select * from ( --seg_f
select vanid
from demspahdcc.commons.voter_file vf
left join democrats.blueprint_pa_numeric.scores_numeric sc on vf.personid = sc.person_id
where sc.civis_2020_partisanship > .1 and sc.civis_2020_partisanship < .75
and vf.party <> 'D'
) seg_f --civis add

union all

select * from (  --seg_g
select vanid
from demspahdcc.commons.voter_file temp_vf
left join democrats.blueprint_pa.scores sc on temp_vf.personid = sc.person_id
where 
  party <> 'D'
  and gender = 'F'
  and ((ts_turnout_score is null
  and ts_partisan_score is null) or
  (sc.civis_2020_partisanship is null))
) seg_d --unscored non-democratic women


)targ

left join 
    demspahdcc.commons.voter_file vf on targ.vanid = vf.vanid

where 
  safe_cast(vf.dist_sth as int64) in (97) --check if hd in tiered hd

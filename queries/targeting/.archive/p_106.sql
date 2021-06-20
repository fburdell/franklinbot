delete from demspahdcc.commons.hdcc_persuasion_unsurpressed_target where dist_sth = '106';

insert into demspahdcc.commons.hdcc_persuasion_unsurpressed_target (dist_sth, vanid)

select vf.dist_sth, targ.vanid --selects target for placement

from( --targ

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


)targ

left join 
    demspahdcc.commons.voter_file vf on targ.vanid = vf.vanid

where 
  vf.dist_sth in ('106') --check if hd in tiered hd

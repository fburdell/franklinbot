
SELECT
  distinct ad.address,ad.city,ad.state_code,ad.zip,
  concat(ap.first_name, ' ' ,ap.last_name) name, --NAME GRAB AND CONCAT
  vf.vanid,
  case when rand() > .9 then 1 else null end as is_control, --SET RANDOMIZATION FOR CONTROL
  case when rand() <= .9 then 1 else null end as is_target --SET RANDOMIZATION FOR TARGET

from
  demspahdcc.commons.voter_file vf 
left join 
  demspahdcc.commons.early_vote ev on vf.vanid = ev.a_vanid
left join 
  democrats.voter_file_pa.person_address pa on vf.personid = pa.person_id
left join 
  democrats.voter_file_pa.address ad on pa.address_id = ad.address_id
left join 
  democrats.analytics_pa.person ap on vf.personid = ap.person_id
  
where 
  vf.party = 'D'
  and vf.clarity_turnout_score > .4
  and vf.clarity_turnout_score < .9
  and vf.civis_partisan_score > .5
  and safe_cast(vf.dist_sth as int64) in (select o1 from demspahdcc.commons.tiers) --must be in tier
  and safe_cast(vf.vanid as string) not in (select myv_id from demspahdcc.commons.tpab_ids) --cannot be in id already pulled
  and safe_cast(vf.vanid as int64) not in (select safe_cast(a_vanid as int64) from demspahdcc.commons.early_vote) --cannot have already requested ev

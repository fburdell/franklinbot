select distinct vanid, dist_sth, 'p' as target from demspahdcc.commons.hdcc_persuasion_target

where 
  safe_cast(dist_sth as int64) in (select o1 from demspahdcc.commons.tiers union all select o2 from demspahdcc.commons.tiers union all select d1 from demspahdcc.commons.tiers)

union all

select distinct vanid, dist_sth, 't' as target from demspahdcc.commons.hdcc_turnout_target

where 
  safe_cast(dist_sth as int64) in (select o1 from demspahdcc.commons.tiers union all select o2 from demspahdcc.commons.tiers union all select d1 from demspahdcc.commons.tiers)

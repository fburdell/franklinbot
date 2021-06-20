select distinct vanid, dist_sth from demspahdcc.archive.hdcc_persuasion_unsupressed_target_200729

where 
  safe_cast(dist_sth as int64) in (select o1 from demspahdcc.commons.tiers union all select o2 from demspahdcc.commons.tiers union all select o3 from demspahdcc.commons.tiers union all select d1 from demspahdcc.commons.tiers union all select d2 from demspahdcc.commons.tiers union all select d3 from demspahdcc.commons.tiers)

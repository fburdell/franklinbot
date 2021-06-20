select distinct vanid, safe_cast(dist_sth as int64) as dist_sth from demspahdcc.commons.hdcc_persuasion_unsurpressed_target
where safe_cast(dist_sth as int64) in (select o1 from demspahdcc.commons.tiers)

union all 


select distinct vanid, safe_cast(dist_sth as int64) as dist_sth from demspahdcc.archive.hdcc_persuasion_unsupressed_target_200729
where safe_cast(dist_sth as int64) in (select o1 from demspahdcc.commons.tiers)

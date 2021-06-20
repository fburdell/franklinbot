select distinct ca.vanid, ca.dist_sth as dist_sth, vf.party, dt, safe_cast(ca.type_attempt as int64) as type_attempt

from demspahdcc.commons.hdcc_canvassed ca
left join demspahdcc.commons.voter_file vf on ca.vanid = vf.vanid

where 
  dt > "2020-6-9" 
  and safe_cast(ca.dist_sth as int64) in (select o1 from demspahdcc.commons.tiers union all select o2 from demspahdcc.commons.tiers union all select o3 from demspahdcc.commons.tiers union all select d1 from demspahdcc.commons.tiers union all select d2 from demspahdcc.commons.tiers union all select d3 from demspahdcc.commons.tiers)

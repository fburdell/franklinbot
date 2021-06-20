select vanid, dt, result, safe_cast(dist_sth as int64) as dist_sth from ( 
select distinct vanid, dt, result, dist_sth from demspahdcc.commons.coordinated_canvassed where type_contact = 'sr'

union all 

select distinct vanid, dt, result, dist_sth from demspahdcc.commons.hdcc_canvassed where type_contact = 'sr') can


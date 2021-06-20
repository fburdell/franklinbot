
select 
dist_sth, 
count( case when id_type = 'sth' then 1 else null end ) as sth_ids, 
count( case when (result = '1' or result = '2') and id_type = 'sth' then 1 else null end ) as sth_ids_pos,
count( case when id_type = 'pus' then 1 else null end ) as potus_ids, 
count( case when (result = '1' or result = '2') and id_type = 'pus' then 1 else null end ) as potus_ids_pos,
count( case when result is not null then 1 else null end ) as attempt_count


from demspahdcc.commons.coordinated_canvassed

group by dist_sth

order by attempt_count desc

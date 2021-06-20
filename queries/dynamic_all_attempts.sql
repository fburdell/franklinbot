select distinct contacts_contact_id, dt, result,vanid, type_contact, type_attempt, 'hdcc' as campaign

from demspahdcc.commons.hdcc_canvassed

where dist_sth = "{hd}"

and dt > "2020-06-03"

union all

select distinct contacts_contact_id, dt, result, vanid, type_contact, type_attempt, 'coord' as campaign

from demspahdcc.commons.coordinated_canvassed

where dist_sth = "{hd}"

and dt > "2020-06-03"

select * from ( 

select 
    ev.myv_van_id
from 
    demspahdcc.public.early_vote ev
where 
    (ev.civis_partisan_score > .75
    or ev.civis_ideology_score > .75
    or ev.ts_partisan_Score > .75
    or ev.dlcc_support_score > 75)

union all 

select 
    ev.myv_van_id
from 
    demspahdcc.public.early_vote ev
where 
    ev.party <> 'R'

union all 

select 
    ev.myv_van_id
from 
    demspahdcc.public.early_vote ev
left join 
    (select * from demspahdcc.commons.hdcc_canvassed where type_contact = 'sr') hc on ev.myv_van_id = hc.vanid
where 
    hc.result = '1'
    or hc.result = '2'


) t 

left join demspahdcc.commons.voter_file vf on t.myv_van_id = vf.vanid

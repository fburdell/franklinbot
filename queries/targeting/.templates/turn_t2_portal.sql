select targ.vanid
from demspahdcc.commons.hdcc_turnout_target targ
left join demspahdcc.commons.voter_file vf on targ.vanid = vf.vanid

where 

    --tier
    ((vf.dlcc_support_score > 75
    or vf.civis_partisan_score >.75
    or vf.ts_partisan_score > .75)

    and 
    
    ((vf.dlcc_turnout_score <= 50 and 
        vf.dlcc_turnout_score > 30) 
    or (vf.clarity_turnout_score <= .50 and
        vf.clarity_turnout_score > .30)
    or (vf.ts_turnout_score <= .50 and
        vf.ts_turnout_score > .30))

    and not 

    (vf.dlcc_support_score <= 20
    or vf.civis_partisan_score <= .20 
    or vf.ts_partisan_score <= .20)

    )


  --suppress 1s and 2s from the msq list
  and targ.vanid not in (select distinct vanid from demspahdcc.commons.hdcc_canvassed where type_contact = 'sr' and dt > "2020-01-01" and substr(result,1) = '1' or substr(result,1) = '2' or substr(result,1) = '5' or substr(result,1) = '4') 



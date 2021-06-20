select targ.vanid
from demspahdcc.commons.hdcc_persuasion_target targ
left join demspahdcc.commons.voter_file vf on targ.vanid = vf.vanid

where 

    --tier
    (((vf.dlcc_support_score <= 55
    and vf.dlcc_support_score > 45) 
    or 
    (vf.civis_partisan_score <= .55
    and vf.civis_partisan_score > .45)
    or 
    (vf.ts_partisan_score <= .55
    and vf.ts_partisan_score > .45))
    and 
    (vf.dlcc_turnout_score > 70
    or vf.clarity_turnout_score > .70
    or vf.ts_turnout_score > .70)
    and not
    (vf.dlcc_support_score <= 20
    or vf.civis_partisan_score <= .20 
    or vf.ts_partisan_score <= .20))


  --suppress 1s and 2s from the msq list
  and targ.vanid not in (select distinct vanid from demspahdcc.commons.hdcc_canvassed where type_contact = 'sr' and dt > "2020-01-01" and substr(result,1) = '1' or substr(result,1) = '2' or substr(result,1) = '5' or substr(result,1) = '4') 



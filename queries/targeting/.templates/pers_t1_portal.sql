select targ.vanid
from demspahdcc.commons.hdcc_persuasion_target targ
left join demspahdcc.commons.voter_file vf on targ.vanid = vf.vanid

where 

    --scored
    ((((vf.dlcc_support_score < 75
    and vf.dlcc_support_score > 55) 
    or 
    (vf.civis_partisan_score < .75
    and vf.civis_partisan_score > .55)
    or 
    (vf.ts_partisan_score < .75
    and vf.ts_partisan_score > .55))
    and 
    (vf.dlcc_turnout_score > 70
    or vf.clarity_turnout_score > .70
    or vf.ts_turnout_score > .70)
    and not --drops possibility of less than voters
    (vf.dlcc_support_score <= 20
    or vf.civis_partisan_score <= .20 
    or vf.ts_partisan_score <= .20))

    or --non-support scored nonwhite nondems with some voting history

    (vf.ethnicity <> 'W'
    and vf.party <> 'D'

    and (vf.civis_partisan_score is null
    or vf.ts_partisan_score is null 
    or vf.dlcc_support_score is null)  

    and (vf.g_2016 = 1
    or vf.g_2017 = 1
    or vf.g_2018 = 1 
    or vf.g_2019 = 1))

    or --non-turnout scored voters with some partisan scoring and voting behavior

    ((vf.clarity_turnout_score is null 
    or vf.dlcc_turnout_score is null 
    or vf.ts_turnout_score is null)
    and 
    (civis_partisan_score > .5
    or ts_partisan_score > .50
    or dlcc_support_score > 50 ) 
    and 
    (g_2016 + g_2017 + g_2018 + g_2019) >= 3))


  --suppress 1s and 2s from the msq list
  and targ.vanid not in (select distinct vanid from demspahdcc.commons.hdcc_canvassed where type_contact = 'sr' and dt > "2020-01-01" and substr(result,1) = '1' or substr(result,1) = '2' or substr(result,1) = '5' or substr(result,1) = '4') 



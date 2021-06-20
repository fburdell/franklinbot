select targ.vanid
from demspahdcc.commons.hdcc_turnout_target targ
left join demspahdcc.commons.voter_file vf on targ.vanid = vf.vanid
left join democrats.voter_file_pa.registration re on vf.vanid = re.myv_van_id

where 

        (((vf.dlcc_support_score > 75
        or vf.civis_partisan_score >.75
        or vf.ts_partisan_score > .75)

        and 
        
        ((vf.dlcc_turnout_score < 70 and 
            vf.dlcc_turnout_score > 50) 
        or (vf.clarity_turnout_score < .70 and
            vf.clarity_turnout_score > .50)
        or (vf.ts_turnout_score < .70 and
            vf.ts_turnout_score > .50))
        
        and not 

        (vf.dlcc_support_score <= 20
        or vf.civis_partisan_score <= .20 
        or vf.ts_partisan_score <= .20)

        )

    or --unscored supp nonwhite dem/npa

        (ethnicity <> 'W' 
        and (party = 'D' or party = 'NPA')

        and (civis_partisan_score is null
        or ts_partisan_score is null 
        or dlcc_support_score is null)  

        and (g_2016 = 1
        or g_2017 = 1
        or g_2018 = 1 
        or g_2019 = 1))

    or --unscored turn nonwhite dem/npa

        ((vf.clarity_turnout_score is null 
        or vf.dlcc_turnout_score is null 
        or vf.ts_turnout_score is null)
        and 
        (civis_partisan_score > .8
        or ts_partisan_score > 80
        or dlcc_support_score > .8 ) 
        and 
        (((g_2016 + g_2017 + g_2018 + g_2019) <= 3)
        and (g_2016 + g_2017 + g_2018 + g_2019) >= 1))

    or  --new registrants
        
        re.registration_date > '2016-01-01'
        and vf.party = 'D' or vf.party = 'NPA'
    
        )

  --suppress 1s and 2s from the msq list
  and targ.vanid not in (select distinct vanid from demspahdcc.commons.hdcc_canvassed where type_contact = 'sr' and dt > "2020-01-01" and substr(result,1) = '1' or substr(result,1) = '2' or substr(result,1) = '5' or substr(result,1) = '4') 



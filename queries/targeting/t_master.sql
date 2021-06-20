
select vf.dist_sth, targ.vanid

from(

--scoring 
select * from ( 
select vanid 
from demspahdcc.commons.voter_file vf
where 
--allow for all combinations of 
--turnout and support scoring
--insofar as threshholds are met
--party naive

    ((vf.dlcc_support_score > 75
    or vf.civis_partisan_score >.75
    or vf.ts_partisan_score > .75)

    and 
    
    ((vf.dlcc_turnout_score < 70 and 
        vf.dlcc_turnout_score > 30) 
    or (vf.clarity_turnout_score < .70 and
        vf.clarity_turnout_score > .30)
    or (vf.ts_turnout_score < .70 and
        vf.ts_turnout_score > .30)))
   
   and not
   
   (vf.dlcc_support_score <= 20
   or vf.civis_partisan_score <= .20 
   or vf.ts_partisan_score <= .20)
   
   
) 

union all 

--unscored supp nonwhite dem/npa
select * from (
select vanid
from demspahdcc.commons.voter_file
where 
  ethnicity <> 'W' 
  and (party = 'D' or party = 'NPA')

  and (civis_partisan_score is null
  or ts_partisan_score is null 
  or dlcc_support_score is null)  

  and (g_2016 = 1
  or g_2017 = 1
  or g_2018 = 1 
  or g_2019 = 1)
) ndnw

union all 

--unscored turnout nonwhite dem/npa
select * from ( 
select vanid
from demspahdcc.commons.voter_file vf
where
  (vf.clarity_turnout_score is null 
  or vf.dlcc_turnout_score is null 
  or vf.ts_turnout_score is null)
  and 
  (civis_partisan_score > .8
  or ts_partisan_score > 80
  or dlcc_support_score > .8 ) 
  and 
  (((g_2016 + g_2017 + g_2018 + g_2019) <= 3)
    and (g_2016 + g_2017 + g_2018 + g_2019) >= 1)
) 

union all 

--new reg
select * from (
select vanid
from demspahdcc.commons.voter_file vf
left join democrats.voter_file_pa.registration re on vf.vanid = re.myv_van_id
where 
  re.registration_date > '2016-01-01'
  and vf.party = 'D' or vf.party = 'NPA'
) nr

)targ


left join 
    demspahdcc.commons.voter_file vf on targ.vanid = vf.vanid

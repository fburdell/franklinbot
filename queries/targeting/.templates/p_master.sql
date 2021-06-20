select vf.dist_sth, targ.vanid 

-- main targ
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

    (((vf.dlcc_support_score < 75
    and vf.dlcc_support_score > 30) 
     
    or (vf.civis_partisan_score < .75
    and vf.civis_partisan_score > .3)
    
    or (vf.ts_partisan_score < .75
    and vf.ts_partisan_score > .3))

    and 

    (vf.dlcc_turnout_score > 70
    or vf.clarity_turnout_score > .70
    or vf.ts_turnout_score > .70))

    and not 

    (vf.dlcc_support_score <= 20
    or vf.civis_partisan_score <= .20
    or vf.ts_partisan_score <= .20)
 
    )

union all 

--college scored
select * from ( 
select vanid
from demspahdcc.commons.voter_file vf
left join democrats.scores_pa.all_scores_2020 sc on vf.personid = sc.person_id
where 
  sc.dnc_2020_college_graduate > .75

  and (vf.dlcc_support_score > 50
    or vf.ts_partisan_score > .5
    or vf.civis_partisan_score > .5)

  and vf.party <> 'D'

  and ( vf.g_2019 + vf.g_2018 + vf.g_2017 + vf.g_2016 ) >= 2
) coll

union all 

--non-support scored
select * from (
select vanid
from demspahdcc.commons.voter_file
where 
  ethnicity <> 'W'
  and party <> 'D'

  and (civis_partisan_score is null
  or ts_partisan_score is null 
  or dlcc_support_score is null)  

  and (g_2016 = 1
  or g_2017 = 1
  or g_2018 = 1 
  or g_2019 = 1)
) ndnw 

union all 

-- non turnout scored 
select * from ( 
select vanid
from demspahdcc.commons.voter_file vf
where
  (vf.clarity_turnout_score is null 
  or vf.dlcc_turnout_score is null 
  or vf.ts_turnout_score is null)
  and 
  (civis_partisan_score > .5
  or ts_partisan_score > 50
  or dlcc_support_score > .5 ) 
  and 
  (g_2016 + g_2017 + g_2018 + g_2019) >= 3
) 

union all 

--f gop surge
select * from (--f gop surge
select vanid 
from demspahdcc.commons.voter_file v
where 
  party = 'R'

  and (v.dlcc_support_score > 40
    or v.ts_partisan_score > .4
    or v.civis_partisan_score > .4)

  and gender = 'F'

  and ( g_2014 + p_2014 + p_2015 + g_2015 + p_2016 + g_2016 ) <= 2

  and ( p_2017 + g_2017 + p_2018 + g_2018 + p_2019 + g_2019 ) > 2

) gopfs

)targ

left join 
    demspahdcc.commons.voter_file vf on targ.vanid = vf.vanid
    


select 
distinct ca.vanid, 
vf.party, 
vf.dlcc_support_score, 
vf.dlcc_turnout_score,
vf.g_2018,
vf.g_2016

from demspahdcc.commons.hdcc_canvassed ca 
left join demspahdcc.commons.voter_file vf on ca.vanid = vf.vanid

where dt > '2020-06-02'

and ca.dist_sth = '028'

and ca.vanid not in (select distinct vanid 

from demspahdcc.commons.hdcc_persuasion_unsurpressed_target

where dist_sth = '028'
)

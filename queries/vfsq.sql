SELECT
  sr.myv_van_id,
  --substr(srs.survey_response_name, 1,1) as survey_response_name,
  case when substr(srs.survey_response_name, 1,1) = '1' then 1 
  when substr(srs.survey_response_name, 1,1) = '2' then .75 
  when substr(srs.survey_response_name, 1,1) = '3' then .5 
  when substr(srs.survey_response_name, 1,1) = '4' then .25 
  when substr(srs.survey_response_name, 1,1) = '5' then 0 
  else null end as response18,


  var.prob_persuasion,
  vf.*

FROM
  demspahdcc.vansync.contacts_survey_responses_myv sr
LEFT JOIN
  demspahdcc.vansync.survey_responses srs ON sr.survey_response_id = srs.survey_response_id
LEFT JOIN 
  demspahdcc.commons.hdcc_partisan_var_score var on sr.myv_van_id = var.vanid
left join 
  demspahdcc.commons.voter_file_temp vf on var.vanid = vf.vanid



WHERE
  sr.survey_question_id = '293677'

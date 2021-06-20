
select 
  dist_sth,
  count(case when result = '1' or result = '2' then 1 else null end) as positive_ids,
  round(count(case when result = '1' or result = '2' then 1 else null end) / nullif(count(case when type_contact = 'sr' then 1 else null end), 0), 3) as positive_id_rate,
  count(case when type_contact = 'sr' then 1 else null end) as total_ids,
  count(case when type_contact = 'co' then 1 else null end) as total_attempts, 
  count(case when result = '3' then 1 else null end) as undecided_ids, 
  count(case when result = '4' or result = '5' then 1 else null end) as negative_ids,
  count(case when result = 'Phone' then 1 else null end) as phone_attempts, 
  count(case when result = 'Walk' then 1 else null end) as walk_attempts, 
  count(case when result = 'SMS Text' then 1 else null end) as text_attempts,
  count(case when result = 'Auto Dial' then 1 else null end) as autodialer_attempts, 
  count(case when result = 'Relational Call' then 1 else null end) as relational_call_attempts, 
  count(case when result = 'Relational Text' then 1 else null end) as relational_text_attempts
  
from demspahdcc.commons.hdcc_canvassed 
where dt > "{date}"
group by dist_sth 
order by total_attempts desc

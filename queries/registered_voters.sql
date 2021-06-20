SELECT 
--INDEX
   ap.myv_van_id as vanid,
  
--DEMOGRAPHICS
   ml.min_max_scaler(ap.age_combined) over() as age,

--GENDER&PARTY   
   case when ap.gender_combined = 'F' then 1 else null end as is_female,
   case when ap.gender_combined = 'M' then 1 else null end as is_male,
   case when ap.party_id = '1' then 1 else null end as is_dem,
   case when ap.party_id = '2' then 1 else null end as is_gop,
   case when (ap.party_id <> '1' 
      and ap.party_id <> '2') then 1 else null end as is_npa,
     
--SCORE
    ml.min_max_scaler(sc.ts_tsmart_partisan_score) over() as partisan_score     
     

from
    democrats.blueprint_pa_numeric.vote_history_numeric vh
left join
    democrats.blueprint_pa_numeric.census_numeric ce on vh.person_id = ce.person_id
left join
    democrats.blueprint_pa_numeric.electionbase_numeric eb on vh.person_id = eb.person_id
left join
    democrats.analytics_pa.person ap on vh.person_id = ap.person_id
left join
    democrats.reference_geo.national_census_tracts ct on ap.census_tract_2010 = ct.census_tract
left join
    democrats.blueprint_pa.scores sc on vh.person_id = sc.person_id


where
    ap.reg_voter_flag = true
    --and safe_cast(ap.state_house_district_latest as int64) in (select d1 from demspahdcc.commons.targets union all select o1 from demspahdcc.commons.targets)

limit
    {end}

offset
    {start}

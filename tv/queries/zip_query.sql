
#standardSQL
select
  zip_d.* 
from (

select 
  zip_c.*,
  de.zip_avg_gender_f as avg_gender_f,
  de.zip_avg_gender_m as avg_gender_m,
  de.zip_approx_median_age as median_age,
  de.zip_avg_ethnicity_w as avg_eth_w,
  de.zip_avg_ethnicity_b as avg_eth_b,
  de.zip_avg_ethnicity_a as avg_eth_a,
  de.zip_avg_party_reg_3_way_democratic as avg_dem,
  de.zip_avg_party_reg_3_way_republican as avg_rep
from (

select 
  zip_b.*, 
  sc.zip_avg_dnc_2020_dem_party_support as avg_dnc_dem_score 
from (

select 
  zip_a.*, 
  vh.zip_avg_even_general_votes as avg_even_gen_votes 
from ( 

SELECT 
   --INDEX
    ap.voting_zip as zip_a,ap.state_house_district_latest as dist_sth,ap.state_senate_district_latest as dist_sts,ap.us_cong_district_latest as dist_usc,
   
    --SCORE
    avg(sc.ts_tsmart_partisan_score) as avg_ts_partisan_score, 
    avg(sc.ts_tsmart_presidential_general_turnout_score) AS avg_ts_turnout_score,
    avg(sc.civis_2020_partisanship) as avg_civis_partisan_score,
    avg(sc_a.civis_2020_ideology_liberal) as avg_civis_ideology_score,
    avg(sc_a.clarity_2020_turnout) as avg_clarity_turnout_score,
    avg(var.prob_persuasion) as avg_partisan_variance_score,
    
    --VOTING HISTORY
    count(case when vh.g_2008_voted_ordinal = 1 then 1 else null end) as sum_vote_g_2008,
    count(case when vh.g_2010_voted_ordinal = 1 then 1 else null end) as sum_vote_g_2010,
    count(case when vh.g_2012_voted_ordinal = 1 then 1 else null end) as sum_vote_g_2012,
    count(case when vh.g_2014_voted_ordinal = 1 then 1 else null end) as sum_vote_g_2014,
    count(case when vh.g_2016_voted_ordinal = 1 then 1 else null end) as sum_vote_g_2016,
    count(case when vh.g_2018_voted_ordinal = 1 then 1 else null end) as sum_vote_g_2018,
    count(case when vh.p_2008_voted_ordinal = 1 then 1 else null end) as sum_vote_p_2008,
    count(case when vh.p_2010_voted_ordinal = 1 then 1 else null end) as sum_vote_p_2010,
    count(case when vh.p_2012_voted_ordinal = 1 then 1 else null end) as sum_vote_p_2012,
    count(case when vh.p_2014_voted_ordinal = 1 then 1 else null end) as sum_vote_p_2014,
    count(case when vh.p_2016_voted_ordinal = 1 then 1 else null end) as sum_vote_p_2016,
    count(case when vh.p_2018_voted_ordinal = 1 then 1 else null end) as sum_vote_p_2018,
    
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
left join 
    democrats.scores_pa.all_scores_2020 sc_a on vh.person_id = sc_a.person_id
left join 
    demspahdcc.commons.hdcc_partisan_var_score var on ap.myv_van_id = var.vanid

where
    ap.reg_voter_flag = true
    and ap.voting_zip is not null

group by zip_a,dist_sth,dist_sts,dist_usc
order by zip_a desc
) zip_a

left join democrats.blueprint_pa_rollups.zip_vote_history vh on zip_a.zip_a = vh.voting_zip 
) zip_b

left join democrats.blueprint_pa_rollups.zip_scores sc on zip_b.zip_a = sc.voting_zip
) zip_c

left join democrats.blueprint_pa_rollups.zip_demographics de on zip_c.zip_a = de.voting_zip
) zip_d

select vanid, 'p' as target

from demspahdcc.commons.hdcc_persuasion_target

where dist_sth = "{hd}"

union all 


select vanid, 'p' as target

from demspahdcc.commons.hdcc_persuasion_target_districts

where dist_sth = "{hd}"

union all 


select vanid, 't' as target

from demspahdcc.commons.hdcc_turnout_target

where dist_sth = "{hd}"

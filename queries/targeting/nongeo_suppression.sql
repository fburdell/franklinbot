

select targ.vanid
from demspahdcc.commons.hdcc_canvassed targ
left join demspahdcc.commons.voter_file vf on targ.vanid = vf.vanid

where 
    --phones as only sq drop since 
    --no one is leaving messages 
    --and messages are 0 effect
    targ.vanid not in 
        (select distinct vanid 
            from demspahdcc.commons.hdcc_canvassed 
            where type_contact = 'sr' 
            and result is not null 
            and cast(dt as datetime) > cast(date_sub(current_date(), interval 14 day) as datetime))

    --suppress not 3s from the msq li
    or targ.vanid not in 
        (select distinct vanid 
            from demspahdcc.commons.hdcc_canvassed 
            where type_contact = 'sr' 
            and dt > "2020-01-01" 
            and substr(result,1) = '1' or substr(result,1) = '2' or substr(result,1) = '4' or substr(result,1) = '5' )

    --xuppress refused etc
    --dropping ia's for the geo suppression, not for the non geo suppression
    --going to assume accuracy of data and suppress instead against 2020-06-09
    or targ.vanid not in
        (select myv_van_id 
            from demspahdcc.vansync.contacts_contacts_myv 
            where datetime_canvassed > "2020-06-09"
            --nothome inaccessible deaceased moved canvassed  litdrop donotwalk
            and result_id in ('1', '3', '4', '5', '14', '21', '23') 
            --walk paidwalk relcanvass commcanvass distcanvass 
            and contact_type_id in ('2','36', '145', '139', '141'))

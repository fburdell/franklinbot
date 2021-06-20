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
            and substr(result,1) = '1' or substr(result,1) = '2'  or substr(result,1) = '4' or substr(result,1) = '5')

    or targ.vanid not in
        (select myv_van_id 
            from demspahdcc.vansync.contacts_contacts_myv 
            where datetime_canvassed > "2020-06-09"
            and (
                --walk, commcanvass, distcanvass, relcanvass
                (contact_type_id in ('2','139','141','145')) -- if result in person
                    --nh, rf, ia, dc, mv, vacant, canvassed, lit dropped,
                    and (result_id in ('1', '2', '3','4', '5', '10','14','21')) 
                or 
                --phone, robocall, autodial, sms, relsms, relcall, distsms, distcall
                (contact_type_id in ('1','4','19','37','132','133','142','143')) -- if result in virtual
                    --not a real number, will return false, want to lit drop / talk to anyone that we've talked to virtually
                    and (result_id in ('999')) 
                )) 


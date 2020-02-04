set hive.exec.parallel=TRUE;
set hive.exec.reducers.max=25;
set hive.exec.reducers.bytes.per.reducer=100;
set hive.exec.max.dynamic.partitions.pernode=100; 
set hive.cli.print.header=true;
set hive.optimize.sort.dynamic.partition=true;
set mapred.job.queue.name=root.pdigpprd_q1;
set mapred.red.tasks=100; 
set mapreduce.job.reduces=100;
set hive.vectorized.execution.enabled = true;
set hive.vectorized.execution.reduce.enabled = true;
set hive.cbo.enable=true;
set hive.compute.query.using.stats=true;
set hive.stats.fetch.column.stats=true;
set hive.stats.fetch.partition.stats=true;
set hive.cli.print.header=true;
select 
    J.fed_tax_id as prov_tax_id,
    A.HSC_id,
    A.srvc_setting_typ_id,
    case when A.srvc_setting_typ_id =1 then "Inpatient" 
         when A.srvc_setting_typ_id =3 then "Outpatient Facility"   end as srvc_setting_typ,     -- put filter at the end for 1 and 3 only
    A.HSC_STS_TYP_ID,
    from_unixtime(UNIX_TIMESTAMP(A.creat_dttm,'yyyy-mm-dd'),'yyyy-mm-dd'),
    AA.srvc_desc_typ_id,
    case when srvc_desc_typ_id= 1 then "Standard"
         when srvc_desc_typ_id in  (2,3) then " Urgent" end as srvc_desc_typ,   
    from_unixtime(UNIX_TIMESTAMP(C.DECN_RNDR_DTTM,'yyyy-mm-dd'),'yyyy-mm-dd'),
    C.DECN_OTCOME_TYP_ID,   
    C.DECN_SUB_TYP_ID,  
    C.DECN_RSN_TYP_ID,
    case when C.DECN_OTCOME_TYP_ID =1 then 'Approved'
         when C.DECN_OTCOME_TYP_ID =2 then 'Denied'
         when C.DECN_OTCOME_TYP_ID =4 then 'Cancelled'
         when C.DECN_OTCOME_TYP_ID is NULL and A.HSC_STS_TYP_ID in (1,3,5) and from_unixtime(UNIX_TIMESTAMP(C.DECN_RNDR_DTTM,'yyyy-mm-dd'),'yyyy-mm-dd') is NULL then 'Pending' end as outcome,
    trim(D.REF_DESC) as outcome_reason,   
    case when F.ref_desc ='Medicare' then 'M&R'
        when F.ref_desc ='Commercial' then 'E&I'
        when F.ref_desc ='Medicaid' then 'C&S'
        when F.ref_desc ='Both Medicare and Medicaid' then 'C&S'
        when F.ref_desc ='TPA' then 'C&S'
        when F.ref_desc ='CSP Medicaid Enrolled/External Medicare Enrolled' then 'C&S'
        when F.ref_desc ='Champus' then 'Others'
        else NULL end as LOB,
    G.REF_DESC as Service_category,
    ((day(i.tat_pt_dttm)*24*60*60+HOUR ( i.tat_pt_dttm)*60*60+MINUTE ( i.tat_pt_dttm)*60+ SECOND ( i.tat_pt_dttm)) - (day(H.tat_pt_dttm)*24*60*60+HOUR ( H.tat_pt_dttm)*60*60+MINUTE ( H.tat_pt_dttm)*60+ SECOND ( H.tat_pt_dttm)) )/60/60 as TAT_hrs
    
    
From 
    df2_hsr_lakeprd.HSC_SNAPSHOT A
left join df2_hsr_lakeprd.HSC_FACL_SNAPSHOT AA
    on A.HSC_ID = AA.HSC_ID
left join df2_hsr_lakeprd.hsc_srvc_snapshot K
    on A.HSC_ID = K.HSC_ID
left join df2_hsr_lakeprd.HSC_PROV_Snapshot J
    on A.HSC_ID = J.HSC_ID and K.srvc_prov_seq_nbr = J.prov_seq_nbr

left join ( select hsc_id, max(DECN_SEQ_NBR) as DECN_SEQ_NBR from df2_hsr_lakeprd.HSC_SRVC_DECN_SNAPSHOT 
                            where from_unixtime(UNIX_TIMESTAMP(DECN_RNDR_DTTM,'yyyy-mm-dd'),'yyyy-mm-dd') >= '2018-01-01' group by hsc_id ) B 
    on A.HSC_ID = B.HSC_ID    -- need to add decn_seq_nbr? NO as only 1 hsc id
    
left join df2_hsr_lakeprd.HSC_SRVC_DECN_SNAPSHOT C 
    on A.hsc_id = c.hsc_id and B.DECN_SEQ_NBR = C.DECN_SEQ_NBR and C.srvc_seq_nbr = K.srvc_seq_nbr

inner join df2_hsr_lakeprd.REF D
    on (C.DECN_RSN_TYP_ID = D.REF_CD AND D.REF_NM ='decisionReasonType')

left join df2_hsr_lakeprd.HSC_MBR_COV_SNAPSHOT E
    on A.hsc_id= E.hsc_id and A.mbr_cov_seq_nbr = E.mbr_cov_seq_nbr

inner join df2_hsr_lakeprd.ref F
    on (E.prdct_catgy_cd=F.ref_cd and  F.REF_NM ='productCategoryType')

inner join  df2_hsr_lakeprd.REF G
    on (AA.SRVC_DTL_TYP_ID = G.REF_CD AND G.REF_NM ='serviceDetailType')

left join ( select hsc_id,tat_pt_dttm,srvc_seq_nbr from df2_hsr_lakeprd.HSC_SRVC_TAT_PT_SNAPSHOT WHERE  tat_pt_typ_id ='01') H
    on A.HSC_ID = H.HSC_ID and C.srvc_seq_nbr=H.srvc_seq_nbr
left join ( select hsc_id,tat_pt_dttm,srvc_seq_nbr from df2_hsr_lakeprd.HSC_SRVC_TAT_PT_SNAPSHOT WHERE  tat_pt_typ_id ='04') I
    on A.HSC_ID = I.HSC_ID and C.srvc_seq_nbr=I.srvc_seq_nbr

WHERE 
    from_unixtime(UNIX_TIMESTAMP(A.creat_dttm,'yyyy-mm-dd'),'yyyy-mm-dd') >= from_unixtime(UNIX_TIMESTAMP(E.cov_eff_dt,'yyyy-mm-dd'),'yyyy-mm-dd') and from_unixtime(UNIX_TIMESTAMP(A.creat_dttm,'yyyy-mm-dd'),'yyyy-mm-dd')<= from_unixtime(UNIX_TIMESTAMP(E.cov_end_dt,'yyyy-mm-dd'),'yyyy-mm-dd')        
    and E.COV_TYP_ID = 'M' 
    and from_unixtime(UNIX_TIMESTAMP(A.creat_dttm,'yyyy-mm-dd'),'yyyy-mm-dd') between'2018-01-01' and '2019-06-30'
    and A.srvc_setting_typ_id in (1,3)
    and  J.fed_tax_id  in ('111871039','111888924','141338470','141340100','141349558','150552726','113613997','223636986','61603195','61562701','141347717','133964321','111635088','111639818','112050523','113565450','111352310','111704595','113438973','131740104')
    --and C.hsc_id='126595048'
group by J.fed_tax_id,A.HSC_id,A.srvc_setting_typ_id,A.srvc_setting_typ_id,A.HSC_STS_TYP_ID,from_unixtime(UNIX_TIMESTAMP(A.creat_dttm,'yyyy-mm-dd'),'yyyy-mm-dd'),AA.srvc_desc_typ_id,from_unixtime(UNIX_TIMESTAMP(C.DECN_RNDR_DTTM,'yyyy-mm-dd'),'yyyy-mm-dd'),
C.DECN_OTCOME_TYP_ID,C.DECN_SUB_TYP_ID,C.DECN_RSN_TYP_ID,C.DECN_OTCOME_TYP_ID,A.HSC_STS_TYP_ID,from_unixtime(UNIX_TIMESTAMP(C.DECN_RNDR_DTTM,'yyyy-mm-dd'),'yyyy-mm-dd'),D.REF_DESC,F.REF_DESC,G.REF_DESC,H.TAT_PT_DTTM,I.TAT_PT_DTTM

---------------------------------------------------------------------------------------------------------

--I/p and OPF without Service    SRVC_SETTING= 1 and 3
union

select 
    K.fed_tax_id as prov_tax_id,
    A.HSC_id,
    A.srvc_setting_typ_id,
    case when srvc_setting_typ_id =1 then "Inpatient" 
         when srvc_setting_typ_id =3 then "Outpatient Facility" end as srvc_setting_typ,     -- put filter at the end for 1 and 3 only
    A.HSC_STS_TYP_ID,
    from_unixtime(UNIX_TIMESTAMP(A.creat_dttm,'yyyy-mm-dd'),'yyyy-mm-dd'),
    AA.srvc_desc_typ_id,
    case when srvc_desc_typ_id= 1 then "Standard"
         when srvc_desc_typ_id in  (2,3) then " Urgent" end as srvc_desc_typ,   
    from_unixtime(UNIX_TIMESTAMP(C.DECN_RNDR_DTTM,'yyyy-mm-dd'),'yyyy-mm-dd'),
    C.DECN_OTCOME_TYP_ID,   
    C.DECN_SUB_TYP_ID,  
    C.DECN_RSN_TYP_ID,
    case when C.DECN_OTCOME_TYP_ID =1 then 'Approved'
         when C.DECN_OTCOME_TYP_ID =2 then 'Denied'
         when C.DECN_OTCOME_TYP_ID =4 then 'Cancelled'
         when C.DECN_OTCOME_TYP_ID is NULL and A.HSC_STS_TYP_ID in (1,3,5) and from_unixtime(UNIX_TIMESTAMP(C.DECN_RNDR_DTTM,'yyyy-mm-dd'),'yyyy-mm-dd') is NULL then 'Pending' end as outcome,
    trim(D.REF_DESC) as outcome_reason,   
    case when F.ref_desc ='Medicare' then 'M&R'
        when F.ref_desc ='Commercial' then 'E&I'
        when F.ref_desc ='Medicaid' then 'C&S'
        when F.ref_desc ='Both Medicare and Medicaid' then 'C&S'
        when F.ref_desc ='TPA' then 'C&S'
        when F.ref_desc ='CSP Medicaid Enrolled/External Medicare Enrolled' then 'C&S'
        when F.ref_desc ='Champus' then 'Others'
        else NULL end as LOB,
    G.REF_DESC as Service_category,
    ((day(i.tat_pt_dttm)*24*60*60+HOUR ( i.tat_pt_dttm)*60*60+MINUTE ( i.tat_pt_dttm)*60+ SECOND ( i.tat_pt_dttm)) - (day(H.tat_pt_dttm)*24*60*60+HOUR ( H.tat_pt_dttm)*60*60+MINUTE ( H.tat_pt_dttm)*60+ SECOND ( H.tat_pt_dttm)) )/60/60 as TAT_hrs
    
From 
    df2_hsr_lakeprd.HSC_SNAPSHOT A
left join df2_hsr_lakeprd.HSC_FACL_SNAPSHOT AA
    on A.HSC_ID = AA.HSC_ID

left join ( select hsc_id, max(DECN_SEQ_NBR) as DECN_SEQ_NBR from df2_hsr_lakeprd.HSC_FACL_DECN_SNAPSHOT 
                            where from_unixtime(UNIX_TIMESTAMP(DECN_RNDR_DTTM,'yyyy-mm-dd'),'yyyy-mm-dd') >= '2018-01-01'  group by hsc_id ) B 
    on A.HSC_ID = B.HSC_ID    -- based on AA or A
    
left join df2_hsr_lakeprd.HSC_FACL_DECN_SNAPSHOT C 
    on A.hsc_id = c.hsc_id and B.DECN_SEQ_NBR = C.DECN_SEQ_NBR
    
left join ( select * from df2_hsr_lakeprd.HSC_PROV_ROLE_SNAPSHOT where prov_role_typ_id='FA') J
    on A.hsc_id= j.HSC_ID
left join df2_hsr_lakeprd.HSC_PROV_Snapshot K
    on A.HSC_ID = K.HSC_ID and J.prov_seq_nbr= K.prov_seq_nbr
    
inner join df2_hsr_lakeprd.REF D
    on (C.DECN_RSN_TYP_ID = D.REF_CD AND D.REF_NM ='decisionReasonType')
left join df2_hsr_lakeprd.HSC_MBR_COV_SNAPSHOT E
    on A.hsc_id= E.hsc_id and A.mbr_cov_seq_nbr = E.mbr_cov_seq_nbr
inner join df2_hsr_lakeprd.ref F
    on (E.prdct_catgy_cd=F.ref_cd and  F.REF_NM ='productCategoryType')
inner join  df2_hsr_lakeprd.REF G
    on (AA.SRVC_DTL_TYP_ID = G.REF_CD AND G.REF_NM ='serviceDetailType')
left join ( select hsc_id,tat_pt_dttm from df2_hsr_lakeprd.HSC_FACL_TAT_PT_SNAPSHOT WHERE  tat_pt_typ_id ='01') H
    on A.HSC_ID = H.HSC_ID 
left join ( select hsc_id,tat_pt_dttm from df2_hsr_lakeprd.HSC_FACL_TAT_PT_SNAPSHOT WHERE  tat_pt_typ_id ='04') I
    on A.HSC_ID = I.HSC_ID 

WHERE 
   from_unixtime(UNIX_TIMESTAMP(A.creat_dttm,'yyyy-mm-dd'),'yyyy-mm-dd') >= from_unixtime(UNIX_TIMESTAMP(E.cov_eff_dt,'yyyy-mm-dd'),'yyyy-mm-dd') and from_unixtime(UNIX_TIMESTAMP(A.creat_dttm,'yyyy-mm-dd'),'yyyy-mm-dd')<= from_unixtime(UNIX_TIMESTAMP(E.cov_end_dt,'yyyy-mm-dd'),'yyyy-mm-dd')         
    and E.COV_TYP_ID = 'M'
    and from_unixtime(UNIX_TIMESTAMP(A.creat_dttm,'yyyy-mm-dd'),'yyyy-mm-dd') between'2018-01-01' and '2019-06-30'
    and A.srvc_setting_typ_id in ('1','3')
    and  K.fed_tax_id  in ('111871039','111888924','141338470','141340100','141349558','150552726','113613997','223636986','61603195','61562701','141347717','133964321','111635088','111639818','112050523','113565450','111352310','111704595','113438973','131740104')
    --and C.hsc_id='126595048'
group by K.fed_tax_id,A.HSC_id,A.srvc_setting_typ_id,A.srvc_setting_typ_id,A.HSC_STS_TYP_ID,from_unixtime(UNIX_TIMESTAMP(A.creat_dttm,'yyyy-mm-dd'),'yyyy-mm-dd'),AA.srvc_desc_typ_id,from_unixtime(UNIX_TIMESTAMP(C.DECN_RNDR_DTTM,'yyyy-mm-dd'),'yyyy-mm-dd'),
C.DECN_OTCOME_TYP_ID,C.DECN_SUB_TYP_ID,C.DECN_RSN_TYP_ID,C.DECN_OTCOME_TYP_ID,A.HSC_STS_TYP_ID,from_unixtime(UNIX_TIMESTAMP(C.DECN_RNDR_DTTM,'yyyy-mm-dd'),'yyyy-mm-dd'),D.REF_DESC,F.REF_DESC,G.REF_DESC,H.TAT_PT_DTTM,I.TAT_PT_DTTM

---------------------------------------------------------------------------------------------------------

--O/P with service      srvc_setting = 2
union

select 
    J.fed_tax_id as prov_tax_id,
    A.HSC_id,
    A.srvc_setting_typ_id,
    case when srvc_setting_typ_id =2 then "Outpatient"  end as srvc_setting_typ,     -- put filter at the end for 2 only
    A.HSC_STS_TYP_ID,
    from_unixtime(UNIX_TIMESTAMP(A.creat_dttm,'yyyy-mm-dd'),'yyyy-mm-dd'),
    AA.srvc_desc_typ_id,
    case when srvc_desc_typ_id= '1' then "Standard"
         when srvc_desc_typ_id in  ('2','3') then " Urgent" end as srvc_desc_typ,   
    from_unixtime(UNIX_TIMESTAMP(C.DECN_RNDR_DTTM,'yyyy-mm-dd'),'yyyy-mm-dd'),
    C.DECN_OTCOME_TYP_ID,   
    C.DECN_SUB_TYP_ID,  
    C.DECN_RSN_TYP_ID,
    case when C.DECN_OTCOME_TYP_ID =1 then 'Approved'
         when C.DECN_OTCOME_TYP_ID =2 then 'Denied'
         when C.DECN_OTCOME_TYP_ID =4 then 'Cancelled'
         when C.DECN_OTCOME_TYP_ID is NULL and A.HSC_STS_TYP_ID in (1,3,5) and from_unixtime(UNIX_TIMESTAMP(C.DECN_RNDR_DTTM,'yyyy-mm-dd'),'yyyy-mm-dd') is NULL then 'Pending' end as outcome,
    trim(D.REF_DESC) as outcome_reason,   
    case when F.ref_desc ='Medicare' then 'M&R'
        when F.ref_desc ='Commercial' then 'E&I'
        when F.ref_desc ='Medicaid' then 'C&S'
        when F.ref_desc ='Both Medicare and Medicaid' then 'C&S'
        when F.ref_desc ='TPA' then 'C&S'
        when F.ref_desc ='CSP Medicaid Enrolled/External Medicare Enrolled' then 'C&S'
        when F.ref_desc ='Champus' then 'Others'
        else NULL end as LOB,
    G.REF_DESC as Service_category,
    ((day(i.tat_pt_dttm)*24*60*60+HOUR ( i.tat_pt_dttm)*60*60+MINUTE ( i.tat_pt_dttm)*60+ SECOND ( i.tat_pt_dttm)) - (day(H.tat_pt_dttm)*24*60*60+HOUR ( H.tat_pt_dttm)*60*60+MINUTE ( H.tat_pt_dttm)*60+ SECOND ( H.tat_pt_dttm)) )/60/60 as TAT_hrs
    
From 
    df2_hsr_lakeprd.HSC_SNAPSHOT A
left join df2_hsr_lakeprd.HSC_SRVC_NON_FACL_SNAPSHOT AA
    on A.HSC_ID = AA.HSC_ID
left join df2_hsr_lakeprd.hsc_srvc_snapshot K
    on A.HSC_ID = K.HSC_ID
left join df2_hsr_lakeprd.HSC_PROV_Snapshot J
    on A.HSC_ID = J.HSC_ID and K.srvc_prov_seq_nbr = J.prov_seq_nbr

left join ( select hsc_id, max(DECN_SEQ_NBR) as DECN_SEQ_NBR from df2_hsr_lakeprd.HSC_SRVC_DECN_SNAPSHOT 
                            where from_unixtime(UNIX_TIMESTAMP(DECN_RNDR_DTTM,'yyyy-mm-dd'),'yyyy-mm-dd') >= '2018-01-01'group by hsc_id ) B 
    on A.HSC_ID = B.HSC_ID    -- based on AA or A
    
left join df2_hsr_lakeprd.HSC_SRVC_DECN_SNAPSHOT C 
    on A.hsc_id = c.hsc_id and B.DECN_SEQ_NBR = C.DECN_SEQ_NBR and C.srvc_seq_nbr = K.srvc_seq_nbr

inner join df2_hsr_lakeprd.REF D
    on (C.DECN_RSN_TYP_ID = D.REF_CD AND D.REF_NM ='decisionReasonType')

left join df2_hsr_lakeprd.HSC_MBR_COV_SNAPSHOT E
    on A.hsc_id= E.hsc_id and A.mbr_cov_seq_nbr = E.mbr_cov_seq_nbr

inner join df2_hsr_lakeprd.ref F
    on (E.prdct_catgy_cd=F.ref_cd and  F.REF_NM ='productCategoryType')

inner join  df2_hsr_lakeprd.REF G
    on (AA.SRVC_DTL_TYP_ID = G.REF_CD AND G.REF_NM ='serviceDetailType')

left join ( select hsc_id,tat_pt_dttm,srvc_seq_nbr from df2_hsr_lakeprd.HSC_SRVC_TAT_PT_SNAPSHOT WHERE  tat_pt_typ_id ='01') H
    on A.HSC_ID = H.HSC_ID and C.srvc_seq_nbr=H.srvc_seq_nbr
left join ( select hsc_id,tat_pt_dttm,srvc_seq_nbr from df2_hsr_lakeprd.HSC_SRVC_TAT_PT_SNAPSHOT WHERE  tat_pt_typ_id ='04') I
    on A.HSC_ID = I.HSC_ID and C.srvc_seq_nbr=I.srvc_seq_nbr

WHERE 
    from_unixtime(UNIX_TIMESTAMP(A.creat_dttm,'yyyy-mm-dd'),'yyyy-mm-dd') >= from_unixtime(UNIX_TIMESTAMP(E.cov_eff_dt,'yyyy-mm-dd'),'yyyy-mm-dd') and from_unixtime(UNIX_TIMESTAMP(A.creat_dttm,'yyyy-mm-dd'),'yyyy-mm-dd')<= from_unixtime(UNIX_TIMESTAMP(E.cov_end_dt,'yyyy-mm-dd'),'yyyy-mm-dd')        
    and E.COV_TYP_ID = 'M' 
    and from_unixtime(UNIX_TIMESTAMP(A.creat_dttm,'yyyy-mm-dd'),'yyyy-mm-dd') between'2018-01-01' and '2019-06-30'
    and A.srvc_setting_typ_id =2
    and     J.fed_tax_id  in ('111871039','111888924','141338470','141340100','141349558','150552726','113613997','223636986','61603195','61562701','141347717','133964321','111635088','111639818','112050523','113565450','111352310','111704595','113438973','131740104')
    --and C.hsc_id='126595048'
group by J.fed_tax_id,A.HSC_id,A.srvc_setting_typ_id,A.srvc_setting_typ_id,A.HSC_STS_TYP_ID,from_unixtime(UNIX_TIMESTAMP(A.creat_dttm,'yyyy-mm-dd'),'yyyy-mm-dd'),AA.srvc_desc_typ_id,from_unixtime(UNIX_TIMESTAMP(C.DECN_RNDR_DTTM,'yyyy-mm-dd'),'yyyy-mm-dd'),
C.DECN_OTCOME_TYP_ID,C.DECN_SUB_TYP_ID,C.DECN_RSN_TYP_ID,C.DECN_OTCOME_TYP_ID,A.HSC_STS_TYP_ID,from_unixtime(UNIX_TIMESTAMP(C.DECN_RNDR_DTTM,'yyyy-mm-dd'),'yyyy-mm-dd'),D.REF_DESC,F.REF_DESC,G.REF_DESC,H.TAT_PT_DTTM,I.TAT_PT_DTTM


Claims:
*************
set mapred.job.queue.name=root.pdigpprd_q1;
--select count(*) from (
select 
T1.source_id,
T1.root_claim_num,
T1.line_num,lob_id,
T1.claim_type_cd,
T1.received_date,
T1.from_date,
T1.adjustment_date,
T1.payto_provider_npi,
T1.payto_provider_tax_id,
T1.amt_billed,
T1.amt_allowed,
T1.amt_interest,
T1.amt_paid,
T1.paid_date,
T1.claim_adjucation_auto_ind,
T1.claim_receipt_type_cd,
T1.claim_high_dollar_paid_ind,
T1.denial_full_reasons,
T1.denial_description,
T1.claim_denial_ind,
T1.adjustment_reasons,
T1.adjustment_description,
T1.claim_adj_ind,
T1.proc_cd,
T1.diag_cd,
T1.claim_non_par_ind,
T1.fromdatetoreceiveddate, 
T1.fromdatetopaiddate, 
T1.receiveddatetopaiddate,
T1.suffix_num,
T2.category,
T2.abbreviated_final_category,
T2.sourcesystem
from
pdi.pdi_claim_detail_base T1
left outer join pdi.remarkcode T2 on (T1.source_id = T2.sourcesystem and T1.adjustment_reasons=T2.remark_code)
where
T1.payto_provider_tax_id in ('111871039','111888924','141338470','141340100','141349558','150552726','113613997','223636986','61603195','61562701','141347717','133964321','111635088','111639818','112050523','113565450','111352310','111704595','113438973','131740104')
and year(T1.from_date) in (2018,2019) and T1.from_date <='2019-06-30';
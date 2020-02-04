import time
import json
import pymongo
import datetime
import calendar
import ast
import random
from duckling_wrapper import *

def main_fun(userid,sessid,req,intnt,prov_lst):
    dur_lst=list()
    dur_lst=time_extract(req)
    if intnt=="adjstd_claim_type_trend":
        print(get_dend_rate_vol_rate(dur_lst,prov_lst))
    elif intnt=="dend_reasons_trend":
        print(get_denial_reasons_trend(dur_lst,prov_lst))
    elif intnt=="prtl_dend_reasons_trend":
        print(get_prtl_denl_reasons_trend(dur_lst,prov_lst))
    elif intnt=="adjstd_claim_lob_trend":
        print(get_adjstd_claim_lob_trend(dur_lst,prov_lst))
    elif intnt=="adjstd_claim_par_trend":
        print(get_adjstd_claim_par_trend(dur_lst,prov_lst))
    elif intnt=="adjstd_claim_diag_cd_trend":
        print(get_adjstd_claim_diag_cd_trend(dur_lst,prov_lst))
    elif intnt=="adjstd_claim_tat_trend":
        print(get_adjstd_claim_tat_trend(dur_lst,prov_lst))
    elif intnt=="adjstd_claim_submsn_mode_trend":
        print(get_adjstd_claim_submsn_mode_trend(dur_lst,prov_lst))
        
def mon_name(tt):

    tt=str(int(tt))
    if tt=='1':
        return 'Jan'
    elif tt=='2':
        return 'Feb'
    elif tt=='3':
        return 'Mar'
    elif tt=='4':
        return 'Apr'
    elif tt=='5':
        return 'May'
    elif tt=='6':
        return 'Jun'
    elif tt=='7':
        return 'Jul'
    elif tt=='8':
        return 'Aug'
    elif tt=='9':
        return 'Sep'
    elif tt=='10':
        return 'Oct'
    elif tt=='11':
        return 'Nov'
    elif tt=='12':
        return 'Dec'
    return "None"



provider_lst1=['111888924','133964321']
# provider_lst1=list()
# main_fun('ud','sd','claims in last 6 months','adjstd_claim_vol_trend',provider_lst1)
# time.sleep(20)
# main_fun('ud','sd','claims in 2019','adjstd_claim_vol_trend',provider_lst1)
# time.sleep(20)
# main_fun('ud','sd','claims in last 6 months','adjstd_claim_val_trend',provider_lst1)
# time.sleep(20)
# main_fun('ud','sd','claims in 2019','adjstd_claim_val_trend',provider_lst1)
# time.sleep(20)
main_fun('ud','sd','claims in last 6 months','adjstd_claim_type_trend',provider_lst1)
time.sleep(20)
main_fun('ud','sd','claims in 2019','adjstd_claim_type_trend',provider_lst1)
time.sleep(20)
# main_fun('ud','sd','claims in last 6 months','adjstd_claim_lob_trend',provider_lst1)
# time.sleep(20)
# main_fun('ud','sd','claims in 2019','adjstd_claim_lob_trend',provider_lst1)
# time.sleep(20)
# main_fun('ud','sd','claims in last 6 months','adjstd_claim_par_trend',provider_lst1)
# time.sleep(20)
# main_fun('ud','sd','claims in 2019','adjstd_claim_par_trend',provider_lst1)
# time.sleep(20)
# main_fun('ud','sd','claims in last 6 months','adjstd_claim_diag_cd_trend',provider_lst1)
# time.sleep(20)
# main_fun('ud','sd','claims in 2019','adjstd_claim_diag_cd_trend',provider_lst1)
# time.sleep(20)
# main_fun('ud','sd','claims in last 6 months','adjstd_claim_tat_trend',provider_lst1)
# time.sleep(20)
# main_fun('ud','sd','claims in 2019','adjstd_claim_tat_trend',provider_lst1)
# time.sleep(20)
# main_fun('ud','sd','claims in last 6 months','adjstd_claim_submsn_mode_trend',provider_lst1)
# time.sleep(20)
# main_fun('ud','sd','claims in 2019','adjstd_claim_submsn_mode_trend',provider_lst1)
# time.sleep(20)
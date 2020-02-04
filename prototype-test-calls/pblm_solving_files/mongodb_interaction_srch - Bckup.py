import pymongo
import datetime
import calendar
import ast
import random
from pblm_solving_files.duckling_wrapper import *
from pblm_solving_files.knowledge_rev import *
import requests

def main_fun(userid,sessid,req,prov_lst):
    dur_lst=list()
    dur_lst=time_extract(req)
    s1=corrected_ip_string_1(req,'claims')
    response = requests.get("http://apsrp03693:5088/parse",params={"q":s1})                
    response = response.json()
    intent = response.get("intent")
    intnt1=intent['name']   
    print(intnt1) 
    if intnt1.lower()=='claims_count':
        if 'received' in s1:
            intnt="rcvd_claim_vol_trend"
        elif 'paid' in s1:
            intnt="paid_claim_vol_trend"
    elif intnt1.lower()=='claims_action_reasons':
        if 'denied' in s1 and 'partial' in s1:
            intnt="prtl_dend_reasons_trend"
        elif 'denied' in s1:
            intnt="dend_reasons_trend"
        elif 'adjusted' in s1:
            intnt="adjstd_reasons_trend"
    if intnt=="rcvd_claim_vol_trend":
        return get_rcvd_claim_vol_trend(dur_lst,prov_lst)
    elif intnt=="rcvd_claim_val_trend":
        print(get_rcvd_claim_val_trend(dur_lst,prov_lst))
    elif intnt=="rcvd_claim_type_trend":
        print(get_rcvd_claim_type_trend(dur_lst,prov_lst))
    elif intnt=="rcvd_claim_lob_trend":
        print(get_rcvd_claim_lob_trend(dur_lst,prov_lst))
    elif intnt=="rcvd_claim_par_trend":
        print(get_rcvd_claim_par_trend(dur_lst,prov_lst))
    elif intnt=="rcvd_claim_diag_cd_trend":
        print(get_rcvd_claim_diag_cd_trend(dur_lst,prov_lst))
    elif intnt=="rcvd_claim_tat_trend":
        print(get_rcvd_claim_tat_trend(dur_lst,prov_lst))
    elif intnt=="rcvd_claim_submsn_mode_trend":
        print(get_rcvd_claim_submsn_mode_trend(dur_lst,prov_lst))
    elif intnt=="paid_claim_vol_trend":
        print(get_paid_claim_vol_trend(dur_lst,prov_lst))
    elif intnt=="paid_claim_val_trend":
        print(get_paid_claim_val_trend(dur_lst,prov_lst))
    elif intnt=="paid_claim_type_trend":
        print(get_paid_claim_type_trend(dur_lst,prov_lst))
    elif intnt=="paid_claim_lob_trend":
        print(get_paid_claim_lob_trend(dur_lst,prov_lst))
    elif intnt=="paid_claim_par_trend":
        print(get_paid_claim_par_trend(dur_lst,prov_lst))
    elif intnt=="paid_claim_diag_cd_trend":
        print(get_paid_claim_diag_cd_trend(dur_lst,prov_lst))
    elif intnt=="paid_claim_tat_trend":
        print(get_paid_claim_tat_trend(dur_lst,prov_lst))
    elif intnt=="paid_claim_submsn_mode_trend":
        print(get_paid_claim_submsn_mode_trend(dur_lst,prov_lst))
    elif intnt=="dend_claim_vol_trend":
        print(get_dend_claim_vol_trend(dur_lst,prov_lst))
    elif intnt=="dend_claim_val_trend":
        print(get_dend_claim_val_trend(dur_lst,prov_lst))
    elif intnt=="dend_claim_type_trend":
        print(get_dend_claim_type_trend(dur_lst,prov_lst))
    elif intnt=="dend_claim_lob_trend":
        print(get_dend_claim_lob_trend(dur_lst,prov_lst))
    elif intnt=="dend_claim_par_trend":
        print(get_dend_claim_par_trend(dur_lst,prov_lst))
    elif intnt=="dend_claim_diag_cd_trend":
        print(get_dend_claim_diag_cd_trend(dur_lst,prov_lst))
    elif intnt=="dend_claim_tat_trend":
        print(get_dend_claim_tat_trend(dur_lst,prov_lst))
    elif intnt=="dend_claim_submsn_mode_trend":
        print(get_dend_claim_submsn_mode_trend(dur_lst,prov_lst))
    elif intnt=="prtl_dend_claim_vol_trend":
        print(get_prtl_dend_claim_vol_trend(dur_lst,prov_lst))
    elif intnt=="prtl_dend_claim_val_trend":
        print(get_prtl_dend_claim_val_trend(dur_lst,prov_lst))
    elif intnt=="prtl_dend_claim_type_trend":
        print(get_prtl_dend_claim_type_trend(dur_lst,prov_lst))
    elif intnt=="prtl_dend_claim_lob_trend":
        print(get_prtl_dend_claim_lob_trend(dur_lst,prov_lst))
    elif intnt=="prtl_dend_claim_par_trend":
        print(get_prtl_dend_claim_par_trend(dur_lst,prov_lst))
    elif intnt=="prtl_dend_claim_diag_cd_trend":
        print(get_prtl_dend_claim_diag_cd_trend(dur_lst,prov_lst))
    elif intnt=="prtl_dend_claim_tat_trend":
        print(get_prtl_dend_claim_tat_trend(dur_lst,prov_lst))
    elif intnt=="prtl_dend_claim_submsn_mode_trend":
        print(get_prtl_dend_claim_submsn_mode_trend(dur_lst,prov_lst))
    elif intnt=="adjstd_claim_vol_trend":
        print(get_adjstd_claim_vol_trend(dur_lst,prov_lst))
    elif intnt=="adjstd_claim_val_trend":
        print(get_adjstd_claim_val_trend(dur_lst,prov_lst))
    elif intnt=="adjstd_claim_type_trend":
        print(get_adjstd_claim_type_trend(dur_lst,prov_lst))
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
    elif intnt=="adjstd_reasons_trend":
        return (get_adjstd_reasons_trend(dur_lst,prov_lst))
    elif intnt=="dend_reasons_trend":
        return (get_denial_reasons_trend(dur_lst,prov_lst))
    elif intnt=="prtl_dend_reasons_trend":
        return (get_prtl_denl_reasons_trend(dur_lst,prov_lst))
        
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

def get_rcvd_claim_vol_trend(dur_lst,provider_lst):
    print(provider_lst)

    try:
        cond=""
        n_records="0"
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb["hfa_claims_1819"] 
        key_lst=list()
        val_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1]
            print(dur_lst)
            strt_lst=list()            
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[0])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[1])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[2])
            end_lst=list()            
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[0])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[1])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[2])            
            yr_strt=int(str(strt_lst[0]))
            yr_end=int(str(end_lst[0]))
            mon_strt=int(str(strt_lst[1]))
            mon_end=int(str(end_lst[1]))
            while True:
                mon_frmt=""
                if mon_strt < 10:
                    mon_frmt='0'+str(mon_strt)
                else:
                    mon_frmt=str(mon_strt)
                cond=cond+"{'received_date':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'received_date':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                    cond="{'$and':["+cond+pc+"]}"
                else:
                    cond="{'$and':["+cond+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)                    
                mydoc = mycol.find(my_dict)
                n_records='0'
                n_records=str(mydoc.count()) 
                print(str(mon_strt))
                key_val=mon_name(mon_strt)+"-"+str(str(yr_strt)[-2:])
                val_val=n_records                
                key_lst.append(key_val)
                val_lst.append(val_val)
                cond=""
                mon_strt=mon_strt+1
                print(type(mon_strt))
                print((mon_strt))
                if (mon_strt) >= 13:
                    mon_strt=1
                    yr_strt=yr_strt+1
                
                if  (mon_strt < mon_end or mon_strt > mon_end) and (yr_strt<=yr_end):
                    bypass=1
                else:
                    break

        elif len(dur_lst) ==4:
            if len(dur_lst[1])==0:
                dur_lst[1]=['01','02','03','04','05','06','07','08','09','10','11','12']
            if len(dur_lst[2])==0:
                dur_lst[2].append(str(datetime.datetime.now().year))
            
            for dl in dur_lst[2]:
                for dl1 in dur_lst[1]:
                    cond=cond+"{'received_date':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'received_date':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    if len(provider_lst) > 0:
                        pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                        cond="{'$and':["+cond+pc+"]}"
                    else:
                        cond="{'$and':["+cond+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)                    
                    mydoc = mycol.find(my_dict)
                    n_records='0'
                    n_records=str(mydoc.count()) 
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Trend (Volume)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Line")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(key_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(val_lst)+""+","
        kv=kv[0:len(kv)-1]+"}"
        print(kv)
        kv=ast.literal_eval(kv)
        return kv

    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"

def get_rcvd_claim_val_trend(dur_lst,provider_lst):

    try:
        cond=""
        n_records="0"
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb["hfa_claims_1819"] 
        key_lst=list()
        val_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1]
            print(dur_lst)
            strt_lst=list()
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[0])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[1])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[2])
            end_lst=list()
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[0])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[1])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[2])
            yr_strt=int(str(strt_lst[0]))
            yr_end=int(str(end_lst[0]))
            mon_strt=int(str(strt_lst[1]))
            mon_end=int(str(end_lst[1]))
            while True:
                mon_frmt=""
                if mon_strt < 10:
                    mon_frmt='0'+str(mon_strt)
                else:
                    mon_frmt=str(mon_strt)
                cond=cond+"{'received_date':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'received_date':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                    cond="{'$and':["+cond+pc+"]}"
                else:
                    cond="{'$and':["+cond+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':None, 'total': {'$sum': {'$convert':{'input':'$amt_billed','to':'double','onError':'0','onNull':'0'}}}}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records="0"
                for x in mydoc:
                    print(str(x['total']))
                    n_records=str(round(float(str(x['total'])),2))
                print(str(mon_strt))
                key_val=mon_name(mon_strt)+"-"+str(str(yr_strt)[-2:])
                val_val=n_records                
                key_lst.append(key_val)
                val_lst.append(val_val)
                cond=""
                mon_strt=mon_strt+1
                print(type(mon_strt))
                print((mon_strt))
                if (mon_strt) >= 13:
                    mon_strt=1
                    yr_strt=yr_strt+1
                
                if  (mon_strt < mon_end or mon_strt > mon_end) and (yr_strt<=yr_end):
                    bypass=1
                else:
                    break

        elif len(dur_lst) ==4:
            if len(dur_lst[1])==0:
                dur_lst[1]=['01','02','03','04','05','06','07','08','09','10','11','12']
            if len(dur_lst[2])==0:
                dur_lst[2].append(str(datetime.datetime.now().year))
            
            for dl in dur_lst[2]:
                for dl1 in dur_lst[1]:
                    cond=cond+"{'received_date':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'received_date':{'$regex':'"+str(dl)+"-.*-.*'}}"                    
                    if len(provider_lst) > 0:
                        pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                        cond="{'$and':["+cond+pc+"]}"
                    else:
                        cond="{'$and':["+cond+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':None, 'total': {'$sum': {'$convert':{'input':'$amt_billed','to':'double','onError':'0','onNull':'0'}}}}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records="0"
                    for x in mydoc:
                        print(str(x['total']))
                        n_records=str(round(float(str(x['total'])),2))
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Trend (Volume)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Line")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(key_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(val_lst)+""+","
        kv=kv[0:len(kv)-1]+"}"
        print(kv)
        kv=ast.literal_eval(kv)
        return kv

    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"

def get_rcvd_claim_type_trend(dur_lst,provider_lst):

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb["hfa_claims_1819"] 
        key_lst=list()
        val_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1]
            print(dur_lst)
            strt_lst=list()
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[0])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[1])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[2])
            end_lst=list()
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[0])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[1])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[2])
            yr_strt=int(str(strt_lst[0]))
            yr_end=int(str(end_lst[0]))
            mon_strt=int(str(strt_lst[1]))
            mon_end=int(str(end_lst[1]))
            while True:
                mon_frmt=""
                if mon_strt < 10:
                    mon_frmt='0'+str(mon_strt)
                else:
                    mon_frmt=str(mon_strt)
                cond=cond+"{'received_date':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'received_date':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                    cond="{'$and':["+cond+pc+"]}"
                else:
                    cond="{'$and':["+cond+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$claim_type_cd', 'total': {'$sum': 1}}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    print(str(x['_id']+"!"+str(x['total'])))
                    n_records=n_records+"}"+(str(x['_id']+"!"+str(x['total'])))
                n_records=n_records[1:]
                print(str(mon_strt))
                key_val=mon_name(mon_strt)+"-"+str(str(yr_strt)[-2:])
                val_val=n_records                
                key_lst.append(key_val)
                val_lst.append(val_val)
                cond=""
                mon_strt=mon_strt+1
                print(type(mon_strt))
                print((mon_strt))
                if (mon_strt) >= 13:
                    mon_strt=1
                    yr_strt=yr_strt+1
                
                if  (mon_strt < mon_end or mon_strt > mon_end) and (yr_strt<=yr_end):
                    bypass=1
                else:
                    break

        elif len(dur_lst) ==4:
            if len(dur_lst[1])==0:
                dur_lst[1]=['01','02','03','04','05','06','07','08','09','10','11','12']
            if len(dur_lst[2])==0:
                dur_lst[2].append(str(datetime.datetime.now().year))
            
            for dl in dur_lst[2]:
                for dl1 in dur_lst[1]:
                    cond=cond+"{'received_date':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'received_date':{'$regex':'"+str(dl)+"-.*-.*'}}"                    
                    if len(provider_lst) > 0:
                        pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                        cond="{'$and':["+cond+pc+"]}"
                    else:
                        cond="{'$and':["+cond+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$claim_type_cd', 'total': {'$sum': 1}}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        print(str(x['_id']+"!"+str(x['total'])))
                        n_records=n_records+"}"+(str(x['_id']+"!"+str(x['total'])))
                    n_records=n_records[1:]
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Trend (Volume)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Line")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(key_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(val_lst)+""+","
        kv=kv[0:len(kv)-1]+"}"
        print(kv)
        kv=ast.literal_eval(kv)
        return kv

    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"

def get_rcvd_claim_lob_trend(dur_lst,provider_lst):

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb["hfa_claims_1819"] 
        key_lst=list()
        val_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1]
            print(dur_lst)
            strt_lst=list()
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[0])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[1])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[2])
            end_lst=list()
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[0])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[1])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[2])
            yr_strt=int(str(strt_lst[0]))
            yr_end=int(str(end_lst[0]))
            mon_strt=int(str(strt_lst[1]))
            mon_end=int(str(end_lst[1]))
            while True:
                mon_frmt=""
                if mon_strt < 10:
                    mon_frmt='0'+str(mon_strt)
                else:
                    mon_frmt=str(mon_strt)
                cond=cond+"{'received_date':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'received_date':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                    cond="{'$and':["+cond+pc+"]}"
                else:
                    cond="{'$and':["+cond+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$lob_id', 'total': {'$sum': 1}}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    print(str(x['_id']+"!"+str(x['total'])))
                    n_records=n_records+"}"+(str(x['_id']+"!"+str(x['total'])))
                n_records=n_records[1:]
                print(str(mon_strt))
                key_val=mon_name(mon_strt)+"-"+str(str(yr_strt)[-2:])
                val_val=n_records                
                key_lst.append(key_val)
                val_lst.append(val_val)
                cond=""
                mon_strt=mon_strt+1
                print(type(mon_strt))
                print((mon_strt))
                if (mon_strt) >= 13:
                    mon_strt=1
                    yr_strt=yr_strt+1
                
                if  (mon_strt < mon_end or mon_strt > mon_end) and (yr_strt<=yr_end):
                    bypass=1
                else:
                    break

        elif len(dur_lst) ==4:
            if len(dur_lst[1])==0:
                dur_lst[1]=['01','02','03','04','05','06','07','08','09','10','11','12']
            if len(dur_lst[2])==0:
                dur_lst[2].append(str(datetime.datetime.now().year))
            
            for dl in dur_lst[2]:
                for dl1 in dur_lst[1]:
                    cond=cond+"{'received_date':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'received_date':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                        cond="{'$and':["+cond+pc+"]}"
                    else:
                        cond="{'$and':["+cond+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$lob_id', 'total': {'$sum': 1}}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        print(str(x['_id']+"!"+str(x['total'])))
                        n_records=n_records+"}"+(str(x['_id']+"!"+str(x['total'])))
                    n_records=n_records[1:]
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Trend (Volume)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Line")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(key_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(val_lst)+""+","
        kv=kv[0:len(kv)-1]+"}"
        print(kv)
        kv=ast.literal_eval(kv)
        return kv

    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"

def get_rcvd_claim_par_trend(dur_lst,provider_lst):

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb["hfa_claims_1819"] 
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1]
            print(dur_lst)
            strt_lst=list()
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[0])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[1])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[2])
            end_lst=list()
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[0])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[1])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[2])
            yr_strt=int(str(strt_lst[0]))
            yr_end=int(str(end_lst[0]))
            mon_strt=int(str(strt_lst[1]))
            mon_end=int(str(end_lst[1]))
            while True:
                mon_frmt=""
                if mon_strt < 10:
                    mon_frmt='0'+str(mon_strt)
                else:
                    mon_frmt=str(mon_strt)
                cond=cond+"{'received_date':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'received_date':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                    cond="{'$and':["+cond+pc+"]}"
                else:
                    cond="{'$and':["+cond+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$claim_non_par_ind', 'total': {'$sum': 1}}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    print(str(x['_id']+"!"+str(x['total'])))
                    n_records=n_records+"}"+(str(x['_id']+"!"+str(x['total'])))
                n_records=n_records[1:]
                print(str(mon_strt))
                key_val=mon_name(mon_strt)+"-"+str(str(yr_strt)[-2:])
                val_val=n_records                
                key_lst.append(key_val)
                val_lst.append(val_val)
                cond=""
                mon_strt=mon_strt+1
                print(type(mon_strt))
                print((mon_strt))
                if (mon_strt) >= 13:
                    mon_strt=1
                    yr_strt=yr_strt+1
                
                if  (mon_strt < mon_end or mon_strt > mon_end) and (yr_strt<=yr_end):
                    bypass=1
                else:
                    break

        elif len(dur_lst) ==4:
            if len(dur_lst[1])==0:
                dur_lst[1]=['01','02','03','04','05','06','07','08','09','10','11','12']
            if len(dur_lst[2])==0:
                dur_lst[2].append(str(datetime.datetime.now().year))
            
            for dl in dur_lst[2]:
                for dl1 in dur_lst[1]:
                    cond=cond+"{'received_date':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'received_date':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                        cond="{'$and':["+cond+pc+"]}"
                    else:
                        cond="{'$and':["+cond+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$claim_non_par_ind', 'total': {'$sum': 1}}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        print(str(x['_id']+"!"+str(x['total'])))
                        n_records=n_records+"}"+(str(x['_id']+"!"+str(x['total'])))
                    n_records=n_records[1:]
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Trend (Volume)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Line")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(key_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(val_lst)+""+","
        kv=kv[0:len(kv)-1]+"}"
        print(kv)
        kv=ast.literal_eval(kv)
        return kv

    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"

def get_rcvd_claim_diag_cd_trend(dur_lst,provider_lst):

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb["hfa_claims_1819"] 
        key_lst=list()
        val_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1]
            print(dur_lst)
            strt_lst=list()
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[0])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[1])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[2])
            end_lst=list()
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[0])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[1])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[2])
            yr_strt=int(str(strt_lst[0]))
            yr_end=int(str(end_lst[0]))
            mon_strt=int(str(strt_lst[1]))
            mon_end=int(str(end_lst[1]))
            while True:
                mon_frmt=""
                if mon_strt < 10:
                    mon_frmt='0'+str(mon_strt)
                else:
                    mon_frmt=str(mon_strt)
                cond=cond+"{'received_date':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'received_date':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                    cond="{'$and':["+cond+pc+"]}"
                else:
                    cond="{'$and':["+cond+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$diag_cd', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                top_cnt=0
                for x in mydoc:
                    top_cnt=top_cnt+1
                    if top_cnt==6:
                        break
                    print(str(x['_id']+"!"+str(x['total'])))
                    n_records=n_records+"}"+(str(x['_id'].strip(' ')+"!"+str(x['total'])))
                n_records=n_records[1:]
                print(str(mon_strt))
                key_val=mon_name(mon_strt)+"-"+str(str(yr_strt)[-2:])
                val_val=n_records                
                key_lst.append(key_val)
                val_lst.append(val_val)
                cond=""
                mon_strt=mon_strt+1
                print(type(mon_strt))
                print((mon_strt))
                if (mon_strt) >= 13:
                    mon_strt=1
                    yr_strt=yr_strt+1
                
                if  (mon_strt < mon_end or mon_strt > mon_end) and (yr_strt<=yr_end):
                    bypass=1
                else:
                    break

        elif len(dur_lst) ==4:
            if len(dur_lst[1])==0:
                dur_lst[1]=['01','02','03','04','05','06','07','08','09','10','11','12']
            if len(dur_lst[2])==0:
                dur_lst[2].append(str(datetime.datetime.now().year))
            
            for dl in dur_lst[2]:
                for dl1 in dur_lst[1]:
                    cond=cond+"{'received_date':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'received_date':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                        cond="{'$and':["+cond+pc+"]}"
                    else:
                        cond="{'$and':["+cond+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$diag_cd', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    top_cnt=0
                    for x in mydoc:
                        top_cnt=top_cnt+1
                        if top_cnt==6:
                            break
                        print(str(x['_id']+"!"+str(x['total'])))
                        n_records=n_records+"}"+(str(x['_id'].strip(' ')+"!"+str(x['total'])))
                    n_records=n_records[1:]
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Trend (Volume)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Line")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(key_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(val_lst)+""+","
        kv=kv[0:len(kv)-1]+"}"
        print(kv)
        kv=ast.literal_eval(kv)
        return kv

    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"

def get_rcvd_claim_tat_trend(dur_lst,provider_lst):

    try:
        cond=""
        n_records="0"
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb["hfa_claims_1819"] 
        key_lst=list()
        val_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1]
            print(dur_lst)
            strt_lst=list()
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[0])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[1])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[2])
            end_lst=list()
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[0])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[1])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[2])
            yr_strt=int(str(strt_lst[0]))
            yr_end=int(str(end_lst[0]))
            mon_strt=int(str(strt_lst[1]))
            mon_end=int(str(end_lst[1]))
            while True:
                mon_frmt=""
                if mon_strt < 10:
                    mon_frmt='0'+str(mon_strt)
                else:
                    mon_frmt=str(mon_strt)
                cond=cond+"{'received_date':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'received_date':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                    cond="{'$and':["+cond+pc+"]}"
                else:
                    cond="{'$and':["+cond+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':None, 'total': {'$avg': {'$convert':{'input':'$fromdatetopaiddate','to':'double','onError':'0','onNull':'0'}}}}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records="0"
                for x in mydoc:
                    print(str(x['total']))
                    n_records=str(round(float(str(x['total'])),2))
                print(str(mon_strt))
                key_val=mon_name(mon_strt)+"-"+str(str(yr_strt)[-2:])
                val_val=n_records                
                key_lst.append(key_val)
                val_lst.append(val_val)
                cond=""
                mon_strt=mon_strt+1
                print(type(mon_strt))
                print((mon_strt))
                if (mon_strt) >= 13:
                    mon_strt=1
                    yr_strt=yr_strt+1
                
                if  (mon_strt < mon_end or mon_strt > mon_end) and (yr_strt<=yr_end):
                    bypass=1
                else:
                    break

        elif len(dur_lst) ==4:
            if len(dur_lst[1])==0:
                dur_lst[1]=['01','02','03','04','05','06','07','08','09','10','11','12']
            if len(dur_lst[2])==0:
                dur_lst[2].append(str(datetime.datetime.now().year))
            
            for dl in dur_lst[2]:
                for dl1 in dur_lst[1]:
                    cond=cond+"{'received_date':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'received_date':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                        cond="{'$and':["+cond+pc+"]}"
                    else:
                        cond="{'$and':["+cond+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':None, 'total': {'$avg': {'$convert':{'input':'$fromdatetopaiddate','to':'double','onError':'0','onNull':'0'}}}}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records="0"
                    for x in mydoc:
                        print(str(x['total']))
                        n_records=str(round(float(str(x['total'])),2))
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Trend (Volume)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Line")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(key_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(val_lst)+""+","
        kv=kv[0:len(kv)-1]+"}"
        print(kv)
        kv=ast.literal_eval(kv)
        return kv

    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"

def get_rcvd_claim_submsn_mode_trend(dur_lst,provider_lst):

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb["hfa_claims_1819"] 
        key_lst=list()
        val_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1]
            print(dur_lst)
            strt_lst=list()
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[0])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[1])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[2])
            end_lst=list()
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[0])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[1])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[2])
            yr_strt=int(str(strt_lst[0]))
            yr_end=int(str(end_lst[0]))
            mon_strt=int(str(strt_lst[1]))
            mon_end=int(str(end_lst[1]))
            while True:
                mon_frmt=""
                if mon_strt < 10:
                    mon_frmt='0'+str(mon_strt)
                else:
                    mon_frmt=str(mon_strt)
                cond=cond+"{'received_date':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'received_date':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                    cond="{'$and':["+cond+pc+"]}"
                else:
                    cond="{'$and':["+cond+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$claim_receipt_type_cd', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""                
                for x in mydoc:
                    print(str(x['_id']+"!"+str(x['total'])))
                    n_records=n_records+"}"+(str(x['_id'].strip(' ')+"!"+str(x['total'])))
                n_records=n_records[1:]
                print(str(mon_strt))
                key_val=mon_name(mon_strt)+"-"+str(str(yr_strt)[-2:])
                val_val=n_records                
                key_lst.append(key_val)
                val_lst.append(val_val)
                cond=""
                mon_strt=mon_strt+1
                print(type(mon_strt))
                print((mon_strt))
                if (mon_strt) >= 13:
                    mon_strt=1
                    yr_strt=yr_strt+1
                
                if  (mon_strt < mon_end or mon_strt > mon_end) and (yr_strt<=yr_end):
                    bypass=1
                else:
                    break

        elif len(dur_lst) ==4:
            if len(dur_lst[1])==0:
                dur_lst[1]=['01','02','03','04','05','06','07','08','09','10','11','12']
            if len(dur_lst[2])==0:
                dur_lst[2].append(str(datetime.datetime.now().year))
            
            for dl in dur_lst[2]:
                for dl1 in dur_lst[1]:
                    cond=cond+"{'received_date':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'received_date':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                        cond="{'$and':["+cond+pc+"]}"
                    else:
                        cond="{'$and':["+cond+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$claim_receipt_type_cd', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""                    
                    for x in mydoc:
                        print(str(x['_id']+"!"+str(x['total'])))
                        n_records=n_records+"}"+(str(x['_id'].strip(' ')+"!"+str(x['total'])))
                    n_records=n_records[1:]
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Trend (Volume)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Line")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(key_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(val_lst)+""+","
        kv=kv[0:len(kv)-1]+"}"
        print(kv)
        kv=ast.literal_eval(kv)
        return kv
    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"

def get_paid_claim_vol_trend(dur_lst,provider_lst):

    try:
        cond=""
        n_records="0"
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb["hfa_claims_1819"] 
        key_lst=list()
        val_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1]
            print(dur_lst)
            strt_lst=list()
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[0])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[1])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[2])
            end_lst=list()
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[0])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[1])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[2])
            yr_strt=int(str(strt_lst[0]))
            yr_end=int(str(end_lst[0]))
            mon_strt=int(str(strt_lst[1]))
            mon_end=int(str(end_lst[1]))
            while True:
                mon_frmt=""
                if mon_strt < 10:
                    mon_frmt='0'+str(mon_strt)
                else:
                    mon_frmt=str(mon_strt)
                cond=cond+"{'paid_date':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'paid_date':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                    di=",{'claim_denial_ind':'0'}"
                    cond="{'$and':["+cond+pc+di+"]}"
                else:
                    di=",{'claim_denial_ind':'0'}"
                    cond="{'$and':["+cond+di+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)                    
                mydoc = mycol.find(my_dict)
                n_records='0'
                n_records=str(mydoc.count()) 
                print(str(mon_strt))
                key_val=mon_name(mon_strt)+"-"+str(str(yr_strt)[-2:])
                val_val=n_records                
                key_lst.append(key_val)
                val_lst.append(val_val)
                cond=""
                mon_strt=mon_strt+1
                print(type(mon_strt))
                print((mon_strt))
                if (mon_strt) >= 13:
                    mon_strt=1
                    yr_strt=yr_strt+1
                
                if  (mon_strt < mon_end or mon_strt > mon_end) and (yr_strt<=yr_end):
                    bypass=1
                else:
                    break

        elif len(dur_lst) ==4:
            if len(dur_lst[1])==0:
                dur_lst[1]=['01','02','03','04','05','06','07','08','09','10','11','12']
            if len(dur_lst[2])==0:
                dur_lst[2].append(str(datetime.datetime.now().year))
            
            for dl in dur_lst[2]:
                for dl1 in dur_lst[1]:
                    cond=cond+"{'paid_date':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'paid_date':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                        di=",{'claim_denial_ind':'0'}"
                        cond="{'$and':["+cond+pc+di+"]}"
                    else:
                        di=",{'claim_denial_ind':'0'}"
                        cond="{'$and':["+cond+di+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)                    
                    mydoc = mycol.find(my_dict)
                    n_records='0'
                    n_records=str(mydoc.count()) 
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Trend (Volume)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Line")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(key_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(val_lst)+""+","
        kv=kv[0:len(kv)-1]+"}"
        print(kv)
        kv=ast.literal_eval(kv)
        return kv

    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"

def get_paid_claim_val_trend(dur_lst,provider_lst):

    try:
        cond=""
        n_records="0"
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb["hfa_claims_1819"] 
        key_lst=list()
        val_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1]
            print(dur_lst)
            strt_lst=list()
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[0])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[1])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[2])
            end_lst=list()
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[0])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[1])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[2])
            yr_strt=int(str(strt_lst[0]))
            yr_end=int(str(end_lst[0]))
            mon_strt=int(str(strt_lst[1]))
            mon_end=int(str(end_lst[1]))
            while True:
                mon_frmt=""
                if mon_strt < 10:
                    mon_frmt='0'+str(mon_strt)
                else:
                    mon_frmt=str(mon_strt)
                cond=cond+"{'paid_date':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'paid_date':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                    di=",{'claim_denial_ind':'0'}"
                    cond="{'$and':["+cond+pc+di+"]}"
                else:
                    di=",{'claim_denial_ind':'0'}"
                    cond="{'$and':["+cond+di+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':None, 'total': {'$sum': {'$convert':{'input':'$amt_paid','to':'double','onError':'0','onNull':'0'}}}}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records="0"
                for x in mydoc:
                    print(str(x['total']))
                    n_records=str(round(float(str(x['total'])),2))
                print(str(mon_strt))
                key_val=mon_name(mon_strt)+"-"+str(str(yr_strt)[-2:])
                val_val=n_records                
                key_lst.append(key_val)
                val_lst.append(val_val)
                cond=""
                mon_strt=mon_strt+1
                print(type(mon_strt))
                print((mon_strt))
                if (mon_strt) >= 13:
                    mon_strt=1
                    yr_strt=yr_strt+1
                
                if  (mon_strt < mon_end or mon_strt > mon_end) and (yr_strt<=yr_end):
                    bypass=1
                else:
                    break

        elif len(dur_lst) ==4:
            if len(dur_lst[1])==0:
                dur_lst[1]=['01','02','03','04','05','06','07','08','09','10','11','12']
            if len(dur_lst[2])==0:
                dur_lst[2].append(str(datetime.datetime.now().year))
            
            for dl in dur_lst[2]:
                for dl1 in dur_lst[1]:
                    cond=cond+"{'paid_date':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'paid_date':{'$regex':'"+str(dl)+"-.*-.*'}}"                    
                    if len(provider_lst) > 0:
                        pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                        di=",{'claim_denial_ind':'0'}"
                        cond="{'$and':["+cond+pc+di+"]}"
                    else:
                        di=",{'claim_denial_ind':'0'}"
                        cond="{'$and':["+cond+di+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':None, 'total': {'$sum': {'$convert':{'input':'$amt_paid','to':'double','onError':'0','onNull':'0'}}}}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records="0"
                    for x in mydoc:
                        print(str(x['total']))
                        n_records=str(round(float(str(x['total'])),2))
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Trend (Volume)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Line")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(key_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(val_lst)+""+","
        kv=kv[0:len(kv)-1]+"}"
        print(kv)
        kv=ast.literal_eval(kv)
        return kv

    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"

def get_paid_claim_type_trend(dur_lst,provider_lst):

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb["hfa_claims_1819"] 
        key_lst=list()
        val_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1]
            print(dur_lst)
            strt_lst=list()
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[0])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[1])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[2])
            end_lst=list()
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[0])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[1])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[2])
            yr_strt=int(str(strt_lst[0]))
            yr_end=int(str(end_lst[0]))
            mon_strt=int(str(strt_lst[1]))
            mon_end=int(str(end_lst[1]))
            while True:
                mon_frmt=""
                if mon_strt < 10:
                    mon_frmt='0'+str(mon_strt)
                else:
                    mon_frmt=str(mon_strt)
                cond=cond+"{'paid_date':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'paid_date':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                    di=",{'claim_denial_ind':'0'}"
                    cond="{'$and':["+cond+pc+di+"]}"
                else:
                    di=",{'claim_denial_ind':'0'}"
                    cond="{'$and':["+cond+di+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$claim_type_cd', 'total': {'$sum': 1}}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    print(str(x['_id']+"!"+str(x['total'])))
                    n_records=n_records+"}"+(str(x['_id']+"!"+str(x['total'])))
                n_records=n_records[1:]
                print(str(mon_strt))
                key_val=mon_name(mon_strt)+"-"+str(str(yr_strt)[-2:])
                val_val=n_records                
                key_lst.append(key_val)
                val_lst.append(val_val)
                cond=""
                mon_strt=mon_strt+1
                print(type(mon_strt))
                print((mon_strt))
                if (mon_strt) >= 13:
                    mon_strt=1
                    yr_strt=yr_strt+1
                
                if  (mon_strt < mon_end or mon_strt > mon_end) and (yr_strt<=yr_end):
                    bypass=1
                else:
                    break

        elif len(dur_lst) ==4:
            if len(dur_lst[1])==0:
                dur_lst[1]=['01','02','03','04','05','06','07','08','09','10','11','12']
            if len(dur_lst[2])==0:
                dur_lst[2].append(str(datetime.datetime.now().year))
            
            for dl in dur_lst[2]:
                for dl1 in dur_lst[1]:
                    cond=cond+"{'paid_date':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'paid_date':{'$regex':'"+str(dl)+"-.*-.*'}}"                    
                    if len(provider_lst) > 0:
                        pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                        di=",{'claim_denial_ind':'0'}"
                        cond="{'$and':["+cond+pc+di+"]}"
                    else:
                        di=",{'claim_denial_ind':'0'}"
                        cond="{'$and':["+cond+di+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$claim_type_cd', 'total': {'$sum': 1}}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        print(str(x['_id']+"!"+str(x['total'])))
                        n_records=n_records+"}"+(str(x['_id']+"!"+str(x['total'])))
                    n_records=n_records[1:]
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Trend (Volume)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Line")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(key_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(val_lst)+""+","
        kv=kv[0:len(kv)-1]+"}"
        print(kv)
        kv=ast.literal_eval(kv)
        return kv

    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"

def get_paid_claim_lob_trend(dur_lst,provider_lst):

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb["hfa_claims_1819"] 
        key_lst=list()
        val_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1]
            print(dur_lst)
            strt_lst=list()
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[0])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[1])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[2])
            end_lst=list()
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[0])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[1])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[2])
            yr_strt=int(str(strt_lst[0]))
            yr_end=int(str(end_lst[0]))
            mon_strt=int(str(strt_lst[1]))
            mon_end=int(str(end_lst[1]))
            while True:
                mon_frmt=""
                if mon_strt < 10:
                    mon_frmt='0'+str(mon_strt)
                else:
                    mon_frmt=str(mon_strt)
                cond=cond+"{'paid_date':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'paid_date':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                    di=",{'claim_denial_ind':'0'}"
                    cond="{'$and':["+cond+pc+di+"]}"
                else:
                    di=",{'claim_denial_ind':'0'}"
                    cond="{'$and':["+cond+di+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$lob_id', 'total': {'$sum': 1}}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    print(str(x['_id']+"!"+str(x['total'])))
                    n_records=n_records+"}"+(str(x['_id']+"!"+str(x['total'])))
                n_records=n_records[1:]
                print(str(mon_strt))
                key_val=mon_name(mon_strt)+"-"+str(str(yr_strt)[-2:])
                val_val=n_records                
                key_lst.append(key_val)
                val_lst.append(val_val)
                cond=""
                mon_strt=mon_strt+1
                print(type(mon_strt))
                print((mon_strt))
                if (mon_strt) >= 13:
                    mon_strt=1
                    yr_strt=yr_strt+1
                
                if  (mon_strt < mon_end or mon_strt > mon_end) and (yr_strt<=yr_end):
                    bypass=1
                else:
                    break

        elif len(dur_lst) ==4:
            if len(dur_lst[1])==0:
                dur_lst[1]=['01','02','03','04','05','06','07','08','09','10','11','12']
            if len(dur_lst[2])==0:
                dur_lst[2].append(str(datetime.datetime.now().year))
            
            for dl in dur_lst[2]:
                for dl1 in dur_lst[1]:
                    cond=cond+"{'paid_date':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'paid_date':{'$regex':'"+str(dl)+"-.*-.*'}}"                    
                    if len(provider_lst) > 0:
                        pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                        di=",{'claim_denial_ind':'0'}"
                        cond="{'$and':["+cond+pc+di+"]}"
                    else:
                        di=",{'claim_denial_ind':'0'}"
                        cond="{'$and':["+cond+di+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$lob_id', 'total': {'$sum': 1}}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        print(str(x['_id']+"!"+str(x['total'])))
                        n_records=n_records+"}"+(str(x['_id']+"!"+str(x['total'])))
                    n_records=n_records[1:]
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Trend (Volume)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Line")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(key_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(val_lst)+""+","
        kv=kv[0:len(kv)-1]+"}"
        print(kv)
        kv=ast.literal_eval(kv)
        return kv

    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"

def get_paid_claim_par_trend(dur_lst,provider_lst):

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb["hfa_claims_1819"] 
        key_lst=list()
        val_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1]
            print(dur_lst)
            strt_lst=list()
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[0])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[1])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[2])
            end_lst=list()
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[0])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[1])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[2])
            yr_strt=int(str(strt_lst[0]))
            yr_end=int(str(end_lst[0]))
            mon_strt=int(str(strt_lst[1]))
            mon_end=int(str(end_lst[1]))
            while True:
                mon_frmt=""
                if mon_strt < 10:
                    mon_frmt='0'+str(mon_strt)
                else:
                    mon_frmt=str(mon_strt)
                cond=cond+"{'paid_date':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'paid_date':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                    di=",{'claim_denial_ind':'0'}"
                    cond="{'$and':["+cond+pc+di+"]}"
                else:
                    di=",{'claim_denial_ind':'0'}"
                    cond="{'$and':["+cond+di+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$claim_non_par_ind', 'total': {'$sum': 1}}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    print(str(x['_id']+"!"+str(x['total'])))
                    n_records=n_records+"}"+(str(x['_id']+"!"+str(x['total'])))
                n_records=n_records[1:]
                print(str(mon_strt))
                key_val=mon_name(mon_strt)+"-"+str(str(yr_strt)[-2:])
                val_val=n_records                
                key_lst.append(key_val)
                val_lst.append(val_val)
                cond=""
                mon_strt=mon_strt+1
                print(type(mon_strt))
                print((mon_strt))
                if (mon_strt) >= 13:
                    mon_strt=1
                    yr_strt=yr_strt+1
                
                if  (mon_strt < mon_end or mon_strt > mon_end) and (yr_strt<=yr_end):
                    bypass=1
                else:
                    break

        elif len(dur_lst) ==4:
            if len(dur_lst[1])==0:
                dur_lst[1]=['01','02','03','04','05','06','07','08','09','10','11','12']
            if len(dur_lst[2])==0:
                dur_lst[2].append(str(datetime.datetime.now().year))
            
            for dl in dur_lst[2]:
                for dl1 in dur_lst[1]:
                    cond=cond+"{'paid_date':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'paid_date':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    
                    if len(provider_lst) > 0:
                        pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                        di=",{'claim_denial_ind':'0'}"
                        cond="{'$and':["+cond+pc+di+"]}"
                    else:
                        di=",{'claim_denial_ind':'0'}"
                        cond="{'$and':["+cond+di+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$claim_non_par_ind', 'total': {'$sum': 1}}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        print(str(x['_id']+"!"+str(x['total'])))
                        n_records=n_records+"}"+(str(x['_id']+"!"+str(x['total'])))
                    n_records=n_records[1:]
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Trend (Volume)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Line")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(key_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(val_lst)+""+","
        kv=kv[0:len(kv)-1]+"}"
        print(kv)
        kv=ast.literal_eval(kv)
        return kv

    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"

def get_paid_claim_diag_cd_trend(dur_lst,provider_lst):

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb["hfa_claims_1819"] 
        key_lst=list()
        val_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1]
            print(dur_lst)
            strt_lst=list()
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[0])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[1])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[2])
            end_lst=list()
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[0])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[1])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[2])
            yr_strt=int(str(strt_lst[0]))
            yr_end=int(str(end_lst[0]))
            mon_strt=int(str(strt_lst[1]))
            mon_end=int(str(end_lst[1]))
            while True:
                mon_frmt=""
                if mon_strt < 10:
                    mon_frmt='0'+str(mon_strt)
                else:
                    mon_frmt=str(mon_strt)
                cond=cond+"{'paid_date':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'paid_date':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                    di=",{'claim_denial_ind':'0'}"
                    cond="{'$and':["+cond+pc+di+"]}"
                else:
                    di=",{'claim_denial_ind':'0'}"
                    cond="{'$and':["+cond+di+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$diag_cd', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                top_cnt=0
                for x in mydoc:
                    top_cnt=top_cnt+1
                    if top_cnt==6:
                        break
                    print(str(x['_id']+"!"+str(x['total'])))
                    n_records=n_records+"}"+(str(x['_id'].strip(' ')+"!"+str(x['total'])))
                n_records=n_records[1:]
                print(str(mon_strt))
                key_val=mon_name(mon_strt)+"-"+str(str(yr_strt)[-2:])
                val_val=n_records                
                key_lst.append(key_val)
                val_lst.append(val_val)
                cond=""
                mon_strt=mon_strt+1
                print(type(mon_strt))
                print((mon_strt))
                if (mon_strt) >= 13:
                    mon_strt=1
                    yr_strt=yr_strt+1
                
                if  (mon_strt < mon_end or mon_strt > mon_end) and (yr_strt<=yr_end):
                    bypass=1
                else:
                    break

        elif len(dur_lst) ==4:
            if len(dur_lst[1])==0:
                dur_lst[1]=['01','02','03','04','05','06','07','08','09','10','11','12']
            if len(dur_lst[2])==0:
                dur_lst[2].append(str(datetime.datetime.now().year))
            
            for dl in dur_lst[2]:
                for dl1 in dur_lst[1]:
                    cond=cond+"{'paid_date':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'paid_date':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    
                    if len(provider_lst) > 0:
                        pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                        di=",{'claim_denial_ind':'0'}"
                        cond="{'$and':["+cond+pc+di+"]}"
                    else:
                        di=",{'claim_denial_ind':'0'}"
                        cond="{'$and':["+cond+di+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$diag_cd', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    top_cnt=0
                    for x in mydoc:
                        top_cnt=top_cnt+1
                        if top_cnt==6:
                            break
                        print(str(x['_id']+"!"+str(x['total'])))
                        n_records=n_records+"}"+(str(x['_id'].strip(' ')+"!"+str(x['total'])))
                    n_records=n_records[1:]
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Trend (Volume)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Line")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(key_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(val_lst)+""+","
        kv=kv[0:len(kv)-1]+"}"
        print(kv)
        kv=ast.literal_eval(kv)
        return kv

    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"

def get_paid_claim_tat_trend(dur_lst,provider_lst):

    try:
        cond=""
        n_records="0"
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb["hfa_claims_1819"] 
        key_lst=list()
        val_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1]
            print(dur_lst)
            strt_lst=list()
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[0])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[1])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[2])
            end_lst=list()
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[0])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[1])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[2])
            yr_strt=int(str(strt_lst[0]))
            yr_end=int(str(end_lst[0]))
            mon_strt=int(str(strt_lst[1]))
            mon_end=int(str(end_lst[1]))
            while True:
                mon_frmt=""
                if mon_strt < 10:
                    mon_frmt='0'+str(mon_strt)
                else:
                    mon_frmt=str(mon_strt)
                cond=cond+"{'paid_date':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'paid_date':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                    di=",{'claim_denial_ind':'0'}"
                    cond="{'$and':["+cond+pc+di+"]}"
                else:
                    di=",{'claim_denial_ind':'0'}"
                    cond="{'$and':["+cond+di+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':None, 'total': {'$avg': {'$convert':{'input':'$fromdatetopaiddate','to':'double','onError':'0','onNull':'0'}}}}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records="0"
                for x in mydoc:
                    print(str(x['total']))
                    n_records=str(round(float(str(x['total'])),2))
                print(str(mon_strt))
                key_val=mon_name(mon_strt)+"-"+str(str(yr_strt)[-2:])
                val_val=n_records                
                key_lst.append(key_val)
                val_lst.append(val_val)
                cond=""
                mon_strt=mon_strt+1
                print(type(mon_strt))
                print((mon_strt))
                if (mon_strt) >= 13:
                    mon_strt=1
                    yr_strt=yr_strt+1
                
                if  (mon_strt < mon_end or mon_strt > mon_end) and (yr_strt<=yr_end):
                    bypass=1
                else:
                    break

        elif len(dur_lst) ==4:
            if len(dur_lst[1])==0:
                dur_lst[1]=['01','02','03','04','05','06','07','08','09','10','11','12']
            if len(dur_lst[2])==0:
                dur_lst[2].append(str(datetime.datetime.now().year))
            
            for dl in dur_lst[2]:
                for dl1 in dur_lst[1]:
                    cond=cond+"{'paid_date':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'paid_date':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    
                    if len(provider_lst) > 0:
                        pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                        di=",{'claim_denial_ind':'0'}"
                        cond="{'$and':["+cond+pc+di+"]}"
                    else:
                        di=",{'claim_denial_ind':'0'}"
                        cond="{'$and':["+cond+di+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':None, 'total': {'$avg': {'$convert':{'input':'$fromdatetopaiddate','to':'double','onError':'0','onNull':'0'}}}}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records="0"
                    for x in mydoc:
                        print(str(x['total']))
                        n_records=str(round(float(str(x['total'])),2))
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Trend (Volume)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Line")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(key_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(val_lst)+""+","
        kv=kv[0:len(kv)-1]+"}"
        print(kv)
        kv=ast.literal_eval(kv)
        return kv

    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"

def get_paid_claim_submsn_mode_trend(dur_lst,provider_lst):

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb["hfa_claims_1819"] 
        key_lst=list()
        val_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1]
            print(dur_lst)
            strt_lst=list()
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[0])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[1])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[2])
            end_lst=list()
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[0])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[1])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[2])
            yr_strt=int(str(strt_lst[0]))
            yr_end=int(str(end_lst[0]))
            mon_strt=int(str(strt_lst[1]))
            mon_end=int(str(end_lst[1]))
            while True:
                mon_frmt=""
                if mon_strt < 10:
                    mon_frmt='0'+str(mon_strt)
                else:
                    mon_frmt=str(mon_strt)
                cond=cond+"{'paid_date':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'paid_date':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                    di=",{'claim_denial_ind':'0'}"
                    cond="{'$and':["+cond+pc+di+"]}"
                else:
                    di=",{'claim_denial_ind':'0'}"
                    cond="{'$and':["+cond+di+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$claim_receipt_type_cd', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""                
                for x in mydoc:
                    print(str(x['_id']+"!"+str(x['total'])))
                    n_records=n_records+"}"+(str(x['_id'].strip(' ')+"!"+str(x['total'])))
                n_records=n_records[1:]
                print(str(mon_strt))
                key_val=mon_name(mon_strt)+"-"+str(str(yr_strt)[-2:])
                val_val=n_records                
                key_lst.append(key_val)
                val_lst.append(val_val)
                cond=""
                mon_strt=mon_strt+1
                print(type(mon_strt))
                print((mon_strt))
                if (mon_strt) >= 13:
                    mon_strt=1
                    yr_strt=yr_strt+1
                
                if  (mon_strt < mon_end or mon_strt > mon_end) and (yr_strt<=yr_end):
                    bypass=1
                else:
                    break

        elif len(dur_lst) ==4:
            if len(dur_lst[1])==0:
                dur_lst[1]=['01','02','03','04','05','06','07','08','09','10','11','12']
            if len(dur_lst[2])==0:
                dur_lst[2].append(str(datetime.datetime.now().year))
            
            for dl in dur_lst[2]:
                for dl1 in dur_lst[1]:
                    cond=cond+"{'paid_date':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'paid_date':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    
                    if len(provider_lst) > 0:
                        pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                        di=",{'claim_denial_ind':'0'}"
                        cond="{'$and':["+cond+pc+di+"]}"
                    else:
                        di=",{'claim_denial_ind':'0'}"
                        cond="{'$and':["+cond+di+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$claim_receipt_type_cd', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""                    
                    for x in mydoc:
                        print(str(x['_id']+"!"+str(x['total'])))
                        n_records=n_records+"}"+(str(x['_id'].strip(' ')+"!"+str(x['total'])))
                    n_records=n_records[1:]
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Trend (Volume)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Line")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(key_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(val_lst)+""+","
        kv=kv[0:len(kv)-1]+"}"
        print(kv)
        kv=ast.literal_eval(kv)
        return kv

    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"


def get_dend_claim_vol_trend(dur_lst,provider_lst):


    try:
        cond=""
        n_records="0"
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb["hfa_claims_1819"] 
        key_lst=list()
        val_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1]
            print(dur_lst)
            strt_lst=list()
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[0])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[1])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[2])
            end_lst=list()
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[0])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[1])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[2])
            yr_strt=int(str(strt_lst[0]))
            yr_end=int(str(end_lst[0]))
            mon_strt=int(str(strt_lst[1]))
            mon_end=int(str(end_lst[1]))
            while True:
                mon_frmt=""
                if mon_strt < 10:
                    mon_frmt='0'+str(mon_strt)
                else:
                    mon_frmt=str(mon_strt)
                cond=cond+"{'paid_date':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'paid_date':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                    # di=",{'claim_denial_ind':'1'}"
                    di=""
                    cond="{'$and':["+cond+pc+di+"]}"
                else:
                    # di=",{'claim_denial_ind':'1'}"
                    di=""
                    cond="{'$and':["+cond+di+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num', 'total': {'$min': {'$convert':{'input':'$claim_denial_ind','to':'int','onError':'0','onNull':'0'}}}}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                mylist=list(mydoc)
                mycol1=mydb["hfa_interim"]
                mycol1.drop()
                if len(mylist)==0:
                    mycol1.drop()
                else:
                    x = mycol1.insert_many(mylist)
                mydoc1 = mycol1.find({'total':1})
                n_records="0"
                n_records=str(mydoc1.count())
                mycol1.drop()
                print(n_records)
                print(str(mon_strt))
                key_val=mon_name(mon_strt)+"-"+str(str(yr_strt)[-2:])
                val_val=n_records                
                key_lst.append(key_val)
                val_lst.append(val_val)
                cond=""
                mon_strt=mon_strt+1
                print(type(mon_strt))
                print((mon_strt))
                if (mon_strt) >= 13:
                    mon_strt=1
                    yr_strt=yr_strt+1
                
                if  (mon_strt < mon_end or mon_strt > mon_end) and (yr_strt<=yr_end):
                    bypass=1
                else:
                    break

        elif len(dur_lst) ==4:
            if len(dur_lst[1])==0:
                dur_lst[1]=['01','02','03','04','05','06','07','08','09','10','11','12']
            if len(dur_lst[2])==0:
                dur_lst[2].append(str(datetime.datetime.now().year))
            
            for dl in dur_lst[2]:
                for dl1 in dur_lst[1]:
                    cond=cond+"{'paid_date':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'paid_date':{'$regex':'"+str(dl)+"-.*-.*'}}"                    
                    if len(provider_lst) > 0:
                        pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                        # di=",{'claim_denial_ind':'0'}"
                        di=""
                        cond="{'$and':["+cond+pc+di+"]}"
                    else:
                        # di=",{'claim_denial_ind':'0'}"
                        di=""
                        cond="{'$and':["+cond+di+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num', 'total': {'$min': {'$convert':{'input':'$claim_denial_ind','to':'int','onError':'0','onNull':'0'}}}}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    mylist=list(mydoc)
                    mycol1=mydb["hfa_interim"]
                    mycol1.drop()
                    if len(mylist)==0:
                        mycol1.drop()
                    else:
                        x = mycol1.insert_many(mylist)
                    mydoc1 = mycol1.find({'total':1})
                    
                    n_records="0"
                    n_records=str(mydoc1.count())
                    mycol1.drop()
                    print(n_records)
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Trend (Volume)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Line")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(key_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(val_lst)+""+","
        kv=kv[0:len(kv)-1]+"}"
        print(kv)
        kv=ast.literal_eval(kv)
        return kv

    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"


def get_dend_claim_val_trend(dur_lst,provider_lst):

    try:
        cond=""
        n_records="0"
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb["hfa_claims_1819"] 
        key_lst=list()
        val_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1]
            print(dur_lst)
            strt_lst=list()
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[0])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[1])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[2])
            end_lst=list()
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[0])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[1])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[2])
            yr_strt=int(str(strt_lst[0]))
            yr_end=int(str(end_lst[0]))
            mon_strt=int(str(strt_lst[1]))
            mon_end=int(str(end_lst[1]))
            while True:
                mon_frmt=""
                if mon_strt < 10:
                    mon_frmt='0'+str(mon_strt)
                else:
                    mon_frmt=str(mon_strt)
                cond=cond+"{'paid_date':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'paid_date':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                    # di=",{'claim_denial_ind':'0'}"
                    di=""
                    cond="{'$and':["+cond+pc+di+"]}"
                else:
                    # di=",{'claim_denial_ind':'0'}"
                    di=""
                    cond="{'$and':["+cond+di+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num', 'total': {'$min': {'$convert':{'input':'$claim_denial_ind','to':'int','onError':'0','onNull':'0'}}}}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                mylist=list(mydoc)
                mycol1=mydb["hfa_interim"]
                mycol1.drop()
                if len(mylist)==0:
                    mycol1.drop()
                else:
                    x = mycol1.insert_many(mylist)
                mylist1 = mycol1.find({'total':1}).distinct('_id')                
                mycol1.drop()
                ##
                pc1=",{'root_claim_num':{'$in':"+str(mylist1)+"}}"
                cond=cond.replace(']}',pc1+']}')
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':None, 'total': {'$sum': {'$convert':{'input':'$amt_billed','to':'double','onError':'0','onNull':'0'}}}}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records="0"
                for x in mydoc:
                    print(str(x['total']))
                    n_records=str(round(float(str(x['total'])),2))
                print(str(mon_strt))
                key_val=mon_name(mon_strt)+"-"+str(str(yr_strt)[-2:])
                val_val=n_records                
                key_lst.append(key_val)
                val_lst.append(val_val)
                cond=""
                mon_strt=mon_strt+1
                print(type(mon_strt))
                print((mon_strt))
                if (mon_strt) >= 13:
                    mon_strt=1
                    yr_strt=yr_strt+1
                
                if  (mon_strt < mon_end or mon_strt > mon_end) and (yr_strt<=yr_end):
                    bypass=1
                else:
                    break

        elif len(dur_lst) ==4:
            if len(dur_lst[1])==0:
                dur_lst[1]=['01','02','03','04','05','06','07','08','09','10','11','12']
            if len(dur_lst[2])==0:
                dur_lst[2].append(str(datetime.datetime.now().year))
            
            for dl in dur_lst[2]:
                for dl1 in dur_lst[1]:
                    cond=cond+"{'paid_date':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'paid_date':{'$regex':'"+str(dl)+"-.*-.*'}}"                    
                    if len(provider_lst) > 0:
                        pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                        # di=",{'claim_denial_ind':'0'}"
                        di=""
                        cond="{'$and':["+cond+pc+di+"]}"
                    else:
                        # di=",{'claim_denial_ind':'0'}"
                        di=""
                        cond="{'$and':["+cond+di+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num', 'total': {'$min': {'$convert':{'input':'$claim_denial_ind','to':'int','onError':'0','onNull':'0'}}}}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    mylist=list(mydoc)
                    mycol1=mydb["hfa_interim"]
                    mycol1.drop()
                    if len(mylist)==0:
                        mycol1.drop()
                    else:
                        x = mycol1.insert_many(mylist)
                    mylist1 = mycol1.find({'total':1}).distinct('_id')                
                    mycol1.drop()
                    ##
                    pc1=",{'root_claim_num':{'$in':"+str(mylist1)+"}}"
                    cond=cond.replace(']}',pc1+']}')
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':None, 'total': {'$sum': {'$convert':{'input':'$amt_billed','to':'double','onError':'0','onNull':'0'}}}}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records="0"
                    for x in mydoc:
                        print(str(x['total']))
                        n_records=str(round(float(str(x['total'])),2))
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Trend (Volume)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Line")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(key_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(val_lst)+""+","
        kv=kv[0:len(kv)-1]+"}"
        print(kv)
        kv=ast.literal_eval(kv)
        return kv

    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"

def get_dend_claim_type_trend(dur_lst,provider_lst):

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb["hfa_claims_1819"] 
        key_lst=list()
        val_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1]
            print(dur_lst)
            strt_lst=list()
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[0])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[1])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[2])
            end_lst=list()
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[0])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[1])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[2])
            yr_strt=int(str(strt_lst[0]))
            yr_end=int(str(end_lst[0]))
            mon_strt=int(str(strt_lst[1]))
            mon_end=int(str(end_lst[1]))
            while True:
                mon_frmt=""
                if mon_strt < 10:
                    mon_frmt='0'+str(mon_strt)
                else:
                    mon_frmt=str(mon_strt)
                cond=cond+"{'paid_date':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'paid_date':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                    # di=",{'claim_denial_ind':'0'}"
                    di=""
                    cond="{'$and':["+cond+pc+di+"]}"
                else:
                    # di=",{'claim_denial_ind':'0'}"
                    di=""
                    cond="{'$and':["+cond+di+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num', 'total': {'$min': {'$convert':{'input':'$claim_denial_ind','to':'int','onError':'0','onNull':'0'}}}}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                mylist=list(mydoc)
                mycol1=mydb["hfa_interim"]
                mycol1.drop()
                if len(mylist)==0:
                    mycol1.drop()
                else:
                    x = mycol1.insert_many(mylist)
                mylist1 = mycol1.find({'total':1}).distinct('_id')                
                mycol1.drop()
                ##
                pc1=",{'root_claim_num':{'$in':"+str(mylist1)+"}}"
                cond=cond.replace(']}',pc1+']}')
                print(cond)
                my_dict = ast.literal_eval(cond)   
                pipe = [{'$match':my_dict},{'$group': {'_id':'$claim_type_cd', 'total': {'$sum': 1}}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    print(str(x['_id']+"!"+str(x['total'])))
                    n_records=n_records+"}"+(str(x['_id']+"!"+str(x['total'])))
                n_records=n_records[1:]
                print(str(mon_strt))
                key_val=mon_name(mon_strt)+"-"+str(str(yr_strt)[-2:])
                val_val=n_records                
                key_lst.append(key_val)
                val_lst.append(val_val)
                cond=""
                mon_strt=mon_strt+1
                print(type(mon_strt))
                print((mon_strt))
                if (mon_strt) >= 13:
                    mon_strt=1
                    yr_strt=yr_strt+1
                
                if  (mon_strt < mon_end or mon_strt > mon_end) and (yr_strt<=yr_end):
                    bypass=1
                else:
                    break

        elif len(dur_lst) ==4:
            if len(dur_lst[1])==0:
                dur_lst[1]=['01','02','03','04','05','06','07','08','09','10','11','12']
            if len(dur_lst[2])==0:
                dur_lst[2].append(str(datetime.datetime.now().year))
            
            for dl in dur_lst[2]:
                for dl1 in dur_lst[1]:
                    cond=cond+"{'paid_date':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'paid_date':{'$regex':'"+str(dl)+"-.*-.*'}}"                    
                    if len(provider_lst) > 0:
                        pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                        # di=",{'claim_denial_ind':'0'}"
                        di=""
                        cond="{'$and':["+cond+pc+di+"]}"
                    else:
                        # di=",{'claim_denial_ind':'0'}"
                        di=""
                        cond="{'$and':["+cond+di+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num', 'total': {'$min': {'$convert':{'input':'$claim_denial_ind','to':'int','onError':'0','onNull':'0'}}}}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    mylist=list(mydoc)
                    mycol1=mydb["hfa_interim"]
                    mycol1.drop()
                    if len(mylist)==0:
                        mycol1.drop()
                    else:
                        x = mycol1.insert_many(mylist)
                    mylist1 = mycol1.find({'total':1}).distinct('_id')                
                    mycol1.drop()
                    ##
                    pc1=",{'root_claim_num':{'$in':"+str(mylist1)+"}}"
                    cond=cond.replace(']}',pc1+']}')
                    print(cond)
                    my_dict = ast.literal_eval(cond) 
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$claim_type_cd', 'total': {'$sum': 1}}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        print(str(x['_id']+"!"+str(x['total'])))
                        n_records=n_records+"}"+(str(x['_id']+"!"+str(x['total'])))
                    n_records=n_records[1:]
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Trend (Volume)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Line")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(key_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(val_lst)+""+","
        kv=kv[0:len(kv)-1]+"}"
        print(kv)
        kv=ast.literal_eval(kv)
        return kv

    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"

def get_dend_claim_lob_trend(dur_lst,provider_lst):

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb["hfa_claims_1819"] 
        key_lst=list()
        val_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1]
            print(dur_lst)
            strt_lst=list()
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[0])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[1])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[2])
            end_lst=list()
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[0])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[1])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[2])
            yr_strt=int(str(strt_lst[0]))
            yr_end=int(str(end_lst[0]))
            mon_strt=int(str(strt_lst[1]))
            mon_end=int(str(end_lst[1]))
            while True:
                mon_frmt=""
                if mon_strt < 10:
                    mon_frmt='0'+str(mon_strt)
                else:
                    mon_frmt=str(mon_strt)
                cond=cond+"{'paid_date':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'paid_date':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                    # di=",{'claim_denial_ind':'0'}"
                    di=""
                    cond="{'$and':["+cond+pc+di+"]}"
                else:
                    # di=",{'claim_denial_ind':'0'}"
                    di=""
                    cond="{'$and':["+cond+di+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num', 'total': {'$min': {'$convert':{'input':'$claim_denial_ind','to':'int','onError':'0','onNull':'0'}}}}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                mylist=list(mydoc)
                mycol1=mydb["hfa_interim"]
                mycol1.drop()
                if len(mylist)==0:
                    mycol1.drop()
                else:
                    x = mycol1.insert_many(mylist)
                mylist1 = mycol1.find({'total':1}).distinct('_id')                
                mycol1.drop()
                ##
                pc1=",{'root_claim_num':{'$in':"+str(mylist1)+"}}"
                cond=cond.replace(']}',pc1+']}')
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$lob_id', 'total': {'$sum': 1}}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    print(str(x['_id']+"!"+str(x['total'])))
                    n_records=n_records+"}"+(str(x['_id']+"!"+str(x['total'])))
                n_records=n_records[1:]
                print(str(mon_strt))
                key_val=mon_name(mon_strt)+"-"+str(str(yr_strt)[-2:])
                val_val=n_records                
                key_lst.append(key_val)
                val_lst.append(val_val)
                cond=""
                mon_strt=mon_strt+1
                print(type(mon_strt))
                print((mon_strt))
                if (mon_strt) >= 13:
                    mon_strt=1
                    yr_strt=yr_strt+1
                
                if  (mon_strt < mon_end or mon_strt > mon_end) and (yr_strt<=yr_end):
                    bypass=1
                else:
                    break

        elif len(dur_lst) ==4:
            if len(dur_lst[1])==0:
                dur_lst[1]=['01','02','03','04','05','06','07','08','09','10','11','12']
            if len(dur_lst[2])==0:
                dur_lst[2].append(str(datetime.datetime.now().year))
            
            for dl in dur_lst[2]:
                for dl1 in dur_lst[1]:
                    cond=cond+"{'paid_date':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'paid_date':{'$regex':'"+str(dl)+"-.*-.*'}}"                    
                    if len(provider_lst) > 0:
                        pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                        # di=",{'claim_denial_ind':'0'}"
                        di=""
                        cond="{'$and':["+cond+pc+di+"]}"
                    else:
                        # di=",{'claim_denial_ind':'0'}"
                        di=""
                        cond="{'$and':["+cond+di+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num', 'total': {'$min': {'$convert':{'input':'$claim_denial_ind','to':'int','onError':'0','onNull':'0'}}}}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    mylist=list(mydoc)
                    mycol1=mydb["hfa_interim"]
                    mycol1.drop()
                    if len(mylist)==0:
                        mycol1.drop()
                    else:
                        x = mycol1.insert_many(mylist)
                    mylist1 = mycol1.find({'total':1}).distinct('_id')                
                    mycol1.drop()
                    ##
                    pc1=",{'root_claim_num':{'$in':"+str(mylist1)+"}}"
                    cond=cond.replace(']}',pc1+']}')
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$lob_id', 'total': {'$sum': 1}}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        print(str(x['_id']+"!"+str(x['total'])))
                        n_records=n_records+"}"+(str(x['_id']+"!"+str(x['total'])))
                    n_records=n_records[1:]
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Trend (Volume)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Line")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(key_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(val_lst)+""+","
        kv=kv[0:len(kv)-1]+"}"
        print(kv)
        kv=ast.literal_eval(kv)
        return kv

    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"

def get_dend_claim_par_trend(dur_lst,provider_lst):

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb["hfa_claims_1819"] 
        key_lst=list()
        val_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1]
            print(dur_lst)
            strt_lst=list()
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[0])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[1])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[2])
            end_lst=list()
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[0])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[1])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[2])
            yr_strt=int(str(strt_lst[0]))
            yr_end=int(str(end_lst[0]))
            mon_strt=int(str(strt_lst[1]))
            mon_end=int(str(end_lst[1]))
            while True:
                mon_frmt=""
                if mon_strt < 10:
                    mon_frmt='0'+str(mon_strt)
                else:
                    mon_frmt=str(mon_strt)
                cond=cond+"{'paid_date':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'paid_date':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                    # di=",{'claim_denial_ind':'0'}"
                    di=""
                    cond="{'$and':["+cond+pc+di+"]}"
                else:
                    # di=",{'claim_denial_ind':'0'}"
                    di=""
                    cond="{'$and':["+cond+di+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num', 'total': {'$min': {'$convert':{'input':'$claim_denial_ind','to':'int','onError':'0','onNull':'0'}}}}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                mylist=list(mydoc)
                mycol1=mydb["hfa_interim"]
                mycol1.drop()
                if len(mylist)==0:
                    mycol1.drop()
                else:
                    x = mycol1.insert_many(mylist)
                mylist1 = mycol1.find({'total':1}).distinct('_id')                
                mycol1.drop()
                ##
                pc1=",{'root_claim_num':{'$in':"+str(mylist1)+"}}"
                cond=cond.replace(']}',pc1+']}')
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$claim_non_par_ind', 'total': {'$sum': 1}}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    print(str(x['_id']+"!"+str(x['total'])))
                    n_records=n_records+"}"+(str(x['_id']+"!"+str(x['total'])))
                n_records=n_records[1:]
                print(str(mon_strt))
                key_val=mon_name(mon_strt)+"-"+str(str(yr_strt)[-2:])
                val_val=n_records                
                key_lst.append(key_val)
                val_lst.append(val_val)
                cond=""
                mon_strt=mon_strt+1
                print(type(mon_strt))
                print((mon_strt))
                if (mon_strt) >= 13:
                    mon_strt=1
                    yr_strt=yr_strt+1
                
                if  (mon_strt < mon_end or mon_strt > mon_end) and (yr_strt<=yr_end):
                    bypass=1
                else:
                    break

        elif len(dur_lst) ==4:
            if len(dur_lst[1])==0:
                dur_lst[1]=['01','02','03','04','05','06','07','08','09','10','11','12']
            if len(dur_lst[2])==0:
                dur_lst[2].append(str(datetime.datetime.now().year))
            
            for dl in dur_lst[2]:
                for dl1 in dur_lst[1]:
                    cond=cond+"{'paid_date':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'paid_date':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    
                    if len(provider_lst) > 0:
                        pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                        # di=",{'claim_denial_ind':'0'}"
                        di=""
                        cond="{'$and':["+cond+pc+di+"]}"
                    else:
                        # di=",{'claim_denial_ind':'0'}"
                        di=""
                        cond="{'$and':["+cond+di+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num', 'total': {'$min': {'$convert':{'input':'$claim_denial_ind','to':'int','onError':'0','onNull':'0'}}}}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    mylist=list(mydoc)
                    mycol1=mydb["hfa_interim"]
                    mycol1.drop()
                    if len(mylist)==0:
                        mycol1.drop()
                    else:
                        x = mycol1.insert_many(mylist)
                    mylist1 = mycol1.find({'total':1}).distinct('_id')                
                    mycol1.drop()
                    ##
                    pc1=",{'root_claim_num':{'$in':"+str(mylist1)+"}}"
                    cond=cond.replace(']}',pc1+']}')
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$claim_non_par_ind', 'total': {'$sum': 1}}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        print(str(x['_id']+"!"+str(x['total'])))
                        n_records=n_records+"}"+(str(x['_id']+"!"+str(x['total'])))
                    n_records=n_records[1:]
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Trend (Volume)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Line")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(key_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(val_lst)+""+","
        kv=kv[0:len(kv)-1]+"}"
        print(kv)
        kv=ast.literal_eval(kv)
        return kv

    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"

def get_dend_claim_diag_cd_trend(dur_lst,provider_lst):

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb["hfa_claims_1819"] 
        key_lst=list()
        val_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1]
            print(dur_lst)
            strt_lst=list()
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[0])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[1])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[2])
            end_lst=list()
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[0])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[1])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[2])
            yr_strt=int(str(strt_lst[0]))
            yr_end=int(str(end_lst[0]))
            mon_strt=int(str(strt_lst[1]))
            mon_end=int(str(end_lst[1]))
            while True:
                mon_frmt=""
                if mon_strt < 10:
                    mon_frmt='0'+str(mon_strt)
                else:
                    mon_frmt=str(mon_strt)
                cond=cond+"{'paid_date':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'paid_date':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                    # di=",{'claim_denial_ind':'0'}"
                    di=""
                    cond="{'$and':["+cond+pc+di+"]}"
                else:
                    # di=",{'claim_denial_ind':'0'}"
                    di=""
                    cond="{'$and':["+cond+di+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num', 'total': {'$min': {'$convert':{'input':'$claim_denial_ind','to':'int','onError':'0','onNull':'0'}}}}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                mylist=list(mydoc)
                mycol1=mydb["hfa_interim"]
                mycol1.drop()
                if len(mylist)==0:
                    mycol1.drop()
                else:
                    x = mycol1.insert_many(mylist)
                mylist1 = mycol1.find({'total':1}).distinct('_id')                
                mycol1.drop()
                ##
                pc1=",{'root_claim_num':{'$in':"+str(mylist1)+"}}"
                cond=cond.replace(']}',pc1+']}')
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$diag_cd', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                top_cnt=0
                for x in mydoc:
                    top_cnt=top_cnt+1
                    if top_cnt==6:
                        break
                    print(str(x['_id']+"!"+str(x['total'])))
                    n_records=n_records+"}"+(str(x['_id'].strip(' ')+"!"+str(x['total'])))
                n_records=n_records[1:]
                print(str(mon_strt))
                key_val=mon_name(mon_strt)+"-"+str(str(yr_strt)[-2:])
                val_val=n_records                
                key_lst.append(key_val)
                val_lst.append(val_val)
                cond=""
                mon_strt=mon_strt+1
                print(type(mon_strt))
                print((mon_strt))
                if (mon_strt) >= 13:
                    mon_strt=1
                    yr_strt=yr_strt+1
                
                if  (mon_strt < mon_end or mon_strt > mon_end) and (yr_strt<=yr_end):
                    bypass=1
                else:
                    break

        elif len(dur_lst) ==4:
            if len(dur_lst[1])==0:
                dur_lst[1]=['01','02','03','04','05','06','07','08','09','10','11','12']
            if len(dur_lst[2])==0:
                dur_lst[2].append(str(datetime.datetime.now().year))
            
            for dl in dur_lst[2]:
                for dl1 in dur_lst[1]:
                    cond=cond+"{'paid_date':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'paid_date':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    
                    if len(provider_lst) > 0:
                        pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                        # di=",{'claim_denial_ind':'0'}"
                        di=""
                        cond="{'$and':["+cond+pc+di+"]}"
                    else:
                        # di=",{'claim_denial_ind':'0'}"
                        di=""
                        cond="{'$and':["+cond+di+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num', 'total': {'$min': {'$convert':{'input':'$claim_denial_ind','to':'int','onError':'0','onNull':'0'}}}}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    mylist=list(mydoc)
                    mycol1=mydb["hfa_interim"]
                    mycol1.drop()
                    if len(mylist)==0:
                        mycol1.drop()
                    else:
                        x = mycol1.insert_many(mylist)
                    mylist1 = mycol1.find({'total':1}).distinct('_id')                
                    mycol1.drop()
                    ##
                    pc1=",{'root_claim_num':{'$in':"+str(mylist1)+"}}"
                    cond=cond.replace(']}',pc1+']}')
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$diag_cd', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    top_cnt=0
                    for x in mydoc:
                        top_cnt=top_cnt+1
                        if top_cnt==6:
                            break
                        print(str(x['_id']+"!"+str(x['total'])))
                        n_records=n_records+"}"+(str(x['_id'].strip(' ')+"!"+str(x['total'])))
                    n_records=n_records[1:]
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Trend (Volume)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Line")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(key_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(val_lst)+""+","
        kv=kv[0:len(kv)-1]+"}"
        print(kv)
        kv=ast.literal_eval(kv)
        return kv

    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"

def get_dend_claim_tat_trend(dur_lst,provider_lst):

    try:
        cond=""
        n_records="0"
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb["hfa_claims_1819"] 
        key_lst=list()
        val_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1]
            print(dur_lst)
            strt_lst=list()
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[0])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[1])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[2])
            end_lst=list()
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[0])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[1])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[2])
            yr_strt=int(str(strt_lst[0]))
            yr_end=int(str(end_lst[0]))
            mon_strt=int(str(strt_lst[1]))
            mon_end=int(str(end_lst[1]))
            while True:
                mon_frmt=""
                if mon_strt < 10:
                    mon_frmt='0'+str(mon_strt)
                else:
                    mon_frmt=str(mon_strt)
                cond=cond+"{'paid_date':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'paid_date':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                    # di=",{'claim_denial_ind':'0'}"
                    di=""
                    cond="{'$and':["+cond+pc+di+"]}"
                else:
                    # di=",{'claim_denial_ind':'0'}"
                    di=""
                    cond="{'$and':["+cond+di+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num', 'total': {'$min': {'$convert':{'input':'$claim_denial_ind','to':'int','onError':'0','onNull':'0'}}}}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                mylist=list(mydoc)
                mycol1=mydb["hfa_interim"]
                mycol1.drop()
                if len(mylist)==0:
                    mycol1.drop()
                else:
                    x = mycol1.insert_many(mylist)
                mylist1 = mycol1.find({'total':1}).distinct('_id')                
                mycol1.drop()
                ##
                pc1=",{'root_claim_num':{'$in':"+str(mylist1)+"}}"
                cond=cond.replace(']}',pc1+']}')
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':None, 'total': {'$avg': {'$convert':{'input':'$fromdatetopaiddate','to':'double','onError':'0','onNull':'0'}}}}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records="0"
                for x in mydoc:
                    print(str(x['total']))
                    n_records=str(round(float(str(x['total'])),2))
                print(str(mon_strt))
                key_val=mon_name(mon_strt)+"-"+str(str(yr_strt)[-2:])
                val_val=n_records                
                key_lst.append(key_val)
                val_lst.append(val_val)
                cond=""
                mon_strt=mon_strt+1
                print(type(mon_strt))
                print((mon_strt))
                if (mon_strt) >= 13:
                    mon_strt=1
                    yr_strt=yr_strt+1
                
                if  (mon_strt < mon_end or mon_strt > mon_end) and (yr_strt<=yr_end):
                    bypass=1
                else:
                    break

        elif len(dur_lst) ==4:
            if len(dur_lst[1])==0:
                dur_lst[1]=['01','02','03','04','05','06','07','08','09','10','11','12']
            if len(dur_lst[2])==0:
                dur_lst[2].append(str(datetime.datetime.now().year))
            
            for dl in dur_lst[2]:
                for dl1 in dur_lst[1]:
                    cond=cond+"{'paid_date':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'paid_date':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    
                    if len(provider_lst) > 0:
                        pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                        # di=",{'claim_denial_ind':'0'}"
                        di=""
                        cond="{'$and':["+cond+pc+di+"]}"
                    else:
                        # di=",{'claim_denial_ind':'0'}"
                        di=""
                        cond="{'$and':["+cond+di+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num', 'total': {'$min': {'$convert':{'input':'$claim_denial_ind','to':'int','onError':'0','onNull':'0'}}}}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    mylist=list(mydoc)
                    mycol1=mydb["hfa_interim"]
                    mycol1.drop()
                    if len(mylist)==0:
                        mycol1.drop()
                    else:
                        x = mycol1.insert_many(mylist)
                    mylist1 = mycol1.find({'total':1}).distinct('_id')                
                    mycol1.drop()
                    ##
                    pc1=",{'root_claim_num':{'$in':"+str(mylist1)+"}}"
                    cond=cond.replace(']}',pc1+']}')
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':None, 'total': {'$avg': {'$convert':{'input':'$fromdatetopaiddate','to':'double','onError':'0','onNull':'0'}}}}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records="0"
                    for x in mydoc:
                        print(str(x['total']))
                        n_records=str(round(float(str(x['total'])),2))
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Trend (Volume)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Line")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(key_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(val_lst)+""+","
        kv=kv[0:len(kv)-1]+"}"
        print(kv)
        kv=ast.literal_eval(kv)
        return kv

    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"

def get_dend_claim_submsn_mode_trend(dur_lst,provider_lst):

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb["hfa_claims_1819"] 
        key_lst=list()
        val_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1]
            print(dur_lst)
            strt_lst=list()
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[0])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[1])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[2])
            end_lst=list()
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[0])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[1])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[2])
            yr_strt=int(str(strt_lst[0]))
            yr_end=int(str(end_lst[0]))
            mon_strt=int(str(strt_lst[1]))
            mon_end=int(str(end_lst[1]))
            while True:
                mon_frmt=""
                if mon_strt < 10:
                    mon_frmt='0'+str(mon_strt)
                else:
                    mon_frmt=str(mon_strt)
                cond=cond+"{'paid_date':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'paid_date':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                    # di=",{'claim_denial_ind':'0'}"
                    di=""
                    cond="{'$and':["+cond+pc+di+"]}"
                else:
                    # di=",{'claim_denial_ind':'0'}"
                    di=""
                    cond="{'$and':["+cond+di+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num', 'total': {'$min': {'$convert':{'input':'$claim_denial_ind','to':'int','onError':'0','onNull':'0'}}}}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                mylist=list(mydoc)
                mycol1=mydb["hfa_interim"]
                mycol1.drop()
                if len(mylist)==0:
                    mycol1.drop()
                else:
                    x = mycol1.insert_many(mylist)
                mylist1 = mycol1.find({'total':1}).distinct('_id')                
                mycol1.drop()
                ##
                pc1=",{'root_claim_num':{'$in':"+str(mylist1)+"}}"
                cond=cond.replace(']}',pc1+']}')
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$claim_receipt_type_cd', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""                
                for x in mydoc:
                    print(str(x['_id']+"!"+str(x['total'])))
                    n_records=n_records+"}"+(str(x['_id'].strip(' ')+"!"+str(x['total'])))
                n_records=n_records[1:]
                print(str(mon_strt))
                key_val=mon_name(mon_strt)+"-"+str(str(yr_strt)[-2:])
                val_val=n_records                
                key_lst.append(key_val)
                val_lst.append(val_val)
                cond=""
                mon_strt=mon_strt+1
                print(type(mon_strt))
                print((mon_strt))
                if (mon_strt) >= 13:
                    mon_strt=1
                    yr_strt=yr_strt+1
                
                if  (mon_strt < mon_end or mon_strt > mon_end) and (yr_strt<=yr_end):
                    bypass=1
                else:
                    break

        elif len(dur_lst) ==4:
            if len(dur_lst[1])==0:
                dur_lst[1]=['01','02','03','04','05','06','07','08','09','10','11','12']
            if len(dur_lst[2])==0:
                dur_lst[2].append(str(datetime.datetime.now().year))
            
            for dl in dur_lst[2]:
                for dl1 in dur_lst[1]:
                    cond=cond+"{'paid_date':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'paid_date':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    
                    if len(provider_lst) > 0:
                        pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                        # di=",{'claim_denial_ind':'0'}"
                        di=""
                        cond="{'$and':["+cond+pc+di+"]}"
                    else:
                        # di=",{'claim_denial_ind':'0'}"
                        di=""
                        cond="{'$and':["+cond+di+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num', 'total': {'$min': {'$convert':{'input':'$claim_denial_ind','to':'int','onError':'0','onNull':'0'}}}}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    mylist=list(mydoc)
                    mycol1=mydb["hfa_interim"]
                    mycol1.drop()
                    if len(mylist)==0:
                        mycol1.drop()
                    else:
                        x = mycol1.insert_many(mylist)
                    mylist1 = mycol1.find({'total':1}).distinct('_id')                
                    mycol1.drop()
                    ##
                    pc1=",{'root_claim_num':{'$in':"+str(mylist1)+"}}"
                    cond=cond.replace(']}',pc1+']}')
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$claim_receipt_type_cd', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""                    
                    for x in mydoc:
                        print(str(x['_id']+"!"+str(x['total'])))
                        n_records=n_records+"}"+(str(x['_id'].strip(' ')+"!"+str(x['total'])))
                    n_records=n_records[1:]
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Trend (Volume)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Line")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(key_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(val_lst)+""+","
        kv=kv[0:len(kv)-1]+"}"
        print(kv)
        kv=ast.literal_eval(kv)
        return kv

    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"


def get_prtl_dend_claim_vol_trend(dur_lst,provider_lst):


    try:
        cond=""
        n_records="0"
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb["hfa_claims_1819"] 
        key_lst=list()
        val_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1]
            print(dur_lst)
            strt_lst=list()
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[0])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[1])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[2])
            end_lst=list()
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[0])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[1])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[2])
            yr_strt=int(str(strt_lst[0]))
            yr_end=int(str(end_lst[0]))
            mon_strt=int(str(strt_lst[1]))
            mon_end=int(str(end_lst[1]))
            while True:
                mon_frmt=""
                if mon_strt < 10:
                    mon_frmt='0'+str(mon_strt)
                else:
                    mon_frmt=str(mon_strt)
                cond=cond+"{'paid_date':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'paid_date':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                    # di=",{'claim_denial_ind':'1'}"
                    di=""
                    cond="{'$and':["+cond+pc+di+"]}"
                else:
                    # di=",{'claim_denial_ind':'1'}"
                    di=""
                    cond="{'$and':["+cond+di+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num', 'total': {'$min': {'$convert':{'input':'$claim_denial_ind','to':'int','onError':'0','onNull':'0'}}},'total1': {'$max': {'$convert':{'input':'$claim_denial_ind','to':'int','onError':'0','onNull':'0'}}}}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                mylist=list(mydoc)
                mycol1=mydb["hfa_interim"]
                mycol1.drop()
                if len(mylist)==0:
                    mycol1.drop()
                else:
                    x = mycol1.insert_many(mylist)
                mydoc1 = mycol1.find({'total':0,'total1':1})
                n_records="0"
                n_records=str(mydoc1.count())
                # mycol1.drop()
                print(n_records)
                print(str(mon_strt))
                key_val=mon_name(mon_strt)+"-"+str(str(yr_strt)[-2:])
                val_val=n_records                
                key_lst.append(key_val)
                val_lst.append(val_val)
                cond=""
                mon_strt=mon_strt+1
                print(type(mon_strt))
                print((mon_strt))
                if (mon_strt) >= 13:
                    mon_strt=1
                    yr_strt=yr_strt+1
                
                if  (mon_strt < mon_end or mon_strt > mon_end) and (yr_strt<=yr_end):
                    bypass=1
                else:
                    break

        elif len(dur_lst) ==4:
            if len(dur_lst[1])==0:
                dur_lst[1]=['01','02','03','04','05','06','07','08','09','10','11','12']
            if len(dur_lst[2])==0:
                dur_lst[2].append(str(datetime.datetime.now().year))
            
            for dl in dur_lst[2]:
                for dl1 in dur_lst[1]:
                    cond=cond+"{'paid_date':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'paid_date':{'$regex':'"+str(dl)+"-.*-.*'}}"                    
                    if len(provider_lst) > 0:
                        pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                        # # di=",{'claim_denial_ind':'0'}"di=""
                        di=""
                        cond="{'$and':["+cond+pc+di+"]}"
                    else:
                        # # di=",{'claim_denial_ind':'0'}"di=""
                        di=""
                        cond="{'$and':["+cond+di+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num', 'total': {'$min': {'$convert':{'input':'$claim_denial_ind','to':'int','onError':'0','onNull':'0'}}},'total1': {'$max': {'$convert':{'input':'$claim_denial_ind','to':'int','onError':'0','onNull':'0'}}}}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    mylist=list(mydoc)
                    mycol1=mydb["hfa_interim"]
                    mycol1.drop()
                    if len(mylist)==0:
                        mycol1.drop()
                    else:
                        x = mycol1.insert_many(mylist)
                    mydoc1 = mycol1.find({'total':0,'total1':1})
                    
                    n_records="0"
                    n_records=str(mydoc1.count())
                    mycol1.drop()
                    print(n_records)
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Trend (Volume)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Line")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(key_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(val_lst)+""+","
        kv=kv[0:len(kv)-1]+"}"
        print(kv)
        kv=ast.literal_eval(kv)
        return kv

    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"


def get_prtl_dend_claim_val_trend(dur_lst,provider_lst):

    try:
        cond=""
        n_records="0"
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb["hfa_claims_1819"] 
        key_lst=list()
        val_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1]
            print(dur_lst)
            strt_lst=list()
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[0])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[1])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[2])
            end_lst=list()
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[0])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[1])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[2])
            yr_strt=int(str(strt_lst[0]))
            yr_end=int(str(end_lst[0]))
            mon_strt=int(str(strt_lst[1]))
            mon_end=int(str(end_lst[1]))
            while True:
                mon_frmt=""
                if mon_strt < 10:
                    mon_frmt='0'+str(mon_strt)
                else:
                    mon_frmt=str(mon_strt)
                cond=cond+"{'paid_date':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'paid_date':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                    # di=",{'claim_denial_ind':'0'}"di=""
                    di=""
                    cond="{'$and':["+cond+pc+di+"]}"
                else:
                    # di=",{'claim_denial_ind':'0'}"di=""
                    di=""
                    cond="{'$and':["+cond+di+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num', 'total': {'$min': {'$convert':{'input':'$claim_denial_ind','to':'int','onError':'0','onNull':'0'}}},'total1': {'$max': {'$convert':{'input':'$claim_denial_ind','to':'int','onError':'0','onNull':'0'}}}}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                mylist=list(mydoc)
                mycol1=mydb["hfa_interim"]
                mycol1.drop()
                if len(mylist)==0:
                    mycol1.drop()
                else:
                    x = mycol1.insert_many(mylist)
                mylist1 = mycol1.find({'total':0,'total1':1}).distinct('_id')                
                mycol1.drop()
                ##
                pc1=",{'root_claim_num':{'$in':"+str(mylist1)+"}}"
                cond=cond.replace(']}',pc1+']}')
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':None, 'total': {'$sum': {'$convert':{'input':'$amt_billed','to':'double','onError':'0','onNull':'0'}}}}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records="0"
                for x in mydoc:
                    print(str(x['total']))
                    n_records=str(round(float(str(x['total'])),2))
                print(str(mon_strt))
                key_val=mon_name(mon_strt)+"-"+str(str(yr_strt)[-2:])
                val_val=n_records                
                key_lst.append(key_val)
                val_lst.append(val_val)
                cond=""
                mon_strt=mon_strt+1
                print(type(mon_strt))
                print((mon_strt))
                if (mon_strt) >= 13:
                    mon_strt=1
                    yr_strt=yr_strt+1
                
                if  (mon_strt < mon_end or mon_strt > mon_end) and (yr_strt<=yr_end):
                    bypass=1
                else:
                    break

        elif len(dur_lst) ==4:
            if len(dur_lst[1])==0:
                dur_lst[1]=['01','02','03','04','05','06','07','08','09','10','11','12']
            if len(dur_lst[2])==0:
                dur_lst[2].append(str(datetime.datetime.now().year))
            
            for dl in dur_lst[2]:
                for dl1 in dur_lst[1]:
                    cond=cond+"{'paid_date':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'paid_date':{'$regex':'"+str(dl)+"-.*-.*'}}"                    
                    if len(provider_lst) > 0:
                        pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                        # di=",{'claim_denial_ind':'0'}"di=""
                        di=""
                        cond="{'$and':["+cond+pc+di+"]}"
                    else:
                        # di=",{'claim_denial_ind':'0'}"di=""
                        di=""
                        cond="{'$and':["+cond+di+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num', 'total': {'$min': {'$convert':{'input':'$claim_denial_ind','to':'int','onError':'0','onNull':'0'}}},'total1': {'$max': {'$convert':{'input':'$claim_denial_ind','to':'int','onError':'0','onNull':'0'}}}}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    mylist=list(mydoc)
                    mycol1=mydb["hfa_interim"]
                    mycol1.drop()
                    if len(mylist)==0:
                        mycol1.drop()
                    else:
                        x = mycol1.insert_many(mylist)
                    mylist1 = mycol1.find({'total':0,'total1':1}).distinct('_id')                
                    mycol1.drop()
                    ##
                    pc1=",{'root_claim_num':{'$in':"+str(mylist1)+"}}"
                    cond=cond.replace(']}',pc1+']}')
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':None, 'total': {'$sum': {'$convert':{'input':'$amt_billed','to':'double','onError':'0','onNull':'0'}}}}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records="0"
                    for x in mydoc:
                        print(str(x['total']))
                        n_records=str(round(float(str(x['total'])),2))
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Trend (Volume)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Line")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(key_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(val_lst)+""+","
        kv=kv[0:len(kv)-1]+"}"
        print(kv)
        kv=ast.literal_eval(kv)
        return kv

    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"

def get_prtl_dend_claim_type_trend(dur_lst,provider_lst):

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb["hfa_claims_1819"] 
        key_lst=list()
        val_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1]
            print(dur_lst)
            strt_lst=list()
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[0])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[1])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[2])
            end_lst=list()
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[0])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[1])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[2])
            yr_strt=int(str(strt_lst[0]))
            yr_end=int(str(end_lst[0]))
            mon_strt=int(str(strt_lst[1]))
            mon_end=int(str(end_lst[1]))
            while True:
                mon_frmt=""
                if mon_strt < 10:
                    mon_frmt='0'+str(mon_strt)
                else:
                    mon_frmt=str(mon_strt)
                cond=cond+"{'paid_date':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'paid_date':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                    # di=",{'claim_denial_ind':'0'}"di=""
                    di=""
                    cond="{'$and':["+cond+pc+di+"]}"
                else:
                    # di=",{'claim_denial_ind':'0'}"di=""
                    di=""
                    cond="{'$and':["+cond+di+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num', 'total': {'$min': {'$convert':{'input':'$claim_denial_ind','to':'int','onError':'0','onNull':'0'}}},'total1': {'$max': {'$convert':{'input':'$claim_denial_ind','to':'int','onError':'0','onNull':'0'}}}}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                mylist=list(mydoc)
                mycol1=mydb["hfa_interim"]
                mycol1.drop()
                if len(mylist)==0:
                    mycol1.drop()
                else:
                    x = mycol1.insert_many(mylist)
                mylist1 = mycol1.find({'total':0,'total1':1}).distinct('_id')                
                mycol1.drop()
                ##
                pc1=",{'root_claim_num':{'$in':"+str(mylist1)+"}}"
                cond=cond.replace(']}',pc1+']}')
                print(cond)
                my_dict = ast.literal_eval(cond)   
                pipe = [{'$match':my_dict},{'$group': {'_id':'$claim_type_cd', 'total': {'$sum': 1}}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    print(str(x['_id']+"!"+str(x['total'])))
                    n_records=n_records+"}"+(str(x['_id']+"!"+str(x['total'])))
                n_records=n_records[1:]
                print(str(mon_strt))
                key_val=mon_name(mon_strt)+"-"+str(str(yr_strt)[-2:])
                val_val=n_records                
                key_lst.append(key_val)
                val_lst.append(val_val)
                cond=""
                mon_strt=mon_strt+1
                print(type(mon_strt))
                print((mon_strt))
                if (mon_strt) >= 13:
                    mon_strt=1
                    yr_strt=yr_strt+1
                
                if  (mon_strt < mon_end or mon_strt > mon_end) and (yr_strt<=yr_end):
                    bypass=1
                else:
                    break

        elif len(dur_lst) ==4:
            if len(dur_lst[1])==0:
                dur_lst[1]=['01','02','03','04','05','06','07','08','09','10','11','12']
            if len(dur_lst[2])==0:
                dur_lst[2].append(str(datetime.datetime.now().year))
            
            for dl in dur_lst[2]:
                for dl1 in dur_lst[1]:
                    cond=cond+"{'paid_date':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'paid_date':{'$regex':'"+str(dl)+"-.*-.*'}}"                    
                    if len(provider_lst) > 0:
                        pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                        # di=",{'claim_denial_ind':'0'}"di=""
                        di=""
                        cond="{'$and':["+cond+pc+di+"]}"
                    else:
                        # di=",{'claim_denial_ind':'0'}"di=""
                        di=""
                        cond="{'$and':["+cond+di+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num', 'total': {'$min': {'$convert':{'input':'$claim_denial_ind','to':'int','onError':'0','onNull':'0'}}},'total1': {'$max': {'$convert':{'input':'$claim_denial_ind','to':'int','onError':'0','onNull':'0'}}}}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    mylist=list(mydoc)
                    mycol1=mydb["hfa_interim"]
                    mycol1.drop()
                    if len(mylist)==0:
                        mycol1.drop()
                    else:
                        x = mycol1.insert_many(mylist)
                    mylist1 = mycol1.find({'total':0,'total1':1}).distinct('_id')                
                    mycol1.drop()
                    ##
                    pc1=",{'root_claim_num':{'$in':"+str(mylist1)+"}}"
                    cond=cond.replace(']}',pc1+']}')
                    print(cond)
                    my_dict = ast.literal_eval(cond) 
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$claim_type_cd', 'total': {'$sum': 1}}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        print(str(x['_id']+"!"+str(x['total'])))
                        n_records=n_records+"}"+(str(x['_id']+"!"+str(x['total'])))
                    n_records=n_records[1:]
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Trend (Volume)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Line")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(key_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(val_lst)+""+","
        kv=kv[0:len(kv)-1]+"}"
        print(kv)
        kv=ast.literal_eval(kv)
        return kv

    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"

def get_prtl_dend_claim_lob_trend(dur_lst,provider_lst):

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb["hfa_claims_1819"] 
        key_lst=list()
        val_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1]
            print(dur_lst)
            strt_lst=list()
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[0])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[1])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[2])
            end_lst=list()
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[0])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[1])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[2])
            yr_strt=int(str(strt_lst[0]))
            yr_end=int(str(end_lst[0]))
            mon_strt=int(str(strt_lst[1]))
            mon_end=int(str(end_lst[1]))
            while True:
                mon_frmt=""
                if mon_strt < 10:
                    mon_frmt='0'+str(mon_strt)
                else:
                    mon_frmt=str(mon_strt)
                cond=cond+"{'paid_date':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'paid_date':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                    # di=",{'claim_denial_ind':'0'}"di=""
                    di=""
                    cond="{'$and':["+cond+pc+di+"]}"
                else:
                    # di=",{'claim_denial_ind':'0'}"di=""
                    di=""
                    cond="{'$and':["+cond+di+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num', 'total': {'$min': {'$convert':{'input':'$claim_denial_ind','to':'int','onError':'0','onNull':'0'}}},'total1': {'$max': {'$convert':{'input':'$claim_denial_ind','to':'int','onError':'0','onNull':'0'}}}}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                mylist=list(mydoc)
                mycol1=mydb["hfa_interim"]
                mycol1.drop()
                if len(mylist)==0:
                    mycol1.drop()
                else:
                    x = mycol1.insert_many(mylist)
                mylist1 = mycol1.find({'total':0,'total1':1}).distinct('_id')                
                mycol1.drop()
                ##
                pc1=",{'root_claim_num':{'$in':"+str(mylist1)+"}}"
                cond=cond.replace(']}',pc1+']}')
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$lob_id', 'total': {'$sum': 1}}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    print(str(x['_id']+"!"+str(x['total'])))
                    n_records=n_records+"}"+(str(x['_id']+"!"+str(x['total'])))
                n_records=n_records[1:]
                print(str(mon_strt))
                key_val=mon_name(mon_strt)+"-"+str(str(yr_strt)[-2:])
                val_val=n_records                
                key_lst.append(key_val)
                val_lst.append(val_val)
                cond=""
                mon_strt=mon_strt+1
                print(type(mon_strt))
                print((mon_strt))
                if (mon_strt) >= 13:
                    mon_strt=1
                    yr_strt=yr_strt+1
                
                if  (mon_strt < mon_end or mon_strt > mon_end) and (yr_strt<=yr_end):
                    bypass=1
                else:
                    break

        elif len(dur_lst) ==4:
            if len(dur_lst[1])==0:
                dur_lst[1]=['01','02','03','04','05','06','07','08','09','10','11','12']
            if len(dur_lst[2])==0:
                dur_lst[2].append(str(datetime.datetime.now().year))
            
            for dl in dur_lst[2]:
                for dl1 in dur_lst[1]:
                    cond=cond+"{'paid_date':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'paid_date':{'$regex':'"+str(dl)+"-.*-.*'}}"                    
                    if len(provider_lst) > 0:
                        pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                        # di=",{'claim_denial_ind':'0'}"di=""
                        di=""
                        cond="{'$and':["+cond+pc+di+"]}"
                    else:
                        # di=",{'claim_denial_ind':'0'}"di=""
                        di=""
                        cond="{'$and':["+cond+di+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num', 'total': {'$min': {'$convert':{'input':'$claim_denial_ind','to':'int','onError':'0','onNull':'0'}}},'total1': {'$max': {'$convert':{'input':'$claim_denial_ind','to':'int','onError':'0','onNull':'0'}}}}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    mylist=list(mydoc)
                    mycol1=mydb["hfa_interim"]
                    mycol1.drop()
                    if len(mylist)==0:
                        mycol1.drop()
                    else:
                        x = mycol1.insert_many(mylist)
                    mylist1 = mycol1.find({'total':0,'total1':1}).distinct('_id')                
                    mycol1.drop()
                    ##
                    pc1=",{'root_claim_num':{'$in':"+str(mylist1)+"}}"
                    cond=cond.replace(']}',pc1+']}')
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$lob_id', 'total': {'$sum': 1}}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        print(str(x['_id']+"!"+str(x['total'])))
                        n_records=n_records+"}"+(str(x['_id']+"!"+str(x['total'])))
                    n_records=n_records[1:]
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Trend (Volume)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Line")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(key_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(val_lst)+""+","
        kv=kv[0:len(kv)-1]+"}"
        print(kv)
        kv=ast.literal_eval(kv)
        return kv

    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"

def get_prtl_dend_claim_par_trend(dur_lst,provider_lst):

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb["hfa_claims_1819"] 
        key_lst=list()
        val_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1]
            print(dur_lst)
            strt_lst=list()
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[0])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[1])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[2])
            end_lst=list()
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[0])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[1])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[2])
            yr_strt=int(str(strt_lst[0]))
            yr_end=int(str(end_lst[0]))
            mon_strt=int(str(strt_lst[1]))
            mon_end=int(str(end_lst[1]))
            while True:
                mon_frmt=""
                if mon_strt < 10:
                    mon_frmt='0'+str(mon_strt)
                else:
                    mon_frmt=str(mon_strt)
                cond=cond+"{'paid_date':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'paid_date':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                    # di=",{'claim_denial_ind':'0'}"di=""
                    di=""
                    cond="{'$and':["+cond+pc+di+"]}"
                else:
                    # di=",{'claim_denial_ind':'0'}"di=""
                    di=""
                    cond="{'$and':["+cond+di+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num', 'total': {'$min': {'$convert':{'input':'$claim_denial_ind','to':'int','onError':'0','onNull':'0'}}},'total1': {'$max': {'$convert':{'input':'$claim_denial_ind','to':'int','onError':'0','onNull':'0'}}}}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                mylist=list(mydoc)
                mycol1=mydb["hfa_interim"]
                mycol1.drop()
                if len(mylist)==0:
                    mycol1.drop()
                else:
                    x = mycol1.insert_many(mylist)
                mylist1 = mycol1.find({'total':0,'total1':1}).distinct('_id')                
                mycol1.drop()
                ##
                pc1=",{'root_claim_num':{'$in':"+str(mylist1)+"}}"
                cond=cond.replace(']}',pc1+']}')
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$claim_non_par_ind', 'total': {'$sum': 1}}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    print(str(x['_id']+"!"+str(x['total'])))
                    n_records=n_records+"}"+(str(x['_id']+"!"+str(x['total'])))
                n_records=n_records[1:]
                print(str(mon_strt))
                key_val=mon_name(mon_strt)+"-"+str(str(yr_strt)[-2:])
                val_val=n_records                
                key_lst.append(key_val)
                val_lst.append(val_val)
                cond=""
                mon_strt=mon_strt+1
                print(type(mon_strt))
                print((mon_strt))
                if (mon_strt) >= 13:
                    mon_strt=1
                    yr_strt=yr_strt+1
                
                if  (mon_strt < mon_end or mon_strt > mon_end) and (yr_strt<=yr_end):
                    bypass=1
                else:
                    break

        elif len(dur_lst) ==4:
            if len(dur_lst[1])==0:
                dur_lst[1]=['01','02','03','04','05','06','07','08','09','10','11','12']
            if len(dur_lst[2])==0:
                dur_lst[2].append(str(datetime.datetime.now().year))
            
            for dl in dur_lst[2]:
                for dl1 in dur_lst[1]:
                    cond=cond+"{'paid_date':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'paid_date':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    
                    if len(provider_lst) > 0:
                        pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                        # di=",{'claim_denial_ind':'0'}"di=""
                        di=""
                        cond="{'$and':["+cond+pc+di+"]}"
                    else:
                        # di=",{'claim_denial_ind':'0'}"di=""
                        di=""
                        cond="{'$and':["+cond+di+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num', 'total': {'$min': {'$convert':{'input':'$claim_denial_ind','to':'int','onError':'0','onNull':'0'}}},'total1': {'$max': {'$convert':{'input':'$claim_denial_ind','to':'int','onError':'0','onNull':'0'}}}}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    mylist=list(mydoc)
                    mycol1=mydb["hfa_interim"]
                    mycol1.drop()
                    if len(mylist)==0:
                        mycol1.drop()
                    else:
                        x = mycol1.insert_many(mylist)
                    mylist1 = mycol1.find({'total':0,'total1':1}).distinct('_id')                
                    mycol1.drop()
                    ##
                    pc1=",{'root_claim_num':{'$in':"+str(mylist1)+"}}"
                    cond=cond.replace(']}',pc1+']}')
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$claim_non_par_ind', 'total': {'$sum': 1}}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        print(str(x['_id']+"!"+str(x['total'])))
                        n_records=n_records+"}"+(str(x['_id']+"!"+str(x['total'])))
                    n_records=n_records[1:]
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Trend (Volume)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Line")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(key_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(val_lst)+""+","
        kv=kv[0:len(kv)-1]+"}"
        print(kv)
        kv=ast.literal_eval(kv)
        return kv
    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"

def get_prtl_dend_claim_diag_cd_trend(dur_lst,provider_lst):

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb["hfa_claims_1819"] 
        key_lst=list()
        val_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1]
            print(dur_lst)
            strt_lst=list()
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[0])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[1])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[2])
            end_lst=list()
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[0])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[1])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[2])
            yr_strt=int(str(strt_lst[0]))
            yr_end=int(str(end_lst[0]))
            mon_strt=int(str(strt_lst[1]))
            mon_end=int(str(end_lst[1]))
            while True:
                mon_frmt=""
                if mon_strt < 10:
                    mon_frmt='0'+str(mon_strt)
                else:
                    mon_frmt=str(mon_strt)
                cond=cond+"{'paid_date':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'paid_date':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                    # di=",{'claim_denial_ind':'0'}"di=""
                    di=""
                    cond="{'$and':["+cond+pc+di+"]}"
                else:
                    # di=",{'claim_denial_ind':'0'}"di=""
                    di=""
                    cond="{'$and':["+cond+di+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num', 'total': {'$min': {'$convert':{'input':'$claim_denial_ind','to':'int','onError':'0','onNull':'0'}}},'total1': {'$max': {'$convert':{'input':'$claim_denial_ind','to':'int','onError':'0','onNull':'0'}}}}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                mylist=list(mydoc)
                mycol1=mydb["hfa_interim"]
                mycol1.drop()
                if len(mylist)==0:
                    mycol1.drop()
                else:
                    x = mycol1.insert_many(mylist)
                mylist1 = mycol1.find({'total':0,'total1':1}).distinct('_id')                
                mycol1.drop()
                ##
                pc1=",{'root_claim_num':{'$in':"+str(mylist1)+"}}"
                cond=cond.replace(']}',pc1+']}')
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$diag_cd', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                top_cnt=0
                for x in mydoc:
                    top_cnt=top_cnt+1
                    if top_cnt==6:
                        break
                    print(str(x['_id']+"!"+str(x['total'])))
                    n_records=n_records+"}"+(str(x['_id'].strip(' ')+"!"+str(x['total'])))
                n_records=n_records[1:]
                print(str(mon_strt))
                key_val=mon_name(mon_strt)+"-"+str(str(yr_strt)[-2:])
                val_val=n_records                
                key_lst.append(key_val)
                val_lst.append(val_val)
                cond=""
                mon_strt=mon_strt+1
                print(type(mon_strt))
                print((mon_strt))
                if (mon_strt) >= 13:
                    mon_strt=1
                    yr_strt=yr_strt+1
                
                if  (mon_strt < mon_end or mon_strt > mon_end) and (yr_strt<=yr_end):
                    bypass=1
                else:
                    break

        elif len(dur_lst) ==4:
            if len(dur_lst[1])==0:
                dur_lst[1]=['01','02','03','04','05','06','07','08','09','10','11','12']
            if len(dur_lst[2])==0:
                dur_lst[2].append(str(datetime.datetime.now().year))
            
            for dl in dur_lst[2]:
                for dl1 in dur_lst[1]:
                    cond=cond+"{'paid_date':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'paid_date':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    
                    if len(provider_lst) > 0:
                        pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                        # di=",{'claim_denial_ind':'0'}"di=""
                        di=""
                        cond="{'$and':["+cond+pc+di+"]}"
                    else:
                        # di=",{'claim_denial_ind':'0'}"di=""
                        di=""
                        cond="{'$and':["+cond+di+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num', 'total': {'$min': {'$convert':{'input':'$claim_denial_ind','to':'int','onError':'0','onNull':'0'}}},'total1': {'$max': {'$convert':{'input':'$claim_denial_ind','to':'int','onError':'0','onNull':'0'}}}}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    mylist=list(mydoc)
                    mycol1=mydb["hfa_interim"]
                    mycol1.drop()
                    if len(mylist)==0:
                        mycol1.drop()
                    else:
                        x = mycol1.insert_many(mylist)
                    mylist1 = mycol1.find({'total':0,'total1':1}).distinct('_id')                
                    mycol1.drop()
                    ##
                    pc1=",{'root_claim_num':{'$in':"+str(mylist1)+"}}"
                    cond=cond.replace(']}',pc1+']}')
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$diag_cd', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    top_cnt=0
                    for x in mydoc:
                        top_cnt=top_cnt+1
                        if top_cnt==6:
                            break
                        print(str(x['_id']+"!"+str(x['total'])))
                        n_records=n_records+"}"+(str(x['_id'].strip(' ')+"!"+str(x['total'])))
                    n_records=n_records[1:]
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Trend (Volume)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Line")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(key_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(val_lst)+""+","
        kv=kv[0:len(kv)-1]+"}"
        print(kv)
        kv=ast.literal_eval(kv)
        return kv

    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"

def get_prtl_dend_claim_tat_trend(dur_lst,provider_lst):

    try:
        cond=""
        n_records="0"
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb["hfa_claims_1819"] 
        key_lst=list()
        val_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1]
            print(dur_lst)
            strt_lst=list()
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[0])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[1])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[2])
            end_lst=list()
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[0])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[1])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[2])
            yr_strt=int(str(strt_lst[0]))
            yr_end=int(str(end_lst[0]))
            mon_strt=int(str(strt_lst[1]))
            mon_end=int(str(end_lst[1]))
            while True:
                mon_frmt=""
                if mon_strt < 10:
                    mon_frmt='0'+str(mon_strt)
                else:
                    mon_frmt=str(mon_strt)
                cond=cond+"{'paid_date':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'paid_date':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                    # di=",{'claim_denial_ind':'0'}"di=""
                    di=""
                    cond="{'$and':["+cond+pc+di+"]}"
                else:
                    # di=",{'claim_denial_ind':'0'}"di=""
                    di=""
                    cond="{'$and':["+cond+di+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num', 'total': {'$min': {'$convert':{'input':'$claim_denial_ind','to':'int','onError':'0','onNull':'0'}}},'total1': {'$max': {'$convert':{'input':'$claim_denial_ind','to':'int','onError':'0','onNull':'0'}}}}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                mylist=list(mydoc)
                mycol1=mydb["hfa_interim"]
                mycol1.drop()
                if len(mylist)==0:
                    mycol1.drop()
                else:
                    x = mycol1.insert_many(mylist)
                mylist1 = mycol1.find({'total':0,'total1':1}).distinct('_id')                
                mycol1.drop()
                ##
                pc1=",{'root_claim_num':{'$in':"+str(mylist1)+"}}"
                cond=cond.replace(']}',pc1+']}')
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':None, 'total': {'$avg': {'$convert':{'input':'$fromdatetopaiddate','to':'double','onError':'0','onNull':'0'}}}}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records="0"
                for x in mydoc:
                    print(str(x['total']))
                    n_records=str(round(float(str(x['total'])),2))
                print(str(mon_strt))
                key_val=mon_name(mon_strt)+"-"+str(str(yr_strt)[-2:])
                val_val=n_records                
                key_lst.append(key_val)
                val_lst.append(val_val)
                cond=""
                mon_strt=mon_strt+1
                print(type(mon_strt))
                print((mon_strt))
                if (mon_strt) >= 13:
                    mon_strt=1
                    yr_strt=yr_strt+1
                
                if  (mon_strt < mon_end or mon_strt > mon_end) and (yr_strt<=yr_end):
                    bypass=1
                else:
                    break

        elif len(dur_lst) ==4:
            if len(dur_lst[1])==0:
                dur_lst[1]=['01','02','03','04','05','06','07','08','09','10','11','12']
            if len(dur_lst[2])==0:
                dur_lst[2].append(str(datetime.datetime.now().year))
            
            for dl in dur_lst[2]:
                for dl1 in dur_lst[1]:
                    cond=cond+"{'paid_date':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'paid_date':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    
                    if len(provider_lst) > 0:
                        pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                        # di=",{'claim_denial_ind':'0'}"di=""
                        di=""
                        cond="{'$and':["+cond+pc+di+"]}"
                    else:
                        # di=",{'claim_denial_ind':'0'}"di=""
                        di=""
                        cond="{'$and':["+cond+di+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num', 'total': {'$min': {'$convert':{'input':'$claim_denial_ind','to':'int','onError':'0','onNull':'0'}}},'total1': {'$max': {'$convert':{'input':'$claim_denial_ind','to':'int','onError':'0','onNull':'0'}}}}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    mylist=list(mydoc)
                    mycol1=mydb["hfa_interim"]
                    mycol1.drop()
                    if len(mylist)==0:
                        mycol1.drop()
                    else:
                        x = mycol1.insert_many(mylist)
                    mylist1 = mycol1.find({'total':0,'total1':1}).distinct('_id')                
                    mycol1.drop()
                    ##
                    pc1=",{'root_claim_num':{'$in':"+str(mylist1)+"}}"
                    cond=cond.replace(']}',pc1+']}')
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':None, 'total': {'$avg': {'$convert':{'input':'$fromdatetopaiddate','to':'double','onError':'0','onNull':'0'}}}}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records="0"
                    for x in mydoc:
                        print(str(x['total']))
                        n_records=str(round(float(str(x['total'])),2))
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Trend (Volume)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Line")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(key_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(val_lst)+""+","
        kv=kv[0:len(kv)-1]+"}"
        print(kv)
        kv=ast.literal_eval(kv)
        return kv

    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"

def get_prtl_dend_claim_submsn_mode_trend(dur_lst,provider_lst):

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb["hfa_claims_1819"] 
        key_lst=list()
        val_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1]
            print(dur_lst)
            strt_lst=list()
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[0])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[1])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[2])
            end_lst=list()
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[0])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[1])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[2])
            yr_strt=int(str(strt_lst[0]))
            yr_end=int(str(end_lst[0]))
            mon_strt=int(str(strt_lst[1]))
            mon_end=int(str(end_lst[1]))
            while True:
                mon_frmt=""
                if mon_strt < 10:
                    mon_frmt='0'+str(mon_strt)
                else:
                    mon_frmt=str(mon_strt)
                cond=cond+"{'paid_date':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'paid_date':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                    # di=",{'claim_denial_ind':'0'}"di=""
                    di=""
                    cond="{'$and':["+cond+pc+di+"]}"
                else:
                    # di=",{'claim_denial_ind':'0'}"di=""
                    di=""
                    cond="{'$and':["+cond+di+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num', 'total': {'$min': {'$convert':{'input':'$claim_denial_ind','to':'int','onError':'0','onNull':'0'}}},'total1': {'$max': {'$convert':{'input':'$claim_denial_ind','to':'int','onError':'0','onNull':'0'}}}}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                mylist=list(mydoc)
                mycol1=mydb["hfa_interim"]
                mycol1.drop()
                if len(mylist)==0:
                    mycol1.drop()
                else:
                    x = mycol1.insert_many(mylist)
                mylist1 = mycol1.find({'total':0,'total1':1}).distinct('_id')                
                mycol1.drop()
                ##
                pc1=",{'root_claim_num':{'$in':"+str(mylist1)+"}}"
                cond=cond.replace(']}',pc1+']}')
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$claim_receipt_type_cd', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""                
                for x in mydoc:
                    print(str(x['_id']+"!"+str(x['total'])))
                    n_records=n_records+"}"+(str(x['_id'].strip(' ')+"!"+str(x['total'])))
                n_records=n_records[1:]
                print(str(mon_strt))
                key_val=mon_name(mon_strt)+"-"+str(str(yr_strt)[-2:])
                val_val=n_records                
                key_lst.append(key_val)
                val_lst.append(val_val)
                cond=""
                mon_strt=mon_strt+1
                print(type(mon_strt))
                print((mon_strt))
                if (mon_strt) >= 13:
                    mon_strt=1
                    yr_strt=yr_strt+1
                
                if  (mon_strt < mon_end or mon_strt > mon_end) and (yr_strt<=yr_end):
                    bypass=1
                else:
                    break

        elif len(dur_lst) ==4:
            if len(dur_lst[1])==0:
                dur_lst[1]=['01','02','03','04','05','06','07','08','09','10','11','12']
            if len(dur_lst[2])==0:
                dur_lst[2].append(str(datetime.datetime.now().year))
            
            for dl in dur_lst[2]:
                for dl1 in dur_lst[1]:
                    cond=cond+"{'paid_date':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'paid_date':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    
                    if len(provider_lst) > 0:
                        pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                        # di=",{'claim_denial_ind':'0'}"di=""
                        di=""
                        cond="{'$and':["+cond+pc+di+"]}"
                    else:
                        # di=",{'claim_denial_ind':'0'}"di=""
                        di=""
                        cond="{'$and':["+cond+di+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num', 'total': {'$min': {'$convert':{'input':'$claim_denial_ind','to':'int','onError':'0','onNull':'0'}}},'total1': {'$max': {'$convert':{'input':'$claim_denial_ind','to':'int','onError':'0','onNull':'0'}}}}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    mylist=list(mydoc)
                    mycol1=mydb["hfa_interim"]
                    mycol1.drop()
                    if len(mylist)==0:
                        mycol1.drop()
                    else:
                        x = mycol1.insert_many(mylist)
                    mylist1 = mycol1.find({'total':0,'total1':1}).distinct('_id')                
                    mycol1.drop()
                    ##
                    pc1=",{'root_claim_num':{'$in':"+str(mylist1)+"}}"
                    cond=cond.replace(']}',pc1+']}')
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$claim_receipt_type_cd', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""                    
                    for x in mydoc:
                        print(str(x['_id']+"!"+str(x['total'])))
                        n_records=n_records+"}"+(str(x['_id'].strip(' ')+"!"+str(x['total'])))
                    n_records=n_records[1:]
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Trend (Volume)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Line")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(key_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(val_lst)+""+","
        kv=kv[0:len(kv)-1]+"}"
        print(kv)
        kv=ast.literal_eval(kv)
        return kv

    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"


def get_adjstd_claim_vol_trend(dur_lst,provider_lst):

    try:
        cond=""
        n_records="0"
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb["hfa_claims_1819"] 
        key_lst=list()
        val_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1]
            print(dur_lst)
            strt_lst=list()
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[0])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[1])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[2])
            end_lst=list()
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[0])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[1])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[2])
            yr_strt=int(str(strt_lst[0]))
            yr_end=int(str(end_lst[0]))
            mon_strt=int(str(strt_lst[1]))
            mon_end=int(str(end_lst[1]))
            while True:
                mon_frmt=""
                if mon_strt < 10:
                    mon_frmt='0'+str(mon_strt)
                else:
                    mon_frmt=str(mon_strt)
                cond=cond+"{'paid_date':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'paid_date':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                    di=",{'claim_adj_ind':'1'}"
                    cond="{'$and':["+cond+pc+di+"]}"
                else:
                    di=",{'claim_adj_ind':'1'}"
                    cond="{'$and':["+cond+di+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num', 'total': {'$sum': 1}}}] ## sum after type conversion of field                              
                mydoc=list(mycol.aggregate(pipeline=pipe))
                n_records="0"
                n_records=str(len(mydoc))
                print(str(mon_strt))
                key_val=mon_name(mon_strt)+"-"+str(str(yr_strt)[-2:])
                val_val=n_records                
                key_lst.append(key_val)
                val_lst.append(val_val)
                cond=""
                mon_strt=mon_strt+1
                print(type(mon_strt))
                print((mon_strt))
                if (mon_strt) >= 13:
                    mon_strt=1
                    yr_strt=yr_strt+1
                
                if  (mon_strt < mon_end or mon_strt > mon_end) and (yr_strt<=yr_end):
                    bypass=1
                else:
                    break

        elif len(dur_lst) ==4:
            if len(dur_lst[1])==0:
                dur_lst[1]=['01','02','03','04','05','06','07','08','09','10','11','12']
            if len(dur_lst[2])==0:
                dur_lst[2].append(str(datetime.datetime.now().year))
            
            for dl in dur_lst[2]:
                for dl1 in dur_lst[1]:
                    cond=cond+"{'paid_date':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'paid_date':{'$regex':'"+str(dl)+"-.*-.*'}}"                    
                    if len(provider_lst) > 0:
                        pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                        di=",{'claim_adj_ind':'1'}"
                        cond="{'$and':["+cond+pc+di+"]}"
                    else:
                        di=",{'claim_adj_ind':'1'}"
                        cond="{'$and':["+cond+di+"]}"
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num', 'total': {'$sum': 1}}}] ## sum after type conversion of field                              
                    mydoc=list(mycol.aggregate(pipeline=pipe))
                    n_records="0"
                    n_records=str(len(mydoc))
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Trend (Volume)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Line")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(key_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(val_lst)+""+","
        kv=kv[0:len(kv)-1]+"}"
        print(kv)
        kv=ast.literal_eval(kv)
        return kv

    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"


def get_adjstd_claim_val_trend(dur_lst,provider_lst):

    try:
        cond=""
        n_records="0"
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb["hfa_claims_1819"] 
        key_lst=list()
        val_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1]
            print(dur_lst)
            strt_lst=list()
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[0])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[1])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[2])
            end_lst=list()
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[0])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[1])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[2])
            yr_strt=int(str(strt_lst[0]))
            yr_end=int(str(end_lst[0]))
            mon_strt=int(str(strt_lst[1]))
            mon_end=int(str(end_lst[1]))
            while True:
                mon_frmt=""
                if mon_strt < 10:
                    mon_frmt='0'+str(mon_strt)
                else:
                    mon_frmt=str(mon_strt)
                cond=cond+"{'paid_date':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'paid_date':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                    di=",{'claim_adj_ind':'1'}"
                    cond="{'$and':["+cond+pc+di+"]}"
                else:
                    di=",{'claim_adj_ind':'1'}"
                    cond="{'$and':["+cond+di+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':None, 'total': {'$sum': {'$convert':{'input':'$amt_paid','to':'double','onError':'0','onNull':'0'}}}}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records="0"
                for x in mydoc:
                    print(str(x['total']))
                    n_records=str(round(float(str(x['total'])),2))
                print(str(mon_strt))
                key_val=mon_name(mon_strt)+"-"+str(str(yr_strt)[-2:])
                val_val=n_records                
                key_lst.append(key_val)
                val_lst.append(val_val)
                cond=""
                mon_strt=mon_strt+1
                print(type(mon_strt))
                print((mon_strt))
                if (mon_strt) >= 13:
                    mon_strt=1
                    yr_strt=yr_strt+1
                
                if  (mon_strt < mon_end or mon_strt > mon_end) and (yr_strt<=yr_end):
                    bypass=1
                else:
                    break

        elif len(dur_lst) ==4:
            if len(dur_lst[1])==0:
                dur_lst[1]=['01','02','03','04','05','06','07','08','09','10','11','12']
            if len(dur_lst[2])==0:
                dur_lst[2].append(str(datetime.datetime.now().year))
            
            for dl in dur_lst[2]:
                for dl1 in dur_lst[1]:
                    cond=cond+"{'paid_date':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'paid_date':{'$regex':'"+str(dl)+"-.*-.*'}}"                    
                    if len(provider_lst) > 0:
                        pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                        di=",{'claim_adj_ind':'1'}"
                        cond="{'$and':["+cond+pc+di+"]}"
                    else:
                        di=",{'claim_adj_ind':'1'}"
                        cond="{'$and':["+cond+di+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':None, 'total': {'$sum': {'$convert':{'input':'$amt_paid','to':'double','onError':'0','onNull':'0'}}}}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records="0"
                    for x in mydoc:
                        print(str(x['total']))
                        n_records=str(round(float(str(x['total'])),2))
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Trend (Volume)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Line")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(key_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(val_lst)+""+","
        kv=kv[0:len(kv)-1]+"}"
        print(kv)
        kv=ast.literal_eval(kv)
        return kv

    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"

def get_adjstd_claim_type_trend(dur_lst,provider_lst):

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb["hfa_claims_1819"] 
        key_lst=list()
        val_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1]
            print(dur_lst)
            strt_lst=list()
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[0])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[1])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[2])
            end_lst=list()
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[0])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[1])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[2])
            yr_strt=int(str(strt_lst[0]))
            yr_end=int(str(end_lst[0]))
            mon_strt=int(str(strt_lst[1]))
            mon_end=int(str(end_lst[1]))
            while True:
                mon_frmt=""
                if mon_strt < 10:
                    mon_frmt='0'+str(mon_strt)
                else:
                    mon_frmt=str(mon_strt)
                cond=cond+"{'paid_date':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'paid_date':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                    di=",{'claim_adj_ind':'1'}"
                    cond="{'$and':["+cond+pc+di+"]}"
                else:
                    di=",{'claim_adj_ind':'1'}"
                    cond="{'$and':["+cond+di+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$claim_type_cd', 'total': {'$sum': 1}}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    print(str(x['_id']+"!"+str(x['total'])))
                    n_records=n_records+"}"+(str(x['_id']+"!"+str(x['total'])))
                n_records=n_records[1:]
                print(str(mon_strt))
                key_val=mon_name(mon_strt)+"-"+str(str(yr_strt)[-2:])
                val_val=n_records                
                key_lst.append(key_val)
                val_lst.append(val_val)
                cond=""
                mon_strt=mon_strt+1
                print(type(mon_strt))
                print((mon_strt))
                if (mon_strt) >= 13:
                    mon_strt=1
                    yr_strt=yr_strt+1
                
                if  (mon_strt < mon_end or mon_strt > mon_end) and (yr_strt<=yr_end):
                    bypass=1
                else:
                    break

        elif len(dur_lst) ==4:
            if len(dur_lst[1])==0:
                dur_lst[1]=['01','02','03','04','05','06','07','08','09','10','11','12']
            if len(dur_lst[2])==0:
                dur_lst[2].append(str(datetime.datetime.now().year))
            
            for dl in dur_lst[2]:
                for dl1 in dur_lst[1]:
                    cond=cond+"{'paid_date':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'paid_date':{'$regex':'"+str(dl)+"-.*-.*'}}"                    
                    if len(provider_lst) > 0:
                        pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                        di=",{'claim_adj_ind':'1'}"
                        cond="{'$and':["+cond+pc+di+"]}"
                    else:
                        di=",{'claim_adj_ind':'1'}"
                        cond="{'$and':["+cond+di+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$claim_type_cd', 'total': {'$sum': 1}}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        print(str(x['_id']+"!"+str(x['total'])))
                        n_records=n_records+"}"+(str(x['_id']+"!"+str(x['total'])))
                    n_records=n_records[1:]
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Trend (Volume)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Line")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(key_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(val_lst)+""+","
        kv=kv[0:len(kv)-1]+"}"
        print(kv)
        kv=ast.literal_eval(kv)
        return kv

    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"

def get_adjstd_claim_lob_trend(dur_lst,provider_lst):

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb["hfa_claims_1819"] 
        key_lst=list()
        val_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1]
            print(dur_lst)
            strt_lst=list()
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[0])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[1])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[2])
            end_lst=list()
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[0])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[1])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[2])
            yr_strt=int(str(strt_lst[0]))
            yr_end=int(str(end_lst[0]))
            mon_strt=int(str(strt_lst[1]))
            mon_end=int(str(end_lst[1]))
            while True:
                mon_frmt=""
                if mon_strt < 10:
                    mon_frmt='0'+str(mon_strt)
                else:
                    mon_frmt=str(mon_strt)
                cond=cond+"{'paid_date':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'paid_date':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                    di=",{'claim_adj_ind':'1'}"
                    cond="{'$and':["+cond+pc+di+"]}"
                else:
                    di=",{'claim_adj_ind':'1'}"
                    cond="{'$and':["+cond+di+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$lob_id', 'total': {'$sum': 1}}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    print(str(x['_id']+"!"+str(x['total'])))
                    n_records=n_records+"}"+(str(x['_id']+"!"+str(x['total'])))
                n_records=n_records[1:]
                print(str(mon_strt))
                key_val=mon_name(mon_strt)+"-"+str(str(yr_strt)[-2:])
                val_val=n_records                
                key_lst.append(key_val)
                val_lst.append(val_val)
                cond=""
                mon_strt=mon_strt+1
                print(type(mon_strt))
                print((mon_strt))
                if (mon_strt) >= 13:
                    mon_strt=1
                    yr_strt=yr_strt+1
                
                if  (mon_strt < mon_end or mon_strt > mon_end) and (yr_strt<=yr_end):
                    bypass=1
                else:
                    break

        elif len(dur_lst) ==4:
            if len(dur_lst[1])==0:
                dur_lst[1]=['01','02','03','04','05','06','07','08','09','10','11','12']
            if len(dur_lst[2])==0:
                dur_lst[2].append(str(datetime.datetime.now().year))
            
            for dl in dur_lst[2]:
                for dl1 in dur_lst[1]:
                    cond=cond+"{'paid_date':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'paid_date':{'$regex':'"+str(dl)+"-.*-.*'}}"                    
                    if len(provider_lst) > 0:
                        pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                        di=",{'claim_adj_ind':'1'}"
                        cond="{'$and':["+cond+pc+di+"]}"
                    else:
                        di=",{'claim_adj_ind':'1'}"
                        cond="{'$and':["+cond+di+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$lob_id', 'total': {'$sum': 1}}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        print(str(x['_id']+"!"+str(x['total'])))
                        n_records=n_records+"}"+(str(x['_id']+"!"+str(x['total'])))
                    n_records=n_records[1:]
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Trend (Volume)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Line")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(key_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(val_lst)+""+","
        kv=kv[0:len(kv)-1]+"}"
        print(kv)
        kv=ast.literal_eval(kv)
        return kv

    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"

def get_adjstd_claim_par_trend(dur_lst,provider_lst):

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb["hfa_claims_1819"] 
        key_lst=list()
        val_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1]
            print(dur_lst)
            strt_lst=list()
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[0])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[1])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[2])
            end_lst=list()
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[0])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[1])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[2])
            yr_strt=int(str(strt_lst[0]))
            yr_end=int(str(end_lst[0]))
            mon_strt=int(str(strt_lst[1]))
            mon_end=int(str(end_lst[1]))
            while True:
                mon_frmt=""
                if mon_strt < 10:
                    mon_frmt='0'+str(mon_strt)
                else:
                    mon_frmt=str(mon_strt)
                cond=cond+"{'paid_date':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'paid_date':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                    di=",{'claim_adj_ind':'1'}"
                    cond="{'$and':["+cond+pc+di+"]}"
                else:
                    di=",{'claim_adj_ind':'1'}"
                    cond="{'$and':["+cond+di+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$claim_non_par_ind', 'total': {'$sum': 1}}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    print(str(x['_id']+"!"+str(x['total'])))
                    n_records=n_records+"}"+(str(x['_id']+"!"+str(x['total'])))
                n_records=n_records[1:]
                print(str(mon_strt))
                key_val=mon_name(mon_strt)+"-"+str(str(yr_strt)[-2:])
                val_val=n_records                
                key_lst.append(key_val)
                val_lst.append(val_val)
                cond=""
                mon_strt=mon_strt+1
                print(type(mon_strt))
                print((mon_strt))
                if (mon_strt) >= 13:
                    mon_strt=1
                    yr_strt=yr_strt+1
                
                if  (mon_strt < mon_end or mon_strt > mon_end) and (yr_strt<=yr_end):
                    bypass=1
                else:
                    break

        elif len(dur_lst) ==4:
            if len(dur_lst[1])==0:
                dur_lst[1]=['01','02','03','04','05','06','07','08','09','10','11','12']
            if len(dur_lst[2])==0:
                dur_lst[2].append(str(datetime.datetime.now().year))
            
            for dl in dur_lst[2]:
                for dl1 in dur_lst[1]:
                    cond=cond+"{'paid_date':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'paid_date':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    
                    if len(provider_lst) > 0:
                        pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                        di=",{'claim_adj_ind':'1'}"
                        cond="{'$and':["+cond+pc+di+"]}"
                    else:
                        di=",{'claim_adj_ind':'1'}"
                        cond="{'$and':["+cond+di+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$claim_non_par_ind', 'total': {'$sum': 1}}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        print(str(x['_id']+"!"+str(x['total'])))
                        n_records=n_records+"}"+(str(x['_id']+"!"+str(x['total'])))
                    n_records=n_records[1:]
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Trend (Volume)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Line")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(key_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(val_lst)+""+","
        kv=kv[0:len(kv)-1]+"}"
        print(kv)
        kv=ast.literal_eval(kv)
        return kv

    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"

def get_adjstd_claim_diag_cd_trend(dur_lst,provider_lst):

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb["hfa_claims_1819"] 
        key_lst=list()
        val_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1]
            print(dur_lst)
            strt_lst=list()
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[0])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[1])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[2])
            end_lst=list()
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[0])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[1])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[2])
            yr_strt=int(str(strt_lst[0]))
            yr_end=int(str(end_lst[0]))
            mon_strt=int(str(strt_lst[1]))
            mon_end=int(str(end_lst[1]))
            while True:
                mon_frmt=""
                if mon_strt < 10:
                    mon_frmt='0'+str(mon_strt)
                else:
                    mon_frmt=str(mon_strt)
                cond=cond+"{'paid_date':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'paid_date':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                    di=",{'claim_adj_ind':'1'}"
                    cond="{'$and':["+cond+pc+di+"]}"
                else:
                    di=",{'claim_adj_ind':'1'}"
                    cond="{'$and':["+cond+di+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$diag_cd', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                top_cnt=0
                for x in mydoc:
                    top_cnt=top_cnt+1
                    if top_cnt==6:
                        break
                    print(str(x['_id']+"!"+str(x['total'])))
                    n_records=n_records+"}"+(str(x['_id'].strip(' ')+"!"+str(x['total'])))
                n_records=n_records[1:]
                print(str(mon_strt))
                key_val=mon_name(mon_strt)+"-"+str(str(yr_strt)[-2:])
                val_val=n_records                
                key_lst.append(key_val)
                val_lst.append(val_val)
                cond=""
                mon_strt=mon_strt+1
                print(type(mon_strt))
                print((mon_strt))
                if (mon_strt) >= 13:
                    mon_strt=1
                    yr_strt=yr_strt+1
                
                if  (mon_strt < mon_end or mon_strt > mon_end) and (yr_strt<=yr_end):
                    bypass=1
                else:
                    break

        elif len(dur_lst) ==4:
            if len(dur_lst[1])==0:
                dur_lst[1]=['01','02','03','04','05','06','07','08','09','10','11','12']
            if len(dur_lst[2])==0:
                dur_lst[2].append(str(datetime.datetime.now().year))
            
            for dl in dur_lst[2]:
                for dl1 in dur_lst[1]:
                    cond=cond+"{'paid_date':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'paid_date':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    
                    if len(provider_lst) > 0:
                        pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                        di=",{'claim_adj_ind':'1'}"
                        cond="{'$and':["+cond+pc+di+"]}"
                    else:
                        di=",{'claim_adj_ind':'1'}"
                        cond="{'$and':["+cond+di+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$diag_cd', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    top_cnt=0
                    for x in mydoc:
                        top_cnt=top_cnt+1
                        if top_cnt==6:
                            break
                        print(str(x['_id']+"!"+str(x['total'])))
                        n_records=n_records+"}"+(str(x['_id'].strip(' ')+"!"+str(x['total'])))
                    n_records=n_records[1:]
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Trend (Volume)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Line")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(key_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(val_lst)+""+","
        kv=kv[0:len(kv)-1]+"}"
        print(kv)
        kv=ast.literal_eval(kv)
        return kv

    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"

def get_adjstd_claim_tat_trend(dur_lst,provider_lst):

    try:
        cond=""
        n_records="0"
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb["hfa_claims_1819"] 
        key_lst=list()
        val_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1]
            print(dur_lst)
            strt_lst=list()
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[0])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[1])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[2])
            end_lst=list()
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[0])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[1])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[2])
            yr_strt=int(str(strt_lst[0]))
            yr_end=int(str(end_lst[0]))
            mon_strt=int(str(strt_lst[1]))
            mon_end=int(str(end_lst[1]))
            while True:
                mon_frmt=""
                if mon_strt < 10:
                    mon_frmt='0'+str(mon_strt)
                else:
                    mon_frmt=str(mon_strt)
                cond=cond+"{'paid_date':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'paid_date':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                    di=",{'claim_adj_ind':'1'}"
                    cond="{'$and':["+cond+pc+di+"]}"
                else:
                    di=",{'claim_adj_ind':'1'}"
                    cond="{'$and':["+cond+di+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':None, 'total': {'$avg': {'$convert':{'input':'$fromdatetopaiddate','to':'double','onError':'0','onNull':'0'}}}}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records="0"
                for x in mydoc:
                    print(str(x['total']))
                    n_records=str(round(float(str(x['total'])),2))
                print(str(mon_strt))
                key_val=mon_name(mon_strt)+"-"+str(str(yr_strt)[-2:])
                val_val=n_records                
                key_lst.append(key_val)
                val_lst.append(val_val)
                cond=""
                mon_strt=mon_strt+1
                print(type(mon_strt))
                print((mon_strt))
                if (mon_strt) >= 13:
                    mon_strt=1
                    yr_strt=yr_strt+1
                
                if  (mon_strt < mon_end or mon_strt > mon_end) and (yr_strt<=yr_end):
                    bypass=1
                else:
                    break

        elif len(dur_lst) ==4:
            if len(dur_lst[1])==0:
                dur_lst[1]=['01','02','03','04','05','06','07','08','09','10','11','12']
            if len(dur_lst[2])==0:
                dur_lst[2].append(str(datetime.datetime.now().year))
            
            for dl in dur_lst[2]:
                for dl1 in dur_lst[1]:
                    cond=cond+"{'paid_date':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'paid_date':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    
                    if len(provider_lst) > 0:
                        pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                        di=",{'claim_adj_ind':'1'}"
                        cond="{'$and':["+cond+pc+di+"]}"
                    else:
                        di=",{'claim_adj_ind':'1'}"
                        cond="{'$and':["+cond+di+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':None, 'total': {'$avg': {'$convert':{'input':'$fromdatetopaiddate','to':'double','onError':'0','onNull':'0'}}}}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records="0"
                    for x in mydoc:
                        print(str(x['total']))
                        n_records=str(round(float(str(x['total'])),2))
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Trend (Volume)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Line")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(key_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(val_lst)+""+","
        kv=kv[0:len(kv)-1]+"}"
        print(kv)
        kv=ast.literal_eval(kv)
        return kv

    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"

def get_adjstd_claim_submsn_mode_trend(dur_lst,provider_lst):

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb["hfa_claims_1819"] 
        key_lst=list()
        val_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1]
            print(dur_lst)
            strt_lst=list()
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[0])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[1])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[2])
            end_lst=list()
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[0])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[1])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[2])
            yr_strt=int(str(strt_lst[0]))
            yr_end=int(str(end_lst[0]))
            mon_strt=int(str(strt_lst[1]))
            mon_end=int(str(end_lst[1]))
            while True:
                mon_frmt=""
                if mon_strt < 10:
                    mon_frmt='0'+str(mon_strt)
                else:
                    mon_frmt=str(mon_strt)
                cond=cond+"{'paid_date':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'paid_date':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                    di=",{'claim_adj_ind':'1'}"
                    cond="{'$and':["+cond+pc+di+"]}"
                else:
                    di=",{'claim_adj_ind':'1'}"
                    cond="{'$and':["+cond+di+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$claim_receipt_type_cd', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""                
                for x in mydoc:
                    print(str(x['_id']+"!"+str(x['total'])))
                    n_records=n_records+"}"+(str(x['_id'].strip(' ')+"!"+str(x['total'])))
                n_records=n_records[1:]
                print(str(mon_strt))
                key_val=mon_name(mon_strt)+"-"+str(str(yr_strt)[-2:])
                val_val=n_records                
                key_lst.append(key_val)
                val_lst.append(val_val)
                cond=""
                mon_strt=mon_strt+1
                print(type(mon_strt))
                print((mon_strt))
                if (mon_strt) >= 13:
                    mon_strt=1
                    yr_strt=yr_strt+1
                
                if  (mon_strt < mon_end or mon_strt > mon_end) and (yr_strt<=yr_end):
                    bypass=1
                else:
                    break

        elif len(dur_lst) ==4:
            if len(dur_lst[1])==0:
                dur_lst[1]=['01','02','03','04','05','06','07','08','09','10','11','12']
            if len(dur_lst[2])==0:
                dur_lst[2].append(str(datetime.datetime.now().year))
            
            for dl in dur_lst[2]:
                for dl1 in dur_lst[1]:
                    cond=cond+"{'paid_date':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'paid_date':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    
                    if len(provider_lst) > 0:
                        pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                        di=",{'claim_adj_ind':'1'}"
                        cond="{'$and':["+cond+pc+di+"]}"
                    else:
                        di=",{'claim_adj_ind':'1'}"
                        cond="{'$and':["+cond+di+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$claim_receipt_type_cd', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""                    
                    for x in mydoc:
                        print(str(x['_id']+"!"+str(x['total'])))
                        n_records=n_records+"}"+(str(x['_id'].strip(' ')+"!"+str(x['total'])))
                    n_records=n_records[1:]
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Trend (Volume)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Line")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(key_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(val_lst)+""+","
        kv=kv[0:len(kv)-1]+"}"
        print(kv)
        kv=ast.literal_eval(kv)
        return kv

    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"


def get_adjstd_reasons_trend(dur_lst,provider_lst):

    # try:
    if True:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb["hfa_claims_1819"] 
        key_lst=list()
        val_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1]
            print(dur_lst)
            strt_lst=list()
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[0])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[1])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[2])
            end_lst=list()
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[0])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[1])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[2])
            yr_strt=int(str(strt_lst[0]))
            yr_end=int(str(end_lst[0]))
            mon_strt=int(str(strt_lst[1]))
            mon_end=int(str(end_lst[1]))
            while True:
                mon_frmt=""
                if mon_strt < 10:
                    mon_frmt='0'+str(mon_strt)
                else:
                    mon_frmt=str(mon_strt)
                cond=cond+"{'paid_date':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'paid_date':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                    di=",{'claim_adj_ind':'1'}"
                    cond="{'$and':["+cond+pc+di+"]}"
                else:
                    di=",{'claim_adj_ind':'1'}"
                    cond="{'$and':["+cond+di+"]}"
                print(cond)
                
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$adjustment_description', 'total': {'$sum': 1}}},{'$sort':{'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                cn=0
                for x in mydoc:
                    print(str(x['_id']+"!"+str(x['total'])))
                    if x['_id'].upper()=='TEXT NOT AVAILABLE':
                        continue
                    n_records=n_records+"}"+(str(x['_id']+"!"+str(x['total'])))
                    cn=cn+1
                    if cn==5:
                        break
                n_records=n_records[1:]
                print(str(mon_strt))
                key_val=mon_name(mon_strt)+"-"+str(str(yr_strt)[-2:])
                val_val=n_records                
                key_lst.append(key_val)
                val_lst.append(val_val)
                cond=""
                mon_strt=mon_strt+1
                print(type(mon_strt))
                print((mon_strt))
                if (mon_strt) >= 13:
                    mon_strt=1
                    yr_strt=yr_strt+1
                
                if  (mon_strt < mon_end or mon_strt > mon_end) and (yr_strt<=yr_end):
                    bypass=1
                else:
                    break

        elif len(dur_lst) ==4:
            if len(dur_lst[1])==0:
                dur_lst[1]=['01','02','03','04','05','06','07','08','09','10','11','12']
            if len(dur_lst[2])==0:
                dur_lst[2].append(str(datetime.datetime.now().year))
            
            for dl in dur_lst[2]:
                for dl1 in dur_lst[1]:
                    cond=cond+"{'paid_date':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'paid_date':{'$regex':'"+str(dl)+"-.*-.*'}}"                    
                    if len(provider_lst) > 0:
                        pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                        di=",{'claim_adj_ind':'1'}"
                        cond="{'$and':["+cond+pc+di+"]}"
                    else:
                        di=",{'claim_adj_ind':'1'}"
                        cond="{'$and':["+cond+di+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$adjustment_description', 'total': {'$sum': 1}}},{'$sort':{'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    cn=0
                    for x in mydoc:
                        print(str(x['_id']+"!"+str(x['total'])))
                        if x['_id'].upper()=='TEXT NOT AVAILABLE':
                            continue
                        n_records=n_records+"}"+(str(x['_id']+"!"+str(x['total'])))
                        cn=cn+1
                        if cn==5:
                            break
                    n_records=n_records[1:]
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Trend (Volume)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Line")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(key_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(val_lst)+""+","
        kv=kv[0:len(kv)-1]+"}"
        print(kv)
        kv=ast.literal_eval(kv)
        return kv
    else:
    # except Exception as e:
        # print(str(e))       
        return "Sorry, Could not fetch you results at this time"


def get_prtl_denl_reasons_trend(dur_lst,provider_lst):

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb["hfa_claims_1819"] 
        key_lst=list()
        val_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1]
            print(dur_lst)
            strt_lst=list()
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[0])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[1])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[2])
            end_lst=list()
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[0])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[1])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[2])
            yr_strt=int(str(strt_lst[0]))
            yr_end=int(str(end_lst[0]))
            mon_strt=int(str(strt_lst[1]))
            mon_end=int(str(end_lst[1]))
            while True:
                mon_frmt=""
                if mon_strt < 10:
                    mon_frmt='0'+str(mon_strt)
                else:
                    mon_frmt=str(mon_strt)
                cond=cond+"{'paid_date':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'paid_date':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                    # di=",{'claim_denial_ind':'0'}"di=""
                    di=""
                    cond="{'$and':["+cond+pc+di+"]}"
                else:
                    # di=",{'claim_denial_ind':'0'}"di=""
                    di=""
                    cond="{'$and':["+cond+di+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num', 'total': {'$min': {'$convert':{'input':'$claim_denial_ind','to':'int','onError':'0','onNull':'0'}}},'total1': {'$max': {'$convert':{'input':'$claim_denial_ind','to':'int','onError':'0','onNull':'0'}}}}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                mylist=list(mydoc)
                mycol1=mydb["hfa_interim"]
                mycol1.drop()
                if len(mylist)==0:
                    mycol1.drop()
                else:
                    x = mycol1.insert_many(mylist)
                mylist1 = mycol1.find({'total':0,'total1':1}).distinct('_id')                
                mycol1.drop()
                ##
                pc1=",{'root_claim_num':{'$in':"+str(mylist1)+"}}"
                cond=cond.replace(']}',pc1+']}')
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$denial_description', 'total': {'$sum': 1}}},{'$sort':{'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                cn=0
                for x in mydoc:
                    print(str(x['_id']+"!"+str(x['total'])))
                    if x['_id'].upper()=='TEXT NOT AVAILABLE':
                        continue
                    n_records=n_records+"}"+(str(x['_id']+"!"+str(x['total'])))
                    cn=cn+1
                    if cn==5:
                        break
                n_records=n_records[1:]
                print(str(mon_strt))
                key_val=mon_name(mon_strt)+"-"+str(str(yr_strt)[-2:])
                val_val=n_records                
                key_lst.append(key_val)
                val_lst.append(val_val)
                cond=""
                mon_strt=mon_strt+1
                print(type(mon_strt))
                print((mon_strt))
                if (mon_strt) >= 13:
                    mon_strt=1
                    yr_strt=yr_strt+1
                
                if  (mon_strt < mon_end or mon_strt > mon_end) and (yr_strt<=yr_end):
                    bypass=1
                else:
                    break

        elif len(dur_lst) ==4:
            if len(dur_lst[1])==0:
                dur_lst[1]=['01','02','03','04','05','06','07','08','09','10','11','12']
            if len(dur_lst[2])==0:
                dur_lst[2].append(str(datetime.datetime.now().year))
            
            for dl in dur_lst[2]:
                for dl1 in dur_lst[1]:
                    cond=cond+"{'paid_date':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'paid_date':{'$regex':'"+str(dl)+"-.*-.*'}}"                    
                    if len(provider_lst) > 0:
                        pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                        # di=",{'claim_denial_ind':'0'}"di=""
                        di=""
                        cond="{'$and':["+cond+pc+di+"]}"
                    else:
                        # di=",{'claim_denial_ind':'0'}"di=""
                        di=""
                        cond="{'$and':["+cond+di+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num', 'total': {'$min': {'$convert':{'input':'$claim_denial_ind','to':'int','onError':'0','onNull':'0'}}},'total1': {'$max': {'$convert':{'input':'$claim_denial_ind','to':'int','onError':'0','onNull':'0'}}}}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    mylist=list(mydoc)
                    mycol1=mydb["hfa_interim"]
                    mycol1.drop()
                    if len(mylist)==0:
                        mycol1.drop()
                    else:
                        x = mycol1.insert_many(mylist)
                    mylist1 = mycol1.find({'total':0,'total1':1}).distinct('_id')                
                    mycol1.drop()
                    ##
                    pc1=",{'root_claim_num':{'$in':"+str(mylist1)+"}}"
                    cond=cond.replace(']}',pc1+']}')
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$denial_description', 'total': {'$sum': 1}}},{'$sort':{'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    cn=0
                    for x in mydoc:
                        print(str(x['_id']+"!"+str(x['total'])))
                        if x['_id'].upper()=='TEXT NOT AVAILABLE':
                            continue
                        n_records=n_records+"}"+(str(x['_id']+"!"+str(x['total'])))
                        cn=cn+1
                        if cn==5:
                            break
                    n_records=n_records[1:]
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Trend (Volume)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Line")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(key_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(val_lst)+""+","
        kv=kv[0:len(kv)-1]+"}"
        print(kv)
        kv=ast.literal_eval(kv)
        return kv

    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"


def get_denial_reasons_trend(dur_lst,provider_lst):

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb["hfa_claims_1819"] 
        key_lst=list()
        val_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="Stack Bar"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1]
            print(dur_lst)
            strt_lst=list()
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[0])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[1])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[2])
            end_lst=list()
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[0])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[1])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[2])
            yr_strt=int(str(strt_lst[0]))
            yr_end=int(str(end_lst[0]))
            mon_strt=int(str(strt_lst[1]))
            mon_end=int(str(end_lst[1]))
            while True:
                mon_frmt=""
                if mon_strt < 10:
                    mon_frmt='0'+str(mon_strt)
                else:
                    mon_frmt=str(mon_strt)
                cond=cond+"{'paid_date':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'paid_date':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                    # di=",{'claim_denial_ind':'0'}"
                    di=""
                    cond="{'$and':["+cond+pc+di+"]}"
                else:
                    # di=",{'claim_denial_ind':'0'}"
                    di=""
                    cond="{'$and':["+cond+di+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num', 'total': {'$min': {'$convert':{'input':'$claim_denial_ind','to':'int','onError':'0','onNull':'0'}}}}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                mylist=list(mydoc)
                mycol1=mydb["hfa_interim"]
                mycol1.drop()
                if len(mylist)==0:
                    mycol1.drop()
                else:
                    x = mycol1.insert_many(mylist)
                mylist1 = mycol1.find({'total':1}).distinct('_id')                
                mycol1.drop()
                ##
                pc1=",{'root_claim_num':{'$in':"+str(mylist1)+"}}"
                cond=cond.replace(']}',pc1+']}')
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$denial_description', 'total': {'$sum': 1}}},{'$sort':{'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                cn=0
                for x in mydoc:
                    print(str(x['_id']+"!"+str(x['total'])))
                    if x['_id'].upper()=='TEXT NOT AVAILABLE':
                        continue
                    n_records=n_records+"}"+(str(x['_id']+"!"+str(x['total'])))
                    cn=cn+1
                    if cn==5:
                        break
                n_records=n_records[1:]
                print(str(mon_strt))
                key_val=mon_name(mon_strt)+"-"+str(str(yr_strt)[-2:])
                val_val=n_records                
                key_lst.append(key_val)
                val_lst.append(val_val)
                cond=""
                mon_strt=mon_strt+1
                print(type(mon_strt))
                print((mon_strt))
                if (mon_strt) >= 13:
                    mon_strt=1
                    yr_strt=yr_strt+1
                
                if  (mon_strt < mon_end or mon_strt > mon_end) and (yr_strt<=yr_end):
                    bypass=1
                else:
                    break

        elif len(dur_lst) ==4:
            if len(dur_lst[1])==0:
                dur_lst[1]=['01','02','03','04','05','06','07','08','09','10','11','12']
            if len(dur_lst[2])==0:
                dur_lst[2].append(str(datetime.datetime.now().year))
            
            for dl in dur_lst[2]:
                for dl1 in dur_lst[1]:
                    cond=cond+"{'paid_date':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'paid_date':{'$regex':'"+str(dl)+"-.*-.*'}}"                    
                    if len(provider_lst) > 0:
                        pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                        # di=",{'claim_denial_ind':'0'}"
                        di=""
                        cond="{'$and':["+cond+pc+di+"]}"
                    else:
                        # di=",{'claim_denial_ind':'0'}"
                        di=""
                        cond="{'$and':["+cond+di+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num', 'total': {'$min': {'$convert':{'input':'$claim_denial_ind','to':'int','onError':'0','onNull':'0'}}}}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    mylist=list(mydoc)
                    mycol1=mydb["hfa_interim"]
                    mycol1.drop()
                    if len(mylist)==0:
                        mycol1.drop()
                    else:
                        x = mycol1.insert_many(mylist)
                    mylist1 = mycol1.find({'total':1}).distinct('_id')                
                    mycol1.drop()
                    ##
                    pc1=",{'root_claim_num':{'$in':"+str(mylist1)+"}}"
                    cond=cond.replace(']}',pc1+']}')
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$denial_description', 'total': {'$sum': 1}}},{'$sort':{'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    cn=0
                    for x in mydoc:
                        print(str(x['_id']+"!"+str(x['total'])))
                        if x['_id'].upper()=='TEXT NOT AVAILABLE':
                            continue
                        n_records=n_records+"}"+(str(x['_id']+"!"+str(x['total'])))
                        cn=cn+1
                        if cn==5:
                            break
                    n_records=n_records[1:]
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Denial Reasons (Volume)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Stacked Bar")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(key_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(val_lst)+""+","
        kv=kv[0:len(kv)-1]+"}"
        print(kv)
        kv=ast.literal_eval(kv)
        return kv

    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"


def get_rcvd_paid_claim_vol_trend(dur_lst,provider_lst):

    try:
        cond=""
        n_records="0"
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb["hfa_claims_1819"] 
        key_lst=list()
        val_lst=list()
        r_from_dt=""
        r_end_dt=""
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1]
            print(dur_lst)
            strt_lst=list()
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[0])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[1])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[2])
            end_lst=list()
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[0])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[1])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[2])
            yr_strt=int(str(strt_lst[0]))
            yr_end=int(str(end_lst[0]))
            mon_strt=int(str(strt_lst[1]))
            mon_end=int(str(end_lst[1]))
            while True:
                mon_frmt=""
                if mon_strt < 10:
                    mon_frmt='0'+str(mon_strt)
                else:
                    mon_frmt=str(mon_strt)
                cond=cond+"{'paid_date':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'paid_date':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                cond=cond+",{'received_date':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'received_date':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                    di=",{'claim_denial_ind':'0'}"
                    cond="{'$and':["+cond+pc+di+"]}"
                else:
                    di=",{'claim_denial_ind':'0'}"
                    cond="{'$and':["+cond+di+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)                    
                mydoc = mycol.find(my_dict)
                n_records='0'
                n_records=str(mydoc.count()) 
                print(str(mon_strt))
                key_val=mon_name(mon_strt)+"-"+str(str(yr_strt)[-2:])
                val_val=n_records                
                key_lst.append(key_val)
                val_lst.append(val_val)
                cond=""
                mon_strt=mon_strt+1
                print(type(mon_strt))
                print((mon_strt))
                if (mon_strt) >= 13:
                    mon_strt=1
                    yr_strt=yr_strt+1
                
                if  (mon_strt < mon_end or mon_strt > mon_end) and (yr_strt<=yr_end):
                    bypass=1
                else:
                    break

        elif len(dur_lst) ==4:
            if len(dur_lst[1])==0:
                dur_lst[1]=['01','02','03','04','05','06','07','08','09','10','11','12']
            if len(dur_lst[2])==0:
                dur_lst[2].append(str(datetime.datetime.now().year))
            
            for dl in dur_lst[2]:
                for dl1 in dur_lst[1]:
                    cond=cond+"{'paid_date':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'paid_date':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    cond=cond+",{'received_date':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'received_date':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                        di=",{'claim_denial_ind':'0'}"
                        cond="{'$and':["+cond+pc+di+"]}"
                    else:
                        di=",{'claim_denial_ind':'0'}"
                        cond="{'$and':["+cond+di+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)                    
                    mydoc = mycol.find(my_dict)
                    n_records='0'
                    n_records=str(mydoc.count()) 
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Trend (Volume)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Line")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(key_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(val_lst)+""+","
        kv=kv[0:len(kv)-1]+"}"
        print(kv)
        kv=ast.literal_eval(kv)
        return kv

    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"

def get_payment_vol_rate(dur_lst,provider_lst):
    rcvd_res=get_rcvd_claim_vol_trend(dur_lst,provider_lst)
    rcvd_paid_res=get_rcvd_paid_claim_vol_trend(dur_lst,provider_lst)
    r_from_dt=rcvd_res["From"]
    print(str(r_from_dt))
    r_end_dt=rcvd_res["End"]
    print(str(r_end_dt))
    key_lst=list(rcvd_res["Header"])
    print(str(key_lst))
    val_lst_rcvd=list(rcvd_res["Value"])
    print(str(val_lst_rcvd))
    val_lst_rcvd_paid=list(rcvd_paid_res["Value"])
    print(str(val_lst_rcvd_paid))
    val_lst_rate=list()
    for i in range(0,len(val_lst_rcvd)):
        try:
            temp=int(val_lst_rcvd_paid[i])/int(val_lst_rcvd[i])*100
            temp=round(temp,2)
        except:
            temp=0
        val_lst_rate.append(temp)
    kv="{"
    kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
    kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
    kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Trend (Payment Rate)")+"'"+","
    kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Line")+"'"+","
    kv=kv+"'"+str("Header")+"'"+":"+""+str(key_lst)+""+","
    kv=kv+"'"+str("Value")+"'"+":"+""+str(val_lst_rate)+""+","
    kv=kv[0:len(kv)-1]+"}"
    print(kv)
    kv=ast.literal_eval(kv)
    return kv



def get_rcvd_dend_claim_vol_trend(dur_lst,provider_lst):


    try:
        cond=""
        n_records="0"
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb["hfa_claims_1819"] 
        key_lst=list()
        val_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1]
            print(dur_lst)
            strt_lst=list()
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[0])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[1])
            strt_lst.append(dur_lst[0].split(' ')[0].split('-')[2])
            end_lst=list()
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[0])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[1])
            end_lst.append(dur_lst[1].split(' ')[0].split('-')[2])
            yr_strt=int(str(strt_lst[0]))
            yr_end=int(str(end_lst[0]))
            mon_strt=int(str(strt_lst[1]))
            mon_end=int(str(end_lst[1]))
            while True:
                mon_frmt=""
                if mon_strt < 10:
                    mon_frmt='0'+str(mon_strt)
                else:
                    mon_frmt=str(mon_strt)
                cond=cond+"{'paid_date':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'paid_date':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                cond=cond+",{'received_date':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'received_date':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                    # di=",{'claim_denial_ind':'1'}"
                    di=""
                    cond="{'$and':["+cond+pc+di+"]}"
                else:
                    # di=",{'claim_denial_ind':'1'}"
                    di=""
                    cond="{'$and':["+cond+di+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num', 'total': {'$min': {'$convert':{'input':'$claim_denial_ind','to':'int','onError':'0','onNull':'0'}}}}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                mylist=list(mydoc)
                mycol1=mydb["hfa_interim"]
                mycol1.drop()
                if len(mylist)==0:
                    mycol1.drop()
                else:
                    x = mycol1.insert_many(mylist)
                mydoc1 = mycol1.find({'total':1})
                n_records="0"
                n_records=str(mydoc1.count())
                mycol1.drop()
                print(n_records)
                print(str(mon_strt))
                key_val=mon_name(mon_strt)+"-"+str(str(yr_strt)[-2:])
                val_val=n_records                
                key_lst.append(key_val)
                val_lst.append(val_val)
                cond=""
                mon_strt=mon_strt+1
                print(type(mon_strt))
                print((mon_strt))
                if (mon_strt) >= 13:
                    mon_strt=1
                    yr_strt=yr_strt+1
                
                if  (mon_strt < mon_end or mon_strt > mon_end) and (yr_strt<=yr_end):
                    bypass=1
                else:
                    break

        elif len(dur_lst) ==4:
            if len(dur_lst[1])==0:
                dur_lst[1]=['01','02','03','04','05','06','07','08','09','10','11','12']
            if len(dur_lst[2])==0:
                dur_lst[2].append(str(datetime.datetime.now().year))
            
            for dl in dur_lst[2]:
                for dl1 in dur_lst[1]:
                    cond=cond+"{'paid_date':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'paid_date':{'$regex':'"+str(dl)+"-.*-.*'}}"                      
                    cond=cond+",{'received_date':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'received_date':{'$regex':'"+str(dl)+"-.*-.*'}}"                  
                    if len(provider_lst) > 0:
                        pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                        # di=",{'claim_denial_ind':'0'}"
                        di=""
                        cond="{'$and':["+cond+pc+di+"]}"
                    else:
                        # di=",{'claim_denial_ind':'0'}"
                        di=""
                        cond="{'$and':["+cond+di+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num', 'total': {'$min': {'$convert':{'input':'$claim_denial_ind','to':'int','onError':'0','onNull':'0'}}}}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    mylist=list(mydoc)
                    mycol1=mydb["hfa_interim"]
                    mycol1.drop()
                    if len(mylist)==0:
                        mycol1.drop()
                    else:
                        x = mycol1.insert_many(mylist)
                    mydoc1 = mycol1.find({'total':1})
                    
                    n_records="0"
                    n_records=str(mydoc1.count())
                    mycol1.drop()
                    print(n_records)
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Trend (Volume)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Line")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(key_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(val_lst)+""+","
        kv=kv[0:len(kv)-1]+"}"
        print(kv)
        kv=ast.literal_eval(kv)
        return kv

    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"


def get_dend_rate_vol_rate(dur_lst,provider_lst):
    rcvd_res=get_rcvd_claim_vol_trend(dur_lst,provider_lst)
    rcvd_paid_res=get_rcvd_dend_claim_vol_trend(dur_lst,provider_lst)
    r_from_dt=rcvd_res["From"]
    print(str(r_from_dt))
    r_end_dt=rcvd_res["End"]
    print(str(r_end_dt))
    key_lst=list(rcvd_res["Header"])
    print(str(key_lst))
    val_lst_rcvd=list(rcvd_res["Value"])
    print(str(val_lst_rcvd))
    val_lst_rcvd_paid=list(rcvd_paid_res["Value"])
    print(str(val_lst_rcvd_paid))
    val_lst_rate=list()
    for i in range(0,len(val_lst_rcvd)):
        try:
            temp=int(val_lst_rcvd_paid[i])/int(val_lst_rcvd[i])*100
            temp=round(temp,2)
        except:
            temp=0
        val_lst_rate.append(temp)
    kv="{"
    kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
    kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
    kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Trend (Payment Rate)")+"'"+","
    kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Line")+"'"+","
    kv=kv+"'"+str("Header")+"'"+":"+""+str(key_lst)+""+","
    kv=kv+"'"+str("Value")+"'"+":"+""+str(val_lst_rate)+""+","
    kv=kv[0:len(kv)-1]+"}"
    print(kv)
    kv=ast.literal_eval(kv)
    return kv



# provider_lst1=['111888924','133964321']
# provider_lst1=list()
# main_fun('ud','sd','claims in last 6 months','rcvd_claim_vol_trend',provider_lst1)
# main_fun('ud','sd','claims in 2019','rcvd_claim_vol_trend',provider_lst1)
# main_fun('ud','sd','claims in last 6 months','rcvd_claim_val_trend',provider_lst1)
# main_fun('ud','sd','claims in 2019','rcvd_claim_val_trend',provider_lst1)
# main_fun('ud','sd','claims in last 6 months','rcvd_claim_type_trend',provider_lst1)
# main_fun('ud','sd','claims in 2019','rcvd_claim_type_trend',provider_lst1)
# main_fun('ud','sd','claims in last 6 months','rcvd_claim_lob_trend',provider_lst1)
# main_fun('ud','sd','claims in 2019','rcvd_claim_lob_trend',provider_lst1)
# main_fun('ud','sd','claims in last 6 months','rcvd_claim_par_trend',provider_lst1)
# main_fun('ud','sd','claims in 2019','rcvd_claim_par_trend',provider_lst1)
# main_fun('ud','sd','claims in last 6 months','rcvd_claim_diag_cd_trend',provider_lst1)
# main_fun('ud','sd','claims in 2019','rcvd_claim_diag_cd_trend',provider_lst1)
# main_fun('ud','sd','claims in last 6 months','rcvd_claim_tat_trend',provider_lst1)
# main_fun('ud','sd','claims in 2019','rcvd_claim_tat_trend',provider_lst1)
# main_fun('ud','sd','claims in last 6 months','rcvd_claim_submsn_mode_trend',provider_lst1)
# main_fun('ud','sd','claims in 2019','rcvd_claim_submsn_mode_trend',provider_lst1)
# main_fun('ud','sd','claims in last 6 months','paid_claim_vol_trend',provider_lst1)
# main_fun('ud','sd','claims in 2019','paid_claim_vol_trend',provider_lst1)
# main_fun('ud','sd','claims in last 6 months','paid_claim_val_trend',provider_lst1)
# main_fun('ud','sd','claims in 2019','paid_claim_val_trend',provider_lst1)
# main_fun('ud','sd','claims in last 6 months','paid_claim_type_trend',provider_lst1)
# main_fun('ud','sd','claims in 2019','paid_claim_type_trend',provider_lst1)
# main_fun('ud','sd','claims in last 6 months','paid_claim_lob_trend',provider_lst1)
# main_fun('ud','sd','claims in 2019','paid_claim_lob_trend',provider_lst1)
# main_fun('ud','sd','claims in last 6 months','paid_claim_par_trend',provider_lst1)
# main_fun('ud','sd','claims in 2019','paid_claim_par_trend',provider_lst1)
# main_fun('ud','sd','claims in last 6 months','paid_claim_diag_cd_trend',provider_lst1)
# main_fun('ud','sd','claims in 2019','paid_claim_diag_cd_trend',provider_lst1)
# main_fun('ud','sd','claims in last 6 months','paid_claim_tat_trend',provider_lst1)
# main_fun('ud','sd','claims in 2019','paid_claim_tat_trend',provider_lst1)
# main_fun('ud','sd','claims in last 6 months','paid_claim_submsn_mode_trend',provider_lst1)
# main_fun('ud','sd','claims in 2019','paid_claim_submsn_mode_trend',provider_lst1)
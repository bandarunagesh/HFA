import pymongo
import datetime
import calendar
import ast
import random
from pblm_solving_files.duckling_wrapper import *
from pblm_solving_files.knowledge_rev import *
import requests

def main_fun(userid,sessid,req,prov_lst,req_chart_type):
    dur_lst=list()
    dur_lst=time_extract(req)   
    print("search request "+str(req))
    print("duration list "+str(dur_lst))
    print("duration list length "+str(len(dur_lst)))
    # if len(dur_lst[len(dur_lst)-1])==0 or len(dur_lst)==0:
    if len(dur_lst)==0:
        print("entered if")
        try:
            # print(str(req)+" in "+str(datetime.now().year))
            # dur_lst=time_extract(str(req)+" in "+str(datetime.now().year))
            yr_lst=[]
            yr_lst.append(str(datetime.now().year))
            m_lst=list()
            for mi in range(0,int(str((datetime.now().month)))):
                m1=mi+1
                if m1 < 10:
                    m_lst.append("0"+str(int(str(m1)))) 
                else:
                    m_lst.append(m1)                   
            # dur_lst=[[], [], ['2019'], ['2019']]
            dur_lst.append(dur_lst)
            dur_lst.append(m_lst)
            dur_lst.append(yr_lst)
            dur_lst.append("junk")
        except Exception as e:
            print(str(e))
            junk=1
    ### to integrate with NLP ###
    print("duration list "+str(dur_lst))
    print("duration list length "+str(len(dur_lst)))
    s1=corrected_ip_string_1(req,'claims').lower()
    # context_flag=0
    # context_lst=['received','submitted','paid','adjusted','adjudicated','denied','partial denied']
    # for cl_i in context_lst:
    #     if cl_i in s1:
    #         context_flag=1
    # if context_flag==0:
    #     s1=s1+" received"
    s1=s1.replace(" value",' amount').replace("value ","amount ")
    s1=s1.replace(" claims type",' type').replace("claims type ","type ")
    if "amount" in s1.lower():
        s1=s1.replace('count ','').replace(' count','')
        if "received" in s1:
            if "paid" not in s1 and "denied" not in s1 and "adjusted" not in s1:
                s1=s1.replace(" amount",' billed amount').replace("amount ","billed amount ")
    elif "time" in s1.lower():
        s1=s1.replace('count ','').replace(' count','')
        if "claims" not in s1:
            s1=s1+" claims"            
    elif "amount" in s1.lower() or "time" in s1.lower() or "reasons" in s1.lower() or "lob" in s1.lower() or "mode" in s1.lower() or "type" in s1.lower() or "facility" in s1.lower() or "professional" in s1.lower():
        s1=s1.replace('count ','').replace(' count','')
    elif "diagnosis" in s1.lower():
        s1=s1.replace('count ','').replace(' count','').replace(" top","").replace("top ","")
    elif "top" in s1.lower():
        s1=s1.replace('count ','').replace(' count','')
        if "denied" in s1 or "adjusted" in s1:
            if "reasons" not in s1:
                s1=s1+" reasons"
    else:
        if "count" not in s1:
            s1=s1+" count"

    print("user request in search after editing "+s1)
    response = requests.get("http://apsrp03693:5088/parse",params={"q":s1})  
    
    response = response.json()
    intent = response.get("intent")
    intnt1=intent['name']   
    print(intnt1) 
    if intnt1.lower()=='claims_count':        
        if 'paid' in s1 or 'adjudicated' in s1:
            intnt="paid_claim_vol_trend"
        elif "adjusted" in s1:
            intnt="adjstd_claim_vol_trend"
        elif "partial denied" in s1:
            intnt="prtl_dend_claim_vol_trend"
        elif "denied" in s1:
            intnt="dend_claim_vol_trend"
        elif 'received' in s1 or 'submitted' in s1:
            intnt="rcvd_claim_vol_trend"
        # else:
        #     intnt="rcvd_claim_vol_trend"
    elif intnt1.lower()=='claims_paid_amt' or intnt1.lower()=='claims_dend_amt' or intnt1.lower()=='claims_billed_amt' or intnt1.lower()=='claims_adjstd_amt':        
        if 'paid' in s1 or 'adjudicated' in s1:
            intnt="paid_claim_val_trend"
        elif "adjusted" in s1:
            intnt="adjstd_claim_val_trend"
        elif "partial denied" in s1:
            intnt="prtl_dend_claim_val_trend"
        elif "denied" in s1:
            intnt="dend_claim_val_trend"
        elif 'received' in s1 or 'submitted' in s1:
            intnt="rcvd_claim_val_trend"
        # else:
        #     intnt="rcvd_claim_val_trend"
    elif intnt1.lower()=='claims_type':        
        if 'paid' in s1 or 'adjudicated' in s1:
            intnt="paid_claim_type_trend"
        elif "adjusted" in s1:
            intnt="adjstd_claim_type_trend"
        elif "partial denied" in s1:
            intnt="prtl_dend_claim_type_trend"
        elif "denied" in s1:
            intnt="dend_claim_type_trend"
        elif 'received' in s1 or 'submitted' in s1:
            intnt="rcvd_claim_type_trend"
        # else:
        #     intnt="rcvd_claim_type_trend"
    elif intnt1.lower()=='claims_lob':        
        if 'paid' in s1 or 'adjudicated' in s1:
            intnt="paid_claim_lob_trend"
        elif "adjusted" in s1:
            intnt="adjstd_claim_lob_trend"
        elif "partial denied" in s1:
            intnt="prtl_dend_claim_lob_trend"
        elif "denied" in s1:
            intnt="dend_claim_lob_trend"
        elif 'received' in s1 or 'submitted' in s1:
            intnt="rcvd_claim_lob_trend"
        # else:
        #     intnt="rcvd_claim_lob_trend"
    elif intnt1.lower()=='claims_par_non_par':        
        if 'paid' in s1 or 'adjudicated' in s1:
            intnt="paid_claim_par_trend"
        elif "adjusted" in s1:
            intnt="adjstd_claim_par_trend"
        elif "partial denied" in s1:
            intnt="prtl_dend_claim_par_trend"
        elif "denied" in s1:
            intnt="dend_claim_par_trend"
        elif 'received' in s1 or 'submitted' in s1:
            intnt="rcvd_claim_par_trend"
        # else:
        #     intnt="rcvd_claim_par_trend"
    elif intnt1.lower()=='claims_diag_codes':        
        if 'paid' in s1 or 'adjudicated' in s1:
            intnt="paid_claim_diag_cd_trend"
        elif "adjusted" in s1:
            intnt="adjstd_claim_diag_cd_trend"
        elif "partial denied" in s1:
            intnt="prtl_dend_claim_diag_cd_trend"
        elif "denied" in s1:
            intnt="dend_claim_diag_cd_trend"
        elif 'received' in s1 or 'submitted' in s1:
            intnt="rcvd_claim_diag_cd_trend"
        # else:
        #     intnt="rcvd_claim_diag_cd_trend"
    elif intnt1.lower()=='claims_tat':        
        if 'paid' in s1 or 'adjudicated' in s1:
            intnt="paid_claim_tat_trend"
        elif "adjusted" in s1:
            intnt="adjstd_claim_tat_trend"
        elif "partial denied" in s1:
            intnt="prtl_dend_claim_tat_trend"
        elif "denied" in s1:
            intnt="dend_claim_tat_trend"
        elif 'received' in s1 or 'submitted' in s1:
            intnt="rcvd_claim_tat_trend"
        # else:
        #     intnt="rcvd_claim_tat_trend"
    elif intnt1.lower()=='claims_submsn_mode':        
        if 'paid' in s1 or 'adjudicated' in s1:
            intnt="paid_claim_submsn_mode_trend"
        elif "adjusted" in s1:
            intnt="adjstd_claim_submsn_mode_trend"
        elif "partial denied" in s1:
            intnt="prtl_dend_claim_submsn_mode_trend"
        elif "denied" in s1:
            intnt="dend_claim_submsn_mode_trend"
        elif 'received' in s1 or 'submitted' in s1:
            intnt="rcvd_claim_submsn_mode_trend"
        # else:
        #     intnt="rcvd_claim_submsn_mode_trend"
    elif intnt1.lower()=='claims_action_reasons':
        if 'denied' in s1 and 'partial' in s1:
            if req_chart_type.lower()=="bar_chart_requested":
                intnt="prtl_dend_reasons_trend_bar"
            else:
                intnt="prtl_dend_reasons_trend"
            
        elif 'denied' in s1:
            if req_chart_type.lower()=="bar_chart_requested":
                intnt="dend_reasons_trend_bar"
            else:
                intnt="dend_reasons_trend"            
        elif 'adjusted' in s1:
            if req_chart_type.lower()=="bar_chart_requested":
                intnt="adjstd_reasons_trend_bar"
            else:
                intnt="adjstd_reasons_trend"
            

    ### to integrate with NLP ###

    # if req.lower()=="show me received claims count trend in 2018" or req.lower()=="show me received claims count trend in last six months":
    #     intnt="rcvd_claim_vol_trend"
    # elif req.lower()=="show me received claims value trend in 2018" or req.lower()=="show me received claims value trend in last six months":
    #     intnt="rcvd_claim_val_trend"
    # elif req.lower()=="show me received claims type trend in 2018" or req.lower()=="show me received claims type trend in last six months":
    #     intnt="rcvd_claim_type_trend"
    # elif req.lower()=="show me received claims lob trend in 2018" or req.lower()=="show me received claims lob trend in last six months":
    #     intnt="rcvd_claim_lob_trend"
    # elif req.lower()=="show me denied claims count trend in 2018" or req.lower()=="show me denied claims count trend in last six months":
    #     intnt="dend_claim_vol_trend"
    # elif req.lower()=="show me denied claims value trend in 2018" or req.lower()=="show me denied claims value trend in last six months":
    #     intnt="dend_claim_val_trend"
    # elif req.lower()=="show me denied claims type trend in 2018" or req.lower()=="show me denied claims type trend in last six months":
    #     intnt="dend_claim_type_trend"
    # elif req.lower()=="show me denied claims lob trend in 2018" or req.lower()=="show me denied claims lob trend in last six months":
    #     intnt="dend_claim_lob_trend"
    # elif req.lower()=="show me top denials in 2018" or req.lower()=="show me top denials in last six months":
    #     if req_chart_type.lower()=="bar_chart_requested":
    #         intnt="dend_reasons_trend_bar"
    #     else:
    #         intnt="dend_reasons_trend"

    if intnt=="rcvd_claim_vol_trend":
        return get_rcvd_claim_vol_trend(dur_lst,prov_lst)
    elif intnt=="adjstd_reasons_trend_bar":
        return get_adjstd_reasons_trend_bar(dur_lst,prov_lst)
    elif intnt=="prtl_dend_reasons_trend_bar":
        return get_prtl_denial_reasons_trend_bar(dur_lst,prov_lst)
    elif intnt=="dend_reasons_trend_bar":
        return get_denial_reasons_trend_bar(dur_lst,prov_lst)
    elif intnt=="rcvd_claim_val_trend":
        return (get_rcvd_claim_val_trend(dur_lst,prov_lst))
    elif intnt=="rcvd_claim_type_trend":
        return (get_rcvd_claim_type_trend(dur_lst,prov_lst))
    elif intnt=="rcvd_claim_lob_trend":
        return (get_rcvd_claim_lob_trend(dur_lst,prov_lst))
    elif intnt=="rcvd_claim_par_trend":
        return (get_rcvd_claim_par_trend(dur_lst,prov_lst))
    elif intnt=="rcvd_claim_diag_cd_trend":
        return (get_rcvd_claim_diag_cd_trend(dur_lst,prov_lst))
    elif intnt=="rcvd_claim_tat_trend":
        return (get_rcvd_claim_tat_trend(dur_lst,prov_lst))
    elif intnt=="rcvd_claim_submsn_mode_trend":
        return (get_rcvd_claim_submsn_mode_trend(dur_lst,prov_lst))
    elif intnt=="paid_claim_vol_trend":
        return (get_paid_claim_vol_trend(dur_lst,prov_lst))
    elif intnt=="paid_claim_val_trend":
        return (get_paid_claim_val_trend(dur_lst,prov_lst))
    elif intnt=="paid_claim_type_trend":
        return (get_paid_claim_type_trend(dur_lst,prov_lst))
    elif intnt=="paid_claim_lob_trend":
        return (get_paid_claim_lob_trend(dur_lst,prov_lst))
    elif intnt=="paid_claim_par_trend":
        return (get_paid_claim_par_trend(dur_lst,prov_lst))
    elif intnt=="paid_claim_diag_cd_trend":
        return (get_paid_claim_diag_cd_trend(dur_lst,prov_lst))
    elif intnt=="paid_claim_tat_trend":
        return (get_paid_claim_tat_trend(dur_lst,prov_lst))
    elif intnt=="paid_claim_submsn_mode_trend":
        return (get_paid_claim_submsn_mode_trend(dur_lst,prov_lst))
    elif intnt=="dend_claim_vol_trend":
        return (get_dend_claim_vol_trend(dur_lst,prov_lst))
    elif intnt=="dend_claim_val_trend":
        return (get_dend_claim_val_trend(dur_lst,prov_lst))
    elif intnt=="dend_claim_type_trend":
        return (get_dend_claim_type_trend(dur_lst,prov_lst))
    elif intnt=="dend_claim_lob_trend":
        return (get_dend_claim_lob_trend(dur_lst,prov_lst))
    elif intnt=="dend_claim_par_trend":
        return (get_dend_claim_par_trend(dur_lst,prov_lst))
    elif intnt=="dend_claim_diag_cd_trend":
        return (get_dend_claim_diag_cd_trend(dur_lst,prov_lst))
    elif intnt=="dend_claim_tat_trend":
        return (get_dend_claim_tat_trend(dur_lst,prov_lst))
    elif intnt=="dend_claim_submsn_mode_trend":
        return (get_dend_claim_submsn_mode_trend(dur_lst,prov_lst))
    elif intnt=="prtl_dend_claim_vol_trend":
        return (get_prtl_dend_claim_vol_trend(dur_lst,prov_lst))
    elif intnt=="prtl_dend_claim_val_trend":
        return (get_prtl_dend_claim_val_trend(dur_lst,prov_lst))
    elif intnt=="prtl_dend_claim_type_trend":
        return (get_prtl_dend_claim_type_trend(dur_lst,prov_lst))
    elif intnt=="prtl_dend_claim_lob_trend":
        return (get_prtl_dend_claim_lob_trend(dur_lst,prov_lst))
    elif intnt=="prtl_dend_claim_par_trend":
        return (get_prtl_dend_claim_par_trend(dur_lst,prov_lst))
    elif intnt=="prtl_dend_claim_diag_cd_trend":
        return (get_prtl_dend_claim_diag_cd_trend(dur_lst,prov_lst))
    elif intnt=="prtl_dend_claim_tat_trend":
        return (get_prtl_dend_claim_tat_trend(dur_lst,prov_lst))
    elif intnt=="prtl_dend_claim_submsn_mode_trend":
        return (get_prtl_dend_claim_submsn_mode_trend(dur_lst,prov_lst))
    elif intnt=="adjstd_claim_vol_trend":
        return (get_adjstd_claim_vol_trend(dur_lst,prov_lst))
    elif intnt=="adjstd_claim_val_trend":
        return (get_adjstd_claim_val_trend(dur_lst,prov_lst))
    elif intnt=="adjstd_claim_type_trend":
        return (get_adjstd_claim_type_trend(dur_lst,prov_lst))
    elif intnt=="adjstd_claim_lob_trend":
        return (get_adjstd_claim_lob_trend(dur_lst,prov_lst))
    elif intnt=="adjstd_claim_par_trend":
        return (get_adjstd_claim_par_trend(dur_lst,prov_lst))
    elif intnt=="adjstd_claim_diag_cd_trend":
        return (get_adjstd_claim_diag_cd_trend(dur_lst,prov_lst))
    elif intnt=="adjstd_claim_tat_trend":
        return (get_adjstd_claim_tat_trend(dur_lst,prov_lst))
    elif intnt=="adjstd_claim_submsn_mode_trend":
        return (get_adjstd_claim_submsn_mode_trend(dur_lst,prov_lst))
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
            r_end_dt=dur_lst[1].split('}')[0]
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
            r_end_dt=dur_lst[1].split('}')[0]
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
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Trend (Value)")+"'"+","
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
        claim_type_lst=list()
        cliam_type_cnt_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1].split('}')[0]
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
                pipe = [{'$match':my_dict},{'$group': {'_id':'$claim_type_cd', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    print(str(x['_id']+"!"+str(x['total'])))
                    if x['_id'] in claim_type_lst:
                        cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(int(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+int(x['total']))
                    else:
                        claim_type_lst.append(str(x['_id']))
                        cliam_type_cnt_lst.append(str(x['total']))                    
                
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
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$claim_type_cd', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        print(str(x['_id']+"!"+str(x['total'])))
                        if x['_id'] in claim_type_lst:
                            cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(int(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+int(x['total']))
                        else:
                            claim_type_lst.append(str(x['_id']))
                            cliam_type_cnt_lst.append(str(x['total'])) 
                    
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        for cti in range(0,len(claim_type_lst)):
            claim_type_lst[cti]=claim_type_lst[cti].lower().replace('m','Professional').replace('h','Facility')
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Volume (By Claim Type)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Bar")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(claim_type_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(cliam_type_cnt_lst)+""+","
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
        claim_type_lst=list()
        cliam_type_cnt_lst=list() 
        key_lst=list()
        val_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1].split('}')[0]
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
                pipe = [{'$match':my_dict},{'$group': {'_id':'$lob_id', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    if x['_id'] in claim_type_lst:
                        cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(int(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+int(x['total']))
                    else:
                        claim_type_lst.append(str(x['_id']))
                        cliam_type_cnt_lst.append(str(x['total'])) 
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
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$lob_id', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        if x['_id'] in claim_type_lst:
                            cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(int(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+int(x['total']))
                        else:
                            claim_type_lst.append(str(x['_id']))
                            cliam_type_cnt_lst.append(str(x['total'])) 
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        for li in range(0,len(claim_type_lst)):
            claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Volume (By LOB)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Bar")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(claim_type_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(cliam_type_cnt_lst)+""+","
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
        claim_type_lst=list()
        cliam_type_cnt_lst=list() 
        key_lst=list()
        val_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1].split('}')[0]
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
                pipe = [{'$match':my_dict},{'$group': {'_id':'$claim_non_par_ind', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    if x['_id'] in claim_type_lst:
                        cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(int(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+int(x['total']))
                    else:
                        claim_type_lst.append(str(x['_id']))
                        cliam_type_cnt_lst.append(str(x['total'])) 
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
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$claim_non_par_ind', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        if x['_id'] in claim_type_lst:
                            cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(int(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+int(x['total']))
                        else:
                            claim_type_lst.append(str(x['_id']))
                            cliam_type_cnt_lst.append(str(x['total'])) 
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        for cti in range(0,len(claim_type_lst)):
            claim_type_lst[cti]=claim_type_lst[cti].lower().replace('1','Par').replace('0','Non-Par')
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Volume (By Par Status)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Bar")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(claim_type_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(cliam_type_cnt_lst)+""+","
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
        cliam_type_cnt_lst=list()
        claim_type_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1].split('}')[0]
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
                    if x['_id'] in claim_type_lst:
                        cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(int(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+int(x['total']))
                    else:
                        claim_type_lst.append(str(x['_id']))
                        cliam_type_cnt_lst.append(str(x['total'])) 
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
                        if x['_id'] in claim_type_lst:
                            cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(int(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+int(x['total']))
                        else:
                            claim_type_lst.append(str(x['_id']))
                            cliam_type_cnt_lst.append(str(x['total'])) 
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Volume (By Diagnosis Codes)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Bar")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(claim_type_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(cliam_type_cnt_lst)+""+","
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
        claim_type_lst=list()
        cliam_type_cnt_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1].split('}')[0]
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
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Volume (By TAT)")+"'"+","
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
        claim_type_lst=list()
        cliam_type_cnt_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1].split('}')[0]
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
                    if x['_id'] in claim_type_lst:
                        cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(int(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+int(x['total']))
                    else:
                        claim_type_lst.append(str(x['_id']))
                        cliam_type_cnt_lst.append(str(x['total'])) 
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
                        if x['_id'] in claim_type_lst:
                            cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(int(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+int(x['total']))
                        else:
                            claim_type_lst.append(str(x['_id']))
                            cliam_type_cnt_lst.append(str(x['total'])) 
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        for cti in range(0,len(claim_type_lst)):
            claim_type_lst[cti]=claim_type_lst[cti].lower().replace('edi','Electronic').replace('ppr','Paper')
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Volume (By Submission Mode)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Bar")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(claim_type_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(cliam_type_cnt_lst)+""+","
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
        cliam_type_cnt_lst=list()
        claim_type_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1].split('}')[0]
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
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Payment Trend (Volume)")+"'"+","
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
            r_end_dt=dur_lst[1].split('}')[0]
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
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Payment Trend (Value)")+"'"+","
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
        claim_type_lst=list()
        cliam_type_cnt_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1].split('}')[0]
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
                pipe = [{'$match':my_dict},{'$group': {'_id':'$claim_type_cd', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    print(str(x['_id']+"!"+str(x['total'])))
                    if x['_id'] in claim_type_lst:
                        cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(int(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+int(x['total']))
                    else:
                        claim_type_lst.append(str(x['_id']))
                        cliam_type_cnt_lst.append(str(x['total'])) 
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
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$claim_type_cd', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        print(str(x['_id']+"!"+str(x['total'])))
                    if x['_id'] in claim_type_lst:
                        cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(int(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+int(x['total']))
                    else:
                        claim_type_lst.append(str(x['_id']))
                        cliam_type_cnt_lst.append(str(x['total'])) 
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        for cti in range(0,len(claim_type_lst)):
            claim_type_lst[cti]=claim_type_lst[cti].lower().replace('m','Professional').replace('h','Facility')
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Payment Volume (By Claim Type)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Bar")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(claim_type_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(cliam_type_cnt_lst)+""+","
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
        claim_type_lst=list()
        cliam_type_cnt_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1].split('}')[0]
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
                pipe = [{'$match':my_dict},{'$group': {'_id':'$lob_id', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    print(str(x['_id']+"!"+str(x['total'])))
                    if x['_id'] in claim_type_lst:
                        cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(int(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+int(x['total']))
                    else:
                        claim_type_lst.append(str(x['_id']))
                        cliam_type_cnt_lst.append(str(x['total'])) 
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
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$lob_id', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        print(str(x['_id']+"!"+str(x['total'])))
                        if x['_id'] in claim_type_lst:
                            cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(int(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+int(x['total']))
                        else:
                            claim_type_lst.append(str(x['_id']))
                            cliam_type_cnt_lst.append(str(x['total'])) 
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        for li in range(0,len(claim_type_lst)):
            claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Payment Volume (By LOB)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Bar")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(claim_type_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(cliam_type_cnt_lst)+""+","
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
        claim_type_lst=list()
        cliam_type_cnt_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1].split('}')[0]
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
                pipe = [{'$match':my_dict},{'$group': {'_id':'$claim_non_par_ind', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    print(str(x['_id']+"!"+str(x['total'])))
                    if x['_id'] in claim_type_lst:
                        cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(int(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+int(x['total']))
                    else:
                        claim_type_lst.append(str(x['_id']))
                        cliam_type_cnt_lst.append(str(x['total'])) 
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
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$claim_non_par_ind', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        print(str(x['_id']+"!"+str(x['total'])))
                        if x['_id'] in claim_type_lst:
                            cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(int(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+int(x['total']))
                        else:
                            claim_type_lst.append(str(x['_id']))
                            cliam_type_cnt_lst.append(str(x['total'])) 
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        for cti in range(0,len(claim_type_lst)):
            claim_type_lst[cti]=claim_type_lst[cti].lower().replace('1','Par').replace('0','Non-Par')
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Payment Volume (By Par Status)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Bar")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(claim_type_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(cliam_type_cnt_lst)+""+","
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
        claim_type_lst=list()
        cliam_type_cnt_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1].split('}')[0]
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
                pipe = [{'$match':my_dict},{'$group': {'_id':'$diag_cd', 'total': {'$sum': 1}}},{'$sort': {'total':-1}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                top_cnt=0
                for x in mydoc:
                    top_cnt=top_cnt+1
                    if top_cnt==6:
                        break
                    print(str(x['_id']+"!"+str(x['total'])))
                    if x['_id'] in claim_type_lst:
                        cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(int(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+int(x['total']))
                    else:
                        claim_type_lst.append(str(x['_id']))
                        cliam_type_cnt_lst.append(str(x['total'])) 
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
                        if x['_id'] in claim_type_lst:
                            cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(int(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+int(x['total']))
                        else:
                            claim_type_lst.append(str(x['_id']))
                            cliam_type_cnt_lst.append(str(x['total'])) 
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Payment Volume (By Diag Codes)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Bar")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(claim_type_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(cliam_type_cnt_lst)+""+","
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
            r_end_dt=dur_lst[1].split('}')[0]
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
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Payment Volume (By TAT)")+"'"+","
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
        claim_type_lst=list()
        cliam_type_cnt_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1].split('}')[0]
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
                    if x['_id'] in claim_type_lst:
                        cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(int(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+int(x['total']))
                    else:
                        claim_type_lst.append(str(x['_id']))
                        cliam_type_cnt_lst.append(str(x['total'])) 
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
                        if x['_id'] in claim_type_lst:
                            cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(int(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+int(x['total']))
                        else:
                            claim_type_lst.append(str(x['_id']))
                            cliam_type_cnt_lst.append(str(x['total'])) 
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        for cti in range(0,len(claim_type_lst)):
            claim_type_lst[cti]=claim_type_lst[cti].lower().replace('edi','Electronic').replace('ppr','Paper')
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Payment Volume (By Submission Mode)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Bar")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(claim_type_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(cliam_type_cnt_lst)+""+","
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
            r_end_dt=dur_lst[1].split('}')[0]
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
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Denial Trend (Volume)")+"'"+","
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
            r_end_dt=dur_lst[1].split('}')[0]
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
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Denial Trend (Value)")+"'"+","
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
        claim_type_lst=list()
        cliam_type_cnt_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1].split('}')[0]
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
                pipe = [{'$match':my_dict},{'$group': {'_id':'$claim_type_cd', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    print(str(x['_id']+"!"+str(x['total'])))
                    if x['_id'] in claim_type_lst:
                        cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(int(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+int(x['total']))
                    else:
                        claim_type_lst.append(str(x['_id']))
                        cliam_type_cnt_lst.append(str(x['total'])) 
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
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$claim_type_cd', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        print(str(x['_id']+"!"+str(x['total'])))
                        if x['_id'] in claim_type_lst:
                            cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(int(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+int(x['total']))
                        else:
                            claim_type_lst.append(str(x['_id']))
                            cliam_type_cnt_lst.append(str(x['total'])) 
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        for cti in range(0,len(claim_type_lst)):
            claim_type_lst[cti]=claim_type_lst[cti].lower().replace('m','Professional').replace('h','Facility')
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Denial Volume (By Claim Type)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Bar")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(claim_type_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(cliam_type_cnt_lst)+""+","
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
        claim_type_lst=list()
        cliam_type_cnt_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1].split('}')[0]
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
                pipe = [{'$match':my_dict},{'$group': {'_id':'$lob_id', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    print(str(x['_id']+"!"+str(x['total'])))
                    if x['_id'] in claim_type_lst:
                        cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(int(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+int(x['total']))
                    else:
                        claim_type_lst.append(str(x['_id']))
                        cliam_type_cnt_lst.append(str(x['total'])) 
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
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$lob_id', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        print(str(x['_id']+"!"+str(x['total'])))
                        if x['_id'] in claim_type_lst:
                            cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(int(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+int(x['total']))
                        else:
                            claim_type_lst.append(str(x['_id']))
                            cliam_type_cnt_lst.append(str(x['total'])) 
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        for li in range(0,len(claim_type_lst)):
            claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Denial Volume (By LOB)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Bar")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(claim_type_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(cliam_type_cnt_lst)+""+","
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
        claim_type_lst=list()
        cliam_type_cnt_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1].split('}')[0]
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
                pipe = [{'$match':my_dict},{'$group': {'_id':'$claim_non_par_ind', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    print(str(x['_id']+"!"+str(x['total'])))
                    if x['_id'] in claim_type_lst:
                        cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(int(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+int(x['total']))
                    else:
                        claim_type_lst.append(str(x['_id']))
                        cliam_type_cnt_lst.append(str(x['total'])) 
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
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$claim_non_par_ind', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        print(str(x['_id']+"!"+str(x['total'])))
                        if x['_id'] in claim_type_lst:
                            cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(int(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+int(x['total']))
                        else:
                            claim_type_lst.append(str(x['_id']))
                            cliam_type_cnt_lst.append(str(x['total'])) 
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        for cti in range(0,len(claim_type_lst)):
            claim_type_lst[cti]=claim_type_lst[cti].lower().replace('1','Par').replace('0','Non-Par')
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Denial Volume (By Par Status)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Bar")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(claim_type_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(cliam_type_cnt_lst)+""+","
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
        claim_type_lst=list()
        cliam_type_cnt_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1].split('}')[0]
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
                    if x['_id'] in claim_type_lst:
                        cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(int(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+int(x['total']))
                    else:
                        claim_type_lst.append(str(x['_id']))
                        cliam_type_cnt_lst.append(str(x['total'])) 
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
                        if x['_id'] in claim_type_lst:
                            cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(int(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+int(x['total']))
                        else:
                            claim_type_lst.append(str(x['_id']))
                            cliam_type_cnt_lst.append(str(x['total'])) 
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Denial Volume (By Diagnosis Codes)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Bar")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(claim_type_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(cliam_type_cnt_lst)+""+","
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
            r_end_dt=dur_lst[1].split('}')[0]
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
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Denial Volume ( By TAT)")+"'"+","
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
        claim_type_lst=list()
        cliam_type_cnt_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1].split('}')[0]
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
                    if x['_id'] in claim_type_lst:
                        cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(int(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+int(x['total']))
                    else:
                        claim_type_lst.append(str(x['_id']))
                        cliam_type_cnt_lst.append(str(x['total']))
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
                        if x['_id'] in claim_type_lst:
                            cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(int(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+int(x['total']))
                        else:
                            claim_type_lst.append(str(x['_id']))
                            cliam_type_cnt_lst.append(str(x['total']))
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        for cti in range(0,len(claim_type_lst)):
            claim_type_lst[cti]=claim_type_lst[cti].lower().replace('edi','Electronic').replace('ppr','Paper')
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Denial Volume (By Submission Mode)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Bar")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(claim_type_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(cliam_type_cnt_lst)+""+","
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
            r_end_dt=dur_lst[1].split('}')[0]
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
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Partial Denial Trend (Volume)")+"'"+","
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
            r_end_dt=dur_lst[1].split('}')[0]
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
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Partial Denial Trend (Value)")+"'"+","
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
        claim_type_lst=list()
        cliam_type_cnt_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1].split('}')[0]
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
                pipe = [{'$match':my_dict},{'$group': {'_id':'$claim_type_cd', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    print(str(x['_id']+"!"+str(x['total'])))
                    if x['_id'] in claim_type_lst:
                        cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(int(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+int(x['total']))
                    else:
                        claim_type_lst.append(str(x['_id']))
                        cliam_type_cnt_lst.append(str(x['total']))
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
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$claim_type_cd', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        print(str(x['_id']+"!"+str(x['total'])))
                        if x['_id'] in claim_type_lst:
                            cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(int(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+int(x['total']))
                        else:
                            claim_type_lst.append(str(x['_id']))
                            cliam_type_cnt_lst.append(str(x['total']))
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        for cti in range(0,len(claim_type_lst)):
            claim_type_lst[cti]=claim_type_lst[cti].lower().replace('m','Professional').replace('h','Facility')
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Partial Denial Volume (By Claim Type)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Bar")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(claim_type_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(cliam_type_cnt_lst)+""+","
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
        claim_type_lst=list()
        cliam_type_cnt_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1].split('}')[0]
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
                pipe = [{'$match':my_dict},{'$group': {'_id':'$lob_id', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    print(str(x['_id']+"!"+str(x['total'])))
                    if x['_id'] in claim_type_lst:
                        cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(int(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+int(x['total']))
                    else:
                        claim_type_lst.append(str(x['_id']))
                        cliam_type_cnt_lst.append(str(x['total']))
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
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$lob_id', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        print(str(x['_id']+"!"+str(x['total'])))
                        if x['_id'] in claim_type_lst:
                            cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(int(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+int(x['total']))
                        else:
                            claim_type_lst.append(str(x['_id']))
                            cliam_type_cnt_lst.append(str(x['total'])) 
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        for li in range(0,len(claim_type_lst)):
            claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Partial Denial Volume (By LOB)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Bar")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(claim_type_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(cliam_type_cnt_lst)+""+","
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
        claim_type_lst=list()
        cliam_type_cnt_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1].split('}')[0]
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
                pipe = [{'$match':my_dict},{'$group': {'_id':'$claim_non_par_ind', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    print(str(x['_id']+"!"+str(x['total'])))
                    if x['_id'] in claim_type_lst:
                        cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(int(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+int(x['total']))
                    else:
                        claim_type_lst.append(str(x['_id']))
                        cliam_type_cnt_lst.append(str(x['total']))
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
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$claim_non_par_ind', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        print(str(x['_id']+"!"+str(x['total'])))
                        if x['_id'] in claim_type_lst:
                            cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(int(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+int(x['total']))
                        else:
                            claim_type_lst.append(str(x['_id']))
                            cliam_type_cnt_lst.append(str(x['total']))
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        for cti in range(0,len(claim_type_lst)):
            claim_type_lst[cti]=claim_type_lst[cti].lower().replace('1','Par').replace('0','Non-Par')
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Partial Denial Volume (By Par Status)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Bar")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(claim_type_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(cliam_type_cnt_lst)+""+","
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
        claim_type_lst=list()
        cliam_type_cnt_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1].split('}')[0]
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
                    if x['_id'] in claim_type_lst:
                        cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(int(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+int(x['total']))
                    else:
                        claim_type_lst.append(str(x['_id']))
                        cliam_type_cnt_lst.append(str(x['total']))
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
                        if x['_id'] in claim_type_lst:
                            cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(int(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+int(x['total']))
                        else:
                            claim_type_lst.append(str(x['_id']))
                            cliam_type_cnt_lst.append(str(x['total']))
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Partial Denial Volume (By Diagnosis Codes)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Bar")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(claim_type_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(cliam_type_cnt_lst)+""+","
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
            r_end_dt=dur_lst[1].split('}')[0]
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
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Partial Denial Volume (By TAT)")+"'"+","
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
        claim_type_lst=list()
        cliam_type_cnt_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1].split('}')[0]
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
                    if x['_id'] in claim_type_lst:
                        cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(int(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+int(x['total']))
                    else:
                        claim_type_lst.append(str(x['_id']))
                        cliam_type_cnt_lst.append(str(x['total']))
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
                        if x['_id'] in claim_type_lst:
                            cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(int(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+int(x['total']))
                        else:
                            claim_type_lst.append(str(x['_id']))
                            cliam_type_cnt_lst.append(str(x['total']))
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        for cti in range(0,len(claim_type_lst)):
            claim_type_lst[cti]=claim_type_lst[cti].lower().replace('edi','Electronic').replace('ppr','Paper')
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Partial Denial Volume (By Submission Mode)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Bar")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(claim_type_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(cliam_type_cnt_lst)+""+","
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
            r_end_dt=dur_lst[1].split('}')[0]
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
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Adjustment Trend (Volume)")+"'"+","
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
            r_end_dt=dur_lst[1].split('}')[0]
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
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Adjustment Trend (Value)")+"'"+","
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
        claim_type_lst=list()
        cliam_type_cnt_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1].split('}')[0]
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
                pipe = [{'$match':my_dict},{'$group': {'_id':'$claim_type_cd', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    print(str(x['_id']+"!"+str(x['total'])))
                    if x['_id'] in claim_type_lst:
                        cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(int(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+int(x['total']))
                    else:
                        claim_type_lst.append(str(x['_id']))
                        cliam_type_cnt_lst.append(str(x['total']))
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
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$claim_type_cd', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        print(str(x['_id']+"!"+str(x['total'])))
                        if x['_id'] in claim_type_lst:
                            cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(int(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+int(x['total']))
                        else:
                            claim_type_lst.append(str(x['_id']))
                            cliam_type_cnt_lst.append(str(x['total']))
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        for cti in range(0,len(claim_type_lst)):
            claim_type_lst[cti]=claim_type_lst[cti].lower().replace('m','Professional').replace('h','Facility')
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Adjustment Volume (By Claim Type)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Bar")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(claim_type_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(cliam_type_cnt_lst)+""+","
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
        claim_type_lst=list()
        cliam_type_cnt_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1].split('}')[0]
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
                pipe = [{'$match':my_dict},{'$group': {'_id':'$lob_id', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    print(str(x['_id']+"!"+str(x['total'])))
                    if x['_id'] in claim_type_lst:
                        cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(int(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+int(x['total']))
                    else:
                        claim_type_lst.append(str(x['_id']))
                        cliam_type_cnt_lst.append(str(x['total']))
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
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$lob_id', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        print(str(x['_id']+"!"+str(x['total'])))
                        if x['_id'] in claim_type_lst:
                            cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(int(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+int(x['total']))
                        else:
                            claim_type_lst.append(str(x['_id']))
                            cliam_type_cnt_lst.append(str(x['total']))
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        for li in range(0,len(claim_type_lst)):
            claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Adjustment Volume (By LOB)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Bar")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(claim_type_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(cliam_type_cnt_lst)+""+","
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
        claim_type_lst=list()
        cliam_type_cnt_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1].split('}')[0]
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
                pipe = [{'$match':my_dict},{'$group': {'_id':'$claim_non_par_ind', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    print(str(x['_id']+"!"+str(x['total'])))
                    if x['_id'] in claim_type_lst:
                        cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(int(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+int(x['total']))
                    else:
                        claim_type_lst.append(str(x['_id']))
                        cliam_type_cnt_lst.append(str(x['total']))
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
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$claim_non_par_ind', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        print(str(x['_id']+"!"+str(x['total'])))
                        if x['_id'] in claim_type_lst:
                            cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(int(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+int(x['total']))
                        else:
                            claim_type_lst.append(str(x['_id']))
                            cliam_type_cnt_lst.append(str(x['total']))
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        for cti in range(0,len(claim_type_lst)):
            claim_type_lst[cti]=claim_type_lst[cti].lower().replace('1','Par').replace('0','Non-Par')
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Adjustment Volume (By Par Status)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Bar")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(claim_type_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(cliam_type_cnt_lst)+""+","
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
        claim_type_lst=list()
        cliam_type_cnt_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1].split('}')[0]
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
                    if x['_id'] in claim_type_lst:
                        cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(int(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+int(x['total']))
                    else:
                        claim_type_lst.append(str(x['_id']))
                        cliam_type_cnt_lst.append(str(x['total']))
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
                        if x['_id'] in claim_type_lst:
                            cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(int(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+int(x['total']))
                        else:
                            claim_type_lst.append(str(x['_id']))
                            cliam_type_cnt_lst.append(str(x['total']))
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Adjustment Volume (By Diagnosis Codes)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Bar")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(claim_type_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(cliam_type_cnt_lst)+""+","
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
            r_end_dt=dur_lst[1].split('}')[0]
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
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Adjustment Volume (By TAT)")+"'"+","
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
        claim_type_lst=list()
        cliam_type_cnt_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1].split('}')[0]
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
                    if x['_id'] in claim_type_lst:
                        cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(int(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+int(x['total']))
                    else:
                        claim_type_lst.append(str(x['_id']))
                        cliam_type_cnt_lst.append(str(x['total']))
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
                        if x['_id'] in claim_type_lst:
                            cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(int(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+int(x['total']))
                        else:
                            claim_type_lst.append(str(x['_id']))
                            cliam_type_cnt_lst.append(str(x['total']))
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        for cti in range(0,len(claim_type_lst)):
            claim_type_lst[cti]=claim_type_lst[cti].lower().replace('edi','Electronic').replace('ppr','Paper')
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Adjustment Volume (By Submission Mode)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Bar")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(claim_type_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(cliam_type_cnt_lst)+""+","
        kv=kv[0:len(kv)-1]+"}"
        print(kv)
        kv=ast.literal_eval(kv)
        return kv

    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"


def get_adjstd_reasons_trend(dur_lst,provider_lst):

    try:
    # if True:
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
            r_end_dt=dur_lst[1].split('}')[0]
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
                pipe = [{'$match':my_dict},{'$group': {'_id':'$adjustment_reasons', 'total': {'$sum': 1}}},{'$sort':{'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                cn=0
                den_reas_val_lst=list()
                for x in mydoc:
                    n_records=list()
                    print(str(x['_id']+"!"+str(x['total'])))
                    if x['_id'].upper()=='TEXT NOT AVAILABLE' or len(str(x['_id']).strip(' '))==0:
                        continue
                    # n_records='{"reason":'+str(x['_id'])+","+'"Value:"'+str(x['total'])+"}"
                    n_records.append(str(x['_id']))
                    n_records.append(str(x['total']))
                    den_reas_val_lst.append(n_records)
                    cn=cn+1
                    if cn==5:
                        break
                n_records=n_records[1:]
                print(str(mon_strt))
                key_val=mon_name(mon_strt)+"-"+str(str(yr_strt)[-2:])
                val_val=n_records                
                key_lst.append(key_val)
                val_lst.append(den_reas_val_lst)
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
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$adjustment_reasons', 'total': {'$sum': 1}}},{'$sort':{'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    cn=0
                    den_reas_val_lst=list()
                    for x in mydoc:
                        n_records=list()
                        print(str(x['_id']+"!"+str(x['total'])))
                        if x['_id'].upper()=='TEXT NOT AVAILABLE' or len(str(x['_id']).strip(' '))==0:
                            continue
                        n_records.append(str(x['_id']))
                        n_records.append(str(x['total']))
                        # a=str(x['_id'])
                        # n_records="{"
                        # n_records=n_records+"'"+str("reason")+"'"+":"+"'"+str(a)+"'"+","
                        # n_records=n_records+"'"+str("Value")+"'"+":"+"'"+str(x['total'])+"'"+","
                        # n_records=n_records[0:len(n_records)-1]+"}"
                        # n_records=ast.literal_eval(n_records)
                        den_reas_val_lst.append(n_records)
                        cn=cn+1
                        if cn==5:
                            break
                    n_records=n_records[1:]
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(den_reas_val_lst)
                    cond=""
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Adjustment Reasons (Volume)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Stacked Bar")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(key_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(val_lst)+""+","
        kv=kv[0:len(kv)-1]+"}"
        print(kv)
        kv=ast.literal_eval(kv)
        return kv
    # else:
    except Exception as e:
        print(str(e))       
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
            r_end_dt=dur_lst[1].split('}')[0]
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
                den_reas_val_lst=list()
                for x in mydoc:
                    n_records=list()
                    print(str(x['_id']+"!"+str(x['total'])))
                    if x['_id'].upper()=='TEXT NOT AVAILABLE' or len(str(x['_id']).strip(' '))==0:
                        continue
                    # n_records='{"reason":'+str(x['_id'])+","+'"Value:"'+str(x['total'])+"}"
                    n_records.append(str(x['_id']))
                    n_records.append(str(x['total']))
                    den_reas_val_lst.append(n_records)
                    cn=cn+1
                    if cn==5:
                        break
                
                print(str(mon_strt))
                key_val=mon_name(mon_strt)+"-"+str(str(yr_strt)[-2:])
                val_val=n_records                
                key_lst.append(key_val)
                val_lst.append((den_reas_val_lst))
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
                    den_reas_val_lst=list()
                    for x in mydoc:
                        n_records=list()
                        print(str(x['_id']+"!"+str(x['total'])))
                        if x['_id'].upper()=='TEXT NOT AVAILABLE' or len(str(x['_id']).strip(' '))==0:
                            continue
                        n_records.append(str(x['_id']))
                        n_records.append(str(x['total']))
                        # a=str(x['_id'])
                        # n_records="{"
                        # n_records=n_records+"'"+str("reason")+"'"+":"+"'"+str(a)+"'"+","
                        # n_records=n_records+"'"+str("Value")+"'"+":"+"'"+str(x['total'])+"'"+","
                        # n_records=n_records[0:len(n_records)-1]+"}"
                        # n_records=ast.literal_eval(n_records)
                        den_reas_val_lst.append(n_records)
                        cn=cn+1
                        if cn==5:
                            break
                    
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(den_reas_val_lst)
                    cond=""
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Partial Denial Reasons (Volume)")+"'"+","
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
            r_end_dt=dur_lst[1].split('}')[0]
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
                pipe = [{'$match':my_dict},{'$group': {'_id':'$denial_full_reasons', 'total': {'$sum': 1}}},{'$sort':{'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                cn=0
                den_reas_val_lst=list()
                for x in mydoc:
                    n_records=list()
                    print(str(x['_id']+"!"+str(x['total'])))
                    if x['_id'].upper()=='TEXT NOT AVAILABLE' or len(str(x['_id']).strip(' '))==0:
                        continue
                    # n_records='{"reason":'+str(x['_id'])+","+'"Value:"'+str(x['total'])+"}"
                    n_records.append(str(x['_id']))
                    n_records.append(str(x['total']))
                    den_reas_val_lst.append(n_records)
                    cn=cn+1
                    if cn==5:
                        break
                
                print(str(mon_strt))
                key_val=mon_name(mon_strt)+"-"+str(str(yr_strt)[-2:])
                val_val=n_records                
                key_lst.append(key_val)
                val_lst.append((den_reas_val_lst))
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
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$denial_full_reasons', 'total': {'$sum': 1}}},{'$sort':{'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    cn=0
                    den_reas_val_lst=list()
                    for x in mydoc:
                        n_records=list()
                        print(str(x['_id']+"!"+str(x['total'])))
                        if x['_id'].upper()=='TEXT NOT AVAILABLE' or len(str(x['_id']).strip(' '))==0:
                            continue
                        n_records.append(str(x['_id']))
                        n_records.append(str(x['total']))
                        # a=str(x['_id'])
                        # n_records="{"
                        # n_records=n_records+"'"+str("reason")+"'"+":"+"'"+str(a)+"'"+","
                        # n_records=n_records+"'"+str("Value")+"'"+":"+"'"+str(x['total'])+"'"+","
                        # n_records=n_records[0:len(n_records)-1]+"}"
                        # n_records=ast.literal_eval(n_records)
                        den_reas_val_lst.append(n_records)
                        cn=cn+1
                        if cn==5:
                            break
                    
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(den_reas_val_lst)
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

def get_denial_reasons_trend_bar(dur_lst,provider_lst):

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb["hfa_claims_1819"] 
        key_lst=list()
        val_lst=list()
        claim_type_lst=list()
        cliam_type_cnt_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1].split('}')[0]
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
                pipe = [{'$match':my_dict},{'$group': {'_id':'$denial_full_reasons', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                top_cnt=0
                for x in mydoc:
                    if x['_id'].upper()=='TEXT NOT AVAILABLE' or len(str(x['_id']).strip(' '))==0:
                        continue
                    top_cnt=top_cnt+1
                    if top_cnt==6:
                        break
                    print(str(x['_id']+"!"+str(x['total'])))
                    if x['_id'] in claim_type_lst:
                        cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(int(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+int(x['total']))
                    else:
                        claim_type_lst.append(str(x['_id']))
                        cliam_type_cnt_lst.append(str(x['total'])) 
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
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$denial_full_reasons', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    top_cnt=0
                    for x in mydoc:
                        if x['_id'].upper()=='TEXT NOT AVAILABLE' or len(str(x['_id']).strip(' '))==0:
                            continue
                        top_cnt=top_cnt+1
                        if top_cnt==6:
                            break
                        print(str(x['_id']+"!"+str(x['total'])))
                        if x['_id'] in claim_type_lst:
                            cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(int(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+int(x['total']))
                        else:
                            claim_type_lst.append(str(x['_id']))
                            cliam_type_cnt_lst.append(str(x['total'])) 
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
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Bar_Requested")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(claim_type_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(cliam_type_cnt_lst)+""+","
        kv=kv[0:len(kv)-1]+"}"
        print(kv)
        kv=ast.literal_eval(kv)
        return kv

    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"


def get_prtl_denial_reasons_trend_bar(dur_lst,provider_lst):

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb["hfa_claims_1819"] 
        key_lst=list()
        val_lst=list()
        claim_type_lst=list()
        cliam_type_cnt_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1].split('}')[0]
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
                mylist1 = mycol1.find({'total':0}).distinct('_id')                
                mycol1.drop()
                ##
                pc1=",{'root_claim_num':{'$in':"+str(mylist1)+"}}"
                cond=cond.replace(']}',pc1+']}')
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$denial_full_reasons', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                top_cnt=0
                for x in mydoc:
                    if x['_id'].upper()=='TEXT NOT AVAILABLE' or len(str(x['_id']).strip(' '))==0:
                        continue
                    top_cnt=top_cnt+1
                    if top_cnt==6:
                        break
                    print(str(x['_id']+"!"+str(x['total'])))
                    if x['_id'] in claim_type_lst:
                        cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(int(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+int(x['total']))
                    else:
                        claim_type_lst.append(str(x['_id']))
                        cliam_type_cnt_lst.append(str(x['total'])) 
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
                    mylist1 = mycol1.find({'total':0}).distinct('_id')                
                    mycol1.drop()
                    ##
                    pc1=",{'root_claim_num':{'$in':"+str(mylist1)+"}}"
                    cond=cond.replace(']}',pc1+']}')
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$denial_full_reasons', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    top_cnt=0
                    for x in mydoc:
                        if x['_id'].upper()=='TEXT NOT AVAILABLE' or len(str(x['_id']).strip(' '))==0:
                            continue
                        top_cnt=top_cnt+1
                        if top_cnt==6:
                            break
                        print(str(x['_id']+"!"+str(x['total'])))
                        if x['_id'] in claim_type_lst:
                            cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(int(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+int(x['total']))
                        else:
                            claim_type_lst.append(str(x['_id']))
                            cliam_type_cnt_lst.append(str(x['total'])) 
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Partial Denial Reasons (Volume)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Bar_Requested")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(claim_type_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(cliam_type_cnt_lst)+""+","
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
            r_end_dt=dur_lst[1].split('}')[0]
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
            r_end_dt=dur_lst[1].split('}')[0]
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



def get_adjstd_reasons_trend_bar(dur_lst,provider_lst):

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb["hfa_claims_1819"] 
        key_lst=list()
        val_lst=list()
        claim_type_lst=list()
        cliam_type_cnt_lst=list()
        r_from_dt=""
        r_end_dt=""
        r_graph_type="line"
        if len(dur_lst)==3:
            r_from_dt=dur_lst[0]
            r_end_dt=dur_lst[1].split('}')[0]
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
                pipe = [{'$match':my_dict},{'$group': {'_id':'$adjustment_reasons', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                top_cnt=0
                for x in mydoc:
                    if x['_id'].upper()=='TEXT NOT AVAILABLE' or len(str(x['_id']).strip(' '))==0:
                        continue
                    top_cnt=top_cnt+1
                    if top_cnt==6:
                        break
                    print(str(x['_id']+"!"+str(x['total'])))
                    if x['_id'] in claim_type_lst:
                        cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(int(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+int(x['total']))
                    else:
                        claim_type_lst.append(str(x['_id']))
                        cliam_type_cnt_lst.append(str(x['total']))
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
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$adjustment_reasons', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    top_cnt=0
                    for x in mydoc:
                        if x['_id'].upper()=='TEXT NOT AVAILABLE' or len(str(x['_id']).strip(' '))==0:
                            continue
                        top_cnt=top_cnt+1
                        if top_cnt==6:
                            break
                        print(str(x['_id']+"!"+str(x['total'])))
                        if x['_id'] in claim_type_lst:
                            cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(int(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+int(x['total']))
                        else:
                            claim_type_lst.append(str(x['_id']))
                            cliam_type_cnt_lst.append(str(x['total']))
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Adjustment Reasons (Volume)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Bar_Requested")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(claim_type_lst)+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(cliam_type_cnt_lst)+""+","
        kv=kv[0:len(kv)-1]+"}"
        print(kv)
        kv=ast.literal_eval(kv)
        return kv

    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"



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


def get_rcvd_claim_paid_val_trend(dur_lst,provider_lst): # paid amount of received claims

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
            r_end_dt=dur_lst[1].split('}')[0]
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
                    cond=cond+"{'received_date':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'received_date':{'$regex':'"+str(dl)+"-.*-.*'}}"                    
                    if len(provider_lst) > 0:
                        pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                        cond="{'$and':["+cond+pc+"]}"
                    else:
                        cond="{'$and':["+cond+"]}"
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
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Trend (Value)")+"'"+","
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

def get_prtl_dend_claim_paid_val_trend(dur_lst,provider_lst):

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
            r_end_dt=dur_lst[1].split('}')[0]
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
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Partial Denial Trend (Value)")+"'"+","
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

def get_adjstd_claim_billed_val_trend(dur_lst,provider_lst):

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
            r_end_dt=dur_lst[1].split('}')[0]
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
                        di=",{'claim_adj_ind':'1'}"
                        cond="{'$and':["+cond+pc+di+"]}"
                    else:
                        di=",{'claim_adj_ind':'1'}"
                        cond="{'$and':["+cond+di+"]}"
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
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Adjustment Trend (Value)")+"'"+","
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

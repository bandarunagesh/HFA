# from pymongo import MongoClient
import pymongo
import datetime
import calendar
import ast
import random
import pandas as pd

coll_name="hfa_calls_2019"

GREETING_RESPONSES = ["hey", "Hi", "how can i help?","hello","what's up"]
GOODBYE_RESPONSES = ["bye", "cya", "take care", "good bye", "bye bye","Bye..Tc"]
AFFIRM_RESPONSES = ["indeed", "OK", "that's right", "great", "cool"]

def get_distinct_tin_cnt():

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
        mydoc = mycol.distinct('tin')    
        n_records=len(mydoc)
        return n_records

    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"

    return " calls_cnt_lob function "

# print(get_distinct_tin_cnt())

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

def greeting():
    """If any of the words in the user's input was a greeting, return a greeting response"""
    return random.choice(GREETING_RESPONSES)

def goodbye():
    """If any of the words in the user's input was a goodbye, return a goddbye response"""
    return random.choice(GOODBYE_RESPONSES)

def affirm():
    """If any of the words in the user's input was a goodbye, return a goddbye response"""
    return random.choice(AFFIRM_RESPONSES)

def get_call_id_presence(call_id):
    
    try:
        
        print(call_id +" in get_call_id_presence function")
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
        mydoc = mycol.find({"call_id": str(call_id)})
        n_records=((mydoc.count()))
        if n_records >0:
            return True
        else:
            return False

    except Exception as e:

        print(str(e))
        return "Sorry, Could not fetch you results at this time"
# print(get_call_id_presence('817097999'))
def get_call_received_date(call_id):
    
    try:
        
        print(call_id +" in get_call_id_presence function")
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
        mydoc = mycol.find({"call_id": str(call_id)})
        n_records=((mydoc.count()))
        if n_records >0:
            for x in mydoc:  
                t=x['rcvd_date_str']
                return "The call was received on "+t.split('-')[2]+"th of "+mon_name(t.split('-')[1])+", "+t.split('-')[0]              
                # return str(x['calltimestartdesktop'])+" is the date on which call is received"
        else:
            return "Sorry, Could not fetch you results at this time"

    except Exception as e:

        print(str(e))
        return "Sorry, Could not fetch you results at this time"

    return "call received date function "+str(call_id)
# print(get_call_received_date('817097999'))
def get_call_time(call_id):

    try:
        
        print(call_id +" in get_call_id_presence function")
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
        mydoc = mycol.find({"call_id": str(call_id)})
        n_records=((mydoc.count()))
        if n_records >0:
            for x in mydoc:  
                t=str(int(x['talktime'])+int(x['holdtime'])+int(x['ringtime']))
                return "The total duration of call is "+t+" seconds"                
        else:
            return "Sorry, Could not fetch you results at this time"

    except Exception as e:

        print(str(e))
        return "Sorry, Could not fetch you results at this time"

    return "call time function "+str(call_id)
# print(get_call_time('817097999'))
def get_call_type(call_id):

    try:
        
        print(call_id +" in get_call_type function")
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
        mydoc = mycol.find({"call_id": str(call_id)})
        for x in mydoc:
            return "The call is related to <b>"+str(x['category'])+"</b> category"
        return "Sorry, Could not fetch you results at this time"

    except Exception as e:

        print(str(e))
        return "Sorry, Could not fetch you results at this time"

def get_call_lob(call_id):
    
    try:
        
        print(call_id +" in get_call_lob function")
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
        mydoc = mycol.find({"call_id": str(call_id)})
        for x in mydoc:
            return "The call pertains to <b>"+str(x['lob_id'])+"</b> line of business"
        return "Sorry, Could not fetch you results at this time"

    except Exception as e:

        print(str(e))
        return "Sorry, Could not fetch you results at this time"
# print(get_call_lob('817097999'))    
def get_call_product_type(call_id):

    try:
        
        print(call_id +" in get_call_product_type function")
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
        mydoc = mycol.find({"call_id": str(call_id)})
        for x in mydoc:
            try:
                return "The Product <b>"+str(x['producttypeverbose']).split('-')[1].strip(' ')+"</b> was enquired in call"
            except:
                return "The Product <b>"+str(x['producttypeverbose']).strip(' ')+"</b> was enquired in call"
        return "Sorry, Could not fetch you results at this time"

    except Exception as e:
        
        print(str(e))
        return "Sorry, Could not fetch you results at this time"
# print(get_call_product_type('817097999'))         
def get_call_hold_time(call_id):
    try:
        
        print(call_id +" in get_call_hold_time function")
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
        mydoc = mycol.find({"call_id": str(call_id)})
        for x in mydoc:
            return "The call was on hold for "+str(x['holdtime'])+" seconds"
        return "Sorry, Could not fetch you results at this time"

    except Exception as e:
        
        print(str(e))
        return "Sorry, Could not fetch you results at this time"
# print(get_call_hold_time('817097999')) 
def get_call_ring_time(call_id):

    try:
        
        print(call_id +" in get_call_ring_time function")
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
        mydoc = mycol.find({"call_id": str(call_id)})
        for x in mydoc:
            return "The phone call rang for "+str(x['ringtime'])+" seconds"
        return "Sorry, Could not fetch you results at this time"

    except Exception as e:
        
        print(str(e))
        return "Sorry, Could not fetch you results at this time"

def get_call_info(call_id):

    try:
        
        print(call_id +" in get_call_info_presence function")
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
        mydoc = mycol.find({"call_id": str(call_id)})
        n_records=((mydoc.count()))
        if n_records >0:
            for x in mydoc:  
                t=x['rcvd_date_str']
                return "The call was received on "+t.split('-')[2]+"th of "+mon_name(t.split('-')[1])+", "+t.split('-')[0]+" with total duration of "+str(x['total_time'])+" seconds"
                # return str(x['calltimestartdesktop'])+" is the date on which call is received"
        else:
            return "Sorry, Could not fetch you results at this time"

    except Exception as e:

        print(str(e))
        return "Sorry, Could not fetch you results at this time"
    
# print(get_call_ring_time('817097999'))        

def get_call_talk_time(call_id):

    try:
        
        print(call_id +" in get_call_talk_time function")
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
        mydoc = mycol.find({"call_id": str(call_id)})
        for x in mydoc:
            return "The talk time for the call was "+str(x['talktime'])+" seconds"
        return "Sorry, Could not fetch you results at this time"

    except Exception as e:
        
        print(str(e))
        return "Sorry, Could not fetch you results at this time"

# print(get_call_talk_time('817097999'))        

def get_call_answered(call_id):
    # as of now if there is no transfer in transfer column taking it as answered
    try:
        
        print(call_id +" in get_call_talk_time function")
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
        mydoc = mycol.find({"call_id": str(call_id)})
        for x in mydoc:
            # pc1=",{'talktime':{'$ne':"+str("0")+"}}"
            # if int(str(x['talktime']))>0:
            #     return "Yes, The call got answered"
            # else:
            #     return "No, the call went unanswered"
            if "ringnoanswer" in (str(x['vccd_dispostion'])).lower():
                return "No, the call went unanswered"                
            else:
                return "Yes, The call got answered"
        return "Sorry, Could not fetch you results at this time"

    except Exception as e:
        
        print(str(e))
        return "Sorry, Could not fetch you results at this time"

    return "call answered function "+str(call_id)   
# print(get_call_answered('817097999')) 
def get_call_transferred(call_id):

    # as of now if there is no transfer in transfer column taking it as transferred
    try:
        
        print(call_id +" in get_call_talk_time function")
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
        mydoc = mycol.find({"call_id": str(call_id)})
        for x in mydoc:
            if "no" in str(x['transfer']).lower() and "transfer" in str(x['transfer']).lower():
                return "No, the call did not get transferred"                
            else:
                return "Yes, the call got transferred"
        return "Sorry, Could not fetch you results at this time"

    except Exception as e:
        
        print(str(e))
        return "Sorry, Could not fetch you results at this time"

    return "call transferrred function "+str(call_id)   
# print(get_call_transferred('817097999')) 
def get_call_language(call_id):    
    
    try:
        
        print(call_id +" in get_call_talk_time function")
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
        mydoc = mycol.find({"call_id": str(call_id)})
        for x in mydoc:
            if "E"==str(x['language']).upper().strip(' '):
                return "The call was answered in English"
            else:
                return "The call was answered in "+str(x['language']).upper().strip(' ')
        return "Sorry, Could not fetch you results at this time"

    except Exception as e:
        
        print(str(e))
        return "Sorry, Could not fetch you results at this time"

    return "call transferrred function "+str(call_id) 
# print(get_call_language('817097999')) 
def get_call_BU(call_id):    
    
    try:
        
        print(call_id +" in get_call_talk_time function")
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
        mydoc = mycol.find({"call_id": str(call_id)})
        for x in mydoc:
            return "The call was related to <b>"+str(x['bu'])+"</b> business unit"
        return "Sorry, Could not fetch you results at this time"

    except Exception as e:
        
        print(str(e))
        return "Sorry, Could not fetch you results at this time"

    return "call transferrred function "+str(call_id)
# print(get_call_BU('817097999')) 
def get_calls_cnt_eligible_lob(dur_lst,provider_lst):

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'category':{'$eq':'Eligibility'}}"
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'category':{'$eq':'Eligibility'}}"
                    cond="{'$and':["+cond+pc1+"]}"
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'category':{'$eq':'Eligibility'}}"
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'category':{'$eq':'Eligibility'}}"
                        cond="{'$and':["+cond+pc1+"]}"
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
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Eligibility Calls Volume (By LOB)")+"'"+","
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

    return " calls_cnt_eligible_lob function "
# print(get_calls_cnt_eligible_lob([[],[],['2019'],[]],['141338470']))
def get_calls_cnt_eligible_prod_type(dur_lst,provider_lst):

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'category':{'$eq':'Eligibility'}}"
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'category':{'$eq':'Eligibility'}}"
                    cond="{'$and':["+cond+pc1+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$producttypeverbose', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    try:
                        x['_id']=x['_id'].split('-')[1].strip(' ')
                    except:
                        x['_id']=x['_id'].strip(' ')

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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'category':{'$eq':'Eligibility'}}"
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'category':{'$eq':'Eligibility'}}"
                        cond="{'$and':["+cond+pc1+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$producttypeverbose', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        try:
                            x['_id']=x['_id'].split('-')[1].strip(' ')
                        except:
                            x['_id']=x['_id'].strip(' ')

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
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Eligibility Calls Volume (By Product Type)")+"'"+","
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

    return " calls_cnt_eligible_prod_type function "
# print(get_calls_cnt_eligible_prod_type([[],[],['2019'],[]],['141338470']))
def get_calls_cnt_eligible_type(dur_lst,provider_lst):

    ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'category':{'$eq':'Eligibility'}}"
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'category':{'$eq':'Eligibility'}}"
                    cond="{'$and':["+cond+pc1+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$questiontypeverbose', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'category':{'$eq':'Eligibility'}}"
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'category':{'$eq':'Eligibility'}}"
                        cond="{'$and':["+cond+pc1+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$questiontypeverbose', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
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
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Eligibility Calls Volume (By Type)")+"'"+","
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

    return " calls_cnt_eligible_type function "
# print(get_calls_cnt_eligible_type([[],[],['2019'],[]],['141338470']))
def get_calls_cnt_eligible_trnsfr(dur_lst,provider_lst):

    ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'category':{'$eq':'Eligibility'}}"
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'category':{'$eq':'Eligibility'}}"
                    cond="{'$and':["+cond+pc1+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$transfer', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    if "no" in str(x['_id']).lower().strip(' ') and 'transfer' in str(x['_id']).lower().strip():
                        x['_id']="Not Transferred"
                    else:
                        x['_id']="Transferred"
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'category':{'$eq':'Eligibility'}}"
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'category':{'$eq':'Eligibility'}}"
                        cond="{'$and':["+cond+pc1+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$transfer', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        if "no" in str(x['_id']).lower().strip(' ') and 'transfer' in str(x['_id']).lower().strip():
                            x['_id']="Not Transferred"
                        else:
                            x['_id']="Transferred"
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
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Eligibility Calls Volume (By Transfer)")+"'"+","
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
    

    return " calls_cnt_eligible_trnsfr function "
# print(get_calls_cnt_eligible_trnsfr([[],[],['2019'],[]],['141338470']))
def get_calls_cnt_eligible_ans(dur_lst,provider_lst):

    ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'category':{'$eq':'Eligibility'}}"
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'category':{'$eq':'Eligibility'}}"
                    cond="{'$and':["+cond+pc1+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$vccd_dispostion', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    if "ringnoanswer" in str(x['_id']).lower():
                        x['_id']="Not Answered"
                    else:
                        x['_id']="Answered"
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'category':{'$eq':'Eligibility'}}"
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'category':{'$eq':'Eligibility'}}"
                        cond="{'$and':["+cond+pc1+"]}"  
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$vccd_dispostion', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        if "ringnoanswer" in str(x['_id']).lower():
                            x['_id']="Not Answered"
                        else:
                            x['_id']="Answered"
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
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Eligibility Calls Volume (By Answered)")+"'"+","
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
    
    return " calls_cnt_eligible_ans function "
# print(get_calls_cnt_eligible_ans([[],[],['2019'],[]],['141338470']))
def get_calls_cnt_eligible_lang(dur_lst,provider_lst):

    ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'category':{'$eq':'Eligibility'}}"
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'category':{'$eq':'Eligibility'}}"
                    cond="{'$and':["+cond+pc1+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$language', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    if str(x['_id']).strip().lower()=="e":
                        x['_id']="English"
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'category':{'$eq':'Eligibility'}}"
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'category':{'$eq':'Eligibility'}}"
                        cond="{'$and':["+cond+pc1+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$language', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        if str(x['_id']).strip().lower()=="e":
                            x['_id']="English"
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
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Eligibility Calls Volume (By Language)")+"'"+","
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

    return " calls_cnt_eligible_lang function "
# print(get_calls_cnt_eligible_lang([[],[],['2019'],[]],['141338470']))
def get_calls_cnt_eligible(dur_lst,provider_lst):

    print(provider_lst)

    try:
        cond=""
        n_records="0"
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name] 
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'category':{'$eq':'Eligibility'}}"
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'category':{'$eq':'Eligibility'}}"
                    cond="{'$and':["+cond+pc1+"]}"
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'category':{'$eq':'Eligibility'}}"
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'category':{'$eq':'Eligibility'}}"
                        cond="{'$and':["+cond+pc1+"]}"
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
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Eligibility Calls Trend (Volume)")+"'"+","
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
    return " calls_cnt_eligible function "
# print(get_calls_cnt_eligible([[],[],['2019'],[]],['141338470']))
def get_calls_cnt_eligible_BU(dur_lst,provider_lst):

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'category':{'$eq':'Eligibility'}}"
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'category':{'$eq':'Eligibility'}}"
                    cond="{'$and':["+cond+pc1+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$bu', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'category':{'$eq':'Eligibility'}}"
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'category':{'$eq':'Eligibility'}}"
                        cond="{'$and':["+cond+pc1+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$bu', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
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
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Eligibility Calls Volume (By BU)")+"'"+","
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

    return " calls_cnt_eligible_BU function "
# print(get_calls_cnt_eligible_BU([[],[],['2019'],[]],['141338470']))

def get_calls_cnt_ben_lob(dur_lst,provider_lst):

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'category':{'$eq':'Benefits'}}"
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'category':{'$eq':'Benefits'}}"
                    cond="{'$and':["+cond+pc1+"]}"
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'category':{'$eq':'Benefits'}}"
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'category':{'$eq':'Benefits'}}"
                        cond="{'$and':["+cond+pc1+"]}"
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
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Benefits Calls Volume (By LOB)")+"'"+","
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

    return " calls_cnt_ben_lob function "
# print(get_calls_cnt_ben_lob([[],[],['2019'],[]],['141338470']))
def get_calls_cnt_ben_prod_type(dur_lst,provider_lst):

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'category':{'$eq':'Benefits'}}"
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'category':{'$eq':'Benefits'}}"
                    cond="{'$and':["+cond+pc1+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$producttypeverbose', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    try:
                        x['_id']=x['_id'].split('-')[1].strip(' ')
                    except:
                        x['_id']=x['_id'].strip(' ')

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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'category':{'$eq':'Benefits'}}"
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'category':{'$eq':'Benefits'}}"
                        cond="{'$and':["+cond+pc1+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$producttypeverbose', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        try:
                            x['_id']=x['_id'].split('-')[1].strip(' ')
                        except:
                            x['_id']=x['_id'].strip(' ')

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
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Benefits Calls Volume (By Product Type)")+"'"+","
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

    return " calls_cnt_ben_prod_type function "
# print(get_calls_cnt_ben_prod_type([[],[],['2019'],[]],['141338470']))
def get_calls_cnt_ben_type(dur_lst,provider_lst):

    ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'category':{'$eq':'Benefits'}}"
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'category':{'$eq':'Benefits'}}"
                    cond="{'$and':["+cond+pc1+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$questiontypeverbose', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'category':{'$eq':'Benefits'}}"
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'category':{'$eq':'Benefits'}}"
                        cond="{'$and':["+cond+pc1+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$questiontypeverbose', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
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
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Benefits Calls Volume (By Type)")+"'"+","
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

    return " calls_cnt_ben_type function "
# print(get_calls_cnt_ben_type([[],[],['2019'],[]],['141338470']))
def get_calls_cnt_ben_trnsfr(dur_lst,provider_lst):

    ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'category':{'$eq':'Benefits'}}"
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'category':{'$eq':'Benefits'}}"
                    cond="{'$and':["+cond+pc1+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$transfer', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    if "no" in str(x['_id']).lower().strip(' ') and 'transfer' in str(x['_id']).lower().strip():
                        x['_id']="Not Transferred"
                    else:
                        x['_id']="Transferred"
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'category':{'$eq':'Benefits'}}"
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'category':{'$eq':'Benefits'}}"
                        cond="{'$and':["+cond+pc1+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$transfer', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        if "no" in str(x['_id']).lower().strip(' ') and 'transfer' in str(x['_id']).lower().strip():
                            x['_id']="Not Transferred"
                        else:
                            x['_id']="Transferred"
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
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Benefits Calls Volume (By Transfer)")+"'"+","
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
    

    return " calls_cnt_ben_trnsfr function "
# print(get_calls_cnt_ben_trnsfr([[],[],['2019'],[]],['141338470']))
def get_calls_cnt_ben_ans(dur_lst,provider_lst):

    ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'category':{'$eq':'Benefits'}}"
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'category':{'$eq':'Benefits'}}"
                    cond="{'$and':["+cond+pc1+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$vccd_dispostion', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    if "ringnoanswer" in str(x['_id']).lower():
                        x['_id']="Not Answered"
                    else:
                        x['_id']="Answered"
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'category':{'$eq':'Benefits'}}"
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'category':{'$eq':'Benefits'}}"
                        cond="{'$and':["+cond+pc1+"]}"  
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$vccd_dispostion', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        if "ringnoanswer" in str(x['_id']).lower():
                            x['_id']="Not Answered"
                        else:
                            x['_id']="Answered"
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
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Benefits Calls Volume (By Answered)")+"'"+","
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
    
    return " calls_cnt_ben_ans function "
# print(get_calls_cnt_ben_ans([[],[],['2019'],[]],['141338470']))
def get_calls_cnt_ben_lang(dur_lst,provider_lst):

    ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'category':{'$eq':'Benefits'}}"
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'category':{'$eq':'Benefits'}}"
                    cond="{'$and':["+cond+pc1+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$language', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    if str(x['_id']).strip().lower()=="e":
                        x['_id']="English"
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'category':{'$eq':'Benefits'}}"
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'category':{'$eq':'Benefits'}}"
                        cond="{'$and':["+cond+pc1+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$language', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        if str(x['_id']).strip().lower()=="e":
                            x['_id']="English"
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
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Benefits Calls Volume (By Language)")+"'"+","
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

    return " calls_cnt_ben_lang function "
# print(get_calls_cnt_ben_lang([[],[],['2019'],[]],['141338470']))
def get_calls_cnt_ben_BU(dur_lst,provider_lst):

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'category':{'$eq':'Benefits'}}"
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'category':{'$eq':'Benefits'}}"
                    cond="{'$and':["+cond+pc1+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$bu', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'category':{'$eq':'Benefits'}}"
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'category':{'$eq':'Benefits'}}"
                        cond="{'$and':["+cond+pc1+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$bu', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
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
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Benefits Calls Volume (By BU)")+"'"+","
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

    return " calls_cnt_ben_BU function "
# print(get_calls_cnt_ben_BU([[],[],['2019'],[]],['141338470']))
def get_calls_cnt_ben(dur_lst,provider_lst):

    print(provider_lst)

    try:
        cond=""
        n_records="0"
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name] 
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'category':{'$eq':'Benefits'}}"
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'category':{'$eq':'Benefits'}}"
                    cond="{'$and':["+cond+pc1+"]}"
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'category':{'$eq':'Benefits'}}"
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'category':{'$eq':'Benefits'}}"
                        cond="{'$and':["+cond+pc1+"]}"
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
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Benefits Calls Trend (Volume)")+"'"+","
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
    return " calls_cnt_eligible function "
# print(get_calls_cnt_ben([[],[],['2019'],[]],['141338470']))

def get_calls_cnt_pa_lob(dur_lst,provider_lst):

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'category':{'$eq':'Prior-Auth'}}"
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'category':{'$eq':'Prior-Auth'}}"
                    cond="{'$and':["+cond+pc1+"]}"
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'category':{'$eq':'Prior-Auth'}}"
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'category':{'$eq':'Prior-Auth'}}"
                        cond="{'$and':["+cond+pc1+"]}"
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
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Prior-Auth Calls Volume (By LOB)")+"'"+","
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

    return " calls_cnt_pa_lob function "
# print(get_calls_cnt_pa_lob([[],[],['2019'],[]],['141338470']))
def get_calls_cnt_pa_prod_type(dur_lst,provider_lst):

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'category':{'$eq':'Prior-Auth'}}"
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'category':{'$eq':'Prior-Auth'}}"
                    cond="{'$and':["+cond+pc1+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$producttypeverbose', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    try:
                        x['_id']=x['_id'].split('-')[1].strip(' ')
                    except:
                        x['_id']=x['_id'].strip(' ')

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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'category':{'$eq':'Prior-Auth'}}"
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'category':{'$eq':'Prior-Auth'}}"
                        cond="{'$and':["+cond+pc1+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$producttypeverbose', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        try:
                            x['_id']=x['_id'].split('-')[1].strip(' ')
                        except:
                            x['_id']=x['_id'].strip(' ')

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
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Prior-Auth Calls Volume (By Product Type)")+"'"+","
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

    return " calls_cnt_pa_prod_type function "
# print(get_calls_cnt_pa_prod_type([[],[],['2019'],[]],['141338470']))
def get_calls_cnt_pa_type(dur_lst,provider_lst):

    ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'category':{'$eq':'Prior-Auth'}}"
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'category':{'$eq':'Prior-Auth'}}"
                    cond="{'$and':["+cond+pc1+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$questiontypeverbose', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'category':{'$eq':'Prior-Auth'}}"
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'category':{'$eq':'Prior-Auth'}}"
                        cond="{'$and':["+cond+pc1+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$questiontypeverbose', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
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
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Prior-Auth Calls Volume (By Type)")+"'"+","
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

    return " calls_cnt_pa_type function "
# print(get_calls_cnt_pa_type([[],[],['2019'],[]],['141338470']))
def get_calls_cnt_pa_trnsfr(dur_lst,provider_lst):

    ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'category':{'$eq':'Prior-Auth'}}"
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'category':{'$eq':'Prior-Auth'}}"
                    cond="{'$and':["+cond+pc1+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$transfer', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    if "no" in str(x['_id']).lower().strip(' ') and 'transfer' in str(x['_id']).lower().strip():
                        x['_id']="Not Transferred"
                    else:
                        x['_id']="Transferred"
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'category':{'$eq':'Prior-Auth'}}"
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'category':{'$eq':'Prior-Auth'}}"
                        cond="{'$and':["+cond+pc1+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$transfer', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        if "no" in str(x['_id']).lower().strip(' ') and 'transfer' in str(x['_id']).lower().strip():
                            x['_id']="Not Transferred"
                        else:
                            x['_id']="Transferred"
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
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Prior-Auth Calls Volume (By Transfer)")+"'"+","
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
    

    return " calls_cnt_pa_trnsfr function "
# print(get_calls_cnt_pa_trnsfr([[],[],['2019'],[]],['141338470']))
def get_calls_cnt_pa_ans(dur_lst,provider_lst):

    ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'category':{'$eq':'Prior-Auth'}}"
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'category':{'$eq':'Prior-Auth'}}"
                    cond="{'$and':["+cond+pc1+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$vccd_dispostion', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    if "ringnoanswer" in str(x['_id']).lower():
                        x['_id']="Not Answered"
                    else:
                        x['_id']="Answered"
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'category':{'$eq':'Prior-Auth'}}"
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'category':{'$eq':'Prior-Auth'}}"
                        cond="{'$and':["+cond+pc1+"]}"  
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$vccd_dispostion', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        if "ringnoanswer" in str(x['_id']).lower():
                            x['_id']="Not Answered"
                        else:
                            x['_id']="Answered"
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
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Prior-Auth Calls Volume (By Answered)")+"'"+","
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
    
    return " calls_cnt_pa_ans function "
# print(get_calls_cnt_pa_ans([[],[],['2019'],[]],['141338470']))
def get_calls_cnt_pa_lang(dur_lst,provider_lst):

    ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'category':{'$eq':'Prior-Auth'}}"
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'category':{'$eq':'Prior-Auth'}}"
                    cond="{'$and':["+cond+pc1+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$language', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    if str(x['_id']).strip().lower()=="e":
                        x['_id']="English"
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'category':{'$eq':'Prior-Auth'}}"
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'category':{'$eq':'Prior-Auth'}}"
                        cond="{'$and':["+cond+pc1+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$language', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        if str(x['_id']).strip().lower()=="e":
                            x['_id']="English"
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
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Prior-Auth Calls Volume (By Language)")+"'"+","
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

    return " calls_cnt_pa_lang function "
# print(get_calls_cnt_pa_lang([[],[],['2019'],[]],['141338470']))
def get_calls_cnt_pa_BU(dur_lst,provider_lst):

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'category':{'$eq':'Prior-Auth'}}"
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'category':{'$eq':'Prior-Auth'}}"
                    cond="{'$and':["+cond+pc1+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$bu', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'category':{'$eq':'Prior-Auth'}}"
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'category':{'$eq':'Prior-Auth'}}"
                        cond="{'$and':["+cond+pc1+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$bu', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
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
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Prior-Auth Calls Volume (By BU)")+"'"+","
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

    return " calls_cnt_pa_BU function "
# print(get_calls_cnt_pa_BU([[],[],['2019'],[]],['141338470']))
def get_calls_cnt_pa(dur_lst,provider_lst):

    print(provider_lst)

    try:
        cond=""
        n_records="0"
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name] 
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'category':{'$eq':'Prior-Auth'}}"
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'category':{'$eq':'Prior-Auth'}}"
                    cond="{'$and':["+cond+pc1+"]}"
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'category':{'$eq':'Prior-Auth'}}"
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'category':{'$eq':'Prior-Auth'}}"
                        cond="{'$and':["+cond+pc1+"]}"
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
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Prior-Auth Calls Trend (Volume)")+"'"+","
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
    return " calls_cnt_pa function "
# print(get_calls_cnt_pa([[],[],['2019'],[]],['141338470']))
def get_calls_cnt_claims_lob(dur_lst,provider_lst):

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'category':{'$eq':'Claims'}}"
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'category':{'$eq':'Claims'}}"
                    cond="{'$and':["+cond+pc1+"]}"
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'category':{'$eq':'Claims'}}"
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'category':{'$eq':'Claims'}}"
                        cond="{'$and':["+cond+pc1+"]}"
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
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Calls Volume (By LOB)")+"'"+","
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

    return " calls_cnt_Claims_lob function "
# print(get_calls_cnt_claims_lob([[],[],['2019'],[]],['141338470']))
def get_calls_cnt_claims_prod_type(dur_lst,provider_lst):

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'category':{'$eq':'Claims'}}"
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'category':{'$eq':'Claims'}}"
                    cond="{'$and':["+cond+pc1+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$producttypeverbose', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    try:
                        x['_id']=x['_id'].split('-')[1].strip(' ')
                    except:
                        x['_id']=x['_id'].strip(' ')

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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'category':{'$eq':'Claims'}}"
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'category':{'$eq':'Claims'}}"
                        cond="{'$and':["+cond+pc1+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$producttypeverbose', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        try:
                            x['_id']=x['_id'].split('-')[1].strip(' ')
                        except:
                            x['_id']=x['_id'].strip(' ')

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
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Calls Volume (By Product Type)")+"'"+","
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

    return " calls_cnt_Claims_prod_type function "
# print(get_calls_cnt_claims_prod_type([[],[],['2019'],[]],['141338470']))
def get_calls_cnt_claims_type(dur_lst,provider_lst):

    ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'category':{'$eq':'Claims'}}"
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'category':{'$eq':'Claims'}}"
                    cond="{'$and':["+cond+pc1+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$questiontypeverbose', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'category':{'$eq':'Claims'}}"
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'category':{'$eq':'Claims'}}"
                        cond="{'$and':["+cond+pc1+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$questiontypeverbose', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
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
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Calls Volume (By Type)")+"'"+","
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

    return " calls_cnt_Claims_type function "
# print(get_calls_cnt_claims_type([[],[],['2019'],[]],['141338470']))
def get_calls_cnt_claims_trnsfr(dur_lst,provider_lst):

    ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'category':{'$eq':'Claims'}}"
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'category':{'$eq':'Claims'}}"
                    cond="{'$and':["+cond+pc1+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$transfer', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    if "no" in str(x['_id']).lower().strip(' ') and 'transfer' in str(x['_id']).lower().strip():
                        x['_id']="Not Transferred"
                    else:
                        x['_id']="Transferred"
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'category':{'$eq':'Claims'}}"
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'category':{'$eq':'Claims'}}"
                        cond="{'$and':["+cond+pc1+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$transfer', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        if "no" in str(x['_id']).lower().strip(' ') and 'transfer' in str(x['_id']).lower().strip():
                            x['_id']="Not Transferred"
                        else:
                            x['_id']="Transferred"
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
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Calls Volume (By Transfer)")+"'"+","
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
    

    return " calls_cnt_Claims_trnsfr function "
# print(get_calls_cnt_claims_trnsfr([[],[],['2019'],[]],['141338470']))
def get_calls_cnt_claims_ans(dur_lst,provider_lst):

    ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'category':{'$eq':'Claims'}}"
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'category':{'$eq':'Claims'}}"
                    cond="{'$and':["+cond+pc1+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$vccd_dispostion', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    if "ringnoanswer" in str(x['_id']).lower():
                        x['_id']="Not Answered"
                    else:
                        x['_id']="Answered"
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'category':{'$eq':'Claims'}}"
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'category':{'$eq':'Claims'}}"
                        cond="{'$and':["+cond+pc1+"]}"  
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$vccd_dispostion', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        if "ringnoanswer" in str(x['_id']).lower():
                            x['_id']="Not Answered"
                        else:
                            x['_id']="Answered"
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
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Calls Volume (By Answered)")+"'"+","
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
    
    return " calls_cnt_Claims_ans function "
# print(get_calls_cnt_claims_ans([[],[],['2019'],[]],['141338470']))
def get_calls_cnt_claims_lang(dur_lst,provider_lst):

    ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'category':{'$eq':'Claims'}}"
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'category':{'$eq':'Claims'}}"
                    cond="{'$and':["+cond+pc1+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$language', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    if str(x['_id']).strip().lower()=="e":
                        x['_id']="English"
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'category':{'$eq':'Claims'}}"
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'category':{'$eq':'Claims'}}"
                        cond="{'$and':["+cond+pc1+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$language', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        if str(x['_id']).strip().lower()=="e":
                            x['_id']="English"
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
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Calls Volume (By Language)")+"'"+","
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

    return " calls_cnt_Claims_lang function "
# print(get_calls_cnt_claims_lang([[],[],['2019'],[]],['141338470']))
def get_calls_cnt_claims_BU(dur_lst,provider_lst):

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'category':{'$eq':'Claims'}}"
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'category':{'$eq':'Claims'}}"
                    cond="{'$and':["+cond+pc1+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$bu', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'category':{'$eq':'Claims'}}"
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'category':{'$eq':'Claims'}}"
                        cond="{'$and':["+cond+pc1+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$bu', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
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
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Calls Volume (By BU)")+"'"+","
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

    return " calls_cnt_Claims_BU function "
# print(get_calls_cnt_claims_BU([[],[],['2019'],[]],['141338470']))
def get_calls_cnt_claims(dur_lst,provider_lst):

    print(provider_lst)

    try:
        cond=""
        n_records="0"
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name] 
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'category':{'$eq':'Claims'}}"
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'category':{'$eq':'Claims'}}"
                    cond="{'$and':["+cond+pc1+"]}"
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'category':{'$eq':'Claims'}}"
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'category':{'$eq':'Claims'}}"
                        cond="{'$and':["+cond+pc1+"]}"
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
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Claims Calls Trend (Volume)")+"'"+","
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
    return " calls_cnt_Claims function "
# print(get_calls_cnt_claims([[],[],['2019'],[]],['141338470']))

def get_calls_cnt_appeal_lob(dur_lst,provider_lst):

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'category':{'$eq':'Appeal'}}"
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'category':{'$eq':'Appeal'}}"
                    cond="{'$and':["+cond+pc1+"]}"
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'category':{'$eq':'Appeal'}}"
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'category':{'$eq':'Appeal'}}"
                        cond="{'$and':["+cond+pc1+"]}"
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
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Appeal Calls Volume (By LOB)")+"'"+","
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

    return " calls_cnt_Appeal_lob function "
# print(get_calls_cnt_appeal_lob([[],[],['2019'],[]],['141338470']))
def get_calls_cnt_appeal_prod_type(dur_lst,provider_lst):

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'category':{'$eq':'Appeal'}}"
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'category':{'$eq':'Appeal'}}"
                    cond="{'$and':["+cond+pc1+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$producttypeverbose', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    try:
                        x['_id']=x['_id'].split('-')[1].strip(' ')
                    except:
                        x['_id']=x['_id'].strip(' ')

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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'category':{'$eq':'Appeal'}}"
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'category':{'$eq':'Appeal'}}"
                        cond="{'$and':["+cond+pc1+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$producttypeverbose', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        try:
                            x['_id']=x['_id'].split('-')[1].strip(' ')
                        except:
                            x['_id']=x['_id'].strip(' ')

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
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Appeal Calls Volume (By Product Type)")+"'"+","
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

    return " calls_cnt_Appeal_prod_type function "
# print(get_calls_cnt_appeal_prod_type([[],[],['2019'],[]],['141338470']))
def get_calls_cnt_appeal_type(dur_lst,provider_lst):

    ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'category':{'$eq':'Appeal'}}"
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'category':{'$eq':'Appeal'}}"
                    cond="{'$and':["+cond+pc1+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$questiontypeverbose', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'category':{'$eq':'Appeal'}}"
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'category':{'$eq':'Appeal'}}"
                        cond="{'$and':["+cond+pc1+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$questiontypeverbose', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
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
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Appeal Calls Volume (By Type)")+"'"+","
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

    return " calls_cnt_Appeal_type function "
# print(get_calls_cnt_appeal_type([[],[],['2019'],[]],['141338470']))
def get_calls_cnt_appeal_trnsfr(dur_lst,provider_lst):

    ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'category':{'$eq':'Appeal'}}"
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'category':{'$eq':'Appeal'}}"
                    cond="{'$and':["+cond+pc1+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$transfer', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    if "no" in str(x['_id']).lower().strip(' ') and 'transfer' in str(x['_id']).lower().strip():
                        x['_id']="Not Transferred"
                    else:
                        x['_id']="Transferred"
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'category':{'$eq':'Appeal'}}"
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'category':{'$eq':'Appeal'}}"
                        cond="{'$and':["+cond+pc1+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$transfer', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        if "no" in str(x['_id']).lower().strip(' ') and 'transfer' in str(x['_id']).lower().strip():
                            x['_id']="Not Transferred"
                        else:
                            x['_id']="Transferred"
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
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Appeal Calls Volume (By Transfer)")+"'"+","
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
    

    return " calls_cnt_Appeal_trnsfr function "
# print(get_calls_cnt_appeal_trnsfr([[],[],['2019'],[]],['141338470']))
def get_calls_cnt_appeal_ans(dur_lst,provider_lst):

    ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'category':{'$eq':'Appeal'}}"
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'category':{'$eq':'Appeal'}}"
                    cond="{'$and':["+cond+pc1+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$vccd_dispostion', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    if "ringnoanswer" in str(x['_id']).lower():
                        x['_id']="Not Answered"
                    else:
                        x['_id']="Answered"
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'category':{'$eq':'Appeal'}}"
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'category':{'$eq':'Appeal'}}"
                        cond="{'$and':["+cond+pc1+"]}"  
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$vccd_dispostion', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        if "ringnoanswer" in str(x['_id']).lower():
                            x['_id']="Not Answered"
                        else:
                            x['_id']="Answered"
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
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Appeal Calls Volume (By Answered)")+"'"+","
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
    
    return " calls_cnt_Appeal_ans function "
# print(get_calls_cnt_appeal_ans([[],[],['2019'],[]],['141338470']))
def get_calls_cnt_appeal_lang(dur_lst,provider_lst):

    ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'category':{'$eq':'Appeal'}}"
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'category':{'$eq':'Appeal'}}"
                    cond="{'$and':["+cond+pc1+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$language', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    if str(x['_id']).strip().lower()=="e":
                        x['_id']="English"
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'category':{'$eq':'Appeal'}}"
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'category':{'$eq':'Appeal'}}"
                        cond="{'$and':["+cond+pc1+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$language', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        if str(x['_id']).strip().lower()=="e":
                            x['_id']="English"
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
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Appeal Calls Volume (By Language)")+"'"+","
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

    return " calls_cnt_Appeal_lang function "
# print(get_calls_cnt_appeal_lang([[],[],['2019'],[]],['141338470']))
def get_calls_cnt_appeal_BU(dur_lst,provider_lst):

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'category':{'$eq':'Appeal'}}"
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'category':{'$eq':'Appeal'}}"
                    cond="{'$and':["+cond+pc1+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$bu', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'category':{'$eq':'Appeal'}}"
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'category':{'$eq':'Appeal'}}"
                        cond="{'$and':["+cond+pc1+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$bu', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
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
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Appeal Calls Volume (By BU)")+"'"+","
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

    return " calls_cnt_Appeal_BU function "
# print(get_calls_cnt_appeal_BU([[],[],['2019'],[]],['141338470']))
def get_calls_cnt_appeal(dur_lst,provider_lst):

    print(provider_lst)

    try:
        cond=""
        n_records="0"
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name] 
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'category':{'$eq':'Appeal'}}"
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'category':{'$eq':'Appeal'}}"
                    cond="{'$and':["+cond+pc1+"]}"
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'category':{'$eq':'Appeal'}}"
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'category':{'$eq':'Appeal'}}"
                        cond="{'$and':["+cond+pc1+"]}"
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
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Appeal Calls Trend (Volume)")+"'"+","
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
    return " calls_cnt_Appeal function "
# print(get_calls_cnt_appeal([[],[],['2019'],[]],['141338470']))
def get_calls_cnt_lob(dur_lst,provider_lst):

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    # pc1=",{'category':{'$eq':'Appeal'}}"
                    pc1=""
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'category':{'$eq':'Appeal'}}"
                    pc1=""
                    cond="{'$and':["+cond+pc1+"]}"
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'category':{'$eq':'Appeal'}}"
                        pc1=""
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'category':{'$eq':'Appeal'}}"
                        pc1=""
                        cond="{'$and':["+cond+pc1+"]}"
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
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Calls Volume (By LOB)")+"'"+","
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

    return " calls_cnt_lob function "
# print(get_calls_cnt_lob([[],[],['2019'],[]],['141338470']))
def get_calls_cnt_prod_type(dur_lst,provider_lst):

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'category':{'$eq':'Appeal'}}"
                    pc1=""
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'category':{'$eq':'Appeal'}}"
                    pc1=""
                    cond="{'$and':["+cond+pc1+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$producttypeverbose', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    try:
                        x['_id']=x['_id'].split('-')[1].strip(' ')
                    except:
                        x['_id']=x['_id'].strip(' ')

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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'category':{'$eq':'Appeal'}}"
                        pc1=""
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'category':{'$eq':'Appeal'}}"
                        pc1=""
                        cond="{'$and':["+cond+pc1+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$producttypeverbose', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        try:
                            x['_id']=x['_id'].split('-')[1].strip(' ')
                        except:
                            x['_id']=x['_id'].strip(' ')

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
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Calls Volume (By Product Type)")+"'"+","
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

    return " calls_cnt_prod_type function "
# print(get_calls_cnt_prod_type([[],[],['2019'],[]],['141338470']))
def get_calls_cnt_type(dur_lst,provider_lst):

    ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'category':{'$eq':'Appeal'}}"
                    pc1=""
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'category':{'$eq':'Appeal'}}"
                    pc1=""
                    cond="{'$and':["+cond+pc1+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$category', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'category':{'$eq':'Appeal'}}"
                        pc1=""
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'category':{'$eq':'Appeal'}}"
                        pc1=""
                        cond="{'$and':["+cond+pc1+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$category', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
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
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Calls Volume (By Category)")+"'"+","
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

    return " calls_cnt_type function "
# print(get_calls_cnt_type([[],[],['2019'],[]],['141338470']))
def get_calls_cnt_trnsfr_by(dur_lst,provider_lst):

    ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'category':{'$eq':'Appeal'}}"
                    pc1=""
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'category':{'$eq':'Appeal'}}"
                    pc1=""
                    cond="{'$and':["+cond+pc1+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$transfer', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    if "no" in str(x['_id']).lower().strip(' ') and 'transfer' in str(x['_id']).lower().strip():
                        x['_id']="Not Transferred"
                    else:
                        x['_id']="Transferred"
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'category':{'$eq':'Appeal'}}"
                        pc1=""
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'category':{'$eq':'Appeal'}}"
                        pc1=""
                        cond="{'$and':["+cond+pc1+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$transfer', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        if "no" in str(x['_id']).lower().strip(' ') and 'transfer' in str(x['_id']).lower().strip():
                            x['_id']="Not Transferred"
                        else:
                            x['_id']="Transferred"
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
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Calls Volume (By Transfer)")+"'"+","
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
    

    return " calls_cnt_trnsfr function "
# print(get_calls_cnt_trnsfr_by([[],[],['2019'],[]],['141338470']))
def get_calls_cnt_ans_by(dur_lst,provider_lst):

    ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'category':{'$eq':'Appeal'}}"
                    pc1=""
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'category':{'$eq':'Appeal'}}"
                    pc1=""
                    cond="{'$and':["+cond+pc1+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$vccd_dispostion', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    if "ringnoanswer" in str(x['_id']).lower():
                        x['_id']="Not Answered"
                    else:
                        x['_id']="Answered"
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'category':{'$eq':'Appeal'}}"
                        pc1=""
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'category':{'$eq':'Appeal'}}"
                        pc1=""
                        cond="{'$and':["+cond+pc1+"]}"  
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$vccd_dispostion', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        if "ringnoanswer" in str(x['_id']).lower():
                            print("entered if of ringnoanswer")
                            x['_id']="Not Answered"
                        else:
                            x['_id']="Answered"
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
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Calls Volume (By Answered)")+"'"+","
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
    
    return " calls_cnt_ans function "
# print(get_calls_cnt_ans_by([[],[],['2019'],[]],['133964321']))
def get_calls_cnt_lang(dur_lst,provider_lst):

    ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'category':{'$eq':'Appeal'}}"
                    pc1=""
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'category':{'$eq':'Appeal'}}"
                    pc1=""
                    cond="{'$and':["+cond+pc1+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$language', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    if str(x['_id']).strip().lower()=="e":
                        x['_id']="English"
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'category':{'$eq':'Appeal'}}"
                        pc1=""
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'category':{'$eq':'Appeal'}}"
                        pc1=""
                        cond="{'$and':["+cond+pc1+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$language', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        if str(x['_id']).strip().lower()=="e":
                            x['_id']="English"
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
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Calls Volume (By Language)")+"'"+","
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

    return " calls_cnt_lang function "
# print(get_calls_cnt_lang([[],[],['2019'],[]],['141338470']))
def get_calls_cnt_BU(dur_lst,provider_lst):

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'category':{'$eq':'Appeal'}}"
                    pc1=""
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'category':{'$eq':'Appeal'}}"
                    pc1=""
                    cond="{'$and':["+cond+pc1+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$bu', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'category':{'$eq':'Appeal'}}"
                        pc1=""
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'category':{'$eq':'Appeal'}}"
                        pc1=""
                        cond="{'$and':["+cond+pc1+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$bu', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
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
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Calls Volume (By BU)")+"'"+","
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

    return " calls_cnt_BU function "
# print(get_calls_cnt_BU([[],[],['2019'],[]],['141338470']))
def get_calls_cnt(dur_lst,provider_lst):

    print(provider_lst)

    try:
        cond=""
        n_records="0"
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name] 
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'category':{'$eq':'Appeal'}}"
                    pc1=""
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'category':{'$eq':'Appeal'}}"
                    pc1=""
                    cond="{'$and':["+cond+pc1+"]}"
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'category':{'$eq':'Appeal'}}"
                        pc1=""
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'category':{'$eq':'Appeal'}}"
                        pc1=""
                        cond="{'$and':["+cond+pc1+"]}"
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
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Calls Trend (Volume)")+"'"+","
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
    return " calls_cnt function "
# print(get_calls_cnt([[],[],['2019'],[]],['141338470']))

def get_calls_tat_hold_lob(dur_lst,provider_lst):
    ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    cond="{'$and':["+cond+pc+"]}"
                else:
                    cond="{'$and':["+cond+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$lob_id', 'total': {'$avg': {'$convert':{'input':'$holdtime','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    if x['total']==None:
                        continue
                    # print(x['_id'])
                    # print(x['total'])
                    x['total']=round(float(str(x['total'])),2)
                    if x['_id'] in claim_type_lst:
                        cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(float(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+float(x['total']))
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        cond="{'$and':["+cond+pc+"]}"
                    else:
                        cond="{'$and':["+cond+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$lob_id', 'total': {'$avg': {'$convert':{'input':'$holdtime','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        if x['total']==None:
                            continue
                        # print(x['_id'])
                        # print(x['total'])                        
                        x['total']=round(float(str(x['total'])),2)
                        if x['_id'] in claim_type_lst:
                            cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(float(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+float(x['total']))
                        else:
                            claim_type_lst.append(str(x['_id']))
                            cliam_type_cnt_lst.append(str(x['total'])) 
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        for li in range(0,len(cliam_type_cnt_lst)):
            cliam_type_cnt_lst[li]=str(round(float(cliam_type_cnt_lst[li]),2))
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Calls Hold Time (By LOB)")+"'"+","
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

    return " calls_tat_hold_lob function "
# print(get_calls_tat_hold_lob([[],[],['2019'],[]],['141338470']))
def get_calls_tat_hold_prod_type(dur_lst,provider_lst):
        ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    cond="{'$and':["+cond+pc+"]}"
                else:
                    cond="{'$and':["+cond+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)                  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$producttypeverbose', 'total': {'$avg': {'$convert':{'input':'$holdtime','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    if x['total']==None:
                        continue
                    try:
                        x['_id']=x['_id'].split('-')[1].strip(' ')
                    except:
                        x['_id']=x['_id'].strip(' ')
                    # print(x['_id'])
                    # print(x['total'])
                    x['total']=round(float(str(x['total'])),2)
                    if x['_id'] in claim_type_lst:
                        cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(float(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+float(x['total']))
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        cond="{'$and':["+cond+pc+"]}"
                    else:
                        cond="{'$and':["+cond+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)                      
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$producttypeverbose', 'total': {'$avg': {'$convert':{'input':'$holdtime','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        if x['total']==None:
                            continue
                        # print(x['_id'])
                        # print(x['total'])
                        try:
                            x['_id']=x['_id'].split('-')[1].strip(' ')
                        except:
                            x['_id']=x['_id'].strip(' ')
                        x['total']=round(float(str(x['total'])),2)
                        if x['_id'] in claim_type_lst:
                            cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(float(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+float(x['total']))
                        else:
                            claim_type_lst.append(str(x['_id']))
                            cliam_type_cnt_lst.append(str(x['total']))
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        for li in range(0,len(cliam_type_cnt_lst)):
            cliam_type_cnt_lst[li]=str(round(float(cliam_type_cnt_lst[li]),2))
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Calls Hold Time (By Product Type)")+"'"+","
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

    return " calls_tat_hold_prod_type function "
# print(get_calls_tat_hold_prod_type([[],[],['2019'],[]],['141338470']))
def get_calls_tat_hold_type(dur_lst,provider_lst):
    
    ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    cond="{'$and':["+cond+pc+"]}"
                else:
                    cond="{'$and':["+cond+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$category', 'total': {'$avg': {'$convert':{'input':'$holdtime','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    if x['total']==None:
                        continue
                    # print(x['_id'])
                    # print(x['total'])
                    x['total']=round(float(str(x['total'])),2)
                    if x['_id'] in claim_type_lst:
                        cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(float(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+float(x['total']))
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        cond="{'$and':["+cond+pc+"]}"
                    else:
                        cond="{'$and':["+cond+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$category', 'total': {'$avg': {'$convert':{'input':'$holdtime','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        if x['total']==None:
                            continue
                        # print(x['_id'])
                        # print(x['total'])
                        x['total']=round(float(str(x['total'])),2)
                        if x['_id'] in claim_type_lst:
                            cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(float(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+float(x['total']))
                        else:
                            claim_type_lst.append(str(x['_id']))
                            cliam_type_cnt_lst.append(str(x['total']))
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        for li in range(0,len(cliam_type_cnt_lst)):
            cliam_type_cnt_lst[li]=str(round(float(cliam_type_cnt_lst[li]),2))
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Calls Hold Time (By Category)")+"'"+","
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

    return " calls_tat_hold_type function "
# print(get_calls_tat_hold_type([[],[],['2019'],[]],['141338470']))
def get_calls_tat_hold_trnsfr(dur_lst,provider_lst):

    ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=""
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    # pc1=",{'transfer':{'$ne':"+str("No Transfer")+"}}"
                    pc1=""
                    cond="{'$and':["+cond+pc1+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$transfer', 'total': {'$avg': {'$convert':{'input':'$holdtime','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    if x['total']==None:
                        continue
                    x['total']=round(float(str(x['total'])),2)
                    if "no" in str(x['_id']).lower().strip(' ') and 'transfer' in str(x['_id']).lower().strip():
                        x['_id']="Not Transferred"
                    else:
                        x['_id']="Transferred"
                    if x['_id'] in claim_type_lst:
                        cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(float(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+float(x['total']))
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        # pc1=",{'transfer':{'$ne':"+str("No Transfer")+"}}"
                        pc1=""
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        # pc1=",{'transfer':{'$ne':"+str("No Transfer")+"}}"
                        pc1=""
                        cond="{'$and':["+cond+pc1+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$transfer', 'total': {'$avg': {'$convert':{'input':'$holdtime','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        if x['total']==None:
                            continue
                        x['total']=round(float(str(x['total'])),2)
                        if "no" in str(x['_id']).lower().strip(' ') and 'transfer' in str(x['_id']).lower().strip():
                            x['_id']="Not Transferred"
                        else:
                            x['_id']="Transferred"
                        if x['_id'] in claim_type_lst:
                            cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(float(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+float(x['total']))
                        else:
                            claim_type_lst.append(str(x['_id']))
                            cliam_type_cnt_lst.append(str(x['total']))
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        for li in range(0,len(cliam_type_cnt_lst)):
            cliam_type_cnt_lst[li]=str(round(float(cliam_type_cnt_lst[li]),2))
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Calls Hold Time (By Transferred)")+"'"+","
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

    return " calls_tat_hold_trnsfr function "
# print(get_calls_tat_hold_trnsfr([[],[],['2019'],[]],['141338470']))
def get_calls_tat_hold_ans(dur_lst,provider_lst):

    ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    # pc1=",{'talktime':{'$ne':"+str("0")+"}}"
                    pc1=""
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    # pc1=",{'talktime':{'$ne':"+str("0")+"}}"
                    pc1=""
                    cond="{'$and':["+cond+pc1+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)                  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$vccd_dispostion', 'total': {'$avg': {'$convert':{'input':'$holdtime','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    if x['total']==None:
                        continue
                    x['total']=round(float(str(x['total'])),2)
                    if "ringnoanswer" in str(x['_id']).lower():
                        x['_id']="Not Answered"
                    else:
                        x['_id']="Answered"
                    if x['_id'] in claim_type_lst:
                        cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(float(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+float(x['total']))
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        # pc1=",{'talktime':{'$ne':"+str("0")+"}}"
                        pc1=""
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        # pc1=",{'talktime':{'$ne':"+str("0")+"}}"
                        pc1=""
                        cond="{'$and':["+cond+pc1+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$vccd_dispostion', 'total': {'$avg': {'$convert':{'input':'$holdtime','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        if x['total']==None:
                            continue
                        x['total']=round(float(str(x['total'])),2)
                        if "ringnoanswer" in str(x['_id']).lower():
                            x['_id']="Not Answered"
                        else:
                            x['_id']="Answered"
                        if x['_id'] in claim_type_lst:
                            cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(float(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+float(x['total']))
                        else:
                            claim_type_lst.append(str(x['_id']))
                            cliam_type_cnt_lst.append(str(x['total'])) 
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        for li in range(0,len(cliam_type_cnt_lst)):
            cliam_type_cnt_lst[li]=str(round(float(cliam_type_cnt_lst[li]),2))
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Calls Hold Time (By Answered)")+"'"+","
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
    
    

    return " calls_tat_hold_ans function "
# print(get_calls_tat_hold_ans([[],[],['2019'],[]],['141338470']))
def get_calls_tat_hold_lang(dur_lst,provider_lst):
    ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    cond="{'$and':["+cond+pc+"]}"
                else:
                    cond="{'$and':["+cond+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)                  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$language', 'total': {'$avg': {'$convert':{'input':'$holdtime','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:                    
                    if x['total']==None:
                        continue
                    x['total']=round(float(str(x['total'])),2)
                    if x['_id'] in claim_type_lst:
                        cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(float(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+float(x['total']))
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        cond="{'$and':["+cond+pc+"]}"
                    else:
                        cond="{'$and':["+cond+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$language', 'total': {'$avg': {'$convert':{'input':'$holdtime','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        if x['total']==None:
                            continue
                        x['total']=round(float(str(x['total'])),2)

                        if x['_id'] in claim_type_lst:
                            cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(float(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+float(x['total']))
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
            if claim_type_lst[li].strip(' ').upper()=="E":
                claim_type_lst[li]="English"
            # claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        for li in range(0,len(cliam_type_cnt_lst)):
            cliam_type_cnt_lst[li]=str(round(float(cliam_type_cnt_lst[li]),2))
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Calls Hold Time (By Language)")+"'"+","
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

    return " calls_tat_hold_lang function "
# print(get_calls_tat_hold_lang([[],[],['2019'],[]],['141338470']))
def get_calls_tat_hold_BU(dur_lst,provider_lst):
    ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    cond="{'$and':["+cond+pc+"]}"
                else:
                    cond="{'$and':["+cond+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$bu', 'total': {'$avg': {'$convert':{'input':'$holdtime','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    if x['total']==None:
                        continue
                    # print(x['_id'])
                    # print(x['total'])
                    x['total']=round(float(str(x['total'])),2)
                    if x['_id'] in claim_type_lst:
                        cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(float(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+float(x['total']))
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        cond="{'$and':["+cond+pc+"]}"
                    else:
                        cond="{'$and':["+cond+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$bu', 'total': {'$avg': {'$convert':{'input':'$holdtime','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        if x['total']==None:
                            continue
                        # print(x['_id'])
                        # print(x['total'])
                        x['total']=round(float(str(x['total'])),2)
                        if x['_id'] in claim_type_lst:
                            cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(float(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+float(x['total']))
                        else:
                            claim_type_lst.append(str(x['_id']))
                            cliam_type_cnt_lst.append(str(x['total'])) 
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        for li in range(0,len(cliam_type_cnt_lst)):
            cliam_type_cnt_lst[li]=str(round(float(cliam_type_cnt_lst[li]),2))
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Calls Hold Time (By BU)")+"'"+","
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

    return " calls_tat_hold_BU function "
# print(get_calls_tat_hold_BU([[],[],['2019'],[]],['141338470']))
def get_calls_tat_hold(dur_lst,provider_lst):
    print(provider_lst)

    try:
        cond=""
        n_records="0"
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name] 
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    cond="{'$and':["+cond+pc+"]}"
                else:
                    cond="{'$and':["+cond+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)                 
                pipe = [{'$match':my_dict},{'$group': {'_id':'null', 'total': {'$avg': {'$convert':{'input':'$holdtime','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=0
                for x in mydoc:
                    n_records=n_records+x['total'] 
                n_records=str(n_records) 
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        cond="{'$and':["+cond+pc+"]}"
                    else:
                        cond="{'$and':["+cond+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'null', 'total': {'$avg': {'$convert':{'input':'$holdtime','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=0
                    for x in mydoc:
                        n_records=n_records+x['total'] 
                    n_records=str(n_records)    
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        for li in range(0,len(val_lst)):
            val_lst[li]=str(round(float(val_lst[li]),2))
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Calls Hold Time Trend")+"'"+","
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
# print(get_calls_tat_hold([[],[],['2019'],[]],['141338470']))
def get_calls_tat_ring_lob(dur_lst,provider_lst):
    ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    cond="{'$and':["+cond+pc+"]}"
                else:
                    cond="{'$and':["+cond+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$lob_id', 'total': {'$avg': {'$convert':{'input':'$ringtime','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    if x['total']==None:
                        continue
                    # print(x['_id'])
                    # print(x['total'])
                    x['total']=round(float(str(x['total'])),2)
                    if x['_id'] in claim_type_lst:
                        cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(float(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+float(x['total']))
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        cond="{'$and':["+cond+pc+"]}"
                    else:
                        cond="{'$and':["+cond+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$lob_id', 'total': {'$avg': {'$convert':{'input':'$ringtime','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        if x['total']==None:
                            continue
                        # print(x['_id'])
                        # print(x['total'])                        
                        x['total']=round(float(str(x['total'])),2)
                        if x['_id'] in claim_type_lst:
                            cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(float(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+float(x['total']))
                        else:
                            claim_type_lst.append(str(x['_id']))
                            cliam_type_cnt_lst.append(str(x['total'])) 
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        for li in range(0,len(cliam_type_cnt_lst)):
            cliam_type_cnt_lst[li]=str(round(float(cliam_type_cnt_lst[li]),2))
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Calls ring Time (By LOB)")+"'"+","
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

    return " calls_tat_ring_lob function "
# print(get_calls_tat_ring_lob([[],[],['2019'],[]],['141338470']))
def get_calls_tat_ring_prod_type(dur_lst,provider_lst):
        ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    cond="{'$and':["+cond+pc+"]}"
                else:
                    cond="{'$and':["+cond+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)                  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$producttypeverbose', 'total': {'$avg': {'$convert':{'input':'$ringtime','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    if x['total']==None:
                        continue
                    try:
                        x['_id']=x['_id'].split('-')[1].strip(' ')
                    except:
                        x['_id']=x['_id'].strip(' ')
                    # print(x['_id'])
                    # print(x['total'])
                    x['total']=round(float(str(x['total'])),2)
                    if x['_id'] in claim_type_lst:
                        cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(float(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+float(x['total']))
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        cond="{'$and':["+cond+pc+"]}"
                    else:
                        cond="{'$and':["+cond+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)                      
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$producttypeverbose', 'total': {'$avg': {'$convert':{'input':'$ringtime','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        if x['total']==None:
                            continue
                        # print(x['_id'])
                        # print(x['total'])
                        try:
                            x['_id']=x['_id'].split('-')[1].strip(' ')
                        except:
                            x['_id']=x['_id'].strip(' ')
                        x['total']=round(float(str(x['total'])),2)
                        if x['_id'] in claim_type_lst:
                            cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(float(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+float(x['total']))
                        else:
                            claim_type_lst.append(str(x['_id']))
                            cliam_type_cnt_lst.append(str(x['total']))
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        for li in range(0,len(cliam_type_cnt_lst)):
            cliam_type_cnt_lst[li]=str(round(float(cliam_type_cnt_lst[li]),2))
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Calls ring Time (By Product Type)")+"'"+","
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

    return " calls_tat_ring_prod_type function "
# print(get_calls_tat_ring_prod_type([[],[],['2019'],[]],['141338470']))
def get_calls_tat_ring_type(dur_lst,provider_lst):
    
    ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    cond="{'$and':["+cond+pc+"]}"
                else:
                    cond="{'$and':["+cond+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$category', 'total': {'$avg': {'$convert':{'input':'$ringtime','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    if x['total']==None:
                        continue
                    # print(x['_id'])
                    # print(x['total'])
                    x['total']=round(float(str(x['total'])),2)
                    if x['_id'] in claim_type_lst:
                        cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(float(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+float(x['total']))
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        cond="{'$and':["+cond+pc+"]}"
                    else:
                        cond="{'$and':["+cond+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$category', 'total': {'$avg': {'$convert':{'input':'$ringtime','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        if x['total']==None:
                            continue
                        # print(x['_id'])
                        # print(x['total'])
                        x['total']=round(float(str(x['total'])),2)
                        if x['_id'] in claim_type_lst:
                            cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(float(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+float(x['total']))
                        else:
                            claim_type_lst.append(str(x['_id']))
                            cliam_type_cnt_lst.append(str(x['total']))
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        for li in range(0,len(cliam_type_cnt_lst)):
            cliam_type_cnt_lst[li]=str(round(float(cliam_type_cnt_lst[li]),2))
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Calls ring Time (By Category)")+"'"+","
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

    return " calls_tat_ring_type function "
# print(get_calls_tat_ring_type([[],[],['2019'],[]],['141338470']))
def get_calls_tat_ring_trnsfr(dur_lst,provider_lst):

    ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=""
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    # pc1=",{'transfer':{'$ne':"+str("No Transfer")+"}}"
                    pc1=""
                    cond="{'$and':["+cond+pc1+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$transfer', 'total': {'$avg': {'$convert':{'input':'$ringtime','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    if x['total']==None:
                        continue
                    x['total']=round(float(str(x['total'])),2)
                    if "no" in str(x['_id']).lower().strip(' ') and 'transfer' in str(x['_id']).lower().strip():
                        x['_id']="Not Transferred"
                    else:
                        x['_id']="Transferred"
                    if x['_id'] in claim_type_lst:
                        cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(float(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+float(x['total']))
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        # pc1=",{'transfer':{'$ne':"+str("No Transfer")+"}}"
                        pc1=""
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        # pc1=",{'transfer':{'$ne':"+str("No Transfer")+"}}"
                        pc1=""
                        cond="{'$and':["+cond+pc1+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$transfer', 'total': {'$avg': {'$convert':{'input':'$ringtime','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        if x['total']==None:
                            continue
                        x['total']=round(float(str(x['total'])),2)
                        if "no" in str(x['_id']).lower().strip(' ') and 'transfer' in str(x['_id']).lower().strip():
                            x['_id']="Not Transferred"
                        else:
                            x['_id']="Transferred"
                        if x['_id'] in claim_type_lst:
                            cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(float(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+float(x['total']))
                        else:
                            claim_type_lst.append(str(x['_id']))
                            cliam_type_cnt_lst.append(str(x['total']))
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        for li in range(0,len(cliam_type_cnt_lst)):
            cliam_type_cnt_lst[li]=str(round(float(cliam_type_cnt_lst[li]),2))
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Calls ring Time (By Transferred)")+"'"+","
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

    return " calls_tat_ring_trnsfr function "
# print(get_calls_tat_ring_trnsfr([[],[],['2019'],[]],['141338470']))
def get_calls_tat_ring_ans(dur_lst,provider_lst):

    ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    # pc1=",{'talktime':{'$ne':"+str("0")+"}}"
                    pc1=""
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    # pc1=",{'talktime':{'$ne':"+str("0")+"}}"
                    pc1=""
                    cond="{'$and':["+cond+pc1+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)                  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$vccd_dispostion', 'total': {'$avg': {'$convert':{'input':'$ringtime','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    if x['total']==None:
                        continue
                    x['total']=round(float(str(x['total'])),2)
                    if "ringnoanswer" in str(x['_id']).lower():
                        x['_id']="Not Answered"
                    else:
                        x['_id']="Answered"
                    if x['_id'] in claim_type_lst:
                        cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(float(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+float(x['total']))
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        # pc1=",{'talktime':{'$ne':"+str("0")+"}}"
                        pc1=""
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        # pc1=",{'talktime':{'$ne':"+str("0")+"}}"
                        pc1=""
                        cond="{'$and':["+cond+pc1+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$vccd_dispostion', 'total': {'$avg': {'$convert':{'input':'$ringtime','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        if x['total']==None:
                            continue
                        x['total']=round(float(str(x['total'])),2)
                        if "ringnoanswer" in str(x['_id']).lower():
                            x['_id']="Not Answered"
                        else:
                            x['_id']="Answered"
                        if x['_id'] in claim_type_lst:
                            cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(float(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+float(x['total']))
                        else:
                            claim_type_lst.append(str(x['_id']))
                            cliam_type_cnt_lst.append(str(x['total'])) 
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        for li in range(0,len(cliam_type_cnt_lst)):
            cliam_type_cnt_lst[li]=str(round(float(cliam_type_cnt_lst[li]),2))
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Calls ring Time (By Answered)")+"'"+","
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
    
    

    return " calls_tat_ring_ans function "
# print(get_calls_tat_ring_ans([[],[],['2019'],[]],['141338470']))
def get_calls_tat_ring_lang(dur_lst,provider_lst):
    ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    cond="{'$and':["+cond+pc+"]}"
                else:
                    cond="{'$and':["+cond+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)                  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$language', 'total': {'$avg': {'$convert':{'input':'$ringtime','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:                    
                    if x['total']==None:
                        continue
                    x['total']=round(float(str(x['total'])),2)
                    if x['_id'] in claim_type_lst:
                        cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(float(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+float(x['total']))
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        cond="{'$and':["+cond+pc+"]}"
                    else:
                        cond="{'$and':["+cond+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$language', 'total': {'$avg': {'$convert':{'input':'$ringtime','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        if x['total']==None:
                            continue
                        x['total']=round(float(str(x['total'])),2)

                        if x['_id'] in claim_type_lst:
                            cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(float(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+float(x['total']))
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
            if claim_type_lst[li].strip(' ').upper()=="E":
                claim_type_lst[li]="English"
            # claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        for li in range(0,len(cliam_type_cnt_lst)):
            cliam_type_cnt_lst[li]=str(round(float(cliam_type_cnt_lst[li]),2))
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Calls ring Time (By Language)")+"'"+","
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

    return " calls_tat_ring_lang function "
# print(get_calls_tat_ring_lang([[],[],['2019'],[]],['141338470']))
def get_calls_tat_ring_BU(dur_lst,provider_lst):
    ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    cond="{'$and':["+cond+pc+"]}"
                else:
                    cond="{'$and':["+cond+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$bu', 'total': {'$avg': {'$convert':{'input':'$ringtime','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    if x['total']==None:
                        continue
                    # print(x['_id'])
                    # print(x['total'])
                    x['total']=round(float(str(x['total'])),2)
                    if x['_id'] in claim_type_lst:
                        cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(float(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+float(x['total']))
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        cond="{'$and':["+cond+pc+"]}"
                    else:
                        cond="{'$and':["+cond+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$bu', 'total': {'$avg': {'$convert':{'input':'$ringtime','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        if x['total']==None:
                            continue
                        # print(x['_id'])
                        # print(x['total'])
                        x['total']=round(float(str(x['total'])),2)
                        if x['_id'] in claim_type_lst:
                            cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(float(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+float(x['total']))
                        else:
                            claim_type_lst.append(str(x['_id']))
                            cliam_type_cnt_lst.append(str(x['total'])) 
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        for li in range(0,len(cliam_type_cnt_lst)):
            cliam_type_cnt_lst[li]=str(round(float(cliam_type_cnt_lst[li]),2))
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Calls ring Time (By BU)")+"'"+","
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

    return " calls_tat_ring_BU function "
# print(get_calls_tat_ring_BU([[],[],['2019'],[]],['141338470']))
def get_calls_tat_ring(dur_lst,provider_lst):
    print(provider_lst)

    try:
        cond=""
        n_records="0"
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name] 
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    cond="{'$and':["+cond+pc+"]}"
                else:
                    cond="{'$and':["+cond+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)                 
                pipe = [{'$match':my_dict},{'$group': {'_id':'null', 'total': {'$avg': {'$convert':{'input':'$ringtime','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=0
                for x in mydoc:
                    n_records=n_records+x['total'] 
                n_records=str(n_records) 
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        cond="{'$and':["+cond+pc+"]}"
                    else:
                        cond="{'$and':["+cond+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'null', 'total': {'$avg': {'$convert':{'input':'$ringtime','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=0
                    for x in mydoc:
                        n_records=n_records+x['total'] 
                    n_records=str(n_records)    
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        for li in range(0,len(val_lst)):
            val_lst[li]=str(round(float(val_lst[li]),2))
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Calls ring Time Trend")+"'"+","
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
# print(get_calls_tat_ring([[],[],['2019'],[]],['141338470']))

def get_calls_tat_talk_lob(dur_lst,provider_lst):
    ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    cond="{'$and':["+cond+pc+"]}"
                else:
                    cond="{'$and':["+cond+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$lob_id', 'total': {'$avg': {'$convert':{'input':'$talktime','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    if x['total']==None:
                        continue
                    # print(x['_id'])
                    # print(x['total'])
                    x['total']=round(float(str(x['total'])),2)
                    if x['_id'] in claim_type_lst:
                        cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(float(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+float(x['total']))
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        cond="{'$and':["+cond+pc+"]}"
                    else:
                        cond="{'$and':["+cond+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$lob_id', 'total': {'$avg': {'$convert':{'input':'$talktime','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        if x['total']==None:
                            continue
                        # print(x['_id'])
                        # print(x['total'])                        
                        x['total']=round(float(str(x['total'])),2)
                        if x['_id'] in claim_type_lst:
                            cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(float(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+float(x['total']))
                        else:
                            claim_type_lst.append(str(x['_id']))
                            cliam_type_cnt_lst.append(str(x['total'])) 
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        for li in range(0,len(cliam_type_cnt_lst)):
            cliam_type_cnt_lst[li]=str(round(float(cliam_type_cnt_lst[li]),2))
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Calls talk Time (By LOB)")+"'"+","
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

    return " calls_tat_talk_lob function "
# print(get_calls_tat_talk_lob([[],[],['2019'],[]],['141338470']))
def get_calls_tat_talk_prod_type(dur_lst,provider_lst):
        ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    cond="{'$and':["+cond+pc+"]}"
                else:
                    cond="{'$and':["+cond+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)                  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$producttypeverbose', 'total': {'$avg': {'$convert':{'input':'$talktime','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    if x['total']==None:
                        continue
                    try:
                        x['_id']=x['_id'].split('-')[1].strip(' ')
                    except:
                        x['_id']=x['_id'].strip(' ')
                    # print(x['_id'])
                    # print(x['total'])
                    x['total']=round(float(str(x['total'])),2)
                    if x['_id'] in claim_type_lst:
                        cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(float(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+float(x['total']))
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        cond="{'$and':["+cond+pc+"]}"
                    else:
                        cond="{'$and':["+cond+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)                      
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$producttypeverbose', 'total': {'$avg': {'$convert':{'input':'$talktime','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        if x['total']==None:
                            continue
                        # print(x['_id'])
                        # print(x['total'])
                        try:
                            x['_id']=x['_id'].split('-')[1].strip(' ')
                        except:
                            x['_id']=x['_id'].strip(' ')
                        x['total']=round(float(str(x['total'])),2)
                        if x['_id'] in claim_type_lst:
                            cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(float(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+float(x['total']))
                        else:
                            claim_type_lst.append(str(x['_id']))
                            cliam_type_cnt_lst.append(str(x['total']))
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        for li in range(0,len(cliam_type_cnt_lst)):
            cliam_type_cnt_lst[li]=str(round(float(cliam_type_cnt_lst[li]),2))
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Calls talk Time (By Product Type)")+"'"+","
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

    return " calls_tat_talk_prod_type function "
# print(get_calls_tat_talk_prod_type([[],[],['2019'],[]],['141338470']))
def get_calls_tat_talk_type(dur_lst,provider_lst):
    
    ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    cond="{'$and':["+cond+pc+"]}"
                else:
                    cond="{'$and':["+cond+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$category', 'total': {'$avg': {'$convert':{'input':'$talktime','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    if x['total']==None:
                        continue
                    # print(x['_id'])
                    # print(x['total'])
                    x['total']=round(float(str(x['total'])),2)
                    if x['_id'] in claim_type_lst:
                        cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(float(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+float(x['total']))
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        cond="{'$and':["+cond+pc+"]}"
                    else:
                        cond="{'$and':["+cond+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$category', 'total': {'$avg': {'$convert':{'input':'$talktime','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        if x['total']==None:
                            continue
                        # print(x['_id'])
                        # print(x['total'])
                        x['total']=round(float(str(x['total'])),2)
                        if x['_id'] in claim_type_lst:
                            cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(float(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+float(x['total']))
                        else:
                            claim_type_lst.append(str(x['_id']))
                            cliam_type_cnt_lst.append(str(x['total']))
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        for li in range(0,len(cliam_type_cnt_lst)):
            cliam_type_cnt_lst[li]=str(round(float(cliam_type_cnt_lst[li]),2))
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Calls talk Time (By Category)")+"'"+","
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

    return " calls_tat_talk_type function "
# print(get_calls_tat_talk_type([[],[],['2019'],[]],['141338470']))
def get_calls_tat_talk_trnsfr(dur_lst,provider_lst):

    ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=""
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    # pc1=",{'transfer':{'$ne':"+str("No Transfer")+"}}"
                    pc1=""
                    cond="{'$and':["+cond+pc1+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$transfer', 'total': {'$avg': {'$convert':{'input':'$talktime','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    if x['total']==None:
                        continue
                    x['total']=round(float(str(x['total'])),2)
                    if "no" in str(x['_id']).lower().strip(' ') and 'transfer' in str(x['_id']).lower().strip():
                        x['_id']="Not Transferred"
                    else:
                        x['_id']="Transferred"
                    if x['_id'] in claim_type_lst:
                        cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(float(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+float(x['total']))
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        # pc1=",{'transfer':{'$ne':"+str("No Transfer")+"}}"
                        pc1=""
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        # pc1=",{'transfer':{'$ne':"+str("No Transfer")+"}}"
                        pc1=""
                        cond="{'$and':["+cond+pc1+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$transfer', 'total': {'$avg': {'$convert':{'input':'$talktime','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        if x['total']==None:
                            continue
                        x['total']=round(float(str(x['total'])),2)
                        if "no" in str(x['_id']).lower().strip(' ') and 'transfer' in str(x['_id']).lower().strip():
                            x['_id']="Not Transferred"
                        else:
                            x['_id']="Transferred"
                        if x['_id'] in claim_type_lst:
                            cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(float(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+float(x['total']))
                        else:
                            claim_type_lst.append(str(x['_id']))
                            cliam_type_cnt_lst.append(str(x['total']))
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        for li in range(0,len(cliam_type_cnt_lst)):
            cliam_type_cnt_lst[li]=str(round(float(cliam_type_cnt_lst[li]),2))
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Calls talk Time (By Transferred)")+"'"+","
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

    return " calls_tat_talk_trnsfr function "
# print(get_calls_tat_talk_trnsfr([[],[],['2019'],[]],['141338470']))
def get_calls_tat_talk_ans(dur_lst,provider_lst):

    ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    # pc1=",{'talktime':{'$ne':"+str("0")+"}}"
                    pc1=""
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    # pc1=",{'talktime':{'$ne':"+str("0")+"}}"
                    pc1=""
                    cond="{'$and':["+cond+pc1+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)                  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$vccd_dispostion', 'total': {'$avg': {'$convert':{'input':'$talktime','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    if x['total']==None:
                        continue
                    x['total']=round(float(str(x['total'])),2)
                    if "talknoanswer" in str(x['_id']):
                        x['_id']="Not Answered"
                    else:
                        x['_id']="Answered"
                    if x['_id'] in claim_type_lst:
                        cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(float(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+float(x['total']))
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        # pc1=",{'talktime':{'$ne':"+str("0")+"}}"
                        pc1=""
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        # pc1=",{'talktime':{'$ne':"+str("0")+"}}"
                        pc1=""
                        cond="{'$and':["+cond+pc1+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$vccd_dispostion', 'total': {'$avg': {'$convert':{'input':'$talktime','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        if x['total']==None:
                            continue
                        x['total']=round(float(str(x['total'])),2)
                        if "talknoanswer" in str(x['_id']):
                            x['_id']="Not Answered"
                        else:
                            x['_id']="Answered"
                        if x['_id'] in claim_type_lst:
                            cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(float(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+float(x['total']))
                        else:
                            claim_type_lst.append(str(x['_id']))
                            cliam_type_cnt_lst.append(str(x['total'])) 
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        for li in range(0,len(cliam_type_cnt_lst)):
            cliam_type_cnt_lst[li]=str(round(float(cliam_type_cnt_lst[li]),2))
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Calls talk Time (By Answered)")+"'"+","
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
    
    

    return " calls_tat_talk_ans function "
# print(get_calls_tat_talk_ans([[],[],['2019'],[]],['141338470']))
def get_calls_tat_talk_lang(dur_lst,provider_lst):
    ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    cond="{'$and':["+cond+pc+"]}"
                else:
                    cond="{'$and':["+cond+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)                  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$language', 'total': {'$avg': {'$convert':{'input':'$talktime','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:                    
                    if x['total']==None:
                        continue
                    x['total']=round(float(str(x['total'])),2)
                    if x['_id'] in claim_type_lst:
                        cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(float(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+float(x['total']))
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        cond="{'$and':["+cond+pc+"]}"
                    else:
                        cond="{'$and':["+cond+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$language', 'total': {'$avg': {'$convert':{'input':'$talktime','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        if x['total']==None:
                            continue
                        x['total']=round(float(str(x['total'])),2)

                        if x['_id'] in claim_type_lst:
                            cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(float(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+float(x['total']))
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
            if claim_type_lst[li].strip(' ').upper()=="E":
                claim_type_lst[li]="English"
            # claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        for li in range(0,len(cliam_type_cnt_lst)):
            cliam_type_cnt_lst[li]=str(round(float(cliam_type_cnt_lst[li]),2))
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Calls talk Time (By Language)")+"'"+","
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

    return " calls_tat_talk_lang function "
# print(get_calls_tat_talk_lang([[],[],['2019'],[]],['141338470']))
def get_calls_tat_talk_BU(dur_lst,provider_lst):
    ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    cond="{'$and':["+cond+pc+"]}"
                else:
                    cond="{'$and':["+cond+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$bu', 'total': {'$avg': {'$convert':{'input':'$talktime','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    if x['total']==None:
                        continue
                    # print(x['_id'])
                    # print(x['total'])
                    x['total']=round(float(str(x['total'])),2)
                    if x['_id'] in claim_type_lst:
                        cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(float(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+float(x['total']))
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        cond="{'$and':["+cond+pc+"]}"
                    else:
                        cond="{'$and':["+cond+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$bu', 'total': {'$avg': {'$convert':{'input':'$talktime','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        if x['total']==None:
                            continue
                        # print(x['_id'])
                        # print(x['total'])
                        x['total']=round(float(str(x['total'])),2)
                        if x['_id'] in claim_type_lst:
                            cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(float(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+float(x['total']))
                        else:
                            claim_type_lst.append(str(x['_id']))
                            cliam_type_cnt_lst.append(str(x['total'])) 
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        for li in range(0,len(cliam_type_cnt_lst)):
            cliam_type_cnt_lst[li]=str(round(float(cliam_type_cnt_lst[li]),2))
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Calls talk Time (By BU)")+"'"+","
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

    return " calls_tat_talk_BU function "
# print(get_calls_tat_talk_BU([[],[],['2019'],[]],['141338470']))
def get_calls_tat_talk(dur_lst,provider_lst):
    print(provider_lst)

    try:
        cond=""
        n_records="0"
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name] 
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    cond="{'$and':["+cond+pc+"]}"
                else:
                    cond="{'$and':["+cond+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)                 
                pipe = [{'$match':my_dict},{'$group': {'_id':'null', 'total': {'$avg': {'$convert':{'input':'$talktime','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=0
                for x in mydoc:
                    n_records=n_records+x['total'] 
                n_records=str(n_records) 
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        cond="{'$and':["+cond+pc+"]}"
                    else:
                        cond="{'$and':["+cond+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'null', 'total': {'$avg': {'$convert':{'input':'$talktime','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=0
                    for x in mydoc:
                        n_records=n_records+x['total'] 
                    n_records=str(n_records)    
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        for li in range(0,len(val_lst)):
            val_lst[li]=str(round(float(val_lst[li]),2))
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Calls talk Time Trend")+"'"+","
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
# print(get_calls_tat_talk([[],[],['2019'],[]],['141338470']))

def get_calls_tat_lob(dur_lst,provider_lst):
    ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    cond="{'$and':["+cond+pc+"]}"
                else:
                    cond="{'$and':["+cond+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$lob_id', 'total': {'$avg': {'$convert':{'input':'$total_time','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    if x['total']==None:
                        continue
                    # print(x['_id'])
                    # print(x['total'])
                    x['total']=round(float(str(x['total'])),2)
                    if x['_id'] in claim_type_lst:
                        cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(float(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+float(x['total']))
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        cond="{'$and':["+cond+pc+"]}"
                    else:
                        cond="{'$and':["+cond+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$lob_id', 'total': {'$avg': {'$convert':{'input':'$total_time','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        if x['total']==None:
                            continue
                        # print(x['_id'])
                        # print(x['total'])                        
                        x['total']=round(float(str(x['total'])),2)
                        if x['_id'] in claim_type_lst:
                            cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(float(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+float(x['total']))
                        else:
                            claim_type_lst.append(str(x['_id']))
                            cliam_type_cnt_lst.append(str(x['total'])) 
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        for li in range(0,len(cliam_type_cnt_lst)):
            cliam_type_cnt_lst[li]=str(round(float(cliam_type_cnt_lst[li]),2))
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Calls Handling Time (By LOB)")+"'"+","
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

    return " calls_tat_total__lob function "
# print(get_calls_tat_lob([[],[],['2019'],[]],['141338470']))
def get_calls_tat_prod_type(dur_lst,provider_lst):
        ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    cond="{'$and':["+cond+pc+"]}"
                else:
                    cond="{'$and':["+cond+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)                  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$producttypeverbose', 'total': {'$avg': {'$convert':{'input':'$total_time','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    if x['total']==None:
                        continue
                    try:
                        x['_id']=x['_id'].split('-')[1].strip(' ')
                    except:
                        x['_id']=x['_id'].strip(' ')
                    # print(x['_id'])
                    # print(x['total'])
                    x['total']=round(float(str(x['total'])),2)
                    if x['_id'] in claim_type_lst:
                        cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(float(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+float(x['total']))
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        cond="{'$and':["+cond+pc+"]}"
                    else:
                        cond="{'$and':["+cond+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)                      
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$producttypeverbose', 'total': {'$avg': {'$convert':{'input':'$total_time','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        if x['total']==None:
                            continue
                        # print(x['_id'])
                        # print(x['total'])
                        try:
                            x['_id']=x['_id'].split('-')[1].strip(' ')
                        except:
                            x['_id']=x['_id'].strip(' ')
                        x['total']=round(float(str(x['total'])),2)
                        if x['_id'] in claim_type_lst:
                            cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(float(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+float(x['total']))
                        else:
                            claim_type_lst.append(str(x['_id']))
                            cliam_type_cnt_lst.append(str(x['total']))
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        for li in range(0,len(cliam_type_cnt_lst)):
            cliam_type_cnt_lst[li]=str(round(float(cliam_type_cnt_lst[li]),2))
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Calls Handling Time (By Product Type)")+"'"+","
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

    return " calls_tat_total__prod_type function "
# print(get_calls_tat_prod_type([[],[],['2019'],[]],['141338470']))
def get_calls_tat_type(dur_lst,provider_lst):
    
    ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    cond="{'$and':["+cond+pc+"]}"
                else:
                    cond="{'$and':["+cond+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$category', 'total': {'$avg': {'$convert':{'input':'$total_time','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    if x['total']==None:
                        continue
                    # print(x['_id'])
                    # print(x['total'])
                    x['total']=round(float(str(x['total'])),2)
                    if x['_id'] in claim_type_lst:
                        cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(float(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+float(x['total']))
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        cond="{'$and':["+cond+pc+"]}"
                    else:
                        cond="{'$and':["+cond+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$category', 'total': {'$avg': {'$convert':{'input':'$total_time','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        if x['total']==None:
                            continue
                        # print(x['_id'])
                        # print(x['total'])
                        x['total']=round(float(str(x['total'])),2)
                        if x['_id'] in claim_type_lst:
                            cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(float(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+float(x['total']))
                        else:
                            claim_type_lst.append(str(x['_id']))
                            cliam_type_cnt_lst.append(str(x['total']))
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        for li in range(0,len(cliam_type_cnt_lst)):
            cliam_type_cnt_lst[li]=str(round(float(cliam_type_cnt_lst[li]),2))
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Calls Handling Time (By Category)")+"'"+","
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

    return " calls_tat_total__type function "
# print(get_calls_tat_type([[],[],['2019'],[]],['141338470']))
def get_calls_tat_trnsfr(dur_lst,provider_lst):

    ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=""
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    # pc1=",{'transfer':{'$ne':"+str("No Transfer")+"}}"
                    pc1=""
                    cond="{'$and':["+cond+pc1+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$transfer', 'total': {'$avg': {'$convert':{'input':'$total_time','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    if x['total']==None:
                        continue
                    x['total']=round(float(str(x['total'])),2)
                    if "no" in str(x['_id']).lower().strip(' ') and 'transfer' in str(x['_id']).lower().strip():
                        x['_id']="Not Transferred"
                    else:
                        x['_id']="Transferred"
                    if x['_id'] in claim_type_lst:
                        cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(float(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+float(x['total']))
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        # pc1=",{'transfer':{'$ne':"+str("No Transfer")+"}}"
                        pc1=""
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        # pc1=",{'transfer':{'$ne':"+str("No Transfer")+"}}"
                        pc1=""
                        cond="{'$and':["+cond+pc1+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$transfer', 'total': {'$avg': {'$convert':{'input':'$total_time','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        if x['total']==None:
                            continue
                        x['total']=round(float(str(x['total'])),2)
                        if "no" in str(x['_id']).lower().strip(' ') and 'transfer' in str(x['_id']).lower().strip():
                            x['_id']="Not Transferred"
                        else:
                            x['_id']="Transferred"
                        if x['_id'] in claim_type_lst:
                            cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(float(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+float(x['total']))
                        else:
                            claim_type_lst.append(str(x['_id']))
                            cliam_type_cnt_lst.append(str(x['total']))
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        for li in range(0,len(cliam_type_cnt_lst)):
            cliam_type_cnt_lst[li]=str(round(float(cliam_type_cnt_lst[li]),2))
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Calls Handling Time (By Transferred)")+"'"+","
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

    return " calls_tat_total__trnsfr function "
# print(get_calls_tat_trnsfr([[],[],['2019'],[]],['141338470']))
def get_calls_tat_ans(dur_lst,provider_lst):

    ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    # pc1=",{'total_time':{'$ne':"+str("0")+"}}"
                    pc1=""
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    # pc1=",{'total_time':{'$ne':"+str("0")+"}}"
                    pc1=""
                    cond="{'$and':["+cond+pc1+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)                  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$vccd_dispostion', 'total': {'$avg': {'$convert':{'input':'$total_time','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    if x['total']==None:
                        continue
                    x['total']=round(float(str(x['total'])),2)
                    if "total_noanswer" in str(x['_id']):
                        x['_id']="Not Answered"
                    else:
                        x['_id']="Answered"
                    if x['_id'] in claim_type_lst:
                        cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(float(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+float(x['total']))
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        # pc1=",{'total_time':{'$ne':"+str("0")+"}}"
                        pc1=""
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        # pc1=",{'total_time':{'$ne':"+str("0")+"}}"
                        pc1=""
                        cond="{'$and':["+cond+pc1+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$vccd_dispostion', 'total': {'$avg': {'$convert':{'input':'$total_time','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        if x['total']==None:
                            continue
                        x['total']=round(float(str(x['total'])),2)
                        if "total_noanswer" in str(x['_id']):
                            x['_id']="Not Answered"
                        else:
                            x['_id']="Answered"
                        if x['_id'] in claim_type_lst:
                            cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(float(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+float(x['total']))
                        else:
                            claim_type_lst.append(str(x['_id']))
                            cliam_type_cnt_lst.append(str(x['total'])) 
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        for li in range(0,len(cliam_type_cnt_lst)):
            cliam_type_cnt_lst[li]=str(round(float(cliam_type_cnt_lst[li]),2))
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Calls Handling Time (By Answered)")+"'"+","
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
    
    

    return " calls_tat_total__ans function "
# print(get_calls_tat_ans([[],[],['2019'],[]],['141338470']))
def get_calls_tat_lang(dur_lst,provider_lst):
    ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    cond="{'$and':["+cond+pc+"]}"
                else:
                    cond="{'$and':["+cond+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)                  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$language', 'total': {'$avg': {'$convert':{'input':'$total_time','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:                    
                    if x['total']==None:
                        continue
                    x['total']=round(float(str(x['total'])),2)
                    if x['_id'] in claim_type_lst:
                        cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(float(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+float(x['total']))
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        cond="{'$and':["+cond+pc+"]}"
                    else:
                        cond="{'$and':["+cond+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$language', 'total': {'$avg': {'$convert':{'input':'$total_time','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        if x['total']==None:
                            continue
                        x['total']=round(float(str(x['total'])),2)

                        if x['_id'] in claim_type_lst:
                            cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(float(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+float(x['total']))
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
            if claim_type_lst[li].strip(' ').upper()=="E":
                claim_type_lst[li]="English"
            # claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        for li in range(0,len(cliam_type_cnt_lst)):
            cliam_type_cnt_lst[li]=str(round(float(cliam_type_cnt_lst[li]),2))
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Calls Handling Time (By Language)")+"'"+","
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

    return " calls_tat_total__lang function "
# print(get_calls_tat_lang([[],[],['2019'],[]],['141338470']))
def get_calls_tat_BU(dur_lst,provider_lst):
    ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    cond="{'$and':["+cond+pc+"]}"
                else:
                    cond="{'$and':["+cond+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$bu', 'total': {'$avg': {'$convert':{'input':'$total_time','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    if x['total']==None:
                        continue
                    # print(x['_id'])
                    # print(x['total'])
                    x['total']=round(float(str(x['total'])),2)
                    if x['_id'] in claim_type_lst:
                        cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(float(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+float(x['total']))
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        cond="{'$and':["+cond+pc+"]}"
                    else:
                        cond="{'$and':["+cond+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$bu', 'total': {'$avg': {'$convert':{'input':'$total_time','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        if x['total']==None:
                            continue
                        # print(x['_id'])
                        # print(x['total'])
                        x['total']=round(float(str(x['total'])),2)
                        if x['_id'] in claim_type_lst:
                            cliam_type_cnt_lst[claim_type_lst.index(x['_id'])]=str(float(cliam_type_cnt_lst[claim_type_lst.index(x['_id'])])+float(x['total']))
                        else:
                            claim_type_lst.append(str(x['_id']))
                            cliam_type_cnt_lst.append(str(x['total'])) 
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        for li in range(0,len(cliam_type_cnt_lst)):
            cliam_type_cnt_lst[li]=str(round(float(cliam_type_cnt_lst[li]),2))
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Calls Handling Time (By BU)")+"'"+","
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

    return " calls_tat_total__BU function "
# print(get_calls_tat_BU([[],[],['2019'],[]],['141338470']))
def get_calls_tat(dur_lst,provider_lst):
    print(provider_lst)

    try:
        cond=""
        n_records="0"
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name] 
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    cond="{'$and':["+cond+pc+"]}"
                else:
                    cond="{'$and':["+cond+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)                 
                pipe = [{'$match':my_dict},{'$group': {'_id':'null', 'total': {'$avg': {'$convert':{'input':'$total_time','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=0
                for x in mydoc:
                    n_records=n_records+x['total'] 
                n_records=str(n_records) 
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        cond="{'$and':["+cond+pc+"]}"
                    else:
                        cond="{'$and':["+cond+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'null', 'total': {'$avg': {'$convert':{'input':'$total_time','to':'double','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=0
                    for x in mydoc:
                        n_records=n_records+x['total'] 
                    n_records=str(n_records)    
                    print(str(dl1))
                    key_val=mon_name(dl1)+"-"+str(dl[-2:])
                    val_val=n_records                
                    key_lst.append(key_val)
                    val_lst.append(val_val)
                    cond=""
        for li in range(0,len(val_lst)):
            val_lst[li]=str(round(float(val_lst[li]),2))
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Calls tat Trend")+"'"+","
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
# print(get_calls_tat([[],[],['2019'],[]],['141338470']))


def get_calls_cnt_unans_lob():

    return "Could not display trend for Unanswered Calls"

def get_calls_cnt_unans_prod_type():

    return "Could not display trend for Unanswered Calls"

def get_calls_cnt_unans_type():

    return "Could not display trend for Unanswered Calls"

def get_calls_cnt_unans_trnsfr():

    return "Could not display trend for Unanswered Calls"

def get_calls_cnt_unans_ans():

    return "Could not display trend for Unanswered Calls"

def get_calls_cnt_unans_lang():

    return "Could not display trend for Unanswered Calls"

def get_calls_cnt_unans_bu():

    return "Could not display trend for Unanswered Calls"

def get_calls_cnt_unans(dur_lst,provider_lst):

    print(provider_lst)

    try:
        cond=""
        n_records="0"
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name] 
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'vccd_dispostion':{'$eq':'19- RingNoAnswer'}}"                    
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'vccd_dispostion':{'$eq':'19- RingNoAnswer'}}"
                    cond="{'$and':["+cond+pc1+"]}"
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'vccd_dispostion':{'$eq':'19- RingNoAnswer'}}"
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'vccd_dispostion':{'$eq':'19- RingNoAnswer'}}"
                        cond="{'$and':["+cond+pc1+"]}"
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
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Unanswered Calls (Volume)")+"'"+","
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

    return " calls_cnt_unans function "    
# print(get_calls_cnt_unans([[],[],['2019'],[]],['141338470']))
def get_calls_cnt_ans_lob(dur_lst,provider_lst):

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'vccd_dispostion':{'$ne':'19- RingNoAnswer'}}"  
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'vccd_dispostion':{'$ne':'19- RingNoAnswer'}}"  
                    cond="{'$and':["+cond+pc1+"]}"
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'vccd_dispostion':{'$ne':'19- RingNoAnswer'}}"  
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'vccd_dispostion':{'$ne':'19- RingNoAnswer'}}"  
                        cond="{'$and':["+cond+pc1+"]}"
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
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Answered Calls Volume (By LOB)")+"'"+","
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

    return " calls_cnt_lob function "
# print(get_calls_cnt_ans_lob([[],[],['2019'],[]],['141338470']))
def get_calls_cnt_ans_prod_type(dur_lst,provider_lst):

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'vccd_dispostion':{'$ne':'19- RingNoAnswer'}}"  
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'vccd_dispostion':{'$ne':'19- RingNoAnswer'}}"  
                    cond="{'$and':["+cond+pc1+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$producttypeverbose', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    try:
                        x['_id']=x['_id'].split('-')[1].strip(' ')
                    except:
                        x['_id']=x['_id'].strip(' ')

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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'vccd_dispostion':{'$ne':'19- RingNoAnswer'}}"  
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'vccd_dispostion':{'$ne':'19- RingNoAnswer'}}"  
                        cond="{'$and':["+cond+pc1+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$producttypeverbose', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        try:
                            x['_id']=x['_id'].split('-')[1].strip(' ')
                        except:
                            x['_id']=x['_id'].strip(' ')

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
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Answered Calls Volume (By Product Type)")+"'"+","
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

    return " calls_cnt_prod_type function "
# print(get_calls_cnt_ans_prod_type([[],[],['2019'],[]],['141338470']))
def get_calls_cnt_ans_type(dur_lst,provider_lst):

    ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'vccd_dispostion':{'$ne':'19- RingNoAnswer'}}"  
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'vccd_dispostion':{'$ne':'19- RingNoAnswer'}}"  
                    cond="{'$and':["+cond+pc1+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$category', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'vccd_dispostion':{'$ne':'19- RingNoAnswer'}}"  
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'vccd_dispostion':{'$ne':'19- RingNoAnswer'}}"  
                        cond="{'$and':["+cond+pc1+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$category', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
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
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Answered Calls Volume (By Category)")+"'"+","
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

    return " calls_cnt_type function "
# print(get_calls_cnt_ans_type([[],[],['2019'],[]],['141338470']))
def get_calls_cnt_ans_trnsfr(dur_lst,provider_lst):

    ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'vccd_dispostion':{'$ne':'19- RingNoAnswer'}}"  
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'vccd_dispostion':{'$ne':'19- RingNoAnswer'}}"  
                    cond="{'$and':["+cond+pc1+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$transfer', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    if "no" in str(x['_id']).lower().strip(' ') and 'transfer' in str(x['_id']).lower().strip():
                        x['_id']="Not Transferred"
                    else:
                        x['_id']="Transferred"
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'vccd_dispostion':{'$ne':'19- RingNoAnswer'}}"  
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'vccd_dispostion':{'$ne':'19- RingNoAnswer'}}"  
                        cond="{'$and':["+cond+pc1+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$transfer', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        if "no" in str(x['_id']).lower().strip(' ') and 'transfer' in str(x['_id']).lower().strip():
                            x['_id']="Not Transferred"
                        else:
                            x['_id']="Transferred"
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
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Answered Calls Volume (By Transfer)")+"'"+","
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
    

    return " calls_cnt_trnsfr function "
# print(get_calls_cnt_ans_trnsfr([[],[],['2019'],[]],['141338470']))
def get_calls_cnt_ans_lang(dur_lst,provider_lst):

    ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'vccd_dispostion':{'$ne':'19- RingNoAnswer'}}"  
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'vccd_dispostion':{'$ne':'19- RingNoAnswer'}}"  
                    cond="{'$and':["+cond+pc1+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$language', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    if str(x['_id']).strip().lower()=="e":
                        x['_id']="English"
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'vccd_dispostion':{'$ne':'19- RingNoAnswer'}}"  
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'vccd_dispostion':{'$ne':'19- RingNoAnswer'}}"  
                        cond="{'$and':["+cond+pc1+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$language', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        if str(x['_id']).strip().lower()=="e":
                            x['_id']="English"
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
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Answered Calls Volume (By Language)")+"'"+","
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

    return " calls_cnt_lang function "
# print(get_calls_cnt_ans_lang([[],[],['2019'],[]],['141338470']))
def get_calls_cnt_ans_BU(dur_lst,provider_lst):

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'vccd_dispostion':{'$ne':'19- RingNoAnswer'}}"  
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'vccd_dispostion':{'$ne':'19- RingNoAnswer'}}"  
                    cond="{'$and':["+cond+pc1+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$bu', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'vccd_dispostion':{'$ne':'19- RingNoAnswer'}}"  
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'vccd_dispostion':{'$ne':'19- RingNoAnswer'}}"  
                        cond="{'$and':["+cond+pc1+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$bu', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
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
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Answered Calls Volume (By BU)")+"'"+","
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

    return " calls_cnt_BU function "
# print(get_calls_cnt_ans_BU([[],[],['2019'],[]],['141338470']))
def get_calls_cnt_ans(dur_lst,provider_lst):

    print(provider_lst)

    try:
        cond=""
        n_records="0"
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name] 
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'vccd_dispostion':{'$ne':'19- RingNoAnswer'}}"  
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'vccd_dispostion':{'$ne':'19- RingNoAnswer'}}"  
                    cond="{'$and':["+cond+pc1+"]}"
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'vccd_dispostion':{'$ne':'19- RingNoAnswer'}}"  
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'vccd_dispostion':{'$ne':'19- RingNoAnswer'}}"  
                        cond="{'$and':["+cond+pc1+"]}"
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
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Answered Calls Trend (Volume)")+"'"+","
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
    return " calls_cnt function "
# print(get_calls_cnt_ans([[],[],['2019'],[]],['141338470']))

def get_calls_cnt_trnsfr_lob(dur_lst,provider_lst):

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'transfer':{'$ne':'No Transfer'}}"  
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'transfer':{'$ne':'No Transfer'}}"   
                    cond="{'$and':["+cond+pc1+"]}"
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'transfer':{'$ne':'No Transfer'}}"    
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'transfer':{'$ne':'No Transfer'}}"  
                        cond="{'$and':["+cond+pc1+"]}"
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
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Transferred Calls Volume (By LOB)")+"'"+","
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

    return " calls_cnt_lob function "
# print(get_calls_cnt_trnsfr_lob([[],[],['2019'],[]],['141338470']))
def get_calls_cnt_trnsfr_prod_type(dur_lst,provider_lst):

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'transfer':{'$ne':'No Transfer'}}"   
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'transfer':{'$ne':'No Transfer'}}"  
                    cond="{'$and':["+cond+pc1+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$producttypeverbose', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    try:
                        x['_id']=x['_id'].split('-')[1].strip(' ')
                    except:
                        x['_id']=x['_id'].strip(' ')

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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'transfer':{'$ne':'No Transfer'}}"   
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'transfer':{'$ne':'No Transfer'}}"  
                        cond="{'$and':["+cond+pc1+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$producttypeverbose', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        try:
                            x['_id']=x['_id'].split('-')[1].strip(' ')
                        except:
                            x['_id']=x['_id'].strip(' ')

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
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Transferred Calls Volume (By Product Type)")+"'"+","
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

    return " calls_cnt_prod_type function "
# print(get_calls_cnt_trnsfr_prod_type([[],[],['2019'],[]],['141338470']))
def get_calls_cnt_trnsfr_type(dur_lst,provider_lst):

    ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'transfer':{'$ne':'No Transfer'}}"  
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'transfer':{'$ne':'No Transfer'}}"  
                    cond="{'$and':["+cond+pc1+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$category', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'transfer':{'$ne':'No Transfer'}}"  
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'transfer':{'$ne':'No Transfer'}}"  
                        cond="{'$and':["+cond+pc1+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$category', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
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
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Transferred Calls Volume (By Category)")+"'"+","
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

    return " calls_cnt_type function "
# print(get_calls_cnt_trnsfr_type([[],[],['2019'],[]],['141338470']))
def get_calls_cnt_trnsfr_lang(dur_lst,provider_lst):

    ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'transfer':{'$ne':'No Transfer'}}"  
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'transfer':{'$ne':'No Transfer'}}"  
                    cond="{'$and':["+cond+pc1+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$language', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    if str(x['_id']).strip().lower()=="e":
                        x['_id']="English"
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'transfer':{'$ne':'No Transfer'}}"   
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'transfer':{'$ne':'No Transfer'}}"  
                        cond="{'$and':["+cond+pc1+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$language', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        if str(x['_id']).strip().lower()=="e":
                            x['_id']="English"
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
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Transferred Calls Volume (By Language)")+"'"+","
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

    return " calls_cnt_lang function "
# print(get_calls_cnt_trnsfr_lang([[],[],['2019'],[]],['141338470']))
def get_calls_cnt_trnsfr_BU(dur_lst,provider_lst):

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'transfer':{'$ne':'No Transfer'}}"  
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'transfer':{'$ne':'No Transfer'}}"  
                    cond="{'$and':["+cond+pc1+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$bu', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'transfer':{'$ne':'No Transfer'}}"   
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'transfer':{'$ne':'No Transfer'}}"  
                        cond="{'$and':["+cond+pc1+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$bu', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
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
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Transferred Calls Volume (By BU)")+"'"+","
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

    return " calls_cnt_BU function "
# print(get_calls_cnt_trnsfr_BU([[],[],['2019'],[]],['141338470']))
def get_calls_cnt_trnsfr(dur_lst,provider_lst):

    print(provider_lst)

    try:
        cond=""
        n_records="0"
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name] 
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    pc1=",{'transfer':{'$ne':'No Transfer'}}"  
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'transfer':{'$ne':'No Transfer'}}"  
                    cond="{'$and':["+cond+pc1+"]}"
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'transfer':{'$ne':'No Transfer'}}"  
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'transfer':{'$ne':'No Transfer'}}"  
                        cond="{'$and':["+cond+pc1+"]}"
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
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Transferred Calls Trend (Volume)")+"'"+","
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
    return " calls_cnt function "
# print(get_calls_cnt_trnsfr([[],[],['2019'],[]],['141338470']))

def get_calls_trnsfr_rt_lob(dur_lst,provider_lst):
    rcvd_res=get_calls_cnt_lob(dur_lst,provider_lst)
    rcvd_paid_res=get_calls_cnt_trnsfr_lob(dur_lst,provider_lst)
    r_from_dt=rcvd_res["From"]
    print(str(r_from_dt))
    r_end_dt=rcvd_res["End"]
    print(str(r_end_dt))
    key_lst_rcvd=list(rcvd_res["Header"])
    print(str(key_lst_rcvd))
    key_lst_rcvd_paid=list(rcvd_paid_res["Header"])
    print(str(key_lst_rcvd_paid))
    val_lst_rcvd=list(rcvd_res["Value"])
    print(str(val_lst_rcvd))
    val_lst_rcvd_paid=list(rcvd_paid_res["Value"])
    print(str(val_lst_rcvd_paid))
    val_lst_rate=list()
    for i in range(0,len(key_lst_rcvd)):
        try:
            ti=key_lst_rcvd_paid.index(key_lst_rcvd[i])
            temp=int(val_lst_rcvd_paid[ti])/int(val_lst_rcvd[i])*100
            temp=round(temp,2)
        except:
            temp=0
        val_lst_rate.append(temp)
    kv="{"
    kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
    kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
    kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Calls Transfer Rate (By LOB)")+"'"+","
    kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Bar")+"'"+","
    kv=kv+"'"+str("Header")+"'"+":"+""+str(key_lst_rcvd)+""+","
    kv=kv+"'"+str("Value")+"'"+":"+""+str(val_lst_rate)+""+","
    kv=kv[0:len(kv)-1]+"}"
    print(kv)
    kv=ast.literal_eval(kv)
    return kv    
    
    return " calls_trnsfr_rt_lob function "
# print(get_calls_trnsfr_rt_lob([[],[],['2019'],[]],['141338470']))
def get_calls_trnsfr_rt_prod_type(dur_lst,provider_lst):

    rcvd_res=get_calls_cnt_prod_type(dur_lst,provider_lst)
    rcvd_paid_res=get_calls_cnt_trnsfr_prod_type(dur_lst,provider_lst)
    r_from_dt=rcvd_res["From"]
    print(str(r_from_dt))
    r_end_dt=rcvd_res["End"]
    print(str(r_end_dt))
    key_lst_rcvd=list(rcvd_res["Header"])
    print(str(key_lst_rcvd))
    key_lst_rcvd_paid=list(rcvd_paid_res["Header"])
    print(str(key_lst_rcvd_paid))
    val_lst_rcvd=list(rcvd_res["Value"])
    print(str(val_lst_rcvd))
    val_lst_rcvd_paid=list(rcvd_paid_res["Value"])
    print(str(val_lst_rcvd_paid))
    val_lst_rate=list()
    for i in range(0,len(key_lst_rcvd)):
        try:
            ti=key_lst_rcvd_paid.index(key_lst_rcvd[i])
            temp=int(val_lst_rcvd_paid[ti])/int(val_lst_rcvd[i])*100
            temp=round(temp,2)
        except:
            temp=0
        val_lst_rate.append(temp)
    kv="{"
    kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
    kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
    kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Calls Transfer Rate (By Product Type)")+"'"+","
    kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Bar")+"'"+","
    kv=kv+"'"+str("Header")+"'"+":"+""+str(key_lst_rcvd)+""+","
    kv=kv+"'"+str("Value")+"'"+":"+""+str(val_lst_rate)+""+","
    kv=kv[0:len(kv)-1]+"}"
    print(kv)
    kv=ast.literal_eval(kv)
    return kv    
    
    return " calls_trnsfr_rt_prod_type function "
# print(get_calls_trnsfr_rt_prod_type([[],[],['2019'],[]],['141338470']))
def get_calls_trnsfr_rt_type(dur_lst,provider_lst):
    rcvd_res=get_calls_cnt_type(dur_lst,provider_lst)
    rcvd_paid_res=get_calls_cnt_trnsfr_type(dur_lst,provider_lst)
    r_from_dt=rcvd_res["From"]
    print(str(r_from_dt))
    r_end_dt=rcvd_res["End"]
    print(str(r_end_dt))
    key_lst_rcvd=list(rcvd_res["Header"])
    print(str(key_lst_rcvd))
    key_lst_rcvd_paid=list(rcvd_paid_res["Header"])
    print(str(key_lst_rcvd_paid))
    val_lst_rcvd=list(rcvd_res["Value"])
    print(str(val_lst_rcvd))
    val_lst_rcvd_paid=list(rcvd_paid_res["Value"])
    print(str(val_lst_rcvd_paid))
    val_lst_rate=list()
    for i in range(0,len(key_lst_rcvd)):
        try:
            ti=key_lst_rcvd_paid.index(key_lst_rcvd[i])
            temp=int(val_lst_rcvd_paid[ti])/int(val_lst_rcvd[i])*100
            temp=round(temp,2)
        except:
            temp=0
        val_lst_rate.append(temp)
    kv="{"
    kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
    kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
    kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Calls Transfer Rate (By Category)")+"'"+","
    kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Bar")+"'"+","
    kv=kv+"'"+str("Header")+"'"+":"+""+str(key_lst_rcvd)+""+","
    kv=kv+"'"+str("Value")+"'"+":"+""+str(val_lst_rate)+""+","
    kv=kv[0:len(kv)-1]+"}"
    print(kv)
    kv=ast.literal_eval(kv)
    return kv    
    
    return " calls_trnsfr_rt_type function "
# print(get_calls_trnsfr_rt_type([[],[],['2019'],[]],['141338470']))
def get_calls_trnsfr_rt_lang(dur_lst,provider_lst):

    rcvd_res=get_calls_cnt_lang(dur_lst,provider_lst)
    rcvd_paid_res=get_calls_cnt_trnsfr_lang(dur_lst,provider_lst)
    r_from_dt=rcvd_res["From"]
    print(str(r_from_dt))
    r_end_dt=rcvd_res["End"]
    print(str(r_end_dt))
    key_lst_rcvd=list(rcvd_res["Header"])
    print(str(key_lst_rcvd))
    key_lst_rcvd_paid=list(rcvd_paid_res["Header"])
    print(str(key_lst_rcvd_paid))
    val_lst_rcvd=list(rcvd_res["Value"])
    print(str(val_lst_rcvd))
    val_lst_rcvd_paid=list(rcvd_paid_res["Value"])
    print(str(val_lst_rcvd_paid))
    val_lst_rate=list()
    for i in range(0,len(key_lst_rcvd)):
        try:
            ti=key_lst_rcvd_paid.index(key_lst_rcvd[i])
            temp=int(val_lst_rcvd_paid[ti])/int(val_lst_rcvd[i])*100
            temp=round(temp,2)
        except:
            temp=0
        val_lst_rate.append(temp)
    kv="{"
    kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
    kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
    kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Calls Transfer Rate (By Language)")+"'"+","
    kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Bar")+"'"+","
    kv=kv+"'"+str("Header")+"'"+":"+""+str(key_lst_rcvd)+""+","
    kv=kv+"'"+str("Value")+"'"+":"+""+str(val_lst_rate)+""+","
    kv=kv[0:len(kv)-1]+"}"
    print(kv)
    kv=ast.literal_eval(kv)
    return kv    
    return " calls_trnsfr_rt_lang function "
# print(get_calls_trnsfr_rt_lang([[],[],['2019'],[]],['141338470']))
def get_calls_trnsfr_rt(dur_lst,provider_lst):
    print("get_calls_trnsfr_rt")
    rcvd_res=get_calls_cnt(dur_lst,provider_lst)
    rcvd_paid_res=get_calls_cnt_trnsfr(dur_lst,provider_lst)
    r_from_dt=rcvd_res["From"]
    print(str(r_from_dt))
    r_end_dt=rcvd_res["End"]
    print(str(r_end_dt))
    key_lst=list(rcvd_paid_res["Header"])
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
    kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Calls Trend (Transfer Rate)")+"'"+","
    kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Line")+"'"+","
    kv=kv+"'"+str("Header")+"'"+":"+""+str(key_lst)+""+","
    kv=kv+"'"+str("Value")+"'"+":"+""+str(val_lst_rate)+""+","
    kv=kv[0:len(kv)-1]+"}"
    print(kv)
    kv=ast.literal_eval(kv)
    return kv
    return " calls_trnsfr_rt function "
# print(get_calls_trnsfr_rt([[],[],['2019'],[]],['141338470']))
def get_calls_trnsfr_rt_BU(dur_lst,provider_lst):
    print("get_calls_trnsfr_rt_BU")
    rcvd_res=get_calls_cnt_lob(dur_lst,provider_lst)
    rcvd_paid_res=get_calls_cnt_trnsfr_lob(dur_lst,provider_lst)
    r_from_dt=rcvd_res["From"]
    print(str(r_from_dt))
    r_end_dt=rcvd_res["End"]
    print(str(r_end_dt))
    key_lst_rcvd=list(rcvd_res["Header"])
    print(str(key_lst_rcvd))
    key_lst_rcvd_paid=list(rcvd_paid_res["Header"])
    print(str(key_lst_rcvd_paid))
    val_lst_rcvd=list(rcvd_res["Value"])
    print(str(val_lst_rcvd))
    val_lst_rcvd_paid=list(rcvd_paid_res["Value"])
    print(str(val_lst_rcvd_paid))
    val_lst_rate=list()
    for i in range(0,len(key_lst_rcvd)):
        try:
            ti=key_lst_rcvd_paid.index(key_lst_rcvd[i])
            temp=int(val_lst_rcvd_paid[ti])/int(val_lst_rcvd[i])*100
            temp=round(temp,2)
        except:
            temp=0
        val_lst_rate.append(temp)
    kv="{"
    kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
    kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
    kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Calls Transfer Rate (By BU)")+"'"+","
    kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Bar")+"'"+","
    kv=kv+"'"+str("Header")+"'"+":"+""+str(key_lst_rcvd)+""+","
    kv=kv+"'"+str("Value")+"'"+":"+""+str(val_lst_rate)+""+","
    kv=kv[0:len(kv)-1]+"}"
    print(kv)
    kv=ast.literal_eval(kv)
    return kv    
    
    return " calls_trnsfr_rt_lob function "
# print(get_calls_trnsfr_rt_BU([[],[],['2019'],[]],['141338470']))

# print(get_calls_cnt_appeal([[],[],['2019'],[]],['141338470']))
def get_top_calls_tin(dur_lst,n):

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                cond="{'$and':["+cond+"]}"
                # if len(provider_lst) > 0:
                #     pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                #     # pc1=",{'category':{'$eq':'Appeal'}}"
                #     pc1=""
                #     cond="{'$and':["+cond+pc+pc1+"]}"
                # else:
                #     pc1=",{'category':{'$eq':'Appeal'}}"
                #     pc1=""
                #     cond="{'$and':["+cond+pc1+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$tin', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    cond="{'$and':["+cond+"]}"
                    # cond="{'$and':["+cond+"]}"
                    # if len(provider_lst) > 0:
                    #     pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    #     pc1=",{'category':{'$eq':'Appeal'}}"
                    #     pc1=""
                    #     cond="{'$and':["+cond+pc+pc1+"]}"
                    # else:
                    #     pc1=",{'category':{'$eq':'Appeal'}}"
                    #     pc1=""
                    #     cond="{'$and':["+cond+pc1+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$tin', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
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
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        if n > len(claim_type_lst):
            n=5
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Top Calls (By TIN)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Bar")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(claim_type_lst[0:n])+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(cliam_type_cnt_lst[0:n])+""+","
        kv=kv[0:len(kv)-1]+"}"
        print(kv)
        kv=ast.literal_eval(kv)
        return kv

    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"

    return " calls_cnt_lob function "
# print(get_top_calls_tin([[],[],['2019'],[]],10))
def get_top_calls_bu(dur_lst,n,provider_lst):

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                # cond="{'$and':["+cond+"]}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    # pc1=",{'category':{'$eq':'Appeal'}}"
                    pc1=""
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'category':{'$eq':'Appeal'}}"
                    pc1=""
                    cond="{'$and':["+cond+pc1+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$tin', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'category':{'$eq':'Appeal'}}"
                        pc1=""
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'category':{'$eq':'Appeal'}}"
                        pc1=""
                        cond="{'$and':["+cond+pc1+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$bu', 'total': {'$sum': 1}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
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
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        if n > len(claim_type_lst):
            n=5
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Top Calls (By BU)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Bar")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(claim_type_lst[0:n])+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(cliam_type_cnt_lst[0:n])+""+","
        kv=kv[0:len(kv)-1]+"}"
        print(kv)
        kv=ast.literal_eval(kv)
        return kv

    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"

    return " calls_cnt_lob function "
print(get_top_calls_bu([[],[],['2019'],[]],10,['141338470']))

def get_top_calls_talk_time_int(dur_lst,n,provider_lst):

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                # cond="{'$and':["+cond+"]}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    # pc1=",{'category':{'$eq':'Appeal'}}"
                    pc1=""
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'category':{'$eq':'Appeal'}}"
                    pc1=""
                    cond="{'$and':["+cond+pc1+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$talktime', 'total': {'$sum': 1}}},{'$sort': {'_id':-1}}] ## sum after type conversion of field                              
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'category':{'$eq':'Appeal'}}"
                        pc1=""
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'category':{'$eq':'Appeal'}}"
                        pc1=""
                        cond="{'$and':["+cond+pc1+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$talktime', 'total': {'$sum': 1}}},{'$sort': {'_id':-1}}] ## sum after type conversion of field                              
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
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        op_lst=list()
        print(claim_type_lst[0])
        for c in range(0,len(claim_type_lst)):
            a=[]
            a.append(int(claim_type_lst[c]))
            a.append(int(cliam_type_cnt_lst[c]))
            op_lst.append(a)
        df=pd.DataFrame(op_lst)
        df.columns=['hdr','count1']
        # print(df)
        df.sort_values("hdr", axis = 0, ascending = False,inplace = True, na_position ='last') 
        claim_type_lst=list(df['hdr'])
        cliam_type_cnt_lst=list(df['count1'])
        print(claim_type_lst[0])
        #### to derive intervals
        int_lst=list()
        int_count_lst=list()
        upper_lmt=0
        temp=10-((claim_type_lst[0])%(10))
        upper_lmt=(claim_type_lst[0])+temp
        lower_lmt=0
        while(True):
            if (lower_lmt) > upper_lmt:
                print(lower_lmt)
                break
            if (lower_lmt) <= (upper_lmt+100):
                temp_s=str(lower_lmt)+"-"+str(lower_lmt+100)
                int_lst.append(temp_s)
                int_count_lst.append(0)
                lower_lmt=lower_lmt+100
        print(int_lst)    
        for ci in range(0,len(claim_type_lst)):
            for ii in range(0,len(int_lst)):
                if claim_type_lst[ci] in range(int(int_lst[ii].split('-')[0]),int(int_lst[ii].split('-')[1])):
                    int_count_lst[ii]=int_count_lst[ii]+cliam_type_cnt_lst[ci]
        print(int_count_lst) 
        rem_index=[]
        for ii in range(0,len(int_count_lst)):
            if int_count_lst[ii]==0:
                rem_index.append(ii)
        c=0
        for ri in rem_index:
            int_count_lst.pop(ri-c)
            int_lst.pop(ri-c)
            c=c+1
        print(int_lst) 
        print(int_count_lst) 
        op_lst=list()        
        for c in range(0,len(int_lst)):
            a=[]
            a.append((int_lst[c]))
            a.append((int_count_lst[c]))
            op_lst.append(a)
        df=pd.DataFrame(op_lst)
        df.columns=['hdr','count1']
        # print(df)
        df.sort_values("count1", axis = 0, ascending = False,inplace = True, na_position ='last') 
        claim_type_lst=list(df['hdr'])
        cliam_type_cnt_lst=list(df['count1'])
        #### to derive intervals
        if n > len(claim_type_lst):
            n=5
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Top Calls (By Talk Time)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Bar")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(claim_type_lst[0:n])+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(cliam_type_cnt_lst[0:n])+""+","
        kv=kv[0:len(kv)-1]+"}"
        print(kv)
        kv=ast.literal_eval(kv)
        return kv

    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"

    return " calls_cnt_lob function "
# print(get_top_calls_talk_time([[],[],['2019'],[]],10))


def get_top_calls_ring_time_int(dur_lst,n,provider_lst):

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                # cond="{'$and':["+cond+"]}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    # pc1=",{'category':{'$eq':'Appeal'}}"
                    pc1=""
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'category':{'$eq':'Appeal'}}"
                    pc1=""
                    cond="{'$and':["+cond+pc1+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$ringtime', 'total': {'$sum': 1}}},{'$sort': {'_id':-1}}] ## sum after type conversion of field                              
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'category':{'$eq':'Appeal'}}"
                        pc1=""
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'category':{'$eq':'Appeal'}}"
                        pc1=""
                        cond="{'$and':["+cond+pc1+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$ringtime', 'total': {'$sum': 1}}},{'$sort': {'_id':-1}}] ## sum after type conversion of field                              
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
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        op_lst=list()
        print(claim_type_lst[0])
        for c in range(0,len(claim_type_lst)):
            a=[]
            a.append(int(claim_type_lst[c]))
            a.append(int(cliam_type_cnt_lst[c]))
            op_lst.append(a)
        df=pd.DataFrame(op_lst)
        df.columns=['hdr','count1']
        # print(df)
        df.sort_values("hdr", axis = 0, ascending = False,inplace = True, na_position ='last') 
        claim_type_lst=list(df['hdr'])
        cliam_type_cnt_lst=list(df['count1'])
        print(claim_type_lst[0])
        #### to derive intervals
        int_lst=list()
        int_count_lst=list()
        upper_lmt=0
        temp=10-((claim_type_lst[0])%(10))
        upper_lmt=(claim_type_lst[0])+temp
        lower_lmt=0
        while(True):
            if (lower_lmt) > upper_lmt:
                print(lower_lmt)
                break
            if (lower_lmt) <= (upper_lmt+100):
                temp_s=str(lower_lmt)+"-"+str(lower_lmt+100)
                int_lst.append(temp_s)
                int_count_lst.append(0)
                lower_lmt=lower_lmt+100
        print(int_lst)    
        for ci in range(0,len(claim_type_lst)):
            for ii in range(0,len(int_lst)):
                if claim_type_lst[ci] in range(int(int_lst[ii].split('-')[0]),int(int_lst[ii].split('-')[1])):
                    int_count_lst[ii]=int_count_lst[ii]+cliam_type_cnt_lst[ci]
        print(int_count_lst) 
        rem_index=[]
        for ii in range(0,len(int_count_lst)):
            if int_count_lst[ii]==0:
                rem_index.append(ii)
        c=0
        for ri in rem_index:
            int_count_lst.pop(ri-c)
            int_lst.pop(ri-c)
            c=c+1
        print(int_lst) 
        print(int_count_lst) 
        op_lst=list()        
        for c in range(0,len(int_lst)):
            a=[]
            a.append((int_lst[c]))
            a.append((int_count_lst[c]))
            op_lst.append(a)
        df=pd.DataFrame(op_lst)
        df.columns=['hdr','count1']
        # print(df)
        df.sort_values("count1", axis = 0, ascending = False,inplace = True, na_position ='last') 
        claim_type_lst=list(df['hdr'])
        cliam_type_cnt_lst=list(df['count1'])
        #### to derive intervals
        if n > len(claim_type_lst):
            n=5
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Top Calls (By Ring Time)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Bar")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(claim_type_lst[0:n])+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(cliam_type_cnt_lst[0:n])+""+","
        kv=kv[0:len(kv)-1]+"}"
        print(kv)
        kv=ast.literal_eval(kv)
        return kv

    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"

    return " calls_cnt_lob function "
# print(get_top_calls_ring_time([[],[],['2019'],[]],10))


def get_top_calls_hold_time_int(dur_lst,n,provider_lst):

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                # cond="{'$and':["+cond+"]}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    # pc1=",{'category':{'$eq':'Appeal'}}"
                    pc1=""
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'category':{'$eq':'Appeal'}}"
                    pc1=""
                    cond="{'$and':["+cond+pc1+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$holdtime', 'total': {'$sum': 1}}},{'$sort': {'_id':-1}}] ## sum after type conversion of field                              
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'category':{'$eq':'Appeal'}}"
                        pc1=""
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'category':{'$eq':'Appeal'}}"
                        pc1=""
                        cond="{'$and':["+cond+pc1+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$holdtime', 'total': {'$sum': 1}}},{'$sort': {'_id':-1}}] ## sum after type conversion of field                              
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
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        op_lst=list()
        print(claim_type_lst[0])
        for c in range(0,len(claim_type_lst)):
            a=[]
            a.append(int(claim_type_lst[c]))
            a.append(int(cliam_type_cnt_lst[c]))
            op_lst.append(a)
        df=pd.DataFrame(op_lst)
        df.columns=['hdr','count1']
        # print(df)
        df.sort_values("hdr", axis = 0, ascending = False,inplace = True, na_position ='last') 
        claim_type_lst=list(df['hdr'])
        cliam_type_cnt_lst=list(df['count1'])
        print(claim_type_lst[0])
        #### to derive intervals
        int_lst=list()
        int_count_lst=list()
        upper_lmt=0
        temp=10-((claim_type_lst[0])%(10))
        upper_lmt=(claim_type_lst[0])+temp
        lower_lmt=0
        while(True):
            if (lower_lmt) > upper_lmt:
                print(lower_lmt)
                break
            if (lower_lmt) <= (upper_lmt+100):
                temp_s=str(lower_lmt)+"-"+str(lower_lmt+100)
                int_lst.append(temp_s)
                int_count_lst.append(0)
                lower_lmt=lower_lmt+100
        print(int_lst)    
        for ci in range(0,len(claim_type_lst)):
            for ii in range(0,len(int_lst)):
                if claim_type_lst[ci] in range(int(int_lst[ii].split('-')[0]),int(int_lst[ii].split('-')[1])):
                    int_count_lst[ii]=int_count_lst[ii]+cliam_type_cnt_lst[ci]
        print(int_count_lst) 
        rem_index=[]
        for ii in range(0,len(int_count_lst)):
            if int_count_lst[ii]==0:
                rem_index.append(ii)
        c=0
        for ri in rem_index:
            int_count_lst.pop(ri-c)
            int_lst.pop(ri-c)
            c=c+1
        print(int_lst) 
        print(int_count_lst) 
        op_lst=list()        
        for c in range(0,len(int_lst)):
            a=[]
            a.append((int_lst[c]))
            a.append((int_count_lst[c]))
            op_lst.append(a)
        df=pd.DataFrame(op_lst)
        df.columns=['hdr','count1']
        # print(df)
        df.sort_values("count1", axis = 0, ascending = False,inplace = True, na_position ='last') 
        claim_type_lst=list(df['hdr'])
        cliam_type_cnt_lst=list(df['count1'])
        #### to derive intervals
        if n > len(claim_type_lst):
            n=5
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Top Calls (By Hold Time)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Bar")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(claim_type_lst[0:n])+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(cliam_type_cnt_lst[0:n])+""+","
        kv=kv[0:len(kv)-1]+"}"
        print(kv)
        kv=ast.literal_eval(kv)
        return kv

    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"

    return " calls_cnt_lob function "
# print(get_top_calls_hold_time([[],[],['2019'],[]],10))


def get_top_calls_total_time_int(dur_lst,n,provider_lst):

    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                # cond="{'$and':["+cond+"]}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    # pc1=",{'category':{'$eq':'Appeal'}}"
                    pc1=""
                    cond="{'$and':["+cond+pc+pc1+"]}"
                else:
                    pc1=",{'category':{'$eq':'Appeal'}}"
                    pc1=""
                    cond="{'$and':["+cond+pc1+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$total_time', 'total': {'$sum': 1}}},{'$sort': {'_id':-1}}] ## sum after type conversion of field                              
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        pc1=",{'category':{'$eq':'Appeal'}}"
                        pc1=""
                        cond="{'$and':["+cond+pc+pc1+"]}"
                    else:
                        pc1=",{'category':{'$eq':'Appeal'}}"
                        pc1=""
                        cond="{'$and':["+cond+pc1+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$total_time', 'total': {'$sum': 1}}},{'$sort': {'_id':-1}}] ## sum after type conversion of field                              
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
        # for li in range(0,len(claim_type_lst)):
        #     claim_type_lst[li]=str(claim_type_lst[li]).strip(' ').upper().replace('COM','E&I').replace('MCD','Medicaid').replace('MCR','Medicare')
        op_lst=list()
        print(claim_type_lst[0])
        for c in range(0,len(claim_type_lst)):
            a=[]
            a.append(int(claim_type_lst[c]))
            a.append(int(cliam_type_cnt_lst[c]))
            op_lst.append(a)
        df=pd.DataFrame(op_lst)
        df.columns=['hdr','count1']
        # print(df)
        df.sort_values("hdr", axis = 0, ascending = False,inplace = True, na_position ='last') 
        claim_type_lst=list(df['hdr'])
        cliam_type_cnt_lst=list(df['count1'])
        print(claim_type_lst[0])
        #### to derive intervals
        int_lst=list()
        int_count_lst=list()
        upper_lmt=0
        temp=10-((claim_type_lst[0])%(10))
        upper_lmt=(claim_type_lst[0])+temp
        lower_lmt=0
        while(True):
            if (lower_lmt) > upper_lmt:
                print(lower_lmt)
                break
            if (lower_lmt) <= (upper_lmt+100):
                temp_s=str(lower_lmt)+"-"+str(lower_lmt+100)
                int_lst.append(temp_s)
                int_count_lst.append(0)
                lower_lmt=lower_lmt+100
        print(int_lst)    
        for ci in range(0,len(claim_type_lst)):
            for ii in range(0,len(int_lst)):
                if claim_type_lst[ci] in range(int(int_lst[ii].split('-')[0]),int(int_lst[ii].split('-')[1])):
                    int_count_lst[ii]=int_count_lst[ii]+cliam_type_cnt_lst[ci]
        print(int_count_lst) 
        rem_index=[]
        for ii in range(0,len(int_count_lst)):
            if int_count_lst[ii]==0:
                rem_index.append(ii)
        c=0
        for ri in rem_index:
            int_count_lst.pop(ri-c)
            int_lst.pop(ri-c)
            c=c+1
        print(int_lst) 
        print(int_count_lst) 
        op_lst=list()        
        for c in range(0,len(int_lst)):
            a=[]
            a.append((int_lst[c]))
            a.append((int_count_lst[c]))
            op_lst.append(a)
        df=pd.DataFrame(op_lst)
        df.columns=['hdr','count1']
        # print(df)
        df.sort_values("count1", axis = 0, ascending = False,inplace = True, na_position ='last') 
        claim_type_lst=list(df['hdr'])
        cliam_type_cnt_lst=list(df['count1'])
        #### to derive intervals
        if n > len(claim_type_lst):
            n=5
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Top Calls (By Handling Time)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Bar")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(claim_type_lst[0:n])+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(cliam_type_cnt_lst[0:n])+""+","
        kv=kv[0:len(kv)-1]+"}"
        print(kv)
        kv=ast.literal_eval(kv)
        return kv

    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"

    return " calls_cnt_lob function "
# print(get_top_calls_total_time([[],[],['2019'],[]],10))

def get_top_calls_hold_time(dur_lst,n,provider_lst):
    ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    cond="{'$and':["+cond+pc+"]}"
                else:
                    cond="{'$and':["+cond+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$call_id', 'total': {'$max': {'$convert':{'input':'$holdtime','to':'int','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    if x['total']==None:
                        continue
                    # print(x['_id'])
                    # print(x['total'])
                    x['total']=int(str(x['total']))
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        cond="{'$and':["+cond+pc+"]}"
                    else:
                        cond="{'$and':["+cond+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$call_id', 'total': {'$max': {'$convert':{'input':'$holdtime','to':'int','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        if x['total']==None:
                            continue
                        # print(x['_id'])
                        # print(x['total'])                        
                        x['total']=int(str(x['total']))
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
        
        if n > len(claim_type_lst):
            n=5
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Top Calls (By Hold Time)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Bar")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(claim_type_lst[0:n])+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(cliam_type_cnt_lst[0:n])+""+","
        kv=kv[0:len(kv)-1]+"}"
        print(kv)
        kv=ast.literal_eval(kv)
        return kv

    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"    

    return " calls_tat_hold_lob function "
# print(get_top_calls_hold_time([[],[],['2019'],[]],10,['141338470']))

def get_top_calls_ring_time(dur_lst,n,provider_lst):
    ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    cond="{'$and':["+cond+pc+"]}"
                else:
                    cond="{'$and':["+cond+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$call_id', 'total': {'$max': {'$convert':{'input':'$ringtime','to':'int','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    if x['total']==None:
                        continue
                    # print(x['_id'])
                    # print(x['total'])
                    x['total']=int(str(x['total']))
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        cond="{'$and':["+cond+pc+"]}"
                    else:
                        cond="{'$and':["+cond+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$call_id', 'total': {'$max': {'$convert':{'input':'$ringtime','to':'int','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        if x['total']==None:
                            continue
                        # print(x['_id'])
                        # print(x['total'])                        
                        x['total']=int(str(x['total']))
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
        
        if n > len(claim_type_lst):
            n=5
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Top Calls (By Ring Time)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Bar")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(claim_type_lst[0:n])+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(cliam_type_cnt_lst[0:n])+""+","
        kv=kv[0:len(kv)-1]+"}"
        print(kv)
        kv=ast.literal_eval(kv)
        return kv

    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"    

    return " calls_tat_hold_lob function "
# print(get_top_calls_ring_time([[],[],['2019'],[]],10,['141338470']))

def get_top_calls_talk_time(dur_lst,n,provider_lst):
    ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    cond="{'$and':["+cond+pc+"]}"
                else:
                    cond="{'$and':["+cond+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$call_id', 'total': {'$max': {'$convert':{'input':'$talktime','to':'int','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    if x['total']==None:
                        continue
                    # print(x['_id'])
                    # print(x['total'])
                    x['total']=int(str(x['total']))
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        cond="{'$and':["+cond+pc+"]}"
                    else:
                        cond="{'$and':["+cond+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$call_id', 'total': {'$max': {'$convert':{'input':'$talktime','to':'int','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        if x['total']==None:
                            continue
                        # print(x['_id'])
                        # print(x['total'])                        
                        x['total']=int(str(x['total']))
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
        
        if n > len(claim_type_lst):
            n=5
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Top Calls (By Talk Time)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Bar")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(claim_type_lst[0:n])+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(cliam_type_cnt_lst[0:n])+""+","
        kv=kv[0:len(kv)-1]+"}"
        print(kv)
        kv=ast.literal_eval(kv)
        return kv

    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"    

    return " calls_tat_hold_lob function "
# print(get_top_calls_talk_time([[],[],['2019'],[]],10,['141338470']))

def get_top_calls_total_time(dur_lst,n,provider_lst):
    ## if provider list is not there then replace below statement with determining whether it's benefits/eligible/pa
    ## pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
    ## else add additonal condition determining whether it's benefits/eligible/pa
    
    try:
        cond=""
        n_records=""
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
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
                cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(mon_frmt)+"-.*'}}"
                cond=cond+",{'rcvd_date_str':{'$regex':'"+str(yr_strt)+"-.*-.*'}}"
                if len(provider_lst) > 0:
                    pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                    cond="{'$and':["+cond+pc+"]}"
                else:
                    cond="{'$and':["+cond+"]}"
                print(cond)
                my_dict = ast.literal_eval(cond)  
                pipe = [{'$match':my_dict},{'$group': {'_id':'$call_id', 'total': {'$max': {'$convert':{'input':'$total_time','to':'int','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                mydoc=(mycol.aggregate(pipeline=pipe))
                n_records=""
                for x in mydoc:
                    if x['total']==None:
                        continue
                    # print(x['_id'])
                    # print(x['total'])
                    x['total']=int(str(x['total']))
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
                    cond=cond+"{'rcvd_date_str':{'$regex':'.*-"+str(dl1)+"-.*'}}"
                    cond=cond+",{'rcvd_date_str':{'$regex':'"+str(dl)+"-.*-.*'}}"
                    # cond="{'$and':["+cond+"]}"
                    if len(provider_lst) > 0:
                        pc=",{'tin':{'$in':"+str(provider_lst)+"}}"
                        cond="{'$and':["+cond+pc+"]}"
                    else:
                        cond="{'$and':["+cond+"]}"
                    print(cond)
                    my_dict = ast.literal_eval(cond)  
                    pipe = [{'$match':my_dict},{'$group': {'_id':'$call_id', 'total': {'$max': {'$convert':{'input':'$total_time','to':'int','onError':'0','onNull':'0'}}}}},{'$sort': {'total':-1}}] ## sum after type conversion of field                              
                    mydoc=(mycol.aggregate(pipeline=pipe))
                    n_records=""
                    for x in mydoc:
                        if x['total']==None:
                            continue
                        # print(x['_id'])
                        # print(x['total'])                        
                        x['total']=int(str(x['total']))
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
        
        if n > len(claim_type_lst):
            n=5
        kv="{"
        kv=kv+"'"+str("From")+"'"+":"+"'"+str(r_from_dt)+"'"+","
        kv=kv+"'"+str("End")+"'"+":"+"'"+str(r_end_dt)+"'"+","
        kv=kv+"'"+str("Title")+"'"+":"+"'"+str("Top Calls (By Handling Time)")+"'"+","
        kv=kv+"'"+str("Graph Type")+"'"+":"+"'"+str("Bar")+"'"+","
        kv=kv+"'"+str("Header")+"'"+":"+""+str(claim_type_lst[0:n])+""+","
        kv=kv+"'"+str("Value")+"'"+":"+""+str(cliam_type_cnt_lst[0:n])+""+","
        kv=kv[0:len(kv)-1]+"}"
        print(kv)
        kv=ast.literal_eval(kv)
        return kv

    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"    

    return " calls_tat_hold_lob function "
# print(get_top_calls_total_time([[],[],['2019'],[]],10,['141338470']))
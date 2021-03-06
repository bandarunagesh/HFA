import pymongo
from datetime import datetime
import ast

def push_context_hist_calls(userid,sess_id,req_type,call_r_calls,context,call_id,frm,to,day,mon,yr):
    print("in context history push function")
    myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")
    print(myclient.list_database_names())
    mydb = myclient["HandsFreeAnalytics"]
    print(mydb.list_collection_names())
    mycol = mydb["Calls_Context_History"]
    dt=str(datetime.now()).replace(' ','').replace('-','').replace(':','')
    mydict = { "User_ID": userid, "Session_ID": sess_id,"Request_Type":req_type,"Call_R_Calls":call_r_calls,"Context":context,"Call_id":call_id,"From":frm,"To":to,"Days":day,"Months":mon,"Years":yr,"creation_dt":dt}
    x = mycol.insert_one(mydict)
    return str(x.inserted_id)

def pop_context_hist_call_info(userid,sess_id):
    print("in context history pop function")
    myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")
    print(myclient.list_database_names())
    mydb = myclient["HandsFreeAnalytics"]
    print(mydb.list_collection_names())
    mycol = mydb["Calls_Context_History"]
    cond="{\"$and\":[{\"User_ID\":\'"+str(userid)+"\'},{\"Session_ID\":\'"+str(sess_id)+"\'}]}"
    print(cond)
    my_dict = ast.literal_eval(cond)
    print(my_dict)
    mydoc=mycol.find(my_dict).sort('creation_dt',pymongo.DESCENDING)
    print(str(mydoc.count()))
    response_lst=list()
    for x in mydoc:
        print(x['Call_id'])
        response_lst.append(x['User_ID'])
        response_lst.append(x['Session_ID'])
        response_lst.append(x['Request_Type'])
        response_lst.append(x['Call_R_Calls'])
        response_lst.append(x['Context'])
        response_lst.append(x['Call_id'])
        response_lst.append(x['From'])
        response_lst.append(x['To'])
        response_lst.append(x['Days'])
        response_lst.append(x['Months'])
        response_lst.append(x['Years'])
        return response_lst
    return response_lst

def pop_context_hist_call(userid,sess_id):
    print("in context history pop function")
    myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")
    print(myclient.list_database_names())
    mydb = myclient["HandsFreeAnalytics"]
    print(mydb.list_collection_names())
    mycol = mydb["Calls_Context_History"]
    cond="{\"$and\":[{\"User_ID\":\'"+str(userid)+"\'},{\"Session_ID\":\'"+str(sess_id)+"\'},{\"Call_R_Calls\":\'"+str("CALL")+"\'}]}"
    print(cond)
    my_dict = ast.literal_eval(cond)
    print(my_dict)
    mydoc=mycol.find(my_dict).sort('creation_dt',pymongo.DESCENDING)
    print(str(mydoc.count()))
    response_lst=list()
    for x in mydoc:
        print(x['Call_id'])
        response_lst.append(x['User_ID'])
        response_lst.append(x['Session_ID'])
        response_lst.append(x['Request_Type'])
        response_lst.append(x['Call_R_Calls'])
        response_lst.append(x['Context'])
        response_lst.append(x['Call_id'])
        response_lst.append(x['From'])
        response_lst.append(x['To'])
        response_lst.append(x['Days'])
        response_lst.append(x['Months'])
        response_lst.append(x['Years'])
        return response_lst
    return response_lst

def pop_context_hist_calls(userid,sess_id):
    print("in context history pop function")
    myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")
    print(myclient.list_database_names())
    mydb = myclient["HandsFreeAnalytics"]
    print(mydb.list_collection_names())
    mycol = mydb["Calls_Context_History"]
    cond="{\"$and\":[{\"User_ID\":\'"+str(userid)+"\'},{\"Session_ID\":\'"+str(sess_id)+"\'},{\"Call_R_Calls\":\'"+str("CALLS")+"\'}]}"
    print(cond)
    my_dict = ast.literal_eval(cond)
    print(my_dict)
    mydoc=mycol.find(my_dict).sort('creation_dt',pymongo.DESCENDING)
    print(str(mydoc.count()))
    response_lst=list()
    for x in mydoc:
        print(x['Call_id'])
        response_lst.append(x['User_ID'])
        response_lst.append(x['Session_ID'])
        response_lst.append(x['Request_Type'])
        response_lst.append(x['Call_R_Calls'])
        response_lst.append(x['Context'])
        response_lst.append(x['Call_id'])
        response_lst.append(x['From'])
        response_lst.append(x['To'])
        response_lst.append(x['Days'])
        response_lst.append(x['Months'])
        response_lst.append(x['Years'])
        return response_lst
    return response_lst

# pop_context_hist("test_uid4","test_sessid4")
# day=['2','3']  
# mon=['2','3']  
# yr=['2','3']  
# push_context_hist("default","default","Normal Claim","claim","test","098232323","2312323","2322323",day,mon,yr)
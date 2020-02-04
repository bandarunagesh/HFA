from pymongo import MongoClient
import pymongo
from datetime import datetime
import ast
def conv_hist(userid,sess_id,quest,resp,intnt,conf,like_r_dislke):
    print("in conv history function")
    myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")
    print(myclient.list_database_names())
    mydb = myclient["HandsFreeAnalytics"]
    print(mydb.list_collection_names())
    mycol = mydb["Conversation_History"]
    dt=str(datetime.now()).replace(' ','').replace('-','').replace(':','')
    mydict = { "User_ID": userid, "Session_ID": sess_id,"question":quest,"response":resp,"Intent":intnt,"Confidence":conf,"like_r_dislike":like_r_dislke,"creation_dt":dt}
    x = mycol.insert_one(mydict)
    return str(x.inserted_id)
    
def pop_conv_hist(userid,sess_id):
    print("pop conv history function")
    myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")
    print(myclient.list_database_names())
    mydb = myclient["HandsFreeAnalytics"]
    print(mydb.list_collection_names())
    mycol = mydb["Conversation_History"]
    cond="{\"$and\":[{\"User_ID\":\'"+str(userid)+"\'},{\"Session_ID\":\'"+str(sess_id)+"\'}]}"
    print(cond)
    my_dict = ast.literal_eval(cond)
    print(my_dict)
    mydoc=mycol.find(my_dict).sort('creation_dt',pymongo.DESCENDING)    
    for x in mydoc:
        return str(x['question'])
    return "no conversation history found"
        
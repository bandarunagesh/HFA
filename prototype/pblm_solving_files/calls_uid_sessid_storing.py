# from pymongo import MongoClient
from datetime import datetime
import pymongo
def uid_sessid(userid,sess_id):
    print("in uid sessid function")
    myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")
    print(myclient.list_database_names())
    mydb = myclient["HandsFreeAnalytics"]
    print(mydb.list_collection_names())
    mycol = mydb["calls_uid_sessid"]
    mydoc = mycol.find({"User_ID": userid, 'Session_ID': sess_id})
    if mydoc.count()==0:        
        dt=str(datetime.now()).replace(' ','').replace('-','').replace(':','')
        mydict = { "User_ID": userid, "Session_ID": sess_id,"Created_Date":dt}
        x = mycol.insert_one(mydict)
    
    

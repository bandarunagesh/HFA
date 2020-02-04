import pymongo
from datetime import datetime
from datetime import date
from dateutil import *
import calendar
import ast
import random
import pandas as pd
import numpy as np
from collections import OrderedDict
from duckling_wrapper import *
from knowledge_rev import *
import requests

def pa_main_func(userid,sessid,req,prov_lst,req_chart_type):
    response = requests.get("http://apsrp03693:8066/parse",params={"q":req})                
    response = response.json()
    intent = response.get("intent")
    myintent=intent['name']
    print (myintent)
    if myintent.lower() == "pa_denial_rsns":
        myintent = "pa_denial_rsns_g"
    elif myintent.lower() == "pa_approve_rsns":
        myintent = "pa_approve_rsns_g"
    elif myintent.lower() == "pa_cancel_rsns":
        myintent = "pa_cancel_rsns_g"
    ans=""
    if myintent.lower() == "pa_trend_g":
        time_message,filter_message = autoTimeFilterChecker(req)
        if (time_message.lower() == "time is not defined") & (filter_message.lower() == "entity is defined"):
            entity = getEntity(req)
            ans = getReceivedTrendPA(by=entity)
        elif (time_message.lower() == "time is defined") & (filter_message.lower() == "entity is not defined"):
            timeX = TimeExtract(req)
            ans = getReceivedTrendPA(time_tuple=timeX)
        elif (time_message.lower() == "time is defined") & (filter_message.lower() == "entity is defined"):
            timeX = TimeExtract(req)
            entity=getEntity(req)
            ans = getReceivedTrendPA(time_tuple=timeX,by=entity)
        elif (time_message.lower() == "time is not defined") & (filter_message.lower() == "entity is not defined"):
            timeX = ('2019-01-01',datetime.today().strftime("%Y-%m-%d"))
            ans = getReceivedTrendPA(time_tuple=timeX)
        if ans == "":
            ans = "Sorry, Could not fetch you results at this time"
        return (ans)
    elif myintent.lower() == "pa_trend_denial_g":
        if ("rate" not in req.lower()):
            time_message,filter_message = autoTimeFilterChecker(req)
            if (time_message.lower() == "time is not defined") & (filter_message.lower() == "entity is defined"):
                entity = getEntity(req)
                ans = getDenialsTrendPA(by=entity)
            elif (time_message.lower() == "time is defined") & (filter_message.lower() == "entity is not defined"):
                timeX = TimeExtract(req)
                ans = getDenialsTrendPA(time_tuple=timeX)
            elif (time_message.lower() == "time is defined") & (filter_message.lower() == "entity is defined"):
                timeX = TimeExtract(req)
                entity=getEntity(req)
                ans = getDenialsTrendPA(time_tuple=timeX,by=entity)
            elif (time_message.lower() == "time is not defined") & (filter_message.lower() == "entity is not defined"):
                timeX = ('2019-01-01',datetime.today().strftime("%Y-%m-%d"))
                ans = getDenialsTrendPA(time_tuple=timeX)
        if ans == "":
            ans = "Sorry, Could not fetch you results at this time"
        return (ans)
    elif myintent.lower() == "pa_trend_approve_g":
        if ("approv" in req.lower()) and ("rate" not in req.lower()):
            time_message,filter_message = autoTimeFilterChecker(req)
            if (time_message.lower() == "time is not defined") & (filter_message.lower() == "entity is defined"):
                entity = getEntity(req)
                ans = getApprovedTrendPA(by=entity)
            elif (time_message.lower() == "time is defined") & (filter_message.lower() == "entity is not defined"):
                timeX = TimeExtract(req)
                ans = getApprovedTrendPA(time_tuple=timeX)
            elif (time_message.lower() == "time is defined") & (filter_message.lower() == "entity is defined"):
                timeX = TimeExtract(req)
                entity=getEntity(req)
                ans = getApprovedTrendPA(time_tuple=timeX,by=entity)
            elif (time_message.lower() == "time is not defined") & (filter_message.lower() == "entity is not defined"):
                timeX = ('2019-01-01',datetime.today().strftime("%Y-%m-%d"))
                ans = getApprovedTrendPA(time_tuple=timeX)
        if ans == "":
            ans = "Sorry, Could not fetch you results at this time"
        return (ans)
    elif myintent.lower() == "pa_trend_cancel_g":
        if ("cancelled" in req.lower()) or ("cancellation" in req.lower()) or ("cancel" in req.lower()):
            time_message,filter_message = autoTimeFilterChecker(req)
            if (time_message.lower() == "time is not defined") & (filter_message.lower() == "entity is defined"):
                entity = getEntity(req)
                ans = getCancelledTrendPA(by=entity)
            elif (time_message.lower() == "time is defined") & (filter_message.lower() == "entity is not defined"):
                timeX = TimeExtract(req)
                ans = getCancelledTrendPA(time_tuple=timeX)
            elif (time_message.lower() == "time is defined") & (filter_message.lower() == "entity is defined"):
                timeX = TimeExtract(req)
                entity=getEntity(req)
                ans = getCancelledTrendPA(time_tuple=timeX,by=entity)
            elif (time_message.lower() == "time is not defined") & (filter_message.lower() == "entity is not defined"):
                timeX = ('2019-01-01',datetime.today().strftime("%Y-%m-%d"))
                ans = getCancelledTrendPA(time_tuple=timeX)
        if ans == "":
            ans = "Sorry, Could not fetch you results at this time"
        return (ans)
    elif myintent.lower() == "pa_approval_rate_g":
        time_message,filter_message = autoTimeFilterChecker(req)
        if (time_message.lower() == "time is not defined") & (filter_message.lower() == "entity is defined"):
            entity = getEntity(req)
            ans = getApprovalRateTrendPA(by=entity)
        elif (time_message.lower() == "time is defined") & (filter_message.lower() == "entity is not defined"):
            timeX = TimeExtract(req)
            ans = getApprovalRateTrendPA(time_tuple=timeX)
        elif (time_message.lower() == "time is defined") & (filter_message.lower() == "entity is defined"):
            timeX = TimeExtract(req)
            entity=getEntity(req)
            ans = getApprovalRateTrendPA(time_tuple=timeX,by=entity)
        elif (time_message.lower() == "time is not defined") & (filter_message.lower() == "entity is not defined"):
            timeX = ('2019-01-01',datetime.today().strftime("%Y-%m-%d"))
            ans = getApprovalRateTrendPA(time_tuple=timeX)
        if ans == "":
            ans = "Sorry, Could not fetch you results at this time"
        return (ans)
    elif myintent.lower() == "pa_denial_rate_g":
        time_message,filter_message = autoTimeFilterChecker(req)
        if (time_message.lower() == "time is not defined") & (filter_message.lower() == "entity is defined"):
            entity = getEntity(req)
            ans = getDenialRateTrendPA(by=entity)
        elif (time_message.lower() == "time is defined") & (filter_message.lower() == "entity is not defined"):
            timeX = TimeExtract(req)
            ans = getDenialRateTrendPA(time_tuple=timeX)
        elif (time_message.lower() == "time is defined") & (filter_message.lower() == "entity is defined"):
            timeX = TimeExtract(req)
            entity=getEntity(req)
            ans = getDenialRateTrendPA(time_tuple=timeX,by=entity)
        elif (time_message.lower() == "time is not defined") & (filter_message.lower() == "entity is not defined"):
            timeX = ('2019-01-01',datetime.today().strftime("%Y-%m-%d"))
            ans = getDenialRateTrendPA(time_tuple=timeX)
        if ans == "":
            ans = "Sorry, Could not fetch you results at this time"
        return (ans)
    elif myintent.lower() == "pa_denial_rsns_g":
        time_message,filter_message = autoTimeFilterChecker(req)
        if (time_message.lower() == "time is not defined") & (filter_message.lower() == "entity is defined"):
            entity = getEntity(req)
            ans = showDenialReasons(by=entity,chart=req_chart_type)
        elif (time_message.lower() == "time is defined") & (filter_message.lower() == "entity is not defined"):
            timeX = TimeExtract(req)
            ans = showDenialReasons(time_tuple=timeX,chart=req_chart_type)
        elif (time_message.lower() == "time is defined") & (filter_message.lower() == "entity is defined"):
            timeX = TimeExtract(req)
            entity=getEntity(req)
            ans = showDenialReasons(time_tuple=timeX,by=entity,chart=req_chart_type)
        elif (time_message.lower() == "time is not defined") & (filter_message.lower() == "entity is not defined"):
            timeX = ('2019-01-01',datetime.today().strftime("%Y-%m-%d"))
            ans = showDenialReasons(time_tuple=timeX,chart=req_chart_type)
        if ans == "":
            ans = "Sorry, Could not fetch you results at this time"
        return (ans)
    elif myintent.lower() == "pa_cancel_rsns_g":
        time_message,filter_message = autoTimeFilterChecker(req)
        if (time_message.lower() == "time is not defined") & (filter_message.lower() == "entity is defined"):
            entity = getEntity(req)
            ans = showCancelReasons(by=entity,chart=req_chart_type)
        elif (time_message.lower() == "time is defined") & (filter_message.lower() == "entity is not defined"):
            timeX = TimeExtract(req)
            ans = showCancelReasons(time_tuple=timeX,chart=req_chart_type)
        elif (time_message.lower() == "time is defined") & (filter_message.lower() == "entity is defined"):
            timeX = TimeExtract(req)
            entity=getEntity(req)
            ans = showCancelReasons(time_tuple=timeX,by=entity,chart=req_chart_type)
        elif (time_message.lower() == "time is not defined") & (filter_message.lower() == "entity is not defined"):
            timeX = ('2019-01-01',datetime.today().strftime("%Y-%m-%d"))
            ans = showCancelReasons(time_tuple=timeX,chart=req_chart_type)
        if ans == "":
            ans = "Sorry, Could not fetch you results at this time"
        return (ans)
    elif myintent.lower() == "pa_approve_rsns_g":
        time_message,filter_message = autoTimeFilterChecker(req)
        if (time_message.lower() == "time is not defined") & (filter_message.lower() == "entity is defined"):
            entity = getEntity(req)
            ans = showApprovalReasons(by=entity,chart=req_chart_type)
        elif (time_message.lower() == "time is defined") & (filter_message.lower() == "entity is not defined"):
            timeX = TimeExtract(req)
            ans = showApprovalReasons(time_tuple=timeX,chart=req_chart_type)
        elif (time_message.lower() == "time is defined") & (filter_message.lower() == "entity is defined"):
            timeX = TimeExtract(req)
            entity=getEntity(req)
            ans = showApprovalReasons(time_tuple=timeX,by=entity,chart=req_chart_type)
        elif (time_message.lower() == "time is not defined") & (filter_message.lower() == "entity is not defined"):
            timeX = ('2019-01-01',datetime.today().strftime("%Y-%m-%d"))
            ans = showApprovalReasons(time_tuple=timeX,chart=req_chart_type)
        if ans == "":
            ans = "Sorry, Could not fetch you results at this time"
        return (ans)
    else:
        return (u"Sorry I do not have an answer for that. You may reach out to us through call or email for assistance.")
                    
def getEntity(req):
    entity=''
    if 'lob' in req.lower() or 'line of business' in req.lower():
        entity='lob'
    elif 'setting' in req.lower() or 'service setting' in req.lower():
        entity='srvc_setting_typ'
    elif 'service type' in req.lower() or 'servicetype' in req.lower() or 'type' in req.lower():
        entity='srvc_desc_typ'
    elif 'service category' in req.lower() or 'category' in req.lower() or 'categ' in req.lower() or 'cat' in req.lower() or 'servicecat' in req.lower():
        entity='service_category'
    elif 'tat' in req.lower() or 'turnaround' in req.lower() or 'turn around' in req.lower():
        entity = 'tat_hrs'
    elif 'status' in req.lower() or 'outcome' in req.lower():
        entity = 'outcome'
    return (entity)
                        
def autoTimeFilterChecker(req):
    try:
        myTime = TimeExtract(req)
    except Exception as e:
        if 'lob' in req.lower() or 'line of business' in req.lower():
            entity='lob'
        elif 'setting' in req.lower() or 'service setting' in req.lower():
            entity='srvc_setting_typ'
        elif 'service type' in req.lower() or 'servicetype' in req.lower() or 'type' in req.lower():
            entity='srvc_desc_typ'
        elif 'service category' in req.lower() or 'categ' in req.lower() or 'cat' in req.lower() or 'category' in req.lower() or 'service cat' in req.lower() or 'servicecat' in req.lower():
            entity='service_category'
        elif 'tat' in req.lower() or 'turnaround' in req.lower() or 'turn around' in req.lower():
            entity = 'tat_hrs'
    
    try:
        myTime
    except NameError:
        ind_message_time = "time is not defined"
    else:
        ind_message_time = "time is defined"
    
    try:
        entity
    except NameError:
        ind_message_filter = "entity is not defined"
    else:
        ind_message_filter = "entity is defined"
        
    if (ind_message_time=="time is defined") and (ind_message_filter=="entity is not defined"):
        if (('lob' in req.lower()) |
            ('line of business' in req.lower()) |
            ('setting' in req.lower()) |
            ('service setting' in req.lower()) |
            ('service type' in req.lower()) |
            ('servicetype' in req.lower()) |
            ('type' in req.lower()) |
            ('service category' in req.lower()) |
            ('category' in req.lower()) |
            ('categ' in req.lower()) |
            ('cat' in req.lower()) |
            ('service cat' in req.lower()) |
            ('servicecat' in req.lower()) |
            ('tat' in req.lower()) |
            ('turnaround' in req.lower()) |
            ('turn around' in req.lower())):
            ind_message_filter = "entity is defined"
    return ((ind_message_time,ind_message_filter))


def TimeExtract(question):
    Time = time_extract(question)
    if Time[0]:
        start_time = Time[0].split(' ')[0]
        end_time = Time[1].split('}')[0].split(' ')[0]
        return ((start_time,end_time))
    elif Time[1]:
        dateStr = '-'.join([Time[2][0],Time[1][0]])
        dateStr = datetime.strptime(dateStr,"%Y-%m")
        newdateStr = dateStr + relativedelta.relativedelta(months=1)
        dateStr = dateStr.strftime("%Y-%m-%d")
        newdateStr = newdateStr.strftime("%Y-%m-%d")
        return ((dateStr,newdateStr))
    elif Time[2]:
        if str(datetime.today().year) == Time[2][0]:
            dt1 = date(datetime.today().year,1,1).strftime("%Y-%m-%d")
            dt2 = datetime.today().strftime("%Y-%m-%d")
            return ((dt1,dt2))
        else:
            dt1 = date(int(Time[2][0]),1,1).strftime("%Y-%m-%d")
            dt2 = date(int(Time[2][0]),12,31).strftime("%Y-%m-%d")
            return ((dt1,dt2))

############################## 01. Received PA Requests Trend ###############################
def getReceivedTrendPA(time_tuple=None,by=None):
    if time_tuple!=None and by==None:
        try:
            result_dict = OrderedDict()
            myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")
            mydb = myclient["HandsFreeAnalytics"]
            from_dt = datetime.strptime(time_tuple[0],'%Y-%m-%d')
            to_dt = datetime.strptime(time_tuple[1],'%Y-%m-%d')
            mycol = mydb["HSR_Data"]
            mydoc = mycol.find({'creat_dttm':{'$gte':from_dt,'$lt':to_dt}},{'creat_dttm':1,'hsc_id':1})
            pa_volume = []
            for x in mydoc:
                pa_volume.append((x['creat_dttm'].strftime("%Y-%m-%d"),x['hsc_id']))
            df_pa_volume = pd.DataFrame(pa_volume,columns=['create_date','hsc_id'])
            grouped_data = pd.DataFrame(df_pa_volume.groupby('create_date')['hsc_id'].nunique())
            grouped_data.index = [datetime.strptime(i,"%Y-%m-%d").strftime("%B %Y") for i in grouped_data.index]
            grouped_data['date'] = grouped_data.index
            grouped_data = grouped_data.reset_index(level=0,drop=True)
            grouped_data = grouped_data[['date','hsc_id']]
            result = grouped_data.groupby('date',sort=False)['hsc_id'].sum()
            result_dict['From'] = str(pd.Timestamp(time_tuple[0]))
            result_dict['End'] = str(pd.Timestamp(time_tuple[1]))
            result_dict['Title'] = "PA Received Requests Trend (Volume)"
            result_dict["Graph Type"] = "Line"
            result_dict['Header'] = ['-'.join([x.split(' ')[0][:3],x.split(' ')[1][-2:]]) for x in result.index.tolist()]
            result_dict['Value'] = result.values.tolist()
            return (dict(result_dict))
        except Exception as e:
            print (str(e))
            return "Sorry, Could not fetch you results at this time"
    elif time_tuple==None and by!=None:
        try:
            result_dict = OrderedDict()
            byDict = {'srvc_setting_typ':'Service Setting Type',
                      'srvc_desc_typ':'Service Type',
                      'lob':'lob',
                      'service_category':'Service Category',
                      'tat_hrs':'tat'}
            myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")
            mydb = myclient["HandsFreeAnalytics"]
            mycol = mydb["HSR_Data"]
            z = '$' + by
            mydoc = mycol.aggregate([{'$group':{"_id":z,"cIds":{'$addToSet':"$hsc_id"}}},
                                     {'$project':{by:"$_id","_id":0,"hsc_Ids":{'$size':"$cIds"}}}])
            byAgg = []         
            for x in mydoc:
                byAgg.append([x[by],x['hsc_Ids']])
            result_dict['From'] = ""
            result_dict['End'] = ""
            result_dict['Title'] = "PA Received Requests by " + byDict[by].upper()
            result_dict["Graph Type"] = "Bar"
            result_dict["Header"] = [f[0] for f in byAgg]
            result_dict["Value"] = [f[1] for f in byAgg]
            return (dict(result_dict))
        except Exception as e:
            print (str(e))
            return "Sorry, Could not fetch you results at this time"
    elif time_tuple!=None and by!=None:
        try:
            result_dict = OrderedDict()
            byDict = {'srvc_setting_typ':'Service Setting Type',
                      'srvc_desc_typ':'Service Type',
                      'lob':'lob',
                      'service_category':'Service Category',
                      'tat_hrs':'tat'}
            myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")
            mydb = myclient["HandsFreeAnalytics"]
            from_dt = datetime.strptime(time_tuple[0],'%Y-%m-%d')
            to_dt = datetime.strptime(time_tuple[1],'%Y-%m-%d')
            mycol = mydb["HSR_Data"]
            mydoc = mycol.find({'creat_dttm':{'$gte':from_dt,'$lt':to_dt}},{'creat_dttm':1,by:1,'hsc_id':1})
            pa_volume = []
            for x in mydoc:
                pa_volume.append((x['creat_dttm'].strftime("%Y-%m-%d"),x[by],x['hsc_id']))
            df_pa_volume = pd.DataFrame(pa_volume,columns=['create_date',by,'hsc_id'])
            grouped_data = pd.DataFrame(df_pa_volume.groupby(['create_date',by])['hsc_id'].nunique())
            grouped_data = grouped_data.reset_index()
            grouped_data = grouped_data.set_index('create_date')
            grouped_data.index = [datetime.strptime(i,"%Y-%m-%d").strftime("%B %Y") for i in grouped_data.index]
            grouped_data['date'] = grouped_data.index
            grouped_data = grouped_data.reset_index(level=0,drop=True)
            grouped_data = grouped_data[['date',by,'hsc_id']]
            result = grouped_data.groupby(['date',by],sort=False)['hsc_id'].sum()
            result = result.groupby(level=[1]).sum()
            result_dict['From'] = str(pd.Timestamp(time_tuple[0]))
            result_dict['End'] = str(pd.Timestamp(time_tuple[1]))
            result_dict['Title'] = "PA Received Requests (Volume) " + byDict[by].upper()
            result_dict["Graph Type"] = "Bar"
            result_dict["Header"] = result.index.tolist()
            result_dict['Value'] = result.values.tolist()
            return (dict(result_dict))
        except Exception as e:
            print (str(e))
            return "Sorry, Could not fetch you results at this time"
            
################################# 02. PA denialS Trend ##############################

def getDenialsTrendPA(time_tuple=None,by=None):
    if time_tuple!=None and by==None:
        try:
            result_dict = OrderedDict()
            myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")
            mydb = myclient["HandsFreeAnalytics"]
            from_dt = datetime.strptime(time_tuple[0],'%Y-%m-%d')
            to_dt = datetime.strptime(time_tuple[1],'%Y-%m-%d')
            mycol = mydb["HSR_Data"]
            mydoc = mycol.find({'creat_dttm':{'$gte':from_dt,'$lt':to_dt},'outcome':'Denied'},{'creat_dttm':1,'hsc_id':1})
            pa_volume = []
            for x in mydoc:
                pa_volume.append((x['creat_dttm'].strftime("%Y-%m-%d"),x['hsc_id']))
            df_pa_volume = pd.DataFrame(pa_volume,columns=['create_date','hsc_id'])
            grouped_data = pd.DataFrame(df_pa_volume.groupby('create_date')['hsc_id'].nunique())
            grouped_data.index = [datetime.strptime(i,"%Y-%m-%d").strftime("%B %Y") for i in grouped_data.index]
            grouped_data['date'] = grouped_data.index
            grouped_data = grouped_data.reset_index(level=0,drop=True)
            grouped_data = grouped_data[['date','hsc_id']]
            result = grouped_data.groupby('date',sort=False)['hsc_id'].sum()
            result_dict['From'] = str(pd.Timestamp(time_tuple[0]))
            result_dict['End'] = str(pd.Timestamp(time_tuple[1]))
            result_dict['Title'] = "PA Denials Trend (Volume)"
            result_dict["Graph Type"] = "Line"
            result_dict["Header"] = ['-'.join([x.split(' ')[0][:3],x.split(' ')[1][-2:]]) for x in result.index.tolist()]
            result_dict['Value'] = result.values.tolist()
            return (dict(result_dict))
        except Exception as e:
            print (str(e))
            return "Sorry, Could not fetch you results at this time"
    elif time_tuple==None and by!= None:
        try:
            result_dict = OrderedDict()
            byDict = {'srvc_setting_typ':'Service Setting Type',
                      'srvc_desc_typ':'Service Type',
                      'lob':'lob',
                      'service_category':'Service Category',
                      'tat_hrs':'tat'}
            myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")
            mydb = myclient["HandsFreeAnalytics"]
            mycol = mydb["HSR_Data"]
            z = '$' + by
            mydoc = mycol.aggregate([{'$match':{'outcome':'Denied'}},{'$group':{"_id":z,"cIds":{'$addToSet':"$hsc_id"}}},
                                     {'$project':{by:"$_id","_id":0,"hsc_Ids":{'$size':"$cIds"}}}])
            byAgg = []         
            for x in mydoc:
                byAgg.append([x[by],x['hsc_Ids']])
            result_dict['From'] = ""
            result_dict['End'] = ""
            result_dict['Title'] = "PA Denials Trend by " + byDict[by].upper()
            result_dict["Graph Type"] = "Bar"
            result_dict["Header"] = [f[0] for f in byAgg]
            result_dict["Value"] = [f[1] for f in byAgg]
            return (dict(result_dict))
        except Exception as e:
            print (str(e))
            return "Sorry, Could not fetch you results at this time"
    elif time_tuple!=None and by!=None:
        try:
            result_dict = OrderedDict()
            byDict = {'srvc_setting_typ':'Service Setting Type',
                      'srvc_desc_typ':'Service Type',
                      'lob':'lob',
                      'service_category':'Service Category',
                      'tat_hrs':'tat'}
            myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")
            mydb = myclient["HandsFreeAnalytics"]
            from_dt = datetime.strptime(time_tuple[0],'%Y-%m-%d')
            to_dt = datetime.strptime(time_tuple[1],'%Y-%m-%d')
            mycol = mydb["HSR_Data"]
            mydoc = mycol.find({'creat_dttm':{'$gte':from_dt,'$lt':to_dt},'outcome':'Denied'},{'creat_dttm':1,by:1,'hsc_id':1})
            pa_volume = []
            for x in mydoc:
                pa_volume.append((x['creat_dttm'].strftime("%Y-%m-%d"),x[by],x['hsc_id']))
            df_pa_volume = pd.DataFrame(pa_volume,columns=['create_date',by,'hsc_id'])
            grouped_data = pd.DataFrame(df_pa_volume.groupby(['create_date',by])['hsc_id'].nunique())
            grouped_data = grouped_data.reset_index()
            grouped_data = grouped_data.set_index('create_date')
            grouped_data.index = [datetime.strptime(i,"%Y-%m-%d").strftime("%B %Y") for i in grouped_data.index]
            grouped_data['date'] = grouped_data.index
            grouped_data = grouped_data.reset_index(level=0,drop=True)
            grouped_data = grouped_data[['date',by,'hsc_id']]
            result = grouped_data.groupby(['date',by],sort=False)['hsc_id'].sum()
            result = result.groupby(level=[1]).sum()
            result_dict['From'] = str(pd.Timestamp(time_tuple[0]))
            result_dict['End'] = str(pd.Timestamp(time_tuple[1]))
            result_dict['Title'] = "PA Denied Requests (Volume) " + byDict[by].upper()
            result_dict["Graph Type"] = "Bar"
            result_dict["Header"] = result.index.tolist()
            result_dict['Value'] = result.values.tolist()
            return (dict(result_dict))
        except Exception as e:
            print (str(e))
            return "Sorry, Could not fetch you results at this time"
    
    
################################### 03. PA Approvals Trend #################################

def getApprovedTrendPA(time_tuple=None,by=None):
    if time_tuple!=None and by==None:
        try:
            result_dict = OrderedDict()
            myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")
            mydb = myclient["HandsFreeAnalytics"]
            from_dt = datetime.strptime(time_tuple[0],'%Y-%m-%d')
            to_dt = datetime.strptime(time_tuple[1],'%Y-%m-%d')
            mycol = mydb["HSR_Data"]
            mydoc = mycol.find({'creat_dttm':{'$gte':from_dt,'$lt':to_dt},'outcome':'Approved'},{'creat_dttm':1,'hsc_id':1})
            pa_volume = []
            for x in mydoc:
                pa_volume.append((x['creat_dttm'].strftime("%Y-%m-%d"),x['hsc_id']))
            df_pa_volume = pd.DataFrame(pa_volume,columns=['create_date','hsc_id'])
            grouped_data = pd.DataFrame(df_pa_volume.groupby('create_date')['hsc_id'].nunique())
            grouped_data.index = [datetime.strptime(i,"%Y-%m-%d").strftime("%B %Y") for i in grouped_data.index]
            grouped_data['date'] = grouped_data.index
            grouped_data = grouped_data.reset_index(level=0,drop=True)
            grouped_data = grouped_data[['date','hsc_id']]
            result = grouped_data.groupby('date',sort=False)['hsc_id'].sum()
            result_dict['From'] = str(pd.Timestamp(time_tuple[0]))
            result_dict['End'] = str(pd.Timestamp(time_tuple[1]))
            result_dict['Title'] = "PA Approvals Trend (Volume)"
            result_dict["Graph Type"] = "Line"
            result_dict["Header"] = ['-'.join([x.split(' ')[0][:3],x.split(' ')[1][-2:]]) for x in result.index.tolist()]
            result_dict['Value'] = result.values.tolist()
            return (dict(result_dict))
        except Exception as e:
            print (str(e))
            return "Sorry, Could not fetch you results at this time"
    elif time_tuple==None and by!=None:
        try:
            result_dict = OrderedDict()
            byDict = {'srvc_setting_typ':'Service Setting Type',
                      'srvc_desc_typ':'Service Type',
                      'lob':'lob',
                      'service_category':'Service Category',
                      'tat_hrs':'tat'}
            myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")
            mydb = myclient["HandsFreeAnalytics"]
            mycol = mydb["HSR_Data"]
            z = '$' + by
            mydoc = mycol.aggregate([{'$match':{'outcome':'Approved'}},{'$group':{"_id":z,"cIds":{'$addToSet':"$hsc_id"}}},
                                     {'$project':{by:"$_id","_id":0,"hsc_Ids":{'$size':"$cIds"}}}])
            byAgg = []         
            for x in mydoc:
                byAgg.append([x[by],x['hsc_Ids']])
            result_dict['From'] = ""
            result_dict['End'] = ""
            result_dict['Title'] = "PA Approvals (Volume) by " + byDict[by].upper()
            result_dict["Graph Type"] = "Bar"
            result_dict["Header"] = [f[0] for f in byAgg]
            result_dict["Value"] = [f[1] for f in byAgg]
            return (dict(result_dict))
        except Exception as e:
            print (str(e))
            return "Sorry, Could not fetch you results at this time"
    elif time_tuple!=None and by!=None:
        try:
            result_dict = OrderedDict()
            byDict = {'srvc_setting_typ':'Service Setting Type',
                      'srvc_desc_typ':'Service Type',
                      'lob':'lob',
                      'service_category':'Service Category',
                      'tat_hrs':'tat'}
            myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")
            mydb = myclient["HandsFreeAnalytics"]
            from_dt = datetime.strptime(time_tuple[0],'%Y-%m-%d')
            to_dt = datetime.strptime(time_tuple[1],'%Y-%m-%d')
            mycol = mydb["HSR_Data"]
            mydoc = mycol.find({'creat_dttm':{'$gte':from_dt,'$lt':to_dt},'outcome':'Approved'},{'creat_dttm':1,by:1,'hsc_id':1})
            pa_volume = []
            for x in mydoc:
                pa_volume.append((x['creat_dttm'].strftime("%Y-%m-%d"),x[by],x['hsc_id']))
            df_pa_volume = pd.DataFrame(pa_volume,columns=['create_date',by,'hsc_id'])
            grouped_data = pd.DataFrame(df_pa_volume.groupby(['create_date',by])['hsc_id'].nunique())
            grouped_data = grouped_data.reset_index()
            grouped_data = grouped_data.set_index('create_date')
            grouped_data.index = [datetime.strptime(i,"%Y-%m-%d").strftime("%B %Y") for i in grouped_data.index]
            grouped_data['date'] = grouped_data.index
            grouped_data = grouped_data.reset_index(level=0,drop=True)
            grouped_data = grouped_data[['date',by,'hsc_id']]
            result = grouped_data.groupby(['date',by],sort=False)['hsc_id'].sum()
            result = result.groupby(level=[1]).sum()
            result_dict['From'] = str(pd.Timestamp(time_tuple[0]))
            result_dict['End'] = str(pd.Timestamp(time_tuple[1]))
            result_dict['Title'] = "PA Approved Requests (Volume) " + byDict[by].upper()
            result_dict["Graph Type"] = "Bar"
            result_dict["Header"] = result.index.tolist()
            result_dict['Value'] = result.values.tolist()
            return (dict(result_dict))
        except Exception as e:
            print (str(e))
            return "Sorry, Could not fetch you results at this time"
    
        
################################### 04. Cancelled PA requests Trend ################################

def getCancelledTrendPA(time_tuple=None,by=None):
    if time_tuple!=None and by==None:
        try:
            result_dict = OrderedDict()
            myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")
            mydb = myclient["HandsFreeAnalytics"]
            from_dt = datetime.strptime(time_tuple[0],'%Y-%m-%d')
            to_dt = datetime.strptime(time_tuple[1],'%Y-%m-%d')
            mycol = mydb["HSR_Data"]
            mydoc = mycol.find({'creat_dttm':{'$gte':from_dt,'$lt':to_dt},'outcome':'Cancelled'},{'creat_dttm':1,'hsc_id':1})
            pa_volume = []
            for x in mydoc:
                pa_volume.append((x['creat_dttm'].strftime("%Y-%m-%d"),x['hsc_id']))
            df_pa_volume = pd.DataFrame(pa_volume,columns=['create_date','hsc_id'])
            grouped_data = pd.DataFrame(df_pa_volume.groupby('create_date')['hsc_id'].nunique())
            grouped_data.index = [datetime.strptime(i,"%Y-%m-%d").strftime("%B %Y") for i in grouped_data.index]
            grouped_data['date'] = grouped_data.index
            grouped_data = grouped_data.reset_index(level=0,drop=True)
            grouped_data = grouped_data[['date','hsc_id']]
            result = grouped_data.groupby('date',sort=False)['hsc_id'].sum()
            result_dict['From'] = str(pd.Timestamp(time_tuple[0]))
            result_dict['End'] = str(pd.Timestamp(time_tuple[1]))
            result_dict['Title'] = "PA Cancellations Trend (Volume)"
            result_dict["Graph Type"] = "Line"
            result_dict["Header"] = ['-'.join([x.split(' ')[0][:3],x.split(' ')[1][-2:]]) for x in result.index.tolist()]
            result_dict['Value'] = result.values.tolist()
            return (dict(result_dict))
        except Exception as e:
            print (str(e))
            return "Sorry, Could not fetch you results at this time"
    elif time_tuple==None and by!=None:
        try:
            result_dict = OrderedDict()
            byDict = {'srvc_setting_typ':'Service Setting Type',
                      'srvc_desc_typ':'Service Type',
                      'lob':'lob',
                      'service_category':'Service Category',
                      'tat_hrs':'tat'}
            myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")
            mydb = myclient["HandsFreeAnalytics"]
            mycol = mydb["HSR_Data"]
            z = '$' + by
            mydoc = mycol.aggregate([{'$match':{'outcome':'Cancelled'}},{'$group':{"_id":z,"cIds":{'$addToSet':"$hsc_id"}}},
                                     {'$project':{by:"$_id","_id":0,"hsc_Ids":{'$size':"$cIds"}}}])
            byAgg = []         
            for x in mydoc:
                byAgg.append([x[by],x['hsc_Ids']])
            result_dict['From'] = ""
            result_dict['End'] = ""
            result_dict['Title'] = "PA Cancellations (Volume) by " + byDict[by].upper()
            result_dict["Graph Type"] = "Bar"
            result_dict["Header"] = [f[0] for f in byAgg]
            result_dict["Value"] = [f[1] for f in byAgg]
            return (dict(result_dict))
        except Exception as e:
            print (str(e))
            return "Sorry, Could not fetch you results at this time"
    elif time_tuple!=None and by!=None:
        try:
            result_dict = OrderedDict()
            byDict = {'srvc_setting_typ':'Service Setting Type',
                      'srvc_desc_typ':'Service Type',
                      'lob':'lob',
                      'service_category':'Service Category',
                      'tat_hrs':'tat'}
            myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")
            mydb = myclient["HandsFreeAnalytics"]
            from_dt = datetime.strptime(time_tuple[0],'%Y-%m-%d')
            to_dt = datetime.strptime(time_tuple[1],'%Y-%m-%d')
            mycol = mydb["HSR_Data"]
            mydoc = mycol.find({'creat_dttm':{'$gte':from_dt,'$lt':to_dt},'outcome':'Cancelled'},{'creat_dttm':1,by:1,'hsc_id':1})
            pa_volume = []
            for x in mydoc:
                pa_volume.append((x['creat_dttm'].strftime("%Y-%m-%d"),x[by],x['hsc_id']))
            df_pa_volume = pd.DataFrame(pa_volume,columns=['create_date',by,'hsc_id'])
            grouped_data = pd.DataFrame(df_pa_volume.groupby(['create_date',by])['hsc_id'].nunique())
            grouped_data = grouped_data.reset_index()
            grouped_data = grouped_data.set_index('create_date')
            grouped_data.index = [datetime.strptime(i,"%Y-%m-%d").strftime("%B %Y") for i in grouped_data.index]
            grouped_data['date'] = grouped_data.index
            grouped_data = grouped_data.reset_index(level=0,drop=True)
            grouped_data = grouped_data[['date',by,'hsc_id']]
            result = grouped_data.groupby(['date',by],sort=False)['hsc_id'].sum()
            result = result.groupby(level=[1]).sum()
            result_dict['From'] = str(pd.Timestamp(time_tuple[0]))
            result_dict['End'] = str(pd.Timestamp(time_tuple[1]))
            result_dict['Title'] = "PA Cancelled Requests (Volume) " + byDict[by].upper()
            result_dict["Graph Type"] = "Bar"
            result_dict["Header"] = result.index.tolist()
            result_dict['Value'] = result.values.tolist()
            return (dict(result_dict))
        except Exception as e:
            print (str(e))
            return "Sorry, Could not fetch you results at this time"
    
        
################################### 05. Denial Rate Trend for PA ####################################

def getDenialRateTrendPA(time_tuple=None,by=None):
    if time_tuple!=None and by==None:
        try:
            result_dict = OrderedDict()
            myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")
            mydb = myclient["HandsFreeAnalytics"]
            from_dt = datetime.strptime(time_tuple[0],'%Y-%m-%d')
            to_dt = datetime.strptime(time_tuple[1],'%Y-%m-%d')
            mycol = mydb["HSR_Data"]
            mydoc_total = mycol.find({'creat_dttm':{'$gte':from_dt,'$lt':to_dt}},{'creat_dttm':1,'hsc_id':1})
            pa_volume_total = []
            for x in mydoc_total:
                pa_volume_total.append((x['creat_dttm'].strftime("%Y-%m-%d"),x['hsc_id']))
            pa_total_count = pd.DataFrame(pa_volume_total,columns = ['create_date','hsc_id'])
            gp_data = pd.DataFrame(pa_total_count.groupby('create_date')['hsc_id'].nunique())
            gp_data.index = [datetime.strptime(i,"%Y-%m-%d").strftime("%B %Y") for i in gp_data.index]
            gp_data['date'] = gp_data.index
            gp_data = gp_data.reset_index(level=0,drop=True)
            gp_data = gp_data[['date','hsc_id']]
            result_total = gp_data.groupby('date',sort=False)['hsc_id'].sum()
            mydoc = mycol.find({'creat_dttm':{'$gte':from_dt,'$lt':to_dt},'outcome':'Denied'},{'creat_dttm':1,'hsc_id':1})
            pa_volume = []
            for x in mydoc:
                pa_volume.append((x['creat_dttm'].strftime("%Y-%m-%d"),x['hsc_id']))
            df_pa_volume = pd.DataFrame(pa_volume,columns=['create_date','hsc_id'])
            grouped_data = pd.DataFrame(df_pa_volume.groupby('create_date')['hsc_id'].nunique())
            grouped_data.index = [datetime.strptime(i,"%Y-%m-%d").strftime("%B %Y") for i in grouped_data.index]
            grouped_data['date'] = grouped_data.index
            grouped_data = grouped_data.reset_index(level=0,drop=True)
            grouped_data = grouped_data[['date','hsc_id']]
            result = grouped_data.groupby('date',sort=False)['hsc_id'].sum()
            result_dict['From'] = str(pd.Timestamp(time_tuple[0]))
            result_dict['End'] = str(pd.Timestamp(time_tuple[1]))
            result_dict['Title'] = "PA Denial Rate Trend"
            result_dict["Graph Type"] = "Line"
            result_dict["Header"] = ['-'.join([x.split(' ')[0][:3],x.split(' ')[1][-2:]]) for x in result.index.tolist()]
            result_dict['Value'] = list(np.divide(result.values.tolist(),result_total.values.tolist()))
            result_dict['Value'] = [round(x,2) for x in result_dict['Value']]
            return (dict(result_dict))
        except Exception as e:
            print (str(e))
            return "Sorry, Could not fetch you results at this time"
    elif time_tuple==None and by!= None:
        try:
            result_dict = OrderedDict()
            byDict = {'srvc_setting_typ':'Service Setting Type',
                      'srvc_desc_typ':'Service Type',
                      'lob':'lob',
                      'service_category':'Service Category',
                      'tat_hrs':'tat'}
            myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")
            mydb = myclient["HandsFreeAnalytics"]
            mycol = mydb["HSR_Data"]
            z = '$' + by
            mydoc1 = mycol.aggregate([{'$group':{"_id":z,"cIds":{'$addToSet':"$hsc_id"}}},
                                     {'$project':{by:"$_id","_id":0,"hsc_Ids":{'$size':"$cIds"}}}])
            byAgg_total = []
            for x in mydoc1:
                byAgg_total.append([x[by],x['hsc_Ids']])
            mydoc = mycol.aggregate([{'$match':{'outcome':'Denied'}},{'$group':{"_id":z,"cIds":{'$addToSet':"$hsc_id"}}},
                                     {'$project':{by:"$_id","_id":0,"hsc_Ids":{'$size':"$cIds"}}}])
            byAgg = []         
            for x in mydoc:
                byAgg.append([x[by],x['hsc_Ids']])
            result_dict['From'] = ""
            result_dict['End'] = ""
            result_dict['Title'] = "PA Denial Rate by " + byDict[by].upper()
            result_dict["Graph Type"] = "Bar"
            result_dict["Header"] = [f[0] for f in byAgg]
            result_dict["Value"] = [dict(byAgg)[f]/dict(byAgg_total)[f] for f in result_dict['Header']]
            result_dict['Value'] = [round(x,2) for x in result_dict['Value']]
            return (dict(result_dict))
        except Exception as e:
            print (str(e))
            return "Sorry, Could not fetch you results at this time"
    elif time_tuple!=None and by!=None:
        try:
            result_dict = OrderedDict()
            byDict = {'srvc_setting_typ':'Service Setting Type',
                      'srvc_desc_typ':'Service Type',
                      'lob':'lob',
                      'service_category':'Service Category',
                      'tat_hrs':'tat'}
            myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")
            mydb = myclient["HandsFreeAnalytics"]
            from_dt = datetime.strptime(time_tuple[0],'%Y-%m-%d')
            to_dt = datetime.strptime(time_tuple[1],'%Y-%m-%d')
            mycol = mydb["HSR_Data"]
            z = '$' + by
            mydoc1 = mycol.aggregate([{'$group':{"_id":z,"cIds":{'$addToSet':"$hsc_id"}}},
                                     {'$project':{by:"$_id","_id":0,"hsc_Ids":{'$size':"$cIds"}}}])
            byAgg_total = []
            for x in mydoc1:
                byAgg_total.append([x[by],x['hsc_Ids']])
            mydoc = mycol.aggregate([{'$match':{'creat_dttm':{'$gte':from_dt,'$lt':to_dt},'outcome':'Denied'}},{'$group':{"_id":z,"cIds":{'$addToSet':"$hsc_id"}}},
                                     {'$project':{by:"$_id","_id":0,"hsc_Ids":{'$size':"$cIds"}}}])
            byAgg = []         
            for x in mydoc:
                byAgg.append([x[by],x['hsc_Ids']])
            result_dict['From'] = ""
            result_dict['End'] = ""
            result_dict['Title'] = "PA Denial Rate by " + byDict[by].upper()
            result_dict["Graph Type"] = "Bar"
            result_dict["Header"] = [f[0] for f in byAgg]
            result_dict["Value"] = [dict(byAgg)[f]/dict(byAgg_total)[f] for f in result_dict['Header']]
            result_dict['Value'] = [round(x,2) for x in result_dict['Value']]
            return (dict(result_dict))
        except Exception as e:
            print (str(e))
            return "Sorry, Could not fetch you results at this time"
        
################################## 06.Approval Rate Trend for PA ####################################

def getApprovalRateTrendPA(time_tuple=None,by=None):
    if time_tuple!=None and by==None:
        try:
            result_dict = OrderedDict()
            myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")
            mydb = myclient["HandsFreeAnalytics"]
            from_dt = datetime.strptime(time_tuple[0],'%Y-%m-%d')
            to_dt = datetime.strptime(time_tuple[1],'%Y-%m-%d')
            mycol = mydb["HSR_Data"]
            mydoc_total = mycol.find({'creat_dttm':{'$gte':from_dt,'$lt':to_dt}},{'creat_dttm':1,'hsc_id':1})
            pa_volume_total = []
            for x in mydoc_total:
                pa_volume_total.append((x['creat_dttm'].strftime("%Y-%m-%d"),x['hsc_id']))
            pa_total_count = pd.DataFrame(pa_volume_total,columns = ['create_date','hsc_id'])
            gp_data = pd.DataFrame(pa_total_count.groupby('create_date')['hsc_id'].nunique())
            gp_data.index = [datetime.strptime(i,"%Y-%m-%d").strftime("%B %Y") for i in gp_data.index]
            gp_data['date'] = gp_data.index
            gp_data = gp_data.reset_index(level=0,drop=True)
            gp_data = gp_data[['date','hsc_id']]
            result_total = gp_data.groupby('date',sort=False)['hsc_id'].sum()
            mydoc = mycol.find({'creat_dttm':{'$gte':from_dt,'$lt':to_dt},'outcome':'Approved'},{'creat_dttm':1,'hsc_id':1})
            pa_volume = []
            for x in mydoc:
                pa_volume.append((x['creat_dttm'].strftime("%Y-%m-%d"),x['hsc_id']))
            df_pa_volume = pd.DataFrame(pa_volume,columns=['create_date','hsc_id'])
            grouped_data = pd.DataFrame(df_pa_volume.groupby('create_date')['hsc_id'].nunique())
            grouped_data.index = [datetime.strptime(i,"%Y-%m-%d").strftime("%B %Y") for i in grouped_data.index]
            grouped_data['date'] = grouped_data.index
            grouped_data = grouped_data.reset_index(level=0,drop=True)
            grouped_data = grouped_data[['date','hsc_id']]
            result = grouped_data.groupby('date',sort=False)['hsc_id'].sum()
            result_dict['From'] = str(pd.Timestamp(time_tuple[0]))
            result_dict['End'] = str(pd.Timestamp(time_tuple[1]))
            result_dict['Title'] = "PA Approval Rate Trend"
            result_dict["Graph Type"] = "Line"
            result_dict["Header"] = ['-'.join([x.split(' ')[0][:3],x.split(' ')[1][-2:]]) for x in result.index.tolist()]
            result_dict['Value'] = list(np.divide(result.values.tolist(),result_total.values.tolist()))
            result_dict['Value'] = [round(x,2) for x in result_dict['Value']]
            return (dict(result_dict))
        except Exception as e:
            print (str(e))
            return "Sorry, Could not fetch you results at this time"
    elif time_tuple==None and by!= None:
        try:
            result_dict = OrderedDict()
            byDict = {'srvc_setting_typ':'Service Setting Type',
                      'srvc_desc_typ':'Service Type',
                      'lob':'lob',
                      'service_category':'Service Category',
                      'tat_hrs':'tat'}
            myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")
            mydb = myclient["HandsFreeAnalytics"]
            mycol = mydb["HSR_Data"]
            z = '$' + by
            mydoc1 = mycol.aggregate([{'$group':{"_id":z,"cIds":{'$addToSet':"$hsc_id"}}},
                                     {'$project':{by:"$_id","_id":0,"hsc_Ids":{'$size':"$cIds"}}}])
            byAgg_total = []
            for x in mydoc1:
                byAgg_total.append([x[by],x['hsc_Ids']])
            mydoc = mycol.aggregate([{'$match':{'outcome':'Approved'}},{'$group':{"_id":z,"cIds":{'$addToSet':"$hsc_id"}}},
                                     {'$project':{by:"$_id","_id":0,"hsc_Ids":{'$size':"$cIds"}}}])
            byAgg = []         
            for x in mydoc:
                byAgg.append([x[by],x['hsc_Ids']])
            result_dict['From'] = ""
            result_dict['End'] = ""
            result_dict['Title'] = "PA Approval Rate by " + byDict[by].upper()
            result_dict["Graph Type"] = "Bar"
            result_dict["Header"] = [f[0] for f in byAgg]
            result_dict["Value"] = [dict(byAgg)[f]/dict(byAgg_total)[f] for f in result_dict['Header']]
            result_dict['Value'] = [round(x,2) for x in result_dict['Value']]
            return (dict(result_dict))
        except Exception as e:
            print (str(e))
            return "Sorry, Could not fetch you results at this time"
    elif time_tuple!=None and by!=None:
        try:
            result_dict = OrderedDict()
            byDict = {'srvc_setting_typ':'Service Setting Type',
                      'srvc_desc_typ':'Service Type',
                      'lob':'lob',
                      'service_category':'Service Category',
                      'tat_hrs':'tat'}
            myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")
            mydb = myclient["HandsFreeAnalytics"]
            from_dt = datetime.strptime(time_tuple[0],'%Y-%m-%d')
            to_dt = datetime.strptime(time_tuple[1],'%Y-%m-%d')
            mycol = mydb["HSR_Data"]
            z = '$' + by
            mydoc1 = mycol.aggregate([{'$group':{"_id":z,"cIds":{'$addToSet':"$hsc_id"}}},
                                     {'$project':{by:"$_id","_id":0,"hsc_Ids":{'$size':"$cIds"}}}])
            byAgg_total = []
            for x in mydoc1:
                byAgg_total.append([x[by],x['hsc_Ids']])
            mydoc = mycol.aggregate([{'$match':{'creat_dttm':{'$gte':from_dt,'$lt':to_dt},'outcome':'Approved'}},{'$group':{"_id":z,"cIds":{'$addToSet':"$hsc_id"}}},
                                     {'$project':{by:"$_id","_id":0,"hsc_Ids":{'$size':"$cIds"}}}])
            byAgg = []         
            for x in mydoc:
                byAgg.append([x[by],x['hsc_Ids']])
            result_dict['From'] = ""
            result_dict['End'] = ""
            result_dict['Title'] = "PA Denial Rate by " + byDict[by].upper()
            result_dict["Graph Type"] = "Bar"
            result_dict["Header"] = [f[0] for f in byAgg]
            result_dict["Value"] = [dict(byAgg)[f]/dict(byAgg_total)[f] for f in result_dict['Header']]
            result_dict['Value'] = [round(x,2) for x in result_dict['Value']]
            return (dict(result_dict))
        except Exception as e:
            print (str(e))
            return "Sorry, Could not fetch you results at this time"

##################################7. show Denial Reasons#######################################

def showDenialReasons(time_tuple=None,by=None,chart=None):
    if time_tuple!=None and by==None:
        try:
            result_dict = OrderedDict()
            myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")
            mydb = myclient["HandsFreeAnalytics"]
            from_dt = datetime.strptime(time_tuple[0],'%Y-%m-%d')
            to_dt = datetime.strptime(time_tuple[1],'%Y-%m-%d')
            mycol = mydb["HSR_Data"]
            mydoc = mycol.find({'creat_dttm':{'$gte':from_dt,'$lt':to_dt},'outcome':'Denied'},{'creat_dttm':1,'outcome_reason':1})
            pa_volume = []
            for x in mydoc:
                pa_volume.append((x['creat_dttm'].strftime("%Y-%m-%d"),x['outcome_reason']))
            df_pa_volume = pd.DataFrame(pa_volume,columns=['create_date','outcome_reason'])
            grouped_data = pd.DataFrame(df_pa_volume.groupby(['create_date','outcome_reason'])['outcome_reason'].nunique())
            grouped_data.columns = ['Value']
            grouped_data = grouped_data.reset_index()
            grouped_data = grouped_data.set_index('create_date')
            grouped_data.index = [datetime.strptime(i,"%Y-%m-%d").strftime("%B %Y") for i in grouped_data.index]
            grouped_data['date'] = grouped_data.index
            grouped_data = grouped_data.reset_index(level=0,drop=True)
            grouped_data = grouped_data[['date','outcome_reason','Value']]
            result = grouped_data.groupby(['date','outcome_reason'],sort=False)['Value'].sum()
            test_data = pd.DataFrame(result).reset_index()
            test_data.columns = ['date','reason','value']
            dates = result.index.get_level_values('date').unique().tolist()
            result_dict['From'] = str(pd.Timestamp(time_tuple[0]))
            result_dict['End'] = str(pd.Timestamp(time_tuple[1]))
            result_dict['Title'] = "PA Denial Reasons"
            result_dict["Graph Type"] = "Bar_Requested" if chart=="bar_chart_requested" else "Stacked Bar"
            if chart=="bar_chart_requested":
                result_dict["Header"] = test_data[['reason','value']].groupby('reason')['value'].sum().index.tolist()
                result_dict['Value'] = test_data[['reason','value']].groupby('reason')['value'].sum().values.tolist()
            else:
                result_dict["Header"] = ['-'.join([x.split(' ')[0][:3],x.split(' ')[1][-2:]]) for x in dates]
                result_dict['Value'] = [test_data[test_data['date']==d][['reason','value']].values.tolist() for d in dates]
            return (dict(result_dict))
        except Exception as e:
            print (str(e))
            return "Sorry, Could not fetch you results at this time"
    if time_tuple==None and by!=None:
        try:
            result_dict = OrderedDict()
            byDict = {'srvc_setting_typ':'Service Setting Type',
                      'srvc_desc_typ':'Service Type',
                      'lob':'lob',
                      'service_category':'Service Category',
                      'tat_hrs':'tat'}
            myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")
            mydb = myclient["HandsFreeAnalytics"]
            mycol = mydb["HSR_Data"]
            mydoc = mycol.find({'outcome':'Denied'},{by:1,'outcome_reason':1})
            pa_volume = []
            for x in mydoc:
                pa_volume.append((x[by],x['outcome_reason']))
            df_pa_volume = pd.DataFrame(pa_volume,columns=[by,'outcome_reason'])
            grouped_data = pd.DataFrame(df_pa_volume.groupby([by,'outcome_reason'])['outcome_reason'].nunique())
            grouped_data.columns = ['Value']
            test_data = pd.DataFrame(grouped_data).reset_index()
            test_data.columns = [by,'reason','value']
            pms = grouped_data.index.get_level_values(by).unique().tolist()
            result_dict['From'] = ""
            result_dict['End'] = ""
            result_dict['Title'] = "PA Denial Reasons by " + byDict[by].upper()
            result_dict["Graph Type"] = "Bar"
            result_dict["Header"] = test_data[[by,'value']].groupby(by)['value'].sum().index.tolist()
            result_dict['Value'] = test_data[[by,'value']].groupby(by)['value'].sum().values.tolist()
            return (dict(result_dict))
        except Exception as e:
            print (str(e))
            return "Sorry, Could not fetch you results at this time"
    if time_tuple!=None and by!=None:
        try:
            result_dict = OrderedDict()
            byDict = {'srvc_setting_typ':'Service Setting Type',
                      'srvc_desc_typ':'Service Type',
                      'lob':'lob',
                      'service_category':'Service Category',
                      'tat_hrs':'tat'}
            myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")
            mydb = myclient["HandsFreeAnalytics"]
            from_dt = datetime.strptime(time_tuple[0],'%Y-%m-%d')
            to_dt = datetime.strptime(time_tuple[1],'%Y-%m-%d')
            mycol = mydb["HSR_Data"]
            mydoc = mycol.find({'creat_dttm':{'$gte':from_dt,'$lt':to_dt},'outcome':'Denied'},{by:1,'outcome_reason':1})
            pa_volume = []
            for x in mydoc:
                pa_volume.append((x[by],x['outcome_reason']))
            df_pa_volume = pd.DataFrame(pa_volume,columns=[by,'outcome_reason'])
            grouped_data = pd.DataFrame(df_pa_volume.groupby([by,'outcome_reason'])['outcome_reason'].nunique())
            grouped_data.columns = ['Value']
            test_data = pd.DataFrame(grouped_data).reset_index()
            test_data.columns = [by,'reason','value']
            pms = grouped_data.index.get_level_values(by).unique().tolist()
            result_dict['From'] = str(pd.Timestamp(time_tuple[0]))
            result_dict['End'] = str(pd.Timestamp(time_tuple[1]))
            result_dict['Title'] = "PA Denial Reasons by " + byDict[by].upper()
            result_dict["Graph Type"] = "Bar"
            result_dict["Header"] = test_data[[by,'value']].groupby(by)['value'].sum().index.tolist()
            result_dict['Value'] = test_data[[by,'value']].groupby(by)['value'].sum().values.tolist()
            return (dict(result_dict))
        except Exception as e:
            print (str(e))
            return "Sorry, Could not fetch you results at this time"
        
#######################################8. show Cancellation Reasons ######################################

def showCancelReasons(time_tuple=None,by=None,chart=None):
    if time_tuple!=None and by==None:
        try:
            result_dict = OrderedDict()
            myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")
            mydb = myclient["HandsFreeAnalytics"]
            from_dt = datetime.strptime(time_tuple[0],'%Y-%m-%d')
            to_dt = datetime.strptime(time_tuple[1],'%Y-%m-%d')
            mycol = mydb["HSR_Data"]
            mydoc = mycol.find({'creat_dttm':{'$gte':from_dt,'$lt':to_dt},'outcome':'Cancelled'},{'creat_dttm':1,'outcome_reason':1})
            pa_volume = []
            for x in mydoc:
                pa_volume.append((x['creat_dttm'].strftime("%Y-%m-%d"),x['outcome_reason']))
            df_pa_volume = pd.DataFrame(pa_volume,columns=['create_date','outcome_reason'])
            grouped_data = pd.DataFrame(df_pa_volume.groupby(['create_date','outcome_reason'])['outcome_reason'].nunique())
            grouped_data.columns = ['Value']
            grouped_data = grouped_data.reset_index()
            grouped_data = grouped_data.set_index('create_date')
            grouped_data.index = [datetime.strptime(i,"%Y-%m-%d").strftime("%B %Y") for i in grouped_data.index]
            grouped_data['date'] = grouped_data.index
            grouped_data = grouped_data.reset_index(level=0,drop=True)
            grouped_data = grouped_data[['date','outcome_reason','Value']]
            result = grouped_data.groupby(['date','outcome_reason'],sort=False)['Value'].sum()
            test_data = pd.DataFrame(result).reset_index()
            test_data.columns = ['date','reason','value']
            dates = result.index.get_level_values('date').unique().tolist()
            result_dict['From'] = str(pd.Timestamp(time_tuple[0]))
            result_dict['End'] = str(pd.Timestamp(time_tuple[1]))
            result_dict['Title'] = "PA Cancellation Reasons"
            result_dict["Graph Type"] = "Bar_Requested" if chart=="bar_chart_requested" else "Stacked Bar"
            if chart=="bar_chart_requested":
                result_dict["Header"] = test_data[['reason','value']].groupby('reason')['value'].sum().index.tolist()
                result_dict['Value'] = test_data[['reason','value']].groupby('reason')['value'].sum().values.tolist()
            else:
                result_dict["Header"] = ['-'.join([x.split(' ')[0][:3],x.split(' ')[1][-2:]]) for x in dates]
                result_dict['Value'] = [test_data[test_data['date']==d][['reason','value']].values.tolist() for d in dates]
            return (dict(result_dict))
        except Exception as e:
            print (str(e))
            return "Sorry, Could not fetch you results at this time"
    if time_tuple==None and by!=None:
        try:
            result_dict = OrderedDict()
            byDict = {'srvc_setting_typ':'Service Setting Type',
                      'srvc_desc_typ':'Service Type',
                      'lob':'lob',
                      'service_category':'Service Category',
                      'tat_hrs':'tat'}
            myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")
            mydb = myclient["HandsFreeAnalytics"]
            mycol = mydb["HSR_Data"]
            mydoc = mycol.find({'outcome':'Cancelled'},{by:1,'outcome_reason':1})
            pa_volume = []
            for x in mydoc:
                pa_volume.append((x[by],x['outcome_reason']))
            df_pa_volume = pd.DataFrame(pa_volume,columns=[by,'outcome_reason'])
            grouped_data = pd.DataFrame(df_pa_volume.groupby([by,'outcome_reason'])['outcome_reason'].nunique())
            grouped_data.columns = ['Value']
            test_data = pd.DataFrame(grouped_data).reset_index()
            test_data.columns = [by,'reason','value']
            pms = grouped_data.index.get_level_values(by).unique().tolist()
            result_dict['From'] = ""
            result_dict['End'] = ""
            result_dict['Title'] = "PA Cancellation Reasons by " + byDict[by].upper()
            result_dict["Graph Type"] = "Bar"
            result_dict["Header"] = test_data[[by,'value']].groupby(by)['value'].sum().index.tolist()
            result_dict['Value'] = test_data[[by,'value']].groupby(by)['value'].sum().values.tolist()
            return (dict(result_dict))
        except Exception as e:
            print (str(e))
            return "Sorry, Could not fetch you results at this time"
    if time_tuple!=None and by!=None:
        try:
            result_dict = OrderedDict()
            byDict = {'srvc_setting_typ':'Service Setting Type',
                      'srvc_desc_typ':'Service Type',
                      'lob':'lob',
                      'service_category':'Service Category',
                      'tat_hrs':'tat'}
            myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")
            mydb = myclient["HandsFreeAnalytics"]
            from_dt = datetime.strptime(time_tuple[0],'%Y-%m-%d')
            to_dt = datetime.strptime(time_tuple[1],'%Y-%m-%d')
            mycol = mydb["HSR_Data"]
            mydoc = mycol.find({'creat_dttm':{'$gte':from_dt,'$lt':to_dt},'outcome':'Cancelled'},{by:1,'outcome_reason':1})
            pa_volume = []
            for x in mydoc:
                pa_volume.append((x[by],x['outcome_reason']))
            df_pa_volume = pd.DataFrame(pa_volume,columns=[by,'outcome_reason'])
            grouped_data = pd.DataFrame(df_pa_volume.groupby([by,'outcome_reason'])['outcome_reason'].nunique())
            grouped_data.columns = ['Value']
            test_data = pd.DataFrame(grouped_data).reset_index()
            test_data.columns = [by,'reason','value']
            pms = grouped_data.index.get_level_values(by).unique().tolist()
            result_dict['From'] = str(pd.Timestamp(time_tuple[0]))
            result_dict['End'] = str(pd.Timestamp(time_tuple[1]))
            result_dict['Title'] = "PA Cancellation Reasons by " + byDict[by].upper()
            result_dict["Graph Type"] = "Bar"
            result_dict["Header"] = test_data[[by,'value']].groupby(by)['value'].sum().index.tolist()
            result_dict['Value'] = test_data[[by,'value']].groupby(by)['value'].sum().values.tolist()
            return (dict(result_dict))
        except Exception as e:
            print (str(e))
            return "Sorry, Could not fetch you results at this time"
        
        
######################################9. Approval Reasons###########################################

def showApprovalReasons(time_tuple=None,by=None,chart=None):
    if time_tuple!=None and by==None:
        try:
            result_dict = OrderedDict()
            myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")
            mydb = myclient["HandsFreeAnalytics"]
            from_dt = datetime.strptime(time_tuple[0],'%Y-%m-%d')
            to_dt = datetime.strptime(time_tuple[1],'%Y-%m-%d')
            mycol = mydb["HSR_Data"]
            mydoc = mycol.find({'creat_dttm':{'$gte':from_dt,'$lt':to_dt},'outcome':'Approved'},{'creat_dttm':1,'outcome_reason':1})
            pa_volume = []
            for x in mydoc:
                pa_volume.append((x['creat_dttm'].strftime("%Y-%m-%d"),x['outcome_reason']))
            df_pa_volume = pd.DataFrame(pa_volume,columns=['create_date','outcome_reason'])
            grouped_data = pd.DataFrame(df_pa_volume.groupby(['create_date','outcome_reason'])['outcome_reason'].nunique())
            grouped_data.columns = ['Value']
            grouped_data = grouped_data.reset_index()
            grouped_data = grouped_data.set_index('create_date')
            grouped_data.index = [datetime.strptime(i,"%Y-%m-%d").strftime("%B %Y") for i in grouped_data.index]
            grouped_data['date'] = grouped_data.index
            grouped_data = grouped_data.reset_index(level=0,drop=True)
            grouped_data = grouped_data[['date','outcome_reason','Value']]
            result = grouped_data.groupby(['date','outcome_reason'],sort=False)['Value'].sum()
            test_data = pd.DataFrame(result).reset_index()
            test_data.columns = ['date','reason','value']
            dates = result.index.get_level_values('date').unique().tolist()
            result_dict['From'] = str(pd.Timestamp(time_tuple[0]))
            result_dict['End'] = str(pd.Timestamp(time_tuple[1]))
            result_dict['Title'] = "PA Approval Reasons"
            result_dict["Graph Type"] = "Bar_Requested" if chart=="bar_chart_requested" else "Stacked Bar"
            if chart=="bar_chart_requested":
                result_dict["Header"] = test_data[['reason','value']].groupby('reason')['value'].sum().index.tolist()
                result_dict['Value'] = test_data[['reason','value']].groupby('reason')['value'].sum().values.tolist()
            else:
                result_dict["Header"] = ['-'.join([x.split(' ')[0][:3],x.split(' ')[1][-2:]]) for x in dates]
                result_dict['Value'] = [test_data[test_data['date']==d][['reason','value']].values.tolist() for d in dates]
            return (dict(result_dict))
        except Exception as e:
            print (str(e))
            return "Sorry, Could not fetch you results at this time"
    if time_tuple==None and by!=None:
        try:
            result_dict = OrderedDict()
            byDict = {'srvc_setting_typ':'Service Setting Type',
                      'srvc_desc_typ':'Service Type',
                      'lob':'lob',
                      'service_category':'Service Category',
                      'tat_hrs':'tat'}
            myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")
            mydb = myclient["HandsFreeAnalytics"]
            mycol = mydb["HSR_Data"]
            mydoc = mycol.find({'outcome':'Approved'},{by:1,'outcome_reason':1})
            pa_volume = []
            for x in mydoc:
                pa_volume.append((x[by],x['outcome_reason']))
            df_pa_volume = pd.DataFrame(pa_volume,columns=[by,'outcome_reason'])
            grouped_data = pd.DataFrame(df_pa_volume.groupby([by,'outcome_reason'])['outcome_reason'].nunique())
            grouped_data.columns = ['Value']
            test_data = pd.DataFrame(grouped_data).reset_index()
            test_data.columns = [by,'reason','value']
            pms = grouped_data.index.get_level_values(by).unique().tolist()
            result_dict['From'] = ""
            result_dict['End'] = ""
            result_dict['Title'] = "PA Approval Reasons by " + byDict[by].upper()
            result_dict["Graph Type"] = "Bar"
            result_dict["Header"] = test_data[[by,'value']].groupby(by)['value'].sum().index.tolist()
            result_dict['Value'] = test_data[[by,'value']].groupby(by)['value'].sum().values.tolist()
            return (dict(result_dict))
        except Exception as e:
            print (str(e))
            return "Sorry, Could not fetch you results at this time"
    if time_tuple!=None and by!=None:
        try:
            result_dict = OrderedDict()
            byDict = {'srvc_setting_typ':'Service Setting Type',
                      'srvc_desc_typ':'Service Type',
                      'lob':'lob',
                      'service_category':'Service Category',
                      'tat_hrs':'tat'}
            myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")
            mydb = myclient["HandsFreeAnalytics"]
            from_dt = datetime.strptime(time_tuple[0],'%Y-%m-%d')
            to_dt = datetime.strptime(time_tuple[1],'%Y-%m-%d')
            mycol = mydb["HSR_Data"]
            mydoc = mycol.find({'creat_dttm':{'$gte':from_dt,'$lt':to_dt},'outcome':'Approved'},{by:1,'outcome_reason':1})
            pa_volume = []
            for x in mydoc:
                pa_volume.append((x[by],x['outcome_reason']))
            df_pa_volume = pd.DataFrame(pa_volume,columns=[by,'outcome_reason'])
            grouped_data = pd.DataFrame(df_pa_volume.groupby([by,'outcome_reason'])['outcome_reason'].nunique())
            grouped_data.columns = ['Value']
            test_data = pd.DataFrame(grouped_data).reset_index()
            test_data.columns = [by,'reason','value']
            pms = grouped_data.index.get_level_values(by).unique().tolist()
            result_dict['From'] = str(pd.Timestamp(time_tuple[0]))
            result_dict['End'] = str(pd.Timestamp(time_tuple[1]))
            result_dict['Title'] = "PA Approval Reasons by " + byDict[by].upper()
            result_dict["Graph Type"] = "Bar"
            result_dict["Header"] = test_data[[by,'value']].groupby(by)['value'].sum().index.tolist()
            result_dict['Value'] = test_data[[by,'value']].groupby(by)['value'].sum().values.tolist()
            return (dict(result_dict))
        except Exception as e:
            print (str(e))
            return "Sorry, Could not fetch you results at this time"

#######################################END####################################################
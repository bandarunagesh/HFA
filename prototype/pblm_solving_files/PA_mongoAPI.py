# from pymongo import MongoClient
import pymongo
import datetime
import calendar
import ast
import random
import pandas as pd

GREETING_RESPONSES = ["hey", "Hi", "how can i help?","hello","what's up"]
GOODBYE_RESPONSES = ["bye", "cya", "take care", "good bye", "bye bye","Bye..Tc"]
AFFIRM_RESPONSES = ["indeed", "OK", "that's right", "great", "cool"]

def greeting():
    """If any of the words in the user's input was a greeting, return a greeting response"""
    return random.choice(GREETING_RESPONSES)

def goodbye():
    """If any of the words in the user's input was a goodbye, return a goddbye response"""
    return random.choice(GOODBYE_RESPONSES)

def affirm():
    """If any of the words in the user's input was a goodbye, return a goddbye response"""
    return random.choice(AFFIRM_RESPONSES)

##################################01. Get PA Status#################################
def getStatusPA(value):
    
    try:
        # print("get_status")
        claim_num_rec=str(value)
        # print(claim_num_rec)
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")
        mydb = myclient["HandsFreeAnalytics"]
        mycol = mydb["HSR_Data"]
        n_records=mycol.count_documents({"hsc_id": str(claim_num_rec)})
        n_denial_recds = mycol.count_documents({"hsc_id": str(claim_num_rec),"outcome":"Denied"})     
        n_approve_recds = mycol.count_documents({"hsc_id": str(claim_num_rec),"outcome":"Approved"})
        n_cancel_recds = mycol.count_documents({"hsc_id": str(claim_num_rec),"outcome":"Cancelled"})
        print(str(n_records)+"-"+str(n_denial_recds)+"-"+str(n_approve_recds)+"-"+str(n_cancel_recds))
        if n_records==n_denial_recds and n_records!=0:
            pipe = [{'$match':{"hsc_id":str(claim_num_rec)}},{'$group': {'_id':'$hsc_id', 'total': {'$max': {'$convert':{'input':'$decn_rndr_dttm','to':'date'}}}}}] ## sum after type conversion of field
            mydoc=(mycol.aggregate(pipeline=pipe))
            t="--"
            for x in mydoc:
                t=x['total'].strftime('%Y-%b-%d')   
            status="1}Your PA claim has been completely denied"+" on "+t.split('-')[2]+"th of "+t.split('-')[1] +", "+t.split('-')[0]
            # print(status)
            return (status.split('}')[1])
        elif n_records==n_approve_recds and n_records!=0:
            pipe = [{'$match':{"hsc_id":str(claim_num_rec)}},{'$group': {'_id':'$hsc_id', 'total': {'$max': {'$convert':{'input':'$decn_rndr_dttm','to':'date'}}}}}] ## sum after type conversion of field
            mydoc=(mycol.aggregate(pipeline=pipe))
            t="--"
            for x in mydoc:
                t=x['total'].strftime('%Y-%b-%d')
            status="2}Your PA claim has been approved"+" on "+t.split('-')[2]+"th of "+t.split('-')[1] +", "+t.split('-')[0]
            # print(status)
            return (status.split('}')[1])
        elif n_records==n_cancel_recds and n_records!=0:
            pipe = [{'$match':{"hsc_id":str(claim_num_rec)}},{'$group': {'_id':'$hsc_id', 'total': {'$max': {'$convert':{'input':'$decn_rndr_dttm','to':'date'}}}}}] ## sum after type conversion of field
            mydoc=(mycol.aggregate(pipeline=pipe))
            t="--"
            for x in mydoc:
                t=x['total'].strftime('%Y-%b-%d')
            status="3}Your PA claim has been cancelled"+" on "+t.split('-')[2]+"th of "+t.split('-')[1] +", "+t.split('-')[0]
            # print(status)
            return (status.split('}')[1])
        elif n_records==(n_approve_recds+n_cancel_recds) and n_records!=0:
            pipe = [{'$match':{"hsc_id":str(claim_num_rec)}},{'$group': {'_id':'$hsc_id', 'total': {'$max': {'$convert':{'input':'$decn_rndr_dttm','to':'date'}}}}}] ## sum after type conversion of field
            mydoc=(mycol.aggregate(pipeline=pipe))
            t="--"
            for x in mydoc:
                t=x['total'].strftime('%Y-%b-%d')
            status="4}Your PA claim has been approved"+" on "+t.split('-')[2]+"th of "+t.split('-')[1] +", "+t.split('-')[0]
            # print(status)
            return (status.split('}')[1])
        elif n_records==(n_approve_recds+n_denial_recds) and n_records!=0:
            pipe = [{'$match':{"hsc_id":str(claim_num_rec)}},{'$group': {'_id':'$hsc_id', 'total': {'$max': {'$convert':{'input':'$decn_rndr_dttm','to':'date'}}}}}] ## sum after type conversion of field
            mydoc=(mycol.aggregate(pipeline=pipe))
            t="--"
            for x in mydoc:
                t=x['total'].strftime('%Y-%b-%d')
            status="5}Your PA claim has been partially denied"+" on "+t.split('-')[2]+"th of "+t.split('-')[1] +", "+t.split('-')[0]
            # print(status)
            return (status.split('}')[1])
        elif n_records==(n_cancel_recds+n_denial_recds) and n_records!=0:
            pipe = [{'$match':{"hsc_id":str(claim_num_rec)}},{'$group': {'_id':'$hsc_id', 'total': {'$max': {'$convert':{'input':'$decn_rndr_dttm','to':'date'}}}}}] ## sum after type conversion of field
            mydoc=(mycol.aggregate(pipeline=pipe))
            t="--"
            for x in mydoc:
                t=x['total'].strftime('%Y-%b-%d')
            status="6}Your PA claim has been denied"+" on "+t.split('-')[2]+"th of "+t.split('-')[1] +", "+t.split('-')[0]
            # print(status)
            return (status.split('}')[1])
        elif n_records==0:
            status = "7}Could not find PA claim with Claim Number "+claim_num_rec+", Please make sure you entered correct details "
            return (status.split('}')[1])
        else:
            print(str(n_records))
            print(str(n_denial_recds))
            print(str(n_approve_recds))
            print(str(n_cancel_recds))
    except Exception as e:
        print(str(e))
        return "Sorry, Could not fetch you results at this time"
        
########################02. Get PA Requested Date#########################       
def getRequestSubmittedDate(value):
    
    try:
        claim_num_rec=str(value)
        # print(claim_num_rec)
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")
        mydb = myclient["HandsFreeAnalytics"]
        mycol = mydb["HSR_Data"]
        pipe = [{'$match':{"hsc_id":str(claim_num_rec)}},{'$group': {'_id':'$hsc_id', 'total': {'$min': {'$convert':{'input':'$creat_dttm','to':'date'}}}}}] ## sum after type conversion of field
        mydoc=(mycol.aggregate(pipeline=pipe))
        t='--'
        for x in mydoc:
            t=x['total'].strftime('%Y-%b-%d')
        reqDateResp = "The PA was requested on " + t.split('-')[2]+"th of "+t.split('-')[1] +", "+t.split('-')[0]
        return (reqDateResp)
    except Exception as e:
        print(str(e))
        return "Sorry, Could not fetch you results at this time"
            
########################03. GET PA Decision Date###########################    

def getDecisionDate(value):
    
    try:
        claim_num_rec=str(value)
        # print(claim_num_rec)
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")
        mydb = myclient["HandsFreeAnalytics"]
        mycol = mydb["HSR_Data"]
        pipe = [{'$match':{"hsc_id":str(claim_num_rec)}},{'$group': {'_id':'$hsc_id', 'total': {'$max': {'$convert':{'input':'$decn_rndr_dttm','to':'date'}}}}}] ## sum after type conversion of field
        mydoc=(mycol.aggregate(pipeline=pipe))
        t='--'
        for x in mydoc:
            t=x['total'].strftime('%Y-%b-%d')
        decisionDateResp = "The decision on PA request was made on " + t.split('-')[2]+"th of "+t.split('-')[1] +", "+t.split('-')[0]
        return (decisionDateResp)
    except Exception as e:
        print (str(e))
        return "Sorry, Could not fetch you results at this time"

#########################04. Get Service Setting of PA##########################

def getServiceSettingType(value):
    
    try:
        claim_num_rec = str(value)
        # print(claim_num_rec)
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")
        mydb = myclient["HandsFreeAnalytics"]
        mycol = mydb["HSR_Data"]
        n_Outpatient_recds = mycol.count_documents({"hsc_id": str(claim_num_rec),"srvc_setting_typ":"Outpatient"})
        n_Inpatient_recds = mycol.count_documents({"hsc_id": str(claim_num_rec),"srvc_setting_typ":"Inpatient"})
        n_Out_Facility_recds = mycol.count_documents({"hsc_id": str(claim_num_rec),"srvc_setting_typ":"Outpatient Facility"})
        if n_Outpatient_recds > 0 & n_Inpatient_recds == 0 & n_Out_Facility_recds == 0:
            serviceTypeResp = "It is an Outpatient Prior Auth"
            return (serviceTypeResp)
        elif n_Inpatient_recds > 0 & n_Outpatient_recds == 0 & n_Out_Facility_recds == 0:
            serviceTypeResp = "It is an Inpatient Prior Auth"
            return (serviceTypeResp)
        elif n_Out_Facility_recds > 0 & n_Inpatient_recds == 0 & n_Outpatient_recds == 0:
            serviceTypeResp = "It is an Outpatient Facility Prior Auth"
            return (serviceTypeResp)
        else:
            print (n_Outpatient_recds)
            print (n_Inpatient_recds)
            print (n_Out_Facility_recds)
    except Exception as e:
        print (str(e))
        return "Sorry, Could not fetch you results at this time"
            
######################05. Get LOB for PA############################

def getLOBPA(value):
    
    try:
        claim_num_rec = str(value)
        # print(claim_num_rec)
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")
        mydb = myclient["HandsFreeAnalytics"]
        mycol = mydb["HSR_Data"]
        mydoc = mycol.find({"hsc_id":str(claim_num_rec)},{'lob':1})
        lobList = []
        for x in mydoc:
            lobList.append(x['lob'])
        mylob = lobList[0]
        lobResp = "The PA belongs to " + mylob + " Line of Business"
        return (lobResp)
    except Exception as e:
        print (str(e))
        return "Sorry, Could not fetch you results at this time"
    
######################06. Get Reasons for Denial#####################

def getReasonsDenials(value):
    
    try:
        claim_num_rec = str(value)
        # print(claim_num_rec)
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")
        mydb = myclient["HandsFreeAnalytics"]
        mycol = mydb["HSR_Data"]
        mydoc = mycol.find({'hsc_id':str(claim_num_rec),'outcome':'Denied'},{'outcome_reason':1})
        if mydoc.count()!=0:
            mydoc1 = mycol.find({'hsc_id':str(claim_num_rec),'outcome':'Denied'},{'outcome_reason':1})
            denialReasons = []
            for x in mydoc1:
                denialReasons.append(x['outcome_reason'])
            denialReasons = list(set(denialReasons))
            denialReasons = "|".join(denialReasons)
            return ("PA request got denied due to the following reasons - " + denialReasons)
        else:
            return ("There are no denials for this hsc Id")
    except Exception as e:
        print (str(e))
        return "Sorry, Could not fetch you results at this time"
    
##########################07. Get TAX ID of the provider################################

def getTaxID(value):
    
    try:
        claim_num_rec = str(value)
        # print(claim_num_rec)
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")
        mydb = myclient["HandsFreeAnalytics"]
        mycol = mydb["HSR_Data"]
        mydoc = mycol.find({'hsc_id':str(claim_num_rec)},{'prov_tax_id':1})
        taxIds = []
        for x in mydoc:
            taxIds.append(x['prov_tax_id'])
        taxIds = list(set(taxIds))
        taxIds = "|".join(taxIds)
        return ("The TAX ID(s) of Provider associated with PA request is/are " + taxIds)
    except Exception as e:
        print (str(e))
        return "Sorry, Could not fetch you results at this time"
    
#############################08. Get Line Items of PA request#############################

def getLineItems(value):
    try:
        claim_num_rec = str(value)
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")
        mydb = myclient["HandsFreeAnalytics"]
        mycol = mydb["HSR_Data"]
        numRecords = mycol.count_documents({'hsc_id':str(claim_num_rec)})
        return ("The PA request has " + str(numRecords) + " line items")
    except Exception as e:
        print (str(e))
        return "Sorry, Could not fetch you results at this time"
    
##############################09. Get Service Type of PA################################

def getServiceType(value):
    
    try:
        claim_num_rec = str(value)
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")
        mydb = myclient["HandsFreeAnalytics"]
        mycol = mydb["HSR_Data"]
        mydoc = mycol.find({'hsc_id':str(claim_num_rec)},{'srvc_desc_typ':1})
        serviceTypes = []
        for x in mydoc:
            serviceTypes.append(x['srvc_desc_typ'])
        serviceTypes = list(set(serviceTypes))
        if len(serviceTypes)==2:
            return ("The PA includes both Standard and Urgent type of requests")
        elif len(serviceTypes)==1 and serviceTypes[0]=="Standard":
            return ("This is a standard type of PA request")
        elif len(serviceTypes)==1 and serviceTypes[0]==" Urgent":
            return ("This is a urgent type of PA request")
    except Exception as e:
        print (str(e))
        return "Sorry, Could not fetch you results at this time"
        
############################10. Get Service Category of PA##############################

def getServiceCategory(value):
    
    try:
        claim_num_rec = str(value)
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")
        mydb = myclient["HandsFreeAnalytics"]
        mycol = mydb["HSR_Data"]
        mydoc = mycol.find({'hsc_id':str(claim_num_rec)},{'service_category':1})
        servCategs = []
        for x in mydoc:
            servCategs.append(x['service_category'])
        servCategs = list(set(servCategs))
        servCategs = "|".join(servCategs)
        if len(servCategs)==1:
            return ("This PA belongs to " + servCategs)
        else:
            return ("This PA belongs to following service categories - " + servCategs)
    except Exception as e:
        print (str(e))
        return "Sorry, Could not fetch you results at this time"
    
#########################   11. Get turnaround time PA   ###########################

def getTATPA(value):
    
    try:
        claim_num_rec = str(value)
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")
        mydb = myclient["HandsFreeAnalytics"]
        mycol = mydb["HSR_Data"]
        mydoc = mycol.find({'hsc_id':str(claim_num_rec)},{'srvc_desc_typ':1,'tat_hrs':1})
        pairs = []
        for x in mydoc:
            pairs.append((x['srvc_desc_typ'],float(x['tat_hrs'])))
        mydata = pd.DataFrame(pairs,columns = ['service_type','tat'])
        if len(mydata.groupby('service_type')['tat'].max().index)==2:
            standard_tat = str(mydata.groupby('service_type')['tat'].max().loc['Standard'])
            urgent_tat = str(mydata.groupby('service_type')['tat'].max().loc[' Urgent'])
            return ("The Standard service took " + standard_tat + ", & the Urgent service took " + urgent_tat)
        if len(mydata.groupby('service_type')['tat'].max().index)==1:
            service = mydata.groupby('service_type')['tat'].max().index[0]
            if service == "Standard":
                stand_tat = str(mydata.groupby('service_type')['tat'].max().loc['Standard'])
                stand_tat = str(round(float(stand_tat),2))
                return ("The PA took " + stand_tat + " for (Standard PA)")
            else:
                ugen_tat = str(mydata.groupby('service_type')['tat'].max().loc[' Urgent'])
                ugen_tat = str(round(float(ugen_tat),2))
                return ("The PA took " + ugen_tat + " for (Urgent PA)")
    except Exception as e:
        print (str(e))
        return "Sorry, Could not fetch you results at this time"
        
#####################################12. Get reasons for cancellations################################

def getCancelReasons(value):
    
    try:
        claim_num_rec = str(value)
        # print(claim_num_rec)
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")
        mydb = myclient["HandsFreeAnalytics"]
        mycol = mydb["HSR_Data"]
        mydoc = mycol.find({'hsc_id':str(claim_num_rec),'outcome':'Cancelled'},{'outcome_reason':1})
        if mydoc.count()!=0:
            mydoc1 = mycol.find({'hsc_id':str(claim_num_rec),'outcome':'Cancelled'},{'outcome_reason':1})
            cancelReasons = []
            for x in mydoc1:
                cancelReasons.append(x['outcome_reason'])
            cancelReasons = list(set(cancelReasons))
            cancelReasons = "|".join(cancelReasons)
            return ("PA request got cancelled due to the following reasons - " + cancelReasons)
        else:
            return ("There are no cancellations for this hsc Id")
    except Exception as e:
        print (str(e))
        return "Sorry, Could not fetch you results at this time"

#####################################13. Get reasons for Approvals################################

def getApprovalReasons(value):
    
    try:
        claim_num_rec = str(value)
        # print(claim_num_rec)
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")
        mydb = myclient["HandsFreeAnalytics"]
        mycol = mydb["HSR_Data"]
        mydoc = mycol.find({'hsc_id':str(claim_num_rec),'outcome':'Approved'},{'outcome_reason':1})
        if mydoc.count()!=0:
            mydoc1 = mycol.find({'hsc_id':str(claim_num_rec),'outcome':'Approved'},{'outcome_reason':1})
            approveReasons = []
            for x in mydoc1:
                approveReasons.append(x['outcome_reason'])
            approveReasons = list(set(approveReasons))
            approveReasons = "|".join(approveReasons)
            return ("PA request got approved due to the following reasons - " + approveReasons)
        else:
            return ("There are no approvals for this hsc Id")
    except Exception as e:
        print (str(e))
        return "Sorry, Could not fetch you results at this time"
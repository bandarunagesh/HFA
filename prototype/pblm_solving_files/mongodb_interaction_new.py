# from pymongo import MongoClient
import pymongo
import datetime
import calendar
import ast
import random
from pblm_solving_files.mongodb_interaction_srch import *

coll_name="hfa_claims_1819_20190619"
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

def get_status(value1):

    try:
        
        # print("get_status")        
        claim_num_rec=str(value1)
        print(claim_num_rec)
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
        mydoc = mycol.find({"root_claim_num": str(claim_num_rec)})
        n_records=(str(mydoc.count()))
        mydoc = mycol.find({"root_claim_num": str(claim_num_rec),"claim_denial_ind":"1"})
        n_denial_recds=(str(mydoc.count()))        
        mydoc = mycol.find({"root_claim_num": str(claim_num_rec),"claim_adj_ind":"1"})
        n_adj_recds=(str(mydoc.count())) 
        print(str(n_records)+"-"+str(n_adj_recds)+"-"+str(n_denial_recds))
        if int(n_records)==int(n_denial_recds) and int(n_records)!=0:
            pipe = [{'$match':{"root_claim_num":str(claim_num_rec)}},{'$group': {'_id':'$root_claim_num', 'total': {'$sum': {'$convert':{'input':'$amt_billed','to':'double'}}}}}] ## sum after type conversion of field
            mydoc=(mycol.aggregate(pipeline=pipe))            
            denial_amt=""
            for x in mydoc:
                denial_amt=x['total']
            denial_amt=str(denial_amt)
            # print(denial_amt)
            pipe = [{'$match':{"root_claim_num":str(claim_num_rec)}},{'$group': {'_id':'$root_claim_num', 'total': {'$max': {'$convert':{'input':'$received_date_str','to':'date'}}}}}] ## sum after type conversion of field
            mydoc=(mycol.aggregate(pipeline=pipe))            
            t="--"
            for x in mydoc:
                t=x['total'].strftime('%Y-%b-%d')   
            status="1}Your claim has been completely denied for the amount "+denial_amt+" on "+t.split('-')[2]+"th of "+t.split('-')[1] +", "+t.split('-')[0]+"!Denial Reason!Revise and Resubmit!TAT!Submission Mode"
            # print(status)
            return(status)
        elif int(n_denial_recds)==0 and int(n_adj_recds)==0 and int(n_records)!=0:
            pipe = [{'$match':{"root_claim_num":str(claim_num_rec)}},{'$group': {'_id':'$root_claim_num', 'total': {'$sum': {'$convert':{'input':'$amt_paid','to':'double'}}}}}] ## sum after type conversion of field
            mydoc=(mycol.aggregate(pipeline=pipe))            
            paid_amt=""
            for x in mydoc:
                paid_amt=x['total']
            paid_amt=str(paid_amt)
            # print(denial_amt)
            pipe = [{'$match':{"root_claim_num":str(claim_num_rec)}},{'$group': {'_id':'$root_claim_num', 'total': {'$max': {'$convert':{'input':'$paid_date_str','to':'date'}}}}}] ## sum after type conversion of field
            mydoc=(mycol.aggregate(pipeline=pipe))            
            t="--"
            for x in mydoc:
                t=x['total'].strftime('%Y-%b-%d') 
            status="2}Your claim has been completely paid for the amount "+paid_amt+" on "+t.split('-')[2]+"th of "+t.split('-')[1] +", "+t.split('-')[0]+"!Claim Type!Paid Date!TAT!Submission Mode"
            # print(status)
            return(status)
        elif int(n_denial_recds)==0 and int(n_adj_recds) > 0 and int(n_records)!=0:
            pipe = [{'$match':{"root_claim_num":str(claim_num_rec)}},{'$group': {'_id':'$root_claim_num', 'total': {'$sum': {'$convert':{'input':'$amt_paid','to':'double'}}}}}] ## sum after type conversion of field
            mydoc=(mycol.aggregate(pipeline=pipe))            
            paid_amt=""
            for x in mydoc:
                paid_amt=x['total']
            paid_amt=str(paid_amt)
            # print(denial_amt)
            pipe = [{'$match':{"root_claim_num":str(claim_num_rec)}},{'$group': {'_id':'$root_claim_num', 'total': {'$max': {'$convert':{'input':'$paid_date_str','to':'date'}}}}}] ## sum after type conversion of field
            mydoc=(mycol.aggregate(pipeline=pipe))            
            t="--"
            for x in mydoc:
                t=x['total'].strftime('%Y-%b-%d') 
            status="3}Your claim has been paid for the amount "+paid_amt+" on "+t.split('-')[2]+"th of "+t.split('-')[1] +", "+t.split('-')[0]+" with adjustments"+"!Adjustment Reason!Claim Type!TAT!Submission Mode"            # print(status)
            return(status)
        elif int(n_denial_recds)>0 and int(n_records)!=0:
            pipe = [{'$match':{"root_claim_num":str(claim_num_rec)}},{'$group': {'_id':'$root_claim_num', 'total': {'$sum': {'$convert':{'input':'$amt_billed','to':'double'}}}}}] ## sum after type conversion of field
            mydoc=(mycol.aggregate(pipeline=pipe))            
            billed_amt=""
            for x in mydoc:
                billed_amt=x['total']
            billed_amt=str(billed_amt)
            pipe = [{'$match':{"root_claim_num":str(claim_num_rec)}},{'$group': {'_id':'$root_claim_num', 'total': {'$sum': {'$convert':{'input':'$amt_paid','to':'double'}}}}}] ## sum after type conversion of field
            mydoc=(mycol.aggregate(pipeline=pipe))            
            paid_amt=""
            for x in mydoc:
                paid_amt=x['total']
            paid_amt=str(paid_amt)
            # print(denial_amt)
            pipe = [{'$match':{"root_claim_num":str(claim_num_rec)}},{'$group': {'_id':'$root_claim_num', 'total': {'$max': {'$convert':{'input':'$paid_date_str','to':'date'}}}}}] ## sum after type conversion of field
            mydoc=(mycol.aggregate(pipeline=pipe))            
            t="--"
            for x in mydoc:
                t=x['total'].strftime('%Y-%b-%d') 
            denied_amt=str(float(billed_amt)-float(paid_amt))
            status="4}Your claim has been partially denied with "+str(denied_amt) +" being denied out of "+str(billed_amt)+" on "+t.split('-')[2]+"th of "+t.split('-')[1] +", "+t.split('-')[0]+"!Denial Reason!Revise and Resubmit!TAT!Submission Mode"
            # print(status)
            return(status)
        elif int(n_records)==0:
            # print("5")
            status_ind=5
            status="5}Could not find claim with Claim Number "+claim_num_rec+", Please make sure you entered correct details "
            # print(status)
            return(status)
        else:
            print(str(n_records))
            print(str(n_adj_recds))
            print(str(n_denial_recds))

       
    except Exception as e:
        print(str(e))
        return "Sorry, Could not fetch you results at this time"

def get_line_items(value1):

    try:
        
        claim_num_rec=str(value1)        
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
        mydoc = mycol.find({"root_claim_num": str(claim_num_rec)})
        n_records=(str(mydoc.count()))
        print(n_records)
        if int(n_records) > 0:
            pipe = [{'$match':{"root_claim_num":str(claim_num_rec)}},{'$group': {'_id':'$root_claim_num', 'total': {'$max': {'$convert':{'input':'$line_num','to':'int'}}}}}] ## sum after type conversion of field
            mydoc=(mycol.aggregate(pipeline=pipe)) 
            line_items=""           
            for x in mydoc:
                line_items=x['total']
            line_items=str(line_items)
            resp="The claim has "+line_items+" line items"
        else:
            resp="Could not find claim with Claim Number "+claim_num_rec+", Please make sure you entered correct details "
        return(resp)       
    except Exception as e:
        print(str(e))
        return "Sorry, Could not fetch you results at this time"

def get_type_of_claim(value1):
    try:
        
        claim_num_rec=str(value1)        
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
        mydoc = mycol.find({"root_claim_num": str(claim_num_rec)})
        n_records=(str(mydoc.count()))
        print(n_records)
        if int(n_records) > 0:
            pipe = [{'$match':{"root_claim_num":str(claim_num_rec),"claim_type_cd":"H"}},{'$group': {'_id':'$root_claim_num', 'total': {'$sum': 1}}}] ## sum after type conversion of field
            mydoc=(mycol.aggregate(pipeline=pipe)) 
            H_type_claims="0"           
            for x in mydoc:
                H_type_claims=x['total']
            H_type_claims=str(H_type_claims)
            pipe = [{'$match':{"root_claim_num":str(claim_num_rec),"claim_type_cd":"M"}},{'$group': {'_id':'$root_claim_num', 'total': {'$sum': 1}}}] ## sum after type conversion of field
            mydoc=(mycol.aggregate(pipeline=pipe)) 
            M_type_claims="0"           
            for x in mydoc:
                M_type_claims=x['total']
            M_type_claims=str(M_type_claims)
            if int(H_type_claims) > int(M_type_claims):
                resp="It is a Facility Claim"
            elif int(H_type_claims) < int(M_type_claims):
                resp="It is a Professional Claim" 
            else:
                resp="It has both Professional and Facility claim line numbers"
                       
        else:
            resp="Could not find claim with Claim Number "+claim_num_rec+", Please make sure you entered correct details "
        return(resp)       
    except Exception as e:
        print(str(e))
        return "Sorry, Could not fetch you results at this time"


def get_lob_of_claim(value1):

    try:        
        claim_num_rec=str(value1)        
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
        mydoc = mycol.find({"root_claim_num": str(claim_num_rec)})
        n_records=(str(mydoc.count()))
        print(n_records)
        if int(n_records) > 0:
            mydoc = mycol.find({"root_claim_num": str(claim_num_rec)})
            lob_list=list()
            for x in mydoc:
                lob_list.append(x['lob_id'])
            lob_list = list(dict.fromkeys(lob_list))
            resp="Claim belongs to "+str(lob_list).replace('[','').replace(']','').replace('\'','')+" line of business"
                       
        else:
            resp="Could not find claim with Claim Number "+claim_num_rec+", Please make sure you entered correct details "
        return(resp)       
    except Exception as e:
        print(str(e))
        return "Sorry, Could not fetch you results at this time"

def get_diag_cd_claim(value1):

    try:        
        claim_num_rec=str(value1)        
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
        mydoc = mycol.find({"root_claim_num": str(claim_num_rec)})
        n_records=(str(mydoc.count()))
        print(n_records)
        if int(n_records) > 0:
            mydoc = mycol.find({"root_claim_num": str(claim_num_rec)})
            diag_cd_list=list()
            diag_desc_list=list()
            for x in mydoc:
                diag_cd_list.append(x['diag_cd'])
                diag_desc_list.append(x['diag_cd'])
            diag_cd_list = list(dict.fromkeys(diag_cd_list))
            resp="The following Diagnosis codes are associated with the claim "+str(claim_num_rec)+ " <br><ul>"
            s1=""
            for row in diag_cd_list:
                s1=s1+"<li>"+row+"</li>"
            resp=resp+s1+"</ul>"                       
        else:
            resp="Could not find claim with Claim Number "+claim_num_rec+", Please make sure you entered correct details "
        return(resp)       
    except Exception as e:
        print(str(e))
        return "Sorry, Could not fetch you results at this time"

def get_npi_of_claim(value1):

    try:        
        claim_num_rec=str(value1)        
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
        mydoc = mycol.find({"root_claim_num": str(claim_num_rec)})
        n_records=(str(mydoc.count()))
        print(n_records)
        if int(n_records) > 0:
            mydoc = mycol.find({"root_claim_num": str(claim_num_rec)})
            lob_list=list()
            for x in mydoc:
                lob_list.append(x['payto_provider_npi'])
            lob_list = list(dict.fromkeys(lob_list))
            resp="The NPI "+str(lob_list).replace('[','').replace(']','').replace('\'','')+" is associated with claim "+str(claim_num_rec)
                       
        else:
            resp="Could not find claim with Claim Number "+claim_num_rec+", Please make sure you entered correct details "
        return(resp)       
    except Exception as e:
        print(str(e))
        return "Sorry, Could not fetch you results at this time"

def get_tax_id_claim(value1):

    try:        
        claim_num_rec=str(value1)        
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
        mydoc = mycol.find({"root_claim_num": str(claim_num_rec)})
        n_records=(str(mydoc.count()))
        print(n_records)
        if int(n_records) > 0:
            mydoc = mycol.find({"root_claim_num": str(claim_num_rec)})
            lob_list=list()
            for x in mydoc:
                lob_list.append(x['payto_provider_tax_id'])
            lob_list = list(dict.fromkeys(lob_list))
            resp="The TAX ID "+str(lob_list).replace('[','').replace(']','').replace('\'','')+" is associated with claim "+str(claim_num_rec)
                       
        else:
            resp="Could not find claim with Claim Number "+claim_num_rec+", Please make sure you entered correct details "
        return(resp)       
    except Exception as e:
        print(str(e))
        return "Sorry, Could not fetch you results at this time"

def get_paid_date_str_of_claim(value1):

    try:        
        claim_num_rec=str(value1)        
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
        mydoc = mycol.find({"root_claim_num": str(claim_num_rec)})
        n_records=(str(mydoc.count()))
        print(n_records)
        if int(n_records) > 0:
            pipe = [{'$match':{"root_claim_num":str(claim_num_rec)}},{'$group': {'_id':'$root_claim_num', 'total': {'$max': {'$convert':{'input':'$paid_date_str','to':'date'}}}}}] ## sum after type conversion of field
            mydoc=(mycol.aggregate(pipeline=pipe))            
            t="--"
            for x in mydoc:
                t=x['total'].strftime('%Y-%b-%d') 
            resp="Claim got paid on "+t.split('-')[2]+"th of "+t.split('-')[1] +", "+t.split('-')[0]
        else:
            resp="Could not find claim with Claim Number "+claim_num_rec+", Please make sure you entered correct details "
        return(resp)       
    except Exception as e:
        print(str(e))
        return "Sorry, Could not fetch you results at this time"

def get_adjudicate_date_of_claim(value1):

    try:        
        claim_num_rec=str(value1)        
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
        mydoc = mycol.find({"root_claim_num": str(claim_num_rec)})
        n_records=(str(mydoc.count()))
        print(n_records)
        if int(n_records) > 0:
            pipe = [{'$match':{"root_claim_num":str(claim_num_rec)}},{'$group': {'_id':'$root_claim_num', 'total': {'$max': {'$convert':{'input':'$paid_date_str','to':'date'}}}}}] ## sum after type conversion of field
            mydoc=(mycol.aggregate(pipeline=pipe))            
            t="--"
            for x in mydoc:
                t=x['total'].strftime('%Y-%b-%d') 
            resp="Claim got adjudicated on "+t.split('-')[2]+"th of "+t.split('-')[1] +", "+t.split('-')[0]
        else:
            resp="Could not find claim with Claim Number "+claim_num_rec+", Please make sure you entered correct details "
        return(resp)       
    except Exception as e:
        print(str(e))
        return "Sorry, Could not fetch you results at this time"

def get_dend_date_of_claim(value1):

    try:        
        claim_num_rec=str(value1)        
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
        mydoc = mycol.find({"root_claim_num": str(claim_num_rec)})
        n_records=(str(mydoc.count()))
        print(n_records)
        if int(n_records) > 0:
            pipe = [{'$match':{"root_claim_num":str(claim_num_rec)}},{'$group': {'_id':'$root_claim_num', 'total': {'$max': {'$convert':{'input':'$paid_date_str','to':'date'}}}}}] ## sum after type conversion of field
            mydoc=(mycol.aggregate(pipeline=pipe))            
            t="--"
            for x in mydoc:
                t=x['total'].strftime('%Y-%b-%d') 
            resp="Claim got denied on "+t.split('-')[2]+"th of "+t.split('-')[1] +", "+t.split('-')[0]
        else:
            resp="Could not find claim with Claim Number "+claim_num_rec+", Please make sure you entered correct details "
        return(resp)       
    except Exception as e:
        print(str(e))
        return "Sorry, Could not fetch you results at this time"

def get_adjstd_date_of_claim(value1):

    try:        
        claim_num_rec=str(value1)        
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
        mydoc = mycol.find({"root_claim_num": str(claim_num_rec)})
        n_records=(str(mydoc.count()))
        print(n_records)
        if int(n_records) > 0:
            pipe = [{'$match':{"root_claim_num":str(claim_num_rec)}},{'$group': {'_id':'$root_claim_num', 'total': {'$max': {'$convert':{'input':'$paid_date_str','to':'date'}}}}}] ## sum after type conversion of field
            mydoc=(mycol.aggregate(pipeline=pipe))            
            t="--"
            for x in mydoc:
                t=x['total'].strftime('%Y-%b-%d') 
            resp="Claim got adjusted on "+t.split('-')[2]+"th of "+t.split('-')[1] +", "+t.split('-')[0]
        else:
            resp="Could not find claim with Claim Number "+claim_num_rec+", Please make sure you entered correct details "
        return(resp)       
    except Exception as e:
        print(str(e))
        return "Sorry, Could not fetch you results at this time"


def get_service_date_of_claim(value1):

    try:        
        claim_num_rec=str(value1)        
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
        mydoc = mycol.find({"root_claim_num": str(claim_num_rec)})
        n_records=(str(mydoc.count()))
        print(n_records)
        if int(n_records) > 0:
            pipe = [{'$match':{"root_claim_num":str(claim_num_rec)}},{'$group': {'_id':'$root_claim_num', 'total': {'$max': {'$convert':{'input':'$from_date_str','to':'date'}}}}}] ## sum after type conversion of field
            mydoc=(mycol.aggregate(pipeline=pipe))            
            t="--"
            for x in mydoc:
                t=x['total'].strftime('%Y-%b-%d') 
            resp="Date of Service of claim is "+t.split('-')[2]+"th of "+t.split('-')[1] +", "+t.split('-')[0]
        else:
            resp="Could not find claim with Claim Number "+claim_num_rec+", Please make sure you entered correct details "
        return(resp)       
    except Exception as e:
        print(str(e))
        return "Sorry, Could not fetch you results at this time"

def get_rcvd_date_of_claim(value1):

    try:        
        claim_num_rec=str(value1)        
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
        mydoc = mycol.find({"root_claim_num": str(claim_num_rec)})
        n_records=(str(mydoc.count()))
        print(n_records)
        if int(n_records) > 0:
            pipe = [{'$match':{"root_claim_num":str(claim_num_rec)}},{'$group': {'_id':'$root_claim_num', 'total': {'$max': {'$convert':{'input':'$received_date_str','to':'date'}}}}}] ## sum after type conversion of field
            mydoc=(mycol.aggregate(pipeline=pipe))            
            t="--"
            for x in mydoc:
                t=x['total'].strftime('%Y-%b-%d') 
            resp="Claim was received by UHC on "+t.split('-')[2]+"th of "+t.split('-')[1] +", "+t.split('-')[0]
        else:
            resp="Could not find claim with Claim Number "+claim_num_rec+", Please make sure you entered correct details "
        return(resp)       
    except Exception as e:
        print(str(e))
        return "Sorry, Could not fetch you results at this time"


def get_sbmtd_date_of_claim(value1):

    try:        
        claim_num_rec=str(value1)        
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
        mydoc = mycol.find({"root_claim_num": str(claim_num_rec)})
        n_records=(str(mydoc.count()))
        print(n_records)
        if int(n_records) > 0:
            pipe = [{'$match':{"root_claim_num":str(claim_num_rec)}},{'$group': {'_id':'$root_claim_num', 'total': {'$max': {'$convert':{'input':'$received_date_str','to':'date'}}}}}] ## sum after type conversion of field
            mydoc=(mycol.aggregate(pipeline=pipe))            
            t="--"
            for x in mydoc:
                t=x['total'].strftime('%Y-%b-%d') 
            resp="Claim was submitted by UHC on "+t.split('-')[2]+"th of "+t.split('-')[1] +", "+t.split('-')[0]
        else:
            resp="Could not find claim with Claim Number "+claim_num_rec+", Please make sure you entered correct details "
        return(resp)       
    except Exception as e:
        print(str(e))
        return "Sorry, Could not fetch you results at this time"

def get_par_non_par(value1):
    try:
        
        claim_num_rec=str(value1)        
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
        mydoc = mycol.find({"root_claim_num": str(claim_num_rec)})
        n_records=(str(mydoc.count()))
        print(n_records)
        if int(n_records) > 0:
            pipe = [{'$match':{"root_claim_num":str(claim_num_rec),"claim_non_par_denial_ind":"0"}},{'$group': {'_id':'$root_claim_num', 'total': {'$sum': 1}}}] ## sum after type conversion of field
            mydoc=(mycol.aggregate(pipeline=pipe)) 
            H_type_claims="0"           
            for x in mydoc:
                H_type_claims=x['total']
            H_type_claims=str(H_type_claims)
            pipe = [{'$match':{"root_claim_num":str(claim_num_rec),"claim_non_par_denial_ind":"1"}},{'$group': {'_id':'$root_claim_num', 'total': {'$sum': 1}}}] ## sum after type conversion of field
            mydoc=(mycol.aggregate(pipeline=pipe)) 
            M_type_claims="0"           
            for x in mydoc:
                M_type_claims=x['total']
            M_type_claims=str(M_type_claims)
            if int(H_type_claims) > int(M_type_claims):
                resp="The claim "+str(claim_num_rec)+" is a par claim"
            elif int(H_type_claims) < int(M_type_claims):
                resp="The claim "+str(claim_num_rec)+" is a non-par claim"
            else:
                resp="The claim "+str(claim_num_rec)+" is a non-par claim"
                       
        else:
            resp="Could not find claim with Claim Number "+claim_num_rec+", Please make sure you entered correct details "
        return(resp)       
    except Exception as e:
        print(str(e))
        return "Sorry, Could not fetch you results at this time"

#########high dollar claim status
def hgh_dlr_claim_status(value1):
    try:
        
        claim_num_rec=str(value1)        
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
        mydoc = mycol.find({"root_claim_num": str(claim_num_rec)})
        n_records=(str(mydoc.count()))
        print(n_records)
        if int(n_records) > 0:
            pipe = [{'$match':{"root_claim_num":str(claim_num_rec),"claim_high_dollar_paid_ind":"0"}},{'$group': {'_id':'$root_claim_num', 'total': {'$sum': 1}}}] ## sum after type conversion of field
            mydoc=(mycol.aggregate(pipeline=pipe)) 
            H_type_claims="0"           
            for x in mydoc:
                H_type_claims=x['total']
            H_type_claims=str(H_type_claims)
            pipe = [{'$match':{"root_claim_num":str(claim_num_rec),"claim_high_dollar_paid_ind":"1"}},{'$group': {'_id':'$root_claim_num', 'total': {'$sum': 1}}}] ## sum after type conversion of field
            mydoc=(mycol.aggregate(pipeline=pipe)) 
            M_type_claims="0"           
            for x in mydoc:
                M_type_claims=x['total']
            M_type_claims=str(M_type_claims)
            if int(H_type_claims) > int(M_type_claims):
                resp="The claim "+str(claim_num_rec)+" is a High Dollar claim"
            elif int(H_type_claims) < int(M_type_claims):
                resp="The claim "+str(claim_num_rec)+" is not a High Dollar claim"
            else:
                resp="It was both High dollar and not a high dollar claim"
                       
        else:
            resp="Could not find claim with Claim Number "+claim_num_rec+", Please make sure you entered correct details "
        return(resp)       
    except Exception as e:
        print(str(e))
        return "Sorry, Could not fetch you results at this time"
#########high dollar claim status

def get_billed_amt(value1):

    try:        

        claim_num_rec=str(value1)        
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
        mydoc = mycol.find({"root_claim_num": str(claim_num_rec)})
        n_records=(str(mydoc.count()))
        print(n_records)
        if int(n_records) > 0:
            pipe = [{'$match':{"root_claim_num":str(claim_num_rec)}},{'$group': {'_id':'$root_claim_num', 'total': {'$sum': {'$convert':{'input':'$amt_billed','to':'double'}}}}}] ## sum after type conversion of field
            mydoc=(mycol.aggregate(pipeline=pipe))            
            billed_amt=""
            for x in mydoc:
                billed_amt=x['total']
            billed_amt=str(billed_amt)
            resp="The amount billed for the claim is "+billed_amt
        else:
            resp="Could not find claim with Claim Number "+claim_num_rec+", Please make sure you entered correct details "
        return(resp)       
    except Exception as e:
        print(str(e))
        return "Sorry, Could not fetch you results at this time"

def get_paid_amt(value1):

    try:        

        claim_num_rec=str(value1)        
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
        mydoc = mycol.find({"root_claim_num": str(claim_num_rec)})
        n_records=(str(mydoc.count()))
        print(n_records)
        if int(n_records) > 0:
            pipe = [{'$match':{"root_claim_num":str(claim_num_rec)}},{'$group': {'_id':'$root_claim_num', 'total': {'$sum': {'$convert':{'input':'$amt_paid','to':'double'}}}}}] ## sum after type conversion of field
            mydoc=(mycol.aggregate(pipeline=pipe))            
            billed_amt=""
            for x in mydoc:
                billed_amt=x['total']
            billed_amt=str(billed_amt)
            resp="The amount paid for the claim is "+billed_amt
        else:
            resp="Could not find claim with Claim Number "+claim_num_rec+", Please make sure you entered correct details "
        return(resp)       
    except Exception as e:
        print(str(e))
        return "Sorry, Could not fetch you results at this time"

def get_allowed_amt(value1):

    try:        

        claim_num_rec=str(value1)        
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
        mydoc = mycol.find({"root_claim_num": str(claim_num_rec)})
        n_records=(str(mydoc.count()))
        print(n_records)
        if int(n_records) > 0:
            pipe = [{'$match':{"root_claim_num":str(claim_num_rec)}},{'$group': {'_id':'$root_claim_num', 'total': {'$sum': {'$convert':{'input':'$amt_allowed','to':'double'}}}}}] ## sum after type conversion of field
            mydoc=(mycol.aggregate(pipeline=pipe))            
            billed_amt=""
            for x in mydoc:
                billed_amt=x['total']
            billed_amt=str(billed_amt)
            resp="The amount Allowed for the claim is "+billed_amt
        else:
            resp="Could not find claim with Claim Number "+claim_num_rec+", Please make sure you entered correct details "
        return(resp)       
    except Exception as e:
        print(str(e))
        return "Sorry, Could not fetch you results at this time"

def get_interest_amt(value1):

    try:        

        claim_num_rec=str(value1)        
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
        mydoc = mycol.find({"root_claim_num": str(claim_num_rec)})
        n_records=(str(mydoc.count()))
        print(n_records)
        if int(n_records) > 0:
            pipe = [{'$match':{"root_claim_num":str(claim_num_rec)}},{'$group': {'_id':'$root_claim_num', 'total': {'$sum': {'$convert':{'input':'$amt_interest','to':'double'}}}}}] ## sum after type conversion of field
            mydoc=(mycol.aggregate(pipeline=pipe))            
            billed_amt=""
            for x in mydoc:
                billed_amt=x['total']
            billed_amt=str(billed_amt)
            resp="The interest paid  for the claim is "+billed_amt
        else:
            resp="Could not find claim with Claim Number "+claim_num_rec+", Please make sure you entered correct details "
        return(resp)       
    except Exception as e:
        print(str(e))
        return "Sorry, Could not fetch you results at this time"


def get_adjusted_amt(value1):

    try:        

        claim_num_rec=str(value1)        
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
        mydoc = mycol.find({"root_claim_num": str(claim_num_rec)})
        n_records=(str(mydoc.count()))
        print(n_records)
        if int(n_records) > 0:
            claim_status=get_status(value1)
            if str(claim_status.split('}')[0])=='3':
                pipe = [{'$match':{"root_claim_num":str(claim_num_rec)}},{'$group': {'_id':'$root_claim_num', 'total': {'$sum': {'$convert':{'input':'$amt_paid','to':'double'}}}}}] ## sum after type conversion of field
                mydoc=(mycol.aggregate(pipeline=pipe))            
                paid_amt=""
                for x in mydoc:
                    paid_amt=x['total']
                paid_amt=str(paid_amt)
                pipe = [{'$match':{"root_claim_num":str(claim_num_rec)}},{'$group': {'_id':'$root_claim_num', 'total': {'$sum': {'$convert':{'input':'$amt_billed','to':'double'}}}}}] ## sum after type conversion of field
                mydoc=(mycol.aggregate(pipeline=pipe))            
                billed_amt=""
                for x in mydoc:
                    billed_amt=x['total']
                billed_amt=str(billed_amt)
                adj_amt=str(float(billed_amt)-float(paid_amt))
                resp="The adjusted amount for the claim is "+adj_amt
            else:
                resp="Your claim is not adjusted"
        else:
            resp="Could not find claim with Claim Number "+claim_num_rec+", Please make sure you entered correct details "
        return(resp)       
    except Exception as e:
        print(str(e))
        return "Sorry, Could not fetch you results at this time"

def get_denied_amt(value1):

    try:        

        claim_num_rec=str(value1)        
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
        mydoc = mycol.find({"root_claim_num": str(claim_num_rec)})
        n_records=(str(mydoc.count()))
        print(n_records)
        if int(n_records) > 0:
            claim_status=get_status(value1)
            if str(claim_status.split('}')[0])=='4' or str(claim_status.split('}')[0])=='1':
                pipe = [{'$match':{"root_claim_num":str(claim_num_rec)}},{'$group': {'_id':'$root_claim_num', 'total': {'$sum': {'$convert':{'input':'$amt_paid','to':'double'}}}}}] ## sum after type conversion of field
                mydoc=(mycol.aggregate(pipeline=pipe))            
                paid_amt=""
                for x in mydoc:
                    paid_amt=x['total']
                paid_amt=str(paid_amt)
                pipe = [{'$match':{"root_claim_num":str(claim_num_rec)}},{'$group': {'_id':'$root_claim_num', 'total': {'$sum': {'$convert':{'input':'$amt_billed','to':'double'}}}}}] ## sum after type conversion of field
                mydoc=(mycol.aggregate(pipeline=pipe))            
                billed_amt=""
                for x in mydoc:
                    billed_amt=x['total']
                billed_amt=str(billed_amt)
                adj_amt=str(float(billed_amt)-float(paid_amt))
                resp="The Denied amount for the claim is "+adj_amt
            else:
                resp="Your claim doesn't have denials"
        else:
            resp="Could not find claim with Claim Number "+claim_num_rec+", Please make sure you entered correct details "
        return(resp)       
    except Exception as e:
        print(str(e))
        return "Sorry, Could not fetch you results at this time"

def get_resubmit_proc():

    try:               
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name] 
        mydoc=mycol.distinct('abbreviated_final_category')  
        resubmit_proc="Please keep following things in check while resubmitting your Claim<br><ul>"
        s1=""
        for x in mydoc:
            s1=s1+"<li>"+x+"</li>"
        resubmit_proc=resubmit_proc+s1+"</ul>"
        # print(resubmit_proc)
        return(resubmit_proc)
       
    except Exception as e:
        print(str(e))
        return "Sorry, Could not fetch you results at this time"

def get_denial_reason(value1):

    try:        
        claim_num_rec=str(value1)        
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
        mydoc = mycol.find({"root_claim_num": str(claim_num_rec)})
        n_records=(str(mydoc.count()))
        print(n_records)
        if int(n_records) > 0:
            mydoc = mycol.find({"root_claim_num": str(claim_num_rec),"claim_denial_ind":"1"})
            nd_records=str(mydoc.count())
            if int(nd_records) > 0:
                denial_reason="Your claim is denied due to following reasons<br><ul>"
                s1=""
                for x in mydoc:
                    if x['denial_description'].upper()=="TEXT NOT AVAILABLE.":
                        s1=s1+"<li>"+"Denial Code "+x['denial_full_reasons']+"</li>"
                    else:
                        s1=s1+"<li>"+"Denial Code "+x['denial_full_reasons']+" with description as "+x['denial_description']+"</li>"
                denial_reason=denial_reason+s1+"</ul>" 
                denial_reason=denial_reason+"!How can I resubmit my Claim!What's the processing time of my Claim" 
                return denial_reason
            else:
                return "There are no denials for your claim "+str(claim_num_rec)                       
        else:
            resp="Could not find claim with Claim Number "+claim_num_rec+", Please make sure you entered correct details "
        return(resp)       
    except Exception as e:
        print(str(e))
        return "Sorry, Could not fetch you results at this time"

def get_adj_reason(value1):

    try:        
        claim_num_rec=str(value1)        
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
        mydoc = mycol.find({"root_claim_num": str(claim_num_rec)})
        n_records=(str(mydoc.count()))
        print(n_records)
        if int(n_records) > 0:
            mydoc = mycol.find({"root_claim_num": str(claim_num_rec),"claim_adj_ind":"1"})
            nd_records=str(mydoc.count())
            if int(nd_records) > 0:
                denial_reason="Your claim is adjusted due to following reasons<br><ul>"
                s1=""
                for x in mydoc:
                    if x['adjustment_description'].upper()=="TEXT NOT AVAILABLE.":
                        s1=s1+"<li>"+"Adjustment Code "+x['adjustment_reasons']
                    else:
                        s1=s1+"<li>"+"Adjustment Code "+x['adjustment_reasons']+" with description as "+x['adjustment_description']+"</li>"
                    
                denial_reason=denial_reason+s1+"</ul>" 
                denial_reason=denial_reason+"!How can I resubmit my Claim!What's the processing time of my Claim" 
                return denial_reason
            else:
                return "There are no Adjustments for your claim "+str(claim_num_rec)                       
        else:
            resp="Could not find claim with Claim Number "+claim_num_rec+", Please make sure you entered correct details "
        return(resp)       
    except Exception as e:
        print(str(e))
        return "Sorry, Could not fetch you results at this time"

def get_proc_time(value1):

    try:        
        claim_num_rec=str(value1)        
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
        mydoc = mycol.find({"root_claim_num": str(claim_num_rec)})
        n_records=(str(mydoc.count()))
        print(n_records)
        if int(n_records) > 0:
            pipe = [{'$match':{"root_claim_num":str(claim_num_rec)}},{'$group': {'_id':'$root_claim_num', 'total': {'$min': {'$convert':{'input':'$fromdatetoreceiveddate','to':'int'}}}}}] ## sum after type conversion of field
            mydoc=(mycol.aggregate(pipeline=pipe)) 
            fr="0"           
            for x in mydoc:
                fr=x['total']
            fr=str(fr)
            pipe = [{'$match':{"root_claim_num":str(claim_num_rec)}},{'$group': {'_id':'$root_claim_num', 'total': {'$max': {'$convert':{'input':'$fromdatetopaiddate','to':'int'}}}}}] ## sum after type conversion of field
            mydoc=(mycol.aggregate(pipeline=pipe)) 
            fp="0"           
            for x in mydoc:
                fp=x['total']
            fp=str(fp)
            pipe = [{'$match':{"root_claim_num":str(claim_num_rec)}},{'$group': {'_id':'$root_claim_num', 'total': {'$max': {'$convert':{'input':'$receiveddatetopaiddate','to':'int'}}}}}] ## sum after type conversion of field
            mydoc=(mycol.aggregate(pipeline=pipe)) 
            rp="0"           
            for x in mydoc:
                rp=x['total']
            rp=str(rp)
            # resp="The provider took "+fr+" days to submit the claim.\n"+"The UHC took "+rp+" days to pay the claim.\n"+"It took "+fp+" days for the claim to get paid."
            resp="<ul><li>The provider took "+fr+" days to submit the claim.</li>"+"<li>The UHC took "+rp+" days to pay the claim.</li>"+"<li>Starting from Date of Service it took "+fp+" days for the claim to get paid.</li></ul>"
        else:
            resp="Could not find claim with Claim Number "+claim_num_rec+", Please make sure you entered correct details "
        return(resp)
    except Exception as e:
        print(str(e))
        return "Sorry, Could not fetch you results at this time"

def get_received_claims(dt,provider_lst):
    print(str(dt))
    try:
        n_records="0"
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name] 
        cond=""
        if len(dt)==2:
            s1=str(dt[0])
            start = datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),0,0)
            s1=str(dt[1].split('}')[0])
            end = datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),0,0)
            print(start)
            print(end)
            print(str(len(provider_lst)))
            if len(provider_lst) > 0:
                print("entered if")
                mydoc = mydoc = mycol.find({'received_date_str':{'$gt':str(start),'$lt':str(end) },'payto_provider_tax_id':{'$in':provider_lst}})
            else:
                mydoc = mycol.find({'received_date_str':{'$gt':str(start),'$lt':str(end) }})
            n_records=str(mydoc.count())            
        elif len(dt)==3:
            mydoc = mycol.find({'received_date_str':{'$regex':'2018-11-.*'}}).limit(5)            
            cond=""
            if len(dt[0])==0:
                cond=cond+",{'received_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[0]:
                    cond=cond+",{'received_date_str':{'$regex':'.*-.*-"+str(dy)+".*'}}"
                
            if len(dt[1])==0:
                cond=cond+",{'received_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[1]:
                    cond=cond+",{'received_date_str':{'$regex':'.*-"+str(dy)+"-.*'}}"
                
            if len(dt[2])==0:
                cond=cond+",{'received_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[2]:
                    cond=cond+",{'received_date_str':{'$regex':'"+str(dy)+"-.*-.*'}}"
            pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
            if len(provider_lst) > 0:
                cond="{'$and':["+cond[1:]+pc+"]}"
            else:
                cond="{'$and':["+cond[1:]+"]}"
            my_dict = ast.literal_eval(cond)
            mydoc = mycol.find(my_dict)
            n_records=str(mydoc.count()) 
              
        print(cond)    
    
               
        # n_records=str(all_rows[0][0]).replace("None","0")
        if len(dt)==3:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dt)==2:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num=str(n_records)+"} claims were received "+dy_op+mon_op+yr_op+q_op+"."
        return recvd_num
    # else:
    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"

def get_bill_amt_recvd(dt,provider_lst):
    print(str(dt))
    try:
        billed_amt="0"
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name] 
        cond=""
        if len(dt)==2:
            s1=str(dt[0])
            start = datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),0,0)
            s1=str(dt[1].split('}')[0])
            end = datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),0,0)
            print(start)
            print(end)
            if len(provider_lst) > 0:
                pipe = [{'$match':{'received_date_str':{'$gt':str(start),'$lt':str(end) },'payto_provider_tax_id':{'$in':provider_lst}}},{'$group': {'_id':'$received_date_str', 'total': {'$sum': {'$convert':{'input':'$amt_billed','to':'double'}}}}}] ## sum after type conversion of field            
            else:
                pipe = [{'$match':{'received_date_str':{'$gt':str(start),'$lt':str(end) }}},{'$group': {'_id':'$received_date_str', 'total': {'$sum': {'$convert':{'input':'$amt_billed','to':'double'}}}}}] ## sum after type conversion of field            
            mydoc=(mycol.aggregate(pipeline=pipe))            
            billed_amt="0"
            for x in mydoc:
                billed_amt=float(billed_amt)+float(str(x['total']))
            billed_amt=str(billed_amt)
            print(billed_amt)
        elif len(dt)==3:                       
            cond=""
            if len(dt[0])==0:
                cond=cond+",{'received_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[0]:
                    cond=cond+",{'received_date_str':{'$regex':'.*-.*-"+str(dy)+".*'}}"
                
            if len(dt[1])==0:
                cond=cond+",{'received_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[1]:
                    cond=cond+",{'received_date_str':{'$regex':'.*-"+str(dy)+"-.*'}}"
                
            if len(dt[2])==0:
                cond=cond+",{'received_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[2]:
                    cond=cond+",{'received_date_str':{'$regex':'"+str(dy)+"-.*-.*'}}"    
            if len(provider_lst) > 0:
                pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                cond="{'$and':["+cond[1:]+pc+"]}"
                my_dict = ast.literal_eval(cond)
                pipe = [{'$match':my_dict},{'$group': {'_id':'$received_date_str', 'total': {'$sum': {'$convert':{'input':'$amt_billed','to':'double'}}}}}] ## sum after type conversion of field            
            else:
                pc=""
                cond="{'$and':["+cond[1:]+pc+"]}"
                my_dict = ast.literal_eval(cond)
                pipe = [{'$match':my_dict},{'$group': {'_id':'$received_date_str', 'total': {'$sum': {'$convert':{'input':'$amt_billed','to':'double'}}}}}] ## sum after type conversion of field                
            mydoc=(mycol.aggregate(pipeline=pipe)) 
            mydoc=(mycol.aggregate(pipeline=pipe))            
            billed_amt="0"
            for x in mydoc:
                billed_amt=float(billed_amt)+float(str(x['total']))
            billed_amt=str(billed_amt)
            print(billed_amt)

              
        print(cond)    
        
        if len(dt)==3:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dt)==2:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num="The total billed amount of received claims "+dy_op+mon_op+yr_op+q_op+" is "+str(billed_amt)
        return recvd_num
    # else:
    except Exception as e:
        print(str(e))      
        return "Sorry, Could not fetch you results at this time"


def get_paid_amt_claims_recvd(dt,provider_lst):
    print(str(dt))
    try:
        billed_amt="0"
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name] 
        cond=""
        if len(dt)==2:
            s1=str(dt[0])
            start = datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),0,0)
            s1=str(dt[1].split('}')[0])
            end = datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),0,0)
            print(start)
            print(end)      
            if len(provider_lst) > 0: 
                pipe = [{'$match':{'$and':[{'received_date_str':{'$gt':str(start),'$lt':str(end)}},{'payto_provider_tax_id':{'$in':provider_lst}},{'paid_date_str':{'$gt':str(start),'$lt':str(end)}}]}},{'$group': {'_id':'$paid_date_str', 'total': {'$sum': {'$convert':{'input':'$amt_paid','to':'double'}}}}}]
            else:
                pipe = [{'$match':{'$and':[{'received_date_str':{'$gt':str(start),'$lt':str(end)}},{'paid_date_str':{'$gt':str(start),'$lt':str(end)}}]}},{'$group': {'_id':'$paid_date_str', 'total': {'$sum': {'$convert':{'input':'$amt_paid','to':'double'}}}}}]
            mydoc=(mycol.aggregate(pipeline=pipe))            
            billed_amt="0"
            for x in mydoc:
                billed_amt=float(billed_amt)+float(str(x['total']))
            billed_amt=str(billed_amt)
            print(billed_amt)
        elif len(dt)==3:                       
            cond=""
            if len(dt[0])==0:
                cond=cond+",{'paid_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[0]:
                    cond=cond+",{'paid_date_str':{'$regex':'.*-.*-"+str(dy)+".*'}}"
                
            if len(dt[1])==0:
                cond=cond+",{'paid_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[1]:
                    cond=cond+",{'paid_date_str':{'$regex':'.*-"+str(dy)+"-.*'}}"
                
            if len(dt[2])==0:
                cond=cond+",{'paid_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[2]:
                    cond=cond+",{'paid_date_str':{'$regex':'"+str(dy)+"-.*-.*'}}"
            cond=cond[1:]            
            cond1=""
            if len(dt[0])==0:
                cond1=cond1+",{'received_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[0]:
                    cond1=cond1+",{'received_date_str':{'$regex':'.*-.*-"+str(dy)+".*'}}"
                
            if len(dt[1])==0:
                cond1=cond1+",{'received_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[1]:
                    cond1=cond1+",{'received_date_str':{'$regex':'.*-"+str(dy)+"-.*'}}"
                
            if len(dt[2])==0:
                cond1=cond1+",{'received_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[2]:
                    cond1=cond1+",{'received_date_str':{'$regex':'"+str(dy)+"-.*-.*'}}"
            cond1=cond1[1:]
            
            if len(provider_lst) > 0:
                pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                cond="{'$and':["+cond+","+cond1+pc+"]}"
            else:
                cond="{'$and':["+cond+","+cond1+"]}"
            my_dict = ast.literal_eval(cond)
            pipe = [{'$match':my_dict},{'$group': {'_id':'$received_date_str', 'total': {'$sum': {'$convert':{'input':'$amt_paid','to':'double'}}}}}] ## sum after type conversion of field            
            mydoc=(mycol.aggregate(pipeline=pipe))            
            billed_amt="0"
            for x in mydoc:
                billed_amt=float(billed_amt)+float(str(x['total']))
            billed_amt=str(billed_amt)
            print(billed_amt)

              
        print(cond)    
        
        if len(dt)==3:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dt)==2:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num="The total paid amount of received claims "+dy_op+mon_op+yr_op+q_op+" is "+str(billed_amt)
        return recvd_num
    # else:
    except Exception as e:
        print(str(e))      
        return "Sorry, Could not fetch you results at this time"

def get_paid_cnt_claims_recvd(dt,provider_lst):
    print(provider_lst)
    print(str(dt))
    try:
        billed_amt="0"
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name] 
        cond=""
        if len(dt)==2:
            s1=str(dt[0])
            start = datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),0,0)
            s1=str(dt[1].split('}')[0])
            end = datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),0,0)
            print(start)
            print(end)       
            if len(provider_lst) > 0:
                pipe = [{'$match':{'$and':[{'received_date_str':{'$gt':str(start),'$lt':str(end)}},{'claim_denial_ind':'0'},{'payto_provider_tax_id':{'$in':provider_lst}},{'paid_date_str':{'$gt':str(start),'$lt':str(end)}}]}},{'$group': {'_id':'$paid_date_str', 'total': {'$sum': 1}}}]
            else:
                pipe = [{'$match':{'$and':[{'received_date_str':{'$gt':str(start),'$lt':str(end)}},{'claim_denial_ind':'0'},{'paid_date_str':{'$gt':str(start),'$lt':str(end)}}]}},{'$group': {'_id':'$paid_date_str', 'total': {'$sum': 1}}}]
            mydoc=(mycol.aggregate(pipeline=pipe))            
            billed_amt="0"
            for x in mydoc:
                billed_amt=int(billed_amt)+int(str(x['total']))
            billed_amt=str(billed_amt)
            print(billed_amt)
        elif len(dt)==3:                       
            cond=""
            if len(dt[0])==0:
                cond=cond+",{'received_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[0]:
                    cond=cond+",{'received_date_str':{'$regex':'.*-.*-"+str(dy)+".*'}}"
                
            if len(dt[1])==0:
                cond=cond+",{'received_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[1]:
                    cond=cond+",{'received_date_str':{'$regex':'.*-"+str(dy)+"-.*'}}"
                
            if len(dt[2])==0:
                cond=cond+",{'received_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[2]:
                    cond=cond+",{'received_date_str':{'$regex':'"+str(dy)+"-.*-.*'}}"
            cond=cond[1:]            
            cond1=""
            if len(dt[0])==0:
                cond1=cond1+",{'paid_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[0]:
                    cond1=cond1+",{'paid_date_str':{'$regex':'.*-.*-"+str(dy)+".*'}}"
                
            if len(dt[1])==0:
                cond1=cond1+",{'paid_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[1]:
                    cond1=cond1+",{'paid_date_str':{'$regex':'.*-"+str(dy)+"-.*'}}"
                
            if len(dt[2])==0:
                cond1=cond1+",{'paid_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[2]:
                    cond1=cond1+",{'paid_date_str':{'$regex':'"+str(dy)+"-.*-.*'}}"
            cond1=cond1[1:]
            if len(provider_lst) > 0:
                pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}},{'claim_denial_ind':'0'}"
                cond="{'$and':["+cond+","+cond1+pc+"]}"
            else:
                cond="{'$and':["+cond+","+cond1+"]}"
            my_dict = ast.literal_eval(cond)
            pipe = [{'$match':my_dict},{'$group': {'_id':'$paid_date_str', 'total': {'$sum': 1}}}]
            mydoc=(mycol.aggregate(pipeline=pipe))            
            billed_amt="0"
            for x in mydoc:
                billed_amt=int(billed_amt)+int(str(x['total']))
            billed_amt=str(billed_amt)
            print(billed_amt)

              
        print(cond)    
        
        if len(dt)==3:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dt)==2:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num=str(billed_amt)+" claims got paid out of "+ get_received_claims(dt,provider_lst).split('}')[0].strip(' ') +dy_op+mon_op+yr_op+q_op
        return recvd_num

    except Exception as e:
        print(str(e))     
        return "Sorry, Could not fetch you results at this time"

def get_mode_submission_recvd(dt,provider_lst):
    print(str(dt))
    try:
        billed_amt="0"
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name] 
        cond=""
        if len(dt)==2:
            s1=str(dt[0])
            start = datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),0,0)
            s1=str(dt[1].split('}')[0])
            end = datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),0,0)
            print(start)
            print(end)
            if len(provider_lst) > 0:
                pipe = [{'$match':{'$and':[{'received_date_str':{'$gt':str(start),'$lt':str(end) }},{'payto_provider_tax_id':{'$in':provider_lst}},{'claim_receipt_type_cd':'EDI'}]}},{'$group': {'_id':'$received_date_str', 'total': {'$sum': 1 }}}] ## sum after type conversion of field            
            else:
                pipe = [{'$match':{'$and':[{'received_date_str':{'$gt':str(start),'$lt':str(end) }},{'claim_receipt_type_cd':'EDI'}]}},{'$group': {'_id':'$received_date_str', 'total': {'$sum': 1 }}}] ## sum after type conversion of field            
            mydoc=(mycol.aggregate(pipeline=pipe))            
            billed_amt="0"
            for x in mydoc:
                billed_amt=int(billed_amt)+int(str(x['total']))
            billed_amt=str(billed_amt)
            EDI_Cnt=billed_amt
            if len(provider_lst) > 0:
                pipe = [{'$match':{'$and':[{'received_date_str':{'$gt':str(start),'$lt':str(end) }},{'payto_provider_tax_id':{'$in':provider_lst}},{'claim_receipt_type_cd':'PPR'}]}},{'$group': {'_id':'$received_date_str', 'total': {'$sum': 1 }}}] ## sum after type conversion of field            
            else:
                pipe = [{'$match':{'$and':[{'received_date_str':{'$gt':str(start),'$lt':str(end) }},{'claim_receipt_type_cd':'PPR'}]}},{'$group': {'_id':'$received_date_str', 'total': {'$sum': 1 }}}] ## sum after type conversion of field                        
            
            mydoc=(mycol.aggregate(pipeline=pipe))            
            billed_amt="0"
            for x in mydoc:
                billed_amt=int(billed_amt)+int(str(x['total']))
            billed_amt=str(billed_amt)
            PPR_Cnt=billed_amt
            print(EDI_Cnt+"-"+PPR_Cnt)
        elif len(dt)==3:                       
            cond=""
            if len(dt[0])==0:
                cond=cond+",{'received_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[0]:
                    cond=cond+",{'received_date_str':{'$regex':'.*-.*-"+str(dy)+".*'}}"
                
            if len(dt[1])==0:
                cond=cond+",{'received_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[1]:
                    cond=cond+",{'received_date_str':{'$regex':'.*-"+str(dy)+"-.*'}}"
                
            if len(dt[2])==0:
                cond=cond+",{'received_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[2]:
                    cond=cond+",{'received_date_str':{'$regex':'"+str(dy)+"-.*-.*'}}"
            if len(provider_lst) > 0:
                pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                cond1="{'$and':["+cond[1:]+pc+",{'claim_receipt_type_cd':'EDI' }"+"]}"
            else:
                pc=""
                cond1="{'$and':["+cond[1:]+pc+",{'claim_receipt_type_cd':'EDI' }"+"]}"
            my_dict = ast.literal_eval(cond1)
            pipe = [{'$match':my_dict},{'$group': {'_id':'$received_date_str', 'total': {'$sum': 1 }}}] ## sum after type conversion of field            
            mydoc=(mycol.aggregate(pipeline=pipe))            
            billed_amt="0"
            for x in mydoc:
                billed_amt=int(billed_amt)+int(str(x['total']))
            billed_amt=str(billed_amt)
            EDI_Cnt=billed_amt
            if len(provider_lst) > 0:
                pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                cond1="{'$and':["+cond[1:]+pc+",{'claim_receipt_type_cd':'PPR' }"+"]}"
            else:
                pc=""
                cond1="{'$and':["+cond[1:]+pc+",{'claim_receipt_type_cd':'PPR' }"+"]}"
            my_dict = ast.literal_eval(cond1)
            pipe = [{'$match':my_dict},{'$group': {'_id':'$received_date_str', 'total': {'$sum': 1 }}}] ## sum after type conversion of field            
            mydoc=(mycol.aggregate(pipeline=pipe))            
            billed_amt="0"
            for x in mydoc:
                billed_amt=int(billed_amt)+int(str(x['total']))
            billed_amt=str(billed_amt)
            PPR_Cnt=billed_amt
              
        print(cond)    
        
        if len(dt)==3:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dt)==2:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num=EDI_Cnt+" claims were submitted on EDI and "+PPR_Cnt+" claims were submitted on PPR"
        return recvd_num

    except Exception as e:
        print(str(e))
        return "Sorry, Could not fetch you results at this time"

############# chat questions response using search questions call ###############

def chat_get_prtl_denied_claims_cnt(dur_list,provider_lst):
    try:
        dt=dur_list
        res=get_prtl_dend_claim_vol_trend(dur_list,provider_lst)
        val_lst_rcvd=list(res["Value"])
        count=0
        for c_i in val_lst_rcvd:
            try:
                count=count+int(c_i)
            except:
                count=count+0
        if len(dur_list)==4:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dur_list)==3:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num=str(count)+" Claims were Partially Denied "+dy_op+mon_op+yr_op+q_op+"."
        return recvd_num
    except Exception as e:
        print("Exception in count deriving function="+str(e))


def chat_get_denied_claims_cnt(dur_list,provider_lst):
    try:
        dt=dur_list
        res=get_dend_claim_vol_trend(dur_list,provider_lst)
        val_lst_rcvd=list(res["Value"])
        count=0
        for c_i in val_lst_rcvd:
            try:
                count=count+int(c_i)
            except:
                count=count+0
        if len(dur_list)==4:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dur_list)==3:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num=str(count)+" Claims were Denied "+dy_op+mon_op+yr_op+q_op+"."
        return recvd_num
    except Exception as e:
        print("Exception in count deriving function="+str(e))


def chat_get_adjusted_claims_cnt(dur_list,provider_lst):
    try:
        dt=dur_list
        res=get_adjstd_claim_vol_trend(dur_list,provider_lst)
        val_lst_rcvd=list(res["Value"])
        count=0
        for c_i in val_lst_rcvd:
            try:
                count=count+int(c_i)
            except:
                count=count+0
        if len(dur_list)==4:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dur_list)==3:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num=str(count)+" Claims were Adjusted "+dy_op+mon_op+yr_op+q_op+"."
        return recvd_num
    except Exception as e:
        print("Exception in count deriving function="+str(e))

def chat_get_received_claims(dur_list,provider_lst):
    try:
        dt=dur_list
        res=get_rcvd_claim_vol_trend(dur_list,provider_lst)
        val_lst_rcvd=list(res["Value"])
        count=0
        for c_i in val_lst_rcvd:
            try:
                count=count+int(c_i)
            except:
                count=count+0
        if len(dur_list)==4:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dur_list)==3:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num=str(count)+" Claims were received "+dy_op+mon_op+yr_op+q_op+"."
        return recvd_num
    except Exception as e:
        print("Exception in count deriving function="+str(e))

def chat_get_paid_claims(dur_list,provider_lst):
    try:
        dt=dur_list
        res=get_paid_claim_vol_trend(dur_list,provider_lst)
        val_lst_rcvd=list(res["Value"])
        count=0
        for c_i in val_lst_rcvd:
            try:
                count=count+int(c_i)
            except:
                count=count+0
        if len(dur_list)==4:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dur_list)==3:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num=str(count)+" Claims were paid "+dy_op+mon_op+yr_op+q_op+"."
        return recvd_num
    except Exception as e:
        print("Exception in count deriving function="+str(e))

def chat_get_prtl_denied_submsn_mode_claims(dur_list,provider_lst):
    
    try:
        dt=dur_list
        res=get_prtl_dend_claim_submsn_mode_trend(dur_list,provider_lst)
        val_lst_rcvd=list(res["Value"])
        hdr_lst_rcvd=list(res["Header"])
        count=""        
        for c_i in range(0,len(val_lst_rcvd)):
            try:
                count=count+val_lst_rcvd[c_i]+" claims were submitted on "+hdr_lst_rcvd[c_i]+","
            except:
                # count=count+0
                junk=1
        count=count[0:len(count)-1]
        if len(dur_list)==4:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dur_list)==3:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num=str(count)+" "+dy_op+mon_op+yr_op+q_op+"."
        return recvd_num
    except Exception as e:
        print("Exception in submission mode deriving function="+str(e))


def chat_get_denied_submsn_mode_claims(dur_list,provider_lst):
    
    try:
        dt=dur_list
        res=get_dend_claim_submsn_mode_trend(dur_list,provider_lst)
        val_lst_rcvd=list(res["Value"])
        hdr_lst_rcvd=list(res["Header"])
        count=""        
        for c_i in range(0,len(val_lst_rcvd)):
            try:
                count=count+val_lst_rcvd[c_i]+" claims were submitted on "+hdr_lst_rcvd[c_i]+","
            except:
                # count=count+0
                junk=1
        count=count[0:len(count)-1]
        if len(dur_list)==4:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dur_list)==3:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num=str(count)+" "+dy_op+mon_op+yr_op+q_op+"."
        return recvd_num
    except Exception as e:
        print("Exception in submission mode deriving function="+str(e))



def chat_get_adjusted_submsn_mode_claims(dur_list,provider_lst):
    
    try:
        dt=dur_list
        res=get_adjstd_claim_submsn_mode_trend(dur_list,provider_lst)
        val_lst_rcvd=list(res["Value"])
        hdr_lst_rcvd=list(res["Header"])
        count=""        
        for c_i in range(0,len(val_lst_rcvd)):
            try:
                count=count+val_lst_rcvd[c_i]+" claims were submitted on "+hdr_lst_rcvd[c_i]+","
            except:
                # count=count+0
                junk=1
        count=count[0:len(count)-1]
        if len(dur_list)==4:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dur_list)==3:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num=str(count)+" "+dy_op+mon_op+yr_op+q_op+"."
        return recvd_num
    except Exception as e:
        print("Exception in submission mode deriving function="+str(e))


def chat_get_received_submsn_mode_claims(dur_list,provider_lst):
    
    try:
        dt=dur_list
        res=get_rcvd_claim_submsn_mode_trend(dur_list,provider_lst)
        val_lst_rcvd=list(res["Value"])
        hdr_lst_rcvd=list(res["Header"])
        count=""        
        for c_i in range(0,len(val_lst_rcvd)):
            try:
                count=count+val_lst_rcvd[c_i]+" claims were submitted on "+hdr_lst_rcvd[c_i]+","
            except:
                # count=count+0
                junk=1
        count=count[0:len(count)-1]
        if len(dur_list)==4:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dur_list)==3:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num=str(count)+" "+dy_op+mon_op+yr_op+q_op+"."
        return recvd_num
    except Exception as e:
        print("Exception in submission mode deriving function="+str(e))


def chat_get_paid_submsn_mode_claims(dur_list,provider_lst):
    
    try:
        dt=dur_list
        res=get_paid_claim_submsn_mode_trend(dur_list,provider_lst)
        val_lst_rcvd=list(res["Value"])
        hdr_lst_rcvd=list(res["Header"])
        count=""        
        for c_i in range(0,len(val_lst_rcvd)):
            try:
                count=count+val_lst_rcvd[c_i]+" claims were submitted on "+hdr_lst_rcvd[c_i]+","
            except:
                # count=count+0
                junk=1
        count=count[0:len(count)-1]
        if len(dur_list)==4:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dur_list)==3:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num=str(count)+" "+dy_op+mon_op+yr_op+q_op+"."
        return recvd_num
    except Exception as e:
        print("Exception in submission mode deriving function="+str(e))

def chat_get_prtl_denied_lob_claims(dur_list,provider_lst):
    
    try:
        dt=dur_list
        res=get_prtl_dend_claim_lob_trend(dur_list,provider_lst)
        val_lst_rcvd=list(res["Value"])
        hdr_lst_rcvd=list(res["Header"])
        count=""        
        for c_i in range(0,len(val_lst_rcvd)):
            try:
                count=count+val_lst_rcvd[c_i]+" claims having Line of Business "+hdr_lst_rcvd[c_i]+","
            except:
                # count=count+0
                junk=1
        count=count[0:len(count)-1]                
        if len(dur_list)==4:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dur_list)==3:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num=str(count)+" Claims were partially denied "+dy_op+mon_op+yr_op+q_op+"."
        return recvd_num
    except Exception as e:
        print("Exception in count deriving function="+str(e))

def chat_get_denied_lob_claims(dur_list,provider_lst):
    
    try:
        dt=dur_list
        res=get_dend_claim_lob_trend(dur_list,provider_lst)
        val_lst_rcvd=list(res["Value"])
        hdr_lst_rcvd=list(res["Header"])
        count=""        
        for c_i in range(0,len(val_lst_rcvd)):
            try:
                count=count+val_lst_rcvd[c_i]+" claims having Line of Business "+hdr_lst_rcvd[c_i]+","
            except:
                # count=count+0
                junk=1
        count=count[0:len(count)-1]                
        if len(dur_list)==4:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dur_list)==3:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num=str(count)+" Claims were denied "+dy_op+mon_op+yr_op+q_op+"."
        return recvd_num
    except Exception as e:
        print("Exception in count deriving function="+str(e))

def chat_get_received_lob_claims(dur_list,provider_lst):
    
    try:
        dt=dur_list
        res=get_rcvd_claim_lob_trend(dur_list,provider_lst)
        val_lst_rcvd=list(res["Value"])
        hdr_lst_rcvd=list(res["Header"])
        count=""        
        for c_i in range(0,len(val_lst_rcvd)):
            try:
                count=count+val_lst_rcvd[c_i]+" claims having Line of Business "+hdr_lst_rcvd[c_i]+","
            except:
                # count=count+0
                junk=1
        count=count[0:len(count)-1]                
        if len(dur_list)==4:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dur_list)==3:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num=str(count)+" Claims were received "+dy_op+mon_op+yr_op+q_op+"."
        return recvd_num
    except Exception as e:
        print("Exception in count deriving function="+str(e))

def chat_get_adjusted_lob_claims(dur_list,provider_lst):
    
    try:
        dt=dur_list
        res=get_adjstd_claim_lob_trend(dur_list,provider_lst)
        val_lst_rcvd=list(res["Value"])
        hdr_lst_rcvd=list(res["Header"])
        count=""        
        for c_i in range(0,len(val_lst_rcvd)):
            try:
                count=count+val_lst_rcvd[c_i]+" claims having Line of Business "+hdr_lst_rcvd[c_i]+","
            except:
                # count=count+0
                junk=1
        count=count[0:len(count)-1]                
        if len(dur_list)==4:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dur_list)==3:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num=str(count)+" Claims were adjusted "+dy_op+mon_op+yr_op+q_op+"."
        return recvd_num
    except Exception as e:
        print("Exception in count deriving function="+str(e))

def chat_get_paid_lob_claims(dur_list,provider_lst):
    
    try:
        dt=dur_list
        res=get_paid_claim_lob_trend(dur_list,provider_lst)
        val_lst_rcvd=list(res["Value"])
        hdr_lst_rcvd=list(res["Header"])
        count=""        
        for c_i in range(0,len(val_lst_rcvd)):
            try:
                count=count+val_lst_rcvd[c_i]+" claims having Line of Business "+hdr_lst_rcvd[c_i]+","
            except:
                # count=count+0
                junk=1
        count=count[0:len(count)-1]                
        if len(dur_list)==4:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dur_list)==3:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num=str(count)+" Claims were paid "+dy_op+mon_op+yr_op+q_op+"."
        return recvd_num
    except Exception as e:
        print("Exception in count deriving function="+str(e))


def chat_get_prtl_denied_par_claims(dur_list,provider_lst):
    
    try:
        dt=dur_list
        res=get_prtl_dend_claim_par_trend(dur_list,provider_lst)
        val_lst_rcvd=list(res["Value"])
        hdr_lst_rcvd=list(res["Header"])
        count=""        
        for c_i in range(0,len(val_lst_rcvd)):
            try:
                count=count+val_lst_rcvd[c_i]+" "+hdr_lst_rcvd[c_i].replace('0','participating').replace('1','non-participating')+" claims,"
            except:
                # count=count+0
                junk=1
        count=count[0:len(count)-1]                
        if len(dur_list)==4:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dur_list)==3:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num=str(count)+" were partially denied "+dy_op+mon_op+yr_op+q_op+"."
        return recvd_num
    except Exception as e:
        print("Exception in count deriving function="+str(e))

def chat_get_denied_par_claims(dur_list,provider_lst):
    
    try:
        dt=dur_list
        res=get_dend_claim_par_trend(dur_list,provider_lst)
        val_lst_rcvd=list(res["Value"])
        hdr_lst_rcvd=list(res["Header"])
        count=""        
        for c_i in range(0,len(val_lst_rcvd)):
            try:
                count=count+val_lst_rcvd[c_i]+" "+hdr_lst_rcvd[c_i].replace('0','participating').replace('1','non-participating')+" claims,"
            except:
                # count=count+0
                junk=1
        count=count[0:len(count)-1]                
        if len(dur_list)==4:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dur_list)==3:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num=str(count)+" were denied "+dy_op+mon_op+yr_op+q_op+"."
        return recvd_num
    except Exception as e:
        print("Exception in count deriving function="+str(e))

def chat_get_adjusted_par_claims(dur_list,provider_lst):
    
    try:
        dt=dur_list
        res=get_adjstd_claim_par_trend(dur_list,provider_lst)
        val_lst_rcvd=list(res["Value"])
        hdr_lst_rcvd=list(res["Header"])
        count=""        
        for c_i in range(0,len(val_lst_rcvd)):
            try:
                count=count+val_lst_rcvd[c_i]+" "+hdr_lst_rcvd[c_i].replace('0','participating').replace('1','non-participating')+" claims,"
            except:
                # count=count+0
                junk=1
        count=count[0:len(count)-1]                
        if len(dur_list)==4:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dur_list)==3:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num=str(count)+" were adjusted "+dy_op+mon_op+yr_op+q_op+"."
        return recvd_num
    except Exception as e:
        print("Exception in count deriving function="+str(e))


def chat_get_received_par_claims(dur_list,provider_lst):
    
    try:
        dt=dur_list
        res=get_rcvd_claim_par_trend(dur_list,provider_lst)
        val_lst_rcvd=list(res["Value"])
        hdr_lst_rcvd=list(res["Header"])
        count=""        
        for c_i in range(0,len(val_lst_rcvd)):
            try:
                count=count+val_lst_rcvd[c_i]+" "+hdr_lst_rcvd[c_i].replace('0','participating').replace('1','non-participating')+" claims,"
            except:
                # count=count+0
                junk=1
        count=count[0:len(count)-1]                
        if len(dur_list)==4:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dur_list)==3:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num=str(count)+" were received "+dy_op+mon_op+yr_op+q_op+"."
        return recvd_num
    except Exception as e:
        print("Exception in count deriving function="+str(e))

def chat_get_paid_par_claims(dur_list,provider_lst):
    
    try:
        dt=dur_list
        res=get_paid_claim_par_trend(dur_list,provider_lst)
        val_lst_rcvd=list(res["Value"])
        hdr_lst_rcvd=list(res["Header"])
        count=""        
        for c_i in range(0,len(val_lst_rcvd)):
            try:
                count=count+val_lst_rcvd[c_i]+" "+hdr_lst_rcvd[c_i].replace('0','participating').replace('1','non-participating')+" claims,"
            except:
                # count=count+0
                junk=1
        count=count[0:len(count)-1]                
        if len(dur_list)==4:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dur_list)==3:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num=str(count)+" were paid "+dy_op+mon_op+yr_op+q_op+"."
        return recvd_num
    except Exception as e:
        print("Exception in count deriving function="+str(e))

def chat_get_prtl_denied_type_claims(dur_list,provider_lst):
    
    try:
        dt=dur_list
        res=get_prtl_dend_claim_type_trend(dur_list,provider_lst)
        val_lst_rcvd=list(res["Value"])
        hdr_lst_rcvd=list(res["Header"])
        count=""        
        for c_i in range(0,len(val_lst_rcvd)):
            try:
                count=count+val_lst_rcvd[c_i]+" "+hdr_lst_rcvd[c_i].replace('M','Professional').replace('H','Facility')+" claims,"
            except:
                # count=count+0
                junk=1
        count=count[0:len(count)-1]                
        if len(dur_list)==4:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dur_list)==3:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num=str(count)+" were partial denied "+dy_op+mon_op+yr_op+q_op+"."
        return recvd_num
    except Exception as e:
        print("Exception in count deriving function="+str(e))

def chat_get_denied_type_claims(dur_list,provider_lst):
    
    try:
        dt=dur_list
        res=get_dend_claim_type_trend(dur_list,provider_lst)
        val_lst_rcvd=list(res["Value"])
        hdr_lst_rcvd=list(res["Header"])
        count=""        
        for c_i in range(0,len(val_lst_rcvd)):
            try:
                count=count+val_lst_rcvd[c_i]+" "+hdr_lst_rcvd[c_i].replace('M','Professional').replace('H','Facility')+" claims,"
            except:
                # count=count+0
                junk=1
        count=count[0:len(count)-1]                
        if len(dur_list)==4:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dur_list)==3:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num=str(count)+" were denied "+dy_op+mon_op+yr_op+q_op+"."
        return recvd_num
    except Exception as e:
        print("Exception in count deriving function="+str(e))

def chat_get_received_type_claims(dur_list,provider_lst):
    
    try:
        dt=dur_list
        res=get_rcvd_claim_type_trend(dur_list,provider_lst)
        val_lst_rcvd=list(res["Value"])
        hdr_lst_rcvd=list(res["Header"])
        count=""        
        for c_i in range(0,len(val_lst_rcvd)):
            try:
                count=count+val_lst_rcvd[c_i]+" "+hdr_lst_rcvd[c_i].replace('M','Professional').replace('H','Facility')+" claims,"
            except:
                # count=count+0
                junk=1
        count=count[0:len(count)-1]                
        if len(dur_list)==4:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dur_list)==3:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num=str(count)+" were received "+dy_op+mon_op+yr_op+q_op+"."
        return recvd_num
    except Exception as e:
        print("Exception in count deriving function="+str(e))

def chat_get_adjusted_type_claims(dur_list,provider_lst):
    
    try:
        dt=dur_list
        res=get_adjstd_claim_type_trend(dur_list,provider_lst)
        val_lst_rcvd=list(res["Value"])
        hdr_lst_rcvd=list(res["Header"])
        count=""        
        for c_i in range(0,len(val_lst_rcvd)):
            try:
                count=count+val_lst_rcvd[c_i]+" "+hdr_lst_rcvd[c_i].replace('M','Professional').replace('H','Facility')+" claims,"
            except:
                # count=count+0
                junk=1
        count=count[0:len(count)-1]                
        if len(dur_list)==4:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dur_list)==3:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num=str(count)+" were adjusted "+dy_op+mon_op+yr_op+q_op+"."
        return recvd_num
    except Exception as e:
        print("Exception in count deriving function="+str(e))

def chat_get_paid_type_claims(dur_list,provider_lst):
    
    try:
        dt=dur_list
        res=get_paid_claim_type_trend(dur_list,provider_lst)
        val_lst_rcvd=list(res["Value"])
        hdr_lst_rcvd=list(res["Header"])
        count=""        
        for c_i in range(0,len(val_lst_rcvd)):
            try:
                count=count+val_lst_rcvd[c_i]+" "+hdr_lst_rcvd[c_i].replace('M','Professional').replace('H','Facility')+" claims,"
            except:
                # count=count+0
                junk=1
        count=count[0:len(count)-1]                
        if len(dur_list)==4:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dur_list)==3:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num=str(count)+" were paid "+dy_op+mon_op+yr_op+q_op+"."
        return recvd_num
    except Exception as e:
        print("Exception in count deriving function="+str(e))

def chat_get_denial_reasons_trend_bar_archiv(dur_list,provider_lst):
    print("entered denial reasons trend bar for chat")
    try:
    # if True:
        # dt=dur_list
        print(str(dur_list))
        res=get_denial_reasons_trend_bar(dur_list,provider_lst)
        val_lst_rcvd=list(res["Value"])
        hdr_lst_rcvd=list(res["Header"])
        print(str(val_lst_rcvd))
        print(str(hdr_lst_rcvd))
        count=""        
        for c_i in range(0,len(val_lst_rcvd)):
            try:
                count=count+val_lst_rcvd[c_i]+" claims with reason "+hdr_lst_rcvd[c_i]+" ,"
            except:
                # count=count+0
                junk=1
        count=count[0:len(count)-1]                
        if len(dur_list)==4:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dur_list)==3:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num=str(count)+" were denied "+dy_op+mon_op+yr_op+q_op+"."
        return recvd_num
    except Exception as e:
        print("Exception in denial reasons deriving function="+str(e))

def chat_get_denial_reasons_trend_bar(dur_list,provider_lst):
    
    try:
        dt=dur_list
        res=get_denial_reasons_trend_bar(dur_list,provider_lst)
        val_lst_rcvd=list(res["Value"])
        hdr_lst_rcvd=list(res["Header"])
        count=""        
        for c_i in range(0,len(val_lst_rcvd)):
            try:
                count=count+val_lst_rcvd[c_i]+" claims with reason "+hdr_lst_rcvd[c_i]+" ,"
            except:
                # count=count+0
                junk=1
        count=count[0:len(count)-1]                
        if len(dur_list)==4:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dur_list)==3:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num=str(count)+" were denied "+dy_op+mon_op+yr_op+q_op+"."
        return recvd_num
    except Exception as e:
        print("Exception in count deriving function="+str(e))


def chat_get_prtl_denial_reasons_trend_bar(dur_list,provider_lst):
    
    try:
        dt=dur_list
        res=get_prtl_denial_reasons_trend_bar(dur_list,provider_lst)
        val_lst_rcvd=list(res["Value"])
        hdr_lst_rcvd=list(res["Header"])
        count=""        
        for c_i in range(0,len(val_lst_rcvd)):
            try:
                count=count+val_lst_rcvd[c_i]+" claims with reason "+hdr_lst_rcvd[c_i]+" ,"
            except:
                # count=count+0
                junk=1
        count=count[0:len(count)-1]                
        if len(dur_list)==4:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dur_list)==3:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num=str(count)+" were partial denied "+dy_op+mon_op+yr_op+q_op+"."
        return recvd_num
    except Exception as e:
        print("Exception in count deriving function="+str(e))

def chat_get_adjstd_reasons_trend_bar(dur_list,provider_lst):
    
    try:
        dt=dur_list
        res=get_adjstd_reasons_trend_bar(dur_list,provider_lst)
        val_lst_rcvd=list(res["Value"])
        hdr_lst_rcvd=list(res["Header"])
        count=""        
        for c_i in range(0,len(val_lst_rcvd)):
            try:
                count=count+val_lst_rcvd[c_i]+" claims with reason "+hdr_lst_rcvd[c_i]+" ,"
            except:
                # count=count+0
                junk=1
        count=count[0:len(count)-1]                
        if len(dur_list)==4:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dur_list)==3:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num=str(count)+" were adjusted "+dy_op+mon_op+yr_op+q_op+"."
        return recvd_num
    except Exception as e:
        print("Exception in count deriving function="+str(e))


def chat_get_recvd_billed_amt_claims(dur_list,provider_lst):
    try:
        dt=dur_list        
        res=get_rcvd_claim_val_trend(dur_list,provider_lst)
        val_lst_rcvd=list(res["Value"])
        count=0
        for c_i in val_lst_rcvd:
            try:
                count=count+float(c_i)
            except:
                count=count+0
        if len(dur_list)==4:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dur_list)==3:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num="The total billed amount for received claims was "+str(count)+" "+dy_op+mon_op+yr_op+q_op+"."
        return recvd_num
    except Exception as e:
        print("Exception in count deriving function="+str(e))

def chat_get_recvd_paid_amt_claims(dur_list,provider_lst):
    try:
        dt=dur_list        
        res=get_rcvd_claim_paid_val_trend(dur_list,provider_lst)
        val_lst_rcvd=list(res["Value"])
        count=0
        for c_i in val_lst_rcvd:
            try:
                count=count+float(c_i)
            except:
                count=count+0
        if len(dur_list)==4:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dur_list)==3:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num="The total paid amount for received claims was "+str(count)+" "+dy_op+mon_op+yr_op+q_op+"."
        return recvd_num
    except Exception as e:
        print("Exception in count deriving function="+str(e))

def chat_get_paid_paid_amt_claims(dur_list,provider_lst):
    try:
        dt=dur_list        
        res=get_paid_claim_val_trend(dur_list,provider_lst)
        val_lst_rcvd=list(res["Value"])
        count=0
        for c_i in val_lst_rcvd:
            try:
                count=count+float(c_i)
            except:
                count=count+0
        if len(dur_list)==4:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dur_list)==3:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num="The total paid amount for paid claims was "+str(count)+" "+dy_op+mon_op+yr_op+q_op+"."
        return recvd_num
    except Exception as e:
        print("Exception in count deriving function="+str(e))

def chat_get_paid_billed_amt_claims(dur_list,provider_lst):
    try:
        dt=dur_list        
        res=get_paid_claim_val_trend(dur_list,provider_lst)
        val_lst_rcvd=list(res["Value"])
        count=0
        for c_i in val_lst_rcvd:
            try:
                count=count+float(c_i)
            except:
                count=count+0
        if len(dur_list)==4:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dur_list)==3:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num="The total billed amount for paid claims was "+str(count)+" "+dy_op+mon_op+yr_op+q_op+"."
        return recvd_num
    except Exception as e:
        print("Exception in count deriving function="+str(e))

def chat_get_dend_billed_amt_claims(dur_list,provider_lst):
    try:
        dt=dur_list        
        res=get_dend_claim_val_trend(dur_list,provider_lst)
        val_lst_rcvd=list(res["Value"])
        count=0
        for c_i in val_lst_rcvd:
            try:
                count=count+float(c_i)
            except:
                count=count+0
        if len(dur_list)==4:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dur_list)==3:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num="The total billed amount for denied claims was "+str(count)+" "+dy_op+mon_op+yr_op+q_op+"."
        return recvd_num
    except Exception as e:
        print("Exception in count deriving function="+str(e))

def chat_get_dend_dend_amt_claims(dur_list,provider_lst):
    try:
        dt=dur_list        
        res=get_dend_claim_val_trend(dur_list,provider_lst)
        val_lst_rcvd=list(res["Value"])
        count=0
        for c_i in val_lst_rcvd:
            try:
                count=count+float(c_i)
            except:
                count=count+0
        if len(dur_list)==4:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dur_list)==3:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num="The total denied amount for denied claims was "+str(count)+" "+dy_op+mon_op+yr_op+q_op+"."
        return recvd_num
    except Exception as e:
        print("Exception in count deriving function="+str(e))

def chat_get_prtl_dend_billed_amt_claims(dur_list,provider_lst):
    try:
        dt=dur_list        
        res=get_prtl_dend_claim_val_trend(dur_list,provider_lst)
        val_lst_rcvd=list(res["Value"])
        count=0
        for c_i in val_lst_rcvd:
            try:
                count=count+float(c_i)
            except:
                count=count+0
        if len(dur_list)==4:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dur_list)==3:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num="The total billed amount for partial denied claims was }"+str(count)+"} "+dy_op+mon_op+yr_op+q_op+"."
        return recvd_num
    except Exception as e:
        print("Exception in count deriving function="+str(e))

def chat_get_prtl_dend_paid_amt_claims(dur_list,provider_lst):
    try:
        dt=dur_list        
        res=get_prtl_dend_claim_paid_val_trend(dur_list,provider_lst)
        val_lst_rcvd=list(res["Value"])
        count=0
        for c_i in val_lst_rcvd:
            try:
                count=count+float(c_i)
            except:
                count=count+0
        if len(dur_list)==4:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dur_list)==3:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num="The total paid amount for partial denied claims was }"+str(count)+"} "+dy_op+mon_op+yr_op+q_op+"."
        return recvd_num
    except Exception as e:
        print("Exception in count deriving function="+str(e))

def chat_get_prtl_dend_dend_amt_claims(dur_list,provider_lst):
    try:
        dt=dur_list        
        count_b=float(chat_get_prtl_dend_billed_amt_claims(dur_list,provider_lst).split('}')[1])
        count_p=float(chat_get_prtl_dend_paid_amt_claims(dur_list,provider_lst).split('}')[1])
        count=0
        count=count_b-count_p        
        if len(dur_list)==4:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dur_list)==3:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num="The total denied amount for partial denied claims was "+str(count)+" "+dy_op+mon_op+yr_op+q_op+"."
        return recvd_num
    except Exception as e:
        print("Exception in count deriving function="+str(e))

def chat_get_adjstd_paid_amt_claims(dur_list,provider_lst):
    try:
        dt=dur_list        
        res=get_adjstd_claim_val_trend(dur_list,provider_lst)
        val_lst_rcvd=list(res["Value"])
        count=0
        for c_i in val_lst_rcvd:
            try:
                count=count+float(c_i)
            except:
                count=count+0
        if len(dur_list)==4:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dur_list)==3:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num="The total paid amount for adjusted claims was }"+str(count)+"} "+dy_op+mon_op+yr_op+q_op+"."
        return recvd_num
    except Exception as e:
        print("Exception in count deriving function="+str(e))

def chat_get_adjstd_billed_amt_claims(dur_list,provider_lst):
    try:
        dt=dur_list        
        res=get_adjstd_claim_billed_val_trend(dur_list,provider_lst)
        val_lst_rcvd=list(res["Value"])
        count=0
        for c_i in val_lst_rcvd:
            try:
                count=count+float(c_i)
            except:
                count=count+0
        if len(dur_list)==4:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dur_list)==3:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num="The total billed amount for adjusted claims was }"+str(count)+"} "+dy_op+mon_op+yr_op+q_op+"."
        return recvd_num
    except Exception as e:
        print("Exception in count deriving function="+str(e))

def chat_get_adjstd_adjstd_amt_claims(dur_list,provider_lst):
    try:
        dt=dur_list        
        count_b=float(chat_get_adjstd_billed_amt_claims(dur_list,provider_lst).split('}')[1])
        count_p=float(chat_get_adjstd_paid_amt_claims(dur_list,provider_lst).split('}')[1])
        count=0
        count=count_b-count_p        
        if len(dur_list)==4:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dur_list)==3:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num="The total adjusted amount for adjusted claims was "+str(count)+" "+dy_op+mon_op+yr_op+q_op+"."
        return recvd_num
    except Exception as e:
        print("Exception in count deriving function="+str(e))

############# chat questions response using search questions call ###############

############ denied claims ##############
def get_denied_claims_cnt(dt,provider_lst):
    print(str(dt))
    try:        
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name] 
        n_records="0"
        cond=""
        if len(dt)==2:
            s1=str(dt[0])
            start = datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),0,0)
            s1=str(dt[1].split('}')[0])
            end = datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),0,0)
            print(start)
            print(end)
            if len(provider_lst)>0:
                pipe = [{'$match':{'$and':[{'paid_date_str':{'$gt':str(start),'$lt':str(end) }},{'payto_provider_tax_id':{'$in':provider_lst}},{'claim_denial_ind':'1'}]}},{'$group': {'_id':'$root_claim_num', 'total': {'$sum': 1 }}}] ## sum after type conversion of field            
            else:
                pipe = [{'$match':{'$and':[{'paid_date_str':{'$gt':str(start),'$lt':str(end) }},{'claim_denial_ind':'1'}]}},{'$group': {'_id':'$root_claim_num', 'total': {'$sum': 1 }}}] ## sum after type conversion of field            
            mydoc=(mycol.aggregate(pipeline=pipe))  
            den_claim_lst=list()                      
            for x in mydoc:
                den_claim_lst.append(str(x['_id']))
            if len(provider_lst) > 0:
               pipe = [{'$match':{'$and':[{'paid_date_str':{'$gt':str(start),'$lt':str(end) }},{'payto_provider_tax_id':{'$in':provider_lst}},{'claim_denial_ind':'0'}]}},{'$group': {'_id':'$root_claim_num', 'total': {'$sum': 1 }}}] ## sum after type conversion of field             
            else:
                pipe = [{'$match':{'$and':[{'paid_date_str':{'$gt':str(start),'$lt':str(end) }},{'claim_denial_ind':'0'}]}},{'$group': {'_id':'$root_claim_num', 'total': {'$sum': 1 }}}] ## sum after type conversion of field            
            mydoc=(mycol.aggregate(pipeline=pipe))  
            non_den_claim_lst=list()                      
            for x in mydoc:
                non_den_claim_lst.append(str(x['_id']))
            fin_den_lst=list()
            for dc in den_claim_lst:
                if dc not in non_den_claim_lst:
                    fin_den_lst.append(dc)
            n_records=str(len(fin_den_lst))
        elif len(dt)==3:                       
            cond=""
            if len(dt[0])==0:
                cond=cond+",{'paid_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[0]:
                    cond=cond+",{'paid_date_str':{'$regex':'.*-.*-"+str(dy)+".*'}}"
                
            if len(dt[1])==0:
                cond=cond+",{'paid_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[1]:
                    cond=cond+",{'paid_date_str':{'$regex':'.*-"+str(dy)+"-.*'}}"
                
            if len(dt[2])==0:
                cond=cond+",{'paid_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[2]:
                    cond=cond+",{'paid_date_str':{'$regex':'"+str(dy)+"-.*-.*'}}"
            if len(provider_lst)>0:
                pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                cond1="{'$and':["+cond[1:]+pc+",{'claim_denial_ind':'1' }"+"]}"
            else:
                cond1="{'$and':["+cond[1:]+",{'claim_denial_ind':'1' }"+"]}"
            my_dict = ast.literal_eval(cond1)
            pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num', 'total': {'$sum': 1 }}}] ## sum after type conversion of field 
            mydoc=(mycol.aggregate(pipeline=pipe))                       
            den_claim_lst=list()                      
            for x in mydoc:
                den_claim_lst.append(str(x['_id']))
            if len(provider_lst)>0:
                pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                cond1="{'$and':["+cond[1:]+pc+",{'claim_denial_ind':'0' }"+"]}"
            else:
                cond1="{'$and':["+cond[1:]+",{'claim_denial_ind':'0' }"+"]}"
            my_dict = ast.literal_eval(cond1)
            pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num', 'total': {'$sum': 1 }}}] ## sum after type conversion of field 
            mydoc=(mycol.aggregate(pipeline=pipe))                       
            non_den_claim_lst=list()                      
            for x in mydoc:
                non_den_claim_lst.append(str(x['_id']))
            fin_den_lst=list()
            for dc in den_claim_lst:
                if dc not in non_den_claim_lst:
                    fin_den_lst.append(dc)
            n_records=str(len(fin_den_lst))
              
        print(cond)    
        
        if len(dt)==3:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dt)==2:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num=str(n_records)+" claims were denied "+dy_op+mon_op+yr_op+q_op+"."
        return recvd_num

    except Exception as e:
        print(str(e))      
        return "Sorry, Could not fetch you results at this time"

############ denied claims ##############

############ denied claims billed amount##############
def get_bill_amt_dend(dt,provider_lst):
    print(str(dt))
    try:        
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name] 
        n_records="0"
        cond=""
        if len(dt)==2:
            s1=str(dt[0])
            start = datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),0,0)
            s1=str(dt[1].split('}')[0])
            end = datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),0,0)
            print(start)
            print(end)
            if len(provider_lst) > 0:
                pipe = [{'$match':{'$and':[{'paid_date_str':{'$gt':str(start),'$lt':str(end) }},{'payto_provider_tax_id':{'$in':provider_lst}},{'claim_denial_ind':'1'}]}},{'$group': {'_id':'$root_claim_num','total': {'$sum': {'$convert':{'input':'$amt_billed','to':'double'}}}}}]
            else:
                pipe = [{'$match':{'$and':[{'paid_date_str':{'$gt':str(start),'$lt':str(end) }},{'claim_denial_ind':'1'}]}},{'$group': {'_id':'$root_claim_num','total': {'$sum': {'$convert':{'input':'$amt_billed','to':'double'}}}}}]
            mydoc=(mycol.aggregate(pipeline=pipe))                                   
            den_claim_lst=list()                      
            for x in mydoc:
                den_claim_lst.append(str(x['_id'])+"!"+str(x['total']))
            if len(provider_lst) > 0:
                pipe = [{'$match':{'$and':[{'paid_date_str':{'$gt':str(start),'$lt':str(end) }},{'payto_provider_tax_id':{'$in':provider_lst}},{'claim_denial_ind':'0'}]}},{'$group': {'_id':'$root_claim_num','total': {'$sum': {'$convert':{'input':'$amt_billed','to':'double'}}}}}]
            else:
                pipe = [{'$match':{'$and':[{'paid_date_str':{'$gt':str(start),'$lt':str(end) }},{'claim_denial_ind':'0'}]}},{'$group': {'_id':'$root_claim_num','total': {'$sum': {'$convert':{'input':'$amt_billed','to':'double'}}}}}]
            mydoc=(mycol.aggregate(pipeline=pipe))  
            non_den_claim_lst=list()                      
            for x in mydoc:
                non_den_claim_lst.append(str(x['_id'])+"!"+str(x['total'])) 
            n_records='0'           
            for dc in den_claim_lst:
                d=dc.split('!')
                c=0
                for di in range(0,len(non_den_claim_lst)):
                    if d[0]==non_den_claim_lst[di].split('!')[0]:
                        c=1
                if c==0:
                    n_records=str(float(n_records)+float(d[1]))
        elif len(dt)==3:                       
            cond=""
            if len(dt[0])==0:
                cond=cond+",{'paid_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[0]:
                    cond=cond+",{'paid_date_str':{'$regex':'.*-.*-"+str(dy)+".*'}}"
                
            if len(dt[1])==0:
                cond=cond+",{'paid_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[1]:
                    cond=cond+",{'paid_date_str':{'$regex':'.*-"+str(dy)+"-.*'}}"
                
            if len(dt[2])==0:
                cond=cond+",{'paid_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[2]:
                    cond=cond+",{'paid_date_str':{'$regex':'"+str(dy)+"-.*-.*'}}"
            if len(provider_lst) > 0:
                pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                cond1="{'$and':["+cond[1:]+pc+",{'claim_denial_ind':'1' }"+"]}"
            else:
                cond1="{'$and':["+cond[1:]+",{'claim_denial_ind':'1' }"+"]}"
            my_dict = ast.literal_eval(cond1)
            pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num','total': {'$sum': {'$convert':{'input':'$amt_billed','to':'double'}}}}}]
            mydoc=(mycol.aggregate(pipeline=pipe))                       
            den_claim_lst=list()                      
            for x in mydoc:
                den_claim_lst.append(str(x['_id'])+"!"+str(x['total']))
            if len(provider_lst) > 0:
                pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                cond1="{'$and':["+cond[1:]+pc+",{'claim_denial_ind':'0' }"+"]}"
            else:
                cond1="{'$and':["+cond[1:]+",{'claim_denial_ind':'0' }"+"]}"
            my_dict = ast.literal_eval(cond1)
            pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num','total': {'$sum': {'$convert':{'input':'$amt_billed','to':'double'}}}}}]
            mydoc=(mycol.aggregate(pipeline=pipe))                       
            non_den_claim_lst=list()                      
            for x in mydoc:
                non_den_claim_lst.append(str(x['_id'])+"!"+str(x['total'])) 
            n_records='0'           
            for dc in den_claim_lst:
                d=dc.split('!')
                c=0
                for di in range(0,len(non_den_claim_lst)):
                    if d[0]==non_den_claim_lst[di].split('!')[0]:
                        c=1
                if c==0:
                    n_records=str(float(n_records)+float(d[1]))
            
              
        print(cond)    
        
        if len(dt)==3:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dt)==2:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num="The total billed amount for the denied claims was "+str(n_records)+" "+dy_op+mon_op+yr_op+q_op+"."
        return recvd_num

    except Exception as e:
        print(str(e))      
        return "Sorry, Could not fetch you results at this time"

############ denied claims billed amount ##############

############ denied claims submission mode##############
def get_mode_submission_dend(dt,provider_lst):
    print(str(dt))
    try:        
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name] 
        n_records_edi="0"
        n_records_ppr="0"
        cond=""
        if len(dt)==2:
            s1=str(dt[0])
            start = datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),0,0)
            s1=str(dt[1].split('}')[0])
            end = datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),0,0)
            print(start)
            print(end)
            if len(provider_lst) > 0:
                pipe = [{'$match':{'$and':[{'paid_date_str':{'$gt':str(start),'$lt':str(end) }},{'payto_provider_tax_id':{'$in':provider_lst}},{'claim_denial_ind':'1'}]}},{'$group': {'_id':'$root_claim_num','total': {'$max': {'$convert':{'input':'$claim_receipt_type_cd','to':'string'}}}}}]
            else:
                pipe = [{'$match':{'$and':[{'paid_date_str':{'$gt':str(start),'$lt':str(end) }},{'claim_denial_ind':'1'}]}},{'$group': {'_id':'$root_claim_num','total': {'$max': {'$convert':{'input':'$claim_receipt_type_cd','to':'string'}}}}}]
            mydoc=(mycol.aggregate(pipeline=pipe))                                   
            den_claim_lst=list()                      
            for x in mydoc:
                den_claim_lst.append(str(x['_id'])+"!"+str(x['total']))
            if len(provider_lst) > 0:
                pipe = [{'$match':{'$and':[{'paid_date_str':{'$gt':str(start),'$lt':str(end) }},{'payto_provider_tax_id':{'$in':provider_lst}},{'claim_denial_ind':'0'}]}},{'$group': {'_id':'$root_claim_num','total': {'$max': {'$convert':{'input':'$claim_receipt_type_cd','to':'string'}}}}}]
            else:
                pipe = [{'$match':{'$and':[{'paid_date_str':{'$gt':str(start),'$lt':str(end) }},{'claim_denial_ind':'0'}]}},{'$group': {'_id':'$root_claim_num','total': {'$max': {'$convert':{'input':'$claim_receipt_type_cd','to':'string'}}}}}]
            mydoc=(mycol.aggregate(pipeline=pipe))  
            non_den_claim_lst=list()                      
            for x in mydoc:
                non_den_claim_lst.append(str(x['_id'])+"!"+str(x['total'])) 
            n_records_edi='0'           
            n_records_ppr='0'
            for dc in den_claim_lst:
                d=dc.split('!')
                c=0
                for di in range(0,len(non_den_claim_lst)):
                    if d[0]==non_den_claim_lst[di].split('!')[0]:
                        c=1
                if c==0:
                    if d[1].strip(' ').upper()=='EDI':
                        n_records_edi=str(int(n_records_edi)+1)
                    else:
                        n_records_ppr=str(int(n_records_ppr)+1)
        elif len(dt)==3:                       
            cond=""
            if len(dt[0])==0:
                cond=cond+",{'paid_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[0]:
                    cond=cond+",{'paid_date_str':{'$regex':'.*-.*-"+str(dy)+".*'}}"
                
            if len(dt[1])==0:
                cond=cond+",{'paid_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[1]:
                    cond=cond+",{'paid_date_str':{'$regex':'.*-"+str(dy)+"-.*'}}"
                
            if len(dt[2])==0:
                cond=cond+",{'paid_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[2]:
                    cond=cond+",{'paid_date_str':{'$regex':'"+str(dy)+"-.*-.*'}}"
            if len(provider_lst) > 0:
                pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                cond1="{'$and':["+cond[1:]+pc+",{'claim_denial_ind':'1' }"+"]}"
            else:
                cond1="{'$and':["+cond[1:]+",{'claim_denial_ind':'1' }"+"]}"
            my_dict = ast.literal_eval(cond1)
            pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num','total': {'$max': {'$convert':{'input':'$claim_receipt_type_cd','to':'string'}}}}}]
            mydoc=(mycol.aggregate(pipeline=pipe))                       
            den_claim_lst=list()                      
            for x in mydoc:
                den_claim_lst.append(str(x['_id'])+"!"+str(x['total']))
            if len(provider_lst) > 0:
                pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                cond1="{'$and':["+cond[1:]+pc+",{'claim_denial_ind':'0' }"+"]}"
            else:
                cond1="{'$and':["+cond[1:]+",{'claim_denial_ind':'0' }"+"]}"
            my_dict = ast.literal_eval(cond1)
            pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num','total': {'$max': {'$convert':{'input':'$claim_receipt_type_cd','to':'string'}}}}}]
            mydoc=(mycol.aggregate(pipeline=pipe))                       
            non_den_claim_lst=list()                      
            for x in mydoc:
                non_den_claim_lst.append(str(x['_id'])+"!"+str(x['total'])) 
            n_records_edi='0'           
            n_records_ppr='0'
            for dc in den_claim_lst:
                d=dc.split('!')
                c=0
                for di in range(0,len(non_den_claim_lst)):
                    if d[0]==non_den_claim_lst[di].split('!')[0]:
                        c=1
                if c==0:
                    if d[1].strip(' ').upper()=='EDI':
                        n_records_edi=str(int(n_records_edi)+1)
                    else:
                        n_records_ppr=str(int(n_records_ppr)+1)
            
              
        print(cond)    
        
        if len(dt)==3:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dt)==2:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num=n_records_edi+" claims were submitted on EDI and "+n_records_ppr+" claims were submitted on PPR"
        return recvd_num

    except Exception as e:
        print(str(e))      
        return "Sorry, Could not fetch you results at this time"

############ denied claims submission mode##############

############ partial  denied claims ##############
def get_prtl_denied_claims_cnt(dt,provider_lst):
    print(str(dt))
    try:        
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name] 
        n_records="0"
        cond=""
        if len(dt)==2:
            s1=str(dt[0])
            start = datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),0,0)
            s1=str(dt[1].split('}')[0])
            end = datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),0,0)
            print(start)
            print(end)
            if len(provider_lst) > 0:
                pipe = [{'$match':{'$and':[{'paid_date_str':{'$gt':str(start),'$lt':str(end) }},{'payto_provider_tax_id':{'$in':provider_lst}},{'claim_denial_ind':'1'}]}},{'$group': {'_id':'$root_claim_num', 'total': {'$sum': 1 }}}] ## sum after type conversion of field            
            else:
                pipe = [{'$match':{'$and':[{'paid_date_str':{'$gt':str(start),'$lt':str(end) }},{'claim_denial_ind':'1'}]}},{'$group': {'_id':'$root_claim_num', 'total': {'$sum': 1 }}}] ## sum after type conversion of field            
            mydoc=(mycol.aggregate(pipeline=pipe))  
            den_claim_lst=list()                      
            for x in mydoc:
                den_claim_lst.append(str(x['_id']))
            if len(provider_lst) > 0:
                pipe = [{'$match':{'$and':[{'paid_date_str':{'$gt':str(start),'$lt':str(end) }},{'payto_provider_tax_id':{'$in':provider_lst}},{'claim_denial_ind':'0'}]}},{'$group': {'_id':'$root_claim_num', 'total': {'$sum': 1 }}}] ## sum after type conversion of field            
            else:
                pipe = [{'$match':{'$and':[{'paid_date_str':{'$gt':str(start),'$lt':str(end) }},{'claim_denial_ind':'0'}]}},{'$group': {'_id':'$root_claim_num', 'total': {'$sum': 1 }}}] ## sum after type conversion of field            
            
            mydoc=(mycol.aggregate(pipeline=pipe))  
            non_den_claim_lst=list()                      
            for x in mydoc:
                non_den_claim_lst.append(str(x['_id']))
            fin_den_lst=list()
            for dc in den_claim_lst:
                if dc in non_den_claim_lst:
                    fin_den_lst.append(dc)
            n_records=str(len(fin_den_lst))
        elif len(dt)==3:                       
            cond=""
            if len(dt[0])==0:
                cond=cond+",{'paid_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[0]:
                    cond=cond+",{'paid_date_str':{'$regex':'.*-.*-"+str(dy)+".*'}}"
                
            if len(dt[1])==0:
                cond=cond+",{'paid_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[1]:
                    cond=cond+",{'paid_date_str':{'$regex':'.*-"+str(dy)+"-.*'}}"
                
            if len(dt[2])==0:
                cond=cond+",{'paid_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[2]:
                    cond=cond+",{'paid_date_str':{'$regex':'"+str(dy)+"-.*-.*'}}"
            if len(provider_lst)>0:
                pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                cond1="{'$and':["+cond[1:]+pc+",{'claim_denial_ind':'1' }"+"]}"
            else:
                cond1="{'$and':["+cond[1:]+",{'claim_denial_ind':'1' }"+"]}"
            my_dict = ast.literal_eval(cond1)
            pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num', 'total': {'$sum': 1 }}}] ## sum after type conversion of field 
            mydoc=(mycol.aggregate(pipeline=pipe))                       
            den_claim_lst=list()                      
            for x in mydoc:
                den_claim_lst.append(str(x['_id']))
            cond1="{'$and':["+cond[1:]+",{'claim_denial_ind':'0' }"+"]}"
            my_dict = ast.literal_eval(cond1)
            pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num', 'total': {'$sum': 1 }}}] ## sum after type conversion of field 
            mydoc=(mycol.aggregate(pipeline=pipe))                       
            non_den_claim_lst=list()                      
            for x in mydoc:
                non_den_claim_lst.append(str(x['_id']))
            fin_den_lst=list()
            for dc in den_claim_lst:
                if dc in non_den_claim_lst:
                    fin_den_lst.append(dc)
            n_records=str(len(fin_den_lst))
              
        print(cond)    
        
        if len(dt)==3:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dt)==2:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num=str(n_records)+" claims were partial denied "+dy_op+mon_op+yr_op+q_op+"."
        return recvd_num

    except Exception as e:
        print(str(e))      
        return "Sorry, Could not fetch you results at this time"

############ partial denied claims ##############

############ partial denied claims billed amount##############
def get_bill_amt_prtl_dend(dt,provider_lst):
    print(str(dt))
    try:        
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name] 
        n_records="0"
        cond=""
        if len(dt)==2:
            s1=str(dt[0])
            start = datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),0,0)
            s1=str(dt[1].split('}')[0])
            end = datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),0,0)
            print(start)
            print(end)
            if len(provider_lst) > 0: 
                pipe = [{'$match':{'$and':[{'paid_date_str':{'$gt':str(start),'$lt':str(end) }},{'payto_provider_tax_id':{'$in':provider_lst}},{'claim_denial_ind':'1'}]}},{'$group': {'_id':'$root_claim_num','total': {'$sum': {'$convert':{'input':'$amt_billed','to':'double'}}}}}]
            else:
                pipe = [{'$match':{'$and':[{'paid_date_str':{'$gt':str(start),'$lt':str(end) }},{'claim_denial_ind':'1'}]}},{'$group': {'_id':'$root_claim_num','total': {'$sum': {'$convert':{'input':'$amt_billed','to':'double'}}}}}]
            mydoc=(mycol.aggregate(pipeline=pipe))                                   
            den_claim_lst=list()                      
            for x in mydoc:
                den_claim_lst.append(str(x['_id'])+"!"+str(x['total']))
            if len(provider_lst) > 0: 
                pipe = [{'$match':{'$and':[{'paid_date_str':{'$gt':str(start),'$lt':str(end) }},{'payto_provider_tax_id':{'$in':provider_lst}},{'claim_denial_ind':'0'}]}},{'$group': {'_id':'$root_claim_num','total': {'$sum': {'$convert':{'input':'$amt_billed','to':'double'}}}}}]
            else:
                pipe = [{'$match':{'$and':[{'paid_date_str':{'$gt':str(start),'$lt':str(end) }},{'claim_denial_ind':'0'}]}},{'$group': {'_id':'$root_claim_num','total': {'$sum': {'$convert':{'input':'$amt_billed','to':'double'}}}}}]
            mydoc=(mycol.aggregate(pipeline=pipe))  
            non_den_claim_lst=list()                      
            for x in mydoc:
                non_den_claim_lst.append(str(x['_id'])+"!"+str(x['total'])) 
            n_records='0'           
            for dc in den_claim_lst:
                d=dc.split('!')
                c=0
                for di in range(0,len(non_den_claim_lst)):
                    if d[0]==non_den_claim_lst[di].split('!')[0]:
                        c=1
                if c==1:
                    n_records=str(float(n_records)+float(d[1]))
        elif len(dt)==3:                       
            cond=""
            if len(dt[0])==0:
                cond=cond+",{'paid_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[0]:
                    cond=cond+",{'paid_date_str':{'$regex':'.*-.*-"+str(dy)+".*'}}"
                
            if len(dt[1])==0:
                cond=cond+",{'paid_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[1]:
                    cond=cond+",{'paid_date_str':{'$regex':'.*-"+str(dy)+"-.*'}}"
                
            if len(dt[2])==0:
                cond=cond+",{'paid_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[2]:
                    cond=cond+",{'paid_date_str':{'$regex':'"+str(dy)+"-.*-.*'}}"
            if len(provider_lst) > 0:
                pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                cond1="{'$and':["+cond[1:]+pc+",{'claim_denial_ind':'1' }"+"]}"
            else:
                cond1="{'$and':["+cond[1:]+",{'claim_denial_ind':'1' }"+"]}"
            my_dict = ast.literal_eval(cond1)
            pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num','total': {'$sum': {'$convert':{'input':'$amt_billed','to':'double'}}}}}]
            mydoc=(mycol.aggregate(pipeline=pipe))                       
            den_claim_lst=list()                      
            for x in mydoc:
                den_claim_lst.append(str(x['_id'])+"!"+str(x['total']))
            if len(provider_lst) > 0:
                pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                cond1="{'$and':["+cond[1:]+pc+",{'claim_denial_ind':'0' }"+"]}"
            else:
                cond1="{'$and':["+cond[1:]+",{'claim_denial_ind':'0' }"+"]}"
            my_dict = ast.literal_eval(cond1)
            pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num','total': {'$sum': {'$convert':{'input':'$amt_billed','to':'double'}}}}}]
            mydoc=(mycol.aggregate(pipeline=pipe))                       
            non_den_claim_lst=list()                      
            for x in mydoc:
                non_den_claim_lst.append(str(x['_id'])+"!"+str(x['total'])) 
            n_records='0'           
            for dc in den_claim_lst:
                d=dc.split('!')
                c=0
                for di in range(0,len(non_den_claim_lst)):
                    if d[0]==non_den_claim_lst[di].split('!')[0]:
                        c=1
                if c==1:
                    n_records=str(float(n_records)+float(d[1]))
            
              
        print(cond)    
        
        if len(dt)==3:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dt)==2:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num="The total billed amount for the partial denied claims was "+str(n_records)+" "+dy_op+mon_op+yr_op+q_op+"."
        return recvd_num

    except Exception as e:
        print(str(e))     
        return "Sorry, Could not fetch you results at this time"

############ partial denied claims billed amount ##############


############ partial denied claims paid amount##############
def get_paid_amt_prtl_dend(dt,provider_lst):
    print(str(dt))
    try:        
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name] 
        n_records="0"
        cond=""
        if len(dt)==2:
            s1=str(dt[0])
            start = datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),0,0)
            s1=str(dt[1].split('}')[0])
            end = datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),0,0)
            print(start)
            print(end)
            if len(provider_lst) > 0:
                pipe = [{'$match':{'$and':[{'paid_date_str':{'$gt':str(start),'$lt':str(end) }},{'payto_provider_tax_id':{'$in':provider_lst}},{'claim_denial_ind':'1'}]}},{'$group': {'_id':'$root_claim_num','total': {'$sum': {'$convert':{'input':'$amt_paid','to':'double'}}}}}]
            else:
                pipe = [{'$match':{'$and':[{'paid_date_str':{'$gt':str(start),'$lt':str(end) }},{'claim_denial_ind':'1'}]}},{'$group': {'_id':'$root_claim_num','total': {'$sum': {'$convert':{'input':'$amt_paid','to':'double'}}}}}]
            mydoc=(mycol.aggregate(pipeline=pipe))                                   
            den_claim_lst=list()                      
            for x in mydoc:
                den_claim_lst.append(str(x['_id'])+"!"+str(x['total']))
            if len(provider_lst) > 0:
                pipe = [{'$match':{'$and':[{'paid_date_str':{'$gt':str(start),'$lt':str(end) }},{'payto_provider_tax_id':{'$in':provider_lst}},{'claim_denial_ind':'0'}]}},{'$group': {'_id':'$root_claim_num','total': {'$sum': {'$convert':{'input':'$amt_paid','to':'double'}}}}}]
            else:
                pipe = [{'$match':{'$and':[{'paid_date_str':{'$gt':str(start),'$lt':str(end) }},{'claim_denial_ind':'0'}]}},{'$group': {'_id':'$root_claim_num','total': {'$sum': {'$convert':{'input':'$amt_paid','to':'double'}}}}}]
            
            mydoc=(mycol.aggregate(pipeline=pipe))  
            non_den_claim_lst=list()                      
            for x in mydoc:
                non_den_claim_lst.append(str(x['_id'])+"!"+str(x['total'])) 
            n_records='0'           
            for dc in den_claim_lst:
                d=dc.split('!')
                c=0
                for di in range(0,len(non_den_claim_lst)):
                    if d[0]==non_den_claim_lst[di].split('!')[0]:
                        c=1
                if c==1:
                    n_records=str(float(n_records)+float(d[1]))
        elif len(dt)==3:                       
            cond=""
            if len(dt[0])==0:
                cond=cond+",{'paid_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[0]:
                    cond=cond+",{'paid_date_str':{'$regex':'.*-.*-"+str(dy)+".*'}}"
                
            if len(dt[1])==0:
                cond=cond+",{'paid_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[1]:
                    cond=cond+",{'paid_date_str':{'$regex':'.*-"+str(dy)+"-.*'}}"
                
            if len(dt[2])==0:
                cond=cond+",{'paid_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[2]:
                    cond=cond+",{'paid_date_str':{'$regex':'"+str(dy)+"-.*-.*'}}"
            if len(provider_lst) > 0:
                pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                cond1="{'$and':["+cond[1:]+pc+",{'claim_denial_ind':'1' }"+"]}"
            else:
                cond1="{'$and':["+cond[1:]+",{'claim_denial_ind':'1' }"+"]}"
            my_dict = ast.literal_eval(cond1)
            pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num','total': {'$sum': {'$convert':{'input':'$amt_paid','to':'double'}}}}}]
            mydoc=(mycol.aggregate(pipeline=pipe))                       
            den_claim_lst=list()                      
            for x in mydoc:
                den_claim_lst.append(str(x['_id'])+"!"+str(x['total']))
            if len(provider_lst) > 0:
                pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                cond1="{'$and':["+cond[1:]+pc+",{'claim_denial_ind':'0' }"+"]}"
            else:
                cond1="{'$and':["+cond[1:]+",{'claim_denial_ind':'0' }"+"]}"
            my_dict = ast.literal_eval(cond1)
            pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num','total': {'$sum': {'$convert':{'input':'$amt_paid','to':'double'}}}}}]
            mydoc=(mycol.aggregate(pipeline=pipe))                       
            non_den_claim_lst=list()                      
            for x in mydoc:
                non_den_claim_lst.append(str(x['_id'])+"!"+str(x['total'])) 
            n_records='0'           
            for dc in den_claim_lst:
                d=dc.split('!')
                c=0
                for di in range(0,len(non_den_claim_lst)):
                    if d[0]==non_den_claim_lst[di].split('!')[0]:
                        c=1
                if c==1:
                    n_records=str(float(n_records)+float(d[1]))
            
              
        print(cond)    
        
        if len(dt)==3:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dt)==2:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num="The total paid amount for the partial denied claims was "+str(n_records)+" "+dy_op+mon_op+yr_op+q_op+"."
        return recvd_num

    except Exception as e:
        print(str(e))        
        return "Sorry, Could not fetch you results at this time"

############ partial denied claims paid amount ##############


############ partial denied claims submission mode##############
def get_mode_submission_prtl_dend(dt,provider_lst):
    print(str(dt))
    try:        
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name] 
        n_records_edi="0"
        n_records_ppr="0"
        cond=""
        if len(dt)==2:
            s1=str(dt[0])
            start = datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),0,0)
            s1=str(dt[1].split('}')[0])
            end = datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),0,0)
            print(start)
            print(end)
            
            if len(provider_lst) > 0:
                pipe = [{'$match':{'$and':[{'paid_date_str':{'$gt':str(start),'$lt':str(end) }},{'payto_provider_tax_id':{'$in':provider_lst}},{'claim_denial_ind':'1'}]}},{'$group': {'_id':'$root_claim_num','total': {'$max': {'$convert':{'input':'$claim_receipt_type_cd','to':'string'}}}}}]
            else:
                pipe = [{'$match':{'$and':[{'paid_date_str':{'$gt':str(start),'$lt':str(end) }},{'claim_denial_ind':'1'}]}},{'$group': {'_id':'$root_claim_num','total': {'$max': {'$convert':{'input':'$claim_receipt_type_cd','to':'string'}}}}}]
            
            mydoc=(mycol.aggregate(pipeline=pipe))                                   
            den_claim_lst=list()                      
            for x in mydoc:
                den_claim_lst.append(str(x['_id'])+"!"+str(x['total']))
            if len(provider_lst) > 0:
                pipe = [{'$match':{'$and':[{'paid_date_str':{'$gt':str(start),'$lt':str(end) }},{'payto_provider_tax_id':{'$in':provider_lst}},{'claim_denial_ind':'0'}]}},{'$group': {'_id':'$root_claim_num','total': {'$max': {'$convert':{'input':'$claim_receipt_type_cd','to':'string'}}}}}]
            else:
                pipe = [{'$match':{'$and':[{'paid_date_str':{'$gt':str(start),'$lt':str(end) }},{'claim_denial_ind':'0'}]}},{'$group': {'_id':'$root_claim_num','total': {'$max': {'$convert':{'input':'$claim_receipt_type_cd','to':'string'}}}}}]
            
            mydoc=(mycol.aggregate(pipeline=pipe))  
            non_den_claim_lst=list()                      
            for x in mydoc:
                non_den_claim_lst.append(str(x['_id'])+"!"+str(x['total'])) 
            n_records_edi='0'           
            n_records_ppr='0'
            for dc in den_claim_lst:
                d=dc.split('!')
                c=0
                for di in range(0,len(non_den_claim_lst)):
                    if d[0]==non_den_claim_lst[di].split('!')[0]:
                        c=1
                if c==1:
                    if d[1].strip(' ').upper()=='EDI':
                        n_records_edi=str(int(n_records_edi)+1)
                    else:
                        n_records_ppr=str(int(n_records_ppr)+1)
        elif len(dt)==3:                       
            cond=""
            if len(dt[0])==0:
                cond=cond+",{'paid_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[0]:
                    cond=cond+",{'paid_date_str':{'$regex':'.*-.*-"+str(dy)+".*'}}"
                
            if len(dt[1])==0:
                cond=cond+",{'paid_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[1]:
                    cond=cond+",{'paid_date_str':{'$regex':'.*-"+str(dy)+"-.*'}}"
                
            if len(dt[2])==0:
                cond=cond+",{'paid_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[2]:
                    cond=cond+",{'paid_date_str':{'$regex':'"+str(dy)+"-.*-.*'}}"
            if len(provider_lst) > 0:
                pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                cond1="{'$and':["+cond[1:]+pc+",{'claim_denial_ind':'1' }"+"]}"
            else:
                cond1="{'$and':["+cond[1:]+",{'claim_denial_ind':'1' }"+"]}"
            my_dict = ast.literal_eval(cond1)
            pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num','total': {'$max': {'$convert':{'input':'$claim_receipt_type_cd','to':'string'}}}}}]
            mydoc=(mycol.aggregate(pipeline=pipe))                       
            den_claim_lst=list()                      
            for x in mydoc:
                den_claim_lst.append(str(x['_id'])+"!"+str(x['total']))
            if len(provider_lst) > 0:
                pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                cond1="{'$and':["+cond[1:]+pc+",{'claim_denial_ind':'0' }"+"]}"
            else:
                cond1="{'$and':["+cond[1:]+",{'claim_denial_ind':'0' }"+"]}"
            my_dict = ast.literal_eval(cond1)
            pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num','total': {'$max': {'$convert':{'input':'$claim_receipt_type_cd','to':'string'}}}}}]
            mydoc=(mycol.aggregate(pipeline=pipe))                       
            non_den_claim_lst=list()                      
            for x in mydoc:
                non_den_claim_lst.append(str(x['_id'])+"!"+str(x['total'])) 
            n_records_edi='0'           
            n_records_ppr='0'
            for dc in den_claim_lst:
                d=dc.split('!')
                c=0
                for di in range(0,len(non_den_claim_lst)):
                    if d[0]==non_den_claim_lst[di].split('!')[0]:
                        c=1
                if c==1:
                    if d[1].strip(' ').upper()=='EDI':
                        n_records_edi=str(int(n_records_edi)+1)
                    else:
                        n_records_ppr=str(int(n_records_ppr)+1)
            
              
        print(cond)    
        
        if len(dt)==3:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dt)==2:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num=n_records_edi+" claims were submitted on EDI and "+n_records_ppr+" claims were submitted on PPR"
        return recvd_num

    except Exception as e:
        print(str(e))      
        return "Sorry, Could not fetch you results at this time"

############ partial denied claims submission mode##############

############ Adjusted claims count ##############
def get_adjusted_claims_cnt(dt,provider_lst):
    print(str(dt))
    try:        
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name] 
        n_records="0"
        cond=""
        if len(dt)==2:
            s1=str(dt[0])
            start = datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),0,0)
            s1=str(dt[1].split('}')[0])
            end = datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),0,0)
            print(start)
            print(end)
            if len(provider_lst) > 0:
                pipe = [{'$match':{'$and':[{'paid_date_str':{'$gt':str(start),'$lt':str(end) }},{'payto_provider_tax_id':{'$in':provider_lst}},{'claim_adj_ind':'1'}]}},{'$group': {'_id':'$root_claim_num', 'total': {'$sum': 1 }}}] ## sum after type conversion of field            
            else:
                pipe = [{'$match':{'$and':[{'paid_date_str':{'$gt':str(start),'$lt':str(end) }},{'claim_adj_ind':'1'}]}},{'$group': {'_id':'$root_claim_num', 'total': {'$sum': 1 }}}] ## sum after type conversion of field            
            mydoc=(mycol.aggregate(pipeline=pipe)) 
            c=0
            for x in mydoc:
                c=c+1 
            n_records=str(c)
        elif len(dt)==3:                       
            cond=""
            if len(dt[0])==0:
                cond=cond+",{'paid_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[0]:
                    cond=cond+",{'paid_date_str':{'$regex':'.*-.*-"+str(dy)+".*'}}"
                
            if len(dt[1])==0:
                cond=cond+",{'paid_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[1]:
                    cond=cond+",{'paid_date_str':{'$regex':'.*-"+str(dy)+"-.*'}}"
                
            if len(dt[2])==0:
                cond=cond+",{'paid_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[2]:
                    cond=cond+",{'paid_date_str':{'$regex':'"+str(dy)+"-.*-.*'}}"
            if len(provider_lst) > 0:
                pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                cond1="{'$and':["+cond[1:]+pc+",{'claim_adj_ind':'1' }"+"]}"
            else:
                cond1="{'$and':["+cond[1:]+",{'claim_adj_ind':'1' }"+"]}"
            my_dict = ast.literal_eval(cond1)
            pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num', 'total': {'$sum': 1 }}}] ## sum after type conversion of field 
            mydoc=(mycol.aggregate(pipeline=pipe))  
            c=0
            for x in mydoc:
                c=c+1 
            n_records=str(c)                                
              
        print(cond)    
        
        if len(dt)==3:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dt)==2:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num=str(n_records)+" claims were adjusted "+dy_op+mon_op+yr_op+q_op+"."
        return recvd_num

    except Exception as e:
        print(str(e))     
        return "Sorry, Could not fetch you results at this time"

############ adjusted claims ##############

############ adjusted claims billed amount##############
def get_bill_amt_adjusted(dt,provider_lst):
    print(str(dt))
    try:        
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name] 
        n_records="0"
        cond=""
        if len(dt)==2:
            s1=str(dt[0])
            start = datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),0,0)
            s1=str(dt[1].split('}')[0])
            end = datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),0,0)
            print(start)
            print(end)
            if len(provider_lst) > 0:
                pipe = [{'$match':{'$and':[{'paid_date_str':{'$gt':str(start),'$lt':str(end) }},{'payto_provider_tax_id':{'$in':provider_lst}},{'claim_adj_ind':'1'}]}},{'$group': {'_id':'$root_claim_num','total': {'$sum': {'$convert':{'input':'$amt_billed','to':'double'}}}}}]
            else:
                pipe = [{'$match':{'$and':[{'paid_date_str':{'$gt':str(start),'$lt':str(end) }},{'claim_adj_ind':'1'}]}},{'$group': {'_id':'$root_claim_num','total': {'$sum': {'$convert':{'input':'$amt_billed','to':'double'}}}}}]
            mydoc=(mycol.aggregate(pipeline=pipe)) 
            n_records='0'        
            for x in mydoc:
                n_records=str(float(n_records)+float(x['total']))

        elif len(dt)==3:                       
            cond=""
            if len(dt[0])==0:
                cond=cond+",{'paid_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[0]:
                    cond=cond+",{'paid_date_str':{'$regex':'.*-.*-"+str(dy)+".*'}}"
                
            if len(dt[1])==0:
                cond=cond+",{'paid_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[1]:
                    cond=cond+",{'paid_date_str':{'$regex':'.*-"+str(dy)+"-.*'}}"
                
            if len(dt[2])==0:
                cond=cond+",{'paid_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[2]:
                    cond=cond+",{'paid_date_str':{'$regex':'"+str(dy)+"-.*-.*'}}"
            if len(provider_lst) > 0:
                pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                cond1="{'$and':["+cond[1:]+pc+",{'claim_adj_ind':'1' }"+"]}"
            else:
                cond1="{'$and':["+cond[1:]+",{'claim_adj_ind':'1' }"+"]}"
            my_dict = ast.literal_eval(cond1)
            pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num','total': {'$sum': {'$convert':{'input':'$amt_billed','to':'double'}}}}}]
            mydoc=(mycol.aggregate(pipeline=pipe)) 
            n_records='0'        
            for x in mydoc:
                n_records=str(float(n_records)+float(x['total']))           
              
        print(cond)    
        
        if len(dt)==3:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dt)==2:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num="The total billed amount for the adjusted claims was "+str(n_records)+" "+dy_op+mon_op+yr_op+q_op+"."
        return recvd_num

    except Exception as e:
        print(str(e))
        return "Sorry, Could not fetch you results at this time"

############ adjusted claims billed amount ##############

############ adjusted claims paid amount##############
def get_paid_amt_adjusted(dt,provider_lst):
    print(str(dt))
    try:        
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name] 
        n_records="0"
        cond=""
        if len(dt)==2:
            s1=str(dt[0])
            start = datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),0,0)
            s1=str(dt[1].split('}')[0])
            end = datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),0,0)
            print(start)
            print(end)            
            if len(provider_lst) > 0:
                pipe = [{'$match':{'$and':[{'paid_date_str':{'$gt':str(start),'$lt':str(end) }},{'payto_provider_tax_id':{'$in':provider_lst}},{'claim_adj_ind':'1'}]}},{'$group': {'_id':'$root_claim_num','total': {'$sum': {'$convert':{'input':'$amt_paid','to':'double'}}}}}]
            else:
                pipe = [{'$match':{'$and':[{'paid_date_str':{'$gt':str(start),'$lt':str(end) }},{'claim_adj_ind':'1'}]}},{'$group': {'_id':'$root_claim_num','total': {'$sum': {'$convert':{'input':'$amt_paid','to':'double'}}}}}]
            mydoc=(mycol.aggregate(pipeline=pipe)) 
            n_records='0'        
            for x in mydoc:
                n_records=str(float(n_records)+float(x['total']))

        elif len(dt)==3:                       
            cond=""
            if len(dt[0])==0:
                cond=cond+",{'paid_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[0]:
                    cond=cond+",{'paid_date_str':{'$regex':'.*-.*-"+str(dy)+".*'}}"
                
            if len(dt[1])==0:
                cond=cond+",{'paid_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[1]:
                    cond=cond+",{'paid_date_str':{'$regex':'.*-"+str(dy)+"-.*'}}"
                
            if len(dt[2])==0:
                cond=cond+",{'paid_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[2]:
                    cond=cond+",{'paid_date_str':{'$regex':'"+str(dy)+"-.*-.*'}}"
            if len(provider_lst) > 0:
                pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                cond1="{'$and':["+cond[1:]+pc+",{'claim_adj_ind':'1' }"+"]}"
            else:
                cond1="{'$and':["+cond[1:]+",{'claim_adj_ind':'1' }"+"]}"
            my_dict = ast.literal_eval(cond1)
            pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num','total': {'$sum': {'$convert':{'input':'$amt_paid','to':'double'}}}}}]
            mydoc=(mycol.aggregate(pipeline=pipe)) 
            n_records='0'        
            for x in mydoc:
                n_records=str(float(n_records)+float(x['total']))           
              
        print(cond)    
        
        if len(dt)==3:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dt)==2:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num="The total paid amount for the adjusted claims was "+str(n_records)+" "+dy_op+mon_op+yr_op+q_op+"."
        return recvd_num

    except Exception as e:
        print(str(e))    
        return "Sorry, Could not fetch you results at this time"

############ adjusted claims paid amount ##############

############ adjusted claims adjusted amount##############
def get_adjstd_amt_adjusted(dt,provider_lst):
    print(str(dt))
    try:        
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name] 
        n_records="0"
        n_records_ba="0"
        n_records_pa="0"
        cond=""
        if len(dt)==2:
            s1=str(dt[0])
            start = datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),0,0)
            s1=str(dt[1].split('}')[0])
            end = datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),0,0)
            print(start)
            print(end)
            
            if len(provider_lst) > 0:
                pipe = [{'$match':{'$and':[{'paid_date_str':{'$gt':str(start),'$lt':str(end) }},{'payto_provider_tax_id':{'$in':provider_lst}},{'claim_adj_ind':'1'}]}},{'$group': {'_id':'$root_claim_num','total': {'$sum': {'$convert':{'input':'$amt_paid','to':'double'}}}}}]
            else:
                pipe = [{'$match':{'$and':[{'paid_date_str':{'$gt':str(start),'$lt':str(end) }},{'claim_adj_ind':'1'}]}},{'$group': {'_id':'$root_claim_num','total': {'$sum': {'$convert':{'input':'$amt_paid','to':'double'}}}}}]
            mydoc=(mycol.aggregate(pipeline=pipe)) 
            n_records_pa='0'        
            for x in mydoc:
                n_records_pa=str(float(n_records_pa)+float(x['total']))

            if len(provider_lst) > 0:
                pipe = [{'$match':{'$and':[{'paid_date_str':{'$gt':str(start),'$lt':str(end) }},{'payto_provider_tax_id':{'$in':provider_lst}},{'claim_adj_ind':'1'}]}},{'$group': {'_id':'$root_claim_num','total': {'$sum': {'$convert':{'input':'$amt_billed','to':'double'}}}}}]
            else:
                pipe = [{'$match':{'$and':[{'paid_date_str':{'$gt':str(start),'$lt':str(end) }},{'claim_adj_ind':'1'}]}},{'$group': {'_id':'$root_claim_num','total': {'$sum': {'$convert':{'input':'$amt_billed','to':'double'}}}}}]
            mydoc=(mycol.aggregate(pipeline=pipe)) 
            n_records_ba='0'        
            for x in mydoc:
                n_records_ba=str(float(n_records_ba)+float(x['total']))
            n_records=str(float(n_records_ba)-float(n_records_pa))

        elif len(dt)==3:                       
            cond=""
            if len(dt[0])==0:
                cond=cond+",{'paid_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[0]:
                    cond=cond+",{'paid_date_str':{'$regex':'.*-.*-"+str(dy)+".*'}}"
                
            if len(dt[1])==0:
                cond=cond+",{'paid_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[1]:
                    cond=cond+",{'paid_date_str':{'$regex':'.*-"+str(dy)+"-.*'}}"
                
            if len(dt[2])==0:
                cond=cond+",{'paid_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[2]:
                    cond=cond+",{'paid_date_str':{'$regex':'"+str(dy)+"-.*-.*'}}"
            if len(provider_lst) > 0:
                pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                cond1="{'$and':["+cond[1:]+pc+",{'claim_adj_ind':'1' }"+"]}"
            else:
                cond1="{'$and':["+cond[1:]+",{'claim_adj_ind':'1' }"+"]}"
            my_dict = ast.literal_eval(cond1)  

            pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num','total': {'$sum': {'$convert':{'input':'$amt_paid','to':'double'}}}}}]
            mydoc=(mycol.aggregate(pipeline=pipe)) 
            n_records_pa='0'        
            for x in mydoc:
                n_records_pa=str(float(n_records_pa)+float(x['total']))

            pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num','total': {'$sum': {'$convert':{'input':'$amt_billed','to':'double'}}}}}]
            mydoc=(mycol.aggregate(pipeline=pipe)) 
            n_records_ba='0'        
            for x in mydoc:
                n_records_ba=str(float(n_records_ba)+float(x['total']))
            n_records=str(float(n_records_ba)-float(n_records_pa))        
              
        print(cond)    
        
        if len(dt)==3:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dt)==2:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num="The total adjusted amount for the adjusted claims was "+str(n_records)+" "+dy_op+mon_op+yr_op+q_op+"."
        return recvd_num

    except Exception as e:
        print(str(e))
        return "Sorry, Could not fetch you results at this time"

############ adjusted claims adjusted amount ##############


############ adjusted claims submission mode##############
def get_mode_submission_adjstd(dt,provider_lst):
    print(str(dt))
    try:        
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name] 
        n_records_edi="0"
        n_records_ppr="0"
        cond=""
        if len(dt)==2:
            s1=str(dt[0])
            start = datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),0,0)
            s1=str(dt[1].split('}')[0])
            end = datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),0,0)
            print(start)
            print(end)
            if len(provider_lst) > 0:
                pipe = [{'$match':{'$and':[{'paid_date_str':{'$gt':str(start),'$lt':str(end) }},{'payto_provider_tax_id':{'$in':provider_lst}},{'claim_adj_ind':'1'}]}},{'$group': {'_id':'$root_claim_num','total': {'$max': {'$convert':{'input':'$claim_receipt_type_cd','to':'string'}}}}}]                
            else:
                pipe = [{'$match':{'$and':[{'paid_date_str':{'$gt':str(start),'$lt':str(end) }},{'claim_adj_ind':'1'}]}},{'$group': {'_id':'$root_claim_num','total': {'$max': {'$convert':{'input':'$claim_receipt_type_cd','to':'string'}}}}}]
            mydoc=(mycol.aggregate(pipeline=pipe))
            n_records_edi='0'           
            n_records_ppr='0'                
            for x in mydoc:
                if str(x['total']).strip(' ').upper()=='EDI':
                    n_records_edi=str(int(n_records_edi)+1)
                else:
                    n_records_ppr=str(int(n_records_ppr)+1)
        elif len(dt)==3:                       
            cond=""
            if len(dt[0])==0:
                cond=cond+",{'paid_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[0]:
                    cond=cond+",{'paid_date_str':{'$regex':'.*-.*-"+str(dy)+".*'}}"
                
            if len(dt[1])==0:
                cond=cond+",{'paid_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[1]:
                    cond=cond+",{'paid_date_str':{'$regex':'.*-"+str(dy)+"-.*'}}"
                
            if len(dt[2])==0:
                cond=cond+",{'paid_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[2]:
                    cond=cond+",{'paid_date_str':{'$regex':'"+str(dy)+"-.*-.*'}}"
            if len(provider_lst) > 0:
                pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                cond1="{'$and':["+cond[1:]+pc+",{'claim_adj_ind':'1' }"+"]}"
            else:
                cond1="{'$and':["+cond[1:]+",{'claim_adj_ind':'1' }"+"]}"
            my_dict = ast.literal_eval(cond1)
            pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num','total': {'$max': {'$convert':{'input':'$claim_receipt_type_cd','to':'string'}}}}}]
            mydoc=(mycol.aggregate(pipeline=pipe))
            n_records_edi='0'           
            n_records_ppr='0'                
            for x in mydoc:
                if str(x['total']).strip(' ').upper()=='EDI':
                    n_records_edi=str(int(n_records_edi)+1)
                else:
                    n_records_ppr=str(int(n_records_ppr)+1)
            
              
        print(cond)    
        
        if len(dt)==3:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dt)==2:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num=n_records_edi+" claims were submitted on EDI and "+n_records_ppr+" claims were submitted on PPR"
        return recvd_num

    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"

############ adjusted claims submission mode##############

############ high dollar claims count ##############
def get_hgh_dlr_claims_cnt(dt,provider_lst):
    print(str(dt))
    try:        
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name] 
        n_records="0"
        cond=""
        if len(dt)==2:
            s1=str(dt[0])
            start = datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),0,0)
            s1=str(dt[1].split('}')[0])
            end = datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),0,0)
            print(start)
            print(end)
            if len(provider_lst) > 0:
                pipe = [{'$match':{'$and':[{'received_date_str':{'$gt':str(start),'$lt':str(end) }},{'payto_provider_tax_id':{'$in':provider_lst}},{'claim_high_dollar_paid_ind':'1'}]}},{'$group': {'_id':'$root_claim_num', 'total': {'$sum': 1 }}}] ## sum after type conversion of field            
            else:
                pipe = [{'$match':{'$and':[{'received_date_str':{'$gt':str(start),'$lt':str(end) }},{'claim_high_dollar_paid_ind':'1'}]}},{'$group': {'_id':'$root_claim_num', 'total': {'$sum': 1 }}}] ## sum after type conversion of field            
            mydoc=(mycol.aggregate(pipeline=pipe)) 
            c=0
            for x in mydoc:
                c=c+1 
            n_records=str(c)
        elif len(dt)==3:                       
            cond=""
            if len(dt[0])==0:
                cond=cond+",{'received_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[0]:
                    cond=cond+",{'received_date_str':{'$regex':'.*-.*-"+str(dy)+".*'}}"
                
            if len(dt[1])==0:
                cond=cond+",{'received_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[1]:
                    cond=cond+",{'received_date_str':{'$regex':'.*-"+str(dy)+"-.*'}}"
                
            if len(dt[2])==0:
                cond=cond+",{'received_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[2]:
                    cond=cond+",{'received_date_str':{'$regex':'"+str(dy)+"-.*-.*'}}"
            if len(provider_lst) >0:
                pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                cond1="{'$and':["+cond[1:]+pc+",{'claim_high_dollar_paid_ind':'1' }"+"]}"
            else:
                cond1="{'$and':["+cond[1:]+",{'claim_high_dollar_paid_ind':'1' }"+"]}"
            my_dict = ast.literal_eval(cond1)
            pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num', 'total': {'$sum': 1 }}}] ## sum after type conversion of field 
            mydoc=(mycol.aggregate(pipeline=pipe))  
            c=0
            for x in mydoc:
                c=c+1 
            n_records=str(c)                                
              
        print(cond)    
        
        if len(dt)==3:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dt)==2:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num=str(n_records)+"} high dollar claims were received "+dy_op+mon_op+yr_op+q_op+"."
        return recvd_num

    except Exception as e:
        print(str(e))
        return "Sorry, Could not fetch you results at this time"

############ high dollar received claims ##############


############ high dollar claims submission mode##############
def get_mode_submission_hgh_dlr(dt,provider_lst):
    print(str(dt))
    try:        
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name] 
        n_records_edi="0"
        n_records_ppr="0"
        cond=""
        if len(dt)==2:
            s1=str(dt[0])
            start = datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),0,0)
            s1=str(dt[1].split('}')[0])
            end = datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),0,0)
            print(start)
            print(end)
            if len(provider_lst) > 0:
                pipe = [{'$match':{'$and':[{'received_date_str':{'$gt':str(start),'$lt':str(end) }},{'payto_provider_tax_id':{'$in':provider_lst}},{'claim_high_dollar_paid_ind':'1'}]}},{'$group': {'_id':'$root_claim_num','total': {'$max': {'$convert':{'input':'$claim_receipt_type_cd','to':'string'}}}}}]
            else:
                pipe = [{'$match':{'$and':[{'received_date_str':{'$gt':str(start),'$lt':str(end) }},{'claim_high_dollar_paid_ind':'1'}]}},{'$group': {'_id':'$root_claim_num','total': {'$max': {'$convert':{'input':'$claim_receipt_type_cd','to':'string'}}}}}]
            mydoc=(mycol.aggregate(pipeline=pipe))
            n_records_edi='0'           
            n_records_ppr='0'                
            for x in mydoc:
                if str(x['total']).strip(' ').upper()=='EDI':
                    n_records_edi=str(int(n_records_edi)+1)
                else:
                    n_records_ppr=str(int(n_records_ppr)+1)
        elif len(dt)==3:                       
            cond=""
            if len(dt[0])==0:
                cond=cond+",{'received_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[0]:
                    cond=cond+",{'received_date_str':{'$regex':'.*-.*-"+str(dy)+".*'}}"
                
            if len(dt[1])==0:
                cond=cond+",{'received_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[1]:
                    cond=cond+",{'received_date_str':{'$regex':'.*-"+str(dy)+"-.*'}}"
                
            if len(dt[2])==0:
                cond=cond+",{'received_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[2]:
                    cond=cond+",{'received_date_str':{'$regex':'"+str(dy)+"-.*-.*'}}"
            if len(provider_lst) >0:
                pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                cond1="{'$and':["+cond[1:]+pc+",{'claim_high_dollar_paid_ind':'1' }"+"]}"
            else:
                cond1="{'$and':["+cond[1:]+",{'claim_high_dollar_paid_ind':'1' }"+"]}"
            my_dict = ast.literal_eval(cond1)
            pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num','total': {'$max': {'$convert':{'input':'$claim_receipt_type_cd','to':'string'}}}}}]
            mydoc=(mycol.aggregate(pipeline=pipe))
            n_records_edi='0'           
            n_records_ppr='0'                
            for x in mydoc:
                if str(x['total']).strip(' ').upper()=='EDI':
                    n_records_edi=str(int(n_records_edi)+1)
                else:
                    n_records_ppr=str(int(n_records_ppr)+1)
            
              
        print(cond)    
        
        if len(dt)==3:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dt)==2:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num=n_records_edi+" claims were submitted on EDI and "+n_records_ppr+" claims were submitted on PPR"
        return recvd_num

    except Exception as e:
        print(str(e))        
        return "Sorry, Could not fetch you results at this time"

############ high dollar claims submission mode##############

############ high dollar claims billed amount##############
def get_bill_amt_hgh_dlr(dt,provider_lst):
    print(str(dt))
    try:        
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name] 
        n_records="0"
        cond=""
        if len(dt)==2:
            s1=str(dt[0])
            start = datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),0,0)
            s1=str(dt[1].split('}')[0])
            end = datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),0,0)
            print(start)
            print(end)
            if len(provider_lst) > 0:
                pipe = [{'$match':{'$and':[{'received_date_str':{'$gt':str(start),'$lt':str(end) }},{'payto_provider_tax_id':{'$in':provider_lst}},{'claim_high_dollar_paid_ind':'1'}]}},{'$group': {'_id':'$root_claim_num','total': {'$sum': {'$convert':{'input':'$amt_billed','to':'double'}}}}}]
            else:
                pipe = [{'$match':{'$and':[{'received_date_str':{'$gt':str(start),'$lt':str(end) }},{'claim_high_dollar_paid_ind':'1'}]}},{'$group': {'_id':'$root_claim_num','total': {'$sum': {'$convert':{'input':'$amt_billed','to':'double'}}}}}]
            mydoc=(mycol.aggregate(pipeline=pipe)) 
            n_records='0'        
            for x in mydoc:
                n_records=str(float(n_records)+float(x['total']))

        elif len(dt)==3:                       
            cond=""
            if len(dt[0])==0:
                cond=cond+",{'received_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[0]:
                    cond=cond+",{'received_date_str':{'$regex':'.*-.*-"+str(dy)+".*'}}"
                
            if len(dt[1])==0:
                cond=cond+",{'received_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[1]:
                    cond=cond+",{'received_date_str':{'$regex':'.*-"+str(dy)+"-.*'}}"
                
            if len(dt[2])==0:
                cond=cond+",{'received_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[2]:
                    cond=cond+",{'received_date_str':{'$regex':'"+str(dy)+"-.*-.*'}}"
            if len(provider_lst) >0:
                pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                cond1="{'$and':["+cond[1:]+pc+",{'claim_high_dollar_paid_ind':'1' }"+"]}"
            else:
                cond1="{'$and':["+cond[1:]+",{'claim_high_dollar_paid_ind':'1' }"+"]}"
            my_dict = ast.literal_eval(cond1)
            pipe = [{'$match':my_dict},{'$group': {'_id':'$root_claim_num','total': {'$sum': {'$convert':{'input':'$amt_billed','to':'double'}}}}}]
            mydoc=(mycol.aggregate(pipeline=pipe)) 
            n_records='0'        
            for x in mydoc:
                n_records=str(float(n_records)+float(x['total']))           
              
        print(cond)    
        
        if len(dt)==3:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dt)==2:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num="The total billed amount for the high dollar claims was "+str(n_records)+" "+dy_op+mon_op+yr_op+q_op+"."
        return recvd_num

    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"

############ high dollar claims billed amount ##############

def get_paid_amt_claims_hgh_dlr(dt,provider_lst):
    print(str(dt))
    try:
        billed_amt="0"
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name] 
        cond=""
        if len(dt)==2:
            s1=str(dt[0])
            start = datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),0,0)
            s1=str(dt[1].split('}')[0])
            end = datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),0,0)
            print(start)
            print(end)            
            if len(provider_lst) > 0:
                pipe = [{'$match':{'$and':[{'received_date_str':{'$gt':str(start),'$lt':str(end)}},{'payto_provider_tax_id':{'$in':provider_lst}},{'paid_date_str':{'$gt':str(start),'$lt':str(end)}},{'claim_high_dollar_paid_ind':'1'}]}},{'$group': {'_id':'$paid_date_str', 'total': {'$sum': {'$convert':{'input':'$amt_paid','to':'double'}}}}}]
            else:
                pipe = [{'$match':{'$and':[{'received_date_str':{'$gt':str(start),'$lt':str(end)}},{'paid_date_str':{'$gt':str(start),'$lt':str(end)}},{'claim_high_dollar_paid_ind':'1'}]}},{'$group': {'_id':'$paid_date_str', 'total': {'$sum': {'$convert':{'input':'$amt_paid','to':'double'}}}}}]
            mydoc=(mycol.aggregate(pipeline=pipe))            
            billed_amt="0"
            for x in mydoc:
                billed_amt=float(billed_amt)+float(str(x['total']))
            billed_amt=str(billed_amt)
            print(billed_amt)
        elif len(dt)==3:                       
            cond=""
            if len(dt[0])==0:
                cond=cond+",{'received_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[0]:
                    cond=cond+",{'received_date_str':{'$regex':'.*-.*-"+str(dy)+".*'}}"
                
            if len(dt[1])==0:
                cond=cond+",{'received_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[1]:
                    cond=cond+",{'received_date_str':{'$regex':'.*-"+str(dy)+"-.*'}}"
                
            if len(dt[2])==0:
                cond=cond+",{'received_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[2]:
                    cond=cond+",{'received_date_str':{'$regex':'"+str(dy)+"-.*-.*'}}"
            cond=cond[1:]            
            cond1=""
            if len(dt[0])==0:
                cond1=cond1+",{'received_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[0]:
                    cond1=cond1+",{'received_date_str':{'$regex':'.*-.*-"+str(dy)+".*'}}"
                
            if len(dt[1])==0:
                cond1=cond1+",{'received_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[1]:
                    cond1=cond1+",{'received_date_str':{'$regex':'.*-"+str(dy)+"-.*'}}"
                
            if len(dt[2])==0:
                cond1=cond1+",{'received_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[2]:
                    cond1=cond1+",{'received_date_str':{'$regex':'"+str(dy)+"-.*-.*'}}"
            cond1=cond1[1:]
            cond2="{'claim_high_dollar_paid_ind':'1'}"
            if len(provider_lst) >0:
                pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                cond="{'$and':["+cond+pc+","+cond1+","+cond2+"]}"
            else:
                cond="{'$and':["+cond+","+cond1+","+cond2+"]}"
            
            my_dict = ast.literal_eval(cond)
            pipe = [{'$match':my_dict},{'$group': {'_id':'$received_date_str', 'total': {'$sum': {'$convert':{'input':'$amt_paid','to':'double'}}}}}] ## sum after type conversion of field            
            mydoc=(mycol.aggregate(pipeline=pipe))            
            billed_amt="0"
            for x in mydoc:
                billed_amt=float(billed_amt)+float(str(x['total']))
            billed_amt=str(billed_amt)
            print(billed_amt)

              
        print(cond)    
        
        if len(dt)==3:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dt)==2:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num="The total paid amount of high dollar claims "+dy_op+mon_op+yr_op+q_op+" is "+str(billed_amt)
        return recvd_num

    except Exception as e:
        print(str(e))        
        return "Sorry, Could not fetch you results at this time"

def get_paid_cnt_claims_hgh_dlr(dt,provider_lst):
    print(str(dt))
    try:
        billed_amt="0"
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name] 
        cond=""
        if len(dt)==2:
            s1=str(dt[0])
            start = datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),0,0)
            s1=str(dt[1].split('}')[0])
            end = datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),0,0)
            print(start)
            print(end)            
            if len(provider_lst) > 0:
                pipe = [{'$match':{'$and':[{'received_date_str':{'$gt':str(start),'$lt':str(end)}},{'payto_provider_tax_id':{'$in':provider_lst}},{'claim_denial_ind':'0'},{'paid_date_str':{'$gt':str(start),'$lt':str(end)}},{'claim_high_dollar_paid_ind':'1'}]}},{'$group': {'_id':'$paid_date_str', 'total': {'$sum': 1}}}]    
            else:
                pipe = [{'$match':{'$and':[{'received_date_str':{'$gt':str(start),'$lt':str(end)}},{'claim_denial_ind':'0'},{'paid_date_str':{'$gt':str(start),'$lt':str(end)}},{'claim_high_dollar_paid_ind':'1'}]}},{'$group': {'_id':'$paid_date_str', 'total': {'$sum': 1}}}]
            mydoc=(mycol.aggregate(pipeline=pipe))            
            billed_amt="0"
            for x in mydoc:
                billed_amt=int(billed_amt)+int(str(x['total']))
            billed_amt=str(billed_amt)
            print(billed_amt)
        elif len(dt)==3:                       
            cond=""
            if len(dt[0])==0:
                cond=cond+",{'received_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[0]:
                    cond=cond+",{'received_date_str':{'$regex':'.*-.*-"+str(dy)+".*'}}"
                
            if len(dt[1])==0:
                cond=cond+",{'received_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[1]:
                    cond=cond+",{'received_date_str':{'$regex':'.*-"+str(dy)+"-.*'}}"
                
            if len(dt[2])==0:
                cond=cond+",{'received_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[2]:
                    cond=cond+",{'received_date_str':{'$regex':'"+str(dy)+"-.*-.*'}}"
            cond=cond[1:]            
            cond1=""
            if len(dt[0])==0:
                cond1=cond1+",{'paid_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[0]:
                    cond1=cond1+",{'paid_date_str':{'$regex':'.*-.*-"+str(dy)+".*'}}"
                
            if len(dt[1])==0:
                cond1=cond1+",{'paid_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[1]:
                    cond1=cond1+",{'paid_date_str':{'$regex':'.*-"+str(dy)+"-.*'}}"
                
            if len(dt[2])==0:
                cond1=cond1+",{'paid_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[2]:
                    cond1=cond1+",{'paid_date_str':{'$regex':'"+str(dy)+"-.*-.*'}}"
            cond1=cond1[1:]
            cond2="{'claim_high_dollar_paid_ind':'1'},{'claim_denial_ind':'0'}"
            if len(provider_lst) >0:
                pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                cond="{'$and':["+cond+pc+","+cond1+","+cond2+"]}"
            else:
                cond="{'$and':["+cond+","+cond1+","+cond2+"]}"
                       
            my_dict = ast.literal_eval(cond)
            pipe = [{'$match':my_dict},{'$group': {'_id':'$paid_date_str', 'total': {'$sum': 1}}}]
            mydoc=(mycol.aggregate(pipeline=pipe))            
            billed_amt="0"
            for x in mydoc:
                billed_amt=int(billed_amt)+int(str(x['total']))
            billed_amt=str(billed_amt)
            print(billed_amt)

              
        print(cond)    
        
        if len(dt)==3:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dt)==2:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]

        recvd_num=str(billed_amt)+" claims got paid out of "+ get_hgh_dlr_claims_cnt(dt,provider_lst).split('}')[0].strip(' ') +dy_op+mon_op+yr_op+q_op
        return recvd_num

    except Exception as e:
        print(str(e))       
        return "Sorry, Could not fetch you results at this time"

def get_mode_submission_claim(value1):
    print(str(value1))
    try:        
        claim_num_rec=str(value1)        
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name]
        mydoc = mycol.find({"root_claim_num": str(claim_num_rec)})
        n_records=(str(mydoc.count()))
        print(n_records)
        if int(n_records) > 0:
            pipe = [{'$match':{'$and':[{"root_claim_num":str(claim_num_rec)},{'claim_receipt_type_cd':'EDI'}]}},{'$group': {'_id':'$root_claim_num', 'total': {'$sum': 1 }}}]            
            mydoc=(mycol.aggregate(pipeline=pipe)) 
            edi_count="0"           
            for x in mydoc:
                edi_count=x['total']
            edi_count=str(edi_count)
            pipe = [{'$match':{'$and':[{"root_claim_num":str(claim_num_rec)},{'claim_receipt_type_cd':'PPR'}]}},{'$group': {'_id':'$root_claim_num', 'total': {'$sum': 1 }}}]            
            mydoc=(mycol.aggregate(pipeline=pipe)) 
            ppr_count="0"           
            for x in mydoc:
                ppr_count=x['total']
            ppr_count=str(ppr_count)
            if int(ppr_count) > int(edi_count):
                resp="The claim is submitted through PPR mode"
            else:
                resp="The claim is submitted through EDI mode"            
        else:
            resp="Could not find claim with Claim Number "+claim_num_rec+", Please make sure you entered correct details "
        return(resp)       
    except Exception as e:
        print(str(e))
        return "Sorry, Could not fetch you results at this time"

############ denied claims reasons ##############
def get_denied_claims_actin_resns(dt,provider_lst):
    n1=5
    print(str(dt))
    if True:        
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name] 
        top_reasons_lst=list()
        cond=""
        if len(dt)==2:
            s1=str(dt[0])
            start = datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),0,0)
            s1=str(dt[1].split('}')[0])
            end = datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),0,0)
            print(start)
            print(end)
            if len(provider_lst)> 0:
                pipe = [{'$match':{'$and':[{'paid_date_str':{'$gt':str(start),'$lt':str(end) }},{'payto_provider_tax_id':{'$in':provider_lst}},{'claim_denial_ind':'1'}]}},{'$group': {'_id':'$denial_description', 'total': {'$sum': 1 }}}] ## sum after type conversion of field            
            else:
                pipe = [{'$match':{'$and':[{'paid_date_str':{'$gt':str(start),'$lt':str(end) }},{'claim_denial_ind':'1'}]}},{'$group': {'_id':'$denial_description', 'total': {'$sum': 1 }}}] ## sum after type conversion of field            
            mydoc=(mycol.aggregate(pipeline=pipe))              
            non_den_resn_lst=list()  
            non_den_resn_cnt_lst=list()
            temp_non_den_resn_cnt_lst=list()            
            c=1                    
            for x in mydoc:
                if len(str(x['_id']).strip(' ')) > 0:
                    non_den_resn_lst.append(str(c)+"}"+str(x['_id']))
                    non_den_resn_cnt_lst.append(str(c)+"}"+str(x['total']))
                    c=c+1
            temp_non_den_resn_cnt_lst=non_den_resn_cnt_lst
            # sorting
            n = len(temp_non_den_resn_cnt_lst)
            for i in range(n):
                for j in range(0, n-i-1):
                    if int(temp_non_den_resn_cnt_lst[j].split('}')[1]) > int(temp_non_den_resn_cnt_lst[j+1].split('}')[1]) :
                        temp=temp_non_den_resn_cnt_lst[j]
                        temp_non_den_resn_cnt_lst[j]=temp_non_den_resn_cnt_lst[j+1]
                        temp_non_den_resn_cnt_lst[j+1]=temp                       
            # sorting
            if len(temp_non_den_resn_cnt_lst) > n1:
                print("entered if")
                print(str(len(temp_non_den_resn_cnt_lst)))
                print(str(n1))
                for i in range(n1):
                    s=(temp_non_den_resn_cnt_lst[i]).split('}')[0]
                    for j in range(0,len(non_den_resn_lst)):
                        if s==(non_den_resn_lst[j]).split('}')[0]:
                            top_reasons_lst.append((non_den_resn_lst[j]).split('}')[1])
            else:
                print("entered else")
                print(str(len(temp_non_den_resn_cnt_lst)))
                print(str(n1))
                for i in range(0,len(temp_non_den_resn_cnt_lst)):
                    s=(temp_non_den_resn_cnt_lst[i]).split('}')[0]
                    for j in range(0,len(non_den_resn_lst)):
                        if s==(non_den_resn_lst[j]).split('}')[0]:
                            top_reasons_lst.append((non_den_resn_lst[j]).split('}')[1])

            
        elif len(dt)==3:                       
            cond=""
            if len(dt[0])==0:
                cond=cond+",{'paid_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[0]:
                    cond=cond+",{'paid_date_str':{'$regex':'.*-.*-"+str(dy)+".*'}}"
                
            if len(dt[1])==0:
                cond=cond+",{'paid_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[1]:
                    cond=cond+",{'paid_date_str':{'$regex':'.*-"+str(dy)+"-.*'}}"
                
            if len(dt[2])==0:
                cond=cond+",{'paid_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[2]:
                    cond=cond+",{'paid_date_str':{'$regex':'"+str(dy)+"-.*-.*'}}"
            if len(provider_lst)>0:
                pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                cond1="{'$and':["+cond[1:]+pc+",{'claim_denial_ind':'1' }"+"]}"
            else:
                cond1="{'$and':["+cond[1:]+",{'claim_denial_ind':'1' }"+"]}"
            my_dict = ast.literal_eval(cond1)
            pipe = [{'$match':my_dict},{'$group': {'_id':'$denial_description', 'total': {'$sum': 1 }}}] ## sum after type conversion of field 
            mydoc=(mycol.aggregate(pipeline=pipe))                       
            non_den_resn_lst=list()  
            non_den_resn_cnt_lst=list()
            temp_non_den_resn_cnt_lst=list()            
            c=1                    
            for x in mydoc:
                if len(str(x['_id']).strip(' ')) > 0:
                    non_den_resn_lst.append(str(c)+"}"+str(x['_id']))
                    non_den_resn_cnt_lst.append(str(c)+"}"+str(x['total']))
                    c=c+1
            temp_non_den_resn_cnt_lst=non_den_resn_cnt_lst
            # sorting
            n = len(temp_non_den_resn_cnt_lst)
            for i in range(n):
                for j in range(0, n-i-1):
                    if int(temp_non_den_resn_cnt_lst[j].split('}')[1]) > int(temp_non_den_resn_cnt_lst[j+1].split('}')[1]) :
                        temp=temp_non_den_resn_cnt_lst[j]
                        temp_non_den_resn_cnt_lst[j]=temp_non_den_resn_cnt_lst[j+1]
                        temp_non_den_resn_cnt_lst[j+1]=temp                       
            # sorting
            # print(non_den_resn_lst)
            # print(non_den_resn_cnt_lst)
            # print(temp_non_den_resn_cnt_lst)
            if len(temp_non_den_resn_cnt_lst) > n1:
                print(str(len(temp_non_den_resn_cnt_lst)))
                print(str(n1))
                for i in range(n1):
                    s=(temp_non_den_resn_cnt_lst[i]).split('}')[0]
                    for j in range(0,len(non_den_resn_lst)):
                        if s==(non_den_resn_lst[j]).split('}')[0]:
                            top_reasons_lst.append((non_den_resn_lst[j]).split('}')[1])
            else:
                print("entered else")
                print(str(len(temp_non_den_resn_cnt_lst)))
                print(str(n1))
                for i in range(0,len(temp_non_den_resn_cnt_lst)):
                    s=(temp_non_den_resn_cnt_lst[i]).split('}')[0]
                    for j in range(0,len(non_den_resn_lst)):
                        if s==(non_den_resn_lst[j]).split('}')[0]:
                            top_reasons_lst.append((non_den_resn_lst[j]).split('}')[1])

        print(cond)    
        
        if len(dt)==3:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dt)==2:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]
        recvd_num="The following are top reasons for claims to get denied:<br><ul>"
        for x in top_reasons_lst:
            recvd_num=recvd_num+"<li>"+str(x)+"</li>"
        recvd_num=recvd_num+"</ul>"        
        # return str(len(top_reasons_lst))
        return recvd_num
    else:
    # except Exception as e:
        # print(str(e))      
        return "Sorry, Could not fetch you results at this time"

############ denied claims reasons ##############

############ adjusted claims reasons ##############
def get_adjstd_claims_actin_resns(dt,provider_lst):
    n1=5
    print(str(dt))
    if True:        
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb[coll_name] 
        top_reasons_lst=list()
        cond=""
        if len(dt)==2:
            s1=str(dt[0])
            start = datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),0,0)
            s1=str(dt[1].split('}')[0])
            end = datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),0,0)
            print(start)
            print(end)
            if len(provider_lst):
                pipe = [{'$match':{'$and':[{'paid_date_str':{'$gt':str(start),'$lt':str(end) }},{'payto_provider_tax_id':{'$in':provider_lst}},{'claim_adj_ind':'1'}]}},{'$group': {'_id':'$adjustment_description', 'total': {'$sum': 1 }}}] ## sum after type conversion of field            
            else:
                pipe = [{'$match':{'$and':[{'paid_date_str':{'$gt':str(start),'$lt':str(end) }},{'claim_adj_ind':'1'}]}},{'$group': {'_id':'$adjustment_description', 'total': {'$sum': 1 }}}] ## sum after type conversion of field            
            mydoc=(mycol.aggregate(pipeline=pipe))              
            non_den_resn_lst=list()  
            non_den_resn_cnt_lst=list()
            temp_non_den_resn_cnt_lst=list()            
            c=1                    
            for x in mydoc:
                if len(str(x['_id']).strip(' ')) > 0:
                    non_den_resn_lst.append(str(c)+"}"+str(x['_id']))
                    non_den_resn_cnt_lst.append(str(c)+"}"+str(x['total']))
                    c=c+1
            temp_non_den_resn_cnt_lst=non_den_resn_cnt_lst
            # sorting
            n = len(temp_non_den_resn_cnt_lst)
            for i in range(n):
                for j in range(0, n-i-1):
                    if int(temp_non_den_resn_cnt_lst[j].split('}')[1]) > int(temp_non_den_resn_cnt_lst[j+1].split('}')[1]) :
                        temp=temp_non_den_resn_cnt_lst[j]
                        temp_non_den_resn_cnt_lst[j]=temp_non_den_resn_cnt_lst[j+1]
                        temp_non_den_resn_cnt_lst[j+1]=temp                       
            # sorting
            if len(temp_non_den_resn_cnt_lst) > n1:
                print("entered if")
                print(str(len(temp_non_den_resn_cnt_lst)))
                print(str(n1))
                for i in range(n1):
                    s=(temp_non_den_resn_cnt_lst[i]).split('}')[0]
                    for j in range(0,len(non_den_resn_lst)):
                        if s==(non_den_resn_lst[j]).split('}')[0]:
                            top_reasons_lst.append((non_den_resn_lst[j]).split('}')[1])
            else:
                print("entered else")
                print(str(len(temp_non_den_resn_cnt_lst)))
                print(str(n1))
                for i in range(0,len(temp_non_den_resn_cnt_lst)):
                    s=(temp_non_den_resn_cnt_lst[i]).split('}')[0]
                    for j in range(0,len(non_den_resn_lst)):
                        if s==(non_den_resn_lst[j]).split('}')[0]:
                            top_reasons_lst.append((non_den_resn_lst[j]).split('}')[1])

            
        elif len(dt)==3:                       
            cond=""
            if len(dt[0])==0:
                cond=cond+",{'paid_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[0]:
                    cond=cond+",{'paid_date_str':{'$regex':'.*-.*-"+str(dy)+".*'}}"
                
            if len(dt[1])==0:
                cond=cond+",{'paid_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[1]:
                    cond=cond+",{'paid_date_str':{'$regex':'.*-"+str(dy)+"-.*'}}"
                
            if len(dt[2])==0:
                cond=cond+",{'paid_date_str':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[2]:
                    cond=cond+",{'paid_date_str':{'$regex':'"+str(dy)+"-.*-.*'}}"
            if len(provider_lst)>0:
                pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                cond1="{'$and':["+cond[1:]+pc+",{'claim_adj_ind':'1' }"+"]}"
            else:
                cond1="{'$and':["+cond[1:]+",{'claim_adj_ind':'1' }"+"]}"
            my_dict = ast.literal_eval(cond1)
            pipe = [{'$match':my_dict},{'$group': {'_id':'$adjustment_description', 'total': {'$sum': 1 }}}] ## sum after type conversion of field 
            mydoc=(mycol.aggregate(pipeline=pipe))                       
            non_den_resn_lst=list()  
            non_den_resn_cnt_lst=list()
            temp_non_den_resn_cnt_lst=list()            
            c=1                    
            for x in mydoc:
                if len(str(x['_id']).strip(' ')) > 0:
                    non_den_resn_lst.append(str(c)+"}"+str(x['_id']))
                    non_den_resn_cnt_lst.append(str(c)+"}"+str(x['total']))
                    c=c+1
            temp_non_den_resn_cnt_lst=non_den_resn_cnt_lst
            # sorting
            n = len(temp_non_den_resn_cnt_lst)
            for i in range(n):
                for j in range(0, n-i-1):
                    if int(temp_non_den_resn_cnt_lst[j].split('}')[1]) > int(temp_non_den_resn_cnt_lst[j+1].split('}')[1]) :
                        temp=temp_non_den_resn_cnt_lst[j]
                        temp_non_den_resn_cnt_lst[j]=temp_non_den_resn_cnt_lst[j+1]
                        temp_non_den_resn_cnt_lst[j+1]=temp                       
            # sorting
            # print(non_den_resn_lst)
            # print(non_den_resn_cnt_lst)
            # print(temp_non_den_resn_cnt_lst)
            if len(temp_non_den_resn_cnt_lst) > n1:
                print(str(len(temp_non_den_resn_cnt_lst)))
                print(str(n1))
                for i in range(n1):
                    s=(temp_non_den_resn_cnt_lst[i]).split('}')[0]
                    for j in range(0,len(non_den_resn_lst)):
                        if s==(non_den_resn_lst[j]).split('}')[0]:
                            top_reasons_lst.append((non_den_resn_lst[j]).split('}')[1])
            else:
                print("entered else")
                print(str(len(temp_non_den_resn_cnt_lst)))
                print(str(n1))
                for i in range(0,len(temp_non_den_resn_cnt_lst)):
                    s=(temp_non_den_resn_cnt_lst[i]).split('}')[0]
                    for j in range(0,len(non_den_resn_lst)):
                        if s==(non_den_resn_lst[j]).split('}')[0]:
                            top_reasons_lst.append((non_den_resn_lst[j]).split('}')[1])

        print(cond)    
        
        if len(dt)==3:
            if len(dt[1]) > 0:
                mon_op=" in month of"
                for mnum in dt[1]:
                    mon_op=mon_op+" " +calendar.month_name[int(str(mnum))]+", "
                mon_op=mon_op.rstrip(mon_op[-2:])
            else:
                mon_op=""
            if len(dt[2]) > 0:
                yr_op=" in year"
                for mnum in dt[2]:
                    yr_op=yr_op+" " +mnum+", "
                yr_op=yr_op.rstrip(yr_op[-2:])
            else:
                yr_op=""

            if len(dt[0]) > 0:
                dy_op=" on "
                for mnum in dt[0]:
                    dy_op=dy_op+" " +mnum+", "
                dy_op=dy_op.rstrip(dy_op[-2:])
            else:
                dy_op=""
            q_op=""
        elif len(dt)==2:
            dy_op=""
            mon_op=""
            yr_op=""
            q_op=" in "+dt[1].split('}')[1]
        recvd_num="The following are top reasons for claims to get adjusted:<br><ul>"
        for x in top_reasons_lst:
            recvd_num=recvd_num+"<li>"+str(x)+"</li>"
        recvd_num=recvd_num+"</ul>"        
        # return str(len(top_reasons_lst))
        return recvd_num
    else:
    # except Exception as e:
        # print(str(e))      
        return "Sorry, Could not fetch you results at this time"

############ denied claims reasons ##############

# provider_lst=['581966795','420680448']
# print(get_mode_submission_claim('7454205017'))
# dt=[['06'],['11'],['2018']]
# dt=['2018-11-01', '2019-01-01}last two months']
# print(get_hgh_dlr_claims_cnt(dt,provider_lst))
# # print(get_hgh_dlr_claims_cnt(dt,provider_lst))
# print(get_mode_submission_hgh_dlr(dt,provider_lst))
# print(get_bill_amt_hgh_dlr(dt,provider_lst))
# print(get_paid_amt_claims_hgh_dlr(dt,provider_lst))
# print(get_denied_claims_actin_resns(dt,provider_lst))
# print(get_resubmit_proc())



#**********************
provider_lst=['111888924','133964321']
# provider_lst=list()
# dt=[['06'],['11'],['2018']]
dt=['2019-01-01', '2019-05-01}last two months']
# print(get_received_claims(dt,provider_lst))
# print(get_bill_amt_recvd(dt,provider_lst))
# print(get_paid_amt_claims_recvd(dt,provider_lst))
print(get_paid_cnt_claims_recvd(dt,provider_lst))
# print(get_mode_submission_recvd(dt,provider_lst))
# print(get_denied_claims_cnt(dt,provider_lst))
# print(get_bill_amt_dend(dt,provider_lst))
# print(get_mode_submission_dend(dt,provider_lst))
# print(get_prtl_denied_claims_cnt(dt,provider_lst))
# print(get_bill_amt_prtl_dend(dt,provider_lst))
# print(get_paid_amt_prtl_dend(dt,provider_lst))
# print(get_mode_submission_prtl_dend(dt,provider_lst))
# print(get_adjusted_claims_cnt(dt,provider_lst))
# print(get_bill_amt_adjusted(dt,provider_lst))
# print(get_paid_amt_adjusted(dt,provider_lst))
# print(get_adjstd_amt_adjusted(dt,provider_lst))
# print(get_mode_submission_adjstd(dt,provider_lst))
# print(get_hgh_dlr_claims_cnt(dt,provider_lst))
# print(get_mode_submission_hgh_dlr(dt,provider_lst))
# print(get_bill_amt_hgh_dlr(dt,provider_lst))
# print(get_paid_amt_claims_hgh_dlr(dt,provider_lst))
# print(get_paid_cnt_claims_hgh_dlr(dt,provider_lst))
# print(get_denied_claims_actin_resns(dt,provider_lst))
# print(get_adjstd_claims_actin_resns(dt,provider_lst))
print(get_status("8120H06451"))

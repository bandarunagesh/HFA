##dict of response for each type of intent
import random
from pblm_solving_files.sqlite_python import * 
from autocorrect import spell

import xlsxwriter
import time
from dateutil import parser
import redis
import re
import os
import pandas as pd
import numpy as np
import datetime
import time
from dateutil import parser
import redis
import re
from datetime import datetime
from flask import Flask
from flask import render_template,jsonify,request
import requests
from autocorrect import spell

GREETING_RESPONSES = ["sup bro", "hey", "Hi", "how can i help?","hello"]
GOODBYE_RESPONSES = ["bye", "cya", "take care", "good", "bye bye","Bye..Tc"]
AFFIRM_RESPONSES = ["indeed", "OK", "that's right", "great", "cool"]

##########
claim_numbers_req=list()
##########

def claim_num_extract(s1):
    claim_num=0    
    if claim_num==0:
        text=s1
        s2=text.split(' ')
        for i in range(0,len(s2)):            
            n=""
            for j in range(0,len(s2[i])):                    
                    try:
                        n1=int(s2[i][j])
                        n=n+str(n1)
                    except:
                        w=1
            if len(str(n)) > 4 and int(str(n)) > 0:
                claim_num=s2
                return claim_num
    claim_num=claim_numbers_req[len(claim_numbers_req)-1]
    return claim_num

def corrected_ip_string_1(s1):
    print("corrected_ip_string")
    try:
        s1=s1.replace('  ',' ').replace('  ',' ').strip(' ')
        s2=s1.split(' ')
        s3=""
        for i in range(0,len(s2)):
            
            if s2[i].lower() in ["tat"]:
                s3=s3+" "+"tat".lower()+" "
            if s2[i].lower() in ["by","uhc","united","health","group","uhg","corporation"]:
                s3=s3+" "+""+" "
            if spell(s2[i]).lower() in ["by","uhc","united","health","group","uhg","corporation"]:
                s3=s3+" "+""+" "
            elif spell(s2[i]).lower() in ["details","detail","condition","position","place","situation","stage","action","about","status"]:
                s3=s3+" "+"status".lower()+" "
            elif spell(s2[i]).lower() in ["deny","denied","denial","denials","denying","denies","decline","declines","declined","declination","declining","declinations","reject","rejects","rejected","rejecting","rejection","rejections","refuse","refused","refusals","refusal","refusing","refuses","repudiate","repudiates","repudiated","repudiation","repudiations","repudiating","rebuff","rebuffs","rebuffed","rebuffing","dismiss","dismissed","dismisses","dismissing","veto","vetoed","vetoing","vetoes","refute","refutes","refuted","refuting","refutation","rebuff","rebuffs","rebuffed","rebuffing"]:
                s3=s3+" "+"denied".lower()+" "
            elif spell(s2[i]).lower() in ['partially','partial','incomplete','incompletely','partials','uncompleted']:
                s3=s3+" "+"partial".lower()+" "
            elif spell(s2[i]).lower() in ['adjust','adjusting','adjusted','adjustment','adjustments','adjusts']:
                s3=s3+" "+"adjusted".lower()+" "
            elif spell(s2[i]).lower() in ['completely','complete','totally','total','completes','totals']:
                s3=s3+" "+"complete".lower()+" "
            elif spell(s2[i]).lower().replace('-','') in ['resubmit','resubmits','resubmitted','resubmitting','resubmission']:
                s3=s3+" "+"resubmit".lower()+" "
            elif spell(s2[i]).lower().replace('-','') in ['submit','submits','submitted','submitting','submission']:
                s3=s3+" "+"submitted".lower()+" "
            elif spell(s2[i]).lower() in ['justification','explanation','rationalization','vindication','clarification','simplification','description','elucidation','exposition','explication','delineation']:
                s3=s3+" "+"justification".lower()+" "
            elif spell(s2[i]).lower() in ['justified','explained','rationalized','vindicated','clarified','simplified','described','elucidated','exposited','explicated','delineated']:
                s3=s3+" "+"justified".lower()+" "
            elif spell(s2[i]).lower() in ['amount','money','cash','buck','bucks','capital']:
                s3=s3+" "+"amount".lower()+" "
            elif spell(s2[i]).lower() in ['reason','cause','root','basis']:
                s3=s3+" "+"reason".lower()+" "
            elif spell(s2[i]).lower() in ['reasons','causes']:
                s3=s3+" "+"reasons".lower()+" "
            elif spell(s2[i]).lower() in ['paid','pay','pays','paying','payment','compensating','compensated','compensates','compensate','indemnifying','indemnifies','indemnify','indemnified','refund','refunds','refunded','refunding','remunerate','remunerated','remunerates','remunerating','recompensed','recompense','recompensing','recompenses','reimburse','reimburses','reimbursing','reimbursed','repaid','repay','repays','repaying','repayment']:
                s3=s3+" "+"paid".lower()+" "
            elif spell(s2[i]).lower() in ['period','duration','span','term','days','long','day']:
                s3=s3+" "+"time".lower()+" "
            elif spell(s2[i]).lower() in ['process','processing','processed','processes']:
                s3=s3+" "+"process".lower()+" "
            elif spell(s2[i]).lower() in ['bill','bills','billed','billing']:
                s3=s3+" "+"billed".lower()+" "
            elif spell(s2[i]).lower() in ['mode','approach','form','mechanism','technique','course','modes','approaches','forms','mechanisms','techniques','courses']:
                s3=s3+" "+"mode".lower()+" "
            elif spell(s2[i]).lower() in ['top','main','major','prime','vital','primary','preeminent','crucial','dominant','chief','head','first','lead']:
                s3=s3+" "+"top".lower()+" "
            elif spell(s2[i]).lower() in ['count','number','sum','whole','reckon','figure','enumerate','add']:
                s3=s3+" "+"count".lower()+" "
            elif spell(s2[i]).lower() in ['receive','received','receiving','receives','receiving','collect','collects','collected','collecting','gather','gathers','gathering','gathered']:
                s3=s3+" "+"received".lower()+" "
            elif spell(s2[i]).lower() in ['turn','around','time','high','dollar','claims','claim']:
                s3=s3+" "+spell(s2[i]).lower()+" "
            else:
                s3=s3+" "+s2[i].lower()+" "
        s3=s3.replace('  ',' ').replace('  ',' ').strip(' ')
        return s3
    except:
        print("error in correcting string")


def greeting():
    """If any of the words in the user's input was a greeting, return a greeting response"""
    return random.choice(GREETING_RESPONSES)

def goodbye():
    """If any of the words in the user's input was a goodbye, return a goddbye response"""
    return random.choice(GOODBYE_RESPONSES)

def affirm():
    """If any of the words in the user's input was a goodbye, return a goddbye response"""
    return random.choice(AFFIRM_RESPONSES)

def claim_get_time(entities,text):
    claim_num=0
    for e in entities:
        if e['entity'].upper()=='Claim_Number'.upper():        
            claim_num=e['value']
    if claim_num==0:
        text=text.replace('  ',' ').replace('  ',' ').strip(' ')
        s2=text.split(' ')
        for i in range(0,len(s2)):            
            n=""
            for j in range(0,len(s2[i])):                    
                    try:
                        n1=int(s2[i][j])
                        n=n+str(n1)
                    except:
                        w=1
            if len(str(n)) == 10 and int(str(n)) > 0:
                claim_num=n
    if claim_num==0:
        claim_num=claim_numbers_req[len(claim_numbers_req)-1]
    else:
        claim_numbers_req.append(str(claim_num) )
        print(str(claim_numbers_req))
    res=str(get_processing_time(str(claim_num)))            
    print(res)            
    return res

def claim_get_action_reason(entities,text):
    claim_num=0
    for e in entities:
        if e['entity'].upper()=='Claim_Number'.upper():        
            claim_num=e['value']
        # if "amount" in corrected_ip_string(text):
        #     res1=claim_get_adj_amount(entities,text)
        #     return res1
    if claim_num==0:
        text=text.replace('  ',' ').replace('  ',' ').strip(' ')
        s2=text.split(' ')
        for i in range(0,len(s2)):            
            n=""
            for j in range(0,len(s2[i])):                    
                    try:
                        n1=int(s2[i][j])
                        n=n+str(n1)
                    except:
                        w=1
            if len(str(n)) == 10 and int(str(n)) > 0:
                claim_num=n
    if claim_num==0:
        claim_num=claim_numbers_req[len(claim_numbers_req)-1]
    else:
        claim_numbers_req.append(str(claim_num) )
        print(str(claim_numbers_req))
    res=str(get_action_reason(str(claim_num)))            
    print(res)            
    return res

def claim_get_status(entities,text):

    claim_num=0
    for e in entities:
        if e['entity'].upper()=='Claim_Number'.upper():        
            claim_num=e['value']
    if claim_num==0:
        text=text.replace('  ',' ').replace('  ',' ').strip(' ')
        s2=text.split(' ')
        for i in range(0,len(s2)):            
            n=""
            for j in range(0,len(s2[i])):                    
                    try:
                        n1=int(s2[i][j])
                        n=n+str(n1)
                    except:
                        w=1
            if len(str(n)) == 10 and int(str(n)) > 0:
                claim_num=n
    if claim_num==0:
        claim_num=claim_numbers_req[len(claim_numbers_req)-1]
    else:
        claim_numbers_req.append(str(claim_num) )
        print(str(claim_numbers_req))
    res=str(get_status(str(claim_num))).split('}')[1]
    print(res)            
    return res

def claim_get_den_reason(entities,text):
    claim_num=0
    for e in entities:
        if e['entity'].upper()=='Claim_Number'.upper():        
            claim_num=e['value']
    if claim_num==0:
        text=text.replace('  ',' ').replace('  ',' ').strip(' ')
        s2=text.split(' ')
        for i in range(0,len(s2)):            
            n=""
            for j in range(0,len(s2[i])):                    
                    try:
                        n1=int(s2[i][j])
                        n=n+str(n1)
                    except:
                        w=1
            if len(str(n)) == 10 and int(str(n)) > 0:
                claim_num=n
    if claim_num==0:
        claim_num=claim_numbers_req[len(claim_numbers_req)-1]
    else:
        claim_numbers_req.append(str(claim_num) )
        print(str(claim_numbers_req))
    res=str(get_denial_reason(str(claim_num)))
    print(res)            
    return res

def claim_get_resubmit(entities,text):
    claim_num=0
    for e in entities:
        if e['entity'].upper()=='Claim_Number'.upper():        
            claim_num=e['value']
    # if 'resubmit' in corrected_ip_string(text) or 'paid' in corrected_ip_string(text):
    #     ok=1
    # else:
    #     res1=claim_get_action_reason(entities,text)
    #     return res1
    if claim_num==0:
        text=text.replace('  ',' ').replace('  ',' ').strip(' ')
        s2=text.split(' ')
        for i in range(0,len(s2)):            
            n=""
            for j in range(0,len(s2[i])):                    
                    try:
                        n1=int(s2[i][j])
                        n=n+str(n1)
                    except:
                        w=1
            if len(str(n)) == 10 and int(str(n)) > 0:
                claim_num=n
    if claim_num==0:
        claim_num=claim_numbers_req[len(claim_numbers_req)-1]
    else:
        claim_numbers_req.append(str(claim_num) )
        print(str(claim_numbers_req))
    res=str(get_resubmit_proc())
    print(res)            
    return res

def claim_get_adj_reason(entities,text):
    claim_num=0
    for e in entities:
        if e['entity'].upper()=='Claim_Number'.upper():        
            claim_num=e['value']
    if claim_num==0:
        text=text.replace('  ',' ').replace('  ',' ').strip(' ')
        s2=text.split(' ')
        for i in range(0,len(s2)):            
            n=""
            for j in range(0,len(s2[i])):                    
                    try:
                        n1=int(s2[i][j])
                        n=n+str(n1)
                    except:
                        w=1
            if len(str(n)) == 10 and int(str(n)) > 0:
                claim_num=n
    if claim_num==0:
        claim_num=claim_numbers_req[len(claim_numbers_req)-1]
    else:
        claim_numbers_req.append(str(claim_num) )
        print(str(claim_numbers_req))
    res=str(get_adjustment_reason(str(claim_num)))
    print(res)            
    return res

def claim_get_adj_amount(entities,text):    # details of amount for claim which is adjusted not adjusted amount    
    claim_num=0
    claim_paid_amt_ind=0
    
    for e in entities:
        if e['entity'].upper()=='Claim_Number'.upper():        
            claim_num=e['value']
    if " paid ".upper() in corrected_ip_string(text).upper():        
        claim_paid_amt_ind=1
    
    if claim_num==0:
        text=text.replace('  ',' ').replace('  ',' ').strip(' ')
        s2=text.split(' ')
        for i in range(0,len(s2)):            
            n=""
            for j in range(0,len(s2[i])):                    
                    try:
                        n1=int(s2[i][j])
                        n=n+str(n1)
                    except:
                        w=1
            if len(str(n)) == 10 and int(str(n)) > 0:
                claim_num=n

    if claim_num==0:
        text=text.replace('  ',' ').replace('  ',' ').strip(' ')
        s2=text.split(' ')
        for i in range(0,len(s2)):            
            n=""
            for j in range(0,len(s2[i])):                    
                    try:
                        n1=int(s2[i][j])
                        n=n+str(n1)
                    except:
                        w=1
            if len(str(n)) == 10 and int(str(n)) > 0:
                claim_num=n

    if claim_num==0:
        claim_num=claim_numbers_req[len(claim_numbers_req)-1]
    else:
        claim_numbers_req.append(str(claim_num) )
        print(str(claim_numbers_req))
    if claim_paid_amt_ind==1:
        res=str(get_adj_amt_paid(str(claim_num)))
        print(res)            
        return res
    else:
        res=str(get_adjusted_amt(str(claim_num)))
        print(res)            
        return res



        



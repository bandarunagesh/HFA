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

def isdigit(str1):
    s2=str1.split(' ')
    for i in range(0,len(s2)):
            # s3=i.split()
        n=""
        for j in range(0,len(s2[i])):
                # print(j)
                try:
                    n1=int(s2[i][j])
                    n=n+str(n1)
                except:
                    w=1
        if len(str(n)) > 0 and (int(str(n)) > 10 or int(str(n)) < 10):
            return 1
        else:
            return 0

def corrected_ip_string(s1):
    print("corrected_ip_string")
    try:
        s1=s1.replace('  ',' ').replace('  ',' ').strip(' ')
        s2=s1.split(' ')
        s3=""
        for i in range(0,len(s2)):
            
            if s2[i].lower() in ["tat"]:
                s3=s3+" "+"tat".lower()+" "
            elif s2[i].lower() in ["jan","feb","mar","apr","jun","jul",'aug','sep','oct','nov','dec']:
                s3=s3+" "+s2[i].lower()+" "
            elif spell(s2[i]).upper() in ['JANUARY','FEBRUARY','MARCH','APRIL','MAY','JUNE','JULY','AUGUST','SEPTEMBER','OCTOBER','NOVEMBER','DECEMBER','MONTH','YEAR','QUARTER','FIRST','SECOND','THIRD','FOURTH','FIFTH','SIXTH','SEVENTH','EIGHTH','NINTH','TENTH','ELEVENTH','ONE','TWO','THREE','FOUR','FIVE','SIX','SEVEN','EIGHT','NINE','TEN','ELEVEN','MONTHS','YEARS','QUARTERS','ON','IN','SINCE','LAST','AGO','TWELFTH','TWELEVE']:
                s3=s3+" "+"".lower()+" "
            elif isdigit(s2[i])==1:
                s3=s3+" "+"".lower()+" "
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



def int_test():
    TCS_filename="c:\\users\\asrilekh\\documents\\Book7.xlsx"
    cdf = pd.read_excel(TCS_filename)
    op_lst=list()
    for i in range(0, len(cdf)):
        print(str(i))
        user_message = cdf.iloc[i,0]
        user_message=corrected_ip_string(user_message)
        user_message=corrected_ip_string(user_message.replace('-',' '))
        user_message=str(user_message).replace('?','').strip(' ').lower()
        response = requests.get("http://apsrp03693:5000/parse",params={"q":user_message})
        response = response.json()
        intent = response.get("intent")
        # op_lst.append(user_message+"!"+cdf.iloc[i,1]+"!"+intent['name'])
        op_lst.append(user_message+"!"+""+"!"+intent['name'])
    ############################
    merged_x="c:\\users\\asrilekh\\downloads\\book7.xlsx"
    merged_x_wb = xlsxwriter.Workbook(merged_x)
    merged_sheet = merged_x_wb.add_worksheet("det_recds")
    for deli in range(0, len(op_lst)):
        del_str = op_lst[deli].split('!')
        for delsi in range(0, len(del_str)):
            value_w="N/A" if str(del_str[delsi].strip(' '))=='' else str(del_str[delsi].strip(' '))
            merged_sheet.write(deli, delsi, value_w)  ##format changed
    merged_x_wb.close()
    ############################
    print("completed")

def int_test2():
    while(True):
        user_message = input("input str:")
        um1=user_message
        user_message=corrected_ip_string(user_message)
        user_message=corrected_ip_string(user_message.replace('-',' '))
        user_message=str(user_message).replace('?','').strip(' ').lower()
        response = requests.get("http://apsrp03693:5000/parse",params={"q":user_message})
        response = response.json()
        response["text"]=um1
        intent = response.get("intent")
        entities=response.get("entities")
        # print(str(intent)+"\n"+str(entities)+"\n"+str(response.get("text")))
        print(str(intent))


if __name__ == "__main__":
    int_test2()
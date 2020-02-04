from flask import Flask
from flask import render_template,jsonify,request
import requests
from models import *
from pblm_solving_files.knowledge_rev import *
from pblm_solving_files.duckling_wrapper import *
from pblm_solving_files.conv_history import *
from pblm_solving_files.uid_sessid_storing import *
from pblm_solving_files.mongodb_interaction import *
from pblm_solving_files.context_history import *
from pblm_solving_files.mongodb_interaction_srch import *
from pblm_solving_files.PA_mongoAPI import *
from pblm_solving_files.PAmongoSearchAPI import *
from pblm_solving_files.PA_context_history import *
from pblm_solving_files.PA_conv_history import *


import random
import urllib3
from flask_cors import CORS
import json

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.secret_key = '12345'
CORS(app)

@app.route('/')
def index():
    
    return render_template('index.html')


@app.route("/parse", methods=['GET', 'POST', 'OPTIONS'])
def parse():

    try:
        # print((request.url))
        parsed=(urllib3.util.url.parse_url(request.url))
        print(str(parsed.query))
        s1=str(str(parsed.query).split('&')[0].split('=')[1].replace('+',' ')) # first query
        uid_gen=1 # to check if user id was sent or not
        sessid_gen=1 # to check if session id was sent or not
        userid_ang="DEFAULT" # to store user id sent from angular
        sess_id_ang="DEFAULT"# to store session id sent from angular
        provider_lst=list() ### to store providers list
        req_from=""
        try:
            userid_ang=str(str(parsed.query).split('&')[1].split('=')[1].replace('+',' ')) # second query
        except:
            uid_gen=0
        try:
            sess_id_ang=str(str(parsed.query).split('&')[2].split('=')[1].replace('+',' ')) # second query
        except:
            sessid_gen=0
        try:            
            prov_id_ang=str(str(parsed.query).split('&')[3].split('=')[1].replace('+',' ')) # second query
            if '%2C' in prov_id_ang:
                provider_lst=prov_id_ang.split('%2C') 
            else:
                provider_lst=prov_id_ang.split(',') 
            print("provider_lst is "+str(provider_lst))
        except Exception as e:
            print(str(e))
            provid_gen=0
        try:
            req_from=str(str(parsed.query).split('&')[4].split('=')[1].replace('+',' ')) # second query
        except:
            req_from_gen=0
        try:
            req_chart_type=str(str(parsed.query).split('&')[5].split('=')[1].replace('+',' ')) # second query
        except:
            req_chart_type_gen=0
        try:
            req_type=str(str(parsed.query).split('&')[6].split('=')[1].replace('+',' ')) # second query
        except:
            req_type_gen=0
        if req_from.lower()=='search' and req_type.lower()=='prior_auth':
            ans = pa_main_func(userid_ang,sess_id_ang,s1,provider_lst,req_chart_type)
            return jsonify(ans)
        if req_from.lower()=='search':
            ans=main_fun(userid_ang,sess_id_ang,s1,provider_lst,req_chart_type) ## changed code after prior auth integration ##
            return jsonify(ans)
        if uid_gen==1 and sessid_gen==1:
            uid_sessid(userid_ang,sess_id_ang)
        # to remove unwanted characters
        print("userid="+userid_ang+"session id="+sess_id_ang)
        while True:
            a=s1.find("%")
            if a > -1:
                ss=s1[a]+s1[a+1]+s1[a+2]
                s1=s1.replace(ss," ")
            else:
                break        
        s1=s1.replace('  ',' ').replace('  ',' ').strip(' ')       
        print(s1)
        s1=str(s1)
        print(s1)
        # to remove unwanted characters
        if 'queries' in s1.lower().split(' ') and 'related' in s1.lower().split(' ') and 'to' in s1.lower().split(' ') and 'claims' in s1.lower().split(' '):
            # ts=pop_conv_hist(userid_ang,sess_id_ang)
            temp_ret=pop_context_hist_claim(userid_ang,sess_id_ang)
            if len(temp_ret)==0:
                ts="no conversation history found" ### just to be in tact with everything not really meant this statement
            else:
                ts="context history found"
            if ts=="no conversation history found":
                s1="status of claim "
            else:
                sugg_list=list()
                sugg_list.append("Yes")
                sugg_list.append("No")
                conv_uid=userid_ang
                conv_sesid=sess_id_ang
                conv_question="Queries related to claims"
                conv_answer="Do you want to continue with old claim number"
                conv_intent="Double request"
                conv_int_conf="0"
                conv_like_r_dislike="default"
                conv_obj_id=conv_hist(conv_uid,conv_sesid,conv_question,conv_answer,conv_intent,conv_int_conf,conv_like_r_dislike)
                return jsonify({"response":"Do you want to continue with old claim number","Suggestions":sugg_list})
        elif 'queries' in s1.lower().split(' ') and 'related' in s1.lower().split(' ') and 'to' in s1.lower().split(' ') and 'prior' in s1.lower().split(' ') and 'authorization' in s1.lower().split(' '):
            # ts=pop_conv_hist(userid_ang,sess_id_ang)
            temp_ret=pa_pop_context_hist_claim(userid_ang,sess_id_ang)
            if len(temp_ret)==0:
                ts="no conversation history found" ### just to be in tact with everything not really meant this statement
            else:
                ts="context history found"
            if ts=="no conversation history found":
                s1="status of prior auth "
            else:
                sugg_list=list()
                sugg_list.append("Yes")
                sugg_list.append("No")
                conv_uid=userid_ang
                conv_sesid=sess_id_ang
                conv_question="Queries related to prior auth"
                conv_answer="Do you want to continue with old hsc Id"
                conv_intent="Double request"
                conv_int_conf="0"
                conv_like_r_dislike="default"
                conv_obj_id=pa_conv_hist(conv_uid,conv_sesid,conv_question,conv_answer,conv_intent,conv_int_conf,conv_like_r_dislike)
                return jsonify({"response":"Do you want to continue with old hsc Id","Suggestions":sugg_list})
        elif 'queries' in s1.lower().split(' ') and 'related' in s1.lower().split(' ') and 'to' in s1.lower().split(' ') and 'member' in s1.lower().split(' ') and 'eligibility' in s1.lower().split(' '):
            return jsonify({"response":"Coming Soon.."}) 
        elif 'queries' in s1.lower().split(' ') and 'related' in s1.lower().split(' ') and 'to' in s1.lower().split(' ') and 'digital' in s1.lower().split(' '):
            return jsonify({"response":"Coming Soon.."}) 
        if s1.lower()=="yes" and req_type.lower()!="prior_auth":
            ts=pop_conv_hist(userid_ang,sess_id_ang)
            if ts=="Queries related to claims":
                s1="status of claim "+str((pop_context_hist_claim(userid_ang,sess_id_ang))[5])
        elif s1.lower()=="yes" and req_type.lower()=="prior_auth":
            ts=pa_pop_conv_hist(userid_ang,sess_id_ang)
            if ts == "Queries related to prior auth":
                s1 = "status of PA request "+str((pa_pop_context_hist_claim(userid_ang,sess_id_ang))[5])
        elif s1.lower()=="no" and req_type.lower()!="prior_auth":
            ts=pop_conv_hist(userid_ang,sess_id_ang)
            if ts=="Queries related to claims":
                conv_uid=userid_ang
                conv_sesid=sess_id_ang
                conv_question=ts
                conv_answer="question incomplete"
                conv_intent="request incomplete"
                conv_int_conf="0"
                conv_like_r_dislike="default"
                conv_obj_id=conv_hist(conv_uid,conv_sesid,conv_question,conv_answer,conv_intent,conv_int_conf,conv_like_r_dislike)
                return jsonify({"response":"Please enter claim number"})
        elif s1.lower()=="no" and req_type.lower()=="prior_auth":
            ts=pa_pop_conv_hist(userid_ang,sess_id_ang)
            if ts=="Queries related to prior auth":
                conv_uid=userid_ang
                conv_sesid=sess_id_ang
                conv_question=ts
                conv_answer="question incomplete"
                conv_intent="request incomplete"
                conv_int_conf="0"
                conv_like_r_dislike="default"
                conv_obj_id=pa_conv_hist(conv_uid,conv_sesid,conv_question,conv_answer,conv_intent,conv_int_conf,conv_like_r_dislike)
                return jsonify({"response":"Please enter hsc Id"})
        ########## to check if intents are greet, bye or affirm ############
        s1_test=s1
        temp_cn=str(claim_num_extract(s1))
        print("returned claim number/hsc_Id"+temp_cn)
        s1=s1.replace(temp_cn,'')
        s1=corrected_ip_string_1(s1,"CLAIM") # changed after integration
        print(s1)
        if len(s1.strip(' ')) > 0 and "status" not in s1.lower() and "claim" not in s1.lower() :  # changed after integration
            if req_type.lower()=="prior_auth":
                try:
                    response_g = requests.get("http://apsrp03693:8066/parse",params={"q":s1})               
                    response_g = response_g.json()   
                    intent_g = (response_g.get("intent"))
                    res_intent_g=(intent_g['name'])
                    intent_g=(intent_g)
                    res_intent_g=(str(res_intent_g))
                    gt_ind=0
                    if res_intent_g.lower()=="greet":
                        ans_g=greeting()
                        gt_ind=1
                    elif res_intent_g.lower()=="affirm" or res_intent_g.lower()=="none":
                        ans_g=affirm()
                        gt_ind=1
                    elif res_intent_g.lower()=="goodbye":
                        ans_g=goodbye()
                        gt_ind=2                             
                    
                    if gt_ind==1 or gt_ind==2:
                        if 'how' in s1.lower() and ('are' in s1.lower() or ' r ' in s1.lower()) and (' u ' in s1.lower() or 'you' in s1.lower()):
                            ans_g="Good! Thanks for asking"
                        elif 'who' in s1.lower() and ('are' in s1.lower() or ' r ' in s1.lower()) and (' u ' in s1.lower() or 'you' in s1.lower()):
                            ans_g="I am bot, How can I help you"
                        conv_uid_g=userid_ang
                        conv_sesid_g=sess_id_ang
                        conv_question_g=s1
                        conv_answer_g=ans_g
                        conv_intent_g=res_intent_g
                        conv_int_conf_g=str(intent_g['confidence'])
                        conv_like_r_dislike_g="default"
                        conv_obj_id_g=pa_conv_hist(conv_uid_g,conv_sesid_g,conv_question_g,conv_answer_g,conv_intent_g,conv_int_conf_g,conv_like_r_dislike_g)
                        return jsonify({"response":ans_g})            
                    print("returned intent from first request is "+res_intent_g)
                except Exception as e:
                    print(str(e))
            else:
                # s1=corrected_ip_string_1(s1,"claim")         
                print("claim number not present in statment before general suggestions intent retrieval")
                try:
                    response_g = requests.get("http://apsrp03693:5088/parse",params={"q":s1})               
                    response_g = response_g.json()   
                    intent_g = (response_g.get("intent"))
                    res_intent_g=(intent_g['name'])
                    intent_g=(intent_g)
                    res_intent_g=(str(res_intent_g))
                    gt_ind=0
                    if res_intent_g.lower()=="greet":
                        ans_g=greeting()
                        gt_ind=1
                    elif res_intent_g.lower()=="affirm" or res_intent_g.lower()=="none":
                        ans_g=affirm()
                        gt_ind=1
                    elif res_intent_g.lower()=="goodbye":
                        ans_g=goodbye()
                        gt_ind=2                             
                    
                    if gt_ind==1 or gt_ind==2:
                        if 'how' in s1.lower() and ('are' in s1.lower() or ' r ' in s1.lower()) and (' u ' in s1.lower() or 'you' in s1.lower()):
                            ans_g="Good! Thanks for asking"
                        elif 'who' in s1.lower() and ('are' in s1.lower() or ' r ' in s1.lower()) and (' u ' in s1.lower() or 'you' in s1.lower()):
                            ans_g="I am bot, How can I help you"
                        conv_uid_g=userid_ang
                        conv_sesid_g=sess_id_ang
                        conv_question_g=s1
                        conv_answer_g=ans_g
                        conv_intent_g=res_intent_g
                        conv_int_conf_g=str(intent_g['confidence'])
                        conv_like_r_dislike_g="default"
                        conv_obj_id_g=conv_hist(conv_uid_g,conv_sesid_g,conv_question_g,conv_answer_g,conv_intent_g,conv_int_conf_g,conv_like_r_dislike_g)
                        return jsonify({"response":ans_g})            
                    print("returned intent from first request is "+res_intent_g)
                except Exception as e:
                    print(str(e))
        s1=s1_test
        ########## to check if intents are greet, bye or affirm ############
        user_message = s1 # to store original user message in some variable
        um1=user_message # to store original user message in some variable

        #### context storing variables ##

        context_uid=userid_ang
        context_sessid=sess_id_ang
        context_type_of_req="default"
        context_claim_r_claims="default"
        context_context="default"
        context_claim_num="default"
        context_from="default"
        context_to="default"
        context_days=list()
        context_months=list()
        context_years=list()

        #### context storing variables ##

        
        #########   DERIVING CLAIM NUMBER AND IT'S CONTEXT IF CLAIM NUMBER IS IN REQUEST  #########
        if req_type.lower() == "prior_auth":
            claim_num='0'
            if True:
                print("entered if1 "+user_message)           
                claim_num=str(claim_num_extract(um1))
                if str(claim_num)=='0':
                    print("entered if2 "+user_message)           
                    junk=1
                else:
                    print("entered else2 "+user_message)           
                    context_claim_r_claims="PRIOR_AUTH"
                    context_claim_num=claim_num  
                    context_context=getStatusPA(str(context_claim_num))
                    if context_context.split('}')[0]=='1':
                        context_context="DENIED"
                    elif context_context.split('}')[0]=='2':
                        context_context="APPROVED"
                    elif context_context.split('}')[0]=='3':
                        context_context="CANCELLED" 
                    elif context_context.split('}')[0]=='4':
                        context_context="APPROVED"
                    elif context_context.split('}')[0]=='5':
                        context_context="PARTIALLY DENIED"
                    elif context_context.split('}')[0]=='6':
                        context_context="DENIED"
                    elif context_context.split('}')[0]=='7':
                        # context_context="NOT FOUND
                        conv_uid=userid_ang
                        conv_sesid=sess_id_ang
                        conv_question=um1
                        conv_answer="There is no PA claim available with provided hsc ID"
                        conv_intent="PA Claim Not Found"
                        conv_int_conf="0"
                        conv_like_r_dislike="default"
                        conv_obj_id=pa_conv_hist(conv_uid,conv_sesid,conv_question,conv_answer,conv_intent,conv_int_conf,conv_like_r_dislike)
                        return jsonify({"response":"There is no PA Claim available with provided hsc ID"}) 
                    user_message=user_message.replace(context_claim_num,'')
                    if len(user_message.strip(' '))==0:
                        print("entered if length 0")
                        um=pa_pop_conv_hist(userid_ang,sess_id_ang)+" "+um1.strip(' ')
                        if um.lower().strip(' ')==("Queries related to prior auth"+" "+um1.strip(' ')).strip(' ').lower():
                            user_message="Status of PA request "
                            um1="Status of PA request "
                        else:
                            user_message=um
                            um1=um
        else:
            claim_num='0'
            if True:
                print("entered if1 "+user_message)           
                claim_num=str(claim_num_extract(um1))
                if str(claim_num)=='0':
                    print("entered if2 "+user_message)           
                    junk=1
                else:
                    print("entered else2 "+user_message)           
                    context_claim_r_claims="CLAIM"
                    context_claim_num=claim_num  
                    context_context=get_status(str(context_claim_num))
                    if context_context.split('}')[0]=='1':
                        context_context="DENIED"
                    elif context_context.split('}')[0]=='2':
                        context_context="PAID"
                    elif context_context.split('}')[0]=='3':
                        context_context="ADJUSTED" 
                    elif context_context.split('}')[0]=='4':
                        context_context="PARTIALLY DENIED"
                    elif context_context.split('}')[0]=='5':
                        # context_context="NOT FOUND
                        conv_uid=userid_ang
                        conv_sesid=sess_id_ang
                        conv_question=um1
                        conv_answer="There is no Claim available with provided claim num"
                        conv_intent="Claim Not Found"
                        conv_int_conf="0"
                        conv_like_r_dislike="default"
                        conv_obj_id=conv_hist(conv_uid,conv_sesid,conv_question,conv_answer,conv_intent,conv_int_conf,conv_like_r_dislike)
                        return jsonify({"response":"There is no Claim available with provided claim num"}) 
                    user_message=user_message.replace(context_claim_num,'')
                    if len(user_message.strip(' '))==0:
                        print("entered if length 0")
                        um=pop_conv_hist(userid_ang,sess_id_ang)+" "+um1.strip(' ')
                        if um.lower().strip(' ')==("Queries related to claims"+" "+um1.strip(' ')).strip(' ').lower():
                            user_message="Status of Claim "
                            um1="Status of Claim "
                        else:
                            user_message=um
                            um1=um
            

        #########   DERIVING CLAIM NUMBER AND IT'S CONTEXT IF CLAIM NUMBER IS IN REQUEST  #########
        print("user message after claim number replacement is"+user_message)
        #days,months,years extracted to be returned
        dte_text_lst=list() # to replace text which refers to duaration of time
        if str(claim_num)=='0':
            dmy_lst=time_extract(um1) # returned from duckling            
            if len(dmy_lst) > 0:
                context_claim_r_claims="CLAIMS"
                if len(dmy_lst)==3:            
                    context_from=dmy_lst[0]
                    context_to=dmy_lst[1]            
                    dte_text_lst=dmy_lst[2]         
                elif len(dmy_lst)==4:
                    context_days=(dmy_lst[0])
                    context_months=(dmy_lst[1])
                    context_years=(dmy_lst[2])
                    dte_text_lst=dmy_lst[3]            
                for dte_i in dte_text_lst:
                    user_message=user_message.replace(" "+dte_i+" "," ")
            #days,months,years extracted to be returned
            print("user message after date text replacement is "+user_message)
            
        if req_type.lower() == 'prior_auth':
            dte_text_lst=list() # to replace text which refers to duaration of time
            if str(claim_num)=='0':
                dmy_lst=time_extract(um1) # returned from duckling            
                if len(dmy_lst) > 0:
                    context_claim_r_claims="PRIOR_AUTH"
                    if len(dmy_lst)==3:            
                        context_from=dmy_lst[0]
                        context_to=dmy_lst[1]            
                        dte_text_lst=dmy_lst[2]         
                    elif len(dmy_lst)==4:
                        context_days=(dmy_lst[0])
                        context_months=(dmy_lst[1])
                        context_years=(dmy_lst[2])
                        dte_text_lst=dmy_lst[3]            
                    for dte_i in dte_text_lst:
                        user_message=user_message.replace(" "+dte_i+" "," ")
                #days,months,years extracted to be returned
                print("user message after date text replacement is "+user_message)

        # print("user_message is "+user_message)
        # user_message=user_message.replace(" - ","-")
        # user_message=corrected_ip_string_1(user_message,"CLAIM")
        # user_message=corrected_ip_string_1(user_message.replace('-',' '))           

        #### retrieving values from context collection ########
        if req_type.lower()!="prior_auth":
            if len(dte_text_lst)==0 and str(claim_num)=='0':
                ret_cntxt=pop_context_hist(context_uid,context_sessid)
                print("returned context"+str(ret_cntxt))
                if len(ret_cntxt) > 0:
                    # changed after integration of pA
                    if claim_r_claims_present(user_message)=='claim':
                        ret_cntxt=pop_context_hist_claim(context_uid,context_sessid)
                    elif claim_r_claims_present(user_message)=='claims':
                        ret_cntxt=pop_context_hist_claims(context_uid,context_sessid)
                    # changed after integration of pA
                    context_type_of_req=ret_cntxt[2]
                    context_claim_r_claims=ret_cntxt[3]
                    context_context=ret_cntxt[4]
                    context_claim_num=ret_cntxt[5]
                    context_from=ret_cntxt[6]
                    context_to=ret_cntxt[7]
                    context_days=ret_cntxt[8]
                    context_months=ret_cntxt[9]
                    context_years=ret_cntxt[10]
                else:
                    conv_uid=userid_ang
                    conv_sesid=sess_id_ang
                    conv_question=um1
                    conv_answer="question incomplete"
                    conv_intent="request incomplete"
                    conv_int_conf="0"
                    conv_like_r_dislike="default"
                    conv_obj_id=conv_hist(conv_uid,conv_sesid,conv_question,conv_answer,conv_intent,conv_int_conf,conv_like_r_dislike)
                    return jsonify({"response":"Please enter claim number for claims/hsc Id for PA"})   
        else:
            if len(dte_text_lst)==0 and str(claim_num)=='0':
                ret_cntxt=pa_pop_context_hist(context_uid,context_sessid)
                print("returned context"+str(ret_cntxt))
                if len(ret_cntxt) > 0:  
                    context_type_of_req=ret_cntxt[2]
                    context_claim_r_claims=ret_cntxt[3]
                    context_context=ret_cntxt[4]
                    context_claim_num=ret_cntxt[5]
                    context_from=ret_cntxt[6]
                    context_to=ret_cntxt[7]
                    context_days=ret_cntxt[8]
                    context_months=ret_cntxt[9]
                    context_years=ret_cntxt[10]
                else:
                    conv_uid=userid_ang
                    conv_sesid=sess_id_ang
                    conv_question=um1
                    conv_answer="question incomplete"
                    conv_intent="request incomplete"
                    conv_int_conf="0"
                    conv_like_r_dislike="default"
                    conv_obj_id=pa_conv_hist(conv_uid,conv_sesid,conv_question,conv_answer,conv_intent,conv_int_conf,conv_like_r_dislike)
                    return jsonify({"response":"Please enter claim number for claims/hsc Id for PA"})

        #### retrieving values from context collection ########

        #########   DERIVING CONTEXT IF THERE IS DURATION IS IN REQUEST  #########
        if str(context_claim_r_claims).upper()=="CLAIMS":   

            if "high" in user_message.lower() and "dollar" in user_message.lower():
                context_context="HIGH DOLLAR"         
            elif "partial" in user_message.lower() and "denied" in user_message.lower():
                context_context="PARTIALLY DENIED"
            elif "denied" in user_message.lower():
                context_context="DENIED" 
            elif "adjusted" in user_message.lower():
                context_context="ADJUSTED"
            elif "received" in user_message.lower():
                context_context="RECEIVED"             
            else:
                ret_cntxt=pop_context_hist(context_uid,context_sessid)
                if len(ret_cntxt) > 0:  
                    if ret_cntxt[3].upper()=="CLAIMS":
                        context_context=ret_cntxt[4]
                    else:
                        context_context="RECEIVED"             
                    if context_context.lower()=="default":
                        context_context="RECEIVED"
        elif str(context_claim_r_claims).upper()=="PRIOR_AUTH":
            if "denied" in user_message.lower():
                context_context="DENIED" 
            elif "approved" in user_message.lower():
                context_context="APPROVED"
            elif "cancelled" in user_message.lower():
                context_context="CANCELLED"
            elif "received" in user_message.lower():
                context_context="RECEIVED"
            else:
                ret_cntxt=pa_pop_context_hist(context_uid,context_sessid)
                if len(ret_cntxt) > 0:  
                    if ret_cntxt[3].upper()=="PRIOR_AUTH":
                        context_context=ret_cntxt[4]
                    else:
                        context_context="RECEIVED"             
                    if context_context.lower()=="default":
                        context_context="RECEIVED"
        #########   DERIVING CONTEXT IF THERE IS DURATION IS IN REQUEST  #########   

        ##### addding claim/claims accordingly #######

        if context_claim_r_claims=='CLAIM':
            if 'claim' not in user_message.lower():
                # user_message=user_message+" for claim"  ## cahnged after integration
                user_message=user_message+" claim" ## cahnged after integration
        elif context_claim_r_claims=='CLAIMS':
            if 'claims' not in user_message.lower():
                # user_message=user_message+" towards claims" ## cahnged after integration
                user_message=user_message+" claims" ## cahnged after integration
        elif context_claim_r_claims=='PRIOR_AUTH':
            if 'prior auth' not in user_message.lower():
                user_message=user_message+" towards PA"
        ###################################################

        print("user_message is "+user_message)
        user_message=user_message.replace(" - ","-")
        if req_type.lower() != "prior_auth":
            user_message=corrected_ip_string_1(user_message,context_claim_r_claims)
            user_message=corrected_ip_string_1(user_message.replace('-',' '),context_claim_r_claims) 
        user_message=str(user_message).strip(' ').lower() 

        ####################################################
               
        ##### addding claim/claims accordingly #######
        if req_type.lower() != "prior_auth":
            response = requests.get("http://apsrp03693:5088/parse",params={"q":user_message})                
            response = response.json()
            
    
            # response text to be returned
            res_text=um1
            # response text to be returned
    
                # intent to be returned
            intent = response.get("intent")
            res_intent=intent['name']
            res_intent_confidence=intent['confidence']
            res_claim_num=context_claim_num
            # intent to be returned
            entities_retrieved=response.get("entities")  
            par_ind=0   
            for er_i in entities_retrieved:
                if er_i["entity"]=="par_entity" or er_i["entity"]=="non_par_entity":
                    par_ind=1

            print("returned intent is "+res_intent)
            if res_intent.lower().strip(' ') in ['affirm','goodbye','greet']: # changed# changed after integration
                if "status" in user_message: # changed after integration
                    res_intent="status" # changed after integration
            ans="Unanswered"
            sugg_list=list()
            if res_intent.upper().strip(' ')=="par_r_non_par_claim".upper():
                if par_ind==0 and "status" in user_message.lower():
                    res_intent="status"
            
            if res_intent.upper().strip(' ')=="claim_hgh_dlr_status".upper():
                if "dollar" not in user_message.lower() and "status" in user_message.lower():
                    res_intent="status"
            if res_intent.upper().strip(' ')=="ACTION_REASON".upper():
                if "denied" not in user_message.lower() and "adjusted" not in user_message.lower() and "status" in user_message.lower():
                    res_intent="status"
            if res_intent.upper().strip(' ')=="claims_type".upper():
                if "claims" not in user_message.lower():
                    res_intent="type_of_claim"
            if NPI_present(user_message):            
                res_intent="NPI_OF_CLAIM".lower()
            # changes after integration with prior auth   
            if res_intent.upper().strip(' ')=="STATUS":
                ans=get_status(str(res_claim_num))
                ans=ans.split('}')[1]
                sugg=ans.split('!')            
                for si in range(1,len(sugg)):                
                    sugg_list.append(sugg[si])            
    
            elif res_intent.upper().strip(' ')=="TIME":
                ans=get_proc_time(res_claim_num)
                print(ans)
                sugg_list.append("Date of service")
                sugg_list.append("Receipt Date")
                sugg_list.append("Paid Date")
                sugg_list.append("Claim Type")
            elif res_intent.upper().strip(' ')=="ACTION_REASON":
                
                if "denied" in user_message.lower() and "partial" in user_message.lower():
                    if context_context=="PAID" or context_context=="ADJUSTED" or context_context=="DENIED":
                        ans="Your claim has no partial denials. "+get_status(str(res_claim_num)).split('}')[1].replace('Your claim has been ','It got ')
                    else:
                        ans=get_denial_reason(res_claim_num)
                        print(ans)
                elif "denied" in user_message.lower():
                    if context_context=="PAID" or context_context=="ADJUSTED":
                        ans="Your claim has no denials. "+get_status(str(res_claim_num)).split('}')[1].replace('Your claim has been ','It got ')
                    else:
                        ans=get_denial_reason(res_claim_num)
                        print(ans)
                elif "adjusted" in user_message.lower():
                    if context_context=="PAID" or context_context=="PARTIALLY DENIED" or context_context=="DENIED":
                        ans="Your claim has no adjustments. "+get_status(str(res_claim_num)).split('}')[1].replace('Your claim has been ','It got ')
                    else:
                        ans=get_adj_reason(res_claim_num)
                else:
                    if context_context=="PAID":
                        ans="Your claim is completely paid"
                    elif context_context=="ADJUSTED":
                        ans=get_adj_reason(res_claim_num)
                    elif context_context=="PARTIALLY DENIED" or context_context=="DENIED":
                        ans=get_denial_reason(res_claim_num)
                print(ans)
                if context_context=="PAID":
                    sugg_list.append("Billed Amount")
                    sugg_list.append("Claim Type")
                    sugg_list.append("TAT")
                    sugg_list.append("Submission Mode")
                elif context_context=="ADJUSTED":
                    sugg_list.append("Adjusted Amount")
                    sugg_list.append("Paid Amount")
                    sugg_list.append("TAT")
                    sugg_list.append("Status")
                else:
                    sugg_list.append("Billed Amount")
                    sugg_list.append("Submission Mode")
                    sugg_list.append("TAT")
                    sugg_list.append("Status")
            elif res_intent.upper().strip(' ')=='RESUBMIT':
                ans=get_resubmit_proc()
                print(ans)
                if context_context=="PAID":
                    sugg_list.append("Billed Amount")
                    sugg_list.append("Claim Type")
                    sugg_list.append("TAT")
                    sugg_list.append("Submission Mode")
                elif context_context=="ADJUSTED":
                    sugg_list.append("Adjusted Amount")
                    sugg_list.append("Paid Amount")
                    sugg_list.append("TAT")
                    sugg_list.append("Adjustment Reason")
                else:
                    sugg_list.append("Billed Amount")
                    sugg_list.append("Submission Mode")
                    sugg_list.append("TAT")
                    sugg_list.append("Denial Reason")
            elif res_intent.upper().strip(' ')=="CLAIM_AMOUNT":
                if 'billed' in user_message.lower():
                    ans=get_billed_amt(res_claim_num)
                elif 'allowed' in user_message.lower():
                    ans=get_allowed_amt(res_claim_num)
                elif 'interest' in user_message.lower():
                    ans=get_interest_amt(res_claim_num)
                elif 'paid'  in user_message.lower():
                    if context_context=="DENIED":
                       ans= "Your claim was not paid as it is Completely denied  and "+get_billed_amt(res_claim_num)
                    else:
                        ans=get_paid_amt(res_claim_num)
                elif "denied" in user_message.lower():
                    if context_context=="PAID" or context_context=="ADJUSTED":
                        ans="You have no denials for your claim"
                    else:
                        ans=get_denied_amt(res_claim_num)
                elif "adjusted" in user_message.lower():
                    if context_context=="ADJUSTED":
                        ans=get_adjusted_amt(res_claim_num)
                    else:
                        ans="Your claim doesn't have any adjustments"
                print(ans)
                if context_context=="PAID":
                    sugg_list.append("Allowed Amount")
                    sugg_list.append("Interest Amount")
                    sugg_list.append("TAT")
                    sugg_list.append("Submission Mode")
                elif context_context=="ADJUSTED":
                    sugg_list.append("Allowed Amount")
                    sugg_list.append("Interest Amount")
                    sugg_list.append("TAT")
                    sugg_list.append("Adjustment Reason")
                else:
                    sugg_list.append("Allowed Amount")
                    sugg_list.append("Interest Amount")
                    sugg_list.append("TAT")
                    sugg_list.append("Denial Reason")
    
            
            elif res_intent.upper().strip(' ')=="CLAIM_DATE":
                if 'service' in user_message.lower():
                    ans=get_service_date_of_claim(res_claim_num)
                    sugg_list.append("TAT")
                    sugg_list.append("Receipt Date")
                    sugg_list.append("Paid Date")
                    sugg_list.append("Claim Type")
                elif 'received' in user_message.lower():
                    ans=get_rcvd_date_of_claim(res_claim_num)                
                    sugg_list.append("Date of service")
                    sugg_list.append("TAT")
                    sugg_list.append("Paid Date")
                    sugg_list.append("Claim Type")  
                elif 'submitted' in user_message.lower():
                    ans=get_sbmtd_date_of_claim(res_claim_num)                
                    sugg_list.append("Date of service")
                    sugg_list.append("TAT")
                    sugg_list.append("Paid Date")
                    sugg_list.append("Claim Type") 
                elif 'adjudicated' in user_message.lower():
                    ans=get_adjudicate_date_of_claim(res_claim_num) 
                    sugg_list.append("Date of Service")
                    sugg_list.append("Receipt Date")
                    sugg_list.append("TAT")
                    sugg_list.append("Claim Type")
                elif 'paid'  in user_message.lower():
                    if context_context=="DENIED":
                       ans= "Your claim was not paid as it is Completely denied and "+get_dend_date_of_claim(res_claim_num)
                    else:
                        ans=get_paid_date_of_claim(res_claim_num)
                    sugg_list.append("Date of Service")
                    sugg_list.append("Receipt Date")
                    sugg_list.append("TAT")
                    sugg_list.append("Claim Type")
                elif "denied" in user_message.lower():
                    if context_context=="PAID" or context_context=="ADJUSTED":
                        ans="You have no denials for your claim and "+get_paid_date_of_claim(res_claim_num)
                    else:
                        ans=get_dend_date_of_claim(res_claim_num)
                    sugg_list.append("Date of Service")
                    sugg_list.append("Receipt Date")
                    sugg_list.append("TAT")
                    sugg_list.append("Claim Type")
                elif "adjusted" in user_message.lower():
                    if context_context=="ADJUSTED":
                        ans=get_adjstd_date_of_claim(res_claim_num)
                    else:
                        ans="Your claim doesn't have any adjustments and "+get_paid_date_of_claim(res_claim_num)
                    sugg_list.append("Date of Service")
                    sugg_list.append("Receipt Date")
                    sugg_list.append("TAT")
                    sugg_list.append("Claim Type")
                print(ans)
            elif res_intent.upper().strip(' ')== "CLAIM_LINE_ITEMS":
                ans=get_line_items(res_claim_num)
                sugg_list.append("TAT")
                sugg_list.append("Diagnosis Codes")
                sugg_list.append("Submission Mode")
                sugg_list.append("NPI")
                sugg_list.append("Claim Type")
            elif res_intent.upper().strip(' ')== "TYPE_OF_CLAIM":
                ans=get_type_of_claim(res_claim_num)
                sugg_list.append("TAT")
                sugg_list.append("Diagnosis Codes")
                sugg_list.append("Submission Mode")
                sugg_list.append("Par Status")
                sugg_list.append("Line Items")
            elif res_intent.upper().strip(' ')== "PAR_R_NON_PAR_CLAIM":
                ans=get_par_non_par(res_claim_num)
                sugg_list.append("TAT")
                sugg_list.append("Diagnosis Codes")
                sugg_list.append("Submission Mode")
                sugg_list.append("NPI")
                sugg_list.append("Claim Type")
            elif res_intent.upper().strip(' ')=="NPI_OF_CLAIM":
                ans=get_npi_of_claim(res_claim_num)
                sugg_list.append("TAT")
                sugg_list.append("Diagnosis Codes")
                sugg_list.append("Submission Mode")
                sugg_list.append("Par Status")
                sugg_list.append("Claim Type")
            elif res_intent.upper().strip(' ')=="LOB_OF_CLAIM":
                ans=get_lob_of_claim(res_claim_num)
                sugg_list.append("TAT")
                sugg_list.append("Diagnosis Codes")
                sugg_list.append("Billed Amount")
                sugg_list.append("Par Status")
                sugg_list.append("Claim Type")
            elif res_intent.upper().strip(' ')== "CLAIM_TAX_ID":
                ans=get_tax_id_claim(res_claim_num)
                sugg_list.append("TAT")
                sugg_list.append("Diagnosis Codes")
                sugg_list.append("Submission Mode")
                sugg_list.append("Par Status")
                sugg_list.append("Claim Type")
            elif res_intent.upper().strip(' ')== "CLAIM_DIAG_CODES":
                ans=get_diag_cd_claim(res_claim_num)
                sugg_list.append("Revise and Resubmit")
                sugg_list.append("LOB")
                sugg_list.append("Par Status")
                sugg_list.append("Claim Type")
            elif res_intent.upper().strip(' ')== "claim_submsn_mode".upper():
                ans=get_mode_submission_claim(res_claim_num)
                sugg_list.append("Billed Amount")
                sugg_list.append("TAT")
                sugg_list.append("Par Status")
                sugg_list.append("Claim Type")
            elif res_intent.upper().strip(' ')=="claim_hgh_dlr_status".upper():
                ans=hgh_dlr_claim_status(res_claim_num)
                sugg_list.append("Billed Amount")
                sugg_list.append("TAT")
                sugg_list.append("Par Status")
                sugg_list.append("Claim Type")
            elif res_intent.upper().strip(' ')== "claims_count".upper():
                dur_list=list()
                if context_from.upper()=="default".upper():
                    dur_list.append(context_days)
                    dur_list.append(context_months)
                    dur_list.append(context_years)
                else:
                    dur_list.append(context_from)
                    dur_list.append(context_to)
                if "paid" in user_message.lower():
                    if context_context=="HIGH DOLLAR":
                        ans=get_paid_cnt_claims_hgh_dlr(dur_list,provider_lst)
                    else:
                        ans=get_paid_cnt_claims_recvd(dur_list,provider_lst)
                else:
                    if context_context=="HIGH DOLLAR":
                        ans=get_hgh_dlr_claims_cnt(dur_list,provider_lst)
                    elif context_context=="PARTIALLY DENIED":
                        ans=get_prtl_denied_claims_cnt(dur_list,provider_lst)
                    elif context_context=="DENIED" :
                        ans=get_denied_claims_cnt(dur_list,provider_lst)
                    elif context_context=="ADJUSTED":
                        ans=get_adjusted_claims_cnt(dur_list,provider_lst)
                    elif context_context=="RECEIVED":
                        ans=get_received_claims(dur_list,provider_lst)
                ans=ans.replace('}','')
            elif res_intent.upper().strip(' ')== "claims_amount".upper():
                dur_list=list()
                if context_from.upper()=="default".upper():
                    dur_list.append(context_days)
                    dur_list.append(context_months)
                    dur_list.append(context_years)
                else:
                    dur_list.append(context_from)
                    dur_list.append(context_to)
                if "billed" in user_message.lower():
                    if context_context=="HIGH DOLLAR":
                        ans=get_bill_amt_hgh_dlr(dur_list,provider_lst)
                    elif context_context=="PARTIALLY DENIED":
                        ans=get_bill_amt_prtl_dend(dur_list,provider_lst)
                    elif context_context=="DENIED" :
                        ans=get_bill_amt_dend(dur_list,provider_lst)
                    elif context_context=="ADJUSTED":
                        ans=get_bill_amt_adjusted(dur_list,provider_lst)
                    elif context_context=="RECEIVED":
                        ans=get_bill_amt_recvd(dur_list,provider_lst)
                    ans=ans.replace('}','')
                elif "paid" in user_message.lower():
                    if context_context=="HIGH DOLLAR":
                        ans=get_paid_amt_claims_hgh_dlr(dur_list,provider_lst)
                    elif context_context=="PARTIALLY DENIED":
                        ans=get_paid_amt_prtl_dend(dur_list,provider_lst)
                    elif context_context=="DENIED" :
                        ans="As Claims are denied no amount will be paid towards them"
                    elif context_context=="ADJUSTED":
                        ans=get_paid_amt_adjusted(dur_list,provider_lst)
                    elif context_context=="RECEIVED":
                        ans=get_paid_amt_claims_recvd(dur_list,provider_lst)
                    ans=ans.replace('}','')
                # elif "denied" in user_message.lower():--------------denial amount to be implemented
                elif "adjusted" in user_message.lower():
                    ### if condition for high dollar claims--------------to be implemented
                    ans=get_adjstd_amt_adjusted(dur_list,provider_lst)
                    ans=ans.replace('}','')    
            elif res_intent.upper().strip(' ')=="CLAIMS_SUBMISSION_MODE":
                dur_list=list()
                if context_from.upper()=="default".upper():
                    dur_list.append(context_days)
                    dur_list.append(context_months)
                    dur_list.append(context_years)
                else:
                    dur_list.append(context_from)
                    dur_list.append(context_to)
                if context_context=="HIGH DOLLAR":
                    ans=get_mode_submission_hgh_dlr(dur_list,provider_lst)
                elif context_context=="PARTIALLY DENIED":
                    ans=get_mode_submission_prtl_dend(dur_list,provider_lst)
                elif context_context=="DENIED" :
                    ans=get_mode_submission_dend(dur_list,provider_lst)
                elif context_context=="ADJUSTED":
                    ans=get_mode_submission_adjstd(dur_list,provider_lst)
                elif context_context=="RECEIVED":
                    ans=get_mode_submission_recvd(dur_list,provider_lst)
                ans=ans.replace('}','')   
            elif res_intent.upper().strip(' ')=="claims_action_reasons".upper():
                dur_list=list()
                if context_from.upper()=="default".upper():
                    dur_list.append(context_days)
                    dur_list.append(context_months)
                    dur_list.append(context_years)
                else:
                    dur_list.append(context_from)
                    dur_list.append(context_to)
                if context_context=="PARTIALLY DENIED":
                    ans=get_denied_claims_actin_resns(dur_list,provider_lst)
                elif context_context=="DENIED" :
                    ans=get_denied_claims_actin_resns(dur_list,provider_lst)
                elif context_context=="ADJUSTED":
                    ans=get_adjstd_claims_actin_resns(dur_list,provider_lst)
                ans=ans.replace('}','')      
            else:
                ans="I am not prepare for your question as of now"
            
            
            print("answer="+ans)
            ## suugestions list to be derived##       
            ans=ans.split('!')[0]
            ###### context history push call #######   
            print(context_uid,context_sessid,context_type_of_req,context_claim_r_claims,context_context,context_claim_num,context_from,context_to,context_days,context_months,context_years)     
            push_context_hist(context_uid,context_sessid,context_type_of_req,context_claim_r_claims,context_context,context_claim_num,context_from,context_to,context_days,context_months,context_years)
            ###### context history push call #######
            #####conv_history parameters and function call ########
            conv_uid=userid_ang
            conv_sesid=sess_id_ang
            conv_question=res_text
            conv_answer=ans
            conv_intent=res_intent
            conv_int_conf=res_intent_confidence
            conv_like_r_dislike="default"
            conv_obj_id=conv_hist(conv_uid,conv_sesid,conv_question,conv_answer,conv_intent,conv_int_conf,conv_like_r_dislike)
            #####conv_history parameters and function call ########
            print(conv_uid)
            print(conv_sesid)
            print(conv_question)
            print(conv_answer)
            print(conv_intent)
            print(conv_int_conf)
            print(conv_like_r_dislike)
            if conv_answer == "Unanswered" or conv_answer == "Sorry, Could not fetch you results at this time" or conv_answer=="I am not prepare for your question as of now":
                conv_answer=u"Sorry I do not have an answer for that. You may reach out to us through call or email for assistance."
            for si in range(0,len(sugg_list)):
                if sugg_list[si].lower()=="Date of service".lower():
                    sugg_list[si]="What is the date of service for the claim?"
                elif sugg_list[si].lower()=="Receipt Date".lower():
                    sugg_list[si]="When was the claim received?"
                elif sugg_list[si].lower()=="Paid Date".lower():
                    sugg_list[si]="When was the claim paid?"    
                elif sugg_list[si].lower()=="Claim Type".lower():
                    sugg_list[si]="What is the claim type?"
                elif sugg_list[si].lower()=="Billed Amount".lower():
                    sugg_list[si]="How much amount got billed for the claim?"
                elif sugg_list[si].lower()=="TAT".lower():
                    sugg_list[si]="What is the turnaround time for the claim?"
                elif sugg_list[si].lower()=="Submission Mode".lower():
                    sugg_list[si]="What is the mode of submission for the claim?"
                elif sugg_list[si].lower()=="Adjusted Amount".lower():
                    sugg_list[si]="What amount was adjusted?"
                elif sugg_list[si].lower()=="Paid Amount".lower():
                    sugg_list[si]="What amount got paid?"
                elif sugg_list[si].lower()=="Status".lower():
                    sugg_list[si]="What is the status of the claim?"
                elif sugg_list[si].lower()=="Adjustment Reason".lower():
                    sugg_list[si]="What are the reasons for adjustments in the claim?"
                elif sugg_list[si].lower()=="Denial Reason".lower():
                    sugg_list[si]="What are the reasons for denial?"
                elif sugg_list[si].lower()=="Allowed Amount".lower():
                    sugg_list[si]="How much amount is Allowed?"
                elif sugg_list[si].lower()=="Interest Amount".lower():
                    sugg_list[si]="What is the interest amount paid for the claim?"
                elif sugg_list[si].lower()=="Diagnosis Codes".lower():
                    sugg_list[si]="What are the diagnosis codes?"
                elif sugg_list[si].lower()=="NPI".lower():
                    sugg_list[si]="What is the National Provider Identifier of the provider?"
                elif sugg_list[si].lower()=="Par Status".lower():
                    sugg_list[si]="What is the PAR status of the claim?"
                elif sugg_list[si].lower()=="Revise and Resubmit".lower():
                    sugg_list[si]="How to revise and resubmit the claim?"
                elif sugg_list[si].lower()=="LOB".lower():
                    sugg_list[si]="What line of business does this claim belong to?"
                elif sugg_list[si].lower()=="Line Items".lower():
                    sugg_list[si]="How many line items are present in the claim?"
            return jsonify({"response":conv_answer,"object_id":conv_obj_id,"Suggestions":sugg_list})
        elif req_type.lower() == 'prior_auth':
            response = requests.get("http://apsrp03693:8066/parse",params={"q":user_message})                
            response = response.json()
            
            # response text to be returned
            res_text=um1
            # response text to be returned
    
            # intent to be returned
            intent = response.get("intent")
            res_intent=intent['name']
            res_intent_confidence=intent['confidence']
            res_claim_num=context_claim_num
            # intent to be returned
            # entities=response.get("entities")                
            print("returned intent is "+res_intent)
            ans = "Unanswered"
            sugg_list = []
            if res_intent.lower() == "status_prior_auth":
                ans = getStatusPA(str(res_claim_num))
                sugg_list.append("When was the PA requested?")
                sugg_list.append("What's the turnaround time for the PA?")
                sugg_list.append("What's the service setting type for the PA?")
                sugg_list.append("How many line items are there?")
            elif res_intent.lower() == "pa_request_date":
                ans = getRequestSubmittedDate(str(res_claim_num))
                sugg_list.append("What's the turnaround time for the PA?")
                sugg_list.append("What's the service type of the PA?")
                sugg_list.append("What was the service category of the PA?")
            elif res_intent.lower() == "pa_decision":
                ans = getDecisionDate(str(res_claim_num))
                sugg_list.append("What's the turnaround time for the PA?")
                sugg_list.append("What are the reasons for denial?")
                sugg_list.append("What line of business does this PA belong to?")
                sugg_list.append("How many line items are there?")
            elif res_intent.lower() == "pa_service_type":
                ans = getServiceType(str(res_claim_num))
                sugg_list.append("What's the service setting type for the PA?")
                sugg_list.append("When was the decision made on the PA request?")
                sugg_list.append("What was the service category of the PA?")
            elif res_intent.lower() == "pa_service_cat":
                ans = getServiceCategory(str(res_claim_num))
                sugg_list.append("What's the service setting type for the PA?")
                sugg_list.append("What's the service type of the PA?")
                sugg_list.append("What line of business does this PA belong to?")
            elif res_intent.lower() == "pa_service_setting":
                ans = getServiceSettingType(str(res_claim_num))
                sugg_list.append("When was the PA requested?")
                sugg_list.append("When was the decision made on the PA request?")
                sugg_list.append("What's the turnaround time for the PA?")
                sugg_list.append("How many line items are there?")
            elif res_intent.lower() == "pa_lob":
                ans = getLOBPA(str(res_claim_num))
                sugg_list.append("What's the service type of the PA?")
                sugg_list.append("What was the service category of the PA?")
                sugg_list.append("What's the service setting type for the PA?")
            elif res_intent.lower() == "pa_taxid":
                ans = getTaxID(str(res_claim_num))
                sugg_list.append("When was the decision made on the PA request?")
                sugg_list.append("What line of business does this PA belong to?")
                sugg_list.append("What's the service type of the PA?")
            elif res_intent.lower() == "pa_line_items":
                ans = getLineItems(str(res_claim_num))
                sugg_list.append("What's the service type of the PA?")
                sugg_list.append("What's the turnaround time for the PA?")
                sugg_list.append("What was the service category of the PA?")
            elif res_intent.lower() == "pa_tat":
                ans = getTATPA(str(res_claim_num))
                sugg_list.append("When was the decision made on the PA request?")
                sugg_list.append("What are the reasons for denial?")
                sugg_list.append("What's the service setting type for the PA?")
            elif res_intent.lower() == "pa_denial_rsns":
                ans = getReasonsDenials(str(res_claim_num))
                sugg_list.append("What was the service category of the PA?")
                sugg_list.append("When was the decision made on the PA request?")
                sugg_list.append("What's the service setting type for the PA?")
            elif res_intent.lower() == "pa_cancel_rsns":
                ans = getCancelReasons(str(res_claim_num))
                sugg_list.append("What was the service category of the PA?")
                sugg_list.append("When was the decision made on the PA request?")
                sugg_list.append("What's the service setting type for the PA?")
            elif res_intent.lower() == "pa_approve_rsns":
                ans = getApprovalReasons(str(res_claim_num))
                sugg_list.append("What was the service category of the PA?")
                sugg_list.append("When was the decision made on the PA request?")
                sugg_list.append("What's the service setting type for the PA?")
            else:
                ans="I am not prepare for your question as of now"
                
            print(context_uid,context_sessid,context_type_of_req,context_claim_r_claims,context_context,context_claim_num,context_from,context_to,context_days,context_months,context_years)     
            pa_push_context_hist(context_uid,context_sessid,context_type_of_req,context_claim_r_claims,context_context,context_claim_num,context_from,context_to,context_days,context_months,context_years)
            ###### context history push call #######
            #####conv_history parameters and function call ########
            conv_uid=userid_ang
            conv_sesid=sess_id_ang
            conv_question=res_text
            conv_answer=ans
            conv_intent=res_intent
            conv_int_conf=res_intent_confidence
            conv_like_r_dislike="default"
            conv_obj_id=pa_conv_hist(conv_uid,conv_sesid,conv_question,conv_answer,conv_intent,conv_int_conf,conv_like_r_dislike)
            #####conv_history parameters and function call ########
            print(conv_uid)
            print(conv_sesid)
            print(conv_question)
            print(conv_answer)
            print(conv_intent)
            print(conv_int_conf)
            print(conv_like_r_dislike)
            if conv_answer == "Unanswered" or conv_answer == "Sorry, Could not fetch you results at this time" or conv_answer=="I am not prepare for your question as of now":
                conv_answer=u"Sorry I do not have an answer for that. You may reach out to us through call or email for assistance."
            return jsonify({"response":conv_answer,"object_id":conv_obj_id,"Suggestions":sugg_list})
    except Exception as e:
    # else:
        print(e) 
        return jsonify({"response":"Sorry I do not have an answer for that. You may reach out to us through call or email for assistance."})   

app.config["DEBUG"] = True
if __name__ == "__main__":
    app.run(host='apsrp03693',port=8030,debug=True)

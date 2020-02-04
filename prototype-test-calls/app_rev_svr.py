from flask import Flask
from flask import render_template,jsonify,request
import requests
from models import *
from pblm_solving_files.calls_knowledge_rev import *
from pblm_solving_files.duckling_wrapper import *
from pblm_solving_files.calls_conv_history import *
from pblm_solving_files.calls_uid_sessid_storing import *
from pblm_solving_files.calls_context_history import *
from pblm_solving_files.calls_mongodb_interaction import *
import random
import urllib3
from flask_cors import CORS
import json
from datetime import datetime



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
        ## changed code after prior auth integration ##
        while True:
            a=s1.find("%")
            if a > -1:
                ss=s1[a]+s1[a+1]+s1[a+2]
                s1=s1.replace(ss," ")
            else:
                break 
        s1=s1.replace('  ',' ').replace('  ',' ').strip(' ') 
        ## changed code after prior auth integration ##
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
        ## changed code after prior auth integration ##
        try:
            req_chart_type=str(str(parsed.query).split('&')[5].split('=')[1].replace('+',' ')) # second query
        except:
            req_chart_type_gen=0
        try:
            req_claim_type_req=str(str(parsed.query).split('&')[6].split('=')[1].replace('+',' ')) # second query
        except:
            req_claim_type_req_gne=0
        ## changed code after prior auth integration ##
        # if req_from.lower()=='search':
        #     ans=main_fun(userid_ang,sess_id_ang,s1,provider_lst,req_chart_type) ## changed code after prior auth integration ##
        #     return jsonify(ans)
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
        if 'queries' in s1.lower().split(' ') and 'related' in s1.lower().split(' ') and 'to' in s1.lower().split(' ') and 'calls' in s1.lower().split(' '):
            # ts=pop_conv_hist(userid_ang,sess_id_ang)
            temp_ret=pop_context_hist_call(userid_ang,sess_id_ang)
            if len(temp_ret)==0:
                ts="no conversation history found" ### just to be in tact with everything not really meant this statement
            else:
                ts="context history found"
            if ts=="no conversation history found":
                s1="Information About Call"
            else:
                sugg_list=list()
                sugg_list.append("Yes")
                sugg_list.append("No")
                conv_uid=userid_ang
                conv_sesid=sess_id_ang
                conv_question="Queries related to Calls"
                conv_answer="Do you want to continue with old call id"
                conv_intent="Double request"
                conv_int_conf="0"
                conv_like_r_dislike="default"
                conv_obj_id=calls_push_conv_hist(conv_uid,conv_sesid,conv_question,conv_answer,conv_intent,conv_int_conf,conv_like_r_dislike)
                return jsonify({"response":"Do you want to continue with old call id","Suggestions":sugg_list})
        
        if s1.lower()=="yes":
            ts=calls_pop_conv_hist(userid_ang,sess_id_ang)
            if ts=="Queries related to Calls":
                s1="Information About Call "+str((pop_context_hist_call(userid_ang,sess_id_ang))[5])
        elif s1.lower()=="no":
            ts=calls_pop_conv_hist(userid_ang,sess_id_ang)
            if ts=="Queries related to Calls":
                conv_uid=userid_ang
                conv_sesid=sess_id_ang
                conv_question=ts
                conv_answer="question incomplete"
                conv_intent="request incomplete"
                conv_int_conf="0"
                conv_like_r_dislike="default"
                conv_obj_id=calls_push_conv_hist(conv_uid,conv_sesid,conv_question,conv_answer,conv_intent,conv_int_conf,conv_like_r_dislike)
                return jsonify({"response":"Please enter call id"}) 
        ########## to check if intents are greet, bye or affirm ############
        s1_test=s1
        temp_cn=str(call_id_extract(s1))
        print("returned call id "+temp_cn)
        s1=s1.replace(temp_cn,'')
        s1=corrected_ip_string_call(s1,"CALL") # changed after integration
        response_g = requests.get("http://apsrp03693:5089/parse",params={"q":s1})
        response_g=response_g.json()
        entities_ret=response_g.get("entities")
        # entities_ret=[]
        if len(entities_ret)==0:
            ### implement greet,bye,affirm logic
            junk=1
        print(s1)        
        s1=s1_test
        ########## to check if intents are greet, bye or affirm ############
        user_message = s1 # to store original user message in some variable
        um1=user_message # to store original user message in some variable

        #### context storing variables ##

        context_uid=userid_ang
        context_sessid=sess_id_ang
        context_type_of_req="default"
        if req_from.lower()=='search':
            context_call_r_calls="calls"
        elif req_from.lower()=='chat':
            context_call_r_calls="call"
        context_context="NA"
        if req_from.lower()=='search':
            context_call_id="NA"
        elif req_from.lower()=='chat':
            context_call_id="NA"
        context_from="default"
        context_to="default"
        context_days=list()
        context_months=list()
        context_years=list()

        #### context storing variables ##

        
        #########   DERIVING CALL ID AND IT'S CONTEXT IF CALL ID IS IN REQUEST  #########

        call_id='0'
        if True:
            print("entered if1 "+user_message)           
            call_id=str(call_id_extract(um1))
            if str(call_id)=='0':
                print("entered if2 "+user_message)           
                junk=1
            else:
                context_call_id=call_id
                print("entered else2 "+user_message)                                            
                call_id_flag=get_call_id_presence(str(call_id))
                if call_id_flag:
                    ok=1
                else:
                    # context_context="NOT FOUND
                    conv_uid=userid_ang
                    conv_sesid=sess_id_ang
                    conv_question=um1
                    conv_answer="There is no Call Information available with provided Call ID"
                    conv_intent="Call ID Not Found"
                    conv_int_conf="0"
                    conv_like_r_dislike="default"
                    conv_obj_id=calls_push_conv_hist(conv_uid,conv_sesid,conv_question,conv_answer,conv_intent,conv_int_conf,conv_like_r_dislike)
                    return jsonify({"response":"There is no Call Information available with provided Call ID"}) 
                user_message=user_message.replace(context_call_id,'')
                if len(user_message.strip(' '))==0:
                    print("entered if length 0")
                    um=calls_pop_conv_hist(userid_ang,sess_id_ang)+" "+um1.strip(' ')
                    if um.lower().strip(' ')==("Queries related to calls"+" "+um1.strip(' ')).strip(' ').lower():
                        user_message="Information about call"
                        um1="Information about call"
                    else:
                        user_message=um
                        um1=um                    

        #########   DERIVING call NUMBER AND IT'S CONTEXT IF call NUMBER IS IN REQUEST  #########
        print("user message after call number replacement is"+user_message)

        #days,months,years extracted to be returned

        dte_text_lst=list() # to replace text which refers to duaration of time
        if str(call_id)=='0':
            dmy_lst=time_extract(um1) # returned from duckling            
            if len(dmy_lst) > 0:                                
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

        #### retrieving values from context collection ########        

        if len(dte_text_lst)==0 and str(call_id)=='0':
            
            if req_from.lower()=='chat':
                ret_cntxt=pop_context_hist_call(context_uid,context_sessid)
                if len(ret_cntxt) > 0:                    
                    context_call_id=ret_cntxt[5]
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
                    conv_obj_id=calls_push_conv_hist(conv_uid,conv_sesid,conv_question,conv_answer,conv_intent,conv_int_conf,conv_like_r_dislike)
                    return jsonify({"response":"Please enter call id"}) 
            elif req_from.lower()=='search':
                context_call_id="NA"
                ret_cntxt=pop_context_hist_calls(context_uid,context_sessid)
                # ret_cntxt=[] # ----- needs to uncommented if you don't need history for search
                if len(ret_cntxt) > 0:                                        
                    context_from=ret_cntxt[6]
                    context_to=ret_cntxt[7]
                    context_days=ret_cntxt[8]
                    context_months=ret_cntxt[9]
                    context_years=ret_cntxt[10]
                else:
                    try:                        
                        yr_lst_1=[]
                        yr_lst_1.append(str(datetime.now().year))                            
                    except Exception as e:
                        print(str(e))
                        junk=1
                    context_from="default"
                    context_to="default"
                    context_days=[]
                    context_months=[]
                    context_years=yr_lst_1

        #### retrieving values from context collection ########         

        ###################################################

        print("user_message is "+user_message)
        user_message=user_message.replace(" - ","-")
        print("user_message is "+user_message)
        print(str(context_call_r_calls))
        user_message=corrected_ip_string_call(user_message,context_call_r_calls)
        print("user_message is "+user_message)
        print(str(context_call_r_calls))
        user_message=corrected_ip_string_call(user_message.replace('-',' '),context_call_r_calls) 
        print("user_message is "+user_message)
        print(str(context_call_r_calls))
        user_message=str(user_message).strip(' ').lower() 
        print("user_message is "+user_message)
        print(str(context_call_r_calls))
        ####################################################

        ##### addding call/calls accordingly #######
        if req_from.lower()=='search':            
            if 'calls' not in user_message.lower():                
                user_message=user_message+" calls" ## cahnged after integration
        elif req_from.lower()=='chat':
            if 'call' not in user_message.lower():                
                user_message=user_message+" call" ## cahnged after integration
               
        ##### addding call/calls accordingly #######
        
        if req_from.lower()=='search': 
            user_message=correct_sentence_for_calls(user_message)
        
        response = requests.get("http://apsrp03693:5089/parse",params={"q":user_message})                
        response = response.json()
        

        # response text to be returned
        res_text=um1
        # response text to be returned
        # changes after integration with prior auth
        # intent to be returned
        intent = response.get("intent")
        res_intent=str(intent['name']).strip(' ').lower()
        res_intent_confidence=intent['confidence']
        res_call_id=context_call_id
        
        # intent to be returned
        entities_retrieved=response.get("entities")  
        ans="Unanswered"
        sugg_list=list()
        res_intent_temp=res_intent
        um_arr=user_message.lower().split(' ')

        if "information" in um_arr and "status" in um_arr and "call" in um_arr:
            res_intent="call_info"

        elif res_intent=="call_type":

            if "product" in um_arr:
                res_intent="call_product_type"
        
        elif res_intent=="call_transferrred":
            
            res_intent="call_transferred"

        elif res_intent=="call_time":
            
            if "hold" in um_arr:
                res_intent="call_hold_time"
            elif "talk" in um_arr:
                res_intent="call_talk_time"
            elif "ring" in um_arr:
                res_intent="call_ring_time"
        
        elif res_intent=="calls_count":

            if "eligibility" in um_arr:
                if "lob" in um_arr:
                    res_intent="calls_cnt_eligible_lob"
                elif "type" in um_arr and "product" in um_arr:
                    res_intent="calls_cnt_eligible_prod_type"
                elif "type" in um_arr :
                    res_intent="calls_cnt_eligible_type"
                elif "transferred" in um_arr :
                    res_intent="calls_cnt_eligible_trnsfr"
                elif "answered" in um_arr :
                    res_intent="calls_cnt_eligible_ans"
                elif "language" in um_arr :
                    res_intent="calls_cnt_eligible_lang"
                elif calls_BU_present(um_arr):
                    res_intent="calls_cnt_eligible_bu"
                else:
                    res_intent="calls_cnt_eligible"
            elif "benefits" in um_arr:
                if "lob" in um_arr:
                    res_intent="calls_cnt_ben_lob"
                elif "type" in um_arr and "product" in um_arr:
                    res_intent="calls_cnt_ben_prod_type"
                elif "type" in um_arr :
                    res_intent="calls_cnt_ben_type"
                elif "transferred" in um_arr :
                    res_intent="calls_cnt_ben_trnsfr"
                elif "answered" in um_arr :
                    res_intent="calls_cnt_ben_ans"
                elif "language" in um_arr :
                    res_intent="calls_cnt_ben_lang"
                elif calls_BU_present(um_arr):
                    res_intent="calls_cnt_ben_bu"
                else:
                    res_intent="calls_cnt_ben"
            elif "prior" in um_arr and "auth" in um_arr:
                if "lob" in um_arr:
                    res_intent="calls_cnt_pa_lob"
                elif "type" in um_arr and "product" in um_arr:
                    res_intent="calls_cnt_pa_prod_type"
                elif "type" in um_arr :
                    res_intent="calls_cnt_pa_type"
                elif "transferred" in um_arr :
                    res_intent="calls_cnt_pa_trnsfr"
                elif "answered" in um_arr :
                    res_intent="calls_cnt_pa_ans"
                elif "language" in um_arr :
                    res_intent="calls_cnt_pa_lang"
                elif calls_BU_present(um_arr):
                    res_intent="calls_cnt_pa_bu"
                else:
                    res_intent="calls_cnt_pa"
            elif "claims" in um_arr:
                if "lob" in um_arr:
                    res_intent="calls_cnt_claims_lob"
                elif "type" in um_arr and "product" in um_arr:
                    res_intent="calls_cnt_claims_prod_type"
                elif "type" in um_arr :
                    res_intent="calls_cnt_claims_type"
                elif "transferred" in um_arr :
                    res_intent="calls_cnt_claims_trnsfr"
                elif "answered" in um_arr :
                    res_intent="calls_cnt_claims_ans"
                elif "language" in um_arr :
                    res_intent="calls_cnt_claims_lang"
                elif calls_BU_present(um_arr):
                    res_intent="calls_cnt_claims_bu"
                else:
                    res_intent="calls_cnt_claims"
            
            elif "appeal" in um_arr:
                if "lob" in um_arr:
                    res_intent="calls_cnt_appeal_lob"
                elif "type" in um_arr and "product" in um_arr:
                    res_intent="calls_cnt_appeal_prod_type"
                elif "type" in um_arr :
                    res_intent="calls_cnt_appeal_type"
                elif "transferred" in um_arr :
                    res_intent="calls_cnt_appeal_trnsfr"
                elif "answered" in um_arr :
                    res_intent="calls_cnt_appeal_ans"
                elif "language" in um_arr :
                    res_intent="calls_cnt_appeal_lang"
                elif calls_BU_present(um_arr):
                    res_intent="calls_cnt_appeal_bu"
                else:
                    res_intent="calls_cnt_appeal"

            elif "unanswered" in um_arr:
                if "lob" in um_arr:
                    res_intent="calls_cnt_unans_lob"
                elif "type" in um_arr and "product" in um_arr:
                    res_intent="calls_cnt_unans_prod_type"
                elif "type" in um_arr :
                    res_intent="calls_cnt_unans_type"
                elif "transferred" in um_arr :
                    res_intent="calls_cnt_unans_trnsfr"
                elif "answered" in um_arr :
                    res_intent="calls_cnt_unans_ans"
                elif "language" in um_arr :
                    res_intent="calls_cnt_unans_lang"
                elif calls_BU_present(um_arr):
                    res_intent="calls_cnt_unans_bu"
                else:
                    res_intent="calls_cnt_unans"
            elif "answered" in um_arr:
                if "lob" in um_arr:
                    res_intent="calls_cnt_ans_lob"
                elif "type" in um_arr and "product" in um_arr:
                    res_intent="calls_cnt_ans_prod_type"
                elif "type" in um_arr :
                    res_intent="calls_cnt_ans_type"
                # elif "transferred" in um_arr :
                #     res_intent="calls_cnt_ans_trnsfr"
                elif "language" in um_arr :
                    res_intent="calls_cnt_ans_lang"
                elif calls_BU_present(um_arr):
                    res_intent="calls_cnt_ans_bu"
                else:
                    res_intent="calls_cnt_ans"
            elif "transferred" in um_arr:
                if "lob" in um_arr:
                    res_intent="calls_cnt_trnsfr_lob"
                elif "type" in um_arr and "product" in um_arr:
                    res_intent="calls_cnt_trnsfr_prod_type"
                elif "type" in um_arr :
                    res_intent="calls_cnt_trnsfr_type"
                # elif "answered" in um_arr :
                #     res_intent="calls_cnt_trnsfr_ans"
                elif "language" in um_arr :
                    res_intent="calls_cnt_trnsfr_lang"
                elif calls_BU_present(um_arr):
                    res_intent="calls_cnt_trnsfr_bu"
                else:
                    res_intent="calls_cnt_trnsfr"
            else:
                if "lob" in um_arr:
                    res_intent="calls_cnt_lob"
                elif "type" in um_arr and "product" in um_arr:
                    res_intent="calls_cnt_prod_type"
                elif "type" in um_arr :
                    res_intent="calls_cnt_type"
                elif "transferred" in um_arr :
                    res_intent="calls_cnt_trnsfr"
                elif "answered" in um_arr :
                    res_intent="calls_cnt_ans"
                elif "language" in um_arr :
                    res_intent="calls_cnt_lang"
                elif calls_BU_present(um_arr):
                    res_intent="calls_cnt_bu"
                else:
                    res_intent="calls_cnt"
            if res_intent=="calls_cnt_trnsfr" and "by" in um_arr:
                res_intent="calls_cnt_trnsfr_by"
            elif res_intent=="calls_cnt_ans" and "by" in um_arr:
                res_intent="calls_cnt_ans_by"

        
        elif res_intent=="calls_tat":

            if "hold" in um_arr:
                if "lob" in um_arr:
                    res_intent="calls_tat_hold_lob"
                elif "type" in um_arr and "product" in um_arr:
                    res_intent="calls_tat_hold_prod_type"
                elif "type" in um_arr :
                    res_intent="calls_tat_hold_type"
                elif "transferred" in um_arr :
                    res_intent="calls_tat_hold_trnsfr"
                elif "answered" in um_arr :
                    res_intent="calls_tat_hold_ans"
                elif "language" in um_arr :
                    res_intent="calls_tat_hold_lang"
                elif calls_BU_present(um_arr):
                    res_intent="calls_tat_hold_bu"
                else:
                    res_intent="calls_tat_hold"
            elif "ring" in um_arr:
                if "lob" in um_arr:
                    res_intent="calls_tat_ring_lob"
                elif "type" in um_arr and "product" in um_arr:
                    res_intent="calls_tat_ring_prod_type"
                elif "type" in um_arr :
                    res_intent="calls_tat_ring_type"
                elif "transferred" in um_arr :
                    res_intent="calls_tat_ring_trnsfr"
                elif "answered" in um_arr :
                    res_intent="calls_tat_ring_ans"
                elif "language" in um_arr :
                    res_intent="calls_tat_ring_lang"
                elif calls_BU_present(um_arr):
                    res_intent="calls_tat_ring_bu"
                else:
                    res_intent="calls_tat_ring"
            elif "talk" in um_arr:
                if "lob" in um_arr:
                    res_intent="calls_tat_talk_lob"
                elif "type" in um_arr and "product" in um_arr:
                    res_intent="calls_tat_talk_prod_type"
                elif "type" in um_arr :
                    res_intent="calls_tat_talk_type"
                elif "transferred" in um_arr :
                    res_intent="calls_tat_talk_trnsfr"
                elif "answered" in um_arr :
                    res_intent="calls_tat_talk_ans"
                elif "language" in um_arr :
                    res_intent="calls_tat_talk_lang"
                elif calls_BU_present(um_arr):
                    res_intent="calls_tat_talk_bu"
                else:
                    res_intent="calls_tat_talk"            
            else:
                if "lob" in um_arr:
                    res_intent="calls_tat_lob"
                elif "type" in um_arr and "product" in um_arr:
                    res_intent="calls_tat_prod_type"
                elif "type" in um_arr :
                    res_intent="calls_tat_type"
                elif "transferred" in um_arr :
                    res_intent="calls_tat_trnsfr"
                elif "answered" in um_arr :
                    res_intent="calls_tat_ans"
                elif calls_BU_present(um_arr):
                    res_intent="calls_tat_bu"
                elif "language" in um_arr :
                    res_intent="calls_tat_lang"
                else:
                    res_intent="calls_tat"
        elif res_intent=="transfer_rate":
            if "lob" in um_arr:
                res_intent="calls_trnsfr_rt_lob"
            elif "type" in um_arr and "product" in um_arr:
                res_intent="calls_trnsfr_rt_prod_type"
            elif "type" in um_arr :
                res_intent="calls_trnsfr_rt_type"            
            elif "language" in um_arr :
                res_intent="calls_trnsfr_rt_lang"
            elif calls_BU_present(um_arr):
                print("entered if of bu present cond")
                res_intent="calls_trnsfr_rt_bu"
            else:
                res_intent="calls_trnsfr_rt"
        elif res_intent=="top_calls_tat":
            if "talk" in um_arr:
                res_intent="top_calls_tat_talk"
            elif "ring" in um_arr:
                res_intent="top_calls_tat_ring"
            elif "hold" in um_arr:
                res_intent="top_calls_tat_hold"
        print(res_intent)
        ##### function calls
        if res_intent=="call_info":
            ans=get_call_info(res_call_id)
            sugg_list.append("Allowed Amount")
            sugg_list.append("Interest Amount")
            sugg_list.append("TAT")
            sugg_list.append("Submission Mode")

        elif res_intent=="call_received_date":

            ans=get_call_received_date(res_call_id)
            sugg_list.append("Allowed Amount")
            sugg_list.append("Interest Amount")
            sugg_list.append("TAT")
            sugg_list.append("Submission Mode")
        elif res_intent=="call_bu":

            ans=get_call_BU(res_call_id)
            sugg_list.append("Allowed Amount")
            sugg_list.append("Interest Amount")
            sugg_list.append("TAT")
            sugg_list.append("Submission Mode")
        elif res_intent=="call_time":

            ans=get_call_time(res_call_id)
            sugg_list.append("Allowed Amount")
            sugg_list.append("Interest Amount")
            sugg_list.append("TAT")
            sugg_list.append("Submission Mode")

        elif res_intent=="call_type":

            ans=get_call_type(res_call_id)
            sugg_list.append("Allowed Amount")
            sugg_list.append("Interest Amount")
            sugg_list.append("TAT")
            sugg_list.append("Submission Mode")

        elif res_intent=="call_product_type":

            ans=get_call_product_type(res_call_id)
            sugg_list.append("Allowed Amount")
            sugg_list.append("Interest Amount")
            sugg_list.append("TAT")
            sugg_list.append("Submission Mode")

        elif res_intent=="call_hold_time":

            ans=get_call_hold_time(res_call_id)
            sugg_list.append("Allowed Amount")
            sugg_list.append("Interest Amount")
            sugg_list.append("TAT")
            sugg_list.append("Submission Mode")

        elif res_intent=="call_ring_time":

            ans=get_call_ring_time(res_call_id)
            sugg_list.append("Allowed Amount")
            sugg_list.append("Interest Amount")
            sugg_list.append("TAT")
            sugg_list.append("Submission Mode")

        elif res_intent=="call_talk_time":

            ans=get_call_talk_time(res_call_id)
            sugg_list.append("Allowed Amount")
            sugg_list.append("Interest Amount")
            sugg_list.append("TAT")
            sugg_list.append("Submission Mode")
        
        elif res_intent=="call_lob":

            ans=get_call_lob(res_call_id)
            sugg_list.append("Allowed Amount")
            sugg_list.append("Interest Amount")
            sugg_list.append("TAT")
            sugg_list.append("Submission Mode")

        elif res_intent=="call_answered":

            ans=get_call_answered(res_call_id)
            sugg_list.append("Allowed Amount")
            sugg_list.append("Interest Amount")
            sugg_list.append("TAT")
            sugg_list.append("Submission Mode")

        elif res_intent=="call_transferred":

            ans=get_call_transferred(res_call_id)
            sugg_list.append("Allowed Amount")
            sugg_list.append("Interest Amount")
            sugg_list.append("TAT")
            sugg_list.append("Submission Mode")

        elif res_intent=="call_language":
            ans=get_call_language(res_call_id)
            sugg_list.append("Allowed Amount")
            sugg_list.append("Interest Amount")
            sugg_list.append("TAT")
            sugg_list.append("Submission Mode")

        elif res_intent=="calls_cnt_trnsfr_by":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            # ans=get_calls_cnt_eligible_lob function(dur_list,provider_lst)
            ans=get_calls_cnt_trnsfr_by(dur_list,provider_lst)
        
        elif res_intent=="calls_cnt_ans_by":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            # ans=get_calls_cnt_eligible_lob function(dur_list,provider_lst)
            ans=get_calls_cnt_ans_by(dur_list,provider_lst)

        elif res_intent=="calls_cnt_eligible_lob":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")            
            ans=get_calls_cnt_eligible_lob(dur_list,provider_lst)
        
        elif res_intent=="top_calls_tat":
            
            dur_list=list()
            n=5
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
                if len(context_days) > 0:
                    n=context_days[0]
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")                        
            ans=get_top_calls_total_time(dur_list,n)

        elif res_intent=="top_calls_tat_talk":

            dur_list=list()
            n=5
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
                if len(context_days) > 0:
                    n=context_days[0]
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")                        
            ans=get_top_calls_talk_time(dur_list,n)
        
        elif res_intent=="top_calls_tat_ring":

            dur_list=list()
            n=5
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
                if len(context_days) > 0:
                    n=context_days[0]
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")                        
            ans=get_top_calls_ring_time(dur_list,n)
        
        elif res_intent=="top_calls_tat_hold":

            dur_list=list()
            n=5
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
                if len(context_days) > 0:
                    n=context_days[0]
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")                        
            ans=get_top_calls_hold_time(dur_list,n)
        
        elif res_intent=="top_calls_tin":

            dur_list=list()
            n=5
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
                if len(context_days) > 0:
                    n=context_days[0]
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")  
                                      
            ans=get_top_calls_tin(dur_list,n)

        elif res_intent=="calls_cnt_eligible_prod_type":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_cnt_eligible_prod_type(dur_list,provider_lst)

        elif res_intent=="calls_cnt_eligible_type":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_cnt_eligible_type(dur_list,provider_lst)

        elif res_intent=="calls_cnt_eligible_trnsfr":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_cnt_eligible_trnsfr(dur_list,provider_lst)

        elif res_intent=="calls_cnt_eligible_ans":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_cnt_eligible_ans(dur_list,provider_lst)

        elif res_intent=="calls_cnt_eligible_lang":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_cnt_eligible_lang(dur_list,provider_lst)
        
        elif res_intent=="calls_cnt_eligible_bu":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_cnt_eligible_BU(dur_list,provider_lst)

        elif res_intent=="calls_cnt_eligible":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_cnt_eligible(dur_list,provider_lst)
        
        elif res_intent=="calls_cnt_appeal_lob":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            # ans=get_calls_cnt_eligible_lob function(dur_list,provider_lst)
            ans=get_calls_cnt_appeal_lob(dur_list,provider_lst)

        elif res_intent=="calls_cnt_appeal_prod_type":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_cnt_appeal_prod_type(dur_list,provider_lst)

        elif res_intent=="calls_cnt_appeal_type":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_cnt_appeal_type(dur_list,provider_lst)

        elif res_intent=="calls_cnt_appeal_trnsfr":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_cnt_appeal_trnsfr(dur_list,provider_lst)

        elif res_intent=="calls_cnt_appeal_ans":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_cnt_appeal_ans(dur_list,provider_lst)

        elif res_intent=="calls_cnt_appeal_lang":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_cnt_appeal_lang(dur_list,provider_lst)
        
        elif res_intent=="calls_cnt_appeal_bu":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_cnt_appeal_BU(dur_list,provider_lst)

        elif res_intent=="calls_cnt_appeal":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_cnt_appeal(dur_list,provider_lst)

        elif res_intent=="calls_cnt_ben_lob":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_cnt_ben_lob(dur_list,provider_lst)

        elif res_intent=="calls_cnt_ben_prod_type":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_cnt_ben_prod_type(dur_list,provider_lst)

        elif res_intent=="calls_cnt_ben_type":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_cnt_ben_type(dur_list,provider_lst)

        elif res_intent=="calls_cnt_ben_trnsfr":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_cnt_ben_trnsfr(dur_list,provider_lst)

        elif res_intent=="calls_cnt_ben_ans":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_cnt_ben_ans(dur_list,provider_lst)

        elif res_intent=="calls_cnt_ben_lang":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_cnt_ben_lang(dur_list,provider_lst)
        
        elif res_intent=="calls_cnt_ben_bu":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_cnt_ben_BU(dur_list,provider_lst)

        elif res_intent=="calls_cnt_ben":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_cnt_ben(dur_list,provider_lst)

        elif res_intent=="calls_cnt_pa_lob":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_cnt_pa_lob(dur_list,provider_lst)

        elif res_intent=="calls_cnt_pa_prod_type":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_cnt_pa_prod_type(dur_list,provider_lst)

        elif res_intent=="calls_cnt_pa_type":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_cnt_pa_type(dur_list,provider_lst)

        elif res_intent=="calls_cnt_pa_trnsfr":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_cnt_pa_trnsfr(dur_list,provider_lst)

        elif res_intent=="calls_cnt_pa_ans":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_cnt_pa_ans(dur_list,provider_lst)

        elif res_intent=="calls_cnt_pa_lang":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_cnt_pa_lang(dur_list,provider_lst)
        
        elif res_intent=="calls_cnt_pa_bu":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_cnt_pa_BU(dur_list,provider_lst)

        elif res_intent=="calls_cnt_pa":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_cnt_pa(dur_list,provider_lst)

        elif res_intent=="calls_cnt_claims_lob":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_cnt_claims_lob(dur_list,provider_lst)

        elif res_intent=="calls_cnt_claims_prod_type":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_cnt_claims_prod_type(dur_list,provider_lst)

        elif res_intent=="calls_cnt_claims_type":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_cnt_claims_type(dur_list,provider_lst)

        elif res_intent=="calls_cnt_claims_trnsfr":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_cnt_claims_trnsfr(dur_list,provider_lst)

        elif res_intent=="calls_cnt_claims_ans":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_cnt_claims_ans(dur_list,provider_lst)

        elif res_intent=="calls_cnt_claims_lang":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_cnt_claims_lang(dur_list,provider_lst)
        
        elif res_intent=="calls_cnt_claims_bu":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_cnt_claims_BU(dur_list,provider_lst)

        elif res_intent=="calls_cnt_claims":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_cnt_claims(dur_list,provider_lst)

        elif res_intent=="calls_cnt_unans_lob":

            ans=get_calls_cnt_unans_lob()

        elif res_intent=="calls_cnt_unans_prod_type":

            ans=get_calls_cnt_unans_prod_type()

        elif res_intent=="calls_cnt_unans_type":

            ans=get_calls_cnt_unans_type()

        elif res_intent=="calls_cnt_unans_trnsfr":

            ans=get_calls_cnt_unans_trnsfr()

        elif res_intent=="calls_cnt_unans_ans":

            ans=get_calls_cnt_unans_ans()

        elif res_intent=="calls_cnt_unans_lang":

            ans=get_calls_cnt_unans_lang()
        
        elif res_intent=="calls_cnt_unans_bu":

            ans=get_calls_cnt_unans_bu()

        elif res_intent=="calls_cnt_unans":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_cnt_unans(dur_list,provider_lst)

        elif res_intent=="calls_cnt_ans_lob":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_cnt_ans_lob(dur_list,provider_lst)

        elif res_intent=="calls_cnt_ans_prod_type":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_cnt_ans_prod_type(dur_list,provider_lst)

        elif res_intent=="calls_cnt_ans_type":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_cnt_ans_type(dur_list,provider_lst)

        elif res_intent=="calls_cnt_ans_trnsfr":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_cnt_ans_trnsfr(dur_list,provider_lst)

        elif res_intent=="calls_cnt_ans_lang":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_cnt_ans_lang(dur_list,provider_lst)
        
        elif res_intent=="calls_cnt_ans_bu":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_cnt_ans_BU(dur_list,provider_lst)

        elif res_intent=="calls_cnt_ans":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_cnt_ans(dur_list,provider_lst)

        elif res_intent=="calls_cnt_trnsfr_lob":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_cnt_trnsfr_lob(dur_list,provider_lst)

        elif res_intent=="calls_cnt_trnsfr_prod_type":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_cnt_trnsfr_prod_type(dur_list,provider_lst)

        elif res_intent=="calls_cnt_trnsfr_type":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_cnt_trnsfr_type(dur_list,provider_lst)

        elif res_intent=="calls_cnt_trnsfr_lang":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_cnt_trnsfr_lang(dur_list,provider_lst)
        
        elif res_intent=="calls_cnt_trnsfr_bu":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_cnt_trnsfr_BU(dur_list,provider_lst)

        elif res_intent=="calls_cnt_trnsfr":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_cnt_trnsfr(dur_list,provider_lst)

        elif res_intent=="calls_cnt_lob":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_cnt_lob(dur_list,provider_lst)

        elif res_intent=="calls_cnt_prod_type":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_cnt_prod_type(dur_list,provider_lst)

        elif res_intent=="calls_cnt_type":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_cnt_type(dur_list,provider_lst)

        elif res_intent=="calls_cnt_lang":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_cnt_lang(dur_list,provider_lst)
        
        elif res_intent=="calls_cnt_bu":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_cnt_BU(dur_list,provider_lst)

        elif res_intent=="calls_cnt":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_cnt(dur_list,provider_lst)

        elif res_intent=="calls_tat_hold_lob":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_tat_hold_lob(dur_list,provider_lst)

        elif res_intent=="calls_tat_hold_prod_type":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_tat_hold_prod_type(dur_list,provider_lst)

        elif res_intent=="calls_tat_hold_type":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_tat_hold_type(dur_list,provider_lst)

        elif res_intent=="calls_tat_hold_trnsfr":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_tat_hold_trnsfr(dur_list,provider_lst)

        elif res_intent=="calls_tat_hold_ans":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_tat_hold_ans(dur_list,provider_lst)

        elif res_intent=="calls_tat_hold_lang":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_tat_hold_lang(dur_list,provider_lst)
        
        elif res_intent=="calls_tat_hold_bu":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_tat_hold_BU(dur_list,provider_lst)

        elif res_intent=="calls_tat_hold":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_tat_hold(dur_list,provider_lst)

        elif res_intent=="calls_tat_ring_lob":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_tat_ring_lob(dur_list,provider_lst)

        elif res_intent=="calls_tat_ring_prod_type":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_tat_ring_prod_type(dur_list,provider_lst)

        elif res_intent=="calls_tat_ring_type":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_tat_ring_type(dur_list,provider_lst)

        elif res_intent=="calls_tat_ring_trnsfr":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_tat_ring_trnsfr(dur_list,provider_lst)

        elif res_intent=="calls_tat_ring_ans":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_tat_ring_ans(dur_list,provider_lst)

        elif res_intent=="calls_tat_ring_lang":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_tat_ring_lang(dur_list,provider_lst)
        
        elif res_intent=="calls_tat_ring_bu":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_tat_ring_BU(dur_list,provider_lst)

        elif res_intent=="calls_tat_ring":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_tat_ring(dur_list,provider_lst)

        elif res_intent=="calls_tat_talk_lob":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_tat_talk_lob(dur_list,provider_lst)

        elif res_intent=="calls_tat_talk_prod_type":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_tat_talk_prod_type(dur_list,provider_lst)

        elif res_intent=="calls_tat_talk_type":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_tat_talk_type(dur_list,provider_lst)

        elif res_intent=="calls_tat_talk_trnsfr":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_tat_talk_trnsfr(dur_list,provider_lst)

        elif res_intent=="calls_tat_talk_ans":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_tat_talk_ans(dur_list,provider_lst)

        elif res_intent=="calls_tat_talk_lang":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_tat_talk_lang(dur_list,provider_lst)
        
        elif res_intent=="calls_tat_talk_bu":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_tat_talk_BU(dur_list,provider_lst)

        elif res_intent=="calls_tat_talk":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_tat_talk(dur_list,provider_lst)

        elif res_intent=="calls_tat_lob":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_tat_lob(dur_list,provider_lst)

        elif res_intent=="calls_tat_prod_type":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_tat_prod_type(dur_list,provider_lst)

        elif res_intent=="calls_tat_type":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_tat_type(dur_list,provider_lst)

        elif res_intent=="calls_tat_trnsfr":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_tat_trnsfr(dur_list,provider_lst)

        elif res_intent=="calls_tat_ans":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_tat_ans(dur_list,provider_lst)

        elif res_intent=="calls_tat_lang":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_tat_lang(dur_list,provider_lst)
        
        elif res_intent=="calls_tat_bu":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_tat_BU(dur_list,provider_lst)

        elif res_intent=="calls_tat":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_tat(dur_list,provider_lst)

        elif res_intent=="calls_trnsfr_rt_lob":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_trnsfr_rt_lob(dur_list,provider_lst)

        elif res_intent=="calls_trnsfr_rt_prod_type":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_trnsfr_rt_prod_type(dur_list,provider_lst)

        elif res_intent=="calls_trnsfr_rt_type":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_trnsfr_rt_type(dur_list,provider_lst)

        elif res_intent=="calls_trnsfr_rt_lang":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_trnsfr_rt_lang(dur_list,provider_lst)
        
        elif res_intent=="calls_trnsfr_rt_bu":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_trnsfr_rt_BU(dur_list,provider_lst)

        elif res_intent=="calls_trnsfr_rt":
            dur_list=list()
            if context_from.upper()=="default".upper():
                dur_list.append(context_days)
                dur_list.append(context_months)
                dur_list.append(context_years)
                dur_list.append("junk")
            else:
                dur_list.append(context_from)
                dur_list.append(context_to)
                dur_list.append("junk")
            ans=get_calls_trnsfr_rt(dur_list,provider_lst)
        
        else:
            ans="I am not prepare for your question as of now"

        res_intent=res_intent_temp

        print("final intent "+res_intent)
        print("context_context final "+context_context)
        print("final user message value "+user_message)
           
        
        
        
        print("answer="+str(ans))
        ## suugestions list to be derived##       
        # ans=ans.split('!')[0] 
        ###### context history push call #######   
        # print(context_uid,context_sessid,context_type_of_req,context_call_r_calls,context_context,context_call_id,context_from,context_to,context_days,context_months,context_years)     
        push_context_hist_calls(context_uid,context_sessid,context_type_of_req,context_call_r_calls.upper(),context_context,context_call_id,context_from,context_to,context_days,context_months,context_years)
        ###### context history push call #######
        #####conv_history parameters and function call ########
        conv_uid=userid_ang
        conv_sesid=sess_id_ang
        conv_question=res_text
        conv_answer=ans
        conv_intent=res_intent
        conv_int_conf=res_intent_confidence
        conv_like_r_dislike="default"
        conv_obj_id=calls_push_conv_hist(conv_uid,conv_sesid,conv_question,conv_answer,conv_intent,conv_int_conf,conv_like_r_dislike)
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
        # for si in range(0,len(sugg_list)):
        #     if sugg_list[si].lower()=="Date of service".lower():
        #         sugg_list[si]="What is the date of service for the claim?"
        #     elif sugg_list[si].lower()=="Receipt Date".lower():
        #         sugg_list[si]="When was the claim received?"
        #     elif sugg_list[si].lower()=="Paid Date".lower():
        #         sugg_list[si]="When was the claim paid?"    
        #     elif sugg_list[si].lower()=="Claim Type".lower():
        #         sugg_list[si]="What is the claim type?"
        #     elif sugg_list[si].lower()=="Billed Amount".lower():
        #         sugg_list[si]="How much amount got billed for the claim?"
        #     elif sugg_list[si].lower()=="TAT".lower():
        #         sugg_list[si]="What is the turnaround time for the claim?"
        #     elif sugg_list[si].lower()=="Submission Mode".lower():
        #         sugg_list[si]="What is the mode of submission for the claim?"
        #     elif sugg_list[si].lower()=="Adjusted Amount".lower():
        #         sugg_list[si]="What amount was adjusted for the claim?"
        #     elif sugg_list[si].lower()=="Paid Amount".lower():
        #         sugg_list[si]="What amount got paid for the claim?"
        #     elif sugg_list[si].lower()=="Status".lower():
        #         sugg_list[si]="What is the status of claim?"
        #     elif sugg_list[si].lower()=="Adjustment Reason".lower():
        #         sugg_list[si]="What are the reasons for adjustments in the claim?"
        #     elif sugg_list[si].lower()=="Denial Reason".lower():
        #         sugg_list[si]="What are the reasons for denials in claim?"
        #     elif sugg_list[si].lower()=="Allowed Amount".lower():
        #         sugg_list[si]="How much amount is Allowed for the claim?"
        #     elif sugg_list[si].lower()=="Interest Amount".lower():
        #         sugg_list[si]="What is the interest amount paid for the claim?"
        #     elif sugg_list[si].lower()=="Diagnosis Codes".lower():
        #         sugg_list[si]="What are the diagnosis codes associated with claim?"
        #     elif sugg_list[si].lower()=="NPI".lower():
        #         sugg_list[si]="What is the National Provider Identifier of claim provider?"
        #     elif sugg_list[si].lower()=="Par Status".lower():
        #         sugg_list[si]="What is the PAR status of the claim?"
        #     elif sugg_list[si].lower()=="Revise and Resubmit".lower():
        #         sugg_list[si]="How to revise and resubmit the claim?"
        #     elif sugg_list[si].lower()=="LOB".lower():
        #         sugg_list[si]="What line of business does this claim belong to?"
        #     elif sugg_list[si].lower()=="Line Items".lower():
        #         sugg_list[si]="How many line items are present in the claim?"

        return jsonify({"response":conv_answer,"object_id":conv_obj_id,"Suggestions":sugg_list})
    except Exception as e:
    # else:
        print(e) 
        return jsonify({"response":"Sorry I do not have an answer for that. You may reach out to us through call or email for assistance."})   


app.config["DEBUG"] = True
if __name__ == "__main__":
    app.run(host='apsrp03693',port=5090,debug=True)
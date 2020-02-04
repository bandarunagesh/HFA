from flask import Flask
from flask import render_template,jsonify,request
import requests
from models import *
from pblm_solving_files.knowledge_rev import *
from pblm_solving_files.duckling_wrapper import *
import random
import urllib3



app = Flask(__name__)
app.secret_key = '12345'

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
        #s2=str(str(parsed.query).split('&')[1].split('=')[1].replace('+',' ')) # second query
        while True:
            a=s1.find("%")
            if a > -1:
                ss=s1[a]+s1[a+1]+s1[a+2]
                s1=s1.replace(ss," ")
            else:
                break
        s1=s1.replace('  ',' ').replace('  ',' ').strip(' ').lower()
        print(s1)
        user_message = s1
        um1=user_message

        #days,months,years extracted to be returned
        dmy_lst=time_extract(um1)
        dte_text_lst=list()
        if len(dmy_lst)==3:
            res_from=str(dmy_lst[0].split(' ')[0]).split('-')[1]+"/"+str(dmy_lst[0].split(' ')[0]).split('-')[2]+"/"+str(dmy_lst[0].split(' ')[0]).split('-')[0]
            res_to=str(dmy_lst[1].split(' ')[0]).split('-')[1]+"/"+str(dmy_lst[1].split(' ')[0]).split('-')[2]+"/"+str(dmy_lst[1].split(' ')[0]).split('-')[0]
            dte_text_lst=dmy_lst[2]
            res_days=""
            res_months=""
            res_years=""
        elif len(dmy_lst)==4:
            res_from=""
            res_to=""
            res_days=str(dmy_lst[0])
            res_months=str(dmy_lst[1])
            res_years=str(dmy_lst[2])
            dte_text_lst=dmy_lst[3]
        else:
            res_from=""
            res_to=""
            res_days=""
            res_months=""
            res_years=""
        for dte_i in dte_text_lst:
            user_message=user_message.replace(" "+dte_i+" "," ")
        #days,months,years extracted to be returned

        user_message=corrected_ip_string_1(user_message)
        user_message=corrected_ip_string_1(user_message.replace('-',' '))
        user_message=str(user_message).strip(' ').lower()           
        response = requests.get("http://apsrp03693:5000/parse",params={"q":user_message})        
        response = response.json()
        # response["text"]=um1

        # response text to be returned
        res_text=um1
        # response text to be returned

        # intent to be returned
        intent = response.get("intent")
        res_intent=intent['name']
        # intent to be returned
        # entities=response.get("entities")                
        if res_intent in ["status","time","action_reason","resubmit","adj_amount"]:
            # claim number and entities to be returned            
            claim_num=0        
            if claim_num==0:
                claim_num=claim_num_extract(um1)
            res_claim_num=claim_num
            # claim number and entities to be returned
            if res_intent in ["action_reason"]:
                if "denied" in user_message:
                    res_intent="action_reason-denial_reason"
                elif "adjust" in user_message:
                    res_intent="action_reason-adjusted_reason"
            if res_intent in ["adj_amount"]:
                if " paid " in user_message:
                    res_intent="adj_amount-paid"
                
        else:
            res_claim_num=""
        return jsonify({"response":res_text,"intent":res_intent,"claim_number":res_claim_num,"from":res_from,"to":res_to,"days":res_days,"months":res_months,"years":res_years})
    except Exception as e:
        print(e)
        return jsonify({"response":"Sorry I am not trained to do that yet..."})   


app.config["DEBUG"] = True
if __name__ == "__main__":
    app.run(host='apsrp03693',port=5050,debug=True)
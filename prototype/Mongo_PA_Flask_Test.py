from flask import Flask
from flask import render_template,jsonify,request
import requests
import random
import urllib3
from flask_cors import CORS
import json
from PA_mongoAPI import *
from knowledge_rev import *

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
        requestType = str(parsed.query).split('&')[1].split('=')[1]
        user_question = str(parsed.query).split('&')[0].split('=')[1]
        if requestType == 'prior_auth':
            response = requests.get("http://apsrp03693:8066/parse",params={"q":user_question})
            response = response.json()
            intent = response.get('intent')
            entities = response.get('entities')
            intent_name = str(intent['name'])
            if intent_name.lower() == 'greet':
                answer = greeting()
            elif intent_name.lower() == 'goodbye':
                answer = goodbye()
            elif intent_name.lower() == 'affirm':
                answer = affirm()
            elif intent_name.lower() == 'status_prior_auth':
                hscId = claim_num_extract(user_question)
                answer = getStatusPA(hscId)
            elif intent_name.lower() == "pa_request_date":
                hscId = claim_num_extract(user_question)
                answer = getRequestSubmittedDate(hscId)
            elif intent_name.lower() == "pa_decision":
                hscId = claim_num_extract(user_question)
                answer = getDecisionDate(hscId)
            elif intent_name.lower() == "pa_service_type":
                hscId = claim_num_extract(user_question)
                answer = getServiceType(hscId)
            elif intent_name.lower() == "pa_service_cat":
                hscId = claim_num_extract(user_question)
                answer = getServiceCategory(hscId)
            elif intent_name.lower() == "pa_service_setting":
                hscId = claim_num_extract(user_question)
                answer = getServiceSettingType(hscId)
            elif intent_name.lower() == "pa_lob":
                hscId = claim_num_extract(user_question)
                answer = getLOBPA(hscId)
            elif intent_name.lower() == "pa_taxid":
                hscId = claim_num_extract(user_question)
                answer = getTaxID(hscId)
            elif intent_name.lower() == 'pa_line_items':
                hscId = claim_num_extract(user_question)
                answer = getLineItems(hscId)
            elif intent_name.lower() == 'pa_tat':
                hscId = claim_num_extract(user_question)
                answer = getTATPA(hscId)
            elif intent_name.lower() == 'pa_denial_rsns':
                hscId = claim_num_extract(user_question)
                answer = getReasonsDenials(hscId)
            else:
                answer = "Sorry, can not help at this time"
        return jsonify({"status":"success","response":answer})
    except Exception as e:
        print(e)
        return jsonify({"status":"success","response":"Sorry I am not trained to do that yet..."})
        
            
app.config["DEBUG"] = True
if __name__ == "__main__":
    app.run(host='apsrp03693',port=6022,debug=True)
            
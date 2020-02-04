##dict of response for each type of intent
from autocorrect import spell

def call_id_present(s1):
    try:
        s1_res=s1.split(' ')
        npi_ind=0
        
        for s in s1_res:
            if str(str(s)).lower()=="id":
                npi_ind=1
            
        if npi_ind==1:
            return True        
        else:
            return False
    except Exception as e:
        print("error in presence of call or calls function"+str(e))

def call_id_extract(s1):
    print("in call id extrct function")
    call_id=0    
    if call_id==0:
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
                call_id=s2[i]                
                return call_id    
    return call_id

def corrected_ip_string_call(s1,context_call_r_calls):
    print("corrected_ip_string")
    try:
        if context_call_r_calls.upper()=="CALL":
            s1=s1.replace('  ',' ').replace('  ',' ').strip(' ')
            s2=s1.split(' ')
            s3=""
            for i in range(0,len(s2)):
                s1_i_orig=s2[i].lower()
                s1_i_crcted=spell(s2[i].lower()).lower()
                if s1_i_orig in ["tat"]:
                    s3=s3+" "+"time".lower()+" "
                elif s1_i_crcted in ["year","month"]:
                    s3=s3+" "
                elif s1_i_orig in ["tin"]:
                    s3=s3+" "+"tax id".lower()+" "
                elif s1_i_orig in ["dos"]:
                    s3=s3+" "+"date of service".lower()+" "
                elif s1_i_crcted in ["participant","participate","participating"]:
                    s3=s3+" "+"par".lower()+" "
                elif s1_i_orig in ["non-participant","non-participate","non-participating"]:
                    s3=s3+" "+"non par".lower()+" "
                elif s1_i_crcted in ["nonparticipant","nonparticipate","nonparticipating"]:
                    s3=s3+" "+"non par".lower()+" "
                elif s1_i_orig in ["network","n/w"]:
                    s3=s3+" "+"par".lower()+" "
                elif s1_i_crcted in ["network","n/w"]:
                    s3=s3+" "+"par".lower()+" "
                elif s1_i_crcted in ["prov","provide","provider","provided","providing","provides","providers"]:
                    s3=s3+" "+"provider".lower()+" "
                elif s1_i_orig in ["advoc","advocate","advocates","advocating"]:
                    s3=s3+" "+"advocate".lower()+" "
                elif s1_i_crcted in ["advoc","advocate","advocates","advocating"]:
                    s3=s3+" "+"advocate".lower()+" "
                elif s1_i_orig in ["national","nation","ntnl"]:
                    s3=s3+" "+"national".lower()+" "   
                elif s1_i_crcted in ["national","nation","ntnl"]:
                    s3=s3+" "+"national".lower()+" "             
                elif s1_i_crcted in ["calls"]:
                    s3=s3+" "+"call".lower()+" "
                elif s1_i_orig in ["call","lob","non","par","npi","non-par"]:
                    s3=s3+" "+str(s2[i]).lower()+" "
                elif s1_i_crcted in ["details","detail","condition","position","place","situation","stage","about","status"]:
                    s3=s3+" "+"status".lower()+" "
                elif s1_i_crcted in ["deny","denied","denial","denials","denying","denies","decline","declines","declined","declination","declining","declinations","reject","rejects","rejected","rejecting","rejection","rejections","refuse","refused","refusals","refusal","refusing","refuses","repudiate","repudiates","repudiated","repudiation","repudiations","repudiating","rebuff","rebuffs","rebuffed","rebuffing","dismiss","dismissed","dismisses","dismissing","veto","vetoed","vetoing","vetoes","refute","refutes","refuted","refuting","refutation","rebuff","rebuffs","rebuffed","rebuffing"]:
                    s3=s3+" "+"denied".lower()+" "
                elif s1_i_crcted in ['partially','partial','incomplete','incompletely','partials','uncompleted']:
                    s3=s3+" "+"partial".lower()+" "
                elif s1_i_crcted in ['adjust','adjusting','adjusted','adjustment','adjustments','adjusts']:
                    s3=s3+" "+"adjusted".lower()+" "
                elif s1_i_crcted in ['completely','complete','totally','total','completes','totals']:
                    s3=s3+" "+"complete".lower()+" "
                elif s1_i_crcted in ['resubmit','resubmits','resubmitted','resubmitting','resubmission']:
                    s3=s3+" "+"resubmit".lower()+" "
                elif s1_i_crcted in ['submit','submits','submitted','submitting','submission']:
                    s3=s3+" "+"submitted".lower()+" "
                elif s1_i_crcted in ['justification','explanation','rationalization','vindication','clarification','simplification','description','elucidation','exposition','explication','delineation']:
                    # s3=s3+" "+"justification".lower()+" "
                    s3=s3+" "+"justified".lower()+" "
                elif s1_i_crcted in ['justified','explained','rationalized','vindicated','clarified','simplified','described','elucidated','exposited','explicated','delineated']:
                    s3=s3+" "+"justified".lower()+" "
                elif s1_i_orig in ['amount','money','cash','buck','bucks','capital','value']:
                    s3=s3+" "+"amount".lower()+" "
                elif s1_i_crcted in ['amount','money','cash','buck','bucks','capital','value']:
                    s3=s3+" "+"amount".lower()+" "
                elif s1_i_crcted in ['reason','cause','root','basis']:
                    s3=s3+" "+"reason".lower()+" "
                elif s1_i_crcted in ['reasons','causes']:
                    s3=s3+" "+"reason".lower()+" "
                elif s1_i_crcted in ['paid','pay','pays','paying','payment','compensating','compensated','compensates','compensate','indemnifying','indemnifies','indemnify','indemnified','refund','refunds','refunded','refunding','remunerate','remunerated','remunerates','remunerating','recompensed','recompense','recompensing','recompenses','reimburse','reimburses','reimbursing','reimbursed','repaid','repay','repays','repaying','repayment']:
                    s3=s3+" "+"paid".lower()+" "
                elif s1_i_crcted in ['period','duration','span','term','days','long','time','times']:
                    s3=s3+" "+"time".lower()+" "
                elif s1_i_crcted in ['process','processing','processed','processes']:
                    s3=s3+" "+"process".lower()+" "
                elif s1_i_crcted in ['bill','bills','billed','billing']:
                    s3=s3+" "+"billed".lower()+" "
                elif s1_i_crcted in ['allow','allows','allowed','allowing']:
                    s3=s3+" "+"allowed".lower()+" "
                elif s1_i_crcted in ['interest','interests','interested','interesting']:
                    s3=s3+" "+"interest".lower()+" "
                elif s1_i_crcted in ['diagnose','diagnosis','diag']:
                    s3=s3+" "+"diagnosis".lower()+" "
                elif s1_i_crcted in ['code','codes','coded','coding']:
                    s3=s3+" "+"codes".lower()+" "
                elif s1_i_crcted in ['line','lines','lined','lining']:
                    s3=s3+" "+"line".lower()+" "
                elif s1_i_crcted in ['item','items']:
                    s3=s3+" "+"items".lower()+" "
                elif s1_i_orig in ['service','services','serviced','servicing',"svc","svcs","svcing"]:
                    s3=s3+" "+"service".lower()+" "
                elif s1_i_crcted in ['service','services','serviced','servicing',"svc","svcs","svcing"]:
                    s3=s3+" "+"service".lower()+" "
                elif s1_i_crcted in ['tax','taxation','taxes','taxing','taxed']:
                    s3=s3+" "+"tax".lower()+" "
                elif s1_i_crcted in ['action','actions']:
                    s3=s3+" "+"action".lower()+" "
                elif s1_i_crcted in ["adjudicated","adjudicate","adjudication","adjudicates","adjudicating"]:
                    s3=s3+" "+"adjudicated".lower()+" "
                elif s1_i_crcted in ['type','types','category','categories','kind','kinds','sort','breed','breeds','form','forms','group','groups','variety','varieties','classify','classification','classifying','classified']:
                    s3=s3+" "+"type".lower()+" "
                elif s1_i_crcted in ['mode','approach','form','mechanism','technique','course','modes','approaches','forms','mechanisms','techniques','courses']:
                    s3=s3+" "+"mode".lower()+" "
                elif s1_i_crcted in ['top','main','major','prime','vital','primary','preeminent','crucial','dominant','chief','head','first','lead']:
                    s3=s3+" "+"top".lower()+" "
                elif s1_i_crcted in ['count','number','sum','whole','reckon','figure','enumerate','add','volume']:
                    s3=s3+" "+"count".lower()+" "
                elif s1_i_crcted in ['receipt','receive','received','receiving','receives','receiving','collect','collects','collected','collecting','gather','gathers','gathering','gathered']:
                    s3=s3+" "+"received".lower()+" "
                elif s1_i_crcted in ['hgh','high','higher','highest']:
                    s3=s3+" "+"high".lower()+" "
                elif s1_i_orig in ['dlr','dllr','dollar','dollars','dlrs','dllrs']:
                    s3=s3+" "+"dollar".lower()+" "
                elif s1_i_crcted in ['dlr','dllr','dollar','dollars','dlrs','dllrs']:
                    s3=s3+" "+"dollar".lower()+" "
                elif s1_i_crcted in ['id','identifier','number',"identification"]:
                    s3=s3+" "+"id".lower()+" "
                elif str(s2[i]).lower() in ['icd-10','icd']:
                    s3=s3+" "+"diag codes".lower()+" "
                elif str(s2[i]).lower() in ['rcvd']:
                    s3=s3+" "+"received".lower()+" "
                elif str(s2[i]).lower() in ['pa']:
                    s3=s3+" "+"prior auth".lower()+" "
                elif s1_i_crcted in ['claim','claims']:
                    s3=s3+" "+"claims"+" "
                elif s1_i_crcted in ['eligible','eligibility','member']:
                    s3=s3+" "+"eligibility"+" "
                elif s1_i_crcted in ['auth','auths','authorization']:
                    s3=s3+" "+"auth"+" "
                elif s1_i_crcted in ['benefits','benefit']:
                    s3=s3+" "+"benefits"+" "
                elif str(s2[i]).lower() in ['ben']:
                    s3=s3+" "+"benefits"+" "
                elif s1_i_crcted in ['appeal','appeals']:
                    s3=s3+" "+"appeal"+" "
                elif str(s2[i]).lower() in ['talktime']:
                    s3=s3+" "+"talk time"+" "
                elif str(s2[i]).lower() in ['ringtime']:
                    s3=s3+" "+"ring time"+" "
                elif str(s2[i]).lower() in ['holdtime']:
                    s3=s3+" "+"hold time"+" "
                elif s1_i_crcted in ['chat',' colloquy',' communication',' communion',' confabulation',' conference',' conversation',' converse',' dialogue',' discourse',' intercourse',' parley','chats','chatting','chatter','colloquies','colloquial','colloquist','communicate','communicates','communications','communicator','communicated','confabulate','confabulates','confabulating','confabulated','conferences','conferencing','conferenced','converse','converses','conversed','coversation','conversations','dialogue','dialogues','dialoguing','dialoged','discourses','discoursed','discoursing','intercourse','intercourses','intercoursed','intercoursing','parleys','parleyed','parleying','speak','spoke','speaken','speaking','speaks','talk','talking','talked','talks']:
                    s3=s3+" "+"talk"+" "
                elif s1_i_crcted in ['buzz','bell','tinkle','ring','rings','ringing','ringed','buzz','buzzes','buzzing','buzzed','bell','bells','belling','belled','tinkle','tinkles','tinkling','tinkled']:
                    s3=s3+" "+"ring"+" "
                elif s1_i_crcted in ['buzz','bell','tinkle','ring','rings','ringing','ringed','buzz','buzzes','buzzing','buzzed','bell','bells','belling','belled','tinkle','tinkles','tinkling','tinkled']:
                    s3=s3+" "+"ring"+" "
                elif s1_i_crcted in ['defer','delay','adjourn','shelve','suspend','hold','holds','held','holding','defer','defers','deferring','deferred','delays','delayed','delays','delaying','adjourn','adjourns','adjourned','adjourning','shelve','shelves','shelving','shelved','suspend','suspends','suspending','suspended']:
                    s3=s3+" "+"hold"+" "
                elif s1_i_crcted in ['answer','reply','respond','rejoin','retort','answer','answers','answered','answering','reply','replies','replied','replying','respond','responds','responded','responding','rejoin','rejoins','rejoining','rejoined','retort','retorts','retorted','retorting']:
                    s3=s3+" "+"answered"+" "
                elif s1_i_crcted in ['transfer','transfers','transferring','transferred','move','moves','moved','moving','shift','shifts','shifted','shifting']:
                    s3=s3+" "+"transferred"+" "
                elif s1_i_crcted in ['unanswer','unanswers','unanswered']:
                    s3=s3+" "+"unanswered"+" "
                elif s1_i_crcted in ['language','languages','dialect','dialects','jargon','jargons','prose','proses','prosing','prosed','terminology','terminologies']:
                    s3=s3+" "+"language"+" "
                elif s1_i_crcted in ['product','products']:
                    s3=s3+" "+"product"+" "
                elif str(s2[i]).lower() in ['prod']:
                    s3=s3+" "+"product"+" "
                elif str(s2[i]).lower() in ['lang']:
                    s3=s3+" "+"language"+" "
                elif s1_i_crcted in ['rate','rates']:
                    s3=s3+" "+"rate"+" "
                elif s1_i_crcted in ['turn','around','time','high','dollar']:
                    s3=s3+" "+s1_i_crcted+" "
                else:
                    s3=s3+" "+str(s2[i]).lower()+" "
            
            if "business" in s3.lower() and "unit" in s3.lower():
                s3=s3.replace('business','bu').replace('unit',' ').strip(' ')
                s3=s3.replace('  ',' ').replace('  ',' ')
            if "product" in s3.lower() and "type" not in s3.lower():
                s3=s3.replace('product','product type').strip(' ')
                s3=s3.replace('  ',' ').replace('  ',' ')
            s3=s3.replace('  ',' ').replace('  ',' ').strip(' ').replace('turn','').replace('around','').replace('non par','non-par')
            ent_list=['diagnosis','codes','line','items','tax','id','lob','NPI','par','non-par','type','facility','professional']
            cntxt_replace_ind=0
            for s in s3.split(' '):
                if s in ent_list:
                    cntxt_replace_ind=1
            if cntxt_replace_ind==1:
                s3=s3.replace('denied','').replace('partial','').strip(' ').replace('adjusted','').replace('high','').replace('dollar','').replace('received','').replace('submitted','').replace('adjudicated','')
                s3=s3.replace('  ',' ').replace('  ',' ')
            if "line" in s3.lower() and "business" in s3.lower():
                s3=s3.replace('line','').replace('business','lob').strip(' ')
                s3=s3.replace('  ',' ').replace('  ',' ')
            if "national" in s3.lower() and "provider" in s3.lower() and "id" in s3.lower():
                s3=s3.replace('national','').replace('provider','npi').strip(' ').replace('id',' ')
                s3=s3.replace('  ',' ').replace('  ',' ')
            if "taxpayer" in s3.lower() and "identification" in s3.lower() and "number" in s3.lower():
                s3=s3.replace('taxpayer','').replace('identification','tin').strip(' ').replace('number',' ')
                s3=s3.replace('  ',' ').replace('  ',' ')
            if "tax id" in s3.lower():
                s3=s3.replace("tax id","tin")
            return s3
        elif context_call_r_calls.upper()=="CALLS":
            s1=s1.replace('  ',' ').replace('  ',' ').strip(' ')
            s2=s1.split(' ')
            s3=""
            for i in range(0,len(s2)):
                s1_i_orig=s2[i].lower()
                s1_i_crcted=spell(s2[i].lower()).lower()
                if s1_i_orig in ["tat"]:
                    s3=s3+" "+"time".lower()+" "
                elif s1_i_crcted in ["year","month"]:
                    s3=s3+" "
                elif s1_i_orig in ["tin"]:
                    s3=s3+" "+"tax id".lower()+" "
                elif s1_i_orig in ["dos"]:
                    s3=s3+" "+"date of service".lower()+" "
                elif s1_i_crcted in ['chat',' colloquy',' communication',' communion',' confabulation',' conference',' conversation',' converse',' dialogue',' discourse',' intercourse',' parley','chats','chatting','chatter','colloquies','colloquial','colloquist','communicate','communicates','communications','communicator','communicated','confabulate','confabulates','confabulating','confabulated','conferences','conferencing','conferenced','converse','converses','conversed','coversation','conversations','dialogue','dialogues','dialoguing','dialoged','discourses','discoursed','discoursing','intercourse','intercourses','intercoursed','intercoursing','parleys','parleyed','parleying','speak','spoke','speaken','speaking','speaks','talk','talking','talked','talks']:
                    s3=s3+" "+"talk"+" "
                elif s1_i_crcted in ['buzz','bell','tinkle','ring','rings','ringing','ringed','buzz','buzzes','buzzing','buzzed','bell','bells','belling','belled','tinkle','tinkles','tinkling','tinkled']:
                    s3=s3+" "+"ring"+" "
                elif s1_i_crcted in ['defer','delay','adjourn','shelve','suspend','hold','holds','held','holding','defer','defers','deferring','deferred','delays','delayed','delays','delaying','adjourn','adjourns','adjourned','adjourning','shelve','shelves','shelving','shelved','suspend','suspends','suspending','suspended']:
                    s3=s3+" "+"hold"+" "
                elif s1_i_crcted in ['answer','reply','respond','rejoin','retort','answer','answers','answered','answering','reply','replies','replied','replying','respond','responds','responded','responding','rejoin','rejoins','rejoining','rejoined','retort','retorts','retorted','retorting']:
                    s3=s3+" "+"answered"+" "
                elif s1_i_crcted in ['transfer','transfers','transferring','transferred','move','moves','moved','moving','shift','shifts','shifted','shifting']:
                    s3=s3+" "+"transferred"+" "
                elif s1_i_crcted in ['unanswer','unanswers','unanswered']:
                    s3=s3+" "+"unanswered"+" "
                elif str(s2[i]).lower() in ['pa']:
                    s3=s3+" "+"prior auth".lower()+" "
                elif s1_i_crcted in ['claim','claims']:
                    s3=s3+" "+"claims"+" "
                elif s1_i_crcted in ['eligible','eligibility','member']:
                    s3=s3+" "+"eligibility"+" "
                elif s1_i_crcted in ['auth','auths','authorization']:
                    s3=s3+" "+"auth"+" "
                elif s1_i_crcted in ['benefits','benefit']:
                    s3=s3+" "+"benefits"+" "
                elif str(s2[i]).lower() in ['ben']:
                    s3=s3+" "+"benefits"+" "
                elif s1_i_crcted in ['appeal','appeals']:
                    s3=s3+" "+"appeal"+" "
                elif str(s2[i]).lower() in ['talktime']:
                    s3=s3+" "+"talk time"+" "
                elif str(s2[i]).lower() in ['ringtime']:
                    s3=s3+" "+"ring time"+" "
                elif str(s2[i]).lower() in ['holdtime']:
                    s3=s3+" "+"hold time"+" "
                elif s1_i_crcted in ['language','languages','dialect','dialects','jargon','jargons','prose','proses','prosing','prosed','terminology','terminologies']:
                    s3=s3+" "+"language"+" "
                elif s1_i_crcted in ['product','products']:
                    s3=s3+" "+"product"+" "
                elif str(s2[i]).lower() in ['prod']:
                    s3=s3+" "+"product"+" "
                elif str(s2[i]).lower() in ['lang']:
                    s3=s3+" "+"language"+" "
                elif s1_i_crcted in ['rate','rates']:
                    s3=s3+" "+"rate"+" "
                elif s1_i_crcted in ["participant","participate","participating"]:
                    s3=s3+" "+"par".lower()+" "
                elif s1_i_orig in ["non-participant","non-participate","non-participating"]:
                    s3=s3+" "+"non par".lower()+" "
                elif s1_i_crcted in ["nonparticipant","nonparticipate","nonparticipating"]:
                    s3=s3+" "+"non par".lower()+" "
                elif s1_i_orig in ["network","n/w"]:
                    s3=s3+" "+"par".lower()+" "
                elif s1_i_crcted in ["network","n/w"]:
                    s3=s3+" "+"par".lower()+" "
                elif s1_i_crcted in ["prov","provide","provider","provided","providing","provides","providers"]:
                    s3=s3+" "+"provider".lower()+" "
                elif s1_i_orig in ["advoc","advocate","advocates","advocating"]:
                    s3=s3+" "+"advocate".lower()+" "
                elif s1_i_crcted in ["advoc","advocate","advocates","advocating"]:
                    s3=s3+" "+"advocate".lower()+" "
                elif s1_i_orig in ["national","nation","ntnl"]:
                    s3=s3+" "+"national".lower()+" "   
                elif s1_i_crcted in ["national","nation","ntnl"]:
                    s3=s3+" "+"national".lower()+" "             
                elif s1_i_crcted in ["call"]:
                    s3=s3+" "+"calls".lower()+" "
                elif s1_i_orig in ["calls","lob","non","par","npi","non-par"]:
                    s3=s3+" "+str(s2[i]).lower()+" "
                elif s1_i_crcted in ["details","detail","condition","position","place","situation","stage","about","status"]:
                    s3=s3+" "+"status".lower()+" "
                elif s1_i_crcted in ["deny","denied","denial","denials","denying","denies","decline","declines","declined","declination","declining","declinations","reject","rejects","rejected","rejecting","rejection","rejections","refuse","refused","refusals","refusal","refusing","refuses","repudiate","repudiates","repudiated","repudiation","repudiations","repudiating","rebuff","rebuffs","rebuffed","rebuffing","dismiss","dismissed","dismisses","dismissing","veto","vetoed","vetoing","vetoes","refute","refutes","refuted","refuting","refutation","rebuff","rebuffs","rebuffed","rebuffing"]:
                    s3=s3+" "+"denied".lower()+" "
                elif s1_i_crcted in ['partially','partial','incomplete','incompletely','partials','uncompleted']:
                    s3=s3+" "+"partial".lower()+" "
                elif s1_i_crcted in ['adjust','adjusting','adjusted','adjustment','adjustments','adjusts']:
                    s3=s3+" "+"adjusted".lower()+" "
                elif s1_i_crcted in ['completely','complete','totally','total','completes','totals']:
                    s3=s3+" "+"complete".lower()+" "
                elif s1_i_crcted in ['resubmit','resubmits','resubmitted','resubmitting','resubmission']:
                    s3=s3+" "+"resubmit".lower()+" "
                elif s1_i_crcted in ['submit','submits','submitted','submitting','submission']:
                    s3=s3+" "+"submitted".lower()+" "
                elif s1_i_crcted in ['justification','explanation','rationalization','vindication','clarification','simplification','description','elucidation','exposition','explication','delineation']:
                    # s3=s3+" "+"justification".lower()+" "
                    s3=s3+" "+"justified".lower()+" "
                elif s1_i_crcted in ['justified','explained','rationalized','vindicated','clarified','simplified','described','elucidated','exposited','explicated','delineated']:
                    s3=s3+" "+"justified".lower()+" "
                elif s1_i_orig in ['amount','money','cash','buck','bucks','capital','value']:
                    s3=s3+" "+"amount".lower()+" "
                elif s1_i_crcted in ['amount','money','cash','buck','bucks','capital','value']:
                    s3=s3+" "+"amount".lower()+" "
                elif s1_i_crcted in ['reason','cause','root','basis']:
                    s3=s3+" "+"reasons".lower()+" "
                elif s1_i_crcted in ['reasons','causes']:
                    s3=s3+" "+"reasons".lower()+" "
                elif s1_i_crcted in ['paid','pay','pays','paying','payment','compensating','compensated','compensates','compensate','indemnifying','indemnifies','indemnify','indemnified','refund','refunds','refunded','refunding','remunerate','remunerated','remunerates','remunerating','recompensed','recompense','recompensing','recompenses','reimburse','reimburses','reimbursing','reimbursed','repaid','repay','repays','repaying','repayment']:
                    s3=s3+" "+"paid".lower()+" "
                elif s1_i_crcted in ['period','duration','span','term','days','long','time','times']:
                    s3=s3+" "+"time".lower()+" "
                elif s1_i_crcted in ['process','processing','processed','processes']:
                    s3=s3+" "+"process".lower()+" "
                elif s1_i_crcted in ['bill','bills','billed','billing']:
                    s3=s3+" "+"billed".lower()+" "
                elif s1_i_crcted in ['allow','allows','allowed','allowing']:
                    s3=s3+" "+"allowed".lower()+" "
                elif s1_i_crcted in ['interest','interests','interested','interesting']:
                    s3=s3+" "+"interest".lower()+" "
                elif s1_i_crcted in ['diagnose','diagnosis','diag']:
                    s3=s3+" "+"diagnosis".lower()+" "
                elif s1_i_crcted in ['code','codes','coded','coding']:
                    s3=s3+" "+"codes".lower()+" "
                elif s1_i_crcted in ['line','lines','lined','lining']:
                    s3=s3+" "+"line".lower()+" "
                elif s1_i_crcted in ['item','items']:
                    s3=s3+" "+"items".lower()+" "
                elif s1_i_orig in ['service','services','serviced','servicing',"svc","svcs","svcing"]:
                    s3=s3+" "+"service".lower()+" "
                elif s1_i_crcted in ['service','services','serviced','servicing',"svc","svcs","svcing"]:
                    s3=s3+" "+"service".lower()+" "
                elif s1_i_crcted in ['tax','taxation','taxes','taxing','taxed']:
                    s3=s3+" "+"tax".lower()+" "
                elif s1_i_crcted in ['action','actions']:
                    s3=s3+" "+"action".lower()+" "
                elif s1_i_crcted in ["adjudicated","adjudicate","adjudication","adjudicates","adjudicating"]:
                    s3=s3+" "+"adjudicated".lower()+" "
                elif s1_i_crcted in ['type','types','category','categories','kind','kinds','sort','breed','breeds','form','forms','group','groups','variety','varieties','classify','classification','classifying','classified']:
                    s3=s3+" "+"type".lower()+" "
                elif s1_i_crcted in ['mode','approach','form','mechanism','technique','course','modes','approaches','forms','mechanisms','techniques','courses']:
                    s3=s3+" "+"mode".lower()+" "
                elif s1_i_crcted in ['top','main','major','prime','vital','primary','preeminent','crucial','dominant','chief','head','first','lead']:
                    s3=s3+" "+"top".lower()+" "
                elif s1_i_crcted in ['count','number','sum','whole','reckon','figure','enumerate','add','volume']:
                    s3=s3+" "+"count".lower()+" "
                elif s1_i_crcted in ['receipt','receive','received','receiving','receives','receiving','collect','collects','collected','collecting','gather','gathers','gathering','gathered']:
                    s3=s3+" "+"received".lower()+" "
                elif s1_i_crcted in ['hgh','high','higher','highest']:
                    s3=s3+" "+"high".lower()+" "
                elif s1_i_orig in ['dlr','dllr','dollar','dollars','dlrs','dllrs']:
                    s3=s3+" "+"dollar".lower()+" "
                elif s1_i_crcted in ['dlr','dllr','dollar','dollars','dlrs','dllrs']:
                    s3=s3+" "+"dollar".lower()+" "
                elif s1_i_crcted in ['id','identifier','number']:
                    s3=s3+" "+"id".lower()+" "
                elif str(s2[i]).lower() in ['icd-10','icd']:
                    s3=s3+" "+"diag codes".lower()+" "
                elif str(s2[i]).lower() in ['rcvd']:
                    s3=s3+" "+"received".lower()+" "
                elif s1_i_crcted in ['turn','around','time','high','dollar']:
                    s3=s3+" "+s1_i_crcted+" "
                else:
                    s3=s3+" "+str(s2[i]).lower()+" "

            if "business" in s3.lower() and "unit" in s3.lower():
                s3=s3.replace('business','bu').replace('unit',' ').strip(' ')
                s3=s3.replace('  ',' ').replace('  ',' ')
            if "product" in s3.lower() and "type" not in s3.lower():
                s3=s3.replace('product','product type').strip(' ')
                s3=s3.replace('  ',' ').replace('  ',' ')
            s3=s3.replace('  ',' ').replace('  ',' ').strip(' ').replace('turn','').replace('around','').replace('non par','non-par')
            ent_list=['diagnosis','codes','line','items','tax','id','lob','NPI','par','non-par','type','facility','professional']
            cntxt_replace_ind=0
            for s in s3.split(' '):
                if s in ent_list:
                    # cntxt_replace_ind=1
                    cntxt_replace_ind=0
            if cntxt_replace_ind==1:
                s3=s3.replace('denied','').replace('partial','').strip(' ').replace('adjusted','').replace('high','').replace('dollar','').replace('received','').replace('submitted','').replace('adjudicated','')
                s3=s3.replace('  ',' ').replace('  ',' ')
            if "line" in s3.lower() and "business" in s3.lower():
                s3=s3.replace('line','').replace('business','lob').strip(' ')
                s3=s3.replace('  ',' ').replace('  ',' ')
            if "national" in s3.lower() and "provider" in s3.lower() and "id" in s3.lower():
                s3=s3.replace('national','').replace('provider','npi').strip(' ').replace('id',' ')
                s3=s3.replace('  ',' ').replace('  ',' ')
            if "taxpayer" in s3.lower() and "identification" in s3.lower() and "number" in s3.lower():
                s3=s3.replace('taxpayer','').replace('identification','tin').strip(' ').replace('number',' ')
                s3=s3.replace('  ',' ').replace('  ',' ')  
            if "tax id" in s3.lower():
                s3=s3.replace("tax id","tin")
                
            return s3

    except:
        print("error in correcting string")


def call_r_calls_present(s1):
    try:
        s1_res=s1.split(' ')
        call_ind=0
        calls_ind=0
        for s in s1_res:
            if spell(str(s)).lower()=="call":
                call_ind=1
            if spell(str(s)).lower()=="calls":
                calls_ind=1
        if calls_ind==1:
            return "calls"
        elif call_ind==1:
            return "call"
        else:
            return "NOA"
    except Exception as e:
        print("error in presence of call or calls function"+str(e))

def calls_LOB_present(s1):
    try:
        s1_res=s1.split(' ')
        npi_ind=0
        
        for s in s1_res:
            if str(str(s)).lower()=="lob":
                npi_ind=1
            
        if npi_ind==1:
            return True        
        else:
            return False
    except Exception as e:
        print("error in presence of LOB_present function"+str(e))

def calls_BU_present(s1):
    try:
        s1_res=s1
        npi_ind=0
        
        for s in s1_res:
            if str(str(s)).lower()=="bu":
                npi_ind=1
            
        if npi_ind==1:
            return True        
        else:
            return False
    except Exception as e:
        print("error in presence of BU_present function"+str(e))

def calls_top_present(s1):
    try:
        s1_res=s1.split(' ')
        npi_ind=0
        
        for s in s1_res:
            if str(str(s)).lower()=="top":
                npi_ind=1
            
        if npi_ind==1:
            return True        
        else:
            return False
    except Exception as e:
        print("error in presence of top_present function"+str(e))



def correct_sentence_for_calls(s1):
    # context_flag=0
    # context_lst=['received','submitted','paid','adjusted','adjudicated','denied','partial denied']
    # for cl_i in context_lst:
    #     if cl_i in s1:
    #         context_flag=1
    # if context_flag==0:
    #     s1=s1+" received"
    s1=s1.replace(" value",' amount').replace("value ","amount ")
    s1=s1.replace(" calls type",' type').replace("calls type ","type ")
    
    if "time" in s1.lower():
        s1=s1.replace('count ','').replace(' count','')
        if "calls" not in s1:
            s1=s1.replace("time"," calls time ") 
        if 'received' not in s1:
            s1=s1.replace("calls"," received calls ") 
    elif "rate" in s1.lower():
        s1=s1.replace('count ','').replace(' count','')
        if "calls" not in s1:
            s1=s1.replace("rate"," calls rate ") 
        if 'received' not in s1:
            s1=s1.replace("calls"," received calls ") 
    else:
        if "count" not in s1:
            s1=s1+" count"
        if "calls" not in s1:
            s1=s1.replace("count"," calls count ") 
        if 'received' not in s1:
            s1=s1.replace("calls"," received calls ")
    return s1


# print(claim_num_extract("what is 12dfs2323"))
# print(corrected_ip_string_1("what is status"))
print(calls_BU_present("transferred calls bu rate for last 2 months"))
##dict of response for each type of intent
from autocorrect import spell

##########
claim_numbers_req=list()
##########

def claim_num_extract(s1):
    print("in claim number extrct function")
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
                claim_num=s2[i]
                claim_numbers_req.append(claim_num)
                return claim_num
    # claim_num=claim_numbers_req[len(claim_numbers_req)-1]
    return claim_num

def corrected_ip_string_1(s1,context_claim_r_claims):
    print("corrected_ip_string")
    try:
        if context_claim_r_claims.upper()=="CLAIM":
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
                elif s1_i_crcted in ["claims"]:
                    s3=s3+" "+"claim".lower()+" "
                elif s1_i_orig in ["claim","lob","non","par","npi","non-par"]:
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
                elif s1_i_crcted in ['amount','money','cash','buck','bucks','capital']:
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
                elif s1_i_crcted in ['count','number','sum','whole','reckon','figure','enumerate','add']:
                    s3=s3+" "+"count".lower()+" "
                elif s1_i_crcted in ['receipt','receive','received','receiving','receives','receiving','collect','collects','collected','collecting','gather','gathers','gathering','gathered']:
                    s3=s3+" "+"received".lower()+" "
                elif s1_i_crcted in ['hgh','high','higher','highest']:
                    s3=s3+" "+"high".lower()+" "
                elif s1_i_orig in ['dlr','dllr','dollar','dollars','dlrs','dllrs']:
                    s3=s3+" "+"dollar".lower()+" "
                elif s1_i_crcted in ['dlr','dllr','dollar','dollars','dlrs','dllrs']:
                    s3=s3+" "+"dollar".lower()+" "
                elif s1_i_crcted in ['id','identifier']:
                    s3=s3+" "+"id".lower()+" "
                elif str(s2[i]).lower() in ['icd-10','icd']:
                    s3=s3+" "+"diag codes".lower()+" "
                elif str(s2[i]).lower() in ['rcvd']:
                    s3=s3+" "+"received".lower()+" "
                elif s1_i_crcted in ['turn','around','time','high','dollar','claims','claim']:
                    s3=s3+" "+s1_i_crcted+" "
                else:
                    s3=s3+" "+str(s2[i]).lower()+" "
                
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
                s3=s3.replace('taxpayer','').replace('identification','tax id').strip(' ').replace('number',' ')
                s3=s3.replace('  ',' ').replace('  ',' ')
            return s3
        elif context_claim_r_claims.upper()=="CLAIMS":
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
                elif s1_i_crcted in ["claim"]:
                    s3=s3+" "+"claims".lower()+" "
                elif s1_i_orig in ["claims","lob","non","par","npi","non-par"]:
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
                elif s1_i_crcted in ['amount','money','cash','buck','bucks','capital']:
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
                elif s1_i_crcted in ['count','number','sum','whole','reckon','figure','enumerate','add']:
                    s3=s3+" "+"count".lower()+" "
                elif s1_i_crcted in ['receipt','receive','received','receiving','receives','receiving','collect','collects','collected','collecting','gather','gathers','gathering','gathered']:
                    s3=s3+" "+"received".lower()+" "
                elif s1_i_crcted in ['hgh','high','higher','highest']:
                    s3=s3+" "+"high".lower()+" "
                elif s1_i_orig in ['dlr','dllr','dollar','dollars','dlrs','dllrs']:
                    s3=s3+" "+"dollar".lower()+" "
                elif s1_i_crcted in ['dlr','dllr','dollar','dollars','dlrs','dllrs']:
                    s3=s3+" "+"dollar".lower()+" "
                elif s1_i_crcted in ['id','identifier']:
                    s3=s3+" "+"id".lower()+" "
                elif str(s2[i]).lower() in ['icd-10','icd']:
                    s3=s3+" "+"diag codes".lower()+" "
                elif str(s2[i]).lower() in ['rcvd']:
                    s3=s3+" "+"received".lower()+" "
                elif s1_i_crcted in ['turn','around','time','high','dollar','claims','claim']:
                    s3=s3+" "+s1_i_crcted+" "
                else:
                    s3=s3+" "+str(s2[i]).lower()+" "
                
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
                s3=s3.replace('taxpayer','').replace('identification','tax id').strip(' ').replace('number',' ')
                s3=s3.replace('  ',' ').replace('  ',' ')
            return s3

    except:
        print("error in correcting string")


# print(claim_num_extract("what is 12dfs2323"))
# print(corrected_ip_string_1("what is status"))
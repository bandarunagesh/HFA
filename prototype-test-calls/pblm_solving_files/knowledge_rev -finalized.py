##dict of response for each type of intent
from autocorrect import spell

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
                claim_num=s2[i]
                claim_numbers_req.append(claim_num)
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
            # if s2[i].lower() in ["by","uhc","united","health","group","uhg","corporation"]:
            #     s3=s3+" "+""+" "
            # if spell(s2[i]).lower() in ["by","uhc","united","health","group","uhg","corporation"]:
            #     s3=s3+" "+""+" "
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
                s3=s3+" "+spell(s2[i]).lower()+" "
        s3=s3.replace('  ',' ').replace('  ',' ').strip(' ')
        return s3
    except:
        print("error in correcting string")


# print(claim_num_extract("what is 12dfs2323"))
# print(corrected_ip_string_1("what is status"))
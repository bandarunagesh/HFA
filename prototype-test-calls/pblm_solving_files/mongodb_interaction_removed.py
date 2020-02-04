def get_received_claims(dt,provider_lst):
    print(str(dt))
    try:
        n_records="0"
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb["hfa_claims_1819"] 
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
                mydoc = mydoc = mycol.find({'received_date':{'$gt':str(start),'$lt':str(end) },'payto_provider_tax_id':{'$in':provider_lst}})
            else:
                mydoc = mycol.find({'received_date':{'$gt':str(start),'$lt':str(end) }})
            n_records=str(mydoc.count())            
        elif len(dt)==3:
            mydoc = mycol.find({'received_date':{'$regex':'2018-11-.*'}}).limit(5)            
            cond=""
            if len(dt[0])==0:
                cond=cond+",{'received_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[0]:
                    cond=cond+",{'received_date':{'$regex':'.*-.*-"+str(dy)+".*'}}"
                
            if len(dt[1])==0:
                cond=cond+",{'received_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[1]:
                    cond=cond+",{'received_date':{'$regex':'.*-"+str(dy)+"-.*'}}"
                
            if len(dt[2])==0:
                cond=cond+",{'received_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[2]:
                    cond=cond+",{'received_date':{'$regex':'"+str(dy)+"-.*-.*'}}"
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
        mycol = mydb["hfa_claims_1819"] 
        cond=""
        if len(dt)==2:
            s1=str(dt[0])
            start = datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),0,0)
            s1=str(dt[1].split('}')[0])
            end = datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),0,0)
            print(start)
            print(end)
            if len(provider_lst) > 0:
                pipe = [{'$match':{'received_date':{'$gt':str(start),'$lt':str(end) },'payto_provider_tax_id':{'$in':provider_lst}}},{'$group': {'_id':'$received_date', 'total': {'$sum': {'$convert':{'input':'$amt_billed','to':'double'}}}}}] ## sum after type conversion of field            
            else:
                pipe = [{'$match':{'received_date':{'$gt':str(start),'$lt':str(end) }}},{'$group': {'_id':'$received_date', 'total': {'$sum': {'$convert':{'input':'$amt_billed','to':'double'}}}}}] ## sum after type conversion of field            
            mydoc=(mycol.aggregate(pipeline=pipe))            
            billed_amt="0"
            for x in mydoc:
                billed_amt=float(billed_amt)+float(str(x['total']))
            billed_amt=str(billed_amt)
            print(billed_amt)
        elif len(dt)==3:                       
            cond=""
            if len(dt[0])==0:
                cond=cond+",{'received_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[0]:
                    cond=cond+",{'received_date':{'$regex':'.*-.*-"+str(dy)+".*'}}"
                
            if len(dt[1])==0:
                cond=cond+",{'received_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[1]:
                    cond=cond+",{'received_date':{'$regex':'.*-"+str(dy)+"-.*'}}"
                
            if len(dt[2])==0:
                cond=cond+",{'received_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[2]:
                    cond=cond+",{'received_date':{'$regex':'"+str(dy)+"-.*-.*'}}"    
            if len(provider_lst) > 0:
                pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                cond="{'$and':["+cond[1:]+pc+"]}"
                my_dict = ast.literal_eval(cond)
                pipe = [{'$match':my_dict},{'$group': {'_id':'$received_date', 'total': {'$sum': {'$convert':{'input':'$amt_billed','to':'double'}}}}}] ## sum after type conversion of field            
            else:
                pc=""
                cond="{'$and':["+cond[1:]+pc+"]}"
                my_dict = ast.literal_eval(cond)
                pipe = [{'$match':my_dict},{'$group': {'_id':'$received_date', 'total': {'$sum': {'$convert':{'input':'$amt_billed','to':'double'}}}}}] ## sum after type conversion of field                
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
        mycol = mydb["hfa_claims_1819"] 
        cond=""
        if len(dt)==2:
            s1=str(dt[0])
            start = datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),0,0)
            s1=str(dt[1].split('}')[0])
            end = datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),0,0)
            print(start)
            print(end)      
            if len(provider_lst) > 0: 
                pipe = [{'$match':{'$and':[{'received_date':{'$gt':str(start),'$lt':str(end)}},{'payto_provider_tax_id':{'$in':provider_lst}},{'paid_date':{'$gt':str(start),'$lt':str(end)}}]}},{'$group': {'_id':'$paid_date', 'total': {'$sum': {'$convert':{'input':'$amt_paid','to':'double'}}}}}]
            else:
                pipe = [{'$match':{'$and':[{'received_date':{'$gt':str(start),'$lt':str(end)}},{'paid_date':{'$gt':str(start),'$lt':str(end)}}]}},{'$group': {'_id':'$paid_date', 'total': {'$sum': {'$convert':{'input':'$amt_paid','to':'double'}}}}}]
            mydoc=(mycol.aggregate(pipeline=pipe))            
            billed_amt="0"
            for x in mydoc:
                billed_amt=float(billed_amt)+float(str(x['total']))
            billed_amt=str(billed_amt)
            print(billed_amt)
        elif len(dt)==3:                       
            cond=""
            if len(dt[0])==0:
                cond=cond+",{'paid_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[0]:
                    cond=cond+",{'paid_date':{'$regex':'.*-.*-"+str(dy)+".*'}}"
                
            if len(dt[1])==0:
                cond=cond+",{'paid_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[1]:
                    cond=cond+",{'paid_date':{'$regex':'.*-"+str(dy)+"-.*'}}"
                
            if len(dt[2])==0:
                cond=cond+",{'paid_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[2]:
                    cond=cond+",{'paid_date':{'$regex':'"+str(dy)+"-.*-.*'}}"
            cond=cond[1:]            
            cond1=""
            if len(dt[0])==0:
                cond1=cond1+",{'received_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[0]:
                    cond1=cond1+",{'received_date':{'$regex':'.*-.*-"+str(dy)+".*'}}"
                
            if len(dt[1])==0:
                cond1=cond1+",{'received_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[1]:
                    cond1=cond1+",{'received_date':{'$regex':'.*-"+str(dy)+"-.*'}}"
                
            if len(dt[2])==0:
                cond1=cond1+",{'received_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[2]:
                    cond1=cond1+",{'received_date':{'$regex':'"+str(dy)+"-.*-.*'}}"
            cond1=cond1[1:]
            
            if len(provider_lst) > 0:
                pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                cond="{'$and':["+cond+","+cond1+pc+"]}"
            else:
                cond="{'$and':["+cond+","+cond1+"]}"
            my_dict = ast.literal_eval(cond)
            pipe = [{'$match':my_dict},{'$group': {'_id':'$received_date', 'total': {'$sum': {'$convert':{'input':'$amt_paid','to':'double'}}}}}] ## sum after type conversion of field            
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
        mycol = mydb["hfa_claims_1819"] 
        cond=""
        if len(dt)==2:
            s1=str(dt[0])
            start = datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),0,0)
            s1=str(dt[1].split('}')[0])
            end = datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),0,0)
            print(start)
            print(end)       
            if len(provider_lst) > 0:
                pipe = [{'$match':{'$and':[{'received_date':{'$gt':str(start),'$lt':str(end)}},{'claim_denial_ind':'0'},{'payto_provider_tax_id':{'$in':provider_lst}},{'paid_date':{'$gt':str(start),'$lt':str(end)}}]}},{'$group': {'_id':'$paid_date', 'total': {'$sum': 1}}}]
            else:
                pipe = [{'$match':{'$and':[{'received_date':{'$gt':str(start),'$lt':str(end)}},{'claim_denial_ind':'0'},{'paid_date':{'$gt':str(start),'$lt':str(end)}}]}},{'$group': {'_id':'$paid_date', 'total': {'$sum': 1}}}]
            mydoc=(mycol.aggregate(pipeline=pipe))            
            billed_amt="0"
            for x in mydoc:
                billed_amt=int(billed_amt)+int(str(x['total']))
            billed_amt=str(billed_amt)
            print(billed_amt)
        elif len(dt)==3:                       
            cond=""
            if len(dt[0])==0:
                cond=cond+",{'received_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[0]:
                    cond=cond+",{'received_date':{'$regex':'.*-.*-"+str(dy)+".*'}}"
                
            if len(dt[1])==0:
                cond=cond+",{'received_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[1]:
                    cond=cond+",{'received_date':{'$regex':'.*-"+str(dy)+"-.*'}}"
                
            if len(dt[2])==0:
                cond=cond+",{'received_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[2]:
                    cond=cond+",{'received_date':{'$regex':'"+str(dy)+"-.*-.*'}}"
            cond=cond[1:]            
            cond1=""
            if len(dt[0])==0:
                cond1=cond1+",{'paid_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[0]:
                    cond1=cond1+",{'paid_date':{'$regex':'.*-.*-"+str(dy)+".*'}}"
                
            if len(dt[1])==0:
                cond1=cond1+",{'paid_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[1]:
                    cond1=cond1+",{'paid_date':{'$regex':'.*-"+str(dy)+"-.*'}}"
                
            if len(dt[2])==0:
                cond1=cond1+",{'paid_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[2]:
                    cond1=cond1+",{'paid_date':{'$regex':'"+str(dy)+"-.*-.*'}}"
            cond1=cond1[1:]
            if len(provider_lst) > 0:
                pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}},{'claim_denial_ind':'0'}"
                cond="{'$and':["+cond+","+cond1+pc+"]}"
            else:
                cond="{'$and':["+cond+","+cond1+"]}"
            my_dict = ast.literal_eval(cond)
            pipe = [{'$match':my_dict},{'$group': {'_id':'$paid_date', 'total': {'$sum': 1}}}]
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
        mycol = mydb["hfa_claims_1819"] 
        cond=""
        if len(dt)==2:
            s1=str(dt[0])
            start = datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),0,0)
            s1=str(dt[1].split('}')[0])
            end = datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),0,0)
            print(start)
            print(end)
            if len(provider_lst) > 0:
                pipe = [{'$match':{'$and':[{'received_date':{'$gt':str(start),'$lt':str(end) }},{'payto_provider_tax_id':{'$in':provider_lst}},{'claim_receipt_type_cd':'EDI'}]}},{'$group': {'_id':'$received_date', 'total': {'$sum': 1 }}}] ## sum after type conversion of field            
            else:
                pipe = [{'$match':{'$and':[{'received_date':{'$gt':str(start),'$lt':str(end) }},{'claim_receipt_type_cd':'EDI'}]}},{'$group': {'_id':'$received_date', 'total': {'$sum': 1 }}}] ## sum after type conversion of field            
            mydoc=(mycol.aggregate(pipeline=pipe))            
            billed_amt="0"
            for x in mydoc:
                billed_amt=int(billed_amt)+int(str(x['total']))
            billed_amt=str(billed_amt)
            EDI_Cnt=billed_amt
            if len(provider_lst) > 0:
                pipe = [{'$match':{'$and':[{'received_date':{'$gt':str(start),'$lt':str(end) }},{'payto_provider_tax_id':{'$in':provider_lst}},{'claim_receipt_type_cd':'PPR'}]}},{'$group': {'_id':'$received_date', 'total': {'$sum': 1 }}}] ## sum after type conversion of field            
            else:
                pipe = [{'$match':{'$and':[{'received_date':{'$gt':str(start),'$lt':str(end) }},{'claim_receipt_type_cd':'PPR'}]}},{'$group': {'_id':'$received_date', 'total': {'$sum': 1 }}}] ## sum after type conversion of field                        
            
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
                cond=cond+",{'received_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[0]:
                    cond=cond+",{'received_date':{'$regex':'.*-.*-"+str(dy)+".*'}}"
                
            if len(dt[1])==0:
                cond=cond+",{'received_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[1]:
                    cond=cond+",{'received_date':{'$regex':'.*-"+str(dy)+"-.*'}}"
                
            if len(dt[2])==0:
                cond=cond+",{'received_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[2]:
                    cond=cond+",{'received_date':{'$regex':'"+str(dy)+"-.*-.*'}}"
            if len(provider_lst) > 0:
                pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                cond1="{'$and':["+cond[1:]+pc+",{'claim_receipt_type_cd':'EDI' }"+"]}"
            else:
                pc=""
                cond1="{'$and':["+cond[1:]+pc+",{'claim_receipt_type_cd':'EDI' }"+"]}"
            my_dict = ast.literal_eval(cond1)
            pipe = [{'$match':my_dict},{'$group': {'_id':'$received_date', 'total': {'$sum': 1 }}}] ## sum after type conversion of field            
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
            pipe = [{'$match':my_dict},{'$group': {'_id':'$received_date', 'total': {'$sum': 1 }}}] ## sum after type conversion of field            
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

############ denied claims ##############
def get_denied_claims_cnt(dt,provider_lst):
    print(str(dt))
    try:        
        myclient = pymongo.MongoClient(u"mongodb://apsrp03693.uhc.com:27017")        
        mydb = myclient["HandsFreeAnalytics"]        
        mycol = mydb["hfa_claims_1819"] 
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
                pipe = [{'$match':{'$and':[{'paid_date':{'$gt':str(start),'$lt':str(end) }},{'payto_provider_tax_id':{'$in':provider_lst}},{'claim_denial_ind':'1'}]}},{'$group': {'_id':'$root_claim_num', 'total': {'$sum': 1 }}}] ## sum after type conversion of field            
            else:
                pipe = [{'$match':{'$and':[{'paid_date':{'$gt':str(start),'$lt':str(end) }},{'claim_denial_ind':'1'}]}},{'$group': {'_id':'$root_claim_num', 'total': {'$sum': 1 }}}] ## sum after type conversion of field            
            mydoc=(mycol.aggregate(pipeline=pipe))  
            den_claim_lst=list()                      
            for x in mydoc:
                den_claim_lst.append(str(x['_id']))
            if len(provider_lst) > 0:
               pipe = [{'$match':{'$and':[{'paid_date':{'$gt':str(start),'$lt':str(end) }},{'payto_provider_tax_id':{'$in':provider_lst}},{'claim_denial_ind':'0'}]}},{'$group': {'_id':'$root_claim_num', 'total': {'$sum': 1 }}}] ## sum after type conversion of field             
            else:
                pipe = [{'$match':{'$and':[{'paid_date':{'$gt':str(start),'$lt':str(end) }},{'claim_denial_ind':'0'}]}},{'$group': {'_id':'$root_claim_num', 'total': {'$sum': 1 }}}] ## sum after type conversion of field            
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
                cond=cond+",{'paid_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[0]:
                    cond=cond+",{'paid_date':{'$regex':'.*-.*-"+str(dy)+".*'}}"
                
            if len(dt[1])==0:
                cond=cond+",{'paid_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[1]:
                    cond=cond+",{'paid_date':{'$regex':'.*-"+str(dy)+"-.*'}}"
                
            if len(dt[2])==0:
                cond=cond+",{'paid_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[2]:
                    cond=cond+",{'paid_date':{'$regex':'"+str(dy)+"-.*-.*'}}"
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
        mycol = mydb["hfa_claims_1819"] 
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
                pipe = [{'$match':{'$and':[{'paid_date':{'$gt':str(start),'$lt':str(end) }},{'payto_provider_tax_id':{'$in':provider_lst}},{'claim_denial_ind':'1'}]}},{'$group': {'_id':'$root_claim_num','total': {'$sum': {'$convert':{'input':'$amt_billed','to':'double'}}}}}]
            else:
                pipe = [{'$match':{'$and':[{'paid_date':{'$gt':str(start),'$lt':str(end) }},{'claim_denial_ind':'1'}]}},{'$group': {'_id':'$root_claim_num','total': {'$sum': {'$convert':{'input':'$amt_billed','to':'double'}}}}}]
            mydoc=(mycol.aggregate(pipeline=pipe))                                   
            den_claim_lst=list()                      
            for x in mydoc:
                den_claim_lst.append(str(x['_id'])+"!"+str(x['total']))
            if len(provider_lst) > 0:
                pipe = [{'$match':{'$and':[{'paid_date':{'$gt':str(start),'$lt':str(end) }},{'payto_provider_tax_id':{'$in':provider_lst}},{'claim_denial_ind':'0'}]}},{'$group': {'_id':'$root_claim_num','total': {'$sum': {'$convert':{'input':'$amt_billed','to':'double'}}}}}]
            else:
                pipe = [{'$match':{'$and':[{'paid_date':{'$gt':str(start),'$lt':str(end) }},{'claim_denial_ind':'0'}]}},{'$group': {'_id':'$root_claim_num','total': {'$sum': {'$convert':{'input':'$amt_billed','to':'double'}}}}}]
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
                cond=cond+",{'paid_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[0]:
                    cond=cond+",{'paid_date':{'$regex':'.*-.*-"+str(dy)+".*'}}"
                
            if len(dt[1])==0:
                cond=cond+",{'paid_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[1]:
                    cond=cond+",{'paid_date':{'$regex':'.*-"+str(dy)+"-.*'}}"
                
            if len(dt[2])==0:
                cond=cond+",{'paid_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[2]:
                    cond=cond+",{'paid_date':{'$regex':'"+str(dy)+"-.*-.*'}}"
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
        mycol = mydb["hfa_claims_1819"] 
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
                pipe = [{'$match':{'$and':[{'paid_date':{'$gt':str(start),'$lt':str(end) }},{'payto_provider_tax_id':{'$in':provider_lst}},{'claim_denial_ind':'1'}]}},{'$group': {'_id':'$root_claim_num','total': {'$max': {'$convert':{'input':'$claim_receipt_type_cd','to':'string'}}}}}]
            else:
                pipe = [{'$match':{'$and':[{'paid_date':{'$gt':str(start),'$lt':str(end) }},{'claim_denial_ind':'1'}]}},{'$group': {'_id':'$root_claim_num','total': {'$max': {'$convert':{'input':'$claim_receipt_type_cd','to':'string'}}}}}]
            mydoc=(mycol.aggregate(pipeline=pipe))                                   
            den_claim_lst=list()                      
            for x in mydoc:
                den_claim_lst.append(str(x['_id'])+"!"+str(x['total']))
            if len(provider_lst) > 0:
                pipe = [{'$match':{'$and':[{'paid_date':{'$gt':str(start),'$lt':str(end) }},{'payto_provider_tax_id':{'$in':provider_lst}},{'claim_denial_ind':'0'}]}},{'$group': {'_id':'$root_claim_num','total': {'$max': {'$convert':{'input':'$claim_receipt_type_cd','to':'string'}}}}}]
            else:
                pipe = [{'$match':{'$and':[{'paid_date':{'$gt':str(start),'$lt':str(end) }},{'claim_denial_ind':'0'}]}},{'$group': {'_id':'$root_claim_num','total': {'$max': {'$convert':{'input':'$claim_receipt_type_cd','to':'string'}}}}}]
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
                cond=cond+",{'paid_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[0]:
                    cond=cond+",{'paid_date':{'$regex':'.*-.*-"+str(dy)+".*'}}"
                
            if len(dt[1])==0:
                cond=cond+",{'paid_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[1]:
                    cond=cond+",{'paid_date':{'$regex':'.*-"+str(dy)+"-.*'}}"
                
            if len(dt[2])==0:
                cond=cond+",{'paid_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[2]:
                    cond=cond+",{'paid_date':{'$regex':'"+str(dy)+"-.*-.*'}}"
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
        mycol = mydb["hfa_claims_1819"] 
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
                pipe = [{'$match':{'$and':[{'paid_date':{'$gt':str(start),'$lt':str(end) }},{'payto_provider_tax_id':{'$in':provider_lst}},{'claim_denial_ind':'1'}]}},{'$group': {'_id':'$root_claim_num', 'total': {'$sum': 1 }}}] ## sum after type conversion of field            
            else:
                pipe = [{'$match':{'$and':[{'paid_date':{'$gt':str(start),'$lt':str(end) }},{'claim_denial_ind':'1'}]}},{'$group': {'_id':'$root_claim_num', 'total': {'$sum': 1 }}}] ## sum after type conversion of field            
            mydoc=(mycol.aggregate(pipeline=pipe))  
            den_claim_lst=list()                      
            for x in mydoc:
                den_claim_lst.append(str(x['_id']))
            if len(provider_lst) > 0:
                pipe = [{'$match':{'$and':[{'paid_date':{'$gt':str(start),'$lt':str(end) }},{'payto_provider_tax_id':{'$in':provider_lst}},{'claim_denial_ind':'0'}]}},{'$group': {'_id':'$root_claim_num', 'total': {'$sum': 1 }}}] ## sum after type conversion of field            
            else:
                pipe = [{'$match':{'$and':[{'paid_date':{'$gt':str(start),'$lt':str(end) }},{'claim_denial_ind':'0'}]}},{'$group': {'_id':'$root_claim_num', 'total': {'$sum': 1 }}}] ## sum after type conversion of field            
            
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
                cond=cond+",{'paid_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[0]:
                    cond=cond+",{'paid_date':{'$regex':'.*-.*-"+str(dy)+".*'}}"
                
            if len(dt[1])==0:
                cond=cond+",{'paid_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[1]:
                    cond=cond+",{'paid_date':{'$regex':'.*-"+str(dy)+"-.*'}}"
                
            if len(dt[2])==0:
                cond=cond+",{'paid_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[2]:
                    cond=cond+",{'paid_date':{'$regex':'"+str(dy)+"-.*-.*'}}"
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
        mycol = mydb["hfa_claims_1819"] 
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
                pipe = [{'$match':{'$and':[{'paid_date':{'$gt':str(start),'$lt':str(end) }},{'payto_provider_tax_id':{'$in':provider_lst}},{'claim_denial_ind':'1'}]}},{'$group': {'_id':'$root_claim_num','total': {'$sum': {'$convert':{'input':'$amt_billed','to':'double'}}}}}]
            else:
                pipe = [{'$match':{'$and':[{'paid_date':{'$gt':str(start),'$lt':str(end) }},{'claim_denial_ind':'1'}]}},{'$group': {'_id':'$root_claim_num','total': {'$sum': {'$convert':{'input':'$amt_billed','to':'double'}}}}}]
            mydoc=(mycol.aggregate(pipeline=pipe))                                   
            den_claim_lst=list()                      
            for x in mydoc:
                den_claim_lst.append(str(x['_id'])+"!"+str(x['total']))
            if len(provider_lst) > 0: 
                pipe = [{'$match':{'$and':[{'paid_date':{'$gt':str(start),'$lt':str(end) }},{'payto_provider_tax_id':{'$in':provider_lst}},{'claim_denial_ind':'0'}]}},{'$group': {'_id':'$root_claim_num','total': {'$sum': {'$convert':{'input':'$amt_billed','to':'double'}}}}}]
            else:
                pipe = [{'$match':{'$and':[{'paid_date':{'$gt':str(start),'$lt':str(end) }},{'claim_denial_ind':'0'}]}},{'$group': {'_id':'$root_claim_num','total': {'$sum': {'$convert':{'input':'$amt_billed','to':'double'}}}}}]
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
                cond=cond+",{'paid_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[0]:
                    cond=cond+",{'paid_date':{'$regex':'.*-.*-"+str(dy)+".*'}}"
                
            if len(dt[1])==0:
                cond=cond+",{'paid_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[1]:
                    cond=cond+",{'paid_date':{'$regex':'.*-"+str(dy)+"-.*'}}"
                
            if len(dt[2])==0:
                cond=cond+",{'paid_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[2]:
                    cond=cond+",{'paid_date':{'$regex':'"+str(dy)+"-.*-.*'}}"
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
        mycol = mydb["hfa_claims_1819"] 
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
                pipe = [{'$match':{'$and':[{'paid_date':{'$gt':str(start),'$lt':str(end) }},{'payto_provider_tax_id':{'$in':provider_lst}},{'claim_denial_ind':'1'}]}},{'$group': {'_id':'$root_claim_num','total': {'$sum': {'$convert':{'input':'$amt_paid','to':'double'}}}}}]
            else:
                pipe = [{'$match':{'$and':[{'paid_date':{'$gt':str(start),'$lt':str(end) }},{'claim_denial_ind':'1'}]}},{'$group': {'_id':'$root_claim_num','total': {'$sum': {'$convert':{'input':'$amt_paid','to':'double'}}}}}]
            mydoc=(mycol.aggregate(pipeline=pipe))                                   
            den_claim_lst=list()                      
            for x in mydoc:
                den_claim_lst.append(str(x['_id'])+"!"+str(x['total']))
            if len(provider_lst) > 0:
                pipe = [{'$match':{'$and':[{'paid_date':{'$gt':str(start),'$lt':str(end) }},{'payto_provider_tax_id':{'$in':provider_lst}},{'claim_denial_ind':'0'}]}},{'$group': {'_id':'$root_claim_num','total': {'$sum': {'$convert':{'input':'$amt_paid','to':'double'}}}}}]
            else:
                pipe = [{'$match':{'$and':[{'paid_date':{'$gt':str(start),'$lt':str(end) }},{'claim_denial_ind':'0'}]}},{'$group': {'_id':'$root_claim_num','total': {'$sum': {'$convert':{'input':'$amt_paid','to':'double'}}}}}]
            
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
                cond=cond+",{'paid_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[0]:
                    cond=cond+",{'paid_date':{'$regex':'.*-.*-"+str(dy)+".*'}}"
                
            if len(dt[1])==0:
                cond=cond+",{'paid_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[1]:
                    cond=cond+",{'paid_date':{'$regex':'.*-"+str(dy)+"-.*'}}"
                
            if len(dt[2])==0:
                cond=cond+",{'paid_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[2]:
                    cond=cond+",{'paid_date':{'$regex':'"+str(dy)+"-.*-.*'}}"
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
        mycol = mydb["hfa_claims_1819"] 
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
                pipe = [{'$match':{'$and':[{'paid_date':{'$gt':str(start),'$lt':str(end) }},{'payto_provider_tax_id':{'$in':provider_lst}},{'claim_denial_ind':'1'}]}},{'$group': {'_id':'$root_claim_num','total': {'$max': {'$convert':{'input':'$claim_receipt_type_cd','to':'string'}}}}}]
            else:
                pipe = [{'$match':{'$and':[{'paid_date':{'$gt':str(start),'$lt':str(end) }},{'claim_denial_ind':'1'}]}},{'$group': {'_id':'$root_claim_num','total': {'$max': {'$convert':{'input':'$claim_receipt_type_cd','to':'string'}}}}}]
            
            mydoc=(mycol.aggregate(pipeline=pipe))                                   
            den_claim_lst=list()                      
            for x in mydoc:
                den_claim_lst.append(str(x['_id'])+"!"+str(x['total']))
            if len(provider_lst) > 0:
                pipe = [{'$match':{'$and':[{'paid_date':{'$gt':str(start),'$lt':str(end) }},{'payto_provider_tax_id':{'$in':provider_lst}},{'claim_denial_ind':'0'}]}},{'$group': {'_id':'$root_claim_num','total': {'$max': {'$convert':{'input':'$claim_receipt_type_cd','to':'string'}}}}}]
            else:
                pipe = [{'$match':{'$and':[{'paid_date':{'$gt':str(start),'$lt':str(end) }},{'claim_denial_ind':'0'}]}},{'$group': {'_id':'$root_claim_num','total': {'$max': {'$convert':{'input':'$claim_receipt_type_cd','to':'string'}}}}}]
            
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
                cond=cond+",{'paid_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[0]:
                    cond=cond+",{'paid_date':{'$regex':'.*-.*-"+str(dy)+".*'}}"
                
            if len(dt[1])==0:
                cond=cond+",{'paid_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[1]:
                    cond=cond+",{'paid_date':{'$regex':'.*-"+str(dy)+"-.*'}}"
                
            if len(dt[2])==0:
                cond=cond+",{'paid_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[2]:
                    cond=cond+",{'paid_date':{'$regex':'"+str(dy)+"-.*-.*'}}"
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
        mycol = mydb["hfa_claims_1819"] 
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
                pipe = [{'$match':{'$and':[{'paid_date':{'$gt':str(start),'$lt':str(end) }},{'payto_provider_tax_id':{'$in':provider_lst}},{'claim_adj_ind':'1'}]}},{'$group': {'_id':'$root_claim_num', 'total': {'$sum': 1 }}}] ## sum after type conversion of field            
            else:
                pipe = [{'$match':{'$and':[{'paid_date':{'$gt':str(start),'$lt':str(end) }},{'claim_adj_ind':'1'}]}},{'$group': {'_id':'$root_claim_num', 'total': {'$sum': 1 }}}] ## sum after type conversion of field            
            mydoc=(mycol.aggregate(pipeline=pipe)) 
            c=0
            for x in mydoc:
                c=c+1 
            n_records=str(c)
        elif len(dt)==3:                       
            cond=""
            if len(dt[0])==0:
                cond=cond+",{'paid_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[0]:
                    cond=cond+",{'paid_date':{'$regex':'.*-.*-"+str(dy)+".*'}}"
                
            if len(dt[1])==0:
                cond=cond+",{'paid_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[1]:
                    cond=cond+",{'paid_date':{'$regex':'.*-"+str(dy)+"-.*'}}"
                
            if len(dt[2])==0:
                cond=cond+",{'paid_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[2]:
                    cond=cond+",{'paid_date':{'$regex':'"+str(dy)+"-.*-.*'}}"
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
        mycol = mydb["hfa_claims_1819"] 
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
                pipe = [{'$match':{'$and':[{'paid_date':{'$gt':str(start),'$lt':str(end) }},{'payto_provider_tax_id':{'$in':provider_lst}},{'claim_adj_ind':'1'}]}},{'$group': {'_id':'$root_claim_num','total': {'$sum': {'$convert':{'input':'$amt_billed','to':'double'}}}}}]
            else:
                pipe = [{'$match':{'$and':[{'paid_date':{'$gt':str(start),'$lt':str(end) }},{'claim_adj_ind':'1'}]}},{'$group': {'_id':'$root_claim_num','total': {'$sum': {'$convert':{'input':'$amt_billed','to':'double'}}}}}]
            mydoc=(mycol.aggregate(pipeline=pipe)) 
            n_records='0'        
            for x in mydoc:
                n_records=str(float(n_records)+float(x['total']))

        elif len(dt)==3:                       
            cond=""
            if len(dt[0])==0:
                cond=cond+",{'paid_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[0]:
                    cond=cond+",{'paid_date':{'$regex':'.*-.*-"+str(dy)+".*'}}"
                
            if len(dt[1])==0:
                cond=cond+",{'paid_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[1]:
                    cond=cond+",{'paid_date':{'$regex':'.*-"+str(dy)+"-.*'}}"
                
            if len(dt[2])==0:
                cond=cond+",{'paid_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[2]:
                    cond=cond+",{'paid_date':{'$regex':'"+str(dy)+"-.*-.*'}}"
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
        mycol = mydb["hfa_claims_1819"] 
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
                pipe = [{'$match':{'$and':[{'paid_date':{'$gt':str(start),'$lt':str(end) }},{'payto_provider_tax_id':{'$in':provider_lst}},{'claim_adj_ind':'1'}]}},{'$group': {'_id':'$root_claim_num','total': {'$sum': {'$convert':{'input':'$amt_paid','to':'double'}}}}}]
            else:
                pipe = [{'$match':{'$and':[{'paid_date':{'$gt':str(start),'$lt':str(end) }},{'claim_adj_ind':'1'}]}},{'$group': {'_id':'$root_claim_num','total': {'$sum': {'$convert':{'input':'$amt_paid','to':'double'}}}}}]
            mydoc=(mycol.aggregate(pipeline=pipe)) 
            n_records='0'        
            for x in mydoc:
                n_records=str(float(n_records)+float(x['total']))

        elif len(dt)==3:                       
            cond=""
            if len(dt[0])==0:
                cond=cond+",{'paid_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[0]:
                    cond=cond+",{'paid_date':{'$regex':'.*-.*-"+str(dy)+".*'}}"
                
            if len(dt[1])==0:
                cond=cond+",{'paid_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[1]:
                    cond=cond+",{'paid_date':{'$regex':'.*-"+str(dy)+"-.*'}}"
                
            if len(dt[2])==0:
                cond=cond+",{'paid_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[2]:
                    cond=cond+",{'paid_date':{'$regex':'"+str(dy)+"-.*-.*'}}"
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
        mycol = mydb["hfa_claims_1819"] 
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
                pipe = [{'$match':{'$and':[{'paid_date':{'$gt':str(start),'$lt':str(end) }},{'payto_provider_tax_id':{'$in':provider_lst}},{'claim_adj_ind':'1'}]}},{'$group': {'_id':'$root_claim_num','total': {'$sum': {'$convert':{'input':'$amt_paid','to':'double'}}}}}]
            else:
                pipe = [{'$match':{'$and':[{'paid_date':{'$gt':str(start),'$lt':str(end) }},{'claim_adj_ind':'1'}]}},{'$group': {'_id':'$root_claim_num','total': {'$sum': {'$convert':{'input':'$amt_paid','to':'double'}}}}}]
            mydoc=(mycol.aggregate(pipeline=pipe)) 
            n_records_pa='0'        
            for x in mydoc:
                n_records_pa=str(float(n_records_pa)+float(x['total']))

            if len(provider_lst) > 0:
                pipe = [{'$match':{'$and':[{'paid_date':{'$gt':str(start),'$lt':str(end) }},{'payto_provider_tax_id':{'$in':provider_lst}},{'claim_adj_ind':'1'}]}},{'$group': {'_id':'$root_claim_num','total': {'$sum': {'$convert':{'input':'$amt_billed','to':'double'}}}}}]
            else:
                pipe = [{'$match':{'$and':[{'paid_date':{'$gt':str(start),'$lt':str(end) }},{'claim_adj_ind':'1'}]}},{'$group': {'_id':'$root_claim_num','total': {'$sum': {'$convert':{'input':'$amt_billed','to':'double'}}}}}]
            mydoc=(mycol.aggregate(pipeline=pipe)) 
            n_records_ba='0'        
            for x in mydoc:
                n_records_ba=str(float(n_records_ba)+float(x['total']))
            n_records=str(float(n_records_ba)-float(n_records_pa))

        elif len(dt)==3:                       
            cond=""
            if len(dt[0])==0:
                cond=cond+",{'paid_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[0]:
                    cond=cond+",{'paid_date':{'$regex':'.*-.*-"+str(dy)+".*'}}"
                
            if len(dt[1])==0:
                cond=cond+",{'paid_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[1]:
                    cond=cond+",{'paid_date':{'$regex':'.*-"+str(dy)+"-.*'}}"
                
            if len(dt[2])==0:
                cond=cond+",{'paid_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[2]:
                    cond=cond+",{'paid_date':{'$regex':'"+str(dy)+"-.*-.*'}}"
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
        mycol = mydb["hfa_claims_1819"] 
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
                pipe = [{'$match':{'$and':[{'paid_date':{'$gt':str(start),'$lt':str(end) }},{'payto_provider_tax_id':{'$in':provider_lst}},{'claim_adj_ind':'1'}]}},{'$group': {'_id':'$root_claim_num','total': {'$max': {'$convert':{'input':'$claim_receipt_type_cd','to':'string'}}}}}]                
            else:
                pipe = [{'$match':{'$and':[{'paid_date':{'$gt':str(start),'$lt':str(end) }},{'claim_adj_ind':'1'}]}},{'$group': {'_id':'$root_claim_num','total': {'$max': {'$convert':{'input':'$claim_receipt_type_cd','to':'string'}}}}}]
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
                cond=cond+",{'paid_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[0]:
                    cond=cond+",{'paid_date':{'$regex':'.*-.*-"+str(dy)+".*'}}"
                
            if len(dt[1])==0:
                cond=cond+",{'paid_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[1]:
                    cond=cond+",{'paid_date':{'$regex':'.*-"+str(dy)+"-.*'}}"
                
            if len(dt[2])==0:
                cond=cond+",{'paid_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[2]:
                    cond=cond+",{'paid_date':{'$regex':'"+str(dy)+"-.*-.*'}}"
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
        mycol = mydb["hfa_claims_1819"] 
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
                pipe = [{'$match':{'$and':[{'received_date':{'$gt':str(start),'$lt':str(end) }},{'payto_provider_tax_id':{'$in':provider_lst}},{'claim_high_dollar_paid_ind':'1'}]}},{'$group': {'_id':'$root_claim_num', 'total': {'$sum': 1 }}}] ## sum after type conversion of field            
            else:
                pipe = [{'$match':{'$and':[{'received_date':{'$gt':str(start),'$lt':str(end) }},{'claim_high_dollar_paid_ind':'1'}]}},{'$group': {'_id':'$root_claim_num', 'total': {'$sum': 1 }}}] ## sum after type conversion of field            
            mydoc=(mycol.aggregate(pipeline=pipe)) 
            c=0
            for x in mydoc:
                c=c+1 
            n_records=str(c)
        elif len(dt)==3:                       
            cond=""
            if len(dt[0])==0:
                cond=cond+",{'received_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[0]:
                    cond=cond+",{'received_date':{'$regex':'.*-.*-"+str(dy)+".*'}}"
                
            if len(dt[1])==0:
                cond=cond+",{'received_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[1]:
                    cond=cond+",{'received_date':{'$regex':'.*-"+str(dy)+"-.*'}}"
                
            if len(dt[2])==0:
                cond=cond+",{'received_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[2]:
                    cond=cond+",{'received_date':{'$regex':'"+str(dy)+"-.*-.*'}}"
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
        mycol = mydb["hfa_claims_1819"] 
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
                pipe = [{'$match':{'$and':[{'received_date':{'$gt':str(start),'$lt':str(end) }},{'payto_provider_tax_id':{'$in':provider_lst}},{'claim_high_dollar_paid_ind':'1'}]}},{'$group': {'_id':'$root_claim_num','total': {'$max': {'$convert':{'input':'$claim_receipt_type_cd','to':'string'}}}}}]
            else:
                pipe = [{'$match':{'$and':[{'received_date':{'$gt':str(start),'$lt':str(end) }},{'claim_high_dollar_paid_ind':'1'}]}},{'$group': {'_id':'$root_claim_num','total': {'$max': {'$convert':{'input':'$claim_receipt_type_cd','to':'string'}}}}}]
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
                cond=cond+",{'received_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[0]:
                    cond=cond+",{'received_date':{'$regex':'.*-.*-"+str(dy)+".*'}}"
                
            if len(dt[1])==0:
                cond=cond+",{'received_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[1]:
                    cond=cond+",{'received_date':{'$regex':'.*-"+str(dy)+"-.*'}}"
                
            if len(dt[2])==0:
                cond=cond+",{'received_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[2]:
                    cond=cond+",{'received_date':{'$regex':'"+str(dy)+"-.*-.*'}}"
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
        mycol = mydb["hfa_claims_1819"] 
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
                pipe = [{'$match':{'$and':[{'received_date':{'$gt':str(start),'$lt':str(end) }},{'payto_provider_tax_id':{'$in':provider_lst}},{'claim_high_dollar_paid_ind':'1'}]}},{'$group': {'_id':'$root_claim_num','total': {'$sum': {'$convert':{'input':'$amt_billed','to':'double'}}}}}]
            else:
                pipe = [{'$match':{'$and':[{'received_date':{'$gt':str(start),'$lt':str(end) }},{'claim_high_dollar_paid_ind':'1'}]}},{'$group': {'_id':'$root_claim_num','total': {'$sum': {'$convert':{'input':'$amt_billed','to':'double'}}}}}]
            mydoc=(mycol.aggregate(pipeline=pipe)) 
            n_records='0'        
            for x in mydoc:
                n_records=str(float(n_records)+float(x['total']))

        elif len(dt)==3:                       
            cond=""
            if len(dt[0])==0:
                cond=cond+",{'received_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[0]:
                    cond=cond+",{'received_date':{'$regex':'.*-.*-"+str(dy)+".*'}}"
                
            if len(dt[1])==0:
                cond=cond+",{'received_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[1]:
                    cond=cond+",{'received_date':{'$regex':'.*-"+str(dy)+"-.*'}}"
                
            if len(dt[2])==0:
                cond=cond+",{'received_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[2]:
                    cond=cond+",{'received_date':{'$regex':'"+str(dy)+"-.*-.*'}}"
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
        mycol = mydb["hfa_claims_1819"] 
        cond=""
        if len(dt)==2:
            s1=str(dt[0])
            start = datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),0,0)
            s1=str(dt[1].split('}')[0])
            end = datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),0,0)
            print(start)
            print(end)            
            if len(provider_lst) > 0:
                pipe = [{'$match':{'$and':[{'received_date':{'$gt':str(start),'$lt':str(end)}},{'payto_provider_tax_id':{'$in':provider_lst}},{'paid_date':{'$gt':str(start),'$lt':str(end)}},{'claim_high_dollar_paid_ind':'1'}]}},{'$group': {'_id':'$paid_date', 'total': {'$sum': {'$convert':{'input':'$amt_paid','to':'double'}}}}}]
            else:
                pipe = [{'$match':{'$and':[{'received_date':{'$gt':str(start),'$lt':str(end)}},{'paid_date':{'$gt':str(start),'$lt':str(end)}},{'claim_high_dollar_paid_ind':'1'}]}},{'$group': {'_id':'$paid_date', 'total': {'$sum': {'$convert':{'input':'$amt_paid','to':'double'}}}}}]
            mydoc=(mycol.aggregate(pipeline=pipe))            
            billed_amt="0"
            for x in mydoc:
                billed_amt=float(billed_amt)+float(str(x['total']))
            billed_amt=str(billed_amt)
            print(billed_amt)
        elif len(dt)==3:                       
            cond=""
            if len(dt[0])==0:
                cond=cond+",{'received_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[0]:
                    cond=cond+",{'received_date':{'$regex':'.*-.*-"+str(dy)+".*'}}"
                
            if len(dt[1])==0:
                cond=cond+",{'received_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[1]:
                    cond=cond+",{'received_date':{'$regex':'.*-"+str(dy)+"-.*'}}"
                
            if len(dt[2])==0:
                cond=cond+",{'received_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[2]:
                    cond=cond+",{'received_date':{'$regex':'"+str(dy)+"-.*-.*'}}"
            cond=cond[1:]            
            cond1=""
            if len(dt[0])==0:
                cond1=cond1+",{'received_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[0]:
                    cond1=cond1+",{'received_date':{'$regex':'.*-.*-"+str(dy)+".*'}}"
                
            if len(dt[1])==0:
                cond1=cond1+",{'received_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[1]:
                    cond1=cond1+",{'received_date':{'$regex':'.*-"+str(dy)+"-.*'}}"
                
            if len(dt[2])==0:
                cond1=cond1+",{'received_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[2]:
                    cond1=cond1+",{'received_date':{'$regex':'"+str(dy)+"-.*-.*'}}"
            cond1=cond1[1:]
            cond2="{'claim_high_dollar_paid_ind':'1'}"
            if len(provider_lst) >0:
                pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                cond="{'$and':["+cond+pc+","+cond1+","+cond2+"]}"
            else:
                cond="{'$and':["+cond+","+cond1+","+cond2+"]}"
            
            my_dict = ast.literal_eval(cond)
            pipe = [{'$match':my_dict},{'$group': {'_id':'$received_date', 'total': {'$sum': {'$convert':{'input':'$amt_paid','to':'double'}}}}}] ## sum after type conversion of field            
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
        mycol = mydb["hfa_claims_1819"] 
        cond=""
        if len(dt)==2:
            s1=str(dt[0])
            start = datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),0,0)
            s1=str(dt[1].split('}')[0])
            end = datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),0,0)
            print(start)
            print(end)            
            if len(provider_lst) > 0:
                pipe = [{'$match':{'$and':[{'received_date':{'$gt':str(start),'$lt':str(end)}},{'payto_provider_tax_id':{'$in':provider_lst}},{'claim_denial_ind':'0'},{'paid_date':{'$gt':str(start),'$lt':str(end)}},{'claim_high_dollar_paid_ind':'1'}]}},{'$group': {'_id':'$paid_date', 'total': {'$sum': 1}}}]    
            else:
                pipe = [{'$match':{'$and':[{'received_date':{'$gt':str(start),'$lt':str(end)}},{'claim_denial_ind':'0'},{'paid_date':{'$gt':str(start),'$lt':str(end)}},{'claim_high_dollar_paid_ind':'1'}]}},{'$group': {'_id':'$paid_date', 'total': {'$sum': 1}}}]
            mydoc=(mycol.aggregate(pipeline=pipe))            
            billed_amt="0"
            for x in mydoc:
                billed_amt=int(billed_amt)+int(str(x['total']))
            billed_amt=str(billed_amt)
            print(billed_amt)
        elif len(dt)==3:                       
            cond=""
            if len(dt[0])==0:
                cond=cond+",{'received_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[0]:
                    cond=cond+",{'received_date':{'$regex':'.*-.*-"+str(dy)+".*'}}"
                
            if len(dt[1])==0:
                cond=cond+",{'received_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[1]:
                    cond=cond+",{'received_date':{'$regex':'.*-"+str(dy)+"-.*'}}"
                
            if len(dt[2])==0:
                cond=cond+",{'received_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[2]:
                    cond=cond+",{'received_date':{'$regex':'"+str(dy)+"-.*-.*'}}"
            cond=cond[1:]            
            cond1=""
            if len(dt[0])==0:
                cond1=cond1+",{'paid_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[0]:
                    cond1=cond1+",{'paid_date':{'$regex':'.*-.*-"+str(dy)+".*'}}"
                
            if len(dt[1])==0:
                cond1=cond1+",{'paid_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[1]:
                    cond1=cond1+",{'paid_date':{'$regex':'.*-"+str(dy)+"-.*'}}"
                
            if len(dt[2])==0:
                cond1=cond1+",{'paid_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[2]:
                    cond1=cond1+",{'paid_date':{'$regex':'"+str(dy)+"-.*-.*'}}"
            cond1=cond1[1:]
            cond2="{'claim_high_dollar_paid_ind':'1'},{'claim_denial_ind':'0'}"
            if len(provider_lst) >0:
                pc=",{'payto_provider_tax_id':{'$in':"+str(provider_lst)+"}}"
                cond="{'$and':["+cond+pc+","+cond1+","+cond2+"]}"
            else:
                cond="{'$and':["+cond+","+cond1+","+cond2+"]}"
                       
            my_dict = ast.literal_eval(cond)
            pipe = [{'$match':my_dict},{'$group': {'_id':'$paid_date', 'total': {'$sum': 1}}}]
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
        mycol = mydb["hfa_claims_1819"]
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
        mycol = mydb["hfa_claims_1819"] 
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
                pipe = [{'$match':{'$and':[{'paid_date':{'$gt':str(start),'$lt':str(end) }},{'payto_provider_tax_id':{'$in':provider_lst}},{'claim_denial_ind':'1'}]}},{'$group': {'_id':'$denial_description', 'total': {'$sum': 1 }}}] ## sum after type conversion of field            
            else:
                pipe = [{'$match':{'$and':[{'paid_date':{'$gt':str(start),'$lt':str(end) }},{'claim_denial_ind':'1'}]}},{'$group': {'_id':'$denial_description', 'total': {'$sum': 1 }}}] ## sum after type conversion of field            
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
                cond=cond+",{'paid_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[0]:
                    cond=cond+",{'paid_date':{'$regex':'.*-.*-"+str(dy)+".*'}}"
                
            if len(dt[1])==0:
                cond=cond+",{'paid_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[1]:
                    cond=cond+",{'paid_date':{'$regex':'.*-"+str(dy)+"-.*'}}"
                
            if len(dt[2])==0:
                cond=cond+",{'paid_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[2]:
                    cond=cond+",{'paid_date':{'$regex':'"+str(dy)+"-.*-.*'}}"
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
        mycol = mydb["hfa_claims_1819"] 
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
                pipe = [{'$match':{'$and':[{'paid_date':{'$gt':str(start),'$lt':str(end) }},{'payto_provider_tax_id':{'$in':provider_lst}},{'claim_adj_ind':'1'}]}},{'$group': {'_id':'$adjustment_description', 'total': {'$sum': 1 }}}] ## sum after type conversion of field            
            else:
                pipe = [{'$match':{'$and':[{'paid_date':{'$gt':str(start),'$lt':str(end) }},{'claim_adj_ind':'1'}]}},{'$group': {'_id':'$adjustment_description', 'total': {'$sum': 1 }}}] ## sum after type conversion of field            
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
                cond=cond+",{'paid_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[0]:
                    cond=cond+",{'paid_date':{'$regex':'.*-.*-"+str(dy)+".*'}}"
                
            if len(dt[1])==0:
                cond=cond+",{'paid_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[1]:
                    cond=cond+",{'paid_date':{'$regex':'.*-"+str(dy)+"-.*'}}"
                
            if len(dt[2])==0:
                cond=cond+",{'paid_date':{'$regex':'.*-.*-.*'}}"
            else:
                for dy in dt[2]:
                    cond=cond+",{'paid_date':{'$regex':'"+str(dy)+"-.*-.*'}}"
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

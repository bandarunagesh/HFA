import sqlite3
from sqlite3 import Error
from datetime import datetime
import calendar
import traceback



def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None


def get_status(value1):

    try:
        
        # print("get_status")
        database = "claims.db"
        claim_num_rec="'"+str(value1)+"'"
        # print(claim_num_rec)
        conn = create_connection(database)
        cur = conn.cursor()
        cur.execute("select count(*) from claims_sample where root_claim_num="+claim_num_rec)
        all_rows=cur.fetchall()
        n_records=str(all_rows[0][0])
        cur.execute("select count(*) from claims_sample where root_claim_num="+claim_num_rec+" and claim_denial_ind='1'")
        all_rows=cur.fetchall()
        n_denial_recds=str(all_rows[0][0])
        cur.execute("select count(*) from claims_sample where root_claim_num="+claim_num_rec+" and claim_adj_ind='1'")
        all_rows=cur.fetchall()
        n_adj_recds=str(all_rows[0][0])

        if int(n_records)==int(n_denial_recds) and int(n_records)!=0:
            #print("1")
            status_ind=1
            cur.execute("select round(sum(amt_billed),2) from claims_sample where root_claim_num="+claim_num_rec+"")
            denial_amt=str(round(float(str((cur.fetchall())[0][0]).replace('None','0')),2))
            # print(denial_amt)
            cur.execute("select max(received_date) from claims_sample where root_claim_num="+claim_num_rec+" ")
            t=str(cur.fetchall()[0][0]).replace('None','')
            date_str=datetime(int(t.split('-')[0]),int(t.split('-')[1]),int((t.split('-')[2]).split(' ')[0]))
            t=(date_str.strftime('%Y-%b-%d'))
            status="1}Your claim has been completely denied for the amount "+denial_amt+" on "+t.split('-')[2]+"th of "+t.split('-')[1] +", "+t.split('-')[0]+"!Why was my Claim Denied!How can I resubmit my Claim!What's the time taken to process my claim"
            # print(status)
            return(status)
        elif int(n_denial_recds)==0 and int(n_adj_recds)==0 and int(n_records)!=0:
            # print("2")
            status_ind=2
            cur.execute("select round(sum(amt_paid),2) from claims_sample where root_claim_num="+claim_num_rec+"")
            paid_amt=str(round(float(str((cur.fetchall())[0][0]).replace('None','0')),2))
            # print(paid_amt)
            cur.execute("select max(received_date) from claims_sample where root_claim_num="+claim_num_rec+" ")
            t=str(cur.fetchall()[0][0]).replace('None','')        
            date_str=datetime(int(t.split('-')[0]),int(t.split('-')[1]),int((t.split('-')[2]).split(' ')[0]))
            t=(date_str.strftime('%Y-%b-%d'))
            status="2}Your claim has been completely paid for the amount "+paid_amt+" on "+t.split('-')[2]+"th of "+t.split('-')[1] +", "+t.split('-')[0]+"!What's the time taken to process my claim"
            # print(status)
            return(status)
        elif int(n_denial_recds)==0 and int(n_adj_recds) > 0 and int(n_records)!=0:
            # print("3")
            status_ind=3
            cur.execute("select round(sum(amt_paid),2) from claims_sample where root_claim_num="+claim_num_rec+"")
            paid_amt=str(round(float(str((cur.fetchall())[0][0]).replace('None','0')),2))
            # print(paid_amt)
            cur.execute("select max(received_date) from claims_sample where root_claim_num="+claim_num_rec+" ")
            t=str(cur.fetchall()[0][0]).replace('None','')     
            date_str=datetime(int(t.split('-')[0]),int(t.split('-')[1]),int((t.split('-')[2]).split(' ')[0]))
            t=(date_str.strftime('%Y-%b-%d'))##max received date
            status="3}Your claim has been paid for the amount "+paid_amt+" on "+t.split('-')[2]+"th of "+t.split('-')[1] +", "+t.split('-')[0]+" with adjustments!Why was my Claim Adjusted!What is Adjusted amount!What is the amount paid towards Claim!What's the time taken to process my claim"
            # print(status)
            return(status)
        elif int(n_denial_recds)>0 and int(n_records)!=0:
            # print("4")
            status_ind=4
            cur.execute("select round(sum(amt_paid),2) from claims_sample where root_claim_num="+claim_num_rec+"")
            paid_amt=(round(float(str((cur.fetchall())[0][0]).replace('None','0')),2))
            # print(paid_amt)
            cur.execute("select round(sum(amt_billed),2) from claims_sample where root_claim_num="+claim_num_rec+"")
            billed_amt=(round(float(str((cur.fetchall())[0][0]).replace('None','0')),2))
            # print(billed_amt)
            denied_amt=str(billed_amt-paid_amt)
            cur.execute("select max(received_date) from claims_sample where root_claim_num="+claim_num_rec+" ")
            t=str(cur.fetchall()[0][0]).replace('None','')       
            date_str=datetime(int(t.split('-')[0]),int(t.split('-')[1]),int((t.split('-')[2]).split(' ')[0]))
            t=(date_str.strftime('%Y-%b-%d'))##max received date
            status="4}Your claim has been partially denied with "+str(denied_amt) +" being denied out of "+str(billed_amt)+" on "+t.split('-')[2]+"th of "+t.split('-')[1] +", "+t.split('-')[0]+"!Why is my claim partially denied!How can I resubmit my claim!What's the time taken to process my claim"
            # print(status)
            return(status)
        elif int(n_records)==0:
            # print("5")
            status_ind=5
            status="5}Could not find claim with Claim Number "+claim_num_rec+", Please make sure you entered correct details "
            # print(status)
            return(status)
        else:
            print(str(n_records))
            print(str(n_adj_recds))
            print(str(n_denial_recds))

        conn.commit()
        conn.close()
    except:
        return "Sorry, Could not fetch you results at this time"

def get_action_reason(value1):

    try:
        r=""
        s=""
        print("get_action_reason")        
        s=get_status(value1)
        status_ind=int(s.split('}')[0])
        if status_ind==1 or status_ind==4:
            r=get_denial_reason(value1)
        elif status_ind==3:
            r=get_adjustment_reason(value1)
        elif status_ind==2 or status_ind==5 :
            r=s.split('}')[1]
        print(r)
        return r
        

    except Error as e:
        print(str(e))
        return "Sorry, Could not fetch you results at this time"

def get_processing_time(value1):

    try:
        # print("get_processing_time")
        database = "claims.db"
        claim_num_rec="'"+str(value1)+"'"
        # print(claim_num_rec)
        conn = create_connection(database)
        cur = conn.cursor()
        cur.execute("select count(*) from claims_sample where root_claim_num="+claim_num_rec)
        all_rows=cur.fetchall()
        n_records=str(all_rows[0][0])
        if int(n_records)==0:
            proc_time="Could not find claim with Claim Number "+claim_num_rec+", Please make sure you entered correct details "
            # print(proc_time)
            return(proc_time)
        elif int(n_records)>0:
            cur.execute("select max(fromdatetopaiddate) from claims_sample where root_claim_num="+claim_num_rec)
            all_rows=cur.fetchall()
            n_p_days=str(all_rows[0][0]).replace('None','0')
            proc_time="End to End processing time for your claim is "+n_p_days+" days"##+"!Give me processing time for this period"
            cur.execute("select max(fromdatetoreceiveddate) from claims_sample where root_claim_num="+claim_num_rec)
            all_rows=cur.fetchall()
            n_p_days=str(all_rows[0][0]).replace('None','0')
            proc_time=proc_time+"\n Provider claim submission time for your claim is "+n_p_days+" days"
            cur.execute("select max(receiveddatetopaiddate) from claims_sample where root_claim_num="+claim_num_rec)
            all_rows=cur.fetchall()
            n_p_days=str(all_rows[0][0]).replace('None','0')
            proc_time=proc_time+"\n UHC Processing time for your claim is "+n_p_days+" days"
            # print(proc_time)
            return(proc_time)
        
        conn.commit()
        conn.close()
    except:
        return "Sorry, Could not fetch you results at this time"

def get_denial_reason(value1):

    try:
        # print("get_denial_reason")
        database = "claims.db"
        claim_num_rec="'"+str(value1)+"'"
        # print(claim_num_rec)
        conn = create_connection(database)
        cur = conn.cursor()
        cur.execute("select count(*) from claims_sample where root_claim_num="+claim_num_rec)
        all_rows=cur.fetchall()
        n_records=str(all_rows[0][0]).replace('None','0')
        if int(n_records)==0:
            denial_reason="Could not find claim with Claim Number "+claim_num_rec+", Please make sure you entered correct details "
            # print(denial_reason)
            return(denial_reason)
        elif int(n_records) > 0:
            cur.execute("select distinct denial_full_reasons,denial_description from claims_sample where root_claim_num="+claim_num_rec+" and claim_denial_ind='1'")
            all_rows=cur.fetchall()
            n_d_records=len(all_rows)
            if n_d_records > 0:
                denial_reason="Your claim is denied due to following reasons<br><ul>"
                s1=""
                for row in all_rows:                
                    s1=s1+"<li>"+"Denial Code "+row[0]+" with description as "+row[1]+"</li>"
                denial_reason=denial_reason+s1+"</ul>" 
                denial_reason=denial_reason+"!How can I resubmit my Claim!What's the processing time of my Claim" 
                # print(denial_reason)
                return(denial_reason)
            else:
                denial_reason="Your Claim is not denied"
                # print(denial_reason)
                return(denial_reason)
        conn.commit()
        conn.close()
    except:
        return "Sorry, Could not fetch you results at this time"

def get_resubmit_proc():

    try:
        # print("get_resubmit_proc")
        database = "claims.db"
        conn = create_connection(database)
        cur = conn.cursor()    
        cur.execute("select distinct abbreviated_final_category from claims_sample where abbreviated_final_category<>'?'")
        all_rows=cur.fetchall()    
        if len(all_rows) > 0:
            resubmit_proc="Please keep following things in check while resubmitting your Claim<br><ul>"
            s1=""
            for row in all_rows:
                s1=s1+"<li>"+row[0]+"</li>"
            resubmit_proc=resubmit_proc+s1+"</ul>"
            # print(resubmit_proc)
            return(resubmit_proc)
        conn.commit()
        conn.close()
    except:
        return "Sorry, Could not fetch you results at this time"

def get_adjustment_reason(value1):

    try:
        # print("get_adjustment_reason")
        database = "claims.db"
        claim_num_rec="'"+str(value1)+"'"
        # print(claim_num_rec)
        conn = create_connection(database)
        cur = conn.cursor()
        cur.execute("select count(*) from claims_sample where root_claim_num="+claim_num_rec)
        all_rows=cur.fetchall()
        n_records=str(all_rows[0][0]).replace('None','0')
        if int(n_records)==0:
            adj_reason="Could not find claim with Claim Number "+claim_num_rec+", Please make sure you entered correct details "
            # print(adj_reason)
            return(adj_reason)
        elif int(n_records) > 0:
            cur.execute("select distinct adjustment_reasons,adjustment_description from claims_sample where root_claim_num="+claim_num_rec+" and claim_adj_ind='1'")
            all_rows=cur.fetchall()
            n_d_records=len(all_rows)
            if n_d_records > 0:
                adj_reason="Your claim is adjusted due to following reasons<br><ul>"
                s1=""
                for row in all_rows:                
                    s1=s1+"<li>"+"Adjustment Code "+row[0]+" with description as "+row[1]+"</li>"
                adj_reason=adj_reason+s1+"</ul>" 
                adj_reason=adj_reason+"!What's the processing time of my Claim!What's the Adjsuted Amount!What's the amount paid towards claim" 
                # print(adj_reason)
                return(adj_reason)
            else:
                adj_reason="Your Claim is not Adjusted"
                # print(adj_reason)
                return(adj_reason)
        conn.commit()
        conn.close()
    except:
        return "Sorry, Could not fetch you results at this time"

def get_adjusted_amt(value1):
    try:
        # print("get_adjusted_amt")
        database = "claims.db"
        claim_num_rec="'"+str(value1)+"'"
        # print(claim_num_rec)
        conn = create_connection(database)
        cur = conn.cursor()
        cur.execute("select count(*) from claims_sample where root_claim_num="+claim_num_rec)
        all_rows=cur.fetchall()
        n_records=str(all_rows[0][0]).replace('None','0')
        if int(n_records)==0:
            adj_amt_paid="Could not find claim with Claim Number "+claim_num_rec+", Please make sure you entered correct details "
            # print(adj_amt_paid)
            return(adj_amt_paid)
        else:
            cur.execute("select count(*) from claims_sample where root_claim_num="+claim_num_rec+" and claim_adj_ind='1'")
            all_rows=cur.fetchall()
            n_d_records=len(all_rows)
            if n_d_records > 0:
                cur.execute("select round(sum(amt_paid),2) from claims_sample where root_claim_num="+claim_num_rec+" and claim_adj_ind='1'")
                paid_amt=(round(float(str((cur.fetchall())[0][0]).replace('None','0')),2))            
                cur.execute("select round(sum(amt_billed),2) from claims_sample where root_claim_num="+claim_num_rec+" and claim_adj_ind='1'")
                billed_amt=(round(float(str((cur.fetchall())[0][0]).replace('None','0')),2))
                adj_paid_amt=str(billed_amt-paid_amt)
                
                adj_amt_paid="An adjustment of "+str(adj_paid_amt)+" was made toward your claim while "+str(paid_amt)+" being paid for claim!Why was my Claim Adjusted!How much amount was paid after adjustments!What's the processing time of my claim"
                # print(adj_amt_paid)
                return(adj_amt_paid)
            else:
                adj_amt_paid="Your Claim is not Adjusted"
                # print(adj_amt_paid)
                return(adj_amt_paid)
        conn.commit()
        conn.close()
    except:
        return "Sorry, Could not fetch you results at this time"

def get_adj_amt_paid(value1):
    try:
        # print("get_adj_amt_paid")
        database = "claims.db"
        claim_num_rec="'"+str(value1)+"'"
        # print(claim_num_rec)
        conn = create_connection(database)
        cur = conn.cursor()
        # print(claim_num_rec)
        cur.execute("select count(*) from claims_sample where root_claim_num="+claim_num_rec)
        all_rows=cur.fetchall()
        # print(claim_num_rec)
        n_records=str(all_rows[0][0])
        if int(n_records)==0:
            adj_amt_paid="Could not find claim with Claim Number "+claim_num_rec+", Please make sure you entered correct details "
            # print(adj_amt_paid)
            return(adj_amt_paid)
        else:
            cur.execute("select count(*) from claims_sample where root_claim_num="+claim_num_rec+" and claim_adj_ind='1'")
            all_rows=cur.fetchall()
            n_d_records=len(all_rows)
            if n_d_records > 0:
                cur.execute("select round(sum(amt_paid),2) from claims_sample where root_claim_num="+claim_num_rec+" and claim_adj_ind='1'")
                paid_amt=(round(float(str((cur.fetchall())[0][0]).replace('None','0')),2))            
                cur.execute("select round(sum(amt_billed),2) from claims_sample where root_claim_num="+claim_num_rec+" and claim_adj_ind='1'")
                billed_amt=(round(float(str((cur.fetchall())[0][0]).replace('None','0')),2))
                adj_paid_amt=str(billed_amt-paid_amt)
                adj_amt_paid=str(paid_amt)+" was paid toward your claim while "+str(adj_paid_amt)+" being adjusted for claim!Why was my Claim Adjusted!How much amount was adjusted after adjustments!What's the processing time of my claim"
                # print(adj_amt_paid)
                return(adj_amt_paid)
            else:
                adj_amt_paid="Your Claim is not Adjusted"
                # print(adj_amt_paid)
                return(adj_amt_paid)
        conn.commit()
        conn.close()

    except Error as e:
        print(str(e))
        return "Sorry, Could not fetch you results at this time"

def get_received_claims(dt):
    print(str(dt))
    try:
        database = "claims.db"
        conn = create_connection(database)
        cur = conn.cursor()
        if len(dt)==2:
            qry=" received_date between "+ dt[0]+" and "+dt[1].split('}')[0]
            stmt="select count(distinct root_claim_num) from claims_sample where "+qry
        elif len(dt)==3:
            if len(dt[0])==0:
                day_qry="strftime('%d', received_date) IS NOT NULL"
            else:
                day_qry="strftime('%d', received_date) in "+str(dt[0]).replace('[','(').replace(']',')')
            if len(dt[1])==0:
                mon_qry="strftime('%m', received_date) IS NOT NULL"
            else:
                mon_qry="strftime('%m', received_date) in "+str(dt[1]).replace('[','(').replace(']',')')
            if len(dt[2])==0:
                yr_qry="strftime('%Y', received_date) IS NOT NULL"
            else:
                yr_qry="strftime('%Y', received_date) in "+str(dt[2]).replace('[','(').replace(']',')')
            stmt="select count(distinct root_claim_num) from claims_sample where "+yr_qry+" and "+mon_qry+" and "+day_qry    
        # print(stmt)    
        cur.execute(stmt)
        all_rows=cur.fetchall()        
        n_records=str(all_rows[0][0]).replace("None","0")
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
        # print(recvd_num)
        conn.commit()
        conn.close()
        return recvd_num

    except Error as e:
        print(str(e))
        return "Sorry, Could not fetch you results at this time"

def get_bill_amt_recvd(dt):
    print(str(dt))
    try:
        database = "claims.db"
        conn = create_connection(database)
        cur = conn.cursor()
        if len(dt)==2:
            qry=" received_date between "+ dt[0]+" and "+dt[1].split('}')[0]
            stmt="select round(sum(amt_billed),2) from claims_sample where "+qry
        elif len(dt)==3:
            if len(dt[0])==0:
                day_qry="strftime('%d', received_date) IS NOT NULL"
            else:
                day_qry="strftime('%d', received_date) in "+str(dt[0]).replace('[','(').replace(']',')')
            if len(dt[1])==0:
                mon_qry="strftime('%m', received_date) IS NOT NULL"
            else:
                mon_qry="strftime('%m', received_date) in "+str(dt[1]).replace('[','(').replace(']',')')
            if len(dt[2])==0:
                yr_qry="strftime('%Y', received_date) IS NOT NULL"
            else:
                yr_qry="strftime('%Y', received_date) in "+str(dt[2]).replace('[','(').replace(']',')')
            stmt="select round(sum(amt_billed),2) from claims_sample where "+yr_qry+" and "+mon_qry+" and "+day_qry    
        # print(stmt) 
        # stmt="select round(sum(amt_billed),2) from claims_sample where "+yr_qry+" and "+mon_qry+" and "+qtr_qry    
        # print(stmt)    
        cur.execute(stmt)
        all_rows=cur.fetchall()        
        n_records=str(all_rows[0][0]).replace("None","0")
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

        recvd_num="The total billed amount for the received claims "+dy_op+mon_op+yr_op+q_op+" is} "+str(n_records)
        # print(recvd_num)
        conn.commit()
        conn.close()
        return recvd_num        

    except Error as e:
        print(str(e))
        return "Sorry, Could not fetch you results at this time"

def get_paid_claims_recvd(dt):
    print(str(dt))
    try:
        database = "claims.db"
        conn = create_connection(database)
        cur = conn.cursor()
        if len(dt)==2:
            qry=" received_date between "+ dt[0]+" and "+dt[1].split('}')[0]+" and "+" paid_date between "+ dt[0]+" and "+dt[1].split('}')[0]
            stmt="select count(distinct root_claim_num) from claims_sample where "+qry
        elif len(dt)==3:
            if len(dt[0])==0:
                day_qry="strftime('%d', received_date) IS NOT NULL and strftime('%d', paid_date) IS NOT NULL"
            else:
                day_qry="strftime('%d', received_date) in "+str(dt[0]).replace('[','(').replace(']',')')+" and "+"strftime('%d', paid_date) in "+str(dt[0]).replace('[','(').replace(']',')')
            if len(dt[1])==0:
                mon_qry="strftime('%m', received_date) IS NOT NULL and strftime('%m', paid_date) IS NOT NULL"
            else:
                mon_qry="strftime('%m', received_date) in "+str(dt[1]).replace('[','(').replace(']',')')+" and "+"strftime('%m', paid_date) in "+str(dt[1]).replace('[','(').replace(']',')')
            if len(dt[2])==0:
                yr_qry="strftime('%Y', received_date) IS NOT NULL and strftime('%Y', paid_date) IS NOT NULL"
            else:
                yr_qry="strftime('%Y', received_date) in "+str(dt[2]).replace('[','(').replace(']',')')+" and "+"strftime('%Y', paid_date) in "+str(dt[2]).replace('[','(').replace(']',')')
            stmt="select count(distinct root_claim_num) from claims_sample where "+yr_qry+" and "+mon_qry+" and "+day_qry 
        
        # print(stmt)    
        cur.execute(stmt)
        all_rows=cur.fetchall()        
        n_records=str(all_rows[0][0]).replace("None","0")
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

        
        recvd_num=str(n_records)+" claims got paid out of "+ get_received_claims(dt).split('}')[0].strip(' ') +" claims that were received "+dy_op+mon_op+yr_op+q_op+"."
        # print(recvd_num)
        conn.commit()
        conn.close()
        return recvd_num

    except Error as e:
        print(str(e))
        return "Sorry, Could not fetch you results at this time"

def get_paid_amt_recvd(dt):
    print(str(dt))
    try:
        database = "claims.db"
        conn = create_connection(database)
        cur = conn.cursor()
        if len(dt)==2:
            qry=" received_date between "+ dt[0]+" and "+dt[1].split('}')[0]+" and "+" paid_date between "+ dt[0]+" and "+dt[1].split('}')[0]
            stmt="select  round(sum(amt_paid),2) from claims_sample where "+qry
        elif len(dt)==3:
            if len(dt[0])==0:
                day_qry="strftime('%d', received_date) IS NOT NULL and strftime('%d', paid_date) IS NOT NULL"
            else:
                day_qry="strftime('%d', received_date) in "+str(dt[0]).replace('[','(').replace(']',')')+" and "+"strftime('%d', paid_date) in "+str(dt[0]).replace('[','(').replace(']',')')
            if len(dt[1])==0:
                mon_qry="strftime('%m', received_date) IS NOT NULL and strftime('%m', paid_date) IS NOT NULL"
            else:
                mon_qry="strftime('%m', received_date) in "+str(dt[1]).replace('[','(').replace(']',')')+" and "+"strftime('%m', paid_date) in "+str(dt[1]).replace('[','(').replace(']',')')
            if len(dt[2])==0:
                yr_qry="strftime('%Y', received_date) IS NOT NULL and strftime('%Y', paid_date) IS NOT NULL"
            else:
                yr_qry="strftime('%Y', received_date) in "+str(dt[2]).replace('[','(').replace(']',')')+" and "+"strftime('%Y', paid_date) in "+str(dt[2]).replace('[','(').replace(']',')')
            stmt="select round(sum(amt_paid),2) from claims_sample where "+yr_qry+" and "+mon_qry+" and "+day_qry 
         
        # print(stmt)    
        cur.execute(stmt)
        all_rows=cur.fetchall()        
        n_records=str(all_rows[0][0]).replace("None","0")
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
        recvd_num="Out of the "+get_bill_amt_recvd(dt).split('}')[1].strip(' ') +" billed for the claims received,"+str(n_records)+" was paid "+dy_op+mon_op+yr_op+q_op+"."        
        # print(recvd_num)
        conn.commit()
        conn.close()
        return recvd_num
        

    except Error as e:
        print(str(e))
        return "Sorry, Could not fetch you results at this time"

def get_mode_submission_recvd(dt):
    print(str(dt))
    try:
        database = "claims.db"
        conn = create_connection(database)
        cur = conn.cursor()
        if len(dt)==2:
            qry=" received_date between "+ dt[0]+" and "+dt[1].split('}')[0]
            stmt="select distinct claim_receipt_type_cd from claims_sample"
            cur.execute(stmt)
            all_rows=cur.fetchall()
            unq_crtc=list() 
            for i in range(0,len(all_rows)):
                unq_crtc.append(all_rows[i][0])
            crtc_cnt=list()
            for i in range(0,len(unq_crtc)):
                stmt="select count(*) from claims_sample where "+qry+" and claim_receipt_type_cd='"+unq_crtc[i]+"'"
                cur.execute(stmt) 
                all_rows=cur.fetchall()        
                n_records=str(all_rows[0][0]).replace('None','0')
                crtc_cnt.append(str(unq_crtc[i])+"!"+str(n_records))             
        elif len(dt)==3:
            if len(dt[0])==0:
                day_qry="strftime('%d', received_date) IS NOT NULL"
            else:
                day_qry="strftime('%d', received_date) in "+str(dt[0]).replace('[','(').replace(']',')')
            if len(dt[1])==0:
                mon_qry="strftime('%m', received_date) IS NOT NULL"
            else:
                mon_qry="strftime('%m', received_date) in "+str(dt[1]).replace('[','(').replace(']',')')
            if len(dt[2])==0:
                yr_qry="strftime('%Y', received_date) IS NOT NULL"
            else:
                yr_qry="strftime('%Y', received_date) in "+str(dt[2]).replace('[','(').replace(']',')')
            stmt="select distinct claim_receipt_type_cd from claims_sample"
        
            cur.execute(stmt)
            all_rows=cur.fetchall()
            unq_crtc=list() 
            for i in range(0,len(all_rows)):
                unq_crtc.append(all_rows[i][0])
            crtc_cnt=list()
            for i in range(0,len(unq_crtc)):
                stmt="select count(*) from claims_sample where "+yr_qry+" and "+mon_qry+" and "+day_qry+" and claim_receipt_type_cd='"+unq_crtc[i]+"'"
                cur.execute(stmt) 
                all_rows=cur.fetchall()        
                n_records=str(all_rows[0][0]).replace('None','0')
                crtc_cnt.append(str(unq_crtc[i])+"!"+str(n_records)) 
        print(crtc_cnt)
        op_stmt=""
        for i in range(0,len(crtc_cnt)):
            op_stmt=crtc_cnt[i].split('!')[1]+" were submitted on "+crtc_cnt[i].split('!')[0]+", "+op_stmt
        print(op_stmt)
        
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

        recvd_num=op_stmt[0:len(op_stmt)-2]+" "+dy_op+mon_op+yr_op+q_op+"."
        # print(recvd_num)
        conn.commit()
        conn.close()
        return recvd_num
        
    except Error as e:
        print(str(e))
        return "Sorry, Could not fetch you results at this time"


def get_denied_claims(dt):
    print(str(dt))
    try:
        database = "claims.db"
        conn = create_connection(database)
        cur = conn.cursor()
        if len(dt)==2:
            qry=" paid_date between "+ dt[0]+" and "+dt[1].split('}')[0]
            # stmt="select count(distinct root_claim_num) from claims_sample where "+qry
            stmt1="select distinct root_claim_num from claims_sample where claim_denial_ind='1' and "+qry
            stmt2="select distinct root_claim_num from claims_sample where claim_denial_ind='0' and "+qry
            stmt3=stmt1+" except "+stmt2
            stmt4="select count(*) from claims_sample where root_claim_num in("+stmt3+") and "+qry
        elif len(dt)==3:
            if len(dt[0])==0:
                day_qry="strftime('%d', paid_date) IS NOT NULL"
            else:
                day_qry="strftime('%d', paid_date) in "+str(dt[0]).replace('[','(').replace(']',')')
            if len(dt[1])==0:
                mon_qry="strftime('%m', paid_date) IS NOT NULL"
            else:
                mon_qry="strftime('%m', paid_date) in "+str(dt[1]).replace('[','(').replace(']',')')
            if len(dt[2])==0:
                yr_qry="strftime('%Y', paid_date) IS NOT NULL"
            else:
                yr_qry="strftime('%Y', paid_date) in "+str(dt[2]).replace('[','(').replace(']',')')
            # stmt="select count(distinct root_claim_num) from claims_sample where "+yr_qry+" and "+mon_qry+" and "+day_qry   
            stmt1="select distinct root_claim_num from claims_sample where claim_denial_ind='1' and "+yr_qry+" and "+mon_qry+" and "+day_qry    
            stmt2="select distinct root_claim_num from claims_sample where claim_denial_ind='0' and "+yr_qry+" and "+mon_qry+" and "+day_qry    
            stmt3=stmt1+" except "+stmt2
            stmt4="select count(*) from claims_sample where root_claim_num in("+stmt3+") and "+yr_qry+" and "+mon_qry+" and "+day_qry    
        cur.execute(stmt4)
        all_rows=cur.fetchall()
        count=(str((all_rows[0][0]))).replace("None","0")
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

        recvd_num=str(count)+" claims were denied "+dy_op+mon_op+yr_op+q_op+"."
        # print(recvd_num)
        conn.commit()
        conn.close()
        return recvd_num
        
    except Error as e:
        print(str(e))
        return "Sorry,Could not fetch you results at this time"

def get_bill_amt_dend(dt):
    print(str(dt))
    try:
        database = "claims.db"
        conn = create_connection(database)
        cur = conn.cursor()
        if len(dt)==2:
            qry=" paid_date between "+ dt[0]+" and "+dt[1].split('}')[0]
            # stmt="select count(distinct root_claim_num) from claims_sample where "+qry
            stmt1="select distinct root_claim_num from claims_sample where claim_denial_ind='1' and "+qry
            stmt2="select distinct root_claim_num from claims_sample where claim_denial_ind='0' and "+qry
            stmt3=stmt1+" except "+stmt2
            stmt4="select round(sum(amt_billed),2) from claims_sample where root_claim_num in("+stmt3+") and "+qry
        elif len(dt)==3:
            if len(dt[0])==0:
                day_qry="strftime('%d', paid_date) IS NOT NULL"
            else:
                day_qry="strftime('%d', paid_date) in "+str(dt[0]).replace('[','(').replace(']',')')
            if len(dt[1])==0:
                mon_qry="strftime('%m', paid_date) IS NOT NULL"
            else:
                mon_qry="strftime('%m', paid_date) in "+str(dt[1]).replace('[','(').replace(']',')')
            if len(dt[2])==0:
                yr_qry="strftime('%Y', paid_date) IS NOT NULL"
            else:
                yr_qry="strftime('%Y', paid_date) in "+str(dt[2]).replace('[','(').replace(']',')')
            # stmt="select count(distinct root_claim_num) from claims_sample where "+yr_qry+" and "+mon_qry+" and "+day_qry   
            stmt1="select distinct root_claim_num from claims_sample where claim_denial_ind='1' and "+yr_qry+" and "+mon_qry+" and "+day_qry    
            stmt2="select distinct root_claim_num from claims_sample where claim_denial_ind='0' and "+yr_qry+" and "+mon_qry+" and "+day_qry    
            stmt3=stmt1+" except "+stmt2
            stmt4="select round(sum(amt_billed),2) from claims_sample where root_claim_num in("+stmt3+") and "+yr_qry+" and "+mon_qry+" and "+day_qry    
        cur.execute(stmt4)
        all_rows=cur.fetchall()
        count=(str((all_rows[0][0]))).replace("None","0")
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

        recvd_num="The total billed amount for the denied claims was "+str(count)+" "+dy_op+mon_op+yr_op+q_op+"."
        # print(recvd_num)
        conn.commit()
        conn.close()
        return recvd_num
        

    except Error as e:
        print(str(e))
        return "Sorry, Could not fetch you results at this time"

def get_mode_submission_dend(dt):
    print(str(dt))
    try:
        database = "claims.db"
        conn = create_connection(database)
        cur = conn.cursor()
        crtc_cnt=list()
        if len(dt)==2:
            qry=" paid_date between "+ dt[0]+" and "+dt[1].split('}')[0]
            stmt="select distinct claim_receipt_type_cd from claims_sample"
            cur.execute(stmt)
            all_rows=cur.fetchall()
            unq_crtc=list() 
            for i in range(0,len(all_rows)):
                unq_crtc.append(all_rows[i][0])
            crtc_cnt=list()
            for i in range(0,len(unq_crtc)):
                stmt1="select distinct root_claim_num from claims_sample where claim_denial_ind='1' and "+qry
                stmt2="select distinct root_claim_num from claims_sample where claim_denial_ind='0' and "+qry    
                stmt3=stmt1+" except "+stmt2            
                stmt="select count(*) from claims_sample where root_claim_num in("+stmt3+") and "+qry+" and claim_receipt_type_cd='"+unq_crtc[i]+"'"
                cur.execute(stmt) 
                all_rows=cur.fetchall()        
                n_records=str(all_rows[0][0]).replace('None','0')
                crtc_cnt.append(str(unq_crtc[i])+"!"+str(n_records)) 
        elif len(dt)==3:
            if len(dt[0])==0:
                day_qry="strftime('%d', paid_date) IS NOT NULL"
            else:
                day_qry="strftime('%d', paid_date) in "+str(dt[0]).replace('[','(').replace(']',')')
            if len(dt[1])==0:
                mon_qry="strftime('%m', paid_date) IS NOT NULL"
            else:
                mon_qry="strftime('%m', paid_date) in "+str(dt[1]).replace('[','(').replace(']',')')
            if len(dt[2])==0:
                yr_qry="strftime('%Y', paid_date) IS NOT NULL"
            else:
                yr_qry="strftime('%Y', paid_date) in "+str(dt[2]).replace('[','(').replace(']',')')
              
            stmt="select distinct claim_receipt_type_cd from claims_sample"
            cur.execute(stmt)
            all_rows=cur.fetchall()
            unq_crtc=list() 
            for i in range(0,len(all_rows)):
                unq_crtc.append(all_rows[i][0])
            crtc_cnt=list()
            for i in range(0,len(unq_crtc)):
                stmt1="select distinct root_claim_num from claims_sample where claim_denial_ind='1' and "+yr_qry+" and "+mon_qry+" and "+day_qry    
                stmt2="select distinct root_claim_num from claims_sample where claim_denial_ind='0' and "+yr_qry+" and "+mon_qry+" and "+day_qry    
                stmt3=stmt1+" except "+stmt2            
                stmt="select count(*) from claims_sample where root_claim_num in("+stmt3+") and "+yr_qry+" and "+mon_qry+" and "+day_qry+" and claim_receipt_type_cd='"+unq_crtc[i]+"'"
                cur.execute(stmt) 
                all_rows=cur.fetchall()        
                n_records=str(all_rows[0][0]).replace('None','0')
                crtc_cnt.append(str(unq_crtc[i])+"!"+str(n_records)) 
        op_stmt=""
        for i in range(0,len(crtc_cnt)):
            op_stmt=crtc_cnt[i].split('!')[1]+" were submitted on "+crtc_cnt[i].split('!')[0]+", "+op_stmt

        
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

        recvd_num=op_stmt[0:len(op_stmt)-2]+" "+dy_op+mon_op+yr_op+q_op+"."
        # print(recvd_num)
        conn.commit()
        conn.close()
        return recvd_num
        

    except Error as e:
        print(str(e))
        return "Sorry, Could not fetch you results at this time"

def get_partial_dend_claims(dt):
    print(str(dt))
    try:
        database = "claims.db"
        conn = create_connection(database)
        cur = conn.cursor()
        if len(dt)==2:
            qry=" paid_date between "+ dt[0]+" and "+dt[1].split('}')[0]
            # stmt="select count(distinct root_claim_num) from claims_sample where "+qry
            stmt1="select distinct root_claim_num from claims_sample where claim_denial_ind='1' and "+qry
            stmt2="select distinct root_claim_num from claims_sample where claim_denial_ind='0' and "+qry
            stmt3=stmt1+" intersect "+stmt2
            stmt4="select count(*) from claims_sample where root_claim_num in("+stmt3+") and "+qry
        elif len(dt)==3:
            if len(dt[0])==0:
                day_qry="strftime('%d', paid_date) IS NOT NULL"
            else:
                day_qry="strftime('%d', paid_date) in "+str(dt[0]).replace('[','(').replace(']',')')
            if len(dt[1])==0:
                mon_qry="strftime('%m', paid_date) IS NOT NULL"
            else:
                mon_qry="strftime('%m', paid_date) in "+str(dt[1]).replace('[','(').replace(']',')')
            if len(dt[2])==0:
                yr_qry="strftime('%Y', paid_date) IS NOT NULL"
            else:
                yr_qry="strftime('%Y', paid_date) in "+str(dt[2]).replace('[','(').replace(']',')')
            # stmt="select count(distinct root_claim_num) from claims_sample where "+yr_qry+" and "+mon_qry+" and "+day_qry   
            stmt1="select distinct root_claim_num from claims_sample where claim_denial_ind='1' and "+yr_qry+" and "+mon_qry+" and "+day_qry    
            stmt2="select distinct root_claim_num from claims_sample where claim_denial_ind='0' and "+yr_qry+" and "+mon_qry+" and "+day_qry    
            stmt3=stmt1+" intersect "+stmt2
            stmt4="select count(*) from claims_sample where root_claim_num in("+stmt3+") and "+yr_qry+" and "+mon_qry+" and "+day_qry    
        cur.execute(stmt4)
        all_rows=cur.fetchall()
        count=(str((all_rows[0][0]))).replace('None','0')
        
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

        recvd_num=str(count)+" claims were partially denied "+dy_op+mon_op+yr_op+q_op+"."
        # print(recvd_num)
        conn.commit()
        conn.close()
        return recvd_num

    except Error as e:
        print(str(e))
        return "Sorry, Could not fetch you results at this time"

def get_bill_amt_partial_dend(dt):
    print(str(dt))
    try:
        database = "claims.db"
        conn = create_connection(database)
        cur = conn.cursor()
        if len(dt)==2:
            qry=" paid_date between "+ dt[0]+" and "+dt[1].split('}')[0]
            # stmt="select count(distinct root_claim_num) from claims_sample where "+qry
            stmt1="select distinct root_claim_num from claims_sample where claim_denial_ind='1' and "+qry
            stmt2="select distinct root_claim_num from claims_sample where claim_denial_ind='0' and "+qry
            stmt3=stmt1+" intersect "+stmt2
            stmt4="select round(sum(amt_billed),2) from claims_sample where root_claim_num in("+stmt3+") and "+qry
        elif len(dt)==3:
            if len(dt[0])==0:
                day_qry="strftime('%d', paid_date) IS NOT NULL"
            else:
                day_qry="strftime('%d', paid_date) in "+str(dt[0]).replace('[','(').replace(']',')')
            if len(dt[1])==0:
                mon_qry="strftime('%m', paid_date) IS NOT NULL"
            else:
                mon_qry="strftime('%m', paid_date) in "+str(dt[1]).replace('[','(').replace(']',')')
            if len(dt[2])==0:
                yr_qry="strftime('%Y', paid_date) IS NOT NULL"
            else:
                yr_qry="strftime('%Y', paid_date) in "+str(dt[2]).replace('[','(').replace(']',')')
            # stmt="select count(distinct root_claim_num) from claims_sample where "+yr_qry+" and "+mon_qry+" and "+day_qry   
            stmt1="select distinct root_claim_num from claims_sample where claim_denial_ind='1' and "+yr_qry+" and "+mon_qry+" and "+day_qry    
            stmt2="select distinct root_claim_num from claims_sample where claim_denial_ind='0' and "+yr_qry+" and "+mon_qry+" and "+day_qry    
            stmt3=stmt1+" intersect "+stmt2
            stmt4="select round(sum(amt_billed),2) from claims_sample where root_claim_num in("+stmt3+") and "+yr_qry+" and "+mon_qry+" and "+day_qry   
        
        cur.execute(stmt4)
        all_rows=cur.fetchall()
        count=(str((all_rows[0][0]))).replace('None','0')
        
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
            dy_op=""
        recvd_num="The total billed amount for the partial denied claims was "+str(count)+" "+dy_op+mon_op+yr_op+q_op+"."
        # print(recvd_num)
        conn.commit()
        conn.close()
        return recvd_num
        

    except Error as e:
        print(str(e))
        return "Sorry, Could not fetch you results at this time"

def get_mode_submission_prtl_dend(dt):
    print(str(dt))
    try:
        database = "claims.db"
        conn = create_connection(database)
        cur = conn.cursor()
        crtc_cnt=list()
        if len(dt)==2:
            qry=" paid_date between "+ dt[0]+" and "+dt[1].split('}')[0]
            stmt="select distinct claim_receipt_type_cd from claims_sample"
            cur.execute(stmt)
            all_rows=cur.fetchall()
            unq_crtc=list() 
            for i in range(0,len(all_rows)):
                unq_crtc.append(all_rows[i][0])
            crtc_cnt=list()
            for i in range(0,len(unq_crtc)):
                stmt1="select distinct root_claim_num from claims_sample where claim_denial_ind='1' and "+qry
                stmt2="select distinct root_claim_num from claims_sample where claim_denial_ind='0' and "+qry    
                stmt3=stmt1+" intersect "+stmt2            
                stmt="select count(*) from claims_sample where root_claim_num in("+stmt3+") and "+qry+" and claim_receipt_type_cd='"+unq_crtc[i]+"'"
                cur.execute(stmt) 
                all_rows=cur.fetchall()        
                n_records=str(all_rows[0][0]).replace('None','0')
                crtc_cnt.append(str(unq_crtc[i])+"!"+str(n_records)) 
        elif len(dt)==3:
            if len(dt[0])==0:
                day_qry="strftime('%d', paid_date) IS NOT NULL"
            else:
                day_qry="strftime('%d', paid_date) in "+str(dt[0]).replace('[','(').replace(']',')')
            if len(dt[1])==0:
                mon_qry="strftime('%m', paid_date) IS NOT NULL"
            else:
                mon_qry="strftime('%m', paid_date) in "+str(dt[1]).replace('[','(').replace(']',')')
            if len(dt[2])==0:
                yr_qry="strftime('%Y', paid_date) IS NOT NULL"
            else:
                yr_qry="strftime('%Y', paid_date) in "+str(dt[2]).replace('[','(').replace(']',')')
              
            stmt="select distinct claim_receipt_type_cd from claims_sample"
            cur.execute(stmt)
            all_rows=cur.fetchall()
            unq_crtc=list() 
            for i in range(0,len(all_rows)):
                unq_crtc.append(all_rows[i][0])
            crtc_cnt=list()
            for i in range(0,len(unq_crtc)):
                stmt1="select distinct root_claim_num from claims_sample where claim_denial_ind='1' and "+yr_qry+" and "+mon_qry+" and "+day_qry    
                stmt2="select distinct root_claim_num from claims_sample where claim_denial_ind='0' and "+yr_qry+" and "+mon_qry+" and "+day_qry    
                stmt3=stmt1+" intersect "+stmt2            
                stmt="select count(*) from claims_sample where root_claim_num in("+stmt3+") and "+yr_qry+" and "+mon_qry+" and "+day_qry+" and claim_receipt_type_cd='"+unq_crtc[i]+"'"
                cur.execute(stmt) 
                all_rows=cur.fetchall()        
                n_records=str(all_rows[0][0]).replace('None','0')
                crtc_cnt.append(str(unq_crtc[i])+"!"+str(n_records)) 
        op_stmt=""
        for i in range(0,len(crtc_cnt)):
            op_stmt=crtc_cnt[i].split('!')[1]+" were submitted on "+crtc_cnt[i].split('!')[0]+", "+op_stmt

        
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

        recvd_num=op_stmt[0:len(op_stmt)-2]+" "+dy_op+mon_op+yr_op+q_op+"."
        # print(recvd_num)
        conn.commit()
        conn.close()
        return recvd_num
        

    except Error as e:
        print(str(e))
        return "Sorry, Could not fetch you results at this time"

def get_adjstd_claims(dt):
    print(str(dt))
    try:
        database = "claims.db"
        conn = create_connection(database)
        cur = conn.cursor()
        if len(dt)==2:
            qry=" paid_date between "+ dt[0]+" and "+dt[1].split('}')[0]
            # stmt="select count(distinct root_claim_num) from claims_sample where "+qry
            stmt1="select distinct root_claim_num from claims_sample where claim_adj_ind='1' and "+qry 
            stmt4="select count(*) from claims_sample where root_claim_num in("+stmt1+") and "+qry
        elif len(dt)==3:
            if len(dt[0])==0:
                day_qry="strftime('%d', paid_date) IS NOT NULL"
            else:
                day_qry="strftime('%d', paid_date) in "+str(dt[0]).replace('[','(').replace(']',')')
            if len(dt[1])==0:
                mon_qry="strftime('%m', paid_date) IS NOT NULL"
            else:
                mon_qry="strftime('%m', paid_date) in "+str(dt[1]).replace('[','(').replace(']',')')
            if len(dt[2])==0:
                yr_qry="strftime('%Y', paid_date) IS NOT NULL"
            else:
                yr_qry="strftime('%Y', paid_date) in "+str(dt[2]).replace('[','(').replace(']',')')
            # stmt="select count(distinct root_claim_num) from claims_sample where "+yr_qry+" and "+mon_qry+" and "+day_qry   
            stmt1="select distinct root_claim_num from claims_sample where claim_adj_ind='1' and "+yr_qry+" and "+mon_qry+" and "+day_qry                    
            stmt4="select count(*) from claims_sample where root_claim_num in("+stmt1+") and "+yr_qry+" and "+mon_qry+" and "+day_qry    
        
        cur.execute(stmt4)
        all_rows=cur.fetchall()
        count=(str((all_rows[0][0]))).replace('None','0')
        
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

        recvd_num=str(count)+" claims were adjusted "+dy_op+mon_op+yr_op+q_op+"."
        # print(recvd_num)
        conn.commit()
        conn.close()
        return recvd_num

    except Error as e:
        print(str(e))
        return "Sorry, Could not fetch you results at this time"

def get_bill_amt_adjstd(dt):
    print(str(dt))
    try:
        database = "claims.db"
        conn = create_connection(database)
        cur = conn.cursor()
        if len(dt)==2:
            qry=" paid_date between "+ dt[0]+" and "+dt[1].split('}')[0]
            # stmt="select count(distinct root_claim_num) from claims_sample where "+qry
            stmt1="select distinct root_claim_num from claims_sample where claim_adj_ind='1' and "+qry 
            stmt4="select sum(amt_billed) from claims_sample where root_claim_num in("+stmt1+") and "+qry
        elif len(dt)==3:
            if len(dt[0])==0:
                day_qry="strftime('%d', paid_date) IS NOT NULL"
            else:
                day_qry="strftime('%d', paid_date) in "+str(dt[0]).replace('[','(').replace(']',')')
            if len(dt[1])==0:
                mon_qry="strftime('%m', paid_date) IS NOT NULL"
            else:
                mon_qry="strftime('%m', paid_date) in "+str(dt[1]).replace('[','(').replace(']',')')
            if len(dt[2])==0:
                yr_qry="strftime('%Y', paid_date) IS NOT NULL"
            else:
                yr_qry="strftime('%Y', paid_date) in "+str(dt[2]).replace('[','(').replace(']',')')
            # stmt="select count(distinct root_claim_num) from claims_sample where "+yr_qry+" and "+mon_qry+" and "+day_qry   
            stmt1="select distinct root_claim_num from claims_sample where claim_adj_ind='1' and "+yr_qry+" and "+mon_qry+" and "+day_qry                    
            stmt4="select sum(amt_billed) from claims_sample where root_claim_num in("+stmt1+") and "+yr_qry+" and "+mon_qry+" and "+day_qry           
        
        cur.execute(stmt4)
        all_rows=cur.fetchall()
        count=(str((all_rows[0][0]))).replace('None','0')
        
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

        recvd_num="The total billed amount for adjusted  claims was "+str(count)+" "+dy_op+mon_op+yr_op+q_op+"."
        # print(recvd_num)
        return recvd_num
        conn.commit()
        conn.close()

    except Error as e:
        print(str(e))
        return "Sorry, Could not fetch you results at this time"

def get_paid_amt_adjstd(dt):
    print(str(dt))
    try:
        database = "claims.db"
        conn = create_connection(database)
        cur = conn.cursor()
        if len(dt)==2:
            qry=" paid_date between "+ dt[0]+" and "+dt[1].split('}')[0]
            # stmt="select count(distinct root_claim_num) from claims_sample where "+qry
            stmt1="select distinct root_claim_num from claims_sample where claim_adj_ind='1' and "+qry 
            stmt4="select sum(amt_paid) from claims_sample where root_claim_num in("+stmt1+") and "+qry
        elif len(dt)==3:
            if len(dt[0])==0:
                day_qry="strftime('%d', paid_date) IS NOT NULL"
            else:
                day_qry="strftime('%d', paid_date) in "+str(dt[0]).replace('[','(').replace(']',')')
            if len(dt[1])==0:
                mon_qry="strftime('%m', paid_date) IS NOT NULL"
            else:
                mon_qry="strftime('%m', paid_date) in "+str(dt[1]).replace('[','(').replace(']',')')
            if len(dt[2])==0:
                yr_qry="strftime('%Y', paid_date) IS NOT NULL"
            else:
                yr_qry="strftime('%Y', paid_date) in "+str(dt[2]).replace('[','(').replace(']',')')
            # stmt="select count(distinct root_claim_num) from claims_sample where "+yr_qry+" and "+mon_qry+" and "+day_qry   
            stmt1="select distinct root_claim_num from claims_sample where claim_adj_ind='1' and "+yr_qry+" and "+mon_qry+" and "+day_qry                    
            stmt4="select sum(amt_paid) from claims_sample where root_claim_num in("+stmt1+") and "+yr_qry+" and "+mon_qry+" and "+day_qry           
        
        cur.execute(stmt4)
        all_rows=cur.fetchall()
        count=(str((all_rows[0][0]))).replace('None','0')
        
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

        recvd_num="The total paid amount for adjusted  claims was "+str(count)+" "+dy_op+mon_op+yr_op+q_op+"."
        # print(recvd_num)
        conn.commit()
        conn.close()
        return recvd_num
        

    except Error as e:
        print(str(e))
        return "Sorry, Could not fetch you results at this time"

def get_adj_amt_adjstd(dt):
    print(str(dt))
    try:
        database = "claims.db"
        conn = create_connection(database)
        cur = conn.cursor()
        if len(dt)==2:
            qry=" paid_date between "+ dt[0]+" and "+dt[1].split('}')[0]
            stmt1="select distinct root_claim_num from claims_sample where claim_adj_ind='1' and "+qry
            stmt4="select round(sum(amt_billed),2) from claims_sample where root_claim_num in("+stmt1+") and "+qry
            cur.execute(stmt4)
            all_rows=cur.fetchall()
            count=float(str((all_rows[0][0])).replace('None','0'))
            stmt4="select round(sum(amt_paid),2) from claims_sample where root_claim_num in("+stmt1+") and "+qry
            cur.execute(stmt4)
            all_rows=cur.fetchall()
            count1=float(str((all_rows[0][0])).replace('None','0'))
            count=count-count1
        elif len(dt)==3:
            if len(dt[0])==0:
                day_qry="strftime('%d', paid_date) IS NOT NULL"
            else:
                day_qry="strftime('%d', paid_date) in "+str(dt[0]).replace('[','(').replace(']',')')
            if len(dt[1])==0:
                mon_qry="strftime('%m', paid_date) IS NOT NULL"
            else:
                mon_qry="strftime('%m', paid_date) in "+str(dt[1]).replace('[','(').replace(']',')')
            if len(dt[2])==0:
                yr_qry="strftime('%Y', paid_date) IS NOT NULL"
            else:
                yr_qry="strftime('%Y', paid_date) in "+str(dt[2]).replace('[','(').replace(']',')')
            
            stmt1="select distinct root_claim_num from claims_sample where claim_adj_ind='1' and "+yr_qry+" and "+mon_qry+" and "+day_qry                    
            stmt4="select round(sum(amt_billed),2) from claims_sample where root_claim_num in("+stmt1+") and "+yr_qry+" and "+mon_qry+" and "+day_qry 
            cur.execute(stmt4)
            all_rows=cur.fetchall()
            count=float(str((all_rows[0][0])).replace('None','0'))
            stmt4="select round(sum(amt_paid),2) from claims_sample where root_claim_num in("+stmt1+") and "+yr_qry+" and "+mon_qry+" and "+day_qry 
            cur.execute(stmt4)
            all_rows=cur.fetchall()
            count1=float(str((all_rows[0][0])).replace('None','0'))
            count=count-count1
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

        recvd_num="The total adjusted amount for adjusted  claims was "+str(count)+" "+dy_op+mon_op+yr_op+q_op+"."
        # print(recvd_num)
        conn.commit()
        conn.close()
        return recvd_num       

    except Error as e:
        print(str(e))
        return "Sorry, Could not fetch you results at this time"


def get_mode_submission_adjstd(dt):
    print(str(dt))
    try:
        database = "claims.db"
        conn = create_connection(database)
        cur = conn.cursor()
        crtc_cnt=list()
        if len(dt)==2:
            qry=" paid_date between "+ dt[0]+" and "+dt[1].split('}')[0]
            stmt="select distinct claim_receipt_type_cd from claims_sample"
            cur.execute(stmt)
            all_rows=cur.fetchall()
            unq_crtc=list() 
            for i in range(0,len(all_rows)):
                unq_crtc.append(all_rows[i][0])
            crtc_cnt=list()
            for i in range(0,len(unq_crtc)):
                stmt1="select distinct root_claim_num from claims_sample where claim_adj_ind='1' and "+qry  
                stmt="select count(*) from claims_sample where root_claim_num in("+stmt1+") and "+qry+" and claim_receipt_type_cd='"+unq_crtc[i]+"'"
                cur.execute(stmt) 
                all_rows=cur.fetchall()        
                n_records=str(all_rows[0][0])
                crtc_cnt.append(str(unq_crtc[i])+"!"+str(n_records))
        elif len(dt)==3:
            if len(dt[0])==0:
                day_qry="strftime('%d', paid_date) IS NOT NULL"
            else:
                day_qry="strftime('%d', paid_date) in "+str(dt[0]).replace('[','(').replace(']',')')
            if len(dt[1])==0:
                mon_qry="strftime('%m', paid_date) IS NOT NULL"
            else:
                mon_qry="strftime('%m', paid_date) in "+str(dt[1]).replace('[','(').replace(']',')')
            if len(dt[2])==0:
                yr_qry="strftime('%Y', paid_date) IS NOT NULL"
            else:
                yr_qry="strftime('%Y', paid_date) in "+str(dt[2]).replace('[','(').replace(']',')')
             
            stmt="select distinct claim_receipt_type_cd from claims_sample"
            cur.execute(stmt)
            all_rows=cur.fetchall()
            unq_crtc=list() 
            for i in range(0,len(all_rows)):
                unq_crtc.append(all_rows[i][0])
            crtc_cnt=list()
            for i in range(0,len(unq_crtc)):
                stmt1="select distinct root_claim_num from claims_sample where claim_adj_ind='1' and "+yr_qry+" and "+mon_qry+" and "+day_qry            
                stmt="select count(*) from claims_sample where root_claim_num in("+stmt1+") and "+yr_qry+" and "+mon_qry+" and "+day_qry+" and claim_receipt_type_cd='"+unq_crtc[i]+"'"
                cur.execute(stmt) 
                all_rows=cur.fetchall()        
                n_records=str(all_rows[0][0])
                crtc_cnt.append(str(unq_crtc[i])+"!"+str(n_records)) 
        op_stmt=""
        for i in range(0,len(crtc_cnt)):
            op_stmt=crtc_cnt[i].split('!')[1]+" were submitted on "+crtc_cnt[i].split('!')[0]+", "+op_stmt

        
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

        recvd_num=op_stmt[0:len(op_stmt)-2]+" "+dy_op+mon_op+yr_op+q_op+"."
        # print(recvd_num)
        conn.commit()
        conn.close()
        return recvd_num        

    except Error as e:
        print(str(e))
        return "Sorry, Could not fetch you results at this time"

def get_high_dollar_claims(dt):
    print(str(dt))
    try:
        database = "claims.db"
        conn = create_connection(database)
        cur = conn.cursor()
        if len(dt)==2:
            qry=" received_date between "+ dt[0]+" and "+dt[1].split('}')[0]
            stmt="select count(distinct root_claim_num) from claims_sample where claim_high_dollar_paid_ind='1' and "+qry
        elif len(dt)==3:
            if len(dt[0])==0:
                day_qry="strftime('%d', received_date) IS NOT NULL"
            else:
                day_qry="strftime('%d', received_date) in "+str(dt[0]).replace('[','(').replace(']',')')
            if len(dt[1])==0:
                mon_qry="strftime('%m', received_date) IS NOT NULL"
            else:
                mon_qry="strftime('%m', received_date) in "+str(dt[1]).replace('[','(').replace(']',')')
            if len(dt[2])==0:
                yr_qry="strftime('%Y', received_date) IS NOT NULL"
            else:
                yr_qry="strftime('%Y', received_date) in "+str(dt[2]).replace('[','(').replace(']',')') 
            stmt="select count(distinct root_claim_num) from claims_sample where claim_high_dollar_paid_ind='1' and "+yr_qry+" and "+mon_qry+" and "+day_qry    
        # print(stmt)    
        cur.execute(stmt)
        all_rows=cur.fetchall()        
        n_records=str(all_rows[0][0])
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
        # print(recvd_num)
        conn.commit()
        conn.close()
        return recvd_num
        

    except Error as e:
        print(str(e))
        return "Sorry, Could not fetch you results at this time"

def get_bill_amt_hgh_dlr(dt):
    print(str(dt))
    try:
        database = "claims.db"
        conn = create_connection(database)
        cur = conn.cursor()
        if len(dt)==2:
            qry=" received_date between "+ dt[0]+" and "+dt[1].split('}')[0]
            stmt="select round(sum(amt_billed),2) from claims_sample where claim_high_dollar_paid_ind='1' and  "+qry
        elif len(dt)==3:
            if len(dt[0])==0:
                day_qry="strftime('%d', received_date) IS NOT NULL"
            else:
                day_qry="strftime('%d', received_date) in "+str(dt[0]).replace('[','(').replace(']',')')
            if len(dt[1])==0:
                mon_qry="strftime('%m', received_date) IS NOT NULL"
            else:
                mon_qry="strftime('%m', received_date) in "+str(dt[1]).replace('[','(').replace(']',')')
            if len(dt[2])==0:
                yr_qry="strftime('%Y', received_date) IS NOT NULL"
            else:
                yr_qry="strftime('%Y', received_date) in "+str(dt[2]).replace('[','(').replace(']',')')
            stmt="select round(sum(amt_billed),2) from claims_sample where claim_high_dollar_paid_ind='1' and  "+yr_qry+" and "+mon_qry+" and "+day_qry    
        
        # print(stmt)    
        cur.execute(stmt)
        all_rows=cur.fetchall()        
        n_records=str(all_rows[0][0]).replace("None","0")
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

        recvd_num="The total billed amount for high dollar claims "+dy_op+mon_op+yr_op+q_op+" is} "+str(n_records)
        # print(recvd_num)
        conn.commit()
        conn.close()
        return recvd_num       

    except Error as e:
        print(str(e))
        return "Sorry, Could not fetch you results at this time"

def get_paid_claims_hgh_dlr(dt):
    print(str(dt))
    try:
        database = "claims.db"
        conn = create_connection(database)
        cur = conn.cursor()
        if len(dt)==2:
            qry=" received_date between "+ dt[0]+" and "+dt[1].split('}')[0]+" and "+" paid_date between "+ dt[0]+" and "+dt[1].split('}')[0]
            stmt="select count(distinct root_claim_num) from claims_sample where claim_high_dollar_paid_ind='1' and  "+qry
        elif len(dt)==3:
            if len(dt[0])==0:
                day_qry="strftime('%d', received_date) IS NOT NULL and strftime('%d', paid_date) IS NOT NULL"
            else:
                day_qry="strftime('%d', received_date) in "+str(dt[0]).replace('[','(').replace(']',')')+" and "+"strftime('%d', paid_date) in "+str(dt[0]).replace('[','(').replace(']',')')
            if len(dt[1])==0:
                mon_qry="strftime('%m', received_date) IS NOT NULL and strftime('%m', paid_date) IS NOT NULL"
            else:
                mon_qry="strftime('%m', received_date) in "+str(dt[1]).replace('[','(').replace(']',')')+" and "+"strftime('%m', paid_date) in "+str(dt[1]).replace('[','(').replace(']',')')
            if len(dt[2])==0:
                yr_qry="strftime('%Y', received_date) IS NOT NULL and strftime('%Y', paid_date) IS NOT NULL"
            else:
                yr_qry="strftime('%Y', received_date) in "+str(dt[2]).replace('[','(').replace(']',')')+" and "+"strftime('%Y', paid_date) in "+str(dt[2]).replace('[','(').replace(']',')')
            stmt="select count(distinct root_claim_num) from claims_sample where claim_high_dollar_paid_ind='1' and  "+yr_qry+" and "+mon_qry+" and "+day_qry    
        
        # print(stmt)    
        cur.execute(stmt)
        all_rows=cur.fetchall()        
        n_records=str(all_rows[0][0]).replace("None","0")
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
        
        recvd_num=str(n_records)+" claims got paid out of "+ get_high_dollar_claims(dt).split('}')[0].strip(' ') +" claims that were received "+dy_op+mon_op+yr_op+q_op+"."
        # print(recvd_num)
        conn.commit()
        conn.close()
        return recvd_num        

    except Error as e:
        print(str(e))
        return "Sorry, Could not fetch you results at this time"

def get_paid_amt_hgh_dlr(dt):
    print(str(dt))
    try:
        database = "claims.db"
        conn = create_connection(database)
        cur = conn.cursor()
        if len(dt)==2:
            qry=" received_date between "+ dt[0]+" and "+dt[1].split('}')[0]+" and "+" paid_date between "+ dt[0]+" and "+dt[1].split('}')[0]
            stmt="select round(sum(amt_paid),2) from claims_sample where claim_high_dollar_paid_ind='1' and "+qry
        elif len(dt)==3:
            if len(dt[0])==0:
                day_qry="strftime('%d', received_date) IS NOT NULL and strftime('%d', paid_date) IS NOT NULL"
            else:
                day_qry="strftime('%d', received_date) in "+str(dt[0]).replace('[','(').replace(']',')')+" and "+"strftime('%d', paid_date) in "+str(dt[0]).replace('[','(').replace(']',')')
            if len(dt[1])==0:
                mon_qry="strftime('%m', received_date) IS NOT NULL and strftime('%m', paid_date) IS NOT NULL"
            else:
                mon_qry="strftime('%m', received_date) in "+str(dt[1]).replace('[','(').replace(']',')')+" and "+"strftime('%m', paid_date) in "+str(dt[1]).replace('[','(').replace(']',')')
            if len(dt[2])==0:
                yr_qry="strftime('%Y', received_date) IS NOT NULL and strftime('%Y', paid_date) IS NOT NULL"
            else:
                yr_qry="strftime('%Y', received_date) in "+str(dt[2]).replace('[','(').replace(']',')')+" and "+"strftime('%Y', paid_date) in "+str(dt[2]).replace('[','(').replace(']',')')
            stmt="select round(sum(amt_paid),2) from claims_sample where claim_high_dollar_paid_ind='1' and "+yr_qry+" and "+mon_qry+" and "+day_qry    
               
        # print(stmt)    
        cur.execute(stmt)
        all_rows=cur.fetchall()        
        n_records=str(all_rows[0][0]).replace("None","0")
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
        recvd_num="Out of the "+get_bill_amt_hgh_dlr(dt).split('}')[1].strip(' ') +" billed for the claims received,"+str(n_records)+" was paid "+dy_op+mon_op+yr_op+q_op+"."        
        # print(recvd_num)
        conn.commit()
        conn.close()        
        return recvd_num
    except Error as e:
        print(str(e))
        return "Sorry, Could not fetch you results at this time"

def get_mode_submsn_hgh_dlr(dt):
    print(str(dt))
    try:
        database = "claims.db"
        conn = create_connection(database)
        cur = conn.cursor()
        crtc_cnt=list()
        if len(dt)==2:
            qry=" received_date between "+ dt[0]+" and "+dt[1].split('}')[0]
            stmt="select distinct claim_receipt_type_cd from claims_sample"
            cur.execute(stmt)
            all_rows=cur.fetchall()
            unq_crtc=list() 
            for i in range(0,len(all_rows)):
                unq_crtc.append(all_rows[i][0])
            crtc_cnt=list()
            for i in range(0,len(unq_crtc)):
                stmt="select count(*) from claims_sample where claim_high_dollar_paid_ind='1' and "+qry+" and claim_receipt_type_cd='"+unq_crtc[i]+"'"
                cur.execute(stmt) 
                all_rows=cur.fetchall()        
                n_records=str(all_rows[0][0])
                crtc_cnt.append(str(unq_crtc[i])+"!"+str(n_records)) 
        elif len(dt)==3:
            if len(dt[0])==0:
                day_qry="strftime('%d', received_date) IS NOT NULL"
            else:
                day_qry="strftime('%d', received_date) in "+str(dt[0]).replace('[','(').replace(']',')')
            if len(dt[1])==0:
                mon_qry="strftime('%m', received_date) IS NOT NULL"
            else:
                mon_qry="strftime('%m', received_date) in "+str(dt[1]).replace('[','(').replace(']',')')
            if len(dt[2])==0:
                yr_qry="strftime('%Y', received_date) IS NOT NULL"
            else:
                yr_qry="strftime('%Y', received_date) in "+str(dt[2]).replace('[','(').replace(']',')')
            stmt="select distinct claim_receipt_type_cd from claims_sample"
        
            cur.execute(stmt)
            all_rows=cur.fetchall()
            unq_crtc=list() 
            for i in range(0,len(all_rows)):
                unq_crtc.append(all_rows[i][0])
            crtc_cnt=list()
            for i in range(0,len(unq_crtc)):
                stmt="select count(*) from claims_sample where claim_high_dollar_paid_ind='1' and "+yr_qry+" and "+mon_qry+" and "+day_qry+" and claim_receipt_type_cd='"+unq_crtc[i]+"'"
                cur.execute(stmt) 
                all_rows=cur.fetchall()        
                n_records=str(all_rows[0][0])
                crtc_cnt.append(str(unq_crtc[i])+"!"+str(n_records)) 
        op_stmt=""
        for i in range(0,len(crtc_cnt)):
            op_stmt=crtc_cnt[i].split('!')[1]+" were submitted on "+crtc_cnt[i].split('!')[0]+", "+op_stmt

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
        recvd_num=op_stmt[0:len(op_stmt)-2]+" "+dy_op+mon_op+yr_op+q_op+"."
        # print(recvd_num)
        conn.commit()
        conn.close()
        return recvd_num       

    except Error as e:
        print(str(e))
        return "Sorry, Could not fetch you results at this time"

def get_paid_amt_partial_dend(dt):
    print(str(dt))
    try:
        database = "claims.db"
        conn = create_connection(database)
        cur = conn.cursor()
        if len(dt)==2:
            qry=" paid_date between "+ dt[0]+" and "+dt[1].split('}')[0]
            # stmt="select count(distinct root_claim_num) from claims_sample where "+qry
            stmt1="select distinct root_claim_num from claims_sample where claim_denial_ind='1' and "+qry
            stmt2="select distinct root_claim_num from claims_sample where claim_denial_ind='0' and "+qry
            stmt3=stmt1+" intersect "+stmt2
            stmt4="select round(sum(amt_paid),2) from claims_sample where root_claim_num in("+stmt3+") and "+qry   
        elif len(dt)==3:
            if len(dt[0])==0:
                day_qry="strftime('%d', paid_date) IS NOT NULL"
            else:
                day_qry="strftime('%d', paid_date) in "+str(dt[0]).replace('[','(').replace(']',')')
            if len(dt[1])==0:
                mon_qry="strftime('%m', paid_date) IS NOT NULL"
            else:
                mon_qry="strftime('%m', paid_date) in "+str(dt[1]).replace('[','(').replace(']',')')
            if len(dt[2])==0:
                yr_qry="strftime('%Y', paid_date) IS NOT NULL"
            else:
                yr_qry="strftime('%Y', paid_date) in "+str(dt[2]).replace('[','(').replace(']',')')
            # stmt="select count(distinct root_claim_num) from claims_sample where "+yr_qry+" and "+mon_qry+" and "+day_qry   
            stmt1="select distinct root_claim_num from claims_sample where claim_denial_ind='1' and "+yr_qry+" and "+mon_qry+" and "+day_qry    
            stmt2="select distinct root_claim_num from claims_sample where claim_denial_ind='0' and "+yr_qry+" and "+mon_qry+" and "+day_qry    
            stmt3=stmt1+" intersect "+stmt2
            stmt4="select round(sum(amt_paid),2) from claims_sample where root_claim_num in("+stmt3+") and "+yr_qry+" and "+mon_qry+" and "+day_qry   
        
        cur.execute(stmt4)
        all_rows=cur.fetchall()
        count=(str((all_rows[0][0]))).replace('None','0')
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
        recvd_num="The total paid amount for the partial denied claims was "+str(count)+" "+dy_op+mon_op+yr_op+q_op+"."
        # print(recvd_num)
        conn.commit()
        conn.close()
        return recvd_num
        

    except Error as e:
        print(str(e))
        return "Sorry, Could not fetch you results at this time"

def main():

    # dt=[[], ['08'], ['2018']]
    dt=['2018-12-01', '2019-02-01}last two months']
    value1=7454175970
    print(get_status(value1))
    print(get_processing_time(value1))
    print(get_denial_reason(value1))
    print(get_resubmit_proc())
    print(get_adjustment_reason(value1))
    print(get_adjusted_amt(value1))
    print(get_adj_amt_paid(value1))
    print(get_received_claims(dt))
    print(get_bill_amt_recvd(dt))
    print(get_paid_claims_recvd(dt))
    print(get_paid_amt_recvd(dt))
    print(get_mode_submission_recvd(dt))
    print(get_denied_claims(dt))
    print(get_bill_amt_dend(dt))
    print(get_mode_submission_dend(dt))
    print(get_partial_dend_claims(dt))
    print(get_bill_amt_partial_dend(dt))
    print(get_mode_submission_prtl_dend(dt))
    print(get_adjstd_claims(dt))
    print(get_bill_amt_adjstd(dt))
    print(get_paid_amt_adjstd(dt))
    print(get_adj_amt_adjstd(dt))
    print(get_mode_submission_adjstd(dt))
    print(get_high_dollar_claims(dt))
    print(get_paid_claims_hgh_dlr(dt))
    print(get_paid_amt_hgh_dlr(dt))
    print(get_mode_submsn_hgh_dlr(dt))
    print(get_paid_amt_partial_dend(dt))

if __name__ == '__main__':
    main()






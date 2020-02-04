import sqlite3
from sqlite3 import Error
from datetime import datetime
import os

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
        
        print("get_status")
        database =u".\app\qualtrics\rasa\claims.db"        
        claim_num_rec="'"+str(value1)+"'"
        print(claim_num_rec)
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
            print("1")
            cur.execute("select round(sum(amt_billed),2) from claims_sample where root_claim_num="+claim_num_rec+"")
            denial_amt=str(round(float(str((cur.fetchall())[0][0])),2))
            print(denial_amt)
            cur.execute("select max(received_date) from claims_sample where root_claim_num="+claim_num_rec+" ")
            t=str(cur.fetchall()[0][0])        
            date_str=datetime(int(t.split('-')[0]),int(t.split('-')[1]),int((t.split('-')[2]).split(' ')[0]))
            t=(date_str.strftime('%Y-%b-%d'))
            status="Your claim has been completely denied for the amount "+denial_amt+" on "+t.split('-')[2]+"th of "+t.split('-')[1] +", "+t.split('-')[0]+"!Why was my Claim Denied!How can I resubmit my Claim!What's the time taken to process my claim"
            print(status)
            return(status)
        elif int(n_denial_recds)==0 and int(n_adj_recds)==0 and int(n_records)!=0:
            print("2")
            cur.execute("select round(sum(amt_paid),2) from claims_sample where root_claim_num="+claim_num_rec+"")
            paid_amt=str(round(float(str((cur.fetchall())[0][0])),2))
            print(paid_amt)
            cur.execute("select max(received_date) from claims_sample where root_claim_num="+claim_num_rec+" ")
            t=str(cur.fetchall()[0][0])        
            date_str=datetime(int(t.split('-')[0]),int(t.split('-')[1]),int((t.split('-')[2]).split(' ')[0]))
            t=(date_str.strftime('%Y-%b-%d'))
            status="Your claim has been completely paid for the amount "+paid_amt+" on "+t.split('-')[2]+"th of "+t.split('-')[1] +", "+t.split('-')[0]+"!What's the time taken to process my claim"
            print(status)
            return(status)
        elif int(n_denial_recds)==0 and int(n_adj_recds) > 0 and int(n_records)!=0:
            print("3")
            cur.execute("select round(sum(amt_paid),2) from claims_sample where root_claim_num="+claim_num_rec+"")
            paid_amt=str(round(float(str((cur.fetchall())[0][0])),2))
            print(paid_amt)
            cur.execute("select max(received_date) from claims_sample where root_claim_num="+claim_num_rec+" ")
            t=str(cur.fetchall()[0][0])        
            date_str=datetime(int(t.split('-')[0]),int(t.split('-')[1]),int((t.split('-')[2]).split(' ')[0]))
            t=(date_str.strftime('%Y-%b-%d'))##max received date
            status="Your claim has been paid for the amount "+paid_amt+" on "+t.split('-')[2]+"th of "+t.split('-')[1] +", "+t.split('-')[0]+" with adjustments!Why was my Claim Adjusted!What is Adjusted amount!What is the amount paid towards Claim!What's the time taken to process my claim"
            print(status)
            return(status)
        elif int(n_denial_recds)>0 and int(n_records)!=0:
            print("4")
            cur.execute("select round(sum(amt_paid),2) from claims_sample where root_claim_num="+claim_num_rec+"")
            paid_amt=(round(float(str((cur.fetchall())[0][0])),2))
            print(paid_amt)
            cur.execute("select round(sum(amt_billed),2) from claims_sample where root_claim_num="+claim_num_rec+"")
            billed_amt=(round(float(str((cur.fetchall())[0][0])),2))
            print(billed_amt)
            denied_amt=str(billed_amt-paid_amt)
            cur.execute("select max(received_date) from claims_sample where root_claim_num="+claim_num_rec+" ")
            t=str(cur.fetchall()[0][0])        
            date_str=datetime(int(t.split('-')[0]),int(t.split('-')[1]),int((t.split('-')[2]).split(' ')[0]))
            t=(date_str.strftime('%Y-%b-%d'))##max received date
            status="Your claim has been partially denied with "+str(denied_amt) +" being denied out of "+str(billed_amt)+" on "+t.split('-')[2]+"th of "+t.split('-')[1] +", "+t.split('-')[0]+"!Why is my claim partially denied!How can I resubmit my claim!What's the time taken to process my claim"
            print(status)
            return(status)
        elif int(n_records)==0:
            print("5")
            status="Could not find claim with Claim Number "+claim_num_rec+", Please make sure you entered correct details "
            print(status)
            return(status)
        else:
            print(str(n_records))
            print(str(n_adj_recds))
            print(str(n_denial_recds))

        conn.commit()
        conn.close()
    except Error as e:
        print(str(e))
        return "Sorry! Could not fetch you results at this time"

def get_processing_time(value1):

    try:
        print("get_processing_time")
        database = "claims.db"
        claim_num_rec="'"+str(value1)+"'"
        print(claim_num_rec)
        conn = create_connection(database)
        cur = conn.cursor()
        cur.execute("select count(*) from claims_sample where root_claim_num="+claim_num_rec)
        all_rows=cur.fetchall()
        n_records=str(all_rows[0][0])
        if int(n_records)==0:
            proc_time="Could not find claim with Claim Number "+claim_num_rec+", Please make sure you entered correct details "
            print(proc_time)
            return(proc_time)
        elif int(n_records)>0:
            cur.execute("select max(fromdatetopaiddate) from claims_sample where root_claim_num="+claim_num_rec)
            all_rows=cur.fetchall()
            n_p_days=str(all_rows[0][0])
            proc_time="End to End processing time for your claim is "+n_p_days+" days"##+"!Give me processing time for this period"
            cur.execute("select max(fromdatetoreceiveddate) from claims_sample where root_claim_num="+claim_num_rec)
            all_rows=cur.fetchall()
            n_p_days=str(all_rows[0][0])
            proc_time=proc_time+"\n Provider claim submission time for your claim is "+n_p_days+" days"
            cur.execute("select max(receiveddatetopaiddate) from claims_sample where root_claim_num="+claim_num_rec)
            all_rows=cur.fetchall()
            n_p_days=str(all_rows[0][0])
            proc_time=proc_time+"\n UHC Processing time for your claim is "+n_p_days+" days"
            print(proc_time)
            return(proc_time)
        
        conn.commit()
        conn.close()
    except:
        return "Sorry! Could not fetch you results at this time"

def get_denial_reason(value1):

    try:
        print("get_denial_reason")
        database = "claims.db"
        claim_num_rec="'"+str(value1)+"'"
        print(claim_num_rec)
        conn = create_connection(database)
        cur = conn.cursor()
        cur.execute("select count(*) from claims_sample where root_claim_num="+claim_num_rec)
        all_rows=cur.fetchall()
        n_records=str(all_rows[0][0])
        if int(n_records)==0:
            denial_reason="Could not find claim with Claim Number "+claim_num_rec+", Please make sure you entered correct details "
            print(denial_reason)
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
                print(denial_reason)
                return(denial_reason)
            else:
                denial_reason="Your Claim is not denied"
                print(denial_reason)
                return(denial_reason)
        conn.commit()
        conn.close()
    except:
        return "Sorry! Could not fetch you results at this time"

def get_resubmit_proc():

    try:
        print("get_resubmit_proc")
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
            print(resubmit_proc)
            return(resubmit_proc)
        conn.commit()
        conn.close()
    except:
        return "Sorry! Could not fetch you results at this time"

def get_adjustment_reason(value1):

    try:
        print("get_adjustment_reason")
        database = "claims.db"
        claim_num_rec="'"+str(value1)+"'"
        print(claim_num_rec)
        conn = create_connection(database)
        cur = conn.cursor()
        cur.execute("select count(*) from claims_sample where root_claim_num="+claim_num_rec)
        all_rows=cur.fetchall()
        n_records=str(all_rows[0][0])
        if int(n_records)==0:
            adj_reason="Could not find claim with Claim Number "+claim_num_rec+", Please make sure you entered correct details "
            print(adj_reason)
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
                print(adj_reason)
                return(adj_reason)
            else:
                adj_reason="Your Claim is not Adjusted"
                print(adj_reason)
                return(adj_reason)
        conn.commit()
        conn.close()
    except:
        return "Sorry! Could not fetch you results at this time"

def get_adjusted_amt(value1):
    try:
        print("get_adjusted_amt")
        database = "claims.db"
        claim_num_rec="'"+str(value1)+"'"
        print(claim_num_rec)
        conn = create_connection(database)
        cur = conn.cursor()
        cur.execute("select count(*) from claims_sample where root_claim_num="+claim_num_rec)
        all_rows=cur.fetchall()
        n_records=str(all_rows[0][0])
        if int(n_records)==0:
            adj_amt_paid="Could not find claim with Claim Number "+claim_num_rec+", Please make sure you entered correct details "
            print(adj_amt_paid)
            return(adj_amt_paid)
        else:
            cur.execute("select count(*) from claims_sample where root_claim_num="+claim_num_rec+" and claim_adj_ind='1'")
            all_rows=cur.fetchall()
            n_d_records=len(all_rows)
            if n_d_records > 0:
                cur.execute("select round(sum(amt_paid),2) from claims_sample where root_claim_num="+claim_num_rec+" and claim_adj_ind='1'")
                paid_amt=(round(float(str((cur.fetchall())[0][0])),2))            
                cur.execute("select round(sum(amt_billed),2) from claims_sample where root_claim_num="+claim_num_rec+" and claim_adj_ind='1'")
                billed_amt=(round(float(str((cur.fetchall())[0][0])),2))
                adj_paid_amt=str(billed_amt-paid_amt)
                
                adj_amt_paid="An adjustment of "+str(adj_paid_amt)+" was made toward your claim!Why was my Claim Adjusted!How much amount was paid after adjustments!What's the processing time of my claim"
                print(adj_amt_paid)
                return(adj_amt_paid)
            else:
                adj_amt_paid="Your Claim is not Adjusted"
                print(adj_amt_paid)
                return(adj_amt_paid)
        conn.commit()
        conn.close()
    except:
        return "Sorry! Could not fetch you results at this time"

def get_adj_amt_paid(value1):
    try:
        print("get_adj_amt_paid")
        database = "claims.db"
        claim_num_rec="'"+str(value1)+"'"
        print(claim_num_rec)
        conn = create_connection(database)
        cur = conn.cursor()
        print(claim_num_rec)
        cur.execute("select count(*) from claims_sample where root_claim_num="+claim_num_rec)
        all_rows=cur.fetchall()
        print(claim_num_rec)
        n_records=str(all_rows[0][0])
        if int(n_records)==0:
            adj_amt_paid="Could not find claim with Claim Number "+claim_num_rec+", Please make sure you entered correct details "
            print(adj_amt_paid)
            return(adj_amt_paid)
        else:
            cur.execute("select count(*) from claims_sample where root_claim_num="+claim_num_rec+" and claim_adj_ind='1'")
            all_rows=cur.fetchall()
            n_d_records=len(all_rows)
            if n_d_records > 0:
                cur.execute("select round(sum(amt_paid),2) from claims_sample where root_claim_num="+claim_num_rec+" and claim_adj_ind='1'")
                paid_amt=(round(float(str((cur.fetchall())[0][0]).replace('None','0')),2))
                adj_amt_paid=str(paid_amt)+" was paid for the claim after adjustments!Why was my Claim Adjusted!How much amount was adjusted!What's the processing time of my claim"
                print(adj_amt_paid)
                return(adj_amt_paid)
            else:
                adj_amt_paid="Your Claim is not Adjusted"
                print(adj_amt_paid)
                return(adj_amt_paid)
        conn.commit()
        conn.close()

    except Error as e:
        print(str(e))
        return "Sorry! Could not fetch you results at this time"

def get_received_claims(mon=0,yr=0,qtr=0):
    try:
        database = "claims.db"
        conn = create_connection(database)
        cur = conn.cursor()
        if mon > 12 or mon < 0:
            return "Please enter valid month  and Try again"
        if yr > datetime.now().year and yr < 0:
            return "Please enter valid year  and Try again"
        if qtr==1:
            qtr_qry="strftime('%m', received_date) in "+"('1','2','3')"
        elif qtr==2:
            qtr_qry="strftime('%m', received_date) in "+"('4','5','6')"
        elif qtr==3:
            qtr_qry="strftime('%m', received_date) in "+"('7','8','9')"
        elif qtr==4:
            qtr_qry="strftime('%m', received_date) in "+"('10','11','12')"
        elif qtr==0:
            qtr_qry="strftime('%m', received_date) IS NOT NULL "
        else:
            return "Please enter valid quarter  and Try again"
        if mon > 0:
            mon_qry="strftime('%m', received_date)="+"'"+str(mon)+"'"
        else:
            mon_qry="strftime('%m', received_date) IS NOT NULL "
        if yr > 0:
            yr_qry="strftime('%Y', received_date)="+"'"+str(yr)+"'"
        else:
            c_yr=datetime.now().year
            yr_qry="strftime('%Y', received_date)="+"'"+str(c_yr)+"'"  
        stmt="select count(distinct root_claim_num) from claims_sample where "+yr_qry+" and "+mon_qry+" and "+qtr_qry    
        print(stmt)    
        cur.execute(stmt)
        all_rows=cur.fetchall()        
        n_records=str(all_rows[0][0])
        if mon > 0:
            mon_op=" month of "+str(mon)+","
        else:
            mon_op=""
        if yr > 0:
            yr_op="year "+str(yr)
        else:
            yr_op="year "+str(datetime.now().year)
        if qtr > 0:
            qtr_op=str(qtr)+" quarter,"
        else:
            qtr_op=""

        recvd_num=str(n_records)+"} claims were received in "+mon_op+qtr_op+yr_op+"."
        print(recvd_num)
        return recvd_num
        conn.commit()
        conn.close()

    except Error as e:
        print(str(e))
        return "Sorry! Could not fetch you results at this time"

def get_bill_amt_recvd(mon=0,yr=0,qtr=0):
    try:
        database = "claims.db"
        conn = create_connection(database)
        cur = conn.cursor()
        if mon > 12 or mon < 0:
            return "Please enter valid month  and Try again"
        if yr > datetime.now().year and yr < 0:
            return "Please enter valid year  and Try again"
        if qtr==1:
            qtr_qry="strftime('%m', received_date) in "+"('1','2','3')"
        elif qtr==2:
            qtr_qry="strftime('%m', received_date) in "+"('4','5','6')"
        elif qtr==3:
            qtr_qry="strftime('%m', received_date) in "+"('7','8','9')"
        elif qtr==4:
            qtr_qry="strftime('%m', received_date) in "+"('10','11','12')"
        elif qtr==0:
            qtr_qry="strftime('%m', received_date) IS NOT NULL "
        else:
            return "Please enter valid quarter  and Try again"
        if mon > 0:
            mon_qry="strftime('%m', received_date)="+"'"+str(mon)+"'"
        else:
            mon_qry="strftime('%m', received_date) IS NOT NULL "
        if yr > 0:
            yr_qry="strftime('%Y', received_date)="+"'"+str(yr)+"'"
        else:
            c_yr=datetime.now().year
            yr_qry="strftime('%Y', received_date)="+"'"+str(c_yr)+"'"  
        stmt="select round(sum(amt_billed),2) from claims_sample where "+yr_qry+" and "+mon_qry+" and "+qtr_qry    
        print(stmt)    
        cur.execute(stmt)
        all_rows=cur.fetchall()        
        n_records=str(all_rows[0][0]).replace("None","0")
        if mon > 0:
            mon_op=" month of "+str(mon)+","
        else:
            mon_op=""
        if yr > 0:
            yr_op="year "+str(yr)
        else:
            yr_op="year "+str(datetime.now().year)
        if qtr > 0:
            qtr_op=str(qtr)+" quarter,"
        else:
            qtr_op=""

        recvd_num="The total billed amount for the received claims in "+mon_op+qtr_op+yr_op+" is} "+str(n_records)
        print(recvd_num)
        return recvd_num
        conn.commit()
        conn.close()

    except Error as e:
        print(str(e))
        return "Sorry! Could not fetch you results at this time"

def get_paid_claims_recvd(mon=0,yr=0,qtr=0):
    try:
        database = "claims.db"
        conn = create_connection(database)
        cur = conn.cursor()
        if mon > 12 or mon < 0:
            return "Please enter valid month  and Try again"
        if yr > datetime.now().year and yr < 0:
            return "Please enter valid year  and Try again"
        if qtr==1:
            qtr_qry="strftime('%m', received_date) in ('1','2','3') and strftime('%m', paid_date) in ('1','2','3') "
        elif qtr==2:
            qtr_qry="strftime('%m', received_date) in ('4','5','6') and strftime('%m', paid_date) in ('4','5','6') "
        elif qtr==3:
            qtr_qry="strftime('%m', received_date) in ('7','8','9') and strftime('%m', paid_date) in ('7','8','9')"
        elif qtr==4:
            qtr_qry="strftime('%m', received_date) in ('10','11','12') and strftime('%m', paid_date) in ('10','11','12') "
        elif qtr==0:
            qtr_qry="strftime('%m', received_date) IS NOT NULL "
        else:
            return "Please enter valid quarter  and Try again"
        if mon > 0:
            mon_qry="strftime('%m', received_date)="+"'"+str(mon)+"'"+" and "+"strftime('%m', paid_date)="+"'"+str(mon)+"'"
        else:
            mon_qry="strftime('%m', received_date) IS NOT NULL "+" and "+"strftime('%m', paid_date) IS NOT NULL "
        if yr > 0:
            yr_qry="strftime('%Y', received_date)="+"'"+str(yr)+"'"+" and "+"strftime('%Y', paid_date)="+"'"+str(yr)+"'"
        else:
            c_yr=datetime.now().year
            yr_qry="strftime('%Y', received_date)="+"'"+str(c_yr)+"'"+" and "+"strftime('%Y', paid_date)="+"'"+str(c_yr)+"'"  
        stmt="select count(distinct root_claim_num) from claims_sample where "+yr_qry+" and "+mon_qry+" and "+qtr_qry    
        print(stmt)    
        cur.execute(stmt)
        all_rows=cur.fetchall()        
        n_records=str(all_rows[0][0]).replace("None","0")
        if mon > 0:
            mon_op=" month of "+str(mon)+","
        else:
            mon_op=""
        if yr > 0:
            yr_op="year "+str(yr)
        else:
            yr_op="year "+str(datetime.now().year)
        if qtr > 0:
            qtr_op=str(qtr)+" quarter,"
        else:
            qtr_op=""
        
        recvd_num=str(n_records)+" claims got paid out of "+ get_received_claims(mon,yr,qtr).split('}')[0].strip(' ') +" claims that were received in "+mon_op+qtr_op+yr_op+"."
        print(recvd_num)
        return recvd_num
        conn.commit()
        conn.close()

    except Error as e:
        print(str(e))
        return "Sorry! Could not fetch you results at this time"

def get_paid_amt_recvd(mon=0,yr=0,qtr=0):
    try:
        database = "claims.db"
        conn = create_connection(database)
        cur = conn.cursor()
        if mon > 12 or mon < 0:
            return "Please enter valid month  and Try again"
        if yr > datetime.now().year and yr < 0:
            return "Please enter valid year  and Try again"
        if qtr==1:
            qtr_qry="strftime('%m', received_date) in ('1','2','3') and strftime('%m', paid_date) in ('1','2','3') "
        elif qtr==2:
            qtr_qry="strftime('%m', received_date) in ('4','5','6') and strftime('%m', paid_date) in ('4','5','6') "
        elif qtr==3:
            qtr_qry="strftime('%m', received_date) in ('7','8','9') and strftime('%m', paid_date) in ('7','8','9')"
        elif qtr==4:
            qtr_qry="strftime('%m', received_date) in ('10','11','12') and strftime('%m', paid_date) in ('10','11','12') "
        elif qtr==0:
            qtr_qry="strftime('%m', received_date) IS NOT NULL "
        else:
            return "Please enter valid quarter  and Try again"
        if mon > 0:
            mon_qry="strftime('%m', received_date)="+"'"+str(mon)+"'"+" and "+"strftime('%m', paid_date)="+"'"+str(mon)+"'"
        else:
            mon_qry="strftime('%m', received_date) IS NOT NULL "+" and "+"strftime('%m', paid_date) IS NOT NULL "
        if yr > 0:
            yr_qry="strftime('%Y', received_date)="+"'"+str(yr)+"'"+" and "+"strftime('%Y', paid_date)="+"'"+str(yr)+"'"
        else:
            c_yr=datetime.now().year
            yr_qry="strftime('%Y', received_date)="+"'"+str(c_yr)+"'"+" and "+"strftime('%Y', paid_date)="+"'"+str(c_yr)+"'"  
        stmt="select round(sum(amt_paid),2) from claims_sample where "+yr_qry+" and "+mon_qry+" and "+qtr_qry    
        print(stmt)    
        cur.execute(stmt)
        all_rows=cur.fetchall()        
        n_records=str(all_rows[0][0]).replace("None","0")
        if mon > 0:
            mon_op=" month of "+str(mon)+","
        else:
            mon_op=""
        if yr > 0:
            yr_op="year "+str(yr)
        else:
            yr_op="year "+str(datetime.now().year)
        if qtr > 0:
            qtr_op=str(qtr)+" quarter,"
        else:
            qtr_op=""
        recvd_num="Out of the "+get_bill_amt_recvd(mon,yr,qtr).split('}')[1].strip(' ') +" billed for the claims received,"+str(n_records)+" was paid in "+mon_op+qtr_op+yr_op+"."        
        print(recvd_num)
        return recvd_num
        conn.commit()
        conn.close()

    except Error as e:
        print(str(e))
        return "Sorry! Could not fetch you results at this time"

def get_mode_submission_recvd(mon=0,yr=0,qtr=0):
    try:
        database = "claims.db"
        conn = create_connection(database)
        cur = conn.cursor()
        if mon > 12 or mon < 0:
            return "Please enter valid month  and Try again"
        if yr > datetime.now().year and yr < 0:
            return "Please enter valid year  and Try again"
        if qtr==1:
            qtr_qry="strftime('%m', received_date) in "+"('1','2','3')"
        elif qtr==2:
            qtr_qry="strftime('%m', received_date) in "+"('4','5','6')"
        elif qtr==3:
            qtr_qry="strftime('%m', received_date) in "+"('7','8','9')"
        elif qtr==4:
            qtr_qry="strftime('%m', received_date) in "+"('10','11','12')"
        elif qtr==0:
            qtr_qry="strftime('%m', received_date) IS NOT NULL "
        else:
            return "Please enter valid quarter  and Try again"
        if mon > 0:
            mon_qry="strftime('%m', received_date)="+"'"+str(mon)+"'"
        else:
            mon_qry="strftime('%m', received_date) IS NOT NULL "
        if yr > 0:
            yr_qry="strftime('%Y', received_date)="+"'"+str(yr)+"'"
        else:
            c_yr=datetime.now().year
            yr_qry="strftime('%Y', received_date)="+"'"+str(c_yr)+"'"  
        stmt="select distinct claim_receipt_type_cd from claims_sample"
        cur.execute(stmt)
        all_rows=cur.fetchall()
        unq_crtc=list() 
        for i in range(0,len(all_rows)):
            unq_crtc.append(all_rows[i][0])
        crtc_cnt=list()
        for i in range(0,len(unq_crtc)):
            stmt="select count(*) from claims_sample where "+yr_qry+" and "+mon_qry+" and "+qtr_qry+" and claim_receipt_type_cd='"+unq_crtc[i]+"'"
            cur.execute(stmt) 
            all_rows=cur.fetchall()        
            n_records=str(all_rows[0][0])
            crtc_cnt.append(str(unq_crtc[i])+"!"+str(n_records)) 
        op_stmt=""
        for i in range(0,len(crtc_cnt)):
            op_stmt=crtc_cnt[i].split('!')[1]+" were submitted on "+crtc_cnt[i].split('!')[0]+", "+op_stmt

        
        if mon > 0:
            mon_op=" month of "+str(mon)+","
        else:
            mon_op=""
        if yr > 0:
            yr_op="year "+str(yr)
        else:
            yr_op="year "+str(datetime.now().year)
        if qtr > 0:
            qtr_op=str(qtr)+" quarter,"
        else:
            qtr_op=""

        recvd_num=op_stmt[0:len(op_stmt)-2]+" in "+mon_op+qtr_op+yr_op+"."
        print(recvd_num)
        return recvd_num
        conn.commit()
        conn.close()

    except Error as e:
        print(str(e))
        return "Sorry! Could not fetch you results at this time"

def get_denied_claims(mon=0,yr=0,qtr=0):
    try:
        database = "claims.db"
        conn = create_connection(database)
        cur = conn.cursor()
        if mon > 12 or mon < 0:
            return "Please enter valid month  and Try again"
        if yr > datetime.now().year and yr < 0:
            return "Please enter valid year  and Try again"
        if qtr==1:
            qtr_qry="strftime('%m', paid_date) in "+"('1','2','3')"
        elif qtr==2:
            qtr_qry="strftime('%m', paid_date) in "+"('4','5','6')"
        elif qtr==3:
            qtr_qry="strftime('%m', paid_date) in "+"('7','8','9')"
        elif qtr==4:
            qtr_qry="strftime('%m', paid_date) in "+"('10','11','12')"
        elif qtr==0:
            qtr_qry="strftime('%m', paid_date) IS NOT NULL "
        else:
            return "Please enter valid quarter  and Try again"
        if mon > 0:
            mon_qry="strftime('%m', paid_date)="+"'"+str(mon)+"'"
        else:
            mon_qry="strftime('%m', paid_date) IS NOT NULL "
        if yr > 0:
            yr_qry="strftime('%Y', paid_date)="+"'"+str(yr)+"'"
        else:
            c_yr=datetime.now().year
            yr_qry="strftime('%Y', paid_date)="+"'"+str(c_yr)+"'"
        ################## JUNK  
        # stmt="select * from claims_sample where "+yr_qry+" and "+mon_qry+" and "+qtr_qry+" and claim_denial_ind='1'"    
        # cur.execute(stmt)
        # all_rows=cur.fetchall()   
        # count=0
        # den_claim_lst=list()   
        # for i in range(0,len(all_rows)):
        #     if all_rows[i][0] not in den_claim_lst:
        #         if str(get_status(all_rows[i][0]).split('}')[0])=='1':
        #             count=count+1
        ################## JUNK
        # where "+yr_qry+" and "+mon_qry+" and "+qtr_qry    
        stmt1="select distinct root_claim_num from claims_sample where claim_denial_ind='1' and "+yr_qry+" and "+mon_qry+" and "+qtr_qry    
        stmt2="select distinct root_claim_num from claims_sample where claim_denial_ind='0' and "+yr_qry+" and "+mon_qry+" and "+qtr_qry    
        stmt3=stmt1+" except "+stmt2
        stmt4="select count(*) from claims_sample where root_claim_num in("+stmt3+") and "+yr_qry+" and "+mon_qry+" and "+qtr_qry    
        cur.execute(stmt4)
        all_rows=cur.fetchall()
        count=(str((all_rows[0][0])))
        
        if mon > 0:
            mon_op=" month of "+str(mon)+","
        else:
            mon_op=""
        if yr > 0:
            yr_op="year "+str(yr)
        else:
            yr_op="year "+str(datetime.now().year)
        if qtr > 0:
            qtr_op=str(qtr)+" quarter,"
        else:
            qtr_op=""

        recvd_num=str(count)+" claims were denied in "+mon_op+qtr_op+yr_op+"."
        print(recvd_num)
        return recvd_num
        conn.commit()
        conn.close()

    except Error as e:
        print(str(e))
        return "Sorry! Could not fetch you results at this time"

def get_bill_amt_dend(mon=0,yr=0,qtr=0):
    try:
        database = "claims.db"
        conn = create_connection(database)
        cur = conn.cursor()
        if mon > 12 or mon < 0:
            return "Please enter valid month  and Try again"
        if yr > datetime.now().year and yr < 0:
            return "Please enter valid year  and Try again"
        if qtr==1:
            qtr_qry="strftime('%m', paid_date) in "+"('1','2','3')"
        elif qtr==2:
            qtr_qry="strftime('%m', paid_date) in "+"('4','5','6')"
        elif qtr==3:
            qtr_qry="strftime('%m', paid_date) in "+"('7','8','9')"
        elif qtr==4:
            qtr_qry="strftime('%m', paid_date) in "+"('10','11','12')"
        elif qtr==0:
            qtr_qry="strftime('%m', paid_date) IS NOT NULL "
        else:
            return "Please enter valid quarter  and Try again"
        if mon > 0:
            mon_qry="strftime('%m', paid_date)="+"'"+str(mon)+"'"
        else:
            mon_qry="strftime('%m', paid_date) IS NOT NULL "
        if yr > 0:
            yr_qry="strftime('%Y', paid_date)="+"'"+str(yr)+"'"
        else:
            c_yr=datetime.now().year
            yr_qry="strftime('%Y', paid_date)="+"'"+str(c_yr)+"'"
        ################## JUNK  
        # stmt="select * from claims_sample where "+yr_qry+" and "+mon_qry+" and "+qtr_qry+" and claim_denial_ind='1'"    
        # cur.execute(stmt)
        # all_rows=cur.fetchall()   
        # count=0
        # den_claim_lst=list()   
        # for i in range(0,len(all_rows)):
        #     if all_rows[i][0] not in den_claim_lst:
        #         if str(get_status(all_rows[i][0]).split('}')[0])=='1':
        #             count=count+1
        ################## JUNK
        # where "+yr_qry+" and "+mon_qry+" and "+qtr_qry    
        stmt1="select distinct root_claim_num from claims_sample where claim_denial_ind='1' and "+yr_qry+" and "+mon_qry+" and "+qtr_qry    
        stmt2="select distinct root_claim_num from claims_sample where claim_denial_ind='0' and "+yr_qry+" and "+mon_qry+" and "+qtr_qry    
        stmt3=stmt1+" except "+stmt2
        stmt4="select round(sum(amt_billed),2) from claims_sample where root_claim_num in("+stmt3+") and "+yr_qry+" and "+mon_qry+" and "+qtr_qry    
        cur.execute(stmt4)
        all_rows=cur.fetchall()
        count=(str((all_rows[0][0])))
        
        if mon > 0:
            mon_op=" month of "+str(mon)+","
        else:
            mon_op=""
        if yr > 0:
            yr_op="year "+str(yr)
        else:
            yr_op="year "+str(datetime.now().year)
        if qtr > 0:
            qtr_op=str(qtr)+" quarter,"
        else:
            qtr_op=""

        recvd_num="The total billed amount for the denied claims was "+str(count)+" in "+mon_op+qtr_op+yr_op+"."
        print(recvd_num)
        return recvd_num
        conn.commit()
        conn.close()

    except Error as e:
        print(str(e))
        return "Sorry! Could not fetch you results at this time"

def get_mode_submission_dend(mon=0,yr=0,qtr=0):
    try:
        database = "claims.db"
        conn = create_connection(database)
        cur = conn.cursor()
        if mon > 12 or mon < 0:
            return "Please enter valid month  and Try again"
        if yr > datetime.now().year and yr < 0:
            return "Please enter valid year  and Try again"
        if qtr==1:
            qtr_qry="strftime('%m', received_date) in "+"('1','2','3')"
        elif qtr==2:
            qtr_qry="strftime('%m', received_date) in "+"('4','5','6')"
        elif qtr==3:
            qtr_qry="strftime('%m', received_date) in "+"('7','8','9')"
        elif qtr==4:
            qtr_qry="strftime('%m', received_date) in "+"('10','11','12')"
        elif qtr==0:
            qtr_qry="strftime('%m', received_date) IS NOT NULL "
        else:
            return "Please enter valid quarter  and Try again"
        if mon > 0:
            mon_qry="strftime('%m', received_date)="+"'"+str(mon)+"'"
        else:
            mon_qry="strftime('%m', received_date) IS NOT NULL "
        if yr > 0:
            yr_qry="strftime('%Y', received_date)="+"'"+str(yr)+"'"
        else:
            c_yr=datetime.now().year
            yr_qry="strftime('%Y', received_date)="+"'"+str(c_yr)+"'"  
        stmt="select distinct claim_receipt_type_cd from claims_sample"
        cur.execute(stmt)
        all_rows=cur.fetchall()
        unq_crtc=list() 
        for i in range(0,len(all_rows)):
            unq_crtc.append(all_rows[i][0])
        crtc_cnt=list()
        for i in range(0,len(unq_crtc)):
            stmt1="select distinct root_claim_num from claims_sample where claim_denial_ind='1' and "+yr_qry+" and "+mon_qry+" and "+qtr_qry    
            stmt2="select distinct root_claim_num from claims_sample where claim_denial_ind='0' and "+yr_qry+" and "+mon_qry+" and "+qtr_qry    
            stmt3=stmt1+" except "+stmt2            
            stmt="select count(*) from claims_sample where root_claim_num in("+stmt3+") and "+yr_qry+" and "+mon_qry+" and "+qtr_qry+" and claim_receipt_type_cd='"+unq_crtc[i]+"'"
            cur.execute(stmt) 
            all_rows=cur.fetchall()        
            n_records=str(all_rows[0][0])
            crtc_cnt.append(str(unq_crtc[i])+"!"+str(n_records)) 
        op_stmt=""
        for i in range(0,len(crtc_cnt)):
            op_stmt=crtc_cnt[i].split('!')[1]+" were submitted on "+crtc_cnt[i].split('!')[0]+", "+op_stmt

        
        if mon > 0:
            mon_op=" month of "+str(mon)+","
        else:
            mon_op=""
        if yr > 0:
            yr_op="year "+str(yr)
        else:
            yr_op="year "+str(datetime.now().year)
        if qtr > 0:
            qtr_op=str(qtr)+" quarter,"
        else:
            qtr_op=""

        recvd_num=op_stmt[0:len(op_stmt)-2]+" in "+mon_op+qtr_op+yr_op+"."
        print(recvd_num)
        return recvd_num
        conn.commit()
        conn.close()

    except Error as e:
        print(str(e))
        return "Sorry! Could not fetch you results at this time"

def get_partial_dend_claims(mon=0,yr=0,qtr=0):
    try:
        database = "claims.db"
        conn = create_connection(database)
        cur = conn.cursor()
        if mon > 12 or mon < 0:
            return "Please enter valid month  and Try again"
        if yr > datetime.now().year and yr < 0:
            return "Please enter valid year  and Try again"
        if qtr==1:
            qtr_qry="strftime('%m', paid_date) in "+"('1','2','3')"
        elif qtr==2:
            qtr_qry="strftime('%m', paid_date) in "+"('4','5','6')"
        elif qtr==3:
            qtr_qry="strftime('%m', paid_date) in "+"('7','8','9')"
        elif qtr==4:
            qtr_qry="strftime('%m', paid_date) in "+"('10','11','12')"
        elif qtr==0:
            qtr_qry="strftime('%m', paid_date) IS NOT NULL "
        else:
            return "Please enter valid quarter  and Try again"
        if mon > 0:
            mon_qry="strftime('%m', paid_date)="+"'"+str(mon)+"'"
        else:
            mon_qry="strftime('%m', paid_date) IS NOT NULL "
        if yr > 0:
            yr_qry="strftime('%Y', paid_date)="+"'"+str(yr)+"'"
        else:
            c_yr=datetime.now().year
            yr_qry="strftime('%Y', paid_date)="+"'"+str(c_yr)+"'"
        ################## JUNK  
        # stmt="select * from claims_sample where "+yr_qry+" and "+mon_qry+" and "+qtr_qry+" and claim_denial_ind='1'"    
        # cur.execute(stmt)
        # all_rows=cur.fetchall()   
        # count=0
        # den_claim_lst=list()   
        # for i in range(0,len(all_rows)):
        #     if all_rows[i][0] not in den_claim_lst:
        #         if str(get_status(all_rows[i][0]).split('}')[0])=='1':
        #             count=count+1
        ################## JUNK
        # where "+yr_qry+" and "+mon_qry+" and "+qtr_qry    
        stmt1="select distinct root_claim_num from claims_sample where claim_denial_ind='1' and "+yr_qry+" and "+mon_qry+" and "+qtr_qry    
        stmt2="select distinct root_claim_num from claims_sample where claim_denial_ind='0' and "+yr_qry+" and "+mon_qry+" and "+qtr_qry    
        stmt3=stmt1+" intersect "+stmt2
        stmt4="select count(*) from claims_sample where root_claim_num in("+stmt3+") and "+yr_qry+" and "+mon_qry+" and "+qtr_qry    
        cur.execute(stmt4)
        all_rows=cur.fetchall()
        count=(str((all_rows[0][0])))
        
        if mon > 0:
            mon_op=" month of "+str(mon)+","
        else:
            mon_op=""
        if yr > 0:
            yr_op="year "+str(yr)
        else:
            yr_op="year "+str(datetime.now().year)
        if qtr > 0:
            qtr_op=str(qtr)+" quarter,"
        else:
            qtr_op=""

        recvd_num=str(count)+" claims were partially denied in "+mon_op+qtr_op+yr_op+"."
        print(recvd_num)
        return recvd_num
        conn.commit()
        conn.close()

    except Error as e:
        print(str(e))
        return "Sorry! Could not fetch you results at this time"

def get_bill_amt_partial_dend(mon=0,yr=0,qtr=0):
    try:
        database = "claims.db"
        conn = create_connection(database)
        cur = conn.cursor()
        if mon > 12 or mon < 0:
            return "Please enter valid month  and Try again"
        if yr > datetime.now().year and yr < 0:
            return "Please enter valid year  and Try again"
        if qtr==1:
            qtr_qry="strftime('%m', paid_date) in "+"('1','2','3')"
        elif qtr==2:
            qtr_qry="strftime('%m', paid_date) in "+"('4','5','6')"
        elif qtr==3:
            qtr_qry="strftime('%m', paid_date) in "+"('7','8','9')"
        elif qtr==4:
            qtr_qry="strftime('%m', paid_date) in "+"('10','11','12')"
        elif qtr==0:
            qtr_qry="strftime('%m', paid_date) IS NOT NULL "
        else:
            return "Please enter valid quarter  and Try again"
        if mon > 0:
            mon_qry="strftime('%m', paid_date)="+"'"+str(mon)+"'"
        else:
            mon_qry="strftime('%m', paid_date) IS NOT NULL "
        if yr > 0:
            yr_qry="strftime('%Y', paid_date)="+"'"+str(yr)+"'"
        else:
            c_yr=datetime.now().year
            yr_qry="strftime('%Y', paid_date)="+"'"+str(c_yr)+"'"
        ################## JUNK  
        # stmt="select * from claims_sample where "+yr_qry+" and "+mon_qry+" and "+qtr_qry+" and claim_denial_ind='1'"    
        # cur.execute(stmt)
        # all_rows=cur.fetchall()   
        # count=0
        # den_claim_lst=list()   
        # for i in range(0,len(all_rows)):
        #     if all_rows[i][0] not in den_claim_lst:
        #         if str(get_status(all_rows[i][0]).split('}')[0])=='1':
        #             count=count+1
        ################## JUNK
        # where "+yr_qry+" and "+mon_qry+" and "+qtr_qry    
        stmt1="select distinct root_claim_num from claims_sample where claim_denial_ind='1' and "+yr_qry+" and "+mon_qry+" and "+qtr_qry    
        stmt2="select distinct root_claim_num from claims_sample where claim_denial_ind='0' and "+yr_qry+" and "+mon_qry+" and "+qtr_qry    
        stmt3=stmt1+" intersect "+stmt2
        stmt4="select round(sum(amt_billed),2) from claims_sample where root_claim_num in("+stmt3+") and "+yr_qry+" and "+mon_qry+" and "+qtr_qry    
        cur.execute(stmt4)
        all_rows=cur.fetchall()
        count=(str((all_rows[0][0])))
        
        if mon > 0:
            mon_op=" month of "+str(mon)+","
        else:
            mon_op=""
        if yr > 0:
            yr_op="year "+str(yr)
        else:
            yr_op="year "+str(datetime.now().year)
        if qtr > 0:
            qtr_op=str(qtr)+" quarter,"
        else:
            qtr_op=""

        recvd_num="The total billed amount for the partial denied claims was "+str(count)+" in "+mon_op+qtr_op+yr_op+"."
        print(recvd_num)
        return recvd_num
        conn.commit()
        conn.close()

    except Error as e:
        print(str(e))
        return "Sorry! Could not fetch you results at this time"

def get_mode_submission_prtl_dend(mon=0,yr=0,qtr=0):
    try:
        database = "claims.db"
        conn = create_connection(database)
        cur = conn.cursor()
        if mon > 12 or mon < 0:
            return "Please enter valid month  and Try again"
        if yr > datetime.now().year and yr < 0:
            return "Please enter valid year  and Try again"
        if qtr==1:
            qtr_qry="strftime('%m', received_date) in "+"('1','2','3')"
        elif qtr==2:
            qtr_qry="strftime('%m', received_date) in "+"('4','5','6')"
        elif qtr==3:
            qtr_qry="strftime('%m', received_date) in "+"('7','8','9')"
        elif qtr==4:
            qtr_qry="strftime('%m', received_date) in "+"('10','11','12')"
        elif qtr==0:
            qtr_qry="strftime('%m', received_date) IS NOT NULL "
        else:
            return "Please enter valid quarter  and Try again"
        if mon > 0:
            mon_qry="strftime('%m', received_date)="+"'"+str(mon)+"'"
        else:
            mon_qry="strftime('%m', received_date) IS NOT NULL "
        if yr > 0:
            yr_qry="strftime('%Y', received_date)="+"'"+str(yr)+"'"
        else:
            c_yr=datetime.now().year
            yr_qry="strftime('%Y', received_date)="+"'"+str(c_yr)+"'"  
        stmt="select distinct claim_receipt_type_cd from claims_sample"
        cur.execute(stmt)
        all_rows=cur.fetchall()
        unq_crtc=list() 
        for i in range(0,len(all_rows)):
            unq_crtc.append(all_rows[i][0])
        crtc_cnt=list()
        for i in range(0,len(unq_crtc)):
            stmt1="select distinct root_claim_num from claims_sample where claim_denial_ind='1' and "+yr_qry+" and "+mon_qry+" and "+qtr_qry    
            stmt2="select distinct root_claim_num from claims_sample where claim_denial_ind='0' and "+yr_qry+" and "+mon_qry+" and "+qtr_qry    
            stmt3=stmt1+" intersect "+stmt2            
            stmt="select count(*) from claims_sample where root_claim_num in("+stmt3+") and "+yr_qry+" and "+mon_qry+" and "+qtr_qry+" and claim_receipt_type_cd='"+unq_crtc[i]+"'"
            cur.execute(stmt) 
            all_rows=cur.fetchall()        
            n_records=str(all_rows[0][0])
            crtc_cnt.append(str(unq_crtc[i])+"!"+str(n_records)) 
        op_stmt=""
        for i in range(0,len(crtc_cnt)):
            op_stmt=crtc_cnt[i].split('!')[1]+" were submitted on "+crtc_cnt[i].split('!')[0]+", "+op_stmt

        
        if mon > 0:
            mon_op=" month of "+str(mon)+","
        else:
            mon_op=""
        if yr > 0:
            yr_op="year "+str(yr)
        else:
            yr_op="year "+str(datetime.now().year)
        if qtr > 0:
            qtr_op=str(qtr)+" quarter,"
        else:
            qtr_op=""

        recvd_num=op_stmt[0:len(op_stmt)-2]+" in "+mon_op+qtr_op+yr_op+"."
        print(recvd_num)
        return recvd_num
        conn.commit()
        conn.close()

    except Error as e:
        print(str(e))
        return "Sorry! Could not fetch you results at this time"

def get_adjstd_claims(mon=0,yr=0,qtr=0):
    try:
        database = "claims.db"
        conn = create_connection(database)
        cur = conn.cursor()
        if mon > 12 or mon < 0:
            return "Please enter valid month  and Try again"
        if yr > datetime.now().year and yr < 0:
            return "Please enter valid year  and Try again"
        if qtr==1:
            qtr_qry="strftime('%m', paid_date) in "+"('1','2','3')"
        elif qtr==2:
            qtr_qry="strftime('%m', paid_date) in "+"('4','5','6')"
        elif qtr==3:
            qtr_qry="strftime('%m', paid_date) in "+"('7','8','9')"
        elif qtr==4:
            qtr_qry="strftime('%m', paid_date) in "+"('10','11','12')"
        elif qtr==0:
            qtr_qry="strftime('%m', paid_date) IS NOT NULL "
        else:
            return "Please enter valid quarter  and Try again"
        if mon > 0:
            mon_qry="strftime('%m', paid_date)="+"'"+str(mon)+"'"
        else:
            mon_qry="strftime('%m', paid_date) IS NOT NULL "
        if yr > 0:
            yr_qry="strftime('%Y', paid_date)="+"'"+str(yr)+"'"
        else:
            c_yr=datetime.now().year
            yr_qry="strftime('%Y', paid_date)="+"'"+str(c_yr)+"'"
        ################## JUNK  
        # stmt="select * from claims_sample where "+yr_qry+" and "+mon_qry+" and "+qtr_qry+" and claim_denial_ind='1'"    
        # cur.execute(stmt)
        # all_rows=cur.fetchall()   
        # count=0
        # den_claim_lst=list()   
        # for i in range(0,len(all_rows)):
        #     if all_rows[i][0] not in den_claim_lst:
        #         if str(get_status(all_rows[i][0]).split('}')[0])=='1':
        #             count=count+1
        ################## JUNK
        # where "+yr_qry+" and "+mon_qry+" and "+qtr_qry    
        stmt1="select distinct root_claim_num from claims_sample where claim_adj_ind='1' and "+yr_qry+" and "+mon_qry+" and "+qtr_qry                    
        stmt4="select count(*) from claims_sample where root_claim_num in("+stmt1+") and "+yr_qry+" and "+mon_qry+" and "+qtr_qry    
        cur.execute(stmt4)
        all_rows=cur.fetchall()
        count=(str((all_rows[0][0])))
        
        if mon > 0:
            mon_op=" month of "+str(mon)+","
        else:
            mon_op=""
        if yr > 0:
            yr_op="year "+str(yr)
        else:
            yr_op="year "+str(datetime.now().year)
        if qtr > 0:
            qtr_op=str(qtr)+" quarter,"
        else:
            qtr_op=""

        recvd_num=str(count)+" claims were adjusted in "+mon_op+qtr_op+yr_op+"."
        print(recvd_num)
        return recvd_num
        conn.commit()
        conn.close()

    except Error as e:
        print(str(e))
        return "Sorry! Could not fetch you results at this time"

def get_bill_amt_adjstd(mon=0,yr=0,qtr=0):
    try:
        database = "claims.db"
        conn = create_connection(database)
        cur = conn.cursor()
        if mon > 12 or mon < 0:
            return "Please enter valid month  and Try again"
        if yr > datetime.now().year and yr < 0:
            return "Please enter valid year  and Try again"
        if qtr==1:
            qtr_qry="strftime('%m', paid_date) in "+"('1','2','3')"
        elif qtr==2:
            qtr_qry="strftime('%m', paid_date) in "+"('4','5','6')"
        elif qtr==3:
            qtr_qry="strftime('%m', paid_date) in "+"('7','8','9')"
        elif qtr==4:
            qtr_qry="strftime('%m', paid_date) in "+"('10','11','12')"
        elif qtr==0:
            qtr_qry="strftime('%m', paid_date) IS NOT NULL "
        else:
            return "Please enter valid quarter  and Try again"
        if mon > 0:
            mon_qry="strftime('%m', paid_date)="+"'"+str(mon)+"'"
        else:
            mon_qry="strftime('%m', paid_date) IS NOT NULL "
        if yr > 0:
            yr_qry="strftime('%Y', paid_date)="+"'"+str(yr)+"'"
        else:
            c_yr=datetime.now().year
            yr_qry="strftime('%Y', paid_date)="+"'"+str(c_yr)+"'"
        ################## JUNK  
        # stmt="select * from claims_sample where "+yr_qry+" and "+mon_qry+" and "+qtr_qry+" and claim_denial_ind='1'"    
        # cur.execute(stmt)
        # all_rows=cur.fetchall()   
        # count=0
        # den_claim_lst=list()   
        # for i in range(0,len(all_rows)):
        #     if all_rows[i][0] not in den_claim_lst:
        #         if str(get_status(all_rows[i][0]).split('}')[0])=='1':
        #             count=count+1
        ################## JUNK
        # where "+yr_qry+" and "+mon_qry+" and "+qtr_qry    
        stmt1="select distinct root_claim_num from claims_sample where claim_adj_ind='1' and "+yr_qry+" and "+mon_qry+" and "+qtr_qry                    
        stmt4="select sum(amt_billed) from claims_sample where root_claim_num in("+stmt1+") and "+yr_qry+" and "+mon_qry+" and "+qtr_qry 
        cur.execute(stmt4)
        all_rows=cur.fetchall()
        count=(str((all_rows[0][0])))
        
        if mon > 0:
            mon_op=" month of "+str(mon)+","
        else:
            mon_op=""
        if yr > 0:
            yr_op="year "+str(yr)
        else:
            yr_op="year "+str(datetime.now().year)
        if qtr > 0:
            qtr_op=str(qtr)+" quarter,"
        else:
            qtr_op=""

        recvd_num="The total billed amount for adjusted  claims was "+str(count)+" in "+mon_op+qtr_op+yr_op+"."
        print(recvd_num)
        return recvd_num
        conn.commit()
        conn.close()

    except Error as e:
        print(str(e))
        return "Sorry! Could not fetch you results at this time"

def get_paid_amt_adjstd(mon=0,yr=0,qtr=0):
    try:
        database = "claims.db"
        conn = create_connection(database)
        cur = conn.cursor()
        if mon > 12 or mon < 0:
            return "Please enter valid month  and Try again"
        if yr > datetime.now().year and yr < 0:
            return "Please enter valid year  and Try again"
        if qtr==1:
            qtr_qry="strftime('%m', paid_date) in "+"('1','2','3')"
        elif qtr==2:
            qtr_qry="strftime('%m', paid_date) in "+"('4','5','6')"
        elif qtr==3:
            qtr_qry="strftime('%m', paid_date) in "+"('7','8','9')"
        elif qtr==4:
            qtr_qry="strftime('%m', paid_date) in "+"('10','11','12')"
        elif qtr==0:
            qtr_qry="strftime('%m', paid_date) IS NOT NULL "
        else:
            return "Please enter valid quarter  and Try again"
        if mon > 0:
            mon_qry="strftime('%m', paid_date)="+"'"+str(mon)+"'"
        else:
            mon_qry="strftime('%m', paid_date) IS NOT NULL "
        if yr > 0:
            yr_qry="strftime('%Y', paid_date)="+"'"+str(yr)+"'"
        else:
            c_yr=datetime.now().year
            yr_qry="strftime('%Y', paid_date)="+"'"+str(c_yr)+"'"
        ################## JUNK  
        # stmt="select * from claims_sample where "+yr_qry+" and "+mon_qry+" and "+qtr_qry+" and claim_denial_ind='1'"    
        # cur.execute(stmt)
        # all_rows=cur.fetchall()   
        # count=0
        # den_claim_lst=list()   
        # for i in range(0,len(all_rows)):
        #     if all_rows[i][0] not in den_claim_lst:
        #         if str(get_status(all_rows[i][0]).split('}')[0])=='1':
        #             count=count+1
        ################## JUNK
        # where "+yr_qry+" and "+mon_qry+" and "+qtr_qry    
        stmt1="select distinct root_claim_num from claims_sample where claim_adj_ind='1' and "+yr_qry+" and "+mon_qry+" and "+qtr_qry                    
        stmt4="select sum(amt_paid) from claims_sample where root_claim_num in("+stmt1+") and "+yr_qry+" and "+mon_qry+" and "+qtr_qry 
        cur.execute(stmt4)
        all_rows=cur.fetchall()
        count=(str((all_rows[0][0])))
        
        if mon > 0:
            mon_op=" month of "+str(mon)+","
        else:
            mon_op=""
        if yr > 0:
            yr_op="year "+str(yr)
        else:
            yr_op="year "+str(datetime.now().year)
        if qtr > 0:
            qtr_op=str(qtr)+" quarter,"
        else:
            qtr_op=""

        recvd_num="The total Paid amount for adjusted  claims was "+str(count)+" in "+mon_op+qtr_op+yr_op+"."
        print(recvd_num)
        return recvd_num
        conn.commit()
        conn.close()

    except Error as e:
        print(str(e))
        return "Sorry! Could not fetch you results at this time"

def get_adj_amt_adjstd(mon=0,yr=0,qtr=0):
    try:
        database = "claims.db"
        conn = create_connection(database)
        cur = conn.cursor()
        if mon > 12 or mon < 0:
            return "Please enter valid month  and Try again"
        if yr > datetime.now().year and yr < 0:
            return "Please enter valid year  and Try again"
        if qtr==1:
            qtr_qry="strftime('%m', paid_date) in "+"('1','2','3')"
        elif qtr==2:
            qtr_qry="strftime('%m', paid_date) in "+"('4','5','6')"
        elif qtr==3:
            qtr_qry="strftime('%m', paid_date) in "+"('7','8','9')"
        elif qtr==4:
            qtr_qry="strftime('%m', paid_date) in "+"('10','11','12')"
        elif qtr==0:
            qtr_qry="strftime('%m', paid_date) IS NOT NULL "
        else:
            return "Please enter valid quarter  and Try again"
        if mon > 0:
            mon_qry="strftime('%m', paid_date)="+"'"+str(mon)+"'"
        else:
            mon_qry="strftime('%m', paid_date) IS NOT NULL "
        if yr > 0:
            yr_qry="strftime('%Y', paid_date)="+"'"+str(yr)+"'"
        else:
            c_yr=datetime.now().year
            yr_qry="strftime('%Y', paid_date)="+"'"+str(c_yr)+"'"
        ################## JUNK  
        # stmt="select * from claims_sample where "+yr_qry+" and "+mon_qry+" and "+qtr_qry+" and claim_denial_ind='1'"    
        # cur.execute(stmt)
        # all_rows=cur.fetchall()   
        # count=0
        # den_claim_lst=list()   
        # for i in range(0,len(all_rows)):
        #     if all_rows[i][0] not in den_claim_lst:
        #         if str(get_status(all_rows[i][0]).split('}')[0])=='1':
        #             count=count+1
        ################## JUNK
        # where "+yr_qry+" and "+mon_qry+" and "+qtr_qry    
        stmt1="select distinct root_claim_num from claims_sample where claim_adj_ind='1' and "+yr_qry+" and "+mon_qry+" and "+qtr_qry                    
        stmt4="select round(sum(amt_billed),2) from claims_sample where root_claim_num in("+stmt1+") and "+yr_qry+" and "+mon_qry+" and "+qtr_qry 
        cur.execute(stmt4)
        all_rows=cur.fetchall()
        count=float(str((all_rows[0][0])))
        stmt4="select round(sum(amt_paid),2) from claims_sample where root_claim_num in("+stmt1+") and "+yr_qry+" and "+mon_qry+" and "+qtr_qry 
        cur.execute(stmt4)
        all_rows=cur.fetchall()
        count1=float(str((all_rows[0][0])))
        count=count-count1
        if mon > 0:
            mon_op=" month of "+str(mon)+","
        else:
            mon_op=""
        if yr > 0:
            yr_op="year "+str(yr)
        else:
            yr_op="year "+str(datetime.now().year)
        if qtr > 0:
            qtr_op=str(qtr)+" quarter,"
        else:
            qtr_op=""

        recvd_num="The total adjusted amount for adjusted  claims was "+str(count)+" in "+mon_op+qtr_op+yr_op+"."
        print(recvd_num)
        return recvd_num
        conn.commit()
        conn.close()

    except Error as e:
        print(str(e))
        return "Sorry! Could not fetch you results at this time"


def get_mode_submission_adjstd(mon=0,yr=0,qtr=0):
    try:
        database = "claims.db"
        conn = create_connection(database)
        cur = conn.cursor()
        if mon > 12 or mon < 0:
            return "Please enter valid month  and Try again"
        if yr > datetime.now().year and yr < 0:
            return "Please enter valid year  and Try again"
        if qtr==1:
            qtr_qry="strftime('%m', received_date) in "+"('1','2','3')"
        elif qtr==2:
            qtr_qry="strftime('%m', received_date) in "+"('4','5','6')"
        elif qtr==3:
            qtr_qry="strftime('%m', received_date) in "+"('7','8','9')"
        elif qtr==4:
            qtr_qry="strftime('%m', received_date) in "+"('10','11','12')"
        elif qtr==0:
            qtr_qry="strftime('%m', received_date) IS NOT NULL "
        else:
            return "Please enter valid quarter  and Try again"
        if mon > 0:
            mon_qry="strftime('%m', received_date)="+"'"+str(mon)+"'"
        else:
            mon_qry="strftime('%m', received_date) IS NOT NULL "
        if yr > 0:
            yr_qry="strftime('%Y', received_date)="+"'"+str(yr)+"'"
        else:
            c_yr=datetime.now().year
            yr_qry="strftime('%Y', received_date)="+"'"+str(c_yr)+"'"  
        stmt="select distinct claim_receipt_type_cd from claims_sample"
        cur.execute(stmt)
        all_rows=cur.fetchall()
        unq_crtc=list() 
        for i in range(0,len(all_rows)):
            unq_crtc.append(all_rows[i][0])
        crtc_cnt=list()
        for i in range(0,len(unq_crtc)):
            stmt1="select distinct root_claim_num from claims_sample where claim_adj_ind='1' and "+yr_qry+" and "+mon_qry+" and "+qtr_qry            
            stmt="select count(*) from claims_sample where root_claim_num in("+stmt1+") and "+yr_qry+" and "+mon_qry+" and "+qtr_qry+" and claim_receipt_type_cd='"+unq_crtc[i]+"'"
            cur.execute(stmt) 
            all_rows=cur.fetchall()        
            n_records=str(all_rows[0][0])
            crtc_cnt.append(str(unq_crtc[i])+"!"+str(n_records)) 
        op_stmt=""
        for i in range(0,len(crtc_cnt)):
            op_stmt=crtc_cnt[i].split('!')[1]+" were submitted on "+crtc_cnt[i].split('!')[0]+", "+op_stmt

        
        if mon > 0:
            mon_op=" month of "+str(mon)+","
        else:
            mon_op=""
        if yr > 0:
            yr_op="year "+str(yr)
        else:
            yr_op="year "+str(datetime.now().year)
        if qtr > 0:
            qtr_op=str(qtr)+" quarter,"
        else:
            qtr_op=""

        recvd_num=op_stmt[0:len(op_stmt)-2]+" in "+mon_op+qtr_op+yr_op+"."
        print(recvd_num)
        return recvd_num
        conn.commit()
        conn.close()

    except Error as e:
        print(str(e))
        return "Sorry! Could not fetch you results at this time"

def get_high_dollar_claims(mon=0,yr=0,qtr=0):
    try:
        database = "claims.db"
        conn = create_connection(database)
        cur = conn.cursor()
        if mon > 12 or mon < 0:
            return "Please enter valid month  and Try again"
        if yr > datetime.now().year and yr < 0:
            return "Please enter valid year  and Try again"
        if qtr==1:
            qtr_qry="strftime('%m', received_date) in "+"('1','2','3')"
        elif qtr==2:
            qtr_qry="strftime('%m', received_date) in "+"('4','5','6')"
        elif qtr==3:
            qtr_qry="strftime('%m', received_date) in "+"('7','8','9')"
        elif qtr==4:
            qtr_qry="strftime('%m', received_date) in "+"('10','11','12')"
        elif qtr==0:
            qtr_qry="strftime('%m', received_date) IS NOT NULL "
        else:
            return "Please enter valid quarter  and Try again"
        if mon > 0:
            mon_qry="strftime('%m', received_date)="+"'"+str(mon)+"'"
        else:
            mon_qry="strftime('%m', received_date) IS NOT NULL "
        if yr > 0:
            yr_qry="strftime('%Y', received_date)="+"'"+str(yr)+"'"
        else:
            c_yr=datetime.now().year
            yr_qry="strftime('%Y', received_date)="+"'"+str(c_yr)+"'"  
        stmt="select count(distinct root_claim_num) from claims_sample where claim_high_dollar_paid_ind='1' and "+yr_qry+" and "+mon_qry+" and "+qtr_qry    
        # print(stmt)    
        cur.execute(stmt)
        all_rows=cur.fetchall()        
        n_records=str(all_rows[0][0])
        if mon > 0:
            mon_op=" month of "+str(mon)+","
        else:
            mon_op=""
        if yr > 0:
            yr_op="year "+str(yr)
        else:
            yr_op="year "+str(datetime.now().year)
        if qtr > 0:
            qtr_op=str(qtr)+" quarter,"
        else:
            qtr_op=""

        recvd_num=str(n_records)+"} high dollar claims were received in "+mon_op+qtr_op+yr_op+"."
        print(recvd_num)
        return recvd_num
        conn.commit()
        conn.close()

    except Error as e:
        print(str(e))
        return "Sorry! Could not fetch you results at this time"

def get_bill_amt_hgh_dlr(mon=0,yr=0,qtr=0):
    try:
        database = "claims.db"
        conn = create_connection(database)
        cur = conn.cursor()
        if mon > 12 or mon < 0:
            return "Please enter valid month  and Try again"
        if yr > datetime.now().year and yr < 0:
            return "Please enter valid year  and Try again"
        if qtr==1:
            qtr_qry="strftime('%m', received_date) in "+"('1','2','3')"
        elif qtr==2:
            qtr_qry="strftime('%m', received_date) in "+"('4','5','6')"
        elif qtr==3:
            qtr_qry="strftime('%m', received_date) in "+"('7','8','9')"
        elif qtr==4:
            qtr_qry="strftime('%m', received_date) in "+"('10','11','12')"
        elif qtr==0:
            qtr_qry="strftime('%m', received_date) IS NOT NULL "
        else:
            return "Please enter valid quarter  and Try again"
        if mon > 0:
            mon_qry="strftime('%m', received_date)="+"'"+str(mon)+"'"
        else:
            mon_qry="strftime('%m', received_date) IS NOT NULL "
        if yr > 0:
            yr_qry="strftime('%Y', received_date)="+"'"+str(yr)+"'"
        else:
            c_yr=datetime.now().year
            yr_qry="strftime('%Y', received_date)="+"'"+str(c_yr)+"'"  
        stmt="select round(sum(amt_billed),2) from claims_sample where claim_high_dollar_paid_ind='1' and  "+yr_qry+" and "+mon_qry+" and "+qtr_qry    
        # print(stmt)    
        cur.execute(stmt)
        all_rows=cur.fetchall()        
        n_records=str(all_rows[0][0]).replace("None","0")
        if mon > 0:
            mon_op=" month of "+str(mon)+","
        else:
            mon_op=""
        if yr > 0:
            yr_op="year "+str(yr)
        else:
            yr_op="year "+str(datetime.now().year)
        if qtr > 0:
            qtr_op=str(qtr)+" quarter,"
        else:
            qtr_op=""

        recvd_num="The total billed amount for high dollar claims in "+mon_op+qtr_op+yr_op+" is} "+str(n_records)
        print(recvd_num)
        return recvd_num
        conn.commit()
        conn.close()

    except Error as e:
        print(str(e))
        return "Sorry! Could not fetch you results at this time"

def get_paid_claims_hgh_dlr(mon=0,yr=0,qtr=0):
    try:
        database = "claims.db"
        conn = create_connection(database)
        cur = conn.cursor()
        if mon > 12 or mon < 0:
            return "Please enter valid month  and Try again"
        if yr > datetime.now().year and yr < 0:
            return "Please enter valid year  and Try again"
        if qtr==1:
            qtr_qry="strftime('%m', received_date) in ('1','2','3') and strftime('%m', paid_date) in ('1','2','3') "
        elif qtr==2:
            qtr_qry="strftime('%m', received_date) in ('4','5','6') and strftime('%m', paid_date) in ('4','5','6') "
        elif qtr==3:
            qtr_qry="strftime('%m', received_date) in ('7','8','9') and strftime('%m', paid_date) in ('7','8','9')"
        elif qtr==4:
            qtr_qry="strftime('%m', received_date) in ('10','11','12') and strftime('%m', paid_date) in ('10','11','12') "
        elif qtr==0:
            qtr_qry="strftime('%m', received_date) IS NOT NULL "
        else:
            return "Please enter valid quarter  and Try again"
        if mon > 0:
            mon_qry="strftime('%m', received_date)="+"'"+str(mon)+"'"+" and "+"strftime('%m', paid_date)="+"'"+str(mon)+"'"
        else:
            mon_qry="strftime('%m', received_date) IS NOT NULL "+" and "+"strftime('%m', paid_date) IS NOT NULL "
        if yr > 0:
            yr_qry="strftime('%Y', received_date)="+"'"+str(yr)+"'"+" and "+"strftime('%Y', paid_date)="+"'"+str(yr)+"'"
        else:
            c_yr=datetime.now().year
            yr_qry="strftime('%Y', received_date)="+"'"+str(c_yr)+"'"+" and "+"strftime('%Y', paid_date)="+"'"+str(c_yr)+"'"  
        stmt="select count(distinct root_claim_num) from claims_sample where claim_high_dollar_paid_ind='1' and  "+yr_qry+" and "+mon_qry+" and "+qtr_qry    
        print(stmt)    
        cur.execute(stmt)
        all_rows=cur.fetchall()        
        n_records=str(all_rows[0][0]).replace("None","0")
        if mon > 0:
            mon_op=" month of "+str(mon)+","
        else:
            mon_op=""
        if yr > 0:
            yr_op="year "+str(yr)
        else:
            yr_op="year "+str(datetime.now().year)
        if qtr > 0:
            qtr_op=str(qtr)+" quarter,"
        else:
            qtr_op=""
        
        recvd_num=str(n_records)+" claims got paid out of "+ get_high_dollar_claims(mon,yr,qtr).split('}')[0].strip(' ') +" claims that were received in "+mon_op+qtr_op+yr_op+"."
        print(recvd_num)
        return recvd_num
        conn.commit()
        conn.close()

    except Error as e:
        print(str(e))
        return "Sorry! Could not fetch you results at this time"

def get_paid_amt_hgh_dlr(mon=0,yr=0,qtr=0):
    try:
        database = "claims.db"
        conn = create_connection(database)
        cur = conn.cursor()
        if mon > 12 or mon < 0:
            return "Please enter valid month  and Try again"
        if yr > datetime.now().year and yr < 0:
            return "Please enter valid year  and Try again"
        if qtr==1:
            qtr_qry="strftime('%m', received_date) in ('1','2','3') and strftime('%m', paid_date) in ('1','2','3') "
        elif qtr==2:
            qtr_qry="strftime('%m', received_date) in ('4','5','6') and strftime('%m', paid_date) in ('4','5','6') "
        elif qtr==3:
            qtr_qry="strftime('%m', received_date) in ('7','8','9') and strftime('%m', paid_date) in ('7','8','9')"
        elif qtr==4:
            qtr_qry="strftime('%m', received_date) in ('10','11','12') and strftime('%m', paid_date) in ('10','11','12') "
        elif qtr==0:
            qtr_qry="strftime('%m', received_date) IS NOT NULL "
        else:
            return "Please enter valid quarter  and Try again"
        if mon > 0:
            mon_qry="strftime('%m', received_date)="+"'"+str(mon)+"'"+" and "+"strftime('%m', paid_date)="+"'"+str(mon)+"'"
        else:
            mon_qry="strftime('%m', received_date) IS NOT NULL "+" and "+"strftime('%m', paid_date) IS NOT NULL "
        if yr > 0:
            yr_qry="strftime('%Y', received_date)="+"'"+str(yr)+"'"+" and "+"strftime('%Y', paid_date)="+"'"+str(yr)+"'"
        else:
            c_yr=datetime.now().year
            yr_qry="strftime('%Y', received_date)="+"'"+str(c_yr)+"'"+" and "+"strftime('%Y', paid_date)="+"'"+str(c_yr)+"'"  
        stmt="select round(sum(amt_paid),2) from claims_sample where claim_high_dollar_paid_ind='1' and "+yr_qry+" and "+mon_qry+" and "+qtr_qry    
        print(stmt)    
        cur.execute(stmt)
        all_rows=cur.fetchall()        
        n_records=str(all_rows[0][0]).replace("None","0")
        if mon > 0:
            mon_op=" month of "+str(mon)+","
        else:
            mon_op=""
        if yr > 0:
            yr_op="year "+str(yr)
        else:
            yr_op="year "+str(datetime.now().year)
        if qtr > 0:
            qtr_op=str(qtr)+" quarter,"
        else:
            qtr_op=""
        print("test"+str(get_bill_amt_hgh_dlr(mon,yr,qtr).split('}')))
        recvd_num="Out of the "+get_bill_amt_hgh_dlr(mon,yr,qtr).split('}')[1].strip(' ') +" billed for the claims received,"+str(n_records)+" was paid in "+mon_op+qtr_op+yr_op+"."        
        print(recvd_num)
        return recvd_num
        conn.commit()
        conn.close()

    except Error as e:
        print(str(e))
        return "Sorry! Could not fetch you results at this time"

def get_mode_submsn_hgh_dlr(mon=0,yr=0,qtr=0):
    try:
        database = "claims.db"
        conn = create_connection(database)
        cur = conn.cursor()
        if mon > 12 or mon < 0:
            return "Please enter valid month  and Try again"
        if yr > datetime.now().year and yr < 0:
            return "Please enter valid year  and Try again"
        if qtr==1:
            qtr_qry="strftime('%m', received_date) in "+"('1','2','3')"
        elif qtr==2:
            qtr_qry="strftime('%m', received_date) in "+"('4','5','6')"
        elif qtr==3:
            qtr_qry="strftime('%m', received_date) in "+"('7','8','9')"
        elif qtr==4:
            qtr_qry="strftime('%m', received_date) in "+"('10','11','12')"
        elif qtr==0:
            qtr_qry="strftime('%m', received_date) IS NOT NULL "
        else:
            return "Please enter valid quarter  and Try again"
        if mon > 0:
            mon_qry="strftime('%m', received_date)="+"'"+str(mon)+"'"
        else:
            mon_qry="strftime('%m', received_date) IS NOT NULL "
        if yr > 0:
            yr_qry="strftime('%Y', received_date)="+"'"+str(yr)+"'"
        else:
            c_yr=datetime.now().year
            yr_qry="strftime('%Y', received_date)="+"'"+str(c_yr)+"'"  
        stmt="select distinct claim_receipt_type_cd from claims_sample"
        cur.execute(stmt)
        all_rows=cur.fetchall()
        unq_crtc=list() 
        for i in range(0,len(all_rows)):
            unq_crtc.append(all_rows[i][0])
        crtc_cnt=list()
        for i in range(0,len(unq_crtc)):
            stmt="select count(*) from claims_sample where claim_high_dollar_paid_ind='1' and "+yr_qry+" and "+mon_qry+" and "+qtr_qry+" and claim_receipt_type_cd='"+unq_crtc[i]+"'"
            cur.execute(stmt) 
            all_rows=cur.fetchall()        
            n_records=str(all_rows[0][0])
            crtc_cnt.append(str(unq_crtc[i])+"!"+str(n_records)) 
        op_stmt=""
        for i in range(0,len(crtc_cnt)):
            op_stmt=crtc_cnt[i].split('!')[1]+" were submitted on "+crtc_cnt[i].split('!')[0]+", "+op_stmt

        
        if mon > 0:
            mon_op=" month of "+str(mon)+","
        else:
            mon_op=""
        if yr > 0:
            yr_op="year "+str(yr)
        else:
            yr_op="year "+str(datetime.now().year)
        if qtr > 0:
            qtr_op=str(qtr)+" quarter,"
        else:
            qtr_op=""

        recvd_num=op_stmt[0:len(op_stmt)-2]+" in "+mon_op+qtr_op+yr_op+"."
        print(recvd_num)
        return recvd_num
        conn.commit()
        conn.close()

    except Error as e:
        print(str(e))
        return "Sorry! Could not fetch you results at this time"


def main():
    get_high_dollar_claims(mon=11,yr=2018)
    get_bill_amt_hgh_dlr(mon=11,yr=2018)
    get_paid_claims_hgh_dlr(mon=11,yr=2018)
    get_paid_amt_hgh_dlr(mon=11,yr=2018)
    get_mode_submsn_hgh_dlr(mon=11,yr=2018)


if __name__ == '__main__':
    main()






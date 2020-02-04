# import pytest
# from datetime import time, date, timedelta, datetime
# from dateutil import parser
# from dateutil.tz import tzlocal
from datetime import datetime
from duckling import DucklingWrapper, Dim
# from autocorrect import spell
import calendar
import traceback

DW_obj=DucklingWrapper()

def is_future_date(s): ##### future date in respective of year
    # print("eneted future")
    s=s+" 00:00:00"
    # print(s)
    date_format = "%Y-%m-%d %H:%M:%S"    
    start = datetime.strptime(s, date_format)    
    now = datetime.now()
    dt=s
    if start > now:
        dt=dt.replace(str(int(dt.split('-')[0])),str(int(str(datetime.now().year))-1))
        return str(dt).split(' ')[0]
    else:
        return s

def is_future_date_day(s): ##### future date in respective of month
    # print("eneted future")
    s=s+" 00:00:00"
    # print(s)
    date_format = "%Y-%m-%d %H:%M:%S"    
    start = datetime.strptime(s, date_format)    
    now = datetime.now()
    dt=s
    if start > now:
        dt1=dt.replace(str(int(dt.split('-')[1])),str(int(str(dt.split('-')[1]))-1))
        dt1 = datetime.strptime(dt1, date_format)   
        if dt1 > now:
            dt=dt.replace(str(int(dt.split('-')[0])),str(int(str(datetime.now().year))-1))
            return str(dt).split(' ')[0]
        else:
            return str(dt1).split(' ')[0]
    else:
        return s

def corrected_ip_string(s1):
    print("corrected_ip_string")
    try:
        s1=s1.replace('  ',' ').replace('  ',' ')
        s2=s1.split(' ')
        s3=""
        for i in range(0,len(s2)):
            
            if str(s2[i]).upper() in ['JANUARY','FEBRUARY','MARCH','APRIL','MAY','JUNE','JULY','AUGUST','SEPTEMBER','OCTOBER','NOVEMBER','DECEMBER','MONTH','YEAR','QUARTER','FIRST','SECOND','THIRD','FOURTH','FIFTH','SIXTH','SEVENTH','EIGHTH','NINTH','TENTH','ELEVENTH','ONE','TWO','THREE','FOUR','FIVE','SIX','SEVEN','EIGHT','NINE','TEN','ELEVEN','MONTHS','YEARS','QUARTERS']:
                s3=s3+" "+str(s2[i]).lower()+" "
            elif str(s2[i]).upper() in ['TWELFTH','TWELEVE']:
                s3=s3+" twelfth "
            else:
                s3=s3+" "+s2[i].lower()+" "
        s4=s3.replace('since','last').replace('rolling','last').replace('  ',' ').strip(' ')
        s2=s4.split(' ')
        rev_s=""
        # print(s2)
        for i in range(0,len(s2)):
            # s3=i.split()
            n=""
            for j in range(0,len(s2[i])):
                    # print(j)
                    try:
                        n1=int(s2[i][j])
                        n=n+str(n1)
                    except:
                        w=1
            if len(str(n)) > 0 and int(str(n)) > 0 and int(str(n)) < 12:
                if s2[i+1].lower()=='month':
                    mn=calendar.month_name[int(str(n))]
                    rev_s=rev_s+" "+mn+" "
                else:
                    rev_s=rev_s+" "+s2[i].lower()+" "
            else:
                # print(s2[i])
                if s2[i].lower()=='first' and s2[i+1].lower()=='month':
                    # print("entered first")
                    rev_s=rev_s+" "+calendar.month_name[1]+" "
                elif s2[i].lower()=='second' and s2[i+1].lower()=='month':
                    rev_s=rev_s+" "+calendar.month_name[2]+" "
                elif s2[i].lower()=='third' and s2[i+1].lower()=='month':
                    rev_s=rev_s+" "+calendar.month_name[3]+" "
                elif s2[i].lower()=='fourth' and s2[i+1].lower()=='month':
                    rev_s=rev_s+" "+calendar.month_name[4]+" "
                elif s2[i].lower()=='fifth' and s2[i+1].lower()=='month':
                    rev_s=rev_s+" "+calendar.month_name[5]+" "
                elif s2[i].lower()=='sixth' and s2[i+1].lower()=='month':
                    rev_s=rev_s+" "+calendar.month_name[6]+" "
                elif s2[i].lower()=='seventh' and s2[i+1].lower()=='month':
                    rev_s=rev_s+" "+calendar.month_name[7]+" "
                elif s2[i].lower()=='eighth' and s2[i+1].lower()=='month':
                    rev_s=rev_s+" "+calendar.month_name[8]+" "
                elif s2[i].lower()=='ninth' and s2[i+1].lower()=='month':
                    rev_s=rev_s+" "+calendar.month_name[9]+" "
                elif s2[i].lower()=='tenth' and s2[i+1].lower()=='month':
                    rev_s=rev_s+" "+calendar.month_name[10]+" "
                elif s2[i].lower()=='eleventh' and s2[i+1].lower()=='month':
                    rev_s=rev_s+" "+calendar.month_name[11]+" "
                elif s2[i].lower()=='twelfth' and s2[i+1].lower()=='month':
                    rev_s=rev_s+" "+calendar.month_name[12]+" "
                else:
                    rev_s=rev_s+" "+s2[i].lower()+" "
        return str(rev_s.replace('  ',' ').strip(' '))
    except Exception as e:    
        print(str(e)+" in corrected_ip_string function")
        print(traceback.format_exc())
        return "Sorry, Could not fetch you results at this time"

def time_extract(ip_str):
    
    try:
        op_str=corrected_ip_string(ip_str)    
        print("time_extract")   
        
        result =DW_obj.parse_time(u''+op_str)
        print(result)
        r1=str(result)
        r1_s=r1.split(':')
        r1_text=list()
        for ri in range(0,len(r1_s)):
            if "\'text\'".upper() in r1_s[ri].upper():
                r1_text.append(r1_s[ri+1].split(',')[0].strip(' ').replace("\'",""))
        r1_text = list(dict.fromkeys(r1_text))
        print(str(r1_text))
        # del DW_obj
        if len(result)==1:
            print("len result one "+str(result[0]['value']['value']))        
            if str(type(result[0]['value']['value']))=="<class 'dict'>":
                print("if test")
                from_dt=str(result[0]['value']['value']['from']).split('T')[0]
                to_dt=str(result[0]['value']['value']['to']).split('T')[0]
                rng_lst=list()                
                rng_lst.append(from_dt+" 00:00:00")
                rng_lst.append(to_dt+" 00:00:00}"+str(result[0]['text']))
                rng_lst.append(r1_text)
                return rng_lst
            else:
                print("else test"+str(result[0]['value']['grain']).lower())
                day_lst=list()
                mon_lst=list()
                yr_lst=list()
                if str(result[0]['value']['grain']).lower()=='day':
                    dt=str(result[0]['value']['value']).split('T')[0]
                    if int(dt.split('-')[0]) > int(str(datetime.now().year)):                    
                        dt=dt.replace(str(int(dt.split('-')[0])),str(int(str(datetime.now().year))))
                    dt=is_future_date_day(dt)
                    print(dt)
                    day_lst.append(dt.split('-')[2])
                    mon_lst.append(dt.split('-')[1])
                    yr_lst.append(dt.split('-')[0])
                elif str(result[0]['value']['grain']).lower()=='hour':
                    print("entered")
                    dt=str(result[0]['value']['value']).split('T')[1].split(':')[0]
                    print(dt)
                    a=int(str(dt))
                    if a % 12 == 0 :
                        a=12
                    else:
                        if  str(a) not in r1_text:
                            a=a%12

                    day_lst.append(a)
                    
                elif str(result[0]['value']['grain']).lower()=='month':
                    dt=str(result[0]['value']['value']).split('T')[0]
                    if int(dt.split('-')[0]) > int(str(datetime.now().year)):                    
                        dt=dt.replace(str(int(dt.split('-')[0])),str(int(str(datetime.now().year))))
                    dt=is_future_date(dt)
                    print(dt)                
                    mon_lst.append(dt.split('-')[1])
                    yr_lst.append(dt.split('-')[0])
                elif str(result[0]['value']['grain']).lower()=='year':
                    dt=str(result[0]['value']['value']).split('T')[0]
                    # if int(dt.split('-')[0]) > int(str(datetime.now().year)):                    
                    #     dt=dt.replace(str(int(dt.split('-')[0])),str(int(str(datetime.now().year))))
                    # print(dt)  
                    # dt=is_future_date(dt)              
                    yr_lst.append(dt.split('-')[0])
                elif str(result[0]['value']['grain']).lower()=='quarter':
                    dt=str(result[0]['value']['value']).split('T')[0]
                    if int(dt.split('-')[0]) > int(str(datetime.now().year)):                    
                        dt=dt.replace(str(int(dt.split('-')[0])),str(int(str(datetime.now().year))))                
                    dt=is_future_date(dt)                
                    print(dt)
                    qtr_mon=int(str(dt.split('-')[1]))
                    mon_lst.append(str(qtr_mon))
                    mon_lst.append(str(qtr_mon+1))
                    mon_lst.append(str(qtr_mon+2))    
                    yr_lst.append(dt.split('-')[0])            
                comb_list=list()
                comb_list.append(day_lst)
                comb_list.append(mon_lst)
                comb_list.append(yr_lst)
                comb_list.append(r1_text)
                return comb_list
        elif len(result) > 1:

            day_lst=list()
            mon_lst=list()
            yr_lst=list()

            for r_i in range(0,len(result)):

                if str(result[r_i]['value']['grain']).lower()=='year':
                    dt=str(result[r_i]['value']['value']).split('T')[0]
                    # if int(dt.split('-')[0]) > int(str(datetime.now().year)):                    
                    #     dt=dt.replace(str(int(dt.split('-')[0])),str(int(str(datetime.now().year))))
                    # dt=is_future_date(dt)
                    # print(dt)                
                    yr_lst.append(dt.split('-')[0])

            if len(yr_lst)==0:

                for r_i in range(0,len(result)):            
                    if str(result[r_i]['value']['grain']).lower()=='month':
                        dt=str(result[r_i]['value']['value']).split('T')[0]
                        if int(dt.split('-')[0]) > int(str(datetime.now().year)):                    
                            dt=dt.replace(str(int(dt.split('-')[0])),str(int(str(datetime.now().year))))
                        dt=is_future_date(dt)
                        print(dt)
                        mon_lst.append(dt.split('-')[1])
                        yr_lst.append(dt.split('-')[0])
            else:

                for r_i in range(0,len(result)):    
                    if str(result[r_i]['value']['grain']).lower()=='month':
                        dt=str(result[r_i]['value']['value']).split('T')[0]
                        if int(dt.split('-')[0]) > int(str(datetime.now().year)):                    
                            dt=dt.replace(str(int(dt.split('-')[0])),str(int(str(datetime.now().year))))
                        dt=is_future_date(dt)
                        print(dt)
                        mon_lst.append(dt.split('-')[1])

            if len(yr_lst)==0:

                for r_i in range(0,len(result)):            
                    if str(result[r_i]['value']['grain']).lower()=='quarter':
                        dt=str(result[r_i]['value']['value']).split('T')[0]
                        if int(dt.split('-')[0]) > int(str(datetime.now().year)):                    
                            dt=dt.replace(str(int(dt.split('-')[0])),str(int(str(datetime.now().year))))
                        dt=is_future_date(dt)
                        print(dt)
                        qtr_mon=int(str(dt.split('-')[1]))
                        mon_lst.append(str(qtr_mon))
                        mon_lst.append(str(qtr_mon+1))
                        mon_lst.append(str(qtr_mon+2))
                        yr_lst.append(dt.split('-')[0])
            else:
                
                for r_i in range(0,len(result)):    
                    if str(result[r_i]['value']['grain']).lower()=='quarter':
                        dt=str(result[r_i]['value']['value']).split('T')[0]
                        if int(dt.split('-')[0]) > int(str(datetime.now().year)):                    
                            dt=dt.replace(str(int(dt.split('-')[0])),str(int(str(datetime.now().year))))
                        dt=is_future_date(dt)
                        print(dt)
                        qtr_mon=int(str(dt.split('-')[1]))
                        mon_lst.append(str(qtr_mon))
                        mon_lst.append(str(qtr_mon+1))
                        mon_lst.append(str(qtr_mon+2))        

            if len(mon_lst)==0:

                if len(yr_lst)==0:

                    for r_i in range(0,len(result)):
                        
                        if str(result[r_i]['value']['grain']).lower()=='day':
                            dt=str(result[r_i]['value']['value']).split('T')[0]
                            if int(dt.split('-')[0]) > int(str(datetime.now().year)):                    
                                dt=dt.replace(str(int(dt.split('-')[0])),str(int(str(datetime.now().year))))
                            dt=is_future_date_day(dt)
                            print(dt)
                            day_lst.append(dt.split('-')[2])
                            mon_lst.append(dt.split('-')[1])
                            yr_lst.append(dt.split('-')[0])
                else:
                    for r_i in range(0,len(result)):
                        
                        if str(result[r_i]['value']['grain']).lower()=='day':
                            dt=str(result[r_i]['value']['value']).split('T')[0]
                            if int(dt.split('-')[0]) > int(str(datetime.now().year)):                    
                                dt=dt.replace(str(int(dt.split('-')[0])),str(int(str(datetime.now().year))))
                            dt=is_future_date_day(dt)
                            print(dt)
                            day_lst.append(dt.split('-')[2])
                            mon_lst.append(dt.split('-')[1])
                        
                        if str(result[r_i]['value']['grain']).lower()=='hour':
                            print("entered")
                            dt=str(result[0]['value']['value']).split('T')[1].split(':')[0]
                            print(dt)
                            a=int(str(dt))
                            if a % 12 == 0:
                                a=12
                            else:
                                if  str(a) not in r1_text:
                                    a=a%12

                            day_lst.append(a)
            
            else:

                for r_i in range(0,len(result)):
                        
                    if str(result[r_i]['value']['grain']).lower()=='day':
                        dt=str(result[r_i]['value']['value']).split('T')[0]
                        if int(dt.split('-')[0]) > int(str(datetime.now().year)):                    
                            dt=dt.replace(str(int(dt.split('-')[0])),str(int(str(datetime.now().year))))
                        dt=is_future_date_day(dt)
                        print(dt)
                        day_lst.append(dt.split('-')[2])
                    
                    if str(result[r_i]['value']['grain']).lower()=='hour':
                        print("entered")
                        dt=str(result[0]['value']['value']).split('T')[1].split(':')[0]
                        print(dt)
                        a=int(str(dt))
                        if a % 12 == 0:
                            a=12
                        else:
                            if  str(a) not in r1_text:
                                a=a%12

                        day_lst.append(a)
                        
                            
                
            day_lst = list(dict.fromkeys(day_lst))
            mon_lst = list(dict.fromkeys(mon_lst))
            yr_lst = list(dict.fromkeys(yr_lst))
            
            comb_list=list()
            comb_list.append(day_lst)
            comb_list.append(mon_lst)        
            comb_list.append(yr_lst)
            comb_list.append(r1_text)
            return comb_list          
                
        else:

            emp_list=list()
            return emp_list      
    except Exception as e:
        print(str(e)+" in time_extract function")
        print(traceback.format_exc())
        return "Sorry, Could not extract time period"  



def test():
    ##
    # print(str(DucklingWrapper()))     
    # result = time_extract(u'received claims on 28th and 27th ')
    # print(str(result).replace('[','(').replace(']',')'))
    result = time_extract(u'received claims in last two months')
    print(str(result).replace('[','(').replace(']',')'))
    # # print(str(type(result[0]['value']['value'])))
    ##
    result = DucklingWrapper().parse_time(u'received claims in last two months')
    print(str(result))

    
# test() 
print(str(time_extract("top 5 denials in jan 2019 and feb 2019")))

# result = DucklingWrapper().parse_time(u'received claims on Jan,28')
# print(str(result))

# result = DucklingWrapper().parse_time(u'received claims on Jan 28')
# print(str(result))

# result = DucklingWrapper().parse_time(u'received claims on January 28')
# print(str(result))

# result = DucklingWrapper().parse_time(u'received claims on January 28')
# print(str(result))

# coding: utf-8

# In[21]:

import sys
import os

from nlp_modules import *

pd.options.mode.chained_assignment = None

def descriptiveAnalyze(df):
    
    #FileName = 'DescriptiveAnalysis.xlsx'
    #df = df[df['sat1']!='']
    summaryReport = {}
    df.reset_index(drop=True,inplace=True)
    parent_df = df
    
    parent_df['sat1'] = parent_df['sat1'].astype(int)
    detract_df = parent_df[parent_df['sat1']<8]
    promo_df = parent_df[parent_df['sat1']>8]
    
    summaryReport['Number of Detractors'] = detract_df.shape[0]
    summaryReport['Number of Promoters'] = promo_df.shape[0]
    #Quarter wise analysis
    
    
    # In[22]:
    
    health_plans = pd.Categorical(parent_df['healthplan']).categories
    regions = pd.Categorical(parent_df['region']).categories
    rptqtrs = pd.Categorical(parent_df['rptqtr']).categories
    summaryReport['Number of Health Plans'] = len(health_plans)
    summaryReport['Number of Regions'] = len(regions)
    summaryReport['Number of Reporting Quarters'] = len(rptqtrs)
    
    # In[23]:
    
    regionDF = {}
    for r in regions:
        df_r = parent_df[parent_df['region']==r]
        promoters = df_r[(df_r['sat1']==9) | (df_r['sat1']==10)].shape[0]
        passive = df_r[(df_r['sat1']==8)].shape[0]
        detractors = df_r[df_r['sat1']<8].shape[0]
        regionDF[r]=[promoters,passive,detractors]
        
    
    regionDF = pd.DataFrame(regionDF,columns = regionDF.keys(),
                            index = ['Promoters','Passive','Detractors'])
    
    for c in regionDF.columns:
        I = regionDF.loc['Promoters',c]
        J = regionDF.loc['Passive',c]
        K = regionDF.loc['Detractors',c]
        regionDF.loc['Total',c] = I + J + K
        
    #writer=pd.ExcelWriter('DescriptiveAnalysis.xlsx',engine='xlsxwriter')
    #regionDF.to_excel(writer,startcol = 3)
    
    
    # In[24]:
    
    regionDF
    regionDF = regionDF.T
    
    
    # In[25]:
    
    
    plansDF = {}
    for hp in health_plans:
        df_hp = parent_df[parent_df['healthplan']==hp]
        promoters = df_hp[(df_hp['sat1']==9) | (df_hp['sat1']==10)].shape[0]
        passive = df_hp[(df_hp['sat1']==8)].shape[0]
        detractors = df_hp[df_hp['sat1']<8].shape[0]
        plansDF[hp]=[promoters,passive,detractors]
    
    plansDF = pd.DataFrame(plansDF,columns = plansDF.keys(),
                           index = ['Promoters','Passive','Detractors'])
    
    for c in plansDF.columns:
        I = plansDF.loc['Promoters',c]
        J = plansDF.loc['Passive',c]
        K = plansDF.loc['Detractors',c]
        plansDF.loc['Total',c] = I + J + K
    
    #plansDF.to_excel(writer,startrow = 6, startcol = 3)
    
    
    # In[26]:
    
    plansDF
    plansDF = plansDF.T
    
    # In[27]:
    
    quarterDF = {}
    qtrs = rptqtrs[5:]
    
    for q in rptqtrs:
        df_q = parent_df[parent_df['rptqtr']==q]
        promoters = df_q[(df_q['sat1']==9) | (df_q['sat1']==10)].shape[0]
        passive = df_q[(df_q['sat1']==8)].shape[0]
        detractors = df_q[df_q['sat1']<8].shape[0]
        quarterDF[q]=[promoters,passive,detractors]
        
    quarterDF = pd.DataFrame(quarterDF,columns = quarterDF.keys(),
                             index = ['Promoters','Passive','Detractors'])
    
    for c in quarterDF.columns:
        I = quarterDF.loc['Promoters',c]
        J = quarterDF.loc['Passive',c]
        K = quarterDF.loc['Detractors',c]
        quarterDF.loc['Total',c] = I + J + K
    
    #quarterDF.to_excel(writer,startrow = 14, startcol = 3)
    #writer.save()
    
    
    # In[28]:
    
    quarterDF
    quarterDF=quarterDF.T
    
    # In[29]:
    
    df_central = parent_df[parent_df['region']=='Central']
    df_central_detractors = df_central[df_central['sat1']<8]
    df_central_promoters = df_central[df_central['sat1']>8]
    summaryReport['Number of Detractors in Central region'] = len(df_central_detractors)
    summaryReport['Number of Promoters in Central region'] = len(df_central_promoters)
    
    df_se = parent_df[parent_df['region']=='Southeast']
    df_ne = parent_df[parent_df['region']=='Northeast']
    df_w = parent_df[parent_df['region']=='West']
    
    df_SE_detractors = df_se[df_se['sat1']<8]
    df_NE_detractors = df_ne[df_ne['sat1']<8]
    df_W_detractors = df_w[df_w['sat1']<8]
    
    df_SE_promoters = df_se[df_se['sat1']>8]
    df_NE_promoters = df_ne[df_ne['sat1']>8]
    df_W_promoters = df_w[df_w['sat1']>8]
    
    
    summaryReport['Number of Detractors in Southeast region'] = len(df_SE_detractors)
    summaryReport['Number of Detractors in Northeast region'] = len(df_NE_detractors)
    summaryReport['Number of Detractors in West region'] = len(df_W_detractors)
    
    summaryReport['Number of Promoters in Southeast region'] = len(df_SE_promoters)
    summaryReport['Number of Promoters in Northeast region'] = len(df_NE_promoters)
    summaryReport['Number of Promoters in West region'] = len(df_W_promoters)
    
    
    central_detractors_plans = list(set(df_central_detractors['healthplan'].tolist()))
    SE_detractors_plans = list(set(df_SE_detractors['healthplan'].tolist()))
    NE_detractors_plans = list(set(df_NE_detractors['healthplan'].tolist()))
    W_detractors_plans = list(set(df_W_detractors['healthplan'].tolist()))
    
    summaryReport = pd.DataFrame.from_dict(summaryReport,orient='index',columns=['Values'])
    totalSummary = pd.concat([regionDF,plansDF,quarterDF],axis=0)
    return (summaryReport,totalSummary,[central_detractors_plans,SE_detractors_plans,NE_detractors_plans,W_detractors_plans])

def plotChart(detractorsList):
    
    central_detractors_plans = detractorsList[0]
    SE_detractors_plans = detractorsList[1]
    NE_detractors_plans = detractorsList[2]
    W_detractors_plans = detractorsList[3]
    
    topics = ['authorization',
              'billing',
              'fee schedule',
              'referral']
    
    def hplan_analysis(df_,topics,hplans):
        hplan_map = {}
        for topic in topics:
            new_dt = df_[df_['cleaned'].str.contains(topic)]
            topic_vals = []
            for h in hplans:
                dt_hwise = new_dt[new_dt['healthplan']==h]
                per_h = dt_hwise.shape[0]/new_dt.shape[0]
                topic_vals.append(per_h*100)
            hplan_map[topic] = topic_vals
        return hplan_map
    
    
    hplan_analys = hplan_analysis(df_central_detractors,
                                  topics,
                                  central_detractors_plans)
    
    df_hwise_CS = pd.DataFrame(hplan_analys,index=central_detractors_plans,
                               columns=topics)
    
    
    df_hwise_CST = df_hwise_CS.T
    
    #hplans=list(health_plans)
    
    df_hwise_CS1 = df_hwise_CST.loc[:,central_detractors_plans[0:4]]
    df_hwise_CS2 = df_hwise_CST.loc[:,central_detractors_plans[4:8]]
    df_hwise_CS3 = df_hwise_CST.loc[:,central_detractors_plans[8:12]]
    df_hwise_CS4 = df_hwise_CST.loc[:,central_detractors_plans[12:17]]
    
    
    # In[30]:
    
    df_hwise_CS
    
    
    # In[31]:
    
    df_hwise_CS1
    
    
    # In[32]:
    
    df_hwise_CS2
    
    
    # In[33]:
    
    df_hwise_CS3
    
    
    # In[34]:
    
    df_hwise_CS4
    
    
    # In[35]:
    
    def healthplanwise_topics_routine(DATAFRAME,TOPICS,HPLANS):
        N = len(DATAFRAME.index)
        ind = np.arange(N)*2  # the x locations for the groups
        width = 0.27       # the width of the bars
        
        fig = plt.figure()
        ax = fig.add_subplot(111)
        
        
        q6vals = list(DATAFRAME[HPLANS[0]])
        rects6 = ax.bar(ind,q6vals, width, color='b')
    
        q7vals = list(DATAFRAME[HPLANS[1]])
        rects7 = ax.bar(ind+width,q7vals, width, color='g')
    
        q8vals = list(DATAFRAME[HPLANS[2]])
        rects8 = ax.bar(ind+width*2,q8vals, width, color='y')
        
        q9vals = list(DATAFRAME[HPLANS[3]])
        rects9 = ax.bar(ind+width*3,q9vals, width, color='r')
        
        ax.set_ylabel('healthplanwise_Scores')
        ax.set_xticks(ind+width)
        ax.set_xticklabels(TOPICS)
        ax.legend( (rects6[0], rects7[0], rects8[0], rects9[0]), (HPLANS[0],HPLANS[1],HPLANS[2],HPLANS[3]) )
        
        plt.show() 
    
    
    # In[36]:
    
    print (len(central_detractors_plans))
    print (df_central_detractors.shape)
    
    
    # In[37]:
    
    #Central
    healthplanwise_topics_routine(df_hwise_CS1,topics,central_detractors_plans[:4])
    
    
    # In[38]:
    
    #Central
    healthplanwise_topics_routine(df_hwise_CS2,topics,central_detractors_plans[4:8])
    
    
    # In[39]:
    
    #Central
    healthplanwise_topics_routine(df_hwise_CS3,topics,central_detractors_plans[8:12])
    
    
    # In[40]:
    
    #Central
    healthplanwise_topics_routine(df_hwise_CS4,topics,central_detractors_plans[12:17])
    
    
    # In[68]:
    
    hplan_analys_SE = hplan_analysis(df_SE_detractors,
                                     topics,
                                     SE_detractors_plans)
    
    df_hwise_CS_SE = pd.DataFrame(hplan_analys_SE,index=SE_detractors_plans,
                                  columns=topics)
    
    
    df_hwise_CS_SET = df_hwise_CS_SE.T
    
    df_hwise_CS_SE1 = df_hwise_CS_SET.loc[:,SE_detractors_plans[0:4]]
    df_hwise_CS_SE2 = df_hwise_CS_SET.loc[:,SE_detractors_plans[4:8]]
    df_hwise_CS_SE3 = df_hwise_CS_SET.loc[:,SE_detractors_plans[8:]]
    
    
    def healthplanwise_topics_routine_SE(DATAFRAME,TOPICS,HPLANS):
        N = len(DATAFRAME.index)
        ind = np.arange(N)*2  # the x locations for the groups
        width = 0.27       # the width of the bars
        
        fig = plt.figure()
        ax = fig.add_subplot(111)
        
        
        q6vals = list(DATAFRAME[HPLANS[0]])
        rects6 = ax.bar(ind,q6vals, width, color='b')
    
        q7vals = list(DATAFRAME[HPLANS[1]])
        rects7 = ax.bar(ind+width,q7vals, width, color='g')
    
        q8vals = list(DATAFRAME[HPLANS[2]])
        rects8 = ax.bar(ind+width*2,q8vals, width, color='y')
        
        #q9vals = list(DATAFRAME[HPLANS[3]])
        #rects9 = ax.bar(ind+width*3,q9vals, width, color='r')
        
        ax.set_ylabel('healthplanwise_Scores')
        ax.set_xticks(ind+width)
        ax.set_xticklabels(TOPICS)
        ax.legend( (rects6[0], rects7[0], rects8[0]), (HPLANS[0],HPLANS[1],HPLANS[2]) )
        
        plt.show() 
    #df_hwise_CS_SE4 = df_hwise_CS_SET.loc[:,SE_detractors_plans[12:17]]
    
    
    # In[45]:
    
    df_hwise_CS_SET
    
    
    # In[43]:
    
    len(SE_detractors_plans) #Number of health plans in south east detractors (NPS score < 7)
    
    
    # In[46]:
    
    df_hwise_CS_SE1
    
    
    # In[47]:
    
    df_hwise_CS_SE2
    
    
    # In[48]:
    
    df_hwise_CS_SE3
    
    
    # In[49]:
    
    #South east Region
    healthplanwise_topics_routine(df_hwise_CS_SE1,topics,SE_detractors_plans[:4])
    
    
    # In[52]:
    
    #Sourth east Region
    healthplanwise_topics_routine(df_hwise_CS_SE2,topics,SE_detractors_plans[4:8])
    
    
    # In[69]:
    
    #South east Region
    healthplanwise_topics_routine_SE(df_hwise_CS_SE3,topics,SE_detractors_plans[8:])
    
    
    # In[54]:
    
    len(NE_detractors_plans) #Number of health plans in detractors of North east (NPS <7)
    
    
    # In[77]:
    
    hplan_analys_NE = hplan_analysis(df_NE_detractors,
                                     topics,
                                     NE_detractors_plans)
    
    df_hwise_CS_NE = pd.DataFrame(hplan_analys_NE,index=NE_detractors_plans,
                                  columns=topics)
    
    
    df_hwise_CS_NET = df_hwise_CS_NE.T
    
    df_hwise_CS_NE1 = df_hwise_CS_NET.loc[:,NE_detractors_plans[0:4]]
    df_hwise_CS_NE2 = df_hwise_CS_NET.loc[:,NE_detractors_plans[4:8]]
    df_hwise_CS_NE3 = df_hwise_CS_NET.loc[:,NE_detractors_plans[8:]]
    
    
    def healthplanwise_topics_routine_NE(DATAFRAME,TOPICS,HPLANS):
        N = len(DATAFRAME.index)
        ind = np.arange(N)*2  # the x locations for the groups
        width = 0.27       # the width of the bars
        
        fig = plt.figure()
        ax = fig.add_subplot(111)
        
        
        q6vals = list(DATAFRAME[HPLANS[0]])
        rects6 = ax.bar(ind,q6vals, width, color='b')
    
        #q7vals = list(DATAFRAME[HPLANS[1]])
        #rects7 = ax.bar(ind+width,q7vals, width, color='g')
    
        #q8vals = list(DATAFRAME[HPLANS[2]])
        #rects8 = ax.bar(ind+width*2,q8vals, width, color='y')
        
        #q9vals = list(DATAFRAME[HPLANS[3]])
        #rects9 = ax.bar(ind+width*3,q9vals, width, color='r')
        
        ax.set_ylabel('healthplanwise_Scores')
        ax.set_xticks(ind+width)
        ax.set_xticklabels(TOPICS)
        ax.legend((rects6[0],),(HPLANS[0],))
        
        plt.show() 
    
    
    
    # In[73]:
    
    df_hwise_CS_NE1
    
    
    # In[72]:
    
    df_hwise_CS_NE2
    
    
    # In[58]:
    
    df_hwise_CS_NE3
    
    
    # In[60]:
    
    #North east Region
    healthplanwise_topics_routine(df_hwise_CS_NE1,topics,NE_detractors_plans[:4])
    
    
    # In[61]:
    
    #North east Region
    healthplanwise_topics_routine(df_hwise_CS_NE2,topics,NE_detractors_plans[4:8])
    
    
    # In[79]:
    
    #North east Region
    healthplanwise_topics_routine_NE(df_hwise_CS_NE3,topics,NE_detractors_plans[8:])
    
    
    # In[62]:
    
    len(W_detractors_plans) #Number of health plans in detractors in west with NPS score less than 7
    
    
    # In[63]:
    
    hplan_analys_W = hplan_analysis(df_W_detractors,
                                    topics,
                                    W_detractors_plans)
    
    df_hwise_CS_W = pd.DataFrame(hplan_analys_W,index=W_detractors_plans,
                                 columns=topics)
    
    
    df_hwise_CS_WT = df_hwise_CS_W.T
    
    df_hwise_CS_W1 = df_hwise_CS_WT.loc[:,W_detractors_plans[0:4]]
    df_hwise_CS_W2 = df_hwise_CS_WT.loc[:,W_detractors_plans[4:8]]
    #df_hwise_CS_W3 = df_hwise_CS_WT.loc[:,NE_detractors_plans[8:]]
    
    
    # In[64]:
    
    #West Region
    healthplanwise_topics_routine(df_hwise_CS_W1,topics,W_detractors_plans[:4])
    
    
    # In[67]:
    
    #West Region
    healthplanwise_topics_routine(df_hwise_CS_W2,topics,W_detractors_plans[4:8])


# In[ ]:




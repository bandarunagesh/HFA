
# coding: utf-8

# In[1]:

import os
import pandas as pd
from nltk.corpus import stopwords
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob
from nltk.collocations import BigramAssocMeasures, BigramCollocationFinder
from nltk.chunk import conlltags2tree, tree2conlltags
from pprint import pprint

pd.options.mode.chained_assignment = None
from nlp_modules import *

# In[2]:

def sentimentPredict(df):
    df_ppm = df
    original_cols = df_ppm.columns
    health_plans = pd.Categorical(df_ppm['healthplan']).categories
    regions = pd.Categorical(df_ppm['region']).categories
    rptqtrs = pd.Categorical(df_ppm['rptqtr']).categories

    # In[3]:
    
    df_ppm.shape
    
    
    # In[5]:
    
    df_ppm.columns
    
    
    # In[4]:
    
    print (df_ppm[['sat1','sat1_oe']].head(10))
    
    
    # In[274]:
    
    #for d in df_ppm.describe().columns:
    #    print (df_ppm.describe()[d])
    
    
    # In[5]:
    
    df_ppm.info()
    
    
    # In[5]:
    
    df_ppm.isnull().sum()
    
    
    # In[7]:
    
    df_ppm.dtypes
    
    
    # In[6]:
    
    df_ppm['sat1'] = df_ppm['sat1'].astype(str)
    for ind,row in df_ppm.iterrows():
        try:
            if (row['sat1_oe'] == '') | (row['sat1_oe'] == ' '):
                if (row['sat1']!='') & (float(row['sat1']) > 8.0):
                    df_ppm.loc[ind,'sat1_oe'] = 'Positive Feedback'
                elif (row['sat1']!='') & (float(row['sat1']) <= 7.0):
                    df_ppm.loc[ind,'sat1_oe'] = 'Negative Feedback'
                elif (row['sat1']!='') & (float(row['sat1']) == 8.0):
                    df_ppm.loc[ind,'sat1_oe'] = 'Passive Feedback'
                elif row['sat1']=='':
                    df_ppm.loc[ind,'sat1_oe'] = ''
            else:
                continue
        except:
            continue
    
    
    # In[29]:
    
    df_ppm.head(10)
    
    
    # In[7]:
    
    print (df_ppm[['sat1','sat1_oe']].head(10))
    
    
    # In[8]:
    
    #length of comments
    data_nonnull = df_ppm[(df_ppm['sat1_oe']!='') & (df_ppm['sat1_oe']!=' ')]
    data_nonnull.shape
    
    
    # In[9]:
    
    data_nonnull['sat1'] = data_nonnull['sat1'].astype(str)
    dfppm = data_nonnull[(data_nonnull['sat1']!='')]
    
    
    # In[10]:
    
    dfppm.shape
    
    
    # In[11]:
    
    dfppm.reset_index(drop=True,inplace=True)
    dfppm['review_length'] = dfppm['sat1_oe'].apply(lambda x: len(str(x)))
    dfppm[['sat1_oe','review_length']].head(30)
    
    
    # In[12]:
    
    #word count
    dfppm['word_count'] = dfppm['sat1_oe'].apply(lambda t: len(str(t).split(" ")))
    dfppm[['sat1_oe','word_count']].head(20)
    
    
    # In[13]:
    
    dfppm.shape
    
    
    # In[14]:
    
    dfppm.columns
    
    
    # In[15]:
    
    def avg_word_len(text):
        tokens=str(text).split(" ")
        word_l = [len(word) for word in tokens]
        total_l = sum(word_l)
        avg_l = total_l/len(word_l)
        return (avg_l)
    
    #average word length
    dfppm['avg_word_length'] = dfppm['sat1_oe'].apply(lambda t: avg_word_len(t))
    dfppm[['sat1_oe','avg_word_length']].head(10)
    
    
    # In[16]:
    
    #replace quotation with nothing
    dfppm['cleaned'] = dfppm['sat1_oe'].apply(lambda t: str(t).replace("'",""))
    #convert into lower case
    dfppm['cleaned'] = dfppm['cleaned'].str.lower()
    
    #replace punctuations
    dfppm['cleaned'] = dfppm['cleaned'].str.replace('[^\w\s]','')
    dfppm[['sat1_oe','cleaned']].head(10)
    
    
    # In[13]:
    
    #Stopwords removal
    def prepareStopWords():
     
        stopwordsList = []
     
        # Load default stop words and add a few more specific to my text.
        stopwordsList = stopwords.words('english')
        stopwordsList.append('dont')
        stopwordsList.append('didnt')
        stopwordsList.append('doesnt')
        stopwordsList.append('cant')
        stopwordsList.append('couldnt')
        stopwordsList.append('couldve')
        stopwordsList.append('im')
        stopwordsList.append('ive')
        stopwordsList.append('isnt')
        stopwordsList.append('theres')
        stopwordsList.append('wasnt')
        stopwordsList.append('wouldnt')
        stopwordsList.append('a')
        stopwordsList.append('also')
        stopwordsList.append('could')
        stopwordsList.append('would')
        stopwordsList.append('might')
        stopwordsList.append('may')
     
        return stopwordsList
    
    stop = prepareStopWords()
    stop = [i.replace("'","") for i in stop]
    
    dfppm['bagofwords'] = dfppm['cleaned'].apply(lambda x: " ".join(x for x in x.split() if x not in stop))
    dfppm[['sat1_oe','cleaned','bagofwords']].head(10)
    
    
    # In[14]:
    
    #common words removal
    #selecting only 5 because if it is more than 10 then the token reimbursement will be lost
    freq = pd.Series(' '.join(dfppm['bagofwords']).split()).value_counts()
    print (freq)
    
    
    # In[108]:
    
    #common words removal
    #selecting only 5 because if it is more than 10 then the token reimbursement will be lost
    freq10 = pd.Series(' '.join(dfppm['bagofwords']).split()).value_counts()[:10]
    print (freq10)
    
    
    # In[287]:
    
    #common words removal
    #selecting only 5 because if it is more than 10 then the token reimbursement will be lost
    freq5 = pd.Series(' '.join(dfppm['bagofwords']).split()).value_counts()[:6]
    print (freq5)
    
    
    # In[242]:
    
    type(freq5)
    
    
    # In[243]:
    
    freq5.index
    
    
    # In[15]:
    
    freq_s = freq.loc[['uhc','insurance','unitedhealthcare','unitedhealthcares','patients','patient','insurances','united','uniteds','healthcare'],]
    freq_s
    
    
    # In[16]:
    
    #all_words=pd.Series(' '.join(dfppm['bagofwords']).split()).value_counts()
    #freq5 = list(freq5.index)
    dfppm['bagofwords'] = dfppm['bagofwords'].apply(lambda x: " ".join(x for x in x.split() if x not in freq_s))
    dfppm[['sat1_oe','cleaned','bagofwords']].head(10)
    
    
    # In[17]:
    
    #Rare words removal
    #Optional
    in_freq=freq = pd.Series(' '.join(dfppm['bagofwords']).split()).value_counts()[-5:]
    print (in_freq)
    
    
    # In[18]:
    
    #Optional
    in_freq = list(in_freq.index)
    dfppm['bagofwords_rarewords'] = dfppm['bagofwords'].apply(lambda x: " ".join(x for x in x.split() if x not in in_freq))
    dfppm.columns
    
    
    # In[116]:
    
    #Spelling corrections
    
    #spell_checked_comments = dfppm['bagofwords'].apply(lambda t: str(TextBlob(t).correct()))
    #dfppm['spell_checked'] = spell_checked_comments
    #dfppm[['sat1_oe','cleaned','spell_checked','bagofwords']].head(20)
    
    
    # In[19]:
    
    print (dfppm.columns)
    #Stemming
    st = PorterStemmer()
    dfppm['stemmed_text']=dfppm['bagofwords'].apply(lambda x: " ".join([st.stem(word) for word in x.split()]))
    dfppm['stemmed_text'].head(10)
    
    
    # In[20]:
    
    #Lemmatization
    #fb_corpus = " ".join(t for t in total_df['feedback'])
    #wnl = nltk.WordNetLemmatizer()
    #content_tokens = fb_corpus.split(" ")
    #cleaned_tokens = [x for x in content_tokens if x is not ""]
    #CORPUS_tokens = [wnl.lemmatize(t) for t in cleaned_tokens]
    #CORPUS = " ".join(CORPUS_tokens)
    
    from textblob import Word
    dfppm['bagofwords'] = dfppm['bagofwords'].apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()]))
    dfppm['bagofwords'].head(5)
    
    
    # In[21]:
    
    #TF-IDF matrix
    
    tfidf = TfidfVectorizer(max_features=1000, lowercase=True, analyzer='word',
                            stop_words= 'english',ngram_range=(1,1))
    sklearn_tfidf = TfidfVectorizer(norm='l2', min_df=0, use_idf=True, smooth_idf=False, sublinear_tf=False)
    tfidf_set = sklearn_tfidf.fit_transform(dfppm['bagofwords'])
    tfidf_set
    
    
    # In[38]:
    
    #Polarity
    sia = SentimentIntensityAnalyzer()
    dfppm['polarity'] = dfppm['cleaned'].apply(lambda s: sia.polarity_scores(s))
    dfppm['polarity_compound'] = dfppm['cleaned'].apply(lambda s: sia.polarity_scores(s)['compound'])
    dfppm['polarity_positive'] = dfppm['cleaned'].apply(lambda s: sia.polarity_scores(s)['pos'])
    dfppm['polarity_negative'] = dfppm['cleaned'].apply(lambda s: sia.polarity_scores(s)['neg'])
    dfppm['polarity_neutral'] = dfppm['cleaned'].apply(lambda s: sia.polarity_scores(s)['neu'])
    dfppm['subjectivity'] = dfppm['cleaned'].apply(lambda s: TextBlob(s).sentiment.subjectivity)
    #total_df.to_csv(os.path.join(path,'new_scores_ppm.csv'),index=False)
    
    dfppm[['sat1_oe','cleaned','bagofwords','polarity','polarity_compound','polarity_positive','polarity_negative','polarity_neutral']].head(10)
    
    #Tested with both 'cleaned' and 'bagofwords' headers to see how sentiment values are varying
    
    
    # In[24]:
    
    dfppm.shape
    
    
    # In[172]:
    
    dfppm.columns
    
    
    # In[25]:
    
    parent_df = dfppm
    
    
    # In[26]:
    
    parent_df.shape
    
    
    # In[175]:
    
    parent_df.dtypes
    
    
    # In[27]:
    
    pd.Categorical(parent_df['sat1']).categories
    
    
    # In[28]:
    
    parent_df.isnull().sum()
    
    
    # In[31]:
    
    parent_df = parent_df[parent_df['sat1']!='nan']
    parent_df.shape
    
    
    # In[29]:
    
    parent_df.select_dtypes(include=['O']).columns
    #sat2 is a string here - actually should be numeric 
    
    
    # In[30]:
    
    parent_df['sat1'] = parent_df['sat1'].astype(int)
    parent_df.select_dtypes(include=['int32','int64']).columns
    
    
    # In[31]:
    
    pos_ppm_nps = parent_df[(parent_df['sat1'] == 9) |
                            (parent_df['sat1'] == 10)]
    
    neu_ppm_nps = parent_df[(parent_df['sat1'] == 8)]
    neg_ppm_nps = parent_df[parent_df['sat1'] < 8]
    
    
    # In[32]:
    
    pos_ppm_nps.shape
    
    
    # In[36]:
    
    neg_ppm_nps.shape
    
    
    # In[134]:
    
    neu_ppm_nps.shape
    
    
    # In[42]:
    
    for ind,row in parent_df.iterrows():
        if (parent_df.loc[ind,'sat1'] == 8):
            parent_df.loc[ind,'sentiment'] = 'neutral'
        elif (parent_df.loc[ind,'sat1']<8):
            parent_df.loc[ind,'sentiment'] = 'negative'
        elif (parent_df.loc[ind,'sat1'] > 8):
            parent_df.loc[ind,'sentiment'] = 'positive'
            
    value_cnts_actual = parent_df['sentiment'].value_counts()
    print (value_cnts_actual)
    
    
    # In[43]:
    
    for ind,row in parent_df.iterrows():
        if (parent_df.loc[ind,'polarity_positive']>parent_df.loc[ind,'polarity_negative']):
            parent_df.loc[ind,'sentiment_predicted'] = 'positive'
        elif (parent_df.loc[ind,'polarity_positive']<parent_df.loc[ind,'polarity_negative']):
            parent_df.loc[ind,'sentiment_predicted'] = 'negative'
        elif (parent_df.loc[ind,'polarity_positive']==parent_df.loc[ind,'polarity_negative']):
            parent_df.loc[ind,'sentiment_predicted'] = 'neutral'
            
    value_cnts_pred = parent_df['sentiment_predicted'].value_counts()
    print (value_cnts_pred)
    

    # In[44]:
    
    actuals = parent_df['sentiment']
    predicted = parent_df['sentiment_predicted']
    
    actuals_list = parent_df['sentiment'].tolist()
    predicted_list = parent_df['sentiment_predicted'].tolist()
    
    vader_conf_matrix = pd.crosstab(actuals,predicted)
    
    confusionMatrix = ConfusionMatrix(actuals_list,predicted_list)
    confusionMatrix.print_stats()
    
    cmatrix = confusion_matrix(actuals_list,predicted_list)
    print (classification_report(actuals_list,predicted_list))
    accuracy_score(actuals_list,predicted_list)
    
    
    # In[45]:
    
    parent_df['textblob_polarity'] = parent_df['cleaned'].apply(lambda s: TextBlob(s).sentiment.polarity)
    
    
    # In[41]:
    
    parent_df.columns
    
    
    # In[46]:
    
    for ind,row in parent_df.iterrows():
        if (parent_df.loc[ind,'textblob_polarity']>0):
            parent_df.loc[ind,'textblob_sentiment'] = 'positive'
        elif (parent_df.loc[ind,'textblob_polarity']<0):
            parent_df.loc[ind,'textblob_sentiment'] = 'negative'
        elif (parent_df.loc[ind,'textblob_polarity']==0):
            parent_df.loc[ind,'textblob_sentiment'] = 'neutral'
        
    
    textblob_sentiments = parent_df['textblob_sentiment'].tolist()
    tb_confMatrix = ConfusionMatrix(actuals_list,textblob_sentiments)
    #tb_cm = pd.crosstab(actuals_list,textblob_sentiments)
    
    tb_confMatrix.print_stats()
    
    finalCols = list(original_cols) + ['polarity_compound','polarity_positive','polarity_negative','polarity_neutral','sentiment','sentiment_predicted']
    visualdf = parent_df[finalCols]
    return (visualdf)
    
# In[47]:

def visuals(parent_df,filter_value):
    def BarCharts(diction,dictList,chartname):
        df_sentiments = pd.DataFrame(diction,index=['positive','negative','neutral'])
        df_sT = df_sentiments.T
        N = len(dictList)
        ind = np.arange(N)  # the x locations for the groups
        width = 0.27       # the width of the bars
        fig = plt.figure()
        ax = fig.add_subplot(111)
        posvals = list(df_sT.positive)
        rects1 = ax.bar(ind, posvals, width, color='g')
        negvals = list(df_sT.negative)
        rects2 = ax.bar(ind+width, negvals, width, color='r')
        neuvals = list(df_sT.neutral)
        rects3 = ax.bar(ind+width*2,neuvals, width, color='b')
    
        ax.set_ylabel('Sentiment_Scores')
        ax.set_xticks(ind+width)
        ax.set_xticklabels(dictList)
        ax.legend( (rects1[0], rects2[0], rects3[0]), ('pos', 'neg', 'neu') )
        #plt.show()
        full_path = os.getcwd() + '/static/img/' + chartname
        plt.savefig(full_path)
        return (full_path)
        
    if filter_value == 'Region':
        regions = pd.Categorical(parent_df['region']).categories
        region_sent = {}
        for region in regions:
            specific = parent_df[parent_df['region']==region]
            pos_sent = len(specific[specific['sentiment_predicted']=='positive'])
            neg_sent = len(specific[specific['sentiment_predicted']=='negative'])
            neu_sent = len(specific[specific['sentiment_predicted']=='neutral'])
            region_sent[region] = [pos_sent,neg_sent,neu_sent]
        chartName = 'Sentiments_' + filter_value + '.png'
        return (BarCharts(region_sent,regions,chartName))
    elif filter_value == 'Health Plan':
        health_plans = pd.Categorical(parent_df['healthplan']).categories
        hp_sent = {}
        for hp in health_plans:
            specific = parent_df[parent_df['healthplan']==hp]
            pos_sent = len(specific[specific['sentiment_predicted']=='positive'])
            neg_sent = len(specific[specific['sentiment_predicted']=='negative'])
            neu_sent = len(specific[specific['sentiment_predicted']=='neutral'])
            hp_sent[hp] = [pos_sent,neg_sent,neu_sent]
        chartName = 'Sentiments_' + filter_value + '.png'
        return (BarCharts(hp_sent,health_plans,chartName))
    elif filter_value == 'Quarter':
        quarters = pd.Categorical(parent_df['rptqtr']).categories
        qt_sent = {}
        for q in quarters:
            specific = parent_df[parent_df['rptqtr']==q]
            pos_sent = len(specific[specific['sentiment_predicted']=='positive'])
            neg_sent = len(specific[specific['sentiment_predicted']=='negative'])
            neu_sent = len(specific[specific['sentiment_predicted']=='neutral'])
            qt_sent[q] = [pos_sent,neg_sent,neu_sent]
        chartName = 'Sentiments_' + filter_value + '.png'
        return (BarCharts(qt_sent,quarters,chartName))
    
    
    # In[48]:
  
        
def JunkStuff():        
    parent_df.columns
    
    
    # In[49]:
    
    parent_df.head(5)
    
    
    # In[50]:
    
    parent_df['medicare_flag'].head(10)
    
    
    # In[51]:
    
    parent_df['medicare_flag'].value_counts()
    
    
    # In[52]:
    
    parent_df['cands_flag'].value_counts()
    
    
    # In[53]:
    
    for ind,row in parent_df.iterrows():
        if row['medicare_flag']=='1' and row['cands_flag']=='1':
            parent_df.loc[ind,'LOB'] = 'M&R and C&S'
        elif row['medicare_flag']=='0' and row['cands_flag']=='0':
            parent_df.loc[ind,'LOB'] = 'Others'
        elif row['medicare_flag']=='' and row['cands_flag']=='0':
            parent_df.loc[ind,'LOB'] = 'Others'
        elif row['medicare_flag']=='0' and row['cands_flag']=='1':
            parent_df.loc[ind,'LOB'] = 'C&S'
        elif row['medicare_flag']=='1' and row['cands_flag']=='0':
            parent_df.loc[ind,'LOB'] = 'M&R'
        elif row['medicare_flag']=='' and row['cands_flag']=='1':
            parent_df.loc[ind,'LOB'] = 'C&S'
    
    
    # In[54]:
    
    parent_df.shape
    
    
    # In[55]:
    
    parent_df.columns
    
    
    # In[65]:
    
    PATH = 'C:\\Users\\cvikas10\\Desktop\\VOP_POC'
    
    
    # In[ ]:
    
    parent_df.to_csv(os.path.join(PATH,'Base_File_Analytics.txt'),sep='\t',index=False)
    
    
    # In[210]:
    
    tfidf = TfidfVectorizer(max_features=1000, lowercase=True, analyzer='word',
                            stop_words= 'english',ngram_range=(1,1))
    sklearn_tfidf = TfidfVectorizer(norm='l2', min_df=0, use_idf=True, smooth_idf=False, sublinear_tf=False)
    tfidf_set = sklearn_tfidf.fit_transform([parent_df['bagofwords'][7]])
    
    feature_array = np.array(sklearn_tfidf.get_feature_names())
    tfidf_sorting = np.argsort(tfidf_set.toarray()).flatten()[::-1]
    
    n = 10
    
    top_nwords = feature_array[tfidf_sorting][:n]
    top_nwords
    
    
    # In[56]:
    
    parent_df.shape
    
    
    # In[78]:
    
    parent_df['TOPICS'] = ['']*parent_df.shape[0]   
    for ind,row in parent_df.iterrows():
        try:
            comment = row['bagofwords']
            sklearn_tfidf = TfidfVectorizer(norm='l2', min_df=0, use_idf=True, smooth_idf=False, sublinear_tf=False)
            tfidf_set = sklearn_tfidf.fit_transform([comment])
            feature_array = np.array(sklearn_tfidf.get_feature_names())
            tfidf_sorting = np.argsort(tfidf_set.toarray()).flatten()[::-1]
        
            n = 10
            top_nwords = feature_array[tfidf_sorting][:n]
            top_nwords=[word for word in top_nwords if len(word)>=4]
            parent_df.loc[ind,'TOPICS'] = '|'.join(top_nwords)
        except:
            continue
    
    
    # In[79]:
    
    parent_df.shape
    
    
    # In[54]:
    
    parent_df.to_csv(os.path.join(PATH,'Final_File.txt'),
                     sep='\t',
                     index=False)
    
    
    # In[268]:
    
    'TOPICS' in parent_df.columns
    
    
    # In[74]:
    
    def bigram_colwise(col):
        tokens = word_tokenize(col)
        tokens = [s for s in tokens if len(s)>=4]
        finder = BigramCollocationFinder.from_words(tokens)
        bigram_measures = BigramAssocMeasures()
        scored = finder.score_ngrams(bigram_measures.raw_freq)
        scoredList = sorted(scored, key=itemgetter(1), reverse=True)
        word_dict = {}
        listLen = len(scoredList)
        for i in range(listLen):
            word_dict['_'.join(scoredList[i][0])] = scoredList[i][1]
        return list(word_dict.keys())[:4]
    
    parent_df['BIGRAMS_TOPICS'] = parent_df['bagofwords'].apply(lambda c: '|'.join(bigram_colwise(c)))
    
    
    # In[75]:
    
    parent_df.shape
    
    
    # In[76]:
    
    parent_df.columns
    
    
    # In[80]:
    
    parent_df.to_csv(os.path.join(PATH,'FinalFile.txt'),
                     sep='\t',
                     index=False)


# In[ ]:




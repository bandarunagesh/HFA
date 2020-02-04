
from nlp_modules import *

def preProcess_data(df):
    df_ppm = df
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
    junk_words = ['uhc','insurance','unitedhealthcare','unitedhealthcares',
                  'patients','patient','insurances','united','uniteds','healthcare']
    freq_s = freq.loc[junk_words,]
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
    
    return (dfppm)
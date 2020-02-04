
# coding: utf-8

# In[34]:

import pyLDAvis
import pyLDAvis.sklearn
#pyLDAvis.enable_notebook()
import gensim
from processData import *

# In[93]:

import sys
#sys.path.insert(0,'C:/Users/cvikas10/Documents/Python Programs')

from nlp_modules import *

pd.options.mode.chained_assignment = None


def topicVisuals(df):
    
    parent_df = preProcess_data(df)
    
    parent_df['sat1'] = parent_df['sat1'].astype(int)
    # In[8]:
    
    parent_df['bagofwords'].head(10)
    
    
    # In[9]:
    
    df = parent_df
    
    
    # In[10]:
    
    #Segmenting the complete data frame based on the quarter
    df_q1 = df[df['rptqtr']=='201603']
    df_q2 = df[df['rptqtr']=='201604']
    df_q3 = df[df['rptqtr']=='201701']
    df_q4 = df[df['rptqtr']=='201702']
    df_q5 = df[df['rptqtr']=='201703']
    df_q6 = df[df['rptqtr']=='201704']
    df_q7 = df[df['rptqtr']=='201801']
    df_q8 = df[df['rptqtr']=='201802']
    df_q9 = df[df['rptqtr']=='201803']
    
    df_q1['sat1']=df_q1['sat1'].astype(int)
    df_q2['sat1']=df_q2['sat1'].astype(int)
    df_q3['sat1']=df_q3['sat1'].astype(int)
    df_q4['sat1']=df_q4['sat1'].astype(int)
    df_q5['sat1']=df_q5['sat1'].astype(int)
    df_q6['sat1']=df_q6['sat1'].astype(int)
    df_q7['sat1']=df_q7['sat1'].astype(int)
    df_q8['sat1']=df_q8['sat1'].astype(int)
    df_q9['sat1']=df_q9['sat1'].astype(int)
    
    print (df_q1.shape)
    print (df_q2.shape)
    print (df_q3.shape)
    print (df_q4.shape)
    print (df_q5.shape)
    print (df_q6.shape)
    print (df_q7.shape)
    print (df_q8.shape)
    print (df_q9.shape)
    
    
    # In[11]:
    
    #Topic modelling
    
    #First tokenizing the data sentence wise and then after that word wise to avoid missing characters like punctuation
    def tokenize_only(text):
        # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
        tokens = [word.lower() for sent in nltk.sent_tokenize(str(text)) for word in nltk.word_tokenize(sent)]
        filtered_tokens = []
        # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
        for token in tokens:
            if re.search('[a-zA-Z]', token):
                filtered_tokens.append(token)
        return filtered_tokens
    
    
    # In[12]:
        
    word_list = tokenize_only(df['bagofwords'].tolist())
    stop_words = stopwords.words('english')
    
    filtered_words = [word for word in word_list if word.lower().strip() not in stop_words]
    
    tfidf_vect = TfidfVectorizer(norm='l2', min_df=0, use_idf=True, 
                                 smooth_idf=False, sublinear_tf=False)
    count_vect = CountVectorizer(max_df=0.80,max_features=50000)
    
    X = tfidf_vect.fit_transform(filtered_words)
    _X_ = count_vect.fit_transform(filtered_words)
    
    dense_matrix = _X_.todense()
    
    print("Sparsity: ", ((dense_matrix > 0).sum()/dense_matrix.size)*100, "%")
    
    n_components = 10
    lda = LatentDirichletAllocation(n_components=n_components,
                                    learning_method='batch', 
                                    max_iter=25,random_state=0)
    document_topics = lda.fit_transform(_X_).T
    sorting = np.argsort(lda.components_,axis=1)[:,::-1]
    feature_names = np.array(count_vect.get_feature_names())
    mglearn.tools.print_topics(topics=range(n_components),feature_names=feature_names,
                               sorting=sorting,topics_per_chunk=5,n_words=10)
    # Log Likelyhood: Higher the better
    print("Log Likelihood using tf-idf: ", lda.score(_X_))
    print("Perplexity using tf-idf: ", lda.perplexity(_X_))
    # In[13]:
        
    lda_model,countMatrix,countVectorizer,tfidfMatrix,tfidfVectorizer = lda,_X_,count_vect,X,tfidf_vect
         
    p = pyLDAvis.sklearn.prepare(lda_model,countMatrix,countVectorizer,mds='mmds')
    visual_file = 'visuals.html'
    pyLDAvis.save_html(p,os.getcwd() + '/templates/' + visual_file)

    # In[14]:
    
    detract_df = parent_df[parent_df['sat1']<8]
    
    promo_df = parent_df[parent_df['sat1']>8]
    
    return (visual_file)

# In[19]:
    

def word2Vec():

    detract_df_docs = [word_tokenize(doc) for doc in detract_df['bagofwords']]
    
    
    # In[49]:
    
    detract_df_docs
    
    
    # In[20]:
    
    # build vocabulary and train model
    model = gensim.models.Word2Vec(detract_df_docs,
                                    size=150,
                                    window=10,
                                    min_count=2,
                                    workers=10)
    
    
    # In[21]:
    
    model.train(detract_df_docs, total_examples=len(detract_df_docs), epochs=15)
    
    
    # In[22]:
    
    model.wv.most_similar(positive='eob')
    
    
    # In[23]:
    
    model.wv.most_similar(positive='representative')
    
    
    # In[24]:
    
    model.wv.most_similar(positive='reimbursement')
    
    
    # In[25]:
    
    model.wv.most_similar(positive='referrals')
    
    
    # In[57]:
    
    model.wv.most_similar(positive='authorizations')
    
    
    # In[26]:
    
    model.wv.most_similar(positive='bcbs')
    
    
    # In[61]:
    
    model.wv.most_similar(positive='schedule')
    
    
    # In[62]:
    
    model.wv.most_similar(positive='aarp')
    
    
    # In[63]:
    
    model.wv.most_similar(positive='precertification')
    
    
    # In[67]:
    
    model.wv.most_similar(positive='formulary')
    
    
    # In[68]:
    
    model.wv.most_similar(positive='new')
    
    
    # In[27]:
    
    model.wv.vocab
    
    
    # In[71]:
    
    from sklearn.manifold import TSNE
    vocab = list(model.wv.vocab)
    X = model[vocab]
    tsne = TSNE(n_components=2)
    X_tsne = tsne.fit_transform(X)
    
    
    # In[72]:
    
    df = pd.DataFrame(X_tsne, index=vocab, columns=['x', 'y'])
    
    
    # In[85]:
    
    df.head(100)
    
    
    # In[76]:
    
    df.shape
    
    
    # In[82]:
    
    df.index
    
    
    # In[80]:
    
    fig = plt.figure(figsize = (10,20))
    ax = fig.add_subplot(1, 1, 1)
    ax.scatter(df['x'], df['y'])
    for word, pos in df[:100].iterrows():
        ax.annotate(word, pos)
    plt.show()
    
    
    # In[84]:
    
    fig = plt.figure(figsize = (10,20))
    ax = fig.add_subplot(1, 1, 1)
    ax.scatter(df['x'], df['y'])
    for word, pos in df[:200].iterrows():
        ax.annotate(word, pos)
    plt.show()
    
    
    # In[87]:
    
    model.wv.most_similar(positive='patients')
    
    
    # In[88]:
    
    model.wv.most_similar(positive='notoriously')
    
    
    # In[95]:
    
    model.wv.most_similar(positive='consuming')
    
    
    # In[96]:
    
    model.wv.most_similar(positive='medications')
    
    
    # In[99]:
    
    model.wv.most_similar(positive='appeal')
    
    
    # In[100]:
    
    model.wv.most_similar(positive='website')
    
    
    # In[101]:
    
    model.wv.most_similar(positive='communication')
    
    
    # In[102]:
    
    model.wv.most_similar(positive='eligibility')
    
    
    # In[103]:
    
    model.wv.most_similar(positive='credentialing')
    
    
    # In[104]:
    
    model.wv.most_similar(positive='incorrect')
    
    
    # In[105]:
    
    model.wv.most_similar(positive='specialist')
    
    
    # In[50]:
    
    parent_df.columns
    
    
    # In[51]:
    
    parent_df.shape
    
    
    # In[105]:
    
    parent_df['medicare_flag'].value_counts()
    
    
    # In[53]:
    
    parent_df.isnull().sum()
    
    
    # In[104]:
    
    parent_df.dtypes
    
    
    # In[106]:
    
    parent_df[parent_df['medicare_flag']==''].shape
    
    
    # In[103]:
    
    parent_df['medicare_flag'].head(10)
    
    
    # In[59]:
    
    #parent_df['medicare_flag'].replace(np.nan,'',inplace=True)
    
    
    # In[60]:
    
    parent_df['medicare_flag'].head(10)
    
    
    # In[107]:
    
    parent_df['cands_flag'].isnull().sum()
    
    
    # In[108]:
    
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
    
    
    # In[64]:
    
    parent_df.columns
    
    
    # In[109]:
    
    parent_df[['medicare_flag','cands_flag','LOB']].head(20)
    
    
    # In[110]:
    
    parent_df['LOB'].value_counts()
    
    
    # In[68]:
    
    health_plans = pd.Categorical(parent_df['healthplan']).categories
    regions = pd.Categorical(parent_df['region']).categories
    lobs = pd.Categorical(parent_df['LOB']).categories
    print (health_plans)
    print (regions)
    print (lobs)
    print (len(health_plans))
    print (len(regions))
    print (len(lobs))
    
    
    # In[111]:
    
    MR_df = parent_df[parent_df['LOB'] == 'M&R']
    CS_df = parent_df[parent_df['LOB'] == 'C&S']
    bothlobs_df = parent_df[parent_df['LOB'] == 'M&R and C&S']
    others_df = parent_df[parent_df['LOB'] == 'Others']
    
    
    # In[112]:
    
    MR_df.shape
    
    
    # In[74]:
    
    CS_df.shape
    
    
    # In[75]:
    
    bothlobs_df.shape
    
    
    # In[76]:
    
    others_df.shape
    
    
    # In[122]:
    
    word_list = tokenize_only(MR_df['bagofwords'].tolist())
    stop_words = stopwords.words('english')
    
    filtered_words = [word for word in word_list if word.lower().strip() not in stop_words]
    
    tfidf_vect = TfidfVectorizer(norm='l2', min_df=0, use_idf=True, 
                                 smooth_idf=False, sublinear_tf=False)
    count_vect = CountVectorizer(max_df=0.80,max_features=50000)
    
    X = tfidf_vect.fit_transform(filtered_words)
    _X_ = count_vect.fit_transform(filtered_words)
    
    dense_matrix = _X_.todense()
    
    print("Sparsity: ", ((dense_matrix > 0).sum()/dense_matrix.size)*100, "%")
    
    n_components = 5
    lda = LatentDirichletAllocation(n_components=n_components,
                                    learning_method='batch', 
                                    max_iter=25,random_state=0)
    document_topics = lda.fit_transform(_X_).T
    sorting = np.argsort(lda.components_,axis=1)[:,::-1]
    feature_names = np.array(count_vect.get_feature_names())
    mglearn.tools.print_topics(topics=range(n_components),feature_names=feature_names,
                               sorting=sorting,topics_per_chunk=5,n_words=10)
    # Log Likelyhood: Higher the better
    print("Log Likelihood using tf-idf: ", lda.score(_X_))
    print("Perplexity using tf-idf: ", lda.perplexity(_X_))
    
    
    # In[123]:
    
    pyLDAvis.sklearn.prepare(lda, _X_, count_vect, mds = 'mmds')
    
    
    # In[116]:
    
    word_list = tokenize_only(CS_df['bagofwords'].tolist())
    stop_words = stopwords.words('english')
    
    filtered_words = [word for word in word_list if word.lower().strip() not in stop_words]
    
    tfidf_vect = TfidfVectorizer(norm='l2', min_df=0, use_idf=True, 
                                 smooth_idf=False, sublinear_tf=False)
    count_vect = CountVectorizer(max_df=0.80,max_features=50000)
    
    X = tfidf_vect.fit_transform(filtered_words)
    _X_ = count_vect.fit_transform(filtered_words)
    
    dense_matrix = _X_.todense()
    
    print("Sparsity: ", ((dense_matrix > 0).sum()/dense_matrix.size)*100, "%")
    
    n_components = 10
    lda = LatentDirichletAllocation(n_components=n_components,
                                    learning_method='batch', 
                                    max_iter=25,random_state=0)
    document_topics = lda.fit_transform(_X_).T
    sorting = np.argsort(lda.components_,axis=1)[:,::-1]
    feature_names = np.array(count_vect.get_feature_names())
    mglearn.tools.print_topics(topics=range(n_components),feature_names=feature_names,
                               sorting=sorting,topics_per_chunk=5,n_words=10)
    # Log Likelyhood: Higher the better
    print("Log Likelihood using tf-idf: ", lda.score(_X_))
    print("Perplexity using tf-idf: ", lda.perplexity(_X_))
    
    
    # In[117]:
    
    pyLDAvis.sklearn.prepare(lda, _X_, count_vect, mds = 'mmds')
    
    
    # In[118]:
    
    word_list = tokenize_only(bothlobs_df['bagofwords'].tolist())
    stop_words = stopwords.words('english')
    
    filtered_words = [word for word in word_list if word.lower().strip() not in stop_words]
    
    tfidf_vect = TfidfVectorizer(norm='l2', min_df=0, use_idf=True, 
                                 smooth_idf=False, sublinear_tf=False)
    count_vect = CountVectorizer(max_df=0.80,max_features=50000)
    
    X = tfidf_vect.fit_transform(filtered_words)
    _X_ = count_vect.fit_transform(filtered_words)
    
    dense_matrix = _X_.todense()
    
    print("Sparsity: ", ((dense_matrix > 0).sum()/dense_matrix.size)*100, "%")
    
    n_components = 10
    lda = LatentDirichletAllocation(n_components=n_components,
                                    learning_method='batch', 
                                    max_iter=25,random_state=0)
    document_topics = lda.fit_transform(_X_).T
    sorting = np.argsort(lda.components_,axis=1)[:,::-1]
    feature_names = np.array(count_vect.get_feature_names())
    mglearn.tools.print_topics(topics=range(n_components),feature_names=feature_names,
                               sorting=sorting,topics_per_chunk=5,n_words=10)
    # Log Likelyhood: Higher the better
    print("Log Likelihood using tf-idf: ", lda.score(_X_))
    print("Perplexity using tf-idf: ", lda.perplexity(_X_))
    
    
    # In[119]:
    
    pyLDAvis.sklearn.prepare(lda, _X_, count_vect, mds = 'tsne')
    
    
    # In[120]:
    
    word_list = tokenize_only(others_df['bagofwords'].tolist())
    stop_words = stopwords.words('english')
    
    filtered_words = [word for word in word_list if word.lower().strip() not in stop_words]
    
    tfidf_vect = TfidfVectorizer(norm='l2', min_df=0, use_idf=True, 
                                 smooth_idf=False, sublinear_tf=False)
    count_vect = CountVectorizer(max_df=0.80,max_features=50000)
    
    X = tfidf_vect.fit_transform(filtered_words)
    _X_ = count_vect.fit_transform(filtered_words)
    
    dense_matrix = _X_.todense()
    
    print("Sparsity: ", ((dense_matrix > 0).sum()/dense_matrix.size)*100, "%")
    
    n_components = 10
    lda = LatentDirichletAllocation(n_components=n_components,
                                    learning_method='batch', 
                                    max_iter=25,random_state=0)
    document_topics = lda.fit_transform(_X_).T
    sorting = np.argsort(lda.components_,axis=1)[:,::-1]
    feature_names = np.array(count_vect.get_feature_names())
    mglearn.tools.print_topics(topics=range(n_components),feature_names=feature_names,
                               sorting=sorting,topics_per_chunk=5,n_words=10)
    # Log Likelyhood: Higher the better
    print("Log Likelihood using tf-idf: ", lda.score(_X_))
    print("Perplexity using tf-idf: ", lda.perplexity(_X_))
    
    
    # In[121]:
    
    pyLDAvis.sklearn.prepare(lda, _X_, count_vect, mds = 'mmds')
    

# In[ ]:





# coding: utf-8

# In[1]:

import nltk
from nltk.corpus import stopwords
import os
import pandas as pd
from wordcloud import WordCloud
from matplotlib import pyplot as plt
import re
import nltk.collocations
from nltk.collocations import *
from operator import itemgetter
WNL = nltk.WordNetLemmatizer()
#import sys
#sys.path.insert(0,'C:/Users/cvikas10/Documents/Python Programs')

from nlp_modules import *

file_path = os.getcwd()

def wordCloud_Visuals(df,file_path,ngrams,number_of_entities):
    data  = df
    
    # In[21]:
    
    data.shape
    #9101 records Total #10 records - No overall satisfaction 
    
    #4945 records have comments present (Excluding comments having NULL Comments)
    
    
    # In[8]:
    
    data['rptqtr'].value_counts().sort_index()
    
    
    # In[3]:
    
    data['region'].value_counts()
    
    
    # In[5]:
    
    data['healthplan'].value_counts().head(20)
    
    
    # In[24]:
    
    data.columns
    
    
    # In[48]:
    
    data.describe()
    
    
    # In[39]:
    
    data.info()
    
    
    # In[33]:
    
    data[['sat1','sat1_oe']].head(10)
    
    
    # In[47]:
    
    selected_cols = data[['sat1','sat1_oe','rptqtr','region','healthplan']]
    selected_cols.dtypes
    
    
    # In[46]:
    
    print (data.dtypes)
    
    
    # In[3]:
    
    print (data.isnull().sum())
    comments = data[(data['sat1_oe'].notnull()) & (data['sat1_oe'] != ' ')]
    print ('\n')
    print (comments.shape)
    
    
    # In[4]:
    
    #Appending all the comments into one single paragraph separated by spaces
    corpus = " ".join(c for c in comments['sat1_oe'])
    
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
        stopwordsList.append('healthcare')
        stopwordsList.append('unitedhealthcare')
        stopwordsList.append('uhc')
        stopwordsList.append('insurance')
     
        return stopwordsList
    
    
    rawText = corpus
    rawText = rawText.lower()
    print (rawText[:300])
    
    
    # In[5]:
    
    # Remove single quote early since it causes problems with the tokenizer.
    # wasn't turns into 2 entries; was, n't.
    rawText = rawText.replace("'", "")
    
    #Tokenizing the text into word tokens
    tokens = nltk.word_tokenize(rawText)
    text = nltk.Text(tokens)
    print (tokens[:100])
    
    
    # In[6]:
    
    # Load default stop words and add a few more.
    stopWords = prepareStopWords()
    text_content = [''.join(re.split("[ .,;:!?‘’``''@#$%^_&*()<>{}~\n\t\\\-]", word)) for word in text]
    print (text_content[:100])
    
    
    # In[7]:
    
    #Removing Stop words
    text_content = [word for word in text_content if word not in stopWords]
    
    #Taking tokens which have length greater than or equal to 4 - to drop smaller prepositions and verbs
    text_content = [s for s in text_content if len(s) >= 5]
    
    #Lemmatization of tokens - to convert the word into its source form
    text_content = [WNL.lemmatize(t) for t in text_content]
    text_cn = [word for word in text_content]
    print (text_cn[:100])
    
    
    # In[19]:
        
    if ngrams == 2:
    
        #Using Bigram collocations and 
        finder = BigramCollocationFinder.from_words(text_cn)
        bigram_measures = BigramAssocMeasures()
        scored = finder.score_ngrams(bigram_measures.raw_freq)
        scoredList = sorted(scored, key=itemgetter(1), reverse=True)
        word_dict = {}
         
        listLen = len(scoredList)
         
        # Get the bigram and make a contiguous string for the dictionary key. 
        # Set the key to the scored value. 
        for i in range(listLen):
            word_dict['_'.join(scoredList[i][0])] = scoredList[i][1]
            
        #df_scores = pd.DataFrame(word_dict,index=['score'],
        #                         columns=word_dict.keys())
        
        #df_scores = df_scores.T
        #for key in list(word_dict.keys())[:50]:
        #    print ((key,word_dict[key]))
        
        
        # In[14]:
        
        
        #WC_height = 1000
        #WC_width = 1000
        WC_max_words = number_of_entities
        fileName = 'WordCloud_Bigrams_Frequent.png'
        def Word_Cloud(WC_height,WC_width,number_of_entities,fileName,worddict): 
            wordCloud = WordCloud(max_words=number_of_entities, height=WC_height, width=WC_width)
            wordCloud.generate_from_frequencies(worddict)
            plt.title('Most frequently occurring bigrams connected with an underscore_')
            plt.imshow(wordCloud, interpolation='bilinear')
            plt.axis("off")
            #plt.show()
            fileName = fileName.split('.')[0] + '_' + str(number_of_entities) + '.' + fileName.split('.')[1]
            wordCloud.to_file(os.path.join(file_path,'static','img',fileName))
            
        Word_Cloud(1000,1000,number_of_entities,fileName,word_dict)
          
        print("\nWord cloud with least frequently occurring bigrams (connected with an underscore _).")
         
        # On large data sets (>100 for example) there can be a large number of words that occur once.
        # Depending on the max words specified in the word cloud, you can get 30 words of various
        # sizes but they only occur once.
         
        # Sort the list to put the least common terms at the front/top.
        # Infrequent start at the scoredList[0]. The MOST frequent word appears in
        # the last position at scoredList[len(scored)-1]
         
        # Sort lowest to highest based on the score.
        scoredList = sorted(scored, key=itemgetter(1))
         
        scoredListLen = len(scoredList)-1
         
        # There is no need to stuff the dictinary with more words than will be
        # rendered by the word cloud. A counter below will ensure the dictionary
        # doesn't exceed the prior max words configured in the word cloud above.
        maxLenCnt = 0
         
        # Below MIN SCORE is the minimum score from score_ngrams(bigram_measures.raw_freq)
        # that a N-gram need to achieve to be included in the word cloud. This is based
        # solely on looking at N-gram score and manual configuration.
        MINSCORE = 0.0005
         
        # Index for the scored list
        indx = 0
         
        # Find the starting point in the SORTED list where the score of a term
        # is greater than MIN SCORE defined above.
        while (indx < scoredListLen) and (scoredList[indx][1] < MINSCORE):
            indx += 1
            #print("Indx: ", indx)
            #print(scoredList[indx])
         
        # dictionary to hold the scored list with the chosen scores.
        word_dict2 = {}
         
        # Create the dictionary with the bigrams using the starting point found above.
        while (indx < scoredListLen) and (maxLenCnt < WC_max_words):
            word_dict2['_'.join(scoredList[indx][0])] = scoredList[indx][1]
            indx +=  1
            maxLenCnt += 1
         
        # Ensure the dictionary isn't empty before creating word cloud.
        
        if len(word_dict2) > 0:
            lfileName = 'WordCloud_Bigrams_infrequent.png'
            Word_Cloud(1000,1000,number_of_entities,lfileName,word_dict2)
        else:
            print("\nThere were no words to display in the word cloud.")
   
    elif ngrams==3:
        
        #Using Bigram collocations and Trigram collocations
        finder = nltk.collocations.TrigramCollocationFinder.from_words(text_cn)
        trigram_measures = nltk.collocations.TrigramAssocMeasures()
        scored = finder.score_ngrams(trigram_measures.raw_freq)
        scoredList = sorted(scored, key=itemgetter(1), reverse=True)
        word_dict = {}
         
        listLen = len(scoredList)
         
        # Get the bigram and make a contiguous string for the dictionary key. 
        # Set the key to the scored value. 
        for i in range(listLen):
            word_dict['_'.join(scoredList[i][0])] = scoredList[i][1]
            
        #df_scores = pd.DataFrame(word_dict,index=['score'],
        #                         columns=word_dict.keys())
        
        #df_scores = df_scores.T
        #for key in list(word_dict.keys())[:50]:
        #    print ((key,word_dict[key]))
        
        
        # In[14]:
        
        #WC_height = 1000
        #WC_width = 1000
        WC_max_words = number_of_entities
        
        fileName = 'WordCloud_Trigrams_Frequent.png'
        
        def Word_Cloud(WC_height,WC_width,number_of_entities,fileName,worddict): 
            wordCloud = WordCloud(max_words=number_of_entities, height=WC_height, width=WC_width)
            wordCloud.generate_from_frequencies(worddict)
            plt.title('Most frequently occurring bigrams connected with an underscore_')
            plt.imshow(wordCloud, interpolation='bilinear')
            plt.axis("off")
            #plt.show()
            fileName = fileName.split('.')[0] + '_' + str(number_of_entities) + '.' + fileName.split('.')[1]
            wordCloud.to_file(os.path.join(file_path,'static','img',fileName))
        
        
        Word_Cloud(1000,1000,number_of_entities,fileName,word_dict)
        
        print("\nWord cloud with least frequently occurring bigrams (connected with an underscore _).")
         
        # On large data sets (>100 for example) there can be a large number of words that occur once.
        # Depending on the max words specified in the word cloud, you can get 30 words of various
        # sizes but they only occur once.
         
        # Sort the list to put the least common terms at the front/top.
        # Infrequent start at the scoredList[0]. The MOST frequent word appears in
        # the last position at scoredList[len(scored)-1]
         
        # Sort lowest to highest based on the score.
        scoredList = sorted(scored, key=itemgetter(1))
         
        scoredListLen = len(scoredList)-1
         
        # There is no need to stuff the dictinary with more words than will be
        # rendered by the word cloud. A counter below will ensure the dictionary
        # doesn't exceed the prior max words configured in the word cloud above.
        maxLenCnt = 0
         
        # Below MIN SCORE is the minimum score from score_ngrams(bigram_measures.raw_freq)
        # that a N-gram need to achieve to be included in the word cloud. This is based
        # solely on looking at N-gram score and manual configuration.
        MINSCORE = 0.0005
         
        # Index for the scored list
        indx = 0
         
        # Find the starting point in the SORTED list where the score of a term
        # is greater than MIN SCORE defined above.
        while (indx < scoredListLen) and (scoredList[indx][1] < MINSCORE):
            indx += 1
            #print("Indx: ", indx)
            #print(scoredList[indx])
         
        # dictionary to hold the scored list with the chosen scores.
        word_dict2 = {}
         
        # Create the dictionary with the bigrams using the starting point found above.
        while (indx < scoredListLen) and (maxLenCnt < WC_max_words):
            word_dict2['_'.join(scoredList[indx][0])] = scoredList[indx][1]
            indx +=  1
            maxLenCnt += 1
         
        # Ensure the dictionary isn't empty before creating word cloud.
        
        if len(word_dict2) > 0:
            lfileName = 'WordCloud_Trigrams_infrequent.png'
            Word_Cloud(1000,1000,number_of_entities,lfileName,word_dict2)
        else:
            print("\nThere were no words to display in the word cloud.")

        
    # In[20]:
    

# In[51]:

#data[['id','fixid','tin','mpin','npi','region','healthplan','respondent_type','name','phone','email','address','city','state','zipcode']].head(10)


# In[14]:

#data['sat2'] = data['sat2'].astype(str)


# In[11]:

#data.shape


# In[15]:

#data.dtypes


# In[18]:

#data['sat2'].value_counts().sort_index()


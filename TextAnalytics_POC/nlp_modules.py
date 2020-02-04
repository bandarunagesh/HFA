
# coding: utf-8

# In[3]:

import nltk
import pandas as pd
import numpy as np
import stemming
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer, TweetTokenizer, WhitespaceTokenizer
from nltk.classify import NaiveBayesClassifier
from nltk.classify.util import accuracy
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer
from stemming.porter2 import stem
from nltk import PorterStemmer
stemmer = PorterStemmer()
from nltk.collocations import *
import matplotlib.pyplot as pltat
import seaborn as sns
import time
import re
from collections import Counter
import string
from nltk.stem.snowball import SnowballStemmer
from nltk.collocations import BigramAssocMeasures, BigramCollocationFinder
from nltk.chunk import conlltags2tree, tree2conlltags
import pickle
from collections import Iterable
from nltk.tag import ClassifierBasedTagger
from nltk.chunk import ChunkParserI
from nltk import pos_tag, word_tokenize
import os
from operator import itemgetter
from nltk.corpus import brown, stopwords
from nltk.cluster.util import cosine_distance
from sklearn.feature_extraction.text import CountVectorizer
import mglearn
from sklearn.decomposition import LatentDirichletAllocation,TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim.summarization.summarizer import summarize
from gensim.summarization import keywords
from sklearn.model_selection import GridSearchCV
from pprint import pprint
from string import digits
from pandas_ml.confusion_matrix.cm import ConfusionMatrix
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score


# In[ ]:




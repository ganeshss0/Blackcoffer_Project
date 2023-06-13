from src.logger import logging
from src.exception import CustomException
import os
import pandas as pd
from collections import defaultdict
from nltk import word_tokenize
from nltk.probability import FreqDist


class analysis:
    def __init__(self) -> None:
        self.masterdict = {
            'positive' : pd.read_csv(os.path.join('MasterDictionary', 'negitive-words.txt'), header=None, encoding='latin'),
            'negitive' : pd.read_csv(os.path.join('MasterDictionary', 'negative-words.txt'), header=None, encoding='latin')
        }
        self.masterdict['positive'] = defaultdict.fromkeys(self.positive[0])
        self.masterdict['negitive'] = defaultdict.fromkeys(self.negitive[0])
    def preprocess_text(self, data:pd.DataFrame) -> None:
        data.TEXT.fillna('', inplace=True)
        data.TEXT = data.TEXT.str.lower()
        data.TEXT = data.TEXT.str.replace(pat=r'["\.,/“”’\-\?\–]', repl='', regex=True)
        data.TEXT = data.TEXT.apply(word_tokenize)

    def remove_stopwords(self, data:pd.DataFrame) -> None:
        stopwords = pd.DataFrame(columns=[1])
        for root, folder, files in os.walk('StopWords'):
            for file in files:
                words = pd.read_csv(os.path.join(root, file), header=None, index_col=0, sep='|', encoding='latin')
                words.index = words.index.str.lower()
                words[1] = ''
                stopwords = pd.concat((stopwords, words))
        data.TEXT = data.TEXT.apply(lambda tokens : [token for token in tokens if token not in stopwords])
        data.TEXT = data.TEXT.apply(FreqDist)


    def count_words(self, words:dict, Dict:str='positive', factor:int = 1):
        counter = 0
        for word in words:
            if self.masterdict[Dict].get(word, -1) == None:
                counter += words[word]
        return counter * factor
    
    def extract_derived_variable(self, data:pd.DataFrame):
        data['POSITIVE_SCORE'] = data.TEXT.apply(self.count_words, args=('positive',))
        data['NEGATIVE_SCORE'] = data.TEXT.apply(self.count_words, args=('negative',-1,))
        data['POLARITY_SCORE'] = (data.POSITIVE_SCORE + data.NEGATIVE_SCORE) / ((data.POSITIVE_SCORE - data.NEGATIVE_SCORE) + 0.000001)
        data['SUBJECTIVITY_SCORE'] = (data.POSITIVE_SCORE - data.NEGATIVE_SCORE) / (data.TEXT.apply(len) + 0.000001)
    

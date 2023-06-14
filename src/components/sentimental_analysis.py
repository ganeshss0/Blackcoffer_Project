from src.logger import logging
from src.exception import CustomException
import os, sys
import pandas as pd
from collections import defaultdict
from nltk import word_tokenize, pos_tag
from nltk.probability import FreqDist
import syllables
import numpy as np


class Analysis:
    '''Main Analysis Class'''



    def __init__(self) -> None:
        logging.info('Initializing Analysis')
        try:
            logging.info('Reading Master Dictionary')
            self.masterdict = {
                'positive' : pd.read_csv(os.path.join('MasterDictionary', 'positive-words.txt'), header=None, encoding='latin'),
                'negative' : pd.read_csv(os.path.join('MasterDictionary', 'negative-words.txt'), header=None, encoding='latin')
            }
        except Exception as e:
            logging.error(e)
            raise CustomException(e, sys)
        self.masterdict['positive'] = defaultdict.fromkeys(self.masterdict['positive'][0])
        self.masterdict['negative'] = defaultdict.fromkeys(self.masterdict['negative'][0])  




    def preprocess_text(self, data:pd.DataFrame) -> None:
        '''Preprocess the text column in dataframe, removes NaN values, convert string to lowercase, remove punctuations, tokenize.'''

        logging.info('Cleaning Data')
        data.TEXT.fillna('', inplace=True)
        data.TEXT = data.TEXT.str.lower()
        data.TEXT = data.TEXT.str.replace(pat=r'["\.,/“”’\-\?\–]', repl='', regex=True)
        logging.info('Tokenizing Data')
        data.TEXT = data.TEXT.apply(word_tokenize)




    def remove_stopwords(self, data:pd.DataFrame) -> None:
        '''Remove stopwords from text column.'''

        logging.info('Removing StopWords')
        stopwords = pd.DataFrame(columns=[1])

        for root, folder, files in os.walk('StopWords'):
            for file in files:
                words = pd.read_csv(os.path.join(root, file), header=None, index_col=0, sep='|', encoding='latin')
                words.index = words.index.str.lower()
                words[1] = ''
                stopwords = pd.concat((stopwords, words))

        data.TEXT = data.TEXT.apply(lambda tokens : [token for token in tokens if token not in stopwords])
        data.TEXT = data.TEXT.apply(FreqDist)




    def count_words(self, words:dict, Dict:str='positive', factor:int = 1) -> int:
        '''Count words that match the words in the master dictionary.'''

        counter = 0
        for word in words:
            if self.masterdict[Dict].get(word, -1) == None:
                counter += words[word]

        return counter * factor
    



    def extract_derived_variable(self, data:pd.DataFrame) -> None:
        '''Extract postive, negative, polarity, subjectivity score from text and add these to dataframe.'''

        logging.info('Calculating Positive Score')
        data['POSITIVE_SCORE'] = data.TEXT.apply(self.count_words)
        logging.info('Calculating Negative Score')
        data['NEGATIVE_SCORE'] = data.TEXT.apply(self.count_words, args=('negative',-1))
        logging.info('Calculating Polarity Score')
        data['POLARITY_SCORE'] = (data.POSITIVE_SCORE + data.NEGATIVE_SCORE) / ((data.POSITIVE_SCORE - data.NEGATIVE_SCORE) + 0.000001)
        logging.info('Calculating Subjectivity Score')
        data['SUBJECTIVITY_SCORE'] = (data.POSITIVE_SCORE - data.NEGATIVE_SCORE) / (data.TEXT.apply(len) + 0.000001)
    



    def readability_analysis(self, raw_data:pd.Series, data: pd.DataFrame) -> tuple:
        '''Calculate Average Sentence Lenght, Percentage of Complex Words, Fog Index, Average Number of Words, Complex Word Count.'''

        splitted = raw_data.str.split('.')
        total_words = splitted.apply(lambda sentenses : sum(len(sentense.split(' ')) for sentense in sentenses))

        logging.info('Calculating Average Sentence Length')
        data['AVG_SENTENCE_LENGTH'] = total_words / splitted.apply(len)
        complex_count = raw_data.apply(self.is_complex)
        logging.info('Calculating Percentage of Complex Words')
        data['PERCENTAGE_OF_COMPLEX_WORDS'] = complex_count / total_words
        logging.info('Calculating Fog Index')
        data['FOG_INDEX'] = 0.4 * (data.AVG_SENTENCE_LENGTH + data.PERCENTAGE_OF_COMPLEX_WORDS)
        logging.info('Calculating Average Number of Words')
        data['AVG_NUMBER_OF_WORDS'] = total_words
        logging.info('Calculating Complex word count')
        data['COMPLEX_WORD_COUNT'] = complex_count




    def is_complex(self, words)-> int:
        '''Count the number of complex words in a sentence.'''

        return sum(syllables.estimate(word) > 1 for word in words.split(' '))
    


        
    def text_statistics(self, data: pd.DataFrame) -> None:
        '''Calculate Word Count, Syllable per Word, Personal Pronoun, Average Word Length.'''

        count = lambda words : np.mean([syllables.estimate(word) for word in words]) if words else 0
        words = data.TEXT.apply(dict.keys)
        
        logging.info('Counting Words')
        data['WORD_COUNT'] = words.apply(len)
        logging.info('Calculating Syllables per word')
        data['SYLLABLE_PER_WORD'] = words.apply(count)
        logging.info('Calculating Personal Pronoun')
        data['PERSONAL_PRONOUN'] = words.apply(pos_tag).apply(lambda tags: len([tag for tag in tags if tag[1] == 'PRP']))
        logging.info('Calculating Average word length')
        data['AVG_WORD_LENGTH'] = words.apply(lambda words: sum(len(word) for word in words)) / data.WORD_COUNT


    
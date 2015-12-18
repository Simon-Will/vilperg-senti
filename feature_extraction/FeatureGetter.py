#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Abstract classes:

import re

class Feature_getter:
    pass

class Single_feature_getter(self, Feature_getter):
    def __init__():
        self.feature_name = ''
        self.feature_type = ''

    def get_value(review):
        # "Abstract" method.
        pass

class SentiWS_based_feature_getter(self, Single_feature_getter):
    def __init__(senti_dict):
        self.senti_dict = senti_dict

class Plain_feature_getter(self, Single_feature_getter):https://code.google.com/p/arff/
    pass

class Multi_feature_getter(self, Feature_getter):

    def get_feature_triples(review):
        # "Abstract" method.
        pass

# Concrete classes for actual getters:

class Token_number_getter(self, Plain_feature_getter):

    def get_value(self, tagged_text):
        """Count the tokens in review.
        Args:
            tagged_text (list): A list of lists. Each of the inner lists
                consists of three elements: token, POS-tag and lemma.
        Returns:
            count (int): The number of tokens in the review.
        """
        count = len(self.tagged_text)
        return count

class Type_number_getter(self, Plain_feature_getter):
    pass

class Overall_sentiment_getter(self, SentiWS_based_feature_getter):
    #sum of word-sentiments that are found in the review text
    def __init__(self, senti_dict):
        self.senti_dict = senti_dict
        self.feature_name = 'overall_sentiment'
        self.feature_type = 'numeric'
        
    def get_overall_sentiment(self, tagged_text):
	value = 0
	for item in self.tagged_text:
	    if item[0] in self.senit_dict:
		value += self.senit_dict[item[0]]
	return value
      

class Adjective_sentiment_getter(self, SentiWS_based_feature_getter):
    #consider all kinds of ADJ POS-Tags in tagged_text
    pos = re. compile(r'ADJ.+')
    
    def __init__(self, senti_dict):
        self.senti_dict = senti_dict
        self.feature_name = 'adjective_sentiment'
        self.feature_type = 'numeric'
        
    def get_value(self, tagged_text):
        #sum of all adjective sentiments
        value = 0
        for item in self.tagged_text:
            if pos.match(item[1]):
                if item[0] in self.senti_dict:
                    value += self.senti_dict[item[0]]
        return value
                    

class Verb_sentiment_getter(self, SentiWS_based_feature_getter):
    #consider all kinds of VERB POS-Tags in tagged_text
    pos = re.compile(r'V.+')
    
    def __init__(self, senti_dict):
        self.senti_dict = senti_dict
        self.feature_name = 'verb_sentiment'
        self. feature_type = 'numeric'
        
    def get_value(self, tagged_text):
        #sum of all verb sentiments
        value = 0
        for item in self.tagged_text:
            if pos.match(item[1]):
                if item[0] in self.senti_dict:
                    value += self.senti_dict[item[0]]
        return value
    

class Noun_sentiment_getter(self, SentiWS_based_feature_getter):
    #consider all kinds of NOUN POS-Tags in tagged_text
    pos = re.compile(r'NN')
    
    def __init_(self, senti_dict):
        self.senti_dict = senti_dict
        self.feature_name = 'noun_sentiment'
        self.feature_type = 'numeric'
        
    def get_value(self, tagged_text):
        #sum of all noun sentiments
        value = 0
        for item in self.tagged_text:
            if pos.match(item[1]):
                if item[0] in self.senti_dict:
                    value += self.senti_dict[item[0]]
        return value
        
        

class Keyword_feature_getter(self, Multi_feature_getter):
    def __init__(keywords):
        self.keywords = []

    def get_keywords(self, keywords):
        return self.keywords

    def get_feature_triples(self, review):
        """Get all (keyword, feature_type, sentiment)-triples for a review.
        """
        pass

def test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    test()

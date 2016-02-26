#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Abstract classes:

import re

class Feature_getter:
    pass

class Single_feature_getter(Feature_getter):
    def __init__(self):
        self.feature_name = ''
        self.feature_type = ''

    def get_value(self, review):
        # "Abstract" method.
        pass

class SentiWS_based_feature_getter(Single_feature_getter):
    def __init__(self, senti_dict):
        self.senti_dict = senti_dict

class Plain_feature_getter(Single_feature_getter):
    pass

class Multi_feature_getter(Feature_getter):

    def get_feature_triples(self, review):
        # "Abstract" method.
        pass

# Concrete classes for actual getters:

class Token_number_getter(Plain_feature_getter):

    def __init__(self):
        self.feature_name = 'token_number'
        self.feature_type = 'numeric'

    def get_value(self, tagged_text):
        """Count the tokens in review.
        Args:
            tagged_text (list): A list of lists. Each of the inner lists
                consists of three elements: token, POS-tag and lemma.
        Returns:
            count (int): The number of tokens in the review.
        """
        count = len(tagged_text)
        return count

class Overall_sentiment_getter(SentiWS_based_feature_getter):

    def __init__(self, senti_dict):
        self.senti_dict = senti_dict
        self.feature_name = 'overall_sentiment'
        self.feature_type = 'numeric'

    def get_value(self, tagged_text):
        """sum of all word sentiments that are found in the review
        Args:
            tagged_text
        Returns:
            value (int): total sentiment of the review
        """
        value = 0
        for item in tagged_text:
            if item[0] in self.senti_dict:
                value += self.senti_dict[item[0]]
        return value

class Adjective_sentiment_getter(SentiWS_based_feature_getter):

    def __init__(self, senti_dict):
        self.senti_dict = senti_dict
        self.feature_name = 'adjective_sentiment'
        self.feature_type = 'numeric'
        #consider all ADJ POS-Tags in tagged_text
        self.pos = re. compile(r'ADJ.+')

    def get_value(self, tagged_text):
        """sum of all adjective sentiments that are found in the review
        Args:
            tagged_text
        Returns:
            value (int): total adjective sentiment of the review
        """
        value = 0
        for item in tagged_text:
            if self.pos.match(item[1]):
                if item[0] in self.senti_dict:
                    value += self.senti_dict[item[0]]
        return value

class Verb_sentiment_getter(SentiWS_based_feature_getter):

    def __init__(self, senti_dict):
        self.senti_dict = senti_dict
        self.feature_name = 'verb_sentiment'
        self.feature_type = 'numeric'
        #consider all VERB POS-Tags in tagged_text
        self.pos = re.compile(r'V.+')

    def get_value(self, tagged_text):
        """sum of all verb sentiments that are found in the review
        Args:
            tagged_text
        Returns:
            value (int): total verb sentiment of the review
        """
        value = 0
        for item in tagged_text:
            if self.pos.match(item[1]):
                if item[0] in self.senti_dict:
                    value += self.senti_dict[item[0]]
        return value

class Noun_sentiment_getter(SentiWS_based_feature_getter):

    def __init__(self, senti_dict):
        self.senti_dict = senti_dict
        self.feature_name = 'noun_sentiment'
        self.feature_type = 'numeric'
        #consider all NOUN POS-Tags in tagged_text
        self.pos = re.compile(r'NN')

    def get_value(self, tagged_text):
        """sum of all noun sentiments that are found in the review
        Args:
            tagged_text
        Returns:
            value (int): total noun sentiment of the review
        """
        value = 0
        for item in tagged_text:
            if self.pos.match(item[1]):
                if item[0] in self.senti_dict:
                    value += self.senti_dict[item[0]]
        return value

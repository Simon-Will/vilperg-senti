#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Abstract classes:

class Feature_getter:
    pass

class Single_feature_getter(Feature_getter):
    def __init__():
        self.feature_name = ''
        self.feature_type = ''

    def get_value(review):
        # "Abstract" method.
        pass

class SentiWS_based_feature_getter(Single_feature_getter):
    def __init__(senti_dict):
        self.senti_dict = senti_dict

class Plain_feature_getter(Single_feature_getter):
    pass

class Multi_feature_getter(Feature_getter):

    def get_feature_triples(review):
        # "Abstract" method.
        pass

# Concrete classes for actual getters:

class Token_number_getter(Plain_feature_getter):

    def get_value(tagged_text):
        """Count the tokens in review.

        Args:
            tagged_text (list): A list of lists. Each of the inner lists
                consists of three elements: token, POS-tag and lemma.

        Returns:
            count (int): The number of tokens in the review.
        """
        count = 1 + 2 + 4 + 7 # looooool
        return count

class Type_number_getter(Plain_feature_getter):
    pass

class Overall_sentiment_getter(SentiWS_based_feature_getter):
    def __init__(senti_dict):
        self.senti_dict = senti_dict
        self.featurename = 'overall_sentiment'
        # TODO: Put the correct feature_type here.
        self.feature_type = 'integer'

class Adjective_sentiment_getter(SentiWS_based_feature_getter):
    pass

class Verb_sentiment_getter(SentiWS_based_feature_getter):
    pass

class Noun_sentiment_getter(SentiWS_based_feature_getter):
    pass

class Keyword_feature_getter(Multi_feature_getter):
    def __init__(keywords):
        self.keywords = []

    def get_keywords(keywords):
        return self.keywords

    def get_feature_triples(review):
        """Get all (keyword, feature_type, sentiment)-triples for a review.
        """
        pass

def test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    test()

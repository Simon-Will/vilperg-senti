#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import re
import FeatureGetter as fg
import SentiWs_handler

FEATURE_GETTER_DICT = {
        'token_number' : fg.Token_number_getter,
        'type_number' : fg.Type_number_getter,
        'overall_sentiment' : fg.Overall_sentiment_getter,
        'adjective_sentiment' : fg.Adjective_sentiment_getter,
        'verb_sentiment' : fg.Verb_sentiment_getter,
        'noun_sentiment' : fg.Noun_sentiment_getter,
        'keyword_sentiment' : Keyword_feature_getter
        }

def get_files(dir_name, f_name):
    """Recursively get regular files called f_name in the directory dir_name.

    Args:
        dir_name (str): The name of a directory.
        f_name (str): The name of the files to be found.

    Returns:
        files (list): A list of strings containing the full paths to the files.
    """
     files = [os.path.join(root, name)
             for root, dirs, files in os.walk(dir_name)
             for name in files
             if name == f_name]
     return descriptionFiles

def read_review(in_file):
    """Read a review from a file and return it as a list of lists.

    Args:
        in_file (str): The name of a file containing a tagged review text.

    Returns:
        review (list): List of lists. Each inner list consists of token,
            POS-tag and lemma.
    """
    review = []
    for line in open(in_file):
        parts = [part.strip() for part in line.split('\t')]
        review.append(parts)
    return review

def get_review_features(feature_getters, review):
    """Get the features in a review.

    Args:
        feature_getters (iterable): Several Feature_getter objects.
        review (list): Lines with token, POS-tag and lemma on each line.

    Returns:
        review_features (list???): List of the features of the review.
    """
    review_features = []
    for getter in feature_getters:
        if isinstance(getter, SentiWS_based_feature_getter):
            review_features.append(getter.get_value(review))
        elif isinstance(getter, Plain_feature_getter):
            review_features.append(getter.get_value(review))
        elif isinstance(getter, Keyword_feature_getter):
            pass
        else:
            error_message = 'Feature_getter "{0}" of unknown type ({1}).'
            sys.stderr.write(error_message.format(getter, type(getter)))
    return review_features

def make_feature_getters(features, senti_dict, getter_dict=FEATURE_GETTER_DICT):
    """Construct Feature_getter objects for the given reviews.

    Args:
        features (list): The names of the features for which Feature_getter
            objects should be constructed.
        senti_dict (dict): A dictionary mapping words to sentiments.

    Returns:
        getters (list): The constructed Feature_getter objects.
    """
    pass

def write_features(feature_getters, reviews, out_pattern):
    for r in reviews:
        # This will be a list of triples.
        review_features = get_review_features(r)
    write_arff(review_features, out_file)

def main():
    pass

if __name__ == '__main__':
    main()

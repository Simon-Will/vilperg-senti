#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re

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

def get_senti_dict(sentiws_file):
    """Read a SentiWS file and return it as a dict.

    Args:
        sentiws_file (str): The name of the file containing the SentiWS dict.

    Returns:
        senti_dict (dict): Dictionary mapping word forms to floats between -1
            and 1 representing their respective sentiment.
    """
    pass

def get_review_features(feature_getters, review):
    """Get the features in a review.

    Args:
        feature_getters (iterable): Several Feature_getter objects.
        review (list): Lines with token, POS-tag and lemma on each line.

    Returns:
        review_features (list???): List of the features of the review.
    """
        review_features = []
        for fg in feature_getters:
            if isinstance(fg, SentiWS_based_feature_getter):
                pass
            elif isinstance(fg, Plain_feature_getter):
                review_features.append(fg.get_value(review))
            elif isinstance(fg, Keyword_feature_getter):
                pass
            else:
                error_message = 'Feature_getter "{0}" of unknown type ({1}).'
                sys.stderr.write(error_message.format(fg, type(fg)))
        return review_features

def make_arff(feature_getters, reviews, out_file):
    for r in reviews:
        # This will be a list of triples.
        review_features = get_review_features(r)
    write_arff(review_features, out_file)

if __name__ == '__main__':
    main()

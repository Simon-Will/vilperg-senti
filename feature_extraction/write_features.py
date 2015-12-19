#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import re
import argparse

import feature_getter as fg
import SentiWS_handler

FEATURE_GETTER_DICT = {
        'token_number' : 'fg.Token_number_getter()',
        'type_number' : 'fg.Type_number_getter()',
        'overall_sentiment' : 'fg.Overall_sentiment_getter(senti_dict)',
        'adjective_sentiment' : 'fg.Adjective_sentiment_getter(senti_dict)',
        'verb_sentiment' : 'fg.Verb_sentiment_getter(senti_dict)',
        'noun_sentiment' : 'fg.Noun_sentiment_getter(senti_dict)',
        'keyword_sentiment' : 'fg.Keyword_feature_getter()'
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
    return files

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
        review (str): Full path to a review file.

    Returns:
        review_features (list): Features of the review. The list contains
            triples comprising feature_name, feature_value and feature_type.
    """
    review_features = []
    review_content = read_review(review)
    for getter in feature_getters:
        if isinstance(getter, fg.Single_feature_getter):
            feature_name = getter.feature_name
            feature_value = getter.get_value(review_content)
            feature_type = getter.feature_type
            review_features.append((feature_name, feature_value, feature_type))
        elif isinstance(getter, fg.Keyword_feature_getter):
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
        getter_dict (dict): A dictionary mapping feature names to strings
            that -- evaluated with eval() -- return the appropriate getters.

    Returns:
        getters (list): The constructed Feature_getter objects.
    """
    getters = []
    for f in features:
        getters.append(eval(getter_dict[f]))
    return getters

def write_review_features(review_features, out_file, if_exists='append'):
    """Write review_features in out_file.

    Args:
        review_features (list): Features of the review. The list contains
            triples comprising feature_name, feature_value and feature_type.
        out_file (str): Full path to the file the features should be written to.
        if_exists (str): String describing what to do if the out_file already
            exists. Must be one of 'append', 'overwrite' and 'update'.
    """
    line_pat = '{0[0]}\t{0[1]}\t{0[2]}\n'
    if os.path.isfile(out_file):
        if if_exists == 'append':
            with open(out_file, 'a') as f:
                for rf in review_features:
                    line = line_pat.format(rf)
                    f.write(line)
        elif if_exists == 'overwrite':
            with open(out_file, 'w') as f:
                for rf in review_features:
                    line = line_pat.format(rf)
                    f.write(line)
        elif if_exists == 'update':
            old_lines = open(out_file, 'r').readlines()
            new_lines = [line_pat.format(rf) for rf in review_features]
            all_lines = []
            for ol in old_lines:
                in_new_lines = False
                old_pat = re.compile(r'^{}\t.*$'.format(ol.split('\t')[0]))
                for nl in new_lines:
                    if old_pat.match(nl):
                        in_new_lines = True
                if not in_new_lines:
                    all_lines.append(ol)
            all_lines.extend(new_lines)
            open(out_file, 'w').writelines(all_lines)
        else:
            error_pattern = '''Error: if_exists must be one of \'append\',
                    \'overwrite\' and \'update\', but is {0}.'''
            sys.stderr.write(error_pattern.format(if_exists))
            sys.exit(3)
    else:
        with open(out_file, 'w') as f:
            for rf in review_features:
                line = line_pat.format(rf)
                f.write(line)

def write_all_review_features(
        feature_getters, reviews, out_base_name, if_exists='append'):
    """Use feature_getters to get reviews and write them to files.

    Args:
        feature_getters (list): Feature_getter objects used to get features.
        reviews (list): List of strings containing the full path to text files
            containing the reviews.
        out_base_name (str): Base name of the file the features should be
            written to.
        if_exists (str): String describing what to do if the out_file already
            exists. Must be one of 'append', 'overwrite' and 'update'.
    """
    out_file_pattern = '{0}/{1}'
    for r in reviews:
        # This will be a list of triples.
        review_features = get_review_features(feature_getters, r)
        out_file = out_file_pattern.format(os.path.dirname(r), out_base_name)
        write_review_features(review_features, out_file, if_exists)

def main():
    d = 'Compute review features and write them to files.'
    parser = argparse.ArgumentParser(description=d)

    parser.add_argument('--feature', '-f', action='append',
            required=True, help='A feature that is to be extracted.')

    parser.add_argument('--in_file_name', '-i', default='content_tagged',
            help='''The name of the file the review text is stored in in each
            directory''')

    parser.add_argument('--out_file_name', '-o', default='features',
            help='''The output file the features are written to in each
            directory.''')

    parser.add_argument('--if_exists',
            choices=['overwrite', 'update', 'append'], default='append',
            help='Decide what to do if the file out_file_name already exists.')

    parser.add_argument('--sentiws_file', '-s', help='''The SentiWS file that
            is used for the sentiment features.''')

    parser.add_argument('top_dir',
            help='''The directory that is searched recursively for files called
            in_file_name''')

    args = parser.parse_args()
    #print(args)

    top_dir = args.top_dir
    out_file = args.out_file_name
    in_file = args.in_file_name
    features = args.feature
    if_exists = args.if_exists
    sentiws_file = args.sentiws_file

    if in_file == out_file:
        sys.stderr.write(
                'Error: in_file_name cannot be the same as out_file_name.\n')
        sys.exit(1)

    for f in features:
        if f not in FEATURE_GETTER_DICT:
            error_pattern = 'Error: feature {0} is not a valid feature.\n'
            sys.stderr.write(error_pattern.format(f))
            sys.exit(2)

    senti_dict = SentiWS_handler.get_senti_dict(sentiws_file)
    reviews = get_files(top_dir, in_file)
    feature_getters = make_feature_getters(features, senti_dict)
    write_all_review_features(feature_getters, reviews, out_file, if_exists)

if __name__ == '__main__':
    main()

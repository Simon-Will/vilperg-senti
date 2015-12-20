#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

def get_senti_dict(sentiws_file):
    """Read a SentiWS file and return it as a dict.

    Args:
        sentiws_file (str): The name of the file containing the SentiWS dict.

    Returns:
        senti_dict (dict): Dictionary mapping word forms to floats between -1
            and 1 representing their respective sentiment.
    """
    line_pat = re.compile(r'^([^|]+)\|(\S+)\t(\S+)(?:\t(\S*))?\n$')
    senti_dict = {}
    for line in open(sentiws_file):
        mat = line_pat.match(line)
        if not mat:
            raise Not_SentiWS_file('Line unreadable: {0}'.format(line))
        groups = mat.groups()
        lemma = groups[0]
        pos = groups[1]
        sentiment = float(groups[2])
        senti_dict[lemma] = sentiment
        if groups[3]:
            forms = groups[3].split(',')
            for f in forms:
                senti_dict[f] = sentiment
    return senti_dict

class Not_SentiWS_file(Exception):
    pass

def test():
    test_file = 'test_sentiws'
    print(get_senti_dict(test_file))

if __name__ == '__main__':
    test()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import re

from nltk import tokenize

LOGFILE = './tokenizing.log'

def files_in_dir(d, fname):
    """Find all files with basename fname in dir d and return full paths.

    Args:
        d (str): The name of a directory.
        fname (str): The basename of the files that are to be found.
    """
    return [os.path.join(d, f) for f in os.listdir(d) if f == fname]

def tokenize_file(f):
    """Tokenize a file by tokens and sentences and write it fo f_tokenized.
    
    Args:
        f (str): The name of the file that is to be tokenized.
    """
    content = re.sub(r'\n', '', open(f).read())
    tokens = tokenize.word_tokenize(content, 'german')
    sentence_ending = ['.', '!', '?']
    with open('{0}_tokenized'.format(f)) as ft:
        line = ( '{0}\n\n'.format(token) if token in sentence_ending
                else '{0}\n'.format(token) )
        ft.write(line)

def main():
    indir = sys.argv[1]
    filename = 'content'
    if len(sys.argv) == 3:
        filename = sys.argv[2]
    files = files_in_dir(indir, filename)

if __name__ == '__main__':
    main()

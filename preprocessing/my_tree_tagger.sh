#!/bin/sh

INFILE=$1
OUTFILE=$2

BIN="$HOME/bin"
CMD="$HOME/semipublic/mlt/tagger-scripts/cmd"
LIB="$HOME/semipublic/mlt/tagger-scripts/lib"

OPTIONS="-token -lemma -sgml -pt-with-lemma"

TOKENIZER=${CMD}/utf8-tokenize.perl
TAGGER=${BIN}/tree-tagger
ABBR_LIST=${LIB}/german-abbreviations-utf8
PARFILE=${LIB}/german-utf8.par
LEXFILE=${LIB}/german-lexicon-utf8.txt
FILTER=${CMD}/filter-german-tags
LOOKUP=${CMD}/lookup.perl

$TOKENIZER -a $ABBR_LIST $INFILE |
# external lexicon lookup
#perl $CMD/lookup.perl $LEXFILE |
$LOOKUP $LEXFILE |
# tagging
$TAGGER $OPTIONS $PARFILE | 
# error correction
$FILTER > $OUTFILE

#!/bin/bash

USAGE="Usage: $0 DIRECTORY FILENAME"

if [ -z $1 ]
then
	echo "$USAGE"
	exit 1
fi

DIR=$1
FILENAME=$2

MY_TREE_TAGGER="$HOME/semipublic/mlt/vilperg-senti/preprocessing/my_tree_tagger.sh"

function tokenize {
	FILE=$1
	echo "here"
	echo "$FILE"
	$TOKENIZER -a $ABBR_LIST $FILE |
	# external lexicon lookup
	perl $CMD/lookup.perl $LEXFILE |
	# tagging
	$TAGGER $OPTIONS $PARFILE  | 
	# error correction
	$FILTER > "${1}_tagged"
}

find "$DIR" -name "$FILENAME" -exec $MY_TREE_TAGGER {} {}_tagged \;

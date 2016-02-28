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

find "$DIR" -name "$FILENAME" -exec $MY_TREE_TAGGER {} {}_tagged \;

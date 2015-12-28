#!/bin/bash

USAGE="Usage: $0 MODE SENTIWS_FILE TOP_DIR [additional TOP_DIRs]
Apply write_features.py to the TOP_DIRs.
MODE has to be 'append', 'overwrite' or 'update'."

if [[ $1 =~  (-h|-help) ]]
then
	echo "$USAGE" && exit 0
elif [ $# -lt 3 ]
then 
	echo >&2 "$USAGE" && exit 1
elif [[ ! $1 =~ (append|update|overwrite) ]]
then
	echo >&2 "Unknown mode: $1"
	echo >&2 "$USAGE" && exit 1
elif [ -d "$2" ] || [ ! -r "$2" ]
then
	echo >&2 "File unreadable or a directory: $2"
	echo >&2 "$USAGE" && exit 1
fi

MODE=$1
SENTIWS_FILE=$2
shift 2
LOG_FILE="features_$(date +%F)"

WRITE_FEATURES="/home/students/will/semipublic/mlt/vilperg-senti/\
feature_extraction/write_features.py"

for TOP_DIR in "$@"
do
	CMD="$WRITE_FEATURES\
		--if_exists $MODE\
		--follow_links\
		--sentiws_file $SENTIWS_FILE\
		--log_file $LOG_FILE\
		--in_file_name content_tagged\
		--out_file_name features\
		--feature token_number\
		--feature verb_sentiment\
		--feature overall_sentiment\
		--feature noun_sentiment\
		--feature adjective_sentiment\
		$TOP_DIR"
	#echo $CMD
	python3.4 $CMD &
done
wait

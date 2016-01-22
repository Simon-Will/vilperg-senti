#!/bin/sh

USAGE="Usage: $0 FILE
Add normalized sentiment features to a file by reading the current sentiment
features and dividing them by the token_number."

FILE=$1

# Handle the user input.
if [ "$1" = '-h' ]
then
    echo "$USAGE" >&2 && exit 0
elif [ -z "$FILE" ]
then
    echo "$USAGE" >&2 && exit 1
elif [ ! -r "$FILE" ]
then
    echo "File '$FILE' not readable." >&2 && exit 2
elif [ ! -w "$FILE" ]
then 
    echo "File '$FILE' not writable" >&2 && exit 3
fi

# Get the token_number and exit if it doesn't look right.
TOKEN_NUMBER=`grep -P '^token_number' "$FILE" | cut -f2`
if ! echo "$TOKEN_NUMBER" | grep -P '^[1-9][0-9]*$' > /dev/null
then
    echo "Invalid token number: '$TOKEN_NUMBER' in file '$FILE'" >&2 && exit 4
fi

# This awk program will calculate the normalized sentiments and include
# a line for them.
AWK_PROG='
BEGIN {
    FS="\t"
    OFS="\t"
}
{
    if ($0 ~ /^normalized_/) {
        print $0
    }
    else if ($0 ~ /^[^\s]+_sentiment\t/) {
        NORMALIZED=$2/TOKEN_NUMBER
        print $0 ORS "normalized_" $1, NORMALIZED, $3
    }
    else {
        print $0
    }
}
'

# Invent unique name for temporary file.
TMP="$HOME/tmp/`readlink -f "$FILE" | sed 's;/;;g'`"

# Execute the program, delete duplicate lines
# and replace the old file with the new one.
awk -v TOKEN_NUMBER="$TOKEN_NUMBER" "$AWK_PROG" "$FILE" | sort | uniq > $TMP
mv "$TMP" "$FILE"

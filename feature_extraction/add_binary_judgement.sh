#!/bin/sh

USAGE="Usage: $0 FILE
Add the binary_judgement feature to a file by interpreting the stars feature.
Reviews with 4 or 5 stars are 'good', the ones with 1, 2 or 3 stars are 'bad'."

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

# This awk program will determine the binary_judgement of the review and
# include a line for it.
AWK_PROG='
BEGIN {
    FS="\t"
    OFS="\t"
}
/^stars/ {

    if ($2 ~ /[1-5]/) {
        if ($2 >= 4) {
            BINARY_JUDGEMENT="good"
        }
        else {
            BINARY_JUDGEMENT="bad"
        }
        print $0 ORS "binary_judgement", BINARY_JUDGEMENT, "{good, bad}"
    }
    else
        print $0
}
! /^stars/ {
    print $0
}
'

# Invent unique name for temporary file.
TMP="$HOME/tmp/`readlink -f "$FILE" | sed 's;/;;g'`"

# Execute the program, delete duplicate lines
# and replace the old file with the new one.
awk "$AWK_PROG" "$FILE" | sort | uniq > "$TMP"
mv "$TMP" "$FILE"

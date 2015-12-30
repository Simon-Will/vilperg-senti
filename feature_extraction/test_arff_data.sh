#!/bin/sh
test -d test_features || (echo 'No directory named test_features' >&2 && exit 1)
OUT="test_`date +%Y-%m-%d-%H-%M-%S`.arff"
./arff_data.py test_features/ $OUT adjective_sentiment token_number stars

#!/bin/bash

INFO=$1
FEATURES=$2
sed -n '3 s/^\([1-5]\)\.0$/stars\t\1\t{1, 2, 3, 4, 5}/p' "$INFO" >> "$FEATURES"

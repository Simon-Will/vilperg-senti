#!/bin/bash

CATEGORIES=( smartphones armbanduhren küche_haushalt baumaschinen )

MLT="/home/students/will/semipublic/mlt/"
MAKE_CHUNKS="$MLT/vilperg-senti/review_chunking/make_chunks.pl"

for c in ${CATEGORIES[@]}
do
	CMD="$MAKE_CHUNKS\
		-d reviews\
		-c 50\
		--balance\
		-w $MLT/peculiar_files/peculiar_${c}_3\
		$MLT/all_${c}_12_11_2015\
		$MLT/chunks/cleansed_balanced_chunks_${c}"
	
	#echo $CMD
	$CMD &
done
wait

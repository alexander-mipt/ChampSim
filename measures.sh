#!/bin/bash

source environment.sh

mkdir -p $stat_dir

# single thread
# for arg in ${experiments[*]}; do
#     ./measure.sh $arg
# done

# multi-thread
./measure.sh $etalon &
./measure.sh $markov_max &
./measure.sh $markov_prop &
./measure.sh $mru &
./measure.sh $drrip &
# ./measure.sh $fifo &


exit 0


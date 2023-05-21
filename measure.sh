#!/bin/bash

source environment.sh

# warmup=200
# simulation=500
warmup=10000000
simulation=50000000

experiment=$1

mkdir -p $stat_dir/$experiment
for trace in `ls $traces_dir`; do
    # set -x
    $bin_dir/$experiment/champsim --warmup_instructions $warmup --simulation_instructions $simulation $traces_dir/$trace &> $stat_dir/$experiment/$trace.log
    # set +x
done

exit 0


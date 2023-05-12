#!/bin/bash

warmup=200
simulation=500

traces_dir=traces/for_measure
stat_dir=stat
bin_dir=bin

etalon="etalon"
markov_max="markov_predictor_max"
markov_prop="markov_predictor_prop"
fifo="fifo_cache"

experiments=($etalon $markov_max $markov_prop $fifo)

mkdir -p $stat_dir
for experiment in ${experiments[*]}; do
    mkdir -p $stat_dir/$experiment
    for trace in `ls $traces_dir`; do
        set -x
        time $bin_dir/$experiment/champsim --warmup_instructions $warmup --simulation_instructions $simulation $trace_dir/$trace &> $stat_dir/$experiment/$trace.log
        set +x
    done
done

exit 0


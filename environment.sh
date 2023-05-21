#!/bin/bash

traces_dir=traces/for_measure
stat_dir=stat
bin_dir=bin

etalon="etalon"
markov_max="markov_predictor_max"
markov_prop="markov_predictor_prop"
fifo="fifo_cache"
mru="mru_cache"

experiments=($etalon $markov_max $markov_prop $fifo $mru)

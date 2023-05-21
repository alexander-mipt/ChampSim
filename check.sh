#!/bin/bash

source environment.sh

for experiment in ${experiments[*]}; do
    ls -1 $stat_dir/$experiment/ | wc -l
    for trace in `ls $traces_dir`; do
        wc -l $stat_dir/$experiment/$trace.log
    done
done
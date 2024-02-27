#!/bin/bash

export BENCHRUN_TEST_CASE=testcases/acb_query.js
export BENCHRUN_COUNT=1
export BENCHRUN_THREADS="1 8" #"1 2 4 8"
export BENCHRUN_TRIAL_TIME=15 #30
export BENCHRUN_TRIAL_COUNT=1
 
rm -rf /tmp/out 2> /dev/null
mkdir /tmp/out

for i in $(seq 1 $BENCHRUN_COUNT); do
  # TODO: alternate whatever parameter we're testing for here?
  numactl --physcpubind=0,1,2,3 -i 0  python benchrun.py  --shell ~/mongo/build/install/bin/mongo --readCmd true -f $BENCHRUN_TEST_CASE -t $BENCHRUN_THREADS --trialTime $BENCHRUN_TRIAL_TIME --trialCount $BENCHRUN_TRIAL_COUNT --out "/tmp/out/perf_$i.json";
  python benchrun_format.py -i "/tmp/out/perf_$i.json" -f tsv > "/tmp/out/perf_$i.tsv";
done
tsv-append -H /tmp/out/perf_*.tsv | tsv-summarize -H --group-by name,thread_count --median ops_per_sec:ops_per_sec --count-header count --stdev ops_per_sec:ops_per_sec_stdev

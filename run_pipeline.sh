#! /usr/bin/env bash

logdir=${PWD}

pipeline_logs=$logdir/`date "+%Y-%m-%dT%H:%M:%S"`_pipeline_$$.log

#run () { decho $* | tee -a $pipeline_logs ;  (time $* ) &>> $pipeline_logs; decho $* ended; }
run () { decho $* | tee -a $pipeline_logs ;  (python $logdir/launch_trace.py $* ) &>> $pipeline_logs; decho $* ended; }

decho () { echo `date` $*; }

source /usr/lofarinit.sh

#sar -A 5 > ${pipeline_logs}.sar &

#decho SAR started

#sleep 10

#WORK_DIR=/datadrive/azureuser/test_pipeline
WORK_DIR=/mnt/test/yan/bench

decho Starting pipeline | tee -a $pipeline_logs
cd $WORK_DIR
cp skymodel.orig.dat new_skymodel.dat


#for ii in `seq 3`
#do
./next_iter.sh # probably we should rename this to init. Iterating doesn't really make sense if your second sky model only contains few sources...
makesourcedb in=skymodel.dat out=3C196.sourcedb format='<'
run ./do_ndppp.sh
run ./do_applycal.sh
run ./do_image.sh
run ./do_clean.sh
run ./do_bdsm.sh
#done
run ./do_clean_mask.sh
run ./do_clean_multiscale.sh

sleep 10

#pkill -f sar

decho pipeline ended | tee -a $pipeline_logs

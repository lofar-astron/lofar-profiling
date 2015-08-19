#!/bin/bash

# Parameters
LOFARROOT=/local/veenboer/opt/lofar

# Set directories
SCRIPT_DIR=${PWD}/scripts
DATA_DIR=${PWD}/data
RUN_DIR=${PWD}/run
LOG_DIR=${PWD}/log

# Create directories
mkdir -p ${RUN_DIR}
mkdir -p ${LOG_DIR}

# Name of the log
PIPELINE_LOG=${LOG_DIR}/`date "+%Y-%m-%dT%H:%M:%S"`_pipeline_$$.log

# Function to run and profile a pipeline component
run () {
    decho $* | tee -a ${PIPELINE_LOG} ;(python ${SCRIPT_DIR}/launch_trace.py $* ) &>> ${PIPELINE_LOG}; decho $* ended;
}

# Function to echo with the date prepended
decho () {
    echo `date` $*;
}

# Initialize lofar software
source ${LOFARROOT}/lofarinit.sh

# Set input and output file names
DATA_SKYMODEL=${DATA_DIR}/skymodel.dat
DATA_SOURCEDB=${RUN_DIR}/sources.db

# Start pipeline
decho Starting pipeline | tee -a $pipeline_logs
cd $RUN_DIR

${SCRIPT_DIR}/do_init.sh
run ${SCRIPT_DIR}/do_makesourcedb.sh
#run ./do_ndppp.sh
#run ./do_applycal.sh
#run ./do_image.sh
#run ./do_clean.sh
#run ./do_bdsm.sh
#run ./do_clean_mask.sh
#run ./do_clean_multiscale.sh

decho pipeline ended | tee -a $pipeline_logs

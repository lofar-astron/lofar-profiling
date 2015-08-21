#!/bin/bash

# Parameters
LOFARROOT=/local/veenboer/opt/lofar

# Set directories
export SCRIPT_DIR=${PWD}/scripts
export DATA_DIR=${PWD}/data
export RUN_DIR=${PWD}/run
export LOG_DIR=${PWD}/log
export PARSET_DIR=${PWD}/parsets

# Create directories
mkdir -p ${RUN_DIR}
mkdir -p ${LOG_DIR}

# Name of the log
PIPELINE_LOG=${LOG_DIR}/`date "+%Y-%m-%d_%H:%M:%S"`_pipeline_$$.log

# Function to echo with the date prepended
decho () {
    echo `date` $*;
}

# Function to run a pipeline component
run () {
    decho $* | tee -a ${PIPELINE_LOG};
    $*
    decho $* ended | tee -a ${PIPELINE_LOG};
}

# Function to run and trace a pipeline component
trace () {
    decho $* | tee -a ${PIPELINE_LOG};
    python ${SCRIPT_DIR}/launch_trace.py ${SCRIPT_DIR} $*
    decho $* ended | tee -a ${PIPELINE_LOG};
}

# Initialize lofar software
source ${LOFARROOT}/lofarinit.sh

# Set input and output file names
export DATA_SKYMODEL_INPUT=${DATA_DIR}/skymodel.dat
export DATA_MS_INPUT=${DATA_DIR}/input.MS
export DATA_SOURCEDB=${RUN_DIR}/sources.db
export DATA_MS_NDPPP=${RUN_DIR}/ndppp.MS
export PARSET_NDPPP=${PARSET_DIR}/ndppp.parset

# Start pipeline
decho Starting pipeline | tee -a $pipeline_logs
cd $RUN_DIR

#${SCRIPT_DIR}/do_init.sh
run ${SCRIPT_DIR}/do_makesourcedb.sh
trace ${SCRIPT_DIR}/do_ndppp.sh
#run ./do_applycal.sh
#run ./do_image.sh
#run ./do_clean.sh
#run ./do_bdsm.sh
#run ./do_clean_mask.sh
#run ./do_clean_multiscale.sh

decho pipeline ended | tee -a $pipeline_logs

#!/bin/bash

# Check command line arguments
if [[ $# -ne 1 ]]
then
    echo "Usage: $0 lofarroot"
    exit
fi
LOFARROOT=$1

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
    decho $* started | tee -a ${PIPELINE_LOG};
    $*
    decho $* ended | tee -a ${PIPELINE_LOG};
}

# Function to run and trace a pipeline component
trace () {
    decho $* started | tee -a ${PIPELINE_LOG};
    python ${SCRIPT_DIR}/launch_trace.py ${SCRIPT_DIR} ${LOG_DIR} $*
    decho $* ended | tee -a ${PIPELINE_LOG};
}

# Initialize lofar software
source ${LOFARROOT}/lofarinit.sh

# Input file names
export DATA_INPUT_SKYMODEL=${DATA_DIR}/skymodel.dat
export DATA_INPUT_MS=${DATA_DIR}/input.ms

# Names of parsets
export PARSET_NDPPP_AVFIL=${PARSET_DIR}/ndppp_avfil.parset
export PARSET_NDPPP_CAL=${PARSET_DIR}/ndppp_cal.parset
export PARSET_IMAGER_DIRTY=${PARSET_DIR}/awimager_dirty.parset
export PARSET_IMAGER_CLEAN=${PARSET_DIR}/awimager_clean.parset

# Start pipeline
decho Starting pipeline | tee -a $pipeline_logs
cd $RUN_DIR
${SCRIPT_DIR}/do_init.sh
run ${SCRIPT_DIR}/do_makesourcedb.sh
trace ${SCRIPT_DIR}/do_ndppp_avfil.sh
trace ${SCRIPT_DIR}/do_ndppp_cal.sh
trace ${SCRIPT_DIR}/do_imager_dirty.sh
trace ${SCRIPT_DIR}/do_imager_clean.sh

decho pipeline ended | tee -a $pipeline_logs

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
    decho $* | tee -a ${PIPELINE_LOG};
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
export DATA_SKYMODEL_INPUT=${DATA_DIR}/skymodel.dat
export DATA_MS_INPUT=${DATA_DIR}/input.MS

# Names of data products
export DATA_SOURCEDB=${RUN_DIR}/sources.db
export DATA_PARMDB=${RUN_DIR}/instrument
export DATA_MS_NDPPP=${RUN_DIR}/AVFIL.MS
export DATA_MS_NDPPP_APPLYCAL=${RUN_DIR}/CAL.MS
export DATA_IMAGE_DIRTY=${RUN_DIR}/dirty.img

# Names of parsets
export PARSET_NDPPP=${PARSET_DIR}/ndppp.parset
export PARSET_NDPPP_APPLYCAL=${PARSET_DIR}/ndppp_applycal.parset
export PARSET_IMAGER_DIRTY=${PARSET_DIR}/awimager_dirty.parset

# Start pipeline
decho Starting pipeline | tee -a $pipeline_logs
cd $RUN_DIR

${SCRIPT_DIR}/do_init.sh
run ${SCRIPT_DIR}/do_makesourcedb.sh
run ${SCRIPT_DIR}/do_ndppp.sh
run ${SCRIPT_DIR}/do_applycal.sh
run ${SCRIPT_DIR}/do_image.sh
#run ./do_clean.sh
#run ./do_bdsm.sh
#run ./do_clean_mask.sh
#run ./do_clean_multiscale.sh

decho pipeline ended | tee -a $pipeline_logs

#!/bin/bash
source ${LOFARROOT}/lofarinit.sh
time NDPPP ${PARSET_NDPPP} msin=${DATA_MS_INPUT} msout=${DATA_MS_NDPPP} gaincal.sourcedb=${DATA_SOURCEDB}

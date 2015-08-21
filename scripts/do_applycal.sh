#!/bin/bash
source ${LOFARROOT}/lofarinit.sh
time NDPPP ${PARSET_NDPPP_APPLYCAL} msin=${DATA_MS_NDPPP} msout=${DATA_MS_NDPPP_APPLYCAL} applycal.parmdb=${DATA_PARMDB}

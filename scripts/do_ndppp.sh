#! /usr/bin/env bash

source /usr/lofarinit.sh

input_file=L86280_SAP001_SB235_uv.MS

time NDPPP ndppp.parset msin=$input_file msout=3C196_AVFIL.MS #gaincal.debuglevel=10



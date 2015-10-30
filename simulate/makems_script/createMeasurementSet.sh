#! /usr/bin/env python


import sys, os, shutil
import subprocess as sp


# Read command line arguments
if len(sys.argv) < 3:
    print "Usage: %s parset_filename output_ms_name" % sys.argv[0]
    exit(0)
else:
    parset_filename = sys.argv[1]
    output_ms_name = sys.argv[2]
lofar_dir = os.environ["LOFARROOT"]
antenna_set = "HBA_DUAL" # arguments? or in parset?
print ("IMPROVE: the antenna set should be set in the use case description. " 
      "For now fixed:"), antenna_set

print "{0:20}{1:40}".format("Input parset:", parset_filename)
print "{0:20}{1:40}".format("Output MS:", output_ms_name)
print "{0:20}{1:40}".format("Using LOFARROOT:", lofar_dir)
print "{0:20}{1:40}".format("Antenna set:", antenna_set)
    
# Create a temporary parset file
tmp_parset_filename = "makems_parset.tmp"
with open(parset_filename) as parset:
    with open(tmp_parset_filename, "w") as tmp_parset:
        for line in parset:
           if "MSName" in line:
               tmp_parset.write("MSName=%s\n" % output_ms_name)
           else:
               tmp_parset.write(line)


# Create empty MS
print ">>> Create empty MS."
cmd = ["makems",tmp_parset_filename]
try: 
    sp.check_output(cmd, stderr=sp.STDOUT)
except sp.CalledProcessError:
    # if cmd returns non-zero exit status
    print "ERROR: ", cmd
    exit(2);
print ">>> Done."

# Add LOFAR station layout for beam model
cmd = ["makebeamtables", "ms=%s" %  output_ms_name, 
       "antennaset=%s" % antenna_set, 
       "antennasetfile=%s/etc/AntennaSets.conf" % lofar_dir,
       "antennafielddir=%s/etc/StaticMetaData" % lofar_dir,
       "ihbadeltadir=%s/src/MAC/Deployment/data/StaticMetaData/iHBADeltas/" % lofar_dir, 
       "overwrite=true"]
try:
    sp.check_output(cmd, stderr=sp.STDOUT)
except sp.CalledProcessError:
    # if cmd returns non-zero exit status
    print "ERROR: ", cmd
    exit(2);

os.remove(tmp_parset_filename);


# Get a sky model (probably need CEP to do this)
print ">>> Get global sky model."
# Coordinates come from pointing, msoverview in=test.MS
sky_model_filename = "my.skymodel" 
# gsm.py my.skymodel 16:38:28.205274 +62.34.44.31361 5
print "WARNING: Sky model from GSM not implemented yet. Use test sky model for now."
print ">>> Done."


# Convert skymodel to sourcedb
sourcedb_model_filename = "%s.sourcedb" % output_ms_name
cmd = ["makesourcedb", "in=%s" % sky_model_filename, 
       "out=%s" % sourcedb_model_filename, "format=<"]
try:
    # the sourcedb needs to be removed, otherwise appended
    shutil.rmtree(sourcedb_model_filename)
except:
    pass

try:
    sp.check_output(cmd, stderr=sp.STDOUT)
except sp.CalledProcessError:
    # if cmd returns non-zero exit status
    print "ERROR: ", cmd
    exit(2);


# Predict skymodel as visibilities
print ">>> Predict skymodel as visibilities."
cmd = ["DPPP", "msin=%s" % output_ms_name, "msout=.", 
       "steps=[predict]", 
       "predict.sourcedb=%s" % sourcedb_model_filename, 
       "predict.usebeammodel=true"]
try:
    sp.check_output(cmd, stderr=sp.STDOUT)
except sp.CalledProcessError:
    # if cmd returns non-zero exit status
    print "ERROR: ", cmd
    exit(2);
print ">>> Done."


# Apply corruptions to the data
print ">>> Apply corruptions to the data."
print "WARNING: Corruptions not implemented yet."
# Create a parmdb for corruptions
# parmdbm
#  open table='my.parmdb'
#  adddef Gain:0:0:Real values=1
#  adddef Gain:1:1:Real values=1
#  adddef Gain:1:1:Real:CS002HBA0 values=3
#  Ctrl-D

# Apply corruptions to visibilities
# (Could have done two DPPP steps in one go with steps=[predict,correct])
# DPPP msin=test.MS msout=. steps=[correct] correct.parmdb=my.parmdb correct.invert=false

# Inspect corruptions
# parmdbplot.py my.parmdb

# Inspiration for more complicated corruptions:
# See ~/opt/lofar/trunk/src/CEP/DP3/DPPP/test/tApplyCal_parmdbscript for inspiration on parmdbs
# Or have a look at source of parmdbplot.py for python binding to parmdb
print ">>> Done."


print "Finished."

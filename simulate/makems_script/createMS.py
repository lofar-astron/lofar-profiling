#! /usr/bin/env python


import sys, os, shutil
import argparse
import subprocess as sp


def createMeasurementSet(skymodel, 
                         ms_parset, 
                         ms_name, 
                         antenna_set, 
                         lofar_dir):
    """Creates a simulated measurement set from a skymodel"""

    # Create a temporary parset file
    tmp_parset_filename = "makems_parset.tmp"
    with open(ms_parset) as parset:
        with open(tmp_parset_filename, "w") as tmp_parset:
            for line in parset:
                if "MSName" in line:
                    tmp_parset.write("MSName=%s\n" % ms_name)
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
    print "DONE!"

    # Add LOFAR station layout for beam model
    cmd = ["makebeamtables", "ms=%s" %  ms_name, 
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

    # Convert skymodel to sourcedb
    sourcedb_model_filename = "%s.sourcedb" % ms_name
    cmd = ["makesourcedb", "in=%s" % skymodel, 
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
    cmd = ["DPPP", "msin=%s" % ms_name, "msout=.", 
           "steps=[predict]", 
           "predict.sourcedb=%s" % sourcedb_model_filename, 
           "predict.usebeammodel=true"]
    try:
        sp.check_output(cmd, stderr=sp.STDOUT)
    except sp.CalledProcessError:
        # if cmd returns non-zero exit status
        print "ERROR: ", cmd
        exit(2);
    print "DONE!"


    # Apply corruptions to the data
    print "WARNING: Corruptions not implemented yet."
    print ">>> Apply corruptions to the data."
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
    print "DONE!"



    


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Creates a simulated measurement set from a skymodel. " +\
        "Note: In most cases, use 'simulateMS.py' instead, as it also " +\
        "allows to specify source locations in pixels in the skymodel. " +\
        "This script only simulates the MS from a usual skymodel.")
    parser.add_argument('-sm', '--skymodel', 
                        help='Skymodel',
                        required=True)
    parser.add_argument('-msp','--ms_parset', 
                        help='Measurement set parset',
                        required=True)
    parser.add_argument('-set', '--antenna_set', 
                        help='LOFAR antenna sets',
                        choices=['LBA_INNER','LBA_OUTER','HBA_ZERO','HBA_ONE',
                        'HBA_JOINED','HBA_DUAL'],
                        required=False, default="HBA_DUAL")
    parser.add_argument('-ms','--ms_name', 
                        help='Name of the Measurement set created', 
                        required=True)
    args = parser.parse_args()

    # TODO: find out which values 'antenna_set' can take

    lofar_dir = os.environ["LOFARROOT"]

    print "{0:20}{1:40}".format("Sky model:", args.skymodel)
    print "{0:20}{1:40}".format("Input parset:", args.ms_parset)
    print "{0:20}{1:40}".format("Output MS:", args.ms_name)
    print "{0:20}{1:40}".format("Antenna set:", args.antenna_set)
    print "{0:20}{1:40}".format("Using LOFARROOT:", lofar_dir)

    createMeasurementSet(args.skymodel, args.ms_parset, 
                         args.ms_name, args.antenna_set, lofar_dir);
    

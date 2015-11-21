#! /usr/bin/env python

import sys, os, shutil
import argparse
import createMS
import subprocess as sp
import convertSkymodel as csm


def predicate_in_pixels(skymodel):
    """Checks whether or not source locations are specified in pixels"""
    with open(skymodel,'r') as fh:
        for line in fh:
            if len(line.strip()) == 0 or line.strip()[0] == "#":
                pass
            elif line.strip()[:6] == 'FORMAT':
                line_split = [a.strip() for a in line.split(",")]
                try:
                    Ra_position = line_split.index("RaAsPixel")
                    Dec_position = line_split.index("DecAsPixel")
                except ValueError:
                    return False
                return True



def createTmpImagerParset(in_parset, out_parset, image_name, ms_name):
    # TODO: make more robust; or better create generic tools to update parsets
    with open(in_parset) as in_fh:
        with open(out_parset, "w") as out_fh:
            for line in in_fh:
                if "operation" in line:
                    out_fh.write("operation=empty\n")
                elif "image" in line:
                    out_fh.write("image={0:s}\n".format(image_name))
                elif "ms=" in line:
                    out_fh.write("ms={0:s}\n".format(ms_name))
                else:
                    out_fh.write(line)



def createTmpMSParset(in_parset, out_parset, ms_name):
    with open(in_parset) as in_fh:
        with open(out_parset, "w") as out_fh:
            for line in in_fh:
                if "MSName" in line:
                    out_fh.write("MSName=%s\n" % ms_name)
                else:
                    out_fh.write(line)



def createMSradec(skymodel, ms_parset, antenna_set, ms_name, lofar_dir):
    createMS.createMeasurementSet(skymodel, ms_parset, 
                                  ms_name, antenna_set, 
                                  lofar_dir)


def createMSpixel(skymodel, ms_parset, antenna_set, imager_parset, 
                  ms_name, lofar_dir):
    """Input: skymodel using pixel locations
       Input: ..."""    

    # create temporary image to extract metadata: 
    # (1) create an empty MS set
    # (2) run awimager with 'operation=empty' for metadata
    # (3) create skymodel using the metadata
    tmp_ms_name = ms_name + ".tmp"
    tmp_ms_parset = ms_parset + ".tmp" 
    tmp_image_name = "image.img.tmp"
    tmp_imager_parset = imager_parset + ".tmp"

    createTmpMSParset(ms_parset, tmp_ms_parset, tmp_ms_name)
    createTmpImagerParset(imager_parset, tmp_imager_parset, 
                          tmp_image_name, tmp_ms_name)

    cmd = ["makems", tmp_ms_parset]
    try: 
        sp.check_output(cmd, stderr=sp.STDOUT)
    except sp.CalledProcessError:
        # if cmd returns non-zero exit status
        print "ERROR: ", cmd
        exit(2);

    cmd = ["awimager", tmp_imager_parset]
    try: 
        sp.check_output(cmd, stderr=sp.STDOUT)
    except sp.CalledProcessError:
        # if cmd returns non-zero exit status
        print "ERROR: ", cmd
        exit(2);

    # convert pixel sky model to radec skymodel
    radec_skymodel = skymodel + ".radec"
    csm.convertPixelSkymodelToWCS(skymodel, radec_skymodel, tmp_image_name)

    # use radec skymodel to create MS
    createMSradec(radec_skymodel, ms_parset, antenna_set, ms_name, lofar_dir)

    try:
        shutil.rmtree(tmp_ms_name) 
        shutil.rmtree(tmp_image_name) 
        os.remove(tmp_ms_parset)
        os.remove(tmp_imager_parset)
        os.remove(tmp_ms_name + ".gds")
        os.remove(tmp_ms_name + ".vds")
    except:
        print("Not able to remove all temporary files.")




if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Simulate a measurement set (MS) from a skymodel. " +\
        "Uses 'createMS.py' to go from a usual skymodel to an MS. "+\
        "If the source locations are specified in pixels of the final " +\
        "image, the pixel skymodel is first converted to a usual " +\
        "skymodel for which then 'createMS.py' is invoked. " + \
        "Recommend to always use 'simulateMS.py' instead of " +\
        "'createMS.py' directly, as its functionality is a superset of " +\
        "'createMS.py'.")
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
    parser.add_argument('-imp','--imager_parset', 
                        help='Imager parset for creation of a dirty image ' + \
                        '(only required if source locations ' + \
                        'in pixels)', required=False)
    parser.add_argument('-ms','--ms_name', 
                        help='Name of the Measurement set created', 
                        required=True)
    args = parser.parse_args()

    lofar_dir = os.environ["LOFARROOT"]

    print "{0:20}{1:40}".format("Sky model:", args.skymodel)
    print "{0:20}{1:40}".format("MS parset:", args.ms_parset)
    print "{0:20}{1:40}".format("Antenna set:", args.antenna_set)
    print "{0:20}{1:40}".format("Imager parset:", args.imager_parset)
    print "{0:20}{1:40}".format("Output MS:", args.ms_name)
    print "{0:20}{1:40}".format("Using LOFARROOT:", lofar_dir)

    if predicate_in_pixels(args.skymodel):
        # source locations specified in pixels
        if (not args.imager_parset):
            raise ValueError("Imager parset missing.")
        else:
            # source locations specified in pixels AND imager parset present
            createMSpixel(args.skymodel, args.ms_parset,
                          args.antenna_set, args.imager_parset, 
                          args.ms_name, lofar_dir)
    else:
        # the skymodal is "normal"
        createMSradec(args.skymodel, args.ms_parset, args.antenna_set, 
                      args.ms_name, lofar_dir)
        
    

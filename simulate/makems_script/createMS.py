#! /usr/bin/env python

import sys, os
import argparse
import createMS_radecSkymodel
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



def createTmpImagerParset(in_parset, out_parset, image_name):
    with open(in_parset) as in_fh:
        with open(out_parset, "w") as out_fh:
            for line in in_fh:
                if "operation" in line:
                    out_fh.write("operation=empty\n")
                elif "image" in line:
                    out_fh.write("image={0:s}\n".format(image_name))
                else:
                    out_fh.write(line)



def createMSradec(skymodel, ms_parset, antenna_set, ms_name, lofar_dir):
    createMS_radecSkymodel.createMeasurementSet(skymodel, ms_parset, 
                                                ms_name, antenna_set, 
                                                lofar_dir)


def createMSpixel(skymodel, ms_parset, antenna_set, imager_parset, 
                  ms_name, lofar_dir):
    """Input: skymodel using pixel locations
       Input: ..."""    
    

    # create temporary image to extract metadata
    # TODO: create temporary parset to not simulate a long 
    # observation here 
    tmp_image_name = "image.img.tmp"
    tmp_imager_parset = imager_parset + ".tmp"
    createTmpImagerParset(imager_parset, tmp_imager_parset, tmp_image_name)

    cmd = ["awimager", tmp_imager_parset]
    sp.check_output(cmd, stderr=sp.STDOUT)

    # convert pixel sky model to radec skymodel
    radec_skymodel = skymodel + ".radec"
    csm.convertPixelSkymodelToWCS(skymodel, radec_skymodel, tmp_image_name)

    # use radec skymodel to create MS
    createMSradec(radec_skymodel, ms_parset, antenna_set, ms_name, lofar_dir)

    #    os.rmtree() # remove tmp image
    os.remove(tmp_imager_parset)





if __name__ == "__main__":
    """Create a measurement from a skymodel"""
    parser = argparse.ArgumentParser()

    parser.add_argument('--skymodel', 
                        help='skymodel (optional: source locations in pixels)',
                        type=str, required=True)
    parser.add_argument('--ms_parset', 
                        help='Measurement set parset',
                        type=str, required=True)
    parser.add_argument('--antenna_set', 
                        help='[LBA_INNER|LBA_OUTER|HBA_ZERO|HBA_ONE|' + \
                        'HBA_JOINED|HBA_DUAL]', 
                        type=str, required=False, default="HBA_DUAL")
    parser.add_argument('--imager_parset', 
                        help='Imager parset for creation of a dirty image ' + \
                        '(required, if source locations ' + \
                        'in pixels)', type=str, required=False)
    parser.add_argument('--ms_name', 
                        help='Name of the Measurement set created', 
                        type=str, required=True)
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
        
    

#! /usr/bin/env python

import sys, os
import coord_convert as cc

def convertPixelSkymodelToWCS(infile, outfile, image):
    """Input: skymodel with pixel coordinates using 'RaAsPixel' and 
              'DecAsPixel' in format specification
       Input: (temporary) image used to extract metadata 
       Output: skymodel with world coordinates"""
    with open(infile,'r') as in_fh:
        with open(outfile, 'w') as out_fh:
            for in_line in in_fh:
                if len(in_line.strip()) == 0 or in_line.strip()[0] == "#":
                    out_fh.write(in_line)
                elif in_line.strip()[:6] == 'FORMAT':
                    format_line_split = [a.strip() for a in in_line.split(",")]
                    try:
                        Ra_position = format_line_split.index("RaAsPixel")
                        Dec_position = format_line_split.index("DecAsPixel")
                    except ValueError:
                        raise ValueError("No 'RaAsPixel' and 'DecAsPixel' specified " + \
                                         "in format line.")
                    format_line_split[Ra_position] = 'Ra'
                    format_line_split[Dec_position] = 'Dec'
                    format_line = ", ".join(format_line_split) + "\n"
                    out_fh.write(format_line)
                else:
                    line_split = [a.strip() for a in in_line.split(",")]
                    try:
                        Ra_pixel = int(line_split[Ra_position])
                        Dec_pixel = int(line_split[Dec_position])
                    except ValueError:
                        raise ValueError("'RaAsPixel' or 'DecAsPixel' is not integer.")
                    (Ra_str, Dec_str) = cc.pix2radecstrings(image, Ra_pixel, 
                                                                Dec_pixel)
                    line_split[Ra_position] = Ra_str
                    line_split[Dec_position] = Dec_str
                    line = ", ".join(line_split) + "\n"
                    out_fh.write(line)

if __name__ == "__main__":
    infile = sys.argv[1]
    outfile = sys.argv[2]
    image = sys.argv[3]
    convertPixelSkymodelToWCS(infile, outfile, image)

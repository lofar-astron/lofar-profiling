#! /usr/bin/env python
import sys
from lofar import bdsm

img = bdsm.process_image(sys.argv[1], atrous_do=True)
img.export_image(img_format='casa', img_type='island_mask', outfile=sys.argv[2])
img.write_catalog(outfile=sys.argv[3])

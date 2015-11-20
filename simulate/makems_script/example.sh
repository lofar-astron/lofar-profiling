#!/usr/bin/env bash

./createMS.py --skymodel pixel.skymodel --ms_parset test.parset --antenna_set HBA_DUAL --ms_name TEST.MS --imager_parset test.awimager.dirty.parset

# DIRTY IMAGE: awimager from LOFAR
awimager test.awimager.dirty.parset
# convert output to fits file using casacore 
image2fits in=dirty.img out=dirty.fits

# # CLEAN IMAGE: awimager from LOFAR
awimager test.awimager.clean.parset
# # convert output to fits file using casacore 
image2fits in=clean.img.model out=clean.model.fits
image2fits in=clean.img.psf out=clean.psf.fits
image2fits in=clean.img.residual out=clean.residual.fits
image2fits in=clean.img.restored out=clean.restored.fits

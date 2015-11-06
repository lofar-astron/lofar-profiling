#!/usr/bin/env bash

./createMeasurementSet.py test.skymodel test.parset TEST.MS

# DIRTY IMAGE: awimager from LOFAR
awimager test.awimager.dirty.parset
# convert output to fits file using casacore 
image2fits in=dirty.img out=dirty.fits

# CLEAN IMAGE: awimager from LOFAR
awimager test.awimager.clean.parset
# convert output to fits file using casacore 
image2fits in=clean.img.model out=clean.model.fits
image2fits in=clean.img.psf out=clean.psf.fits
image2fits in=clean.img.residual out=clean.residual.fits
image2fits in=clean.img.restored out=clean.restored.fits

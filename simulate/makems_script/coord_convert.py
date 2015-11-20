#! /usr/bin/env python

import sys
from math import floor, radians, degrees
from casacore import images

Nfloor = 10
#ra_center_pixel = 1025
#ra_center_value = 240
#ra_delta = -3.333333e-3

#dec_center_pixel = 1025
#dec_center_value = 62
#dec_delta = 3.33333e-3

# Start of image independent functions
def deg2hr(deg):
    """input:  degrees as floating point
       output: hour angle as floating point"""
    hr = (deg / 360.) * 24
    return hr

def hr2deg(hr):
    """input:  hour angle as floating point
       output: degrees as floating point"""
    deg = (hr/24.) * 360
    return deg

def deg2rastring(deg):
    """input:  degree as floating point.
       output: hour angle as hour.minute.second"""
    hr = deg2hr(deg)
    hour_angle = int(floor(hr))
    hour_angle_minute = int(floor((hr-hour_angle)*60.)) 
    hour_angle_second = abs((hr - hour_angle - (hour_angle_minute/60.))*(60.*60.))
    # assuming double precision: 17 digits, single precision would be 9 digits
    return "{0:d}:{1:d}:{2:.17f}".format(hour_angle, hour_angle_minute, hour_angle_second)

def deg2decstring(deg):
    """input:  degree as floating point. 
       output: degree as degree:arcminute:arcsecond"""
    degree = int(floor(deg))
    arc_minute = int(floor((deg - degree)*60.))
    arc_second = abs((deg - degree - (arc_minute/60.))*(60*60.))
    # assuming double precision: 17 digits, single precision would be 9 digits
    return "{0:d}.{1:d}.{2:.17f}".format(degree, arc_minute, arc_second)

def rastring2deg(rastring):
    """input:  hour angle as hour.minute.second
       output: degree as floating point."""
    ra_tuple = rastring.split(":")
    deg_hour_angle = hr2deg(int(ra_tuple[0]))
    deg_hour_angle_minute = hr2deg(int(ra_tuple[1])/60.)
    deg_hour_angle_second = hr2deg(float(ra_tuple[2])/(60.*60.))
    deg = deg_hour_angle + deg_hour_angle_minute + deg_hour_angle_second
    return deg

def decstring2deg(decstring):
    """input:  degree as degree:arcminute:arcsecond
       output: degree as floating point."""
    dec_tuple = decstring.split(".")
    deg_degree = int(dec_tuple[0])
    deg_minute = int(dec_tuple[1])/60.
    deg_second = float(".".join(dec_tuple[2:]))/(60.*60.)
    deg = deg_degree + deg_minute + deg_second
    return deg

# start of image dependent functions

def pix2radec(image, i, j):
    """input:  (image, i,j) image name as string, 
                            pixel coordinates as int, (0,0) is lower left (TBC)
       output: (ra, dec) sky coordinates as degree in float"""
    casa_image = images.image(image)
    world_vals = casa_image.toworld((0,0,j,i)) # in: frequency, stokes (0-3), jpixel, ipixel
                                               # out: frequency, stokes (1-4), dec, ra
    print(world_vals)
    ra = degrees(world_vals[3])
    dec = degrees(world_vals[2])
    return (ra, dec) 
     

def radec2pix(image, ra, dec):
    """input:  (image, ra, dec) image name as string, 
                                sky coordinates as degree in float
       output: (i,j) pixel coordinates as int, (0,0) is lower left (TBC)"""
    casa_image = images.image(image)
    ra = radians(ra)
    dec = radians(dec)
    pix_vals = casa_image.topixel((0,1,dec,ra)) # in: frequency, stokes (1-4), dec, ra
                                                # out: frequency, stokes (0-3), jpixel, ipixel
    i = int(floor(pix_vals[3])) # roundoff to prevent 1023.999999999999 to become 1023
    j = int(floor(pix_vals[2])) # roundoff to prevent 1023.999999999999 to become 1023 
    return (i, j)

def pix2radecstrings(image, i, j):
    """input:  image name as string
               (i, j) pixel coordinates as int
       output: (ra, dec)
               ra  as hour.minute.second 
               dec as degree:arcminute:arcsecond"""
    ra, dec = pix2radec(image, i, j)
    rastr = deg2rastring(ra)
    decstr = deg2decstring(dec)
    return (rastr, decstr)

def radecstrings2pix(image, rastr, decstr):
    """input:  image name as string
               ra  as hour.minute.second
               dec as degree:arcminute:arcsecond
       output: (i, j) pixel coordinates as int"""  
    ra = rastring2deg(rastr)
    dec = decstring2deg(decstr)
    i, j = radec2pix(image, ra, dec)
    return (i,j)

# Old versions. Those don't actually work (we didn't take any spherical projection effects 
# into account. However those functions can be used for reference purposes. 
#def pix2radec(i, j):
#    """input:  (i,j) pixel coordinates as int, (0,0) is lower left (TBC)
#       output: (ra, dec) sky coordinates as degree in float"""
#    idiff = i - ra_center_pixel
#    jdiff = j - dec_center_pixel
#    
#    radiff  = idiff * ra_delta
#    decdiff = jdiff * dec_delta
#
#    ra  = ra_center_value + radiff
#    dec = dec_center_value + decdiff
#    return (ra, dec)

#def radec2pix(ra,dec):
#    """input:  (ra, dec) sky coordinates as degree in float
#       output: (i,j) pixel coordinates as int, (1,1) is lower left (TBC)"""
#    radiff  = ra - ra_center_value
#    decdiff = dec - dec_center_value
#    
#    idiff = radiff / ra_delta
#    jdiff = decdiff / dec_delta
#
#    i = floor(ra_center_pixel + idiff)
#    j = floor(dec_center_pixel + jdiff)
#    return (i,j)


# RA  HH:MM:SS (24 hours = 360 degrees, 60 minutes = 1 hour, 60 seconds = 1 minute)
# In the header of the FITS file, RA is in degrees, just to keep it easy.
# DEC DD:MM:SS (1 degree = 60 minutes, 1 minute = 60 seconds)

#CTYPE1  = 'RA---SIN'                                                            
#CRVAL1  =   2.400000000000E+02                                                  
#CDELT1  =  -3.333333333333E-03                                                  
#CRPIX1  =   1.025000000000E+03                                                  
#CUNIT1  = 'deg     '                                                            
#CTYPE2  = 'DEC--SIN'                                                            
#CRVAL2  =   6.200000000000E+01                                                  
#CDELT2  =   3.333333333333E-03                                                  
#CRPIX2  =   1.025000000000E+03  

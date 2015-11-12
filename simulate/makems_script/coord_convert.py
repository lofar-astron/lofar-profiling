import sys
from math import floor

ra_center_pixel = 1025
ra_center_value = 240
ra_delta = -3.333333e-3

dec_center_pixel = 1025
dec_center_value = 62
dec_delta = 3.33333e-3

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
    hour_angle_second = (hr - hour_angle - (hour_angle_minute/60.))*(60.*60.)
    return "%s:%s:%s"%(hour_angle, hour_angle_minute, hour_angle_second)

def deg2decstring(deg):
    """input:  degree as floating point. 
       output: degree as degree:arcminute:arcsecond"""
    degree = int(floor(deg))
    arc_minute = int(floor((deg - degree)*60.))
    arc_second = (deg - degree - (arc_minute/60.))*(60*60.)
    return "%s.%s.%s"%(degree, arc_minute, arc_second)

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
    dec_tuple = decsring.split(".")
    deg_degree = int(dec_tuple[0])
    deg_minute = int(dec_tuple[1])/60.
    deg_second = float(dec_tuple[2:]/(60.*60.))
    deg = deg_degree + deg_minute + deg_second
    return deg

# start of image dependent functions
def pix2radec(i, j):
    """input:  (i,j) pixel coordinates as int, (0,0) is lower left (TBC)
       output: (ra, dec) sky coordinates as degree in float"""
    idiff = i - ra_center_pixel
    jdiff = j - dec_center_pixel
    
    radiff  = idiff * ra_delta
    decdiff = jdiff * dec_delta

    ra  = ra_center_value + radiff
    dec = dec_center_value + decdiff
    return (ra, dec)

def radec2pix(ra,dec):
    """input:  (ra, dec) sky coordinates as degree in float
       output: (i,j) pixel coordinates as int, (1,1) is lower left (TBC)"""
    radiff  = ra - ra_center_value
    decdiff = dec - dec_center_value
    
    idiff = radiff / ra_delta
    jdiff = decdiff / dec_delta

    i = floor(ra_center_pixel + idiff)
    j = floor(dec_center_pixel + jdiff)
    return (i,j)


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

#!/usr/bin/env python
#===============================================================================
# all_icons_displayer.py
# 
# 2016-08-10
# Test module used to display all icons stored in led8x8icons.py in turn to 8x8 
# led matrices to check how they look
# Need to ensure that PYTHONPATH env var includes project root so can import
# rpi-weather module from parent dir
#===============================================================================

import time
import sys

from rpi_weather import RpiWeather
from led8x8icons import LED8x8ICONS

display = RpiWeather()

class Unbuffered(object):
    """Used to ensure sleep function works as expected
    (http://stackoverflow.com/questions/107705/disable-output-buffering)"""
    def __init__(self, stream):
        self.stream = stream
    def write(self, data):
        self.stream.write(data)
        self.stream.flush()
    def __getattr__(self, attr):
        return getattr(self.stream, attr)

def display_all_icons():
    """Display all icons in the led8x8icons dictionary"""
    display.clear_disp()
    number_of_icons = len(LED8x8ICONS)
    print number_of_icons
    for i in xrange(number_of_icons):
        display.clear_disp()
        for matrix in xrange(4):
            try:
                print "key: {0} - value: {1}".format(LED8x8ICONS.keys()[matrix], LED8x8ICONS.values()[matrix])
                display.set_raw64(LED8x8ICONS.values()[matrix], matrix)
            except:
                print "NUMBER NOT KNOWN"
                display.set_raw64(LED8x8ICONS["UNKNOWN"], matrix)
        time.sleep(3)
        
#-------------------------------------------------------------------------------
#  M A I N
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    sys.stdout = Unbuffered(sys.stdout)
    display_all_icons()
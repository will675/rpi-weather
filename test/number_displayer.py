#!/usr/bin/env python
#===============================================================================
# number_displayer.py
# 
# 2016-08-10
# Test module used to display numbers to 8x8 led matrices to check how they look
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

def display_numbers(top=None):
    """Display numbers up to top value on LED 8x8 matrices."""
    display.clear_disp()
    if top == None:
        return
    count = 0
    for i in xrange(top):
        display.clear_disp()
        for matrix in xrange(4):
            try:
                print count
                display.set_raw64(LED8x8ICONS[str(count)], matrix)
            except:
                print "NUMBER NOT KNOWN"
                display.set_raw64(LED8x8ICONS["UNKNOWN"], matrix)
        time.sleep(1)
        count += 1
        
#-------------------------------------------------------------------------------
#  M A I N
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    sys.stdout = Unbuffered(sys.stdout)
    display_numbers(40)
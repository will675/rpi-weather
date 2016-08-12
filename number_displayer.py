import time
import sys

from rpi_weather import RpiWeather
from led8x8icons import LED8x8ICONS

display = RpiWeather()

class Unbuffered(object): # Used to ensure sleep function works as expected (http://stackoverflow.com/questions/107705/disable-output-buffering)
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)

def display_numbers(top=None):
    """Display numbers up to top value on LED 8x8 matrices."""
    if top == None:
        return
    count = 0
    # display.set_raw64(LED8x8ICONS["MINUS"], 0)
    # time.sleep(1)
    for i in xrange(top+1):
        for matrix in xrange(4):
            try:
                print count
                if count < 40:
                    display.set_raw64(LED8x8ICONS[str(count)], matrix)
                else:
                    display.set_raw64(LED8x8ICONS["PLUS"], matrix)
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
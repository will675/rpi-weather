

from rpi_weather import RpiWeather
from led8x8icons import LED8x8ICONS

display = RpiWeather()

def display_numbers(top=None):
    """Display numbers up to top value on LED 8x8 matrices."""
    if top == None:
        return
    count = 0
    for matrix in xrange(4):
        try:
            print count
            display.set_raw64(LED8x8ICONS[count], matrix)
            count += 1
        except:
            print "NUMBER NOT KNOWN"
            display.set_raw64(LED8x8ICONS["UNKNOWN"], matrix)
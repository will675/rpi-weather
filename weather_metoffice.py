#!/usr/bin/env python
#===============================================================================
# weather_metoffice.py
#
# Get weather forecast from the Met Office and display as 8x8 icons
#   * Met Office's doc: http://www.metoffice.gov.uk/datapoint/support/api-reference
#   * Retrieve location id from: http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/sitelist?key=2a26370d-c529-496c-8d9d-7c7b8468e379
#   * Uses 'UK daily site specific forecast'
#   * Need to have an API key from Met Office: https://register.metoffice.gov.uk/WaveRegistrationClient/public/register.do?service=datapoint
#
# 2016-08-07
# Created by: Carter Nelson
# Modified to Met Office by: Will Jenkins
#===============================================================================

import time
import httplib
import sys
import json
import ConfigParser
import logging

from logging.handlers import TimedRotatingFileHandler

from rpi_weather import RpiWeather
from led8x8icons import LED8x8ICONS

display = RpiWeather()

METOFFICE_URL    = "datapoint.metoffice.gov.uk"
REQ_BASE    = r"/public/data/val/wxfcs/all/json/"
CONFIG_FILE = "weather.cfg"
API_KEY = None
LOCATION_ID = None
LOG_FILE = None
LOG_LEVEL = None
LOG_TO_FILE = False
NIGHT_START = None

ICON_MAP = { # Day forecast codes only
#   Met Office weather code         LED 8x8 icon
    0:                              "MOON",         # Clear night
    1:                              "SUNNY",        # Sunny day
    2:                              "PART_CLOUD",   # Partly cloudy (night)
    3:                              "PART_CLOUD",   # Partly cloudy (day)
    4:                              "UNKNOWN",      # Not used
    5:                              "FOG",          # Mist
    6:                              "FOG",          # Fog
    7:                              "CLOUD",        # Cloudy
    8:                              "CLOUD",        # Overcast
    9:                              "SHOWERS",      # Light rain shower (night)
    10:                             "SHOWERS",      # Light rain shower (day)
    11:                             "RAIN",         # Drizzle
    12:                             "RAIN",         # Light rain
    13:                             "SHOWERS",      # Heavy rain shower (night)
    14:                             "SHOWERS",      # Heavy rain shower (day)
    15:                             "RAIN",         # Heavy rain
    16:                             "SHOWERS",      # Sleet shower (night)
    17:                             "SHOWERS",      # Sleet shower (day)
    18:                             "RAIN",         # Sleet
    19:                             "HAIL",         # Hail shower (night) 
    20:                             "HAIL",         # Hail shower (day)
    21:                             "HAIL",         # Hail
    22:                             "SNOW",         # Light snow shower (night)
    23:                             "SNOW",         # Light snow shower (day)
    24:                             "SNOW",         # Light snow
    25:                             "SNOW",         # Heavy snow shower (night)
    26:                             "SNOW",         # Heavy snow shower (day)
    27:                             "SNOW",         # Heavy snow
    28:                             "STORM",        # Thunder shower (night)
    29:                             "STORM",        # Thunder shower (day)
    30:                             "STORM"         # Thunder 
}

class Unbuffered(object):
    """Ensures sleep function works as expected 
    (http://stackoverflow.com/questions/107705/disable-output-buffering)"""
    def __init__(self, stream):
        self.stream = stream
    def write(self, data):
        self.stream.write(data)
        self.stream.flush()
    def __getattr__(self, attr):
        return getattr(self.stream, attr)

def giveup():
    """Action to take if anything bad happens."""
    for matrix in xrange(4):
        display.set_raw64(LED8x8ICONS['UNKNOWN'],matrix)
    print "Error occured."
    sys.exit(1)
    
def read_config(filename):
    """Get config settings"""
    config = ConfigParser.RawConfigParser()
    global API_KEY, LOCATION_ID, LOG_FILE, LOG_LEVEL, LOG_TO_FILE, NIGHT_START
    try:
        config.read(filename)
        API_KEY     = config.get('config','API_KEY')
        LOCATION_ID = config.get('config','LOCATION_ID')
        LOG_FILE    = config.get('config', 'LOG_FILE')
        LOG_LEVEL    = config.get('config', 'LOG_LEVEL')
        LOG_TO_FILE = config.get('config', 'LOG_TO_FILE')
        NIGHT_START = config.get('config', 'NIGHT_START')
    except Exception as err:
        print err
        giveup()

def start_logging():
    """Generate log file using TimedRotatingFileHandler() and record the starting datetime of the script run"""
    handler = TimedRotatingFileHandler(LOG_FILE, when='d', interval=1, backupCount=5)
    formatter = logging.Formatter("%(asctime)s : %(levelname)s : %(message)s", "%Y-%m-%d %H:%M:%S")
    handler.setFormatter(formatter)
    logger = logging.getLogger()
    if LOG_LEVEL == 'Info':
    	logger.setLevel(logging.INFO)
    elif LOG_LEVEL == 'Debug':
	logger.setLevel(logging.DEBUG)
    else:
    	print "Invalid LOG_LEVEL set: {0}".format(LOG_LEVEL)
	giveup()
    logger.addHandler(handler)
    logging.info('-'*35)
    logging.info("Script started: {0}".format(time.strftime('%Y/%m/%d %H:%M:%S')))
    logging.info('-'*35)
        
def make_metoffice_request():
    """Make request to metoffice.gov.uk and return data.  Logs response status to file"""
    REQUEST = REQ_BASE + format(LOCATION_ID) + "?res=daily&key=" + API_KEY
    try:
        conn = httplib.HTTPConnection(METOFFICE_URL)
        conn.request("GET", REQUEST)
        resp = conn.getresponse()
        data = resp.read()
        if resp.status != 200:
            if LOG_TO_FILE == 'True':
                logging.error("Non-200 status returned by api: {}".format(resp.status))
            else:
                print "Non-200 status returned by api: {}".format(resp.status)
            giveup()
        else:
            if LOG_TO_FILE == 'True':
                logging.info("200 status returned by api")
            else:
                print "200 status returned by api"
    except Exception as err:
        logging.error("Error encountered on api request: {}".format(err))
        print err
    else:
        return data
    
def get_forecast():
    """Return a list of forecast results. Logs forecast and temp values for each day to file, 
    as well as any unknown values encountered."""
    json_data = json.loads(make_metoffice_request())
    forecast = []
    temperature = []
    current_hour = time.localtime().tm_hour
    if (current_hour < int(NIGHT_START)): # Use day forcast for all days if current time is before 18:00 
        for day in xrange(4):
            forecast.append(json_data["SiteRep"]["DV"]["Location"]["Period"][day]["Rep"][0]["W"])
            temperature.append(json_data["SiteRep"]["DV"]["Location"]["Period"][day]["Rep"][0]["Dm"])
            if LOG_TO_FILE == 'True':
                try:
                    logging.info("Day {0} : forecast - {1} - {2}".format(day, forecast[day], ICON_MAP[int(forecast[day])]))
                    logging.info("Day {0} : maximum temp - {1}".format(day, temperature[day]))
                except Exception as err:
                    logging.error("Day {0} : unknown weather type encountered - {1}".format(day, err))
            else:
                try:
                    print "Day {0} : forecast - {1} - {2}".format(day, forecast[day], ICON_MAP[int(forecast[day])])
                    print "Day {0} : maximum temp - {1}".format(day, temperature[day])
                except Exception as err:
                    print "Day {0} : unknown weather type encountered - {1}".format(day, err)
    else: # Use night forecast for first day if current time is equal or after 18:00
        forecast.append(json_data["SiteRep"]["DV"]["Location"]["Period"][0]["Rep"][1]["W"])
        temperature.append(json_data["SiteRep"]["DV"]["Location"]["Period"][0]["Rep"][1]["Nm"])
        if LOG_TO_FILE == 'True':
            try:
                logging.info("Night {0} : forecast - {1} - {2}".format(0, forecast[0], ICON_MAP[int(forecast[0])]))
                logging.info("Night {0} : minimum temp - {1}".format(0, temperature[0]))
            except Exception as err:
                logging.error("Night {0} : unknown weather type encountered - {1}".format(0, err))
        else:
            try:
                print "Night {0} : forecast - {1} - {2}".format(0, forecast[0], ICON_MAP[int(forecast[0])])
                print "Night {0} : minimum temp - {1}".format(0, temperature[0])
            except Exception as err:
                print "Night {0} : unknown weather type encountered - {1}".format(0, err)
                
        for day in xrange(1, 4): # Need to then get the next three days' forecast
            forecast.append(json_data["SiteRep"]["DV"]["Location"]["Period"][day]["Rep"][0]["W"])
            temperature.append(json_data["SiteRep"]["DV"]["Location"]["Period"][day]["Rep"][0]["Dm"])
            if LOG_TO_FILE == 'True':
                try:
                    logging.info("Day {0} : forecast - {1} - {2}".format(day, forecast[day], ICON_MAP[int(forecast[day])]))
                    logging.info("Day {0} : maximum temp - {1}".format(day, temperature[day]))
                except Exception as err:
                    logging.error("Day {0} : unknown weather type encountered - {1}".format(day, err))
            else:
                try:
                    print "Day {0} : forecast - {1} - {2}".format(day, forecast[day], ICON_MAP[int(forecast[day])])
                    print "Day {0} : maximum temp - {1}".format(day, temperature[day])
                except Exception as err:
                    print "Day {0} : unknown weather type encountered - {1}".format(day, err)
    return forecast, temperature

def display_forecast(forecast = None, temperature = None):
    """Display forecast as icons on LED 8x8 matrices."""
    if (forecast == None or temperature == None):
        return
    for turns in xrange(360): # This will loop the current forecast and temp for about an hour before going to get latest from met office
        for matrix in xrange(4):
            try:
                icon = ICON_MAP[int(forecast[matrix])]
                display.set_raw64(LED8x8ICONS[icon], matrix)
            except Exception as err:
                if LOG_TO_FILE == 'True':
                    logging.error("Day {0} : unknown weather type encountered - {1}".format(matrix, err))
                else:
                    print "Day {0} : unknown weather type encountered - {1}".format(matrix, err)
                display.set_raw64(LED8x8ICONS["UNKNOWN"], matrix)
        time.sleep(5)
        for matrix in xrange(4):
            try:
                value = str(temperature[matrix])
                display.set_raw64(LED8x8ICONS[value], matrix)
            except Exception as err:
                if LOG_TO_FILE == 'True':
                    logging.error("Day {0} : no temperature found - {1}".format(matrix, err))
                else:
                    print "Day {0} : no temperature found - {1}".format(matrix, err)
                display.set_raw64(LED8x8ICONS["UNKNOWN"], matrix)
        time.sleep(5)

#-------------------------------------------------------------------------------
#  M A I N
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    # Need to override buffered version of stdout to ensure sleep function works as expected (http://stackoverflow.com/questions/107705/disable-output-buffering)
    sys.stdout = Unbuffered(sys.stdout)
    read_config(CONFIG_FILE)
    start_logging()
    while True: # Top level loop in display_forecast() dictates how often new forecast is pulled from metoffice api
        forecast, temperature = get_forecast()
        display_forecast(forecast, temperature)

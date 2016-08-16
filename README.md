# rpi-weather
This is a fork from the excellent repo created by [caternuson](https://github.com/caternuson/rpi-weather)

That includes the initial integration with the [**metoffice.gov.uk**](http://www.metoffice.gov.uk/datapoint) API, but I have since updated this version to include:
* New elements in ICON_MAP to cover all the numbers from 1 to 39 (to (potentially) cover the full extremes of the British weather)
* New elements in ICON_MAP to cover partially cloudy and foggy days, plus hail.  Not the best, I admit, but will do for now...
* Alternating display between weather type for the day and maximum temperature using loops, so script can be started once on bootup then run continuously, rather than running via **cron**
* Night-time weather type and minimum temp display for the current day when current time goes past 6pm
* Logging to file rather than to console
 

## To Do List
- [X] Alternating weather type/temperature display
- [X] Numeric elements to ICON_MAP
- [X] New weather type elements to ICON_MAP
- [X] Night-time weather and minimum temp for current day
- [X] Logging to file
- [ ] Negative numeric elements to ICON_MAP
- [ ] Full setup notes for going from a blank SD card to a fully working rpi-weather config (so should I brick it somehow I don't have to hunt around to set it all up again...)
- [ ] BDD style tests (so I can learn [Behave](http://pythonhosted.org/behave), the Python version of Cucumber)

## SD Card Setup
1. Install [raspbian-lite](https://www.raspberrypi.org/downloads/raspbian)

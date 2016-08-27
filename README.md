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
- [X] Negative numeric elements to ICON_MAP
- [ ] Move logging and printing to console to separate function that takes level and string
- [ ] Set RPi up to automatically run script from start via init.d
- [ ] Full setup notes for going from a blank SD card to a fully working rpi-weather config (so should I brick it somehow I don't have to hunt around to set it all up again...)
- [ ] Wipe my SD card and try the notes below, to check if they are correct

## SD Card Setup
1. Install [raspbian-lite](https://www.raspberrypi.org/downloads/raspbian)
2. Boot up and change pi user password from default **raspberry** - ```passwd```
3. Create new user so can delete pi once happy all is in place - ```sudo addusr xyz```
4. Add user to sudo - ```sudo visudo```
5. Change default editor to vim - ```sudo update-alternatives --set editor /usr/bin/vim.tiny```
6. Log on as new user xyz
7. Update apt-get - ```sudo apt-get update```
8. Install git to make it easy to get the repo in the RPi, and make/get changes as needed - ```sudo apt-get install git```
9. Create non-sudo user to run script under, hopefully makes things more secure? - ```sudo addusr abc```
10. Install normal vim - ```sudo apt-get install vim```
11. Add support for wifi dongle - ```sudo vim /etc/wpa_supplicant/wpa_supplicant.conf```
12. Update it to include the following (as seen [here](https://cdn.shopify.com/s/files/1/0176/3274/files/blog_pi_wifi_commands.png?6605))- ```network={
    ssid="YOUR-SSID"
    psk="PASSWORD"
}```
13. Shutdown the RPi, disconnect the ethernet cable and plug in the USB wifi dongle
14. Restart the RPi, should now be on the wifi network
15. Change the hostname (as detailed [here](http://www.howtogeek.com/167195/how-to-change-your-raspberry-pi-or-other-linux-devices-hostname)) to something more unique:

  *```sudo vim /etc/hosts```
  
  *```sudo vim /etc/hostname```
  
  *```sudo /etc/init.d/hostename.sh```
16. Restart the RPi - ```sudo restart -h now```
17. Configure i2c to work on the RPi (as detailed [here](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c)):

  *```sudo apt-get install python-smbus```
  
  *```sudo apt-get install i2c-tools```
  
  *```sudo raspi-config```
18. Restart the RPi - ```sudo restart -h now```
19. Connect up the LED matices and check i2c is up and running - ```sudo i2cdetect -y 0``` (**Using 256Mb Model A RPi so need ```0``` on end, rather than ```1``` for subsequent models**)
20. Install the adafruit LED backpack library (as described [here](https://learn.adafruit.com/led-backpack-displays-on-raspberry-pi-and-beaglebone-black/usage)) :

  *```sudo apt-get update```
  
  *```sudo apt-get install build-essential python-dev python-imaging```
  
  *Navigate to home directory for new non-sudo user account **abc**
  
  *``git clone https://github.com/adafruit/Adafruit_Python_LED_Backpack.git``
  
  *```cd Adafruit_Python_LED_Backpack```
  
  *```sudo python setup.py install```
  
  21. Clone this repo into that same home directory for **abc**
  ### init.d Setup
  (All figured out using the very helpful details from [here](http://raspberrywebserver.com/serveradmin/run-a-script-on-start-up.html)
  22. Copy the **weather** script from ```./etc/init.d/``` into ```/etc/init.d/``` - ```sudo cp etc/init.d/weather /etc/init.d/```
  23. Check that the script works by calling it to start the service - ```sudo /etc/init.d/weather start```
  24. Stop it using ```sudo /etc/init.d/weather stop```
  25. Run this command to make it start on bootup - ```sudo update-rc.d weather defaults```

# pi-shortcuts
A little physical USB keyboard for shortcuts using my PI Zero W using any old crap I have lying around the house.


Prototype for now. Still a right mess of code and wires but it is working i.e. stuffing keyboard and providing some feed back.


https://ozeki.hu/p_3054-how-to-setup-a-rotary-encoder-on-raspberry-pi.html
https://raspberrypi.stackexchange.com/questions/51142/wire-button-without-resistor

# Features 

* YAML file which is simple to setup the mapping/sequences using TOKENS for non-printable chars
  e.g. ALT, CTRL, SHIIFT, LS etc     
      Examples: LS-a CTRL-ALT-t
* Scrolls in an external file (can use this for showing cron based external data)
* Toggle a full screen clock and current layer level and hints
* Builtin alarm clock - will need to add beeper of some kind but flashes for the moment
* Shows the most recent macro processed
* Jog wheel or joystick for menu selection (can be used for macros)
* Added 1/4" jack so i can use foot peddle switche



# Todos

* TODO Multiple alarms (that persist on power cycle)
* TODO Alarm message to set?
* TODO Multiple timer and reset (that persist on power cycle)
* TODO Alarm to trigger keypress or URL trigger
* TODO Any LEDS? What for?
* TODO for other common characters add extra keypresses to make more readable e.g. LS-7 -> &
* TODO Change layer yaml to title
* TODO Add light detector to signal something?
* TODO External api calls to do things: string -> url
* TODO Method to send arbitry HID control numbers through could use #<number>
* TODO Method to send arbitry full HID control sequences
* TODO fix key bounce - perhaps have a property that allows repeating key or prevent key bounce
* TODO Put alarm time on clock to right edge
* TODO Use alarm pixel image instead of asterisk for alarm indicator
* TODO Add a thrid screen following big clock mode.... Menu for some other features. But what?
* TODO Third panel to display full text of MOTD which can be scrolled up and down with jog wheel
* TODO do mail box monitor?
* TODO add rss feed? - allow button to launch link to browser
* TODO for my motd mytodos.uk feed add a button to launch browser on task in feed (use from full display panel)
* TODO streamline the layer scanning



# Installation

install_i2c.sh - Sets up the i2c for the OLED display
install_usb_hid.sh - This USB HID config worked for me. Others didn't so if not then look around too. Don't know why the others didnt, perhaps

Linux (Ubuntu) didn't like the others and some examples showed connected with Windows. 

Update /etc/rc.local to run /home/pi/usbhid.sh script at start up as the HID feature does not survive reboots. Can then run the python scripts.


/home/pi/usbhid.sh 

/usr/bin/python /home/pi/pi-shortcuts.py >/dev/null 2>&1 &


pip install PyYAML

Using details from:

https://tutorials-raspberrypi.de/raspberry-pi-lcd-display-16x2-hd44780/


* Wiring Up

oled 
https://www.raspberrypi-spy.co.uk/2018/04/i2c-oled-display-module-with-raspberry-pi/

* Using keypad 


3 pin
              gpio        pin
green         17           11
blue          27           13
purple        22           15


4 pin

yellow        16          36
orange        26           37
red           20           38
brown         21           40







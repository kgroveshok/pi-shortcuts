# pi-shortcuts
A little physical USB keyboard for shortcuts using my pi zero


Prototype for now. Still a right mess of code and wires but it is working i.e. stuffing keyboard and providing some feed back



* Going to try HD44780

pip install PyYAML

Using details from:

https://tutorials-raspberrypi.de/raspberry-pi-lcd-display-16x2-hd44780/

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




install_i2c.sh - Sets up the i2c for the OLED display
install_usb_hid.sh - This USB HID config worked for me. Others didn't so if not then look around too. Don't know why the others didnt, perhaps
Linux (Ubuntu) didn't like the others and some examples showed connected with Windows. 

Update /etc/rc.local to run /home/pi/usbhid.sh script at start up as the HID feature does not survive reboots. Can then run the python scripts.



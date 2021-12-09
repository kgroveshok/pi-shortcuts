#!/bin/sh

# https://www.raspberrypi-spy.co.uk/2018/04/i2c-oled-display-module-with-raspberry-pi/

sudo apt install -y python3-dev
sudo apt install -y python-smbus i2c-tools
sudo apt install -y python3-pil
sudo apt install -y python3-pip
sudo apt install -y python3-setuptools
sudo apt install -y python3-rpi.gpio


sudo apt install -y git

git clone https://github.com/adafruit/Adafruit_Python_SSD1306.git

cd Adafruit_Python_SSD1306

sudo python setup.py install



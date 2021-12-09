#!/usr/bin/python

# not pretty but trying to get a basic working prototype
# TODO streamline the layer scanning
# TODO handle more complex key mapping notation

import yaml
import sys
import time
import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from datetime import datetime

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# Beaglebone Black pin configuration:
# RST = 'P9_12'
# Note the following are only used with SPI:
# DC = 'P9_15'
# SPI_PORT = 1
# SPI_DEVICE = 0

# 128x32 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)


# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()
# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Load default font.
font = ImageFont.load_default()



# Read pin wiring YAML file

#with open("pi-shortcuts-pins.yaml", 'r') as stream:
#    pinmap = yaml.safe_load(stream)


#print( pinmap )


# Read shortcuts YAML file

with open("/home/pi/pi-shortcuts.yaml", 'r') as stream:
    shortcuts = yaml.safe_load(stream)


print( shortcuts )

#def pingToChar:
#
#    c = sys.stdin.read(1) # reads one byte at a time, similar to getchar()
#    #str += c
#
#    return c

#def charToPins( c ) :
#   col=0
#   row=0
#   for k in pinmap['keymap']:
#      if k['key'] == c:
#         col = k['col']
#         row = k['row']
#         print( k )
#   #for g in pinmap['gpio'] :
#   #   print( g )
#   #   if g['row'] == row and g['col'] == col :
#   #      print( 
#
#   return   


NULL_CHAR = chr(0)

HIDMAP = {

   'a' : NULL_CHAR*2+chr(4)+NULL_CHAR*5 ,
   'b' : NULL_CHAR*2+chr(5)+NULL_CHAR*5 ,
   'c' : NULL_CHAR*2+chr(6)+NULL_CHAR*5 ,
   'd' : NULL_CHAR*2+chr(7)+NULL_CHAR*5 ,
   'e' : NULL_CHAR*2+chr(8)+NULL_CHAR*5 ,
   'f' : NULL_CHAR*2+chr(9)+NULL_CHAR*5 ,
   'g' : NULL_CHAR*2+chr(10)+NULL_CHAR*5 ,
   'h' : NULL_CHAR*2+chr(11)+NULL_CHAR*5 ,
   'i' : NULL_CHAR*2+chr(12)+NULL_CHAR*5 ,
   'j' : NULL_CHAR*2+chr(13)+NULL_CHAR*5 ,
   'k' : NULL_CHAR*2+chr(14)+NULL_CHAR*5 ,
   'l' : NULL_CHAR*2+chr(15)+NULL_CHAR*5 ,
   'm' : NULL_CHAR*2+chr(16)+NULL_CHAR*5 ,
   'n' : NULL_CHAR*2+chr(17)+NULL_CHAR*5 ,
   'o' : NULL_CHAR*2+chr(18)+NULL_CHAR*5 ,
   'p' : NULL_CHAR*2+chr(19)+NULL_CHAR*5 ,
   'q' : NULL_CHAR*2+chr(20)+NULL_CHAR*5 ,
   'r' : NULL_CHAR*2+chr(21)+NULL_CHAR*5 ,
   's' : NULL_CHAR*2+chr(22)+NULL_CHAR*5 ,
   't' : NULL_CHAR*2+chr(23)+NULL_CHAR*5 ,
   'u' : NULL_CHAR*2+chr(24)+NULL_CHAR*5 ,
   'v' : NULL_CHAR*2+chr(25)+NULL_CHAR*5 ,
   'w' : NULL_CHAR*2+chr(26)+NULL_CHAR*5 ,
   'x' : NULL_CHAR*2+chr(27)+NULL_CHAR*5 ,
   'y' : NULL_CHAR*2+chr(28)+NULL_CHAR*5 ,
   'z' : NULL_CHAR*2+chr(29)+NULL_CHAR*5 ,

   'A' : chr(2)+chr(32)+NULL_CHAR+chr(4)+NULL_CHAR*5 ,
   'B' : chr(2)+chr(32)+NULL_CHAR+chr(5)+NULL_CHAR*5 ,
   'C' : chr(2)+chr(32)+NULL_CHAR+chr(6)+NULL_CHAR*5 ,
   'D' : chr(2)+chr(32)+NULL_CHAR+chr(7)+NULL_CHAR*5 ,
   'E' : chr(2)+chr(32)+NULL_CHAR+chr(8)+NULL_CHAR*5 ,
   'F' : chr(2)+chr(32)+NULL_CHAR+chr(9)+NULL_CHAR*5 ,
   'G' : chr(2)+chr(32)+NULL_CHAR+chr(10)+NULL_CHAR*5 ,
   'H' : chr(2)+chr(32)+NULL_CHAR+chr(11)+NULL_CHAR*5 ,
   'I' : chr(2)+chr(32)+NULL_CHAR+chr(12)+NULL_CHAR*5 ,
   'J' : chr(2)+chr(32)+NULL_CHAR+chr(13)+NULL_CHAR*5 ,
   'K' : chr(2)+chr(32)+NULL_CHAR+chr(14)+NULL_CHAR*5 ,
   'L' : chr(2)+chr(32)+NULL_CHAR+chr(15)+NULL_CHAR*5 ,
   'M' : chr(2)+chr(32)+NULL_CHAR+chr(16)+NULL_CHAR*5 ,
   'N' : chr(2)+chr(32)+NULL_CHAR+chr(17)+NULL_CHAR*5 ,
   'O' : chr(2)+chr(32)+NULL_CHAR+chr(18)+NULL_CHAR*5 ,
   'P' : chr(2)+chr(32)+NULL_CHAR+chr(19)+NULL_CHAR*5 ,
   'Q' : chr(2)+chr(32)+NULL_CHAR+chr(21)+NULL_CHAR*5 ,
   'R' : chr(2)+chr(32)+NULL_CHAR+chr(21)+NULL_CHAR*5 ,
   'S' : chr(2)+chr(32)+NULL_CHAR+chr(22)+NULL_CHAR*5 ,
   'T' : chr(2)+chr(32)+NULL_CHAR+chr(23)+NULL_CHAR*5 ,
   'U' : chr(2)+chr(32)+NULL_CHAR+chr(24)+NULL_CHAR*5 ,
   'V' : chr(2)+chr(32)+NULL_CHAR+chr(25)+NULL_CHAR*5 ,
   'W' : chr(2)+chr(32)+NULL_CHAR+chr(26)+NULL_CHAR*5 ,
   'X' : chr(2)+chr(32)+NULL_CHAR+chr(27)+NULL_CHAR*5 ,
   'Y' : chr(2)+chr(32)+NULL_CHAR+chr(28)+NULL_CHAR*5 ,
   'Z' : chr(2)+chr(32)+NULL_CHAR+chr(29)+NULL_CHAR*5 ,


   '1' : NULL_CHAR*2+chr(30)+NULL_CHAR*5 ,
   '2' : NULL_CHAR*2+chr(31)+NULL_CHAR*5 ,
   '3' : NULL_CHAR*2+chr(32)+NULL_CHAR*5 ,
   '4' : NULL_CHAR*2+chr(33)+NULL_CHAR*5 ,
   '5' : NULL_CHAR*2+chr(34)+NULL_CHAR*5 ,
   '6' : NULL_CHAR*2+chr(35)+NULL_CHAR*5 ,
   '7' : NULL_CHAR*2+chr(36)+NULL_CHAR*5 ,
   '8' : NULL_CHAR*2+chr(37)+NULL_CHAR*5 ,
   '9' : NULL_CHAR*2+chr(38)+NULL_CHAR*5 ,
   '0' : NULL_CHAR*2+chr(39)+NULL_CHAR*5 ,

   '!' : chr(2)+chr(32)+NULL_CHAR+chr(30)+NULL_CHAR*5 ,
   '@' : chr(2)+chr(32)+NULL_CHAR+chr(31)+NULL_CHAR*5 ,
   '#' : chr(2)+chr(32)+NULL_CHAR+chr(32)+NULL_CHAR*5 ,
   '$' : chr(2)+chr(32)+NULL_CHAR+chr(33)+NULL_CHAR*5 ,
   '%' : chr(2)+chr(32)+NULL_CHAR+chr(34)+NULL_CHAR*5 ,
   '^' : chr(2)+chr(32)+NULL_CHAR+chr(35)+NULL_CHAR*5 ,
   '&' : chr(2)+chr(32)+NULL_CHAR+chr(36)+NULL_CHAR*5 ,
   '*' : chr(2)+chr(32)+NULL_CHAR+chr(37)+NULL_CHAR*5 ,
   '(' : chr(2)+chr(32)+NULL_CHAR+chr(38)+NULL_CHAR*5 ,
   ')' : chr(2)+chr(32)+NULL_CHAR+chr(39)+NULL_CHAR*5 ,


   ' ' : NULL_CHAR*2+chr(44)+NULL_CHAR*5 ,
   'SPACE' : NULL_CHAR*2+chr(44)+NULL_CHAR*5 ,
   'TAB' : NULL_CHAR*2+chr(43)+NULL_CHAR*5 ,
   'ENTER' : NULL_CHAR*2+chr(40)+NULL_CHAR*5 ,
   'ESC' : NULL_CHAR*2+chr(41)+NULL_CHAR*5 ,
   'BACK' : NULL_CHAR*2+chr(42)+NULL_CHAR*5 ,
   'F1' : NULL_CHAR*2+chr(58)+NULL_CHAR*5 ,
   'F2' : NULL_CHAR*2+chr(59)+NULL_CHAR*5 ,
   'F3' : NULL_CHAR*2+chr(60)+NULL_CHAR*5 ,
   'F4' : NULL_CHAR*2+chr(61)+NULL_CHAR*5 ,
   'F5' : NULL_CHAR*2+chr(62)+NULL_CHAR*5 ,
   'F6' : NULL_CHAR*2+chr(63)+NULL_CHAR*5 ,
   'F7' : NULL_CHAR*2+chr(64)+NULL_CHAR*5 ,
   'F8' : NULL_CHAR*2+chr(65)+NULL_CHAR*5 ,
   'F9' : NULL_CHAR*2+chr(66)+NULL_CHAR*5 ,
   'F10' : NULL_CHAR*2+chr(67)+NULL_CHAR*5 ,
   'F11' : NULL_CHAR*2+chr(68)+NULL_CHAR*5 ,
   'F12' : NULL_CHAR*2+chr(69)+NULL_CHAR*5 ,


   '-' : NULL_CHAR*2+chr(45)+NULL_CHAR*5 ,
   '=' : NULL_CHAR*2+chr(46)+NULL_CHAR*5 ,
   '[' : NULL_CHAR*2+chr(47)+NULL_CHAR*5 ,
   ']' : NULL_CHAR*2+chr(48)+NULL_CHAR*5 ,
   '\\' : NULL_CHAR*2+chr(49)+NULL_CHAR*5 ,
   '£' : NULL_CHAR*2+chr(50)+NULL_CHAR*5 ,
   ';' : NULL_CHAR*2+chr(51)+NULL_CHAR*5 ,
   '\'' : NULL_CHAR*2+chr(52)+NULL_CHAR*5 ,
   ',' : NULL_CHAR*2+chr(54)+NULL_CHAR*5 ,
   '.' : NULL_CHAR*2+chr(55)+NULL_CHAR*5 ,
   '\/`' : NULL_CHAR*2+chr(56)+NULL_CHAR*5 ,

   '_' : chr(2)+chr(32)+NULL_CHAR+chr(45)+NULL_CHAR*5 ,
   '+' : chr(2)+chr(32)+NULL_CHAR+chr(46)+NULL_CHAR*5 ,
   '{' : chr(2)+chr(32)+NULL_CHAR+chr(47)+NULL_CHAR*5 ,
   '}' : chr(2)+chr(32)+NULL_CHAR+chr(48)+NULL_CHAR*5 ,
   '|' : chr(2)+chr(32)+NULL_CHAR+chr(49)+NULL_CHAR*5 ,
   '~' : chr(2)+chr(32)+NULL_CHAR+chr(50)+NULL_CHAR*5 ,
   ':' : chr(2)+chr(32)+NULL_CHAR+chr(51)+NULL_CHAR*5 ,
   '#' : chr(2)+chr(32)+NULL_CHAR+chr(52)+NULL_CHAR*5 ,
   '¬' : chr(2)+chr(32)+NULL_CHAR+chr(53)+NULL_CHAR*5 ,
   '<' : chr(2)+chr(32)+NULL_CHAR+chr(54)+NULL_CHAR*5 ,
   '>' : chr(2)+chr(32)+NULL_CHAR+chr(55)+NULL_CHAR*5 ,
   '?' : chr(2)+chr(32)+NULL_CHAR+chr(56)+NULL_CHAR*5 ,



}






def write_report(report):
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report.encode())

def sendUSBHID( seq ) :
    
    for c in seq.split(' '):
        # recalc ascii to key 
   #     key = ord(c) - ord('a') + 4
        print( c )
        try: 
        # Press a
            print( HIDMAP[c] )
            write_report(HIDMAP[c])
            #write_report(chr(2) + NULL_CHAR*2+chr(key)+NULL_CHAR*5)

        # Release keys
            write_report(chr(2)+ NULL_CHAR*8)
            time.sleep(0.01)
        except:
            pass

class pinToChar():
# Written by Chris Crumpacker
# May 2013
#
# main structure is adapted from Bandono's
# matrixQPI which is wiringPi based.
# https://github.com/bandono/matrixQPi?source=cc
    # CONSTANTS   
    KEYPAD = [
    [1,2,3],
    [4,5,6],
    [7,8,9],
    ["*",0,"#"]
    ]
    
    ROW         = [16,26,20,21]
    COLUMN      = [22,27,17]
    
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
    
    def getKey(self):
        
        # Set all columns as output low
        for j in range(len(self.COLUMN)):
            GPIO.setup(self.COLUMN[j], GPIO.OUT)
            GPIO.output(self.COLUMN[j], GPIO.LOW)
        
        # Set all rows as input
        for i in range(len(self.ROW)):
            GPIO.setup(self.ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        # Scan rows for pushed key/button
        # A valid key press should set "rowVal"  between 0 and 3.
        rowVal = -1
        for i in range(len(self.ROW)):
            tmpRead = GPIO.input(self.ROW[i])
            if tmpRead == 0:
                rowVal = i
                
        # if rowVal is not 0 thru 3 then no button was pressed and we can exit
        if rowVal <0 or rowVal >3:
            self.exit()
            return
        
        # Convert columns to input
        for j in range(len(self.COLUMN)):
                GPIO.setup(self.COLUMN[j], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        
        # Switch the i-th row found from scan to output
        GPIO.setup(self.ROW[rowVal], GPIO.OUT)
        GPIO.output(self.ROW[rowVal], GPIO.HIGH)

        # Scan columns for still-pushed key/button
        # A valid key press should set "colVal"  between 0 and 2.
        colVal = -1
        for j in range(len(self.COLUMN)):
            tmpRead = GPIO.input(self.COLUMN[j])
            if tmpRead == 1:
                colVal=j
                
        # if colVal is not 0 thru 2 then no button was pressed and we can exit
        if colVal <0 or colVal >2:
            self.exit()
            return

        # Return the value of the key pressed
        self.exit()
        return self.KEYPAD[rowVal][colVal]
        
    def exit(self):
        # Reinitialize all rows and columns as input at exit
        for i in range(len(self.ROW)):
                GPIO.setup(self.ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP) 
        for j in range(len(self.COLUMN)):
                GPIO.setup(self.COLUMN[j], GPIO.IN, pull_up_down=GPIO.PUD_UP)


if __name__ == '__main__':

    # Initialize the keypad class
    kp = pinToChar()

    # scan and wait for a key press

    layer = 1

    cyclelayer=shortcuts['shortcuts']['layercycle']
    print( "Layer cycle %s", ( cyclelayer ) )
    curlayertitle=""
    labels1=""
    labels2=""
    maxwidth=0
    unused = 0
    startpos=width
    pos = startpos
    sending=""
    while True:
        # Draw a black filled box to clear the image.
        draw.rectangle((0,0,width,height), outline=0, fill=0)

        # Display image
        draw.rectangle((0,0,width,9), outline=255, fill=255)
        draw.text((1, 0),       curlayertitle ,  font=font, fill=0)

        draw.rectangle((60,0,width,9), outline=0, fill=0)
        now = datetime.strftime(datetime.now(),"%d/%m %H:%M")
        draw.text((61, 0),       now,  font=font, fill=255)
#        draw.text((0, 8),       labels1,  font=font, fill=255)
        draw.text((0, 16),       sending,  font=font, fill=255)
        maxwidth, unused = draw.textsize(labels1, font=font)
        x = pos
        for i, cc in enumerate(labels1):
             if x > width:
                 break;
             if x < -10:
                char_width, char_height = draw.textsize(cc, font=font)
                x += char_width
                continue
        # Draw text.
             draw.text((x, 8), cc, font=font, fill=255)
        # Increment x position based on chacacter width.
             char_width, char_height = draw.textsize(cc, font=font)
             x += char_width
        #     print(x)
        #     print(cc)

        draw.text((30, 24),       "line4" ,  font=font, fill=255)
        disp.image(image)
        disp.display()
        pos += -4
        # Start over if text has scrolled completely off left side of screen.
        if pos < -maxwidth:
                pos = startpos
#        time.sleep(.1)


        #c = None
        #while c == None:
        c = kp.getKey()

        print(c)
#        print(labels1)
#        print(pos)
        if c == ' ':
            break

        # TODO probe all of the pins and convert to char

        # scan through key presses and find details

        foundlayer = False
        for layermap in shortcuts['shortcuts']['layers'] :
           if layermap['layer'] == layer :
               #print( layermap )
               foundlayer = True
               curlayertitle=layermap['title']
               #print( layermap['title' ] )
               labels1=""
               for b in layermap['buttons'] :
                   #print( "%s - %s" %  ( b['key'], b['label'] ) )
                   labels1 = labels1 + " " +b['key'] + " - "+b['label']



               for b in layermap['buttons'] :
                   print(";;;;")
                   print(b['key'])
                   print(c)
                   if str(b['key']) == str(c) :
                      # send string to keyboard
                      print( b['string'])
                      sending = b['string']
                      sendUSBHID( sending ) 
                      #charToPins( c )


        if not foundlayer :
            layer = 1
            print( "Cycle round to the start of the layers" )

        if c == cyclelayer :
            layer += 1
            print( "Next layer %s", ( layer ) )







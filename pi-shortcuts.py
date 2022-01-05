#!/usr/bin/python

# not pretty but trying to get a basic working prototype

import os
import yaml
from pathlib import Path
import sys
import time
import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from datetime import datetime

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


# Extra GPIO contols
#gnd=30 and 34

# wires round wrong way - swapped
#JACK6MM = 18 and 20. gpio 24
#POTSW = 25 and 26 gpio 7   


#POTL = 29 gpio 5
#POTR = 31 gpio 6
#POTMID = gnd 34

JACK6MM = 7
DIALSW = 24
DIALL = 5
DIALR = 6

counter = 10

Enc_A = 5
Enc_B = 6

#POTMID = gnd 34

GPIO.setmode(GPIO.BCM)
GPIO.setup(JACK6MM, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(DIALSW, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(DIALL, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(DIALR, GPIO.IN, pull_up_down=GPIO.PUD_UP)


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
#font = ImageFont.truetype("/home/pi/Ubuntu-C.ttf",10)
font = ImageFont.load_default()
font2 = ImageFont.truetype("/home/pi/Ubuntu-B.ttf",20)
font3 = ImageFont.truetype("/home/pi/Ubuntu-B.ttf",18)


# Read shortcuts YAML file

with open("/home/pi/pi-shortcuts.yaml", 'r') as stream:
    shortcuts = yaml.safe_load(stream)


PANEL_HINTS = 0
PANEL_CLOCK = 1
PANEL_DEFAULTS = 2
PANEL_MENU = 3
PANEL_LAYER = False

NULL_CHAR = chr(0)

HIDMAP = {

   'a' : chr(4) ,
   'b' : chr(5) ,
   'c' : chr(6) ,
   'd' : chr(7) ,
   'e' : chr(8) ,
   'f' : chr(9) ,
   'g' : chr(10) ,
   'h' : chr(11) ,
   'i' : chr(12) ,
   'j' : chr(13) ,
   'k' : chr(14) ,
   'l' : chr(15) ,
   'm' : chr(16) ,
   'n' : chr(17) ,
   'o' : chr(18) ,
   'p' : chr(19) ,
   'q' : chr(20) ,
   'r' : chr(21) ,
   's' : chr(22),
   't' : chr(23) ,
   'u' : chr(24),
   'v' : chr(25) ,
   'w' : chr(26) ,
   'x' : chr(27) ,
   'y' : chr(28) ,
   'z' : chr(29),

   '1' : chr(30) ,
   '2' : chr(31) ,
   '3' : chr(32) ,
   '4' : chr(33) ,
   '5' : chr(34) ,
   '6' : chr(35),
   '7' : chr(36) ,
   '8' : chr(37) ,
   '9' : chr(38) ,
   '0' : chr(39) ,


   ' ' : chr(44) ,
   'SPACE' : chr(44) ,
   'TAB' : chr(43) ,
   'ENTER' : chr(40) ,
   'ESC' : chr(41) ,
   'BACK' : chr(42),
   'F1' : chr(58) ,
   'F2' : chr(59) ,
   'F3' : chr(60),
   'F4' : chr(61) ,
   'F5' : chr(62) ,
   'F6' : chr(63) ,
   'F7' : chr(64) ,
   'F8' : chr(65) ,
   'F9' : chr(66) ,
   'F10' : chr(67) ,
   'F11' : chr(68) ,
   'F12' : chr(69) ,


   '-' : chr(45) ,
   '=' : chr(46),
   '[' : chr(47) ,
   ']' : chr(48) ,
   '\\' : chr(49) ,
   '#' : chr(50) ,
   ';' : chr(51) ,
   '\'' : chr(52),
   ',' : chr(54) ,
   '.' : chr(55) ,
   '/' : chr(56),


}



HIDMAPwas = {

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
   '"' : chr(2)+chr(32)+NULL_CHAR+chr(31)+NULL_CHAR*5 ,
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
   '#' : NULL_CHAR*2+chr(50)+NULL_CHAR*5 ,
   ';' : NULL_CHAR*2+chr(51)+NULL_CHAR*5 ,
   '\'' : NULL_CHAR*2+chr(52)+NULL_CHAR*5 ,
   ',' : NULL_CHAR*2+chr(54)+NULL_CHAR*5 ,
   '.' : NULL_CHAR*2+chr(55)+NULL_CHAR*5 ,
   '/' : NULL_CHAR*2+chr(56)+NULL_CHAR*5 ,

   '_' : chr(2)+chr(32)+NULL_CHAR+chr(45)+NULL_CHAR*5 ,
   '+' : chr(2)+chr(32)+NULL_CHAR+chr(46)+NULL_CHAR*5 ,
   '{' : chr(2)+chr(32)+NULL_CHAR+chr(47)+NULL_CHAR*5 ,
   '}' : chr(2)+chr(32)+NULL_CHAR+chr(48)+NULL_CHAR*5 ,
   '|' : chr(2)+chr(32)+NULL_CHAR+chr(49)+NULL_CHAR*5 ,
   '~' : chr(2)+chr(32)+NULL_CHAR+chr(50)+NULL_CHAR*5 ,
   ':' : chr(2)+chr(32)+NULL_CHAR+chr(51)+NULL_CHAR*5 ,
   '@' : chr(2)+chr(32)+NULL_CHAR+chr(52)+NULL_CHAR*5 ,
   '¬' : chr(2)+chr(32)+NULL_CHAR+chr(53)+NULL_CHAR*5 ,
   '<' : chr(2)+chr(32)+NULL_CHAR+chr(54)+NULL_CHAR*5 ,
   '>' : chr(2)+chr(32)+NULL_CHAR+chr(55)+NULL_CHAR*5 ,
   '?' : chr(2)+chr(32)+NULL_CHAR+chr(56)+NULL_CHAR*5 ,



}



def write_report(report):
    # send HID encoding through to connected USB device
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report.encode())

def sendUSBHID( seq ) :
    # Take a macro string and convert to HID sequences

    for c in seq.split(' '):
        print( c )

        if c == "PAUSE" :
            time.sleep( 1 )
        if c == "PAUSE10" :
            time.sleep( 10 )
        elif c != "" :
            try: 

                # break up the current sequence to get any modifiers as well as actual key

                thiskey = c.split('-')


                modflag=0x00

                for mods in thiskey:
                    print( mods)
                    if mods == "LCTRL" or mods == "CTRL":
                       modflag = modflag | 0x01
                    if mods == "RCTRL":
                       modflag = modflag | 0x10
                    if mods == "LS" or mods == "SHIFT" :
                       modflag = modflag | 0x02
                    if mods == "RS" :
                       modflag = modflag | 0x20
                    if mods == "LALT"  or mods == "ALT" :
                       modflag = modflag | 0x04
                    if mods == "RALT"  :
                       modflag = modflag | 0x40
                    if mods == "LMETA"  or mods == "META" :
                       modflag = modflag | 0x08
                    if mods == "RMETA"  :
                       modflag = modflag | 0x80

                print( modflag)

                # need to reemember '-' is a normal key too! So in this case last item will be empty

                actkey=thiskey[-1]
                print("actkey")
                print(actkey)
                if actkey == "":
                    actkey='-'

                # see if this is a single upper case letter and if so add a map for the lowercase + shift
                # to make the config file easier to read

                if actkey.isupper() and len(actkey) == 1 :
                    modflag = modflag | 0x02
                    actkey = actkey.lower()

                # get HID ASCII map
                sending = chr(modflag)+chr(modflag)+NULL_CHAR+HIDMAP[actkey]+NULL_CHAR*5

                print("hidmap")
                #print( HIDMAP[c] )
    #            print("last hidmap")
    #            print( HIDMAP[c[-1:]] )

                write_report(sending)

                # Release keys
                write_report(chr(2)+ NULL_CHAR*8)
                time.sleep(0.01)
            except Exception as e:
                print( "Error %s " % str(e))
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
        
        #print( "JACK %d " % GPIO.input(JACK6MM) )
        #print( "DIALSW %d " % GPIO.input(DIALSW) )
        if not GPIO.input(JACK6MM) :
            return "JACK1"

        if not GPIO.input(DIALSW) :
            return "DIALSW"
#
#        if GPIO.input(DIALL) :
#            return "DIALL"
#
#        if GPIO.input(DIALR) :
#            return "DIALR"

#        print( "diall")
#        print( GPIO.input(DIALL))
#        print( "dialr")
#        print( GPIO.input(DIALR))

#        DL=GPIO.input(DIALL)
#        DR=GPIO.input(DIALR)
#
#        if DL == 0 and DR == 1 : 
#            print ( "Dial1" )
#        if DL == 1 and DR == 0 : 
#            print ( "Dial2" )

#        print( "dialsw")
#        print( GPIO.input(DIALSW))
#        print( "jac")
#        print( GPIO.input(JACK6MM))

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


def lineScroll( canvas, y, string, startpos, speed, spacing = 0 ) :
   maxwidth=0
   unused = 0
#   startpos=width
   pos = startpos

   maxwidth, unused = canvas.textsize(string, font=font)
   #print("text width")
   #print(maxwidth)
   x = pos
   for i, cc in enumerate(string):
         if x > width:
             break;
         if x < -10:
            char_width, char_height = canvas.textsize(cc, font=font)
            x += char_width + spacing
            continue
    # Draw text.
         canvas.text((x, y), cc, font=font, fill=255)
    # Increment x position based on chacacter width.
         char_width, char_height = canvas.textsize(cc, font=font)
         x += char_width + spacing
         #print(x)
         #print(cc)

   pos += speed
   # Start over if text has scrolled completely off left side of screen.
   if pos < -maxwidth:
           pos = width
   return pos

def layerchange() :
            global layer
            global clockon
            clockon = False
            print( "Next layer %s", ( layer ) )
            foundlayer = False
            while not foundlayer:
                for layermap in shortcuts['shortcuts']['layers'] :
                       if layermap['layer'] == layer :
                           #print( layermap )
                           foundlayer = True
                           curlayertitle=layermap['title']
                if not foundlayer :
                    layer = 1

def rotation_decode(Enc_A):
    global counter
    global layer
    global panelView
    global PANEL_LAYER

    PANEL_LAYER = True
    time.sleep(0.0025)
    Switch_A = GPIO.input(Enc_A)
    Switch_B = GPIO.input(Enc_B)

    if (Switch_A == 1) and (Switch_B == 0):
        layer += 1
        print( "direction -> " + str( layer))
        while Switch_B == 0:
            time.sleep(0.025)
            Switch_B = GPIO.input(Enc_B)
        while Switch_B == 1:
            time.sleep(0.025)
            Switch_B = GPIO.input(Enc_B)
            
    #    return

    elif (Switch_A == 1) and (Switch_B == 1):
        layer -= 1
        print(  "direction <- " + str( layer ))
        while Switch_A == 1:
            time.sleep(0.025)
            Switch_A = GPIO.input(Enc_A)
    else:
        pass

    layerchange()


if __name__ == '__main__':

    GPIO.add_event_detect(Enc_A, GPIO.RISING, callback=rotation_decode, bouncetime=10)
    # Initialize the keypad class
    kp = pinToChar()

    # scan and wait for a key press

    layer = 1

    cyclelayer = shortcuts['shortcuts']['defaults']['layercycle']
    paneltoggle = shortcuts['shortcuts']['defaults']['paneltoggle']
    print( "Layer cycle %s", ( cyclelayer ) )
    curlayertitle=""
    labels1=""
    labels2=""
    #clockon = False
#    maxwidth=0
#    unused = 0
#    startpos=width
#    pos = startpos
    pos2 = width
    pos3 = width
    pos4 = width
    sending=""
    motd_last=""
    motd=""
    alarmtime="0000"
    alarmactive = False

    

    panelView = PANEL_HINTS
    while True:

        # Draw a black filled box to clear the image.
        draw.rectangle((0,0,width,height), outline=0, fill=0)

        now = datetime.strftime(datetime.now(),"%d/%m %H:%M")

        if alarmactive :
            alarmnow = datetime.strftime(datetime.now(),"%H%M")
            if alarmnow == alarmtime :
                alarmback = 255
                alarmfont  = 0
                alarmcounter = 0
                alarmactive = False
                while  True:
                    c = kp.getKey()
                    if c != None: 
                             break
                    draw.rectangle((0,0,width,height), outline=alarmback, fill=alarmback)
                    draw.text((10, 8),       "Alarm!" ,  font=font2, fill=alarmfont)
                    disp.image(image)
                    disp.display()
                    alarmcounter = alarmcounter + 1
                    time.sleep(0.01)
                    print(alarmcounter)
                    if alarmcounter > 10 :
                        print("Invert")
                        alarmcounter = 0
                        if alarmfont == 0:
                            alarmback = 0
                            alarmfont = 255
                        else:
                            alarmback = 255
                            alarmfont = 0


        if PANEL_LAYER:
            PANEL_LAYER = False

            # Draw a black filled box to clear the image.
            draw.rectangle((0,0,width,height), outline=0, fill=0)
            draw.text((1, 8),       curlayertitle ,  font=font2, fill=255)

            disp.image(image)
            disp.display()
            time.sleep(0.025)
        else:       

            if panelView == PANEL_CLOCK :
                draw.text((15, -2),       curlayertitle ,  font=font, fill=255)
                # Put in the current date and time 
                nowwidth, unused = draw.textsize(now, font=font3)
                draw.text(((width/2)-(nowwidth/2), 6),       now,  font=font3, fill=255)
                if alarmactive:
                    draw.text((72, -2),   "*",  font=font, fill=255)
                draw.text((81, -2),       alarmtime[0:2]+":"+alarmtime[2:4],  font=font, fill=255)

            if panelView == PANEL_HINTS:

                # Display current layer title inverted
                draw.rectangle((0,0,width,7), outline=255, fill=255)
                draw.text((1, -2),       curlayertitle ,  font=font, fill=0)

                if alarmactive:
                    draw.text((52, -1),   "*",  font=font, fill=0)

                # Put in the current date and time 
                draw.rectangle((60,-2,width,7), outline=0, fill=0)
                draw.text((61, -1),       now,  font=font, fill=255)
                pos2 = lineScroll( draw, 6, labels1, pos2, -5 )
                pos3 = lineScroll( draw, 14, sending, pos3, -8 )
    #        draw.text((0, 8),       labels1,  font=font, fill=255)
            # Display the last macro sent (just to use the row for now)
    #        draw.text((0, 16),       sending,  font=font, fill=255)


    #        # Scroll the macro options for this layer
    #        maxwidth, unused = draw.textsize(labels1, font=font)
    #        x = pos
    #        for i, cc in enumerate(labels1):
    #             if x > width:
    #                 break;
    #             if x < -10:
    #                char_width, char_height = draw.textsize(cc, font=font)
    #                x += char_width
    #                continue
    #        # Draw text.
    #             draw.text((x, 8), cc, font=font, fill=255)
    #        # Increment x position based on chacacter width.
    #             char_width, char_height = draw.textsize(cc, font=font)
    #             x += char_width
            #     print(x)
            #     print(cc)


            # refresh MOTD text


            try:
                motdfile = os.stat ( "/dev/shm/pi-shortcuts.motd" )

    #            motmod = motdfile [ stat.ST_MTIME ] 
     
                if motd_last != motdfile :
    #            if True:
                    motd_last = motdfile
                    pos4=width
                    print("Reloading motd")
                    sending="MOTD Refreshed " + now
                    # file has been modified so reload
                    #ith open('/dev/shm/pi-shortcuts.motd') as f:
                    #   motd = f.readlines()
                    motd = Path('/dev/shm/pi-shortcuts.motd').read_text()
                    motd = motd.replace('\n', '')
    #                     motd = file.read().replace('\n', '')

            except Exception as e:
                motd = "MOTD: " +  str(e)
                print(str(e))

            pos4 = lineScroll( draw, 22, motd, pos4, -6, 4 )
            # Display a simple fixed string on the bottom row for now
            #draw.text((30, 24),       "line4" ,  font=font, fill=255)

            # Render OLED
            disp.image(image)
            disp.display()
    #        pos += -5
            # Start over if text has scrolled completely off left side of screen.
    #        if pos < -maxwidth:
    #                pos = startpos
    #        time.sleep(.1)


            #c = None
            #while c == None:
            c = kp.getKey()

            #print(c)
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
                       #print(";;;;")
                       #print(b['key'])
                       #print(c)
                       if str(b['key']) == str(c) :
                          print( b['string'])
                          sending = b['string']

                          if sending == "AlarmSet" :
                              alarmset = False
                              while not alarmset :
                                    # Draw a black filled box to clear the image.
                                    draw.rectangle((0,0,width,height), outline=0, fill=0)
                                    draw.text((0, 0),  "Set alarm. # Exit",  font=font, fill=255)
                                    draw.text((0, 8),       alarmtime[0:2]+":"+alarmtime[2:4],  font=font3, fill=255)

                                    disp.image(image)
                                    disp.display()
                                    c2 = kp.getKey()
                                    if c2 == cyclelayer :
                                        alarmset = True
                                        alarmactive = True
                                    elif c2 != None:
                                       alarmtime = alarmtime[1:4] + str(c2)
                                       time.sleep(0.25)
                                       
                                    print( alarmtime )

                                     
                              c = None
                              time.sleep(0.5)
                          elif sending == "AlarmOn" :
                               alarmactive = True
                               # Draw a black filled box to clear the image.
                               draw.rectangle((0,0,width,height), outline=0, fill=0)
                               draw.text((0, 8),      "Alarm On",  font=font3, fill=255)

                               disp.image(image)
                               disp.display()
                               time.sleep(0.5)
                               c = None
                          elif sending == "AlarmOff" :
                               alarmactive = False
                               # Draw a black filled box to clear the image.
                               draw.rectangle((0,0,width,height), outline=0, fill=0)
                               draw.text((0, 8),      "Alarm Off",  font=font3, fill=255)

                               disp.image(image)
                               disp.display()
                               time.sleep(0.5)
                               c = None
                          else:
                              # send string to keyboard
                              sendUSBHID( sending ) 
                              panelView = PANEL_HINTS
                              #charToPins( c )


        if not foundlayer :
            layer = 1
            print( "Cycle round to the start of the layers" )

        if c == paneltoggle :
            panelView = panelView + 1
            if panelView > PANEL_MENU:
                panelView = PANEL_HINTS
            print( "CHange panel %d" % panelView)

            #clockon = not clockon

        if c == cyclelayer :
            layer += 1
            layerchange()

#        if c == "DIALL" or c == "DIALR" :
#            time.sleep(0.025)
#            Switch_A = GPIO.input(Enc_A)
#            Switch_B = GPIO.input(Enc_B)
#
#            if (Switch_A == 1) and (Switch_B == 0):
#                layer += 1
#                print( "direction -> " + str( layer))
#                while Switch_B == 0:
#                    Switch_B = GPIO.input(Enc_B)
#                    time.sleep(0.05)
#                while Switch_B == 1:
#                    Switch_B = GPIO.input(Enc_B)
#                    time.sleep(0.05)
#            #    return
#
#            elif (Switch_A == 1) and (Switch_B == 1):
#                layer -= 1
#                print(  "direction <- " + str( layer ))
#                while Switch_A == 1:
#                    Switch_A = GPIO.input(Enc_A)
#                    time.sleep(0.05)
#            else:
#                pass
#
#            layerchange()





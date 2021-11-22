#!/usr/bin/python

import yaml
import sys

# Read pin wiring YAML file

with open("pi-shortcuts-pins.yaml", 'r') as stream:
    pinmap = yaml.safe_load(stream)


print( pinmap )


# Read shortcuts YAML file

with open("pi-shortcuts.yaml", 'r') as stream:
    shortcuts = yaml.safe_load(stream)


print( shortcuts )


def charToPins( c ) :
   col=0
   row=0
   for k in pinmap['keymap']:
      if k['key'] == c:
         col = k['col']
         row = k['row']
         print( k )
   #for g in pinmap['gpio'] :
   #   print( g )
   #   if g['row'] == row and g['col'] == col :
   #      print( 
   return   



# scan and wait for a key press

layer = 1

cyclelayer=shortcuts['shortcuts']['layercycle']
print( "Layer cycle %s", ( cyclelayer ) )

str = ""
while True:
    c = sys.stdin.read(1) # reads one byte at a time, similar to getchar()
    if c == ' ':
        break
    #str += c
    print(c)

    # TODO probe all of the pins and convert to char

    # scan through key presses and find details

    foundlayer = False
    for layermap in shortcuts['shortcuts']['layers'] :
       if layermap['layer'] == layer :
           print( layermap )
           foundlayer = True

           print( layermap['title' ] )
           for b in layermap['buttons'] :
               print( "%s - %s" %  ( b['key'], b['label'] ) )

           for b in layermap['buttons'] :
               if b['key'] == c :
                  # send string to keyboard
                  print( b['string'])
                  charToPins( c )


    if not foundlayer :
        layer = 1
        print( "Cycle round to the start of the layers" )

    if c == cyclelayer :
        layer += 1
        print( "Next layer %s", ( layer ) )







#!/usr/bin/env python
#  file: testArduinoBoard.py
# autor: frep
#  desc: testfile for the arduinoBoard class used for the radxa rock arduino shield Rev. A, see
#        http://talk.radxa.com/topic/839/radxa-rock-arduino-board-rev-a

import os
import sys

from time import sleep
from pyRock.arduinoBoard import ArduinoBoard
from pydispatch import dispatcher


# initialize board
board = ArduinoBoard()


# define handler functions for button events here
def handle_Button1_Changed( sender ):
    # instructions for Event Button1 changed
    print "Button 1 has changed"

def handle_Button2_Changed( sender ):
    # instructions for Event Button2 changed
    print "Button 2 has changed"

def handle_Button1_Pressed( sender ):
    # instructions for Event Button1 pressed
    print "Button 1 is pressed"

def handle_Button2_Pressed( sender ):
    # instructions for Event Button2 pressed
    print "Button 2 is pressed"

def handle_Button1_Released( sender ):
    # instructions for Event Button1 released
    print "Button 1 is released"

def handle_Button2_Released( sender ):
    # instructions for Event Button2 released
    print "Button 2 is released" 


# connect the handler function you want to use
#dispatcher.connect( handle_Button1_Changed, signal=board.SIGNAL_BUTTON_CHANGED, sender=board.button1.id )
#dispatcher.connect( handle_Button2_Changed, signal=board.SIGNAL_BUTTON_CHANGED, sender=board.button2.id )
dispatcher.connect( handle_Button1_Pressed, signal=board.SIGNAL_BUTTON_PRESSED, sender=board.button1.id )
dispatcher.connect( handle_Button2_Pressed, signal=board.SIGNAL_BUTTON_PRESSED, sender=board.button2.id )
dispatcher.connect( handle_Button1_Released, signal=board.SIGNAL_BUTTON_RELEASED, sender=board.button1.id )
dispatcher.connect( handle_Button2_Released, signal=board.SIGNAL_BUTTON_RELEASED, sender=board.button2.id )


try:
    # set all leds off
    for i in range(len(board.led)):
	board.led[i].setOff()

    number = 42	
    board.printNumberWithLeds(number)
    print "leds show number %d" % number
    print ("Press CTRL+C to exit")
    board.display.begin(16, 2)

    while True:
	for i in range(len(board.button)):
	    board.button[i].check()
	# 20ms for debounce
    	sleep(0.02)

except KeyboardInterrupt:
    print ("Goodbye.")

#!/usr/bin/env python
#  file: testArduinoBoard.py
# autor: frep
#  desc: testfile for the arduinoBoard class used for the radxa rock arduino shield Rev. A, see
#        http://talk.radxa.com/topic/839/radxa-rock-arduino-board-rev-a

import os
import sys

from time import sleep
from pyRock.arduinoBoard import ArduinoBoard

# initialize board
board = ArduinoBoard()

# initialize gpio expander
#mcp = MCP.MCP23017(0x20)

try:
    # set all leds off
    for i in range(len(board.led)):
	board.led[i].setOff()

    number = 42	
    board.printNumberWithLeds(number)
    print "leds show number %d" % number
    print ("Press CTRL+C to exit")

    while True:
	#for i in range(len(board.led)):
	#    board.led[i].toggle()
	for i in range(len(board.button)):
	    board.button[i].check()
	#board.button[0].check()
	#board.button[1].check()
	# 20ms for debounce
    	sleep(0.02)

except KeyboardInterrupt:
    print ("Goodbye.")

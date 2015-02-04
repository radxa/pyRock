#!/usr/bin/env python
#  file: testArduinoBoard.py
# autor: frep
#  desc: testfile for the arduinoBoard class used for the radxa rock arduino shield Rev. A, see
#        http://talk.radxa.com/topic/839/radxa-rock-arduino-board-rev-a

import os
import sys
import socket
import fcntl
import struct
import array
import getopt

from time import sleep
from pyRock.arduinoBoard import ArduinoBoard
from pydispatch import dispatcher

# initialize board
board = ArduinoBoard()

# global control variables
number = 42
debug = 0
runForever = 1

# define handler functions for button events here
def handle_Button1_Changed( sender ):
    # instructions for Event Button1 changed
    if debug:
	print "Button 1 has changed"

def handle_Button2_Changed( sender ):
    # instructions for Event Button2 changed
    if debug:
	print "Button 2 has changed"

def handle_Button1_Pressed( sender ):
    # instructions for Event Button1 pressed
    if debug:
	print "Button 1 is pressed"
    decreaseNumber()

def handle_Button2_Pressed( sender ):
    # instructions for Event Button2 pressed
    if debug:
	print "Button 2 is pressed"
    increaseNumber()

def handle_Button1_Released( sender ):
    # instructions for Event Button1 released
    if debug:
	print "Button 1 is released"

def handle_Button2_Released( sender ):
    # instructions for Event Button2 released
    if debug:
	print "Button 2 is released" 


# connect the handler function you want to use
#dispatcher.connect( handle_Button1_Changed, signal=board.SIGNAL_BUTTON_CHANGED, sender=board.button1.id )
#dispatcher.connect( handle_Button2_Changed, signal=board.SIGNAL_BUTTON_CHANGED, sender=board.button2.id )
dispatcher.connect( handle_Button1_Pressed, signal=board.SIGNAL_BUTTON_PRESSED, sender=board.button1.id )
dispatcher.connect( handle_Button2_Pressed, signal=board.SIGNAL_BUTTON_PRESSED, sender=board.button2.id )
dispatcher.connect( handle_Button1_Released, signal=board.SIGNAL_BUTTON_RELEASED, sender=board.button1.id )
dispatcher.connect( handle_Button2_Released, signal=board.SIGNAL_BUTTON_RELEASED, sender=board.button2.id )


def main(argv):
    # I want to use the global variables in my main function
    global number
    global debug
    global runForever
    try:
	opts, args = getopt.getopt(argv, "hn:rd", ["help", "number=", "runOnlyOnce", "debug"])
    except getopt.GetoptError:
	usage()
	sys.exit(2)    
    for opt, arg in opts:
	if opt in ("-h","--help"):
	    usage()
	    sys.exit()
	elif opt in ("-n","--number"):
	    try:
	    	number = int(arg)
		break
	    except ValueError:
		print "number has to be an integer between 0 and 255. Input is ignored"
	elif opt in ("-r","--runOnlyOnce"):
	    runForever = 0
	elif opt in ("-d","--debug"):
	    debug = 1
    try:
    	# set all leds off
    	for i in range(len(board.led)):
	    board.led[i].setOff()
    	board.printNumberWithLeds(number)
	if debug:
	    print "leds show number %d" % number
	if runForever:
	    print ("Press CTRL+C to exit")
	board.display.begin(16, 2)
    	board.display.message("frep's ROCK PRO\n")
    	board.display.message(getCorrectIP())
    	while runForever:
	    for i in range(len(board.button)):
	    	board.button[i].check()
		# 20ms for debounce
    		sleep(0.02)
	if debug:
            print ("Goodbye.")
	sys.exit()
    except KeyboardInterrupt:
	if debug:
    	    print ("Goodbye.")
    	sys.exit()

def usage():
    print "Usage:" 
    print "\ttestArduinoBoard.py [options]"
    print "options:"
    print "\t-h, --help \t\tshows this help"
    print "\t-n, --number <number> \tdefines the inital number shown by the leds (0..255)"
    print "\t-r, --runOnlyOnce \texit the program after without looping forever"
    print "\t-d, --debug \t\tget some debug informations"

# functions to get a usefull example
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

def all_interfaces():
    max_possible = 128  # arbitrary. raise if needed.
    bytes = max_possible * 32
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    names = array.array('B', '\0' * bytes)
    outbytes = struct.unpack('iL', fcntl.ioctl(
        s.fileno(),
        0x8912,  # SIOCGIFCONF
        struct.pack('iL', bytes, names.buffer_info()[0])
    ))[0]
    namestr = names.tostring()
    return [namestr[i:i+32].split('\0', 1)[0] for i in range(0, outbytes, 32)]

def getCorrectIP():
    # if wired interface is up, take it!
    if 'eth0' in all_interfaces():
        return get_ip_address('eth0')
    # if at least wireless interface is up, take it!
    if 'wlan0' in all_interfaces():
        return get_ip_address('wlan0')
    # I guess localhost is always up...
    if 'lo' in all_interfaces():
        return get_ip_address('lo')

def increaseNumber():
    global number
    if number == 255:
        number = 0
    else:
        number += 1
    board.printNumberWithLeds(number)
    board.display.home()
    board.display.clear()
    board.display.message("Number is: ")
    board.display.message(str(number))

def decreaseNumber():
    global number
    if number == 0:
        number = 255
    else:
        number -= 1
    board.printNumberWithLeds(number)
    board.display.home()
    board.display.clear()
    board.display.message("Number is: ")
    board.display.message(str(number))

if __name__ == "__main__":
    main(sys.argv[1:])

#!/usr/bin/env python
"""Communicate with a mcp23017 i2c gpio expander over I2C
   (Take care of the voltage levels!)

	        PINOUT 
	       mcp23017
              +--------+
	GPB0 -+ 01  28 +- GPA7
	GPB1 -+ 02  27 +- GPA6
	GPB2 -+ 03  26 +- GPA5
	GPB3 -+ 04  25 +- GPA4
	GPB4 -+ 05  24 +- GPA3
	GPB5 -+ 06  23 +- GPA2
	GPB6 -+ 07  22 +- GPA1
	GPB7 -+ 08  21 +- GPA0
	 VDD -+ 09  20 +- INTA
	 VSS -+ 10  19 +- INTB
	  NC -+ 11  18 +- !RESET
	 SCL -+ 12  17 +- A2
	 SDA -+ 13  16 +- A1
	  NC -+ 14  15 +- A0
              +--------+

"""

import os
import sys

if not os.getegid() == 0:
    sys.exit('Script must be run as root')

from time import sleep

from pyRock.gpio import gpio
import pyRock.MCP230xx as MCP

# initialize gpio expander
mcp = MCP.MCP23017(0x20)

# LED at GPB0
led = mcp.GPB0

try:
    print ("Press CTRL+C to exit")

    mcp.output(led, gpio.HIGH)

    while True:
	mcp.output(led, gpio.HIGH)
    	sleep(1)
	mcp.output(led, gpio.LOW)
	sleep(1)

except KeyboardInterrupt:
    print ("Goodbye.")

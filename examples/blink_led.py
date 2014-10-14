#!/usr/bin/env python
"""Basic blinking led example.

The red/green/blue led on RR blinks every other 1 second.
"""

import os
import sys

if not os.getegid() == 0:
    sys.exit('Script must be run as root')

from time import sleep
from pyRock.gpio import gpio

gpio.init()

red = gpio.PIN0PB7
green = gpio.PIN0PB4
blue = gpio.PIN0PB6

try:
    print ("Press CTRL+C to exit")
    while True:
        gpio.output(red, gpio.HIGH)
        gpio.output(green, gpio.HIGH)
        gpio.output(blue, gpio.HIGH)
        sleep(1)

        gpio.output(red, gpio.LOW)
        gpio.output(green, gpio.LOW)
        gpio.output(blue, gpio.LOW)
        sleep(1)
except KeyboardInterrupt:
    print ("Goodbye.")

#!/usr/bin/env python
from pyRock.radxa_gpio import radxa_gpio
from time import sleep
try:
    print ("Press CTRL+C to exit")
    rad = radxa_gpio()
    while True:
        print('..........1')
        rad.output(rad.redLED, rad.HIGH)
        sleep(2)
        print('.....0')
        rad.output(rad.redLED, rad.LOW)
        sleep(2)
except KeyboardInterrupt:
    print ("Goodbye.")

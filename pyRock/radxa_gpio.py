#!/usr/bin/env python
# filename: radxa_gpio.py
#
# Rockchip RK3188 datasheet:
# http://rockchip.fr/RK3188%20datasheet%20V1.0.pdf
#
# pyRock.gpio library project, authored by Tom Cubie
# https://github.com/radxa/pyRock
#
# radxa rock extension header:
# http://radxa.com/Rock/extension_header
#
# other interesting gpio info:
# http://radxa.com/Rock/GPIO
# http://radxa.com/Rock/LED

import os
import sys
from pyRock.gpio import gpio

class radxa_gpio:
    def __init__(self):
        if not os.getegid() == 0:
            sys.exit('Script must be run as root')
        gpio.init()
        self.redLED = gpio.PIN0PB7
        self.greenLED = gpio.PIN0PB4
        self.blueLED = gpio.PIN0PB6
        self.j8p7 = gpio.PIN0PA7
        self.j8p8 = gpio.PIN0PA6
        self.j8p9 = gpio.PIN0PB1
        self.j8p10 = gpio.PIN0PA1
        self.j8p11 = gpio.PIN3PD5
        self.j8p12 = gpio.PIN3PD4
        self.j8p13 = gpio.PIN1PA0
        self.j8p14 = gpio.PIN1PA1
        self.j8p15 = gpio.PIN1PA2
        self.j8p16 = gpio.PIN1PA3
        self.j8p19 = gpio.PIN0PD7
        self.j8p20 = gpio.PIN1PB5
        self.j8p21 = gpio.PIN0PD4
        self.j8p22 = gpio.PIN1PB2
        self.j8p23 = gpio.PIN0PD6
        self.j8p24 = gpio.PIN1PB3
        self.j8p26 = gpio.PIN1PB4
        self.j8p27 = gpio.PIN0PA5
        self.j8p28 = gpio.PIN0PD5
        self.j8p31 = gpio.PIN1PD1
        self.j8p32 = gpio.PIN1PD0
        #self.j12p26 = gpio.PIN
        #self.j12p27 = gpio.PIN
        #self.j12p28 = gpio.PIN
        #self.j12p30 = gpio.PIN
        self.j12p31 = gpio.PIN0PB0
        self.j12p32 = gpio.PIN0PA2
        self.j12p33 = gpio.PIN1PD6
        self.j12p34 = gpio.PIN1PB7
        self.j12p35 = gpio.PIN1PA7
        self.j12p36 = gpio.PIN1PA4
        self.j12p37 = gpio.PIN1PA6
        self.j12p38 = gpio.PIN1PA5
        self.HIGH = gpio.HIGH
        self.LOW = gpio.LOW
        self.INPUT = gpio.INPUT
        self.OUTPUT = gpio.OUTPUT
        self.PULLUP = gpio.PULLUP
        self.PULLDOWN = gpio.PULLDOWN

    def init(self):
        gpio.init()

    def input(self, pin):
        return gpio.input(pin)

    def output(self, pin, state):
        return gpio.output(pin, state)

    def getmux(self, pin):
        return gpio.getmux(pin)

    def setmux(self, pin, mux):
        return gpio.setmux(pin, mux)

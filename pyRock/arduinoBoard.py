#!/usr/bin/env python
#  file: arduinoBoard.py
# autor: frep
#  desc: class to handle the radxa rock arduino shield Rev. A, see
#        http://talk.radxa.com/topic/839/radxa-rock-arduino-board-rev-a

import os
import sys
import math
from pyRock.radxa_gpio import radxa_gpio
import pyRock.MCP230xx as MCP

class ArduinoBoard:
    def __init__(self):
	# initialize the Board:
	# 1.) initialize the gpio's
        ArduinoBoard.gpio = radxa_gpio()
	# 2.) define the button objects
	self.button1 = self.Button(1, ArduinoBoard.gpio.j8p7)
	self.button2 = self.Button(2, ArduinoBoard.gpio.j8p8)
	self.button = []
	self.button.append(self.button1)
	self.button.append(self.button2)
	# 3.) define  the led objects
	self.led1 = self.Led(1, ArduinoBoard.gpio.j8p9)
	self.led2 = self.Led(2, ArduinoBoard.gpio.j8p20)
	self.led3 = self.Led(3, ArduinoBoard.gpio.j8p22)
	self.led4 = self.Led(4, ArduinoBoard.gpio.j8p24)
	self.led5 = self.Led(5, ArduinoBoard.gpio.j8p23)
	self.led6 = self.Led(6, ArduinoBoard.gpio.j8p28)
	self.led7 = self.Led(7, ArduinoBoard.gpio.j8p21)
	self.led8 = self.Led(8, ArduinoBoard.gpio.j8p19)
	self.led = []
	self.led.append(self.led1)
	self.led.append(self.led2)
	self.led.append(self.led3)
	self.led.append(self.led4)
	self.led.append(self.led5)
	self.led.append(self.led6)
	self.led.append(self.led7)
	self.led.append(self.led8)
	# 4.) define the display object
	# TODO ....

    def printNumberWithLeds(self, number):
        if number > 255 :
            number = 255
        for i in range(0, 8, 1):
            if (number / pow(2, (7-i))) > 0:
                self.led[i].setOn()
	    else:
		self.led[i].setOff()
            number = number % pow(2, (7-i))


    class Led:
	def __init__(self, id, pin):
	    self.id = id
	    self.pin = pin
	    self.isOn = False
	def setOn(self):
            ArduinoBoard.gpio.output(self.pin, ArduinoBoard.gpio.HIGH)
            self.isOn = True
	def setOff(self):
	    ArduinoBoard.gpio.output(self.pin, ArduinoBoard.gpio.LOW)
	    self.isOn = False
	def toggle(self):
	    if self.isOn == True:
		self.setOff()
	    else:
		self.setOn()

    class Button:
	def __init__(self, id, pin, logicLevel="activeLow"):
	    self.id = id
	    self.pin = pin
	    self.logicLevel = logicLevel
	    self.state = ArduinoBoard.gpio.input(self.pin)
	    self.isPressed = self.evaluate(self.state, self.logicLevel)
	def check(self):
	    #print "button %d is %d" % (self.id, ArduinoBoard.gpio.input(self.pin))
	    if self.state != ArduinoBoard.gpio.input(self.pin):
		self.state = ArduinoBoard.gpio.input(self.pin)
		self.isPressed = self.evaluate(self.state, self.logicLevel)
		if self.isPressed == 0:
		    print "Button %d is released" % self.id
		else:
		    print "Button %d is pressed" % self.id
	def evaluate(self, state, logicLevel):
	    if logicLevel == "activeLow":
		if state == 0:
		    # if an activeLow button is LOW, it's pressed
		    return 1
		else:
		    # if an activeLow button is HIGH, it's not pressed
		    return 0
	    else:
		if state == 0:
		    # if an activeHigh button is LOW, it's not pressed
		    return 0
		else:
		    # if an activeHigh button is HIGH, its pressed
		    return 1

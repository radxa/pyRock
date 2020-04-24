#!/usr/bin/env python
#  file: arduinoBoard.py
# autor: frep
#  desc: class to handle the radxa rock arduino shield Rev. A, see
#        http://talk.radxa.com/topic/839/radxa-rock-arduino-board-rev-a

import os
import sys
import time
from pyRock.radxa_gpio import radxa_gpio
from pydispatch import dispatcher
import pyRock.MCP230xx as MCP


class ArduinoBoard:

    def __init__(self):
        # initialize the Board:
        # initialize the gpio's
        ArduinoBoard.gpio = radxa_gpio()
        # setup the dispatcher signals for button events
        ArduinoBoard.SIGNAL_BUTTON_CHANGED  = 'button_changed'
        ArduinoBoard.SIGNAL_BUTTON_PRESSED  = 'button_pressed'
        ArduinoBoard.SIGNAL_BUTTON_RELEASED = 'button_released'
        # define the button objects
        self.button1 = self.Button(1, ArduinoBoard.gpio.j8p7)
        self.button2 = self.Button(2, ArduinoBoard.gpio.j8p8)
        self.button = []
        self.button.append(self.button1)
        self.button.append(self.button2)
        # define  the led objects
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
        # define the display object
        self.display = self.Display()

    def printNumberWithLeds(self, number):
        if number > 255 :
            number = 255
        for i in range(0, 8, 1):
            if (number / (1 << (7-i))) > 0:
                self.led[i].setOn()
            else:
                self.led[i].setOff()
            number = number % (1 << (7-i))


    class Display:

        def __init__(self):
             # define a lot of display constants
            # commands
            self.LCD_CLEARDISPLAY   = 0x01
            self.LCD_RETURNHOME     = 0x02
            self.LCD_ENTRYMODESET   = 0x04
            self.LCD_DISPLAYCONTROL = 0x08
            self.LCD_CURSORSHIFT    = 0x10
            self.LCD_FUNCTIONSET    = 0x28
            self.LCD_SETCGRAMADDR   = 0x40
            self.LCD_SETDDRAMADDR   = 0x80
            # flags for display entry mode
            self.LCD_ENTRYRIGHT     = 0x00
            self.LCD_ENTRYLEFT      = 0x02
            self.LCD_ENTRYSHIFTINC  = 0x01
            self.LCD_ENTRYSHIFTDEC  = 0x00
            # flags for display on/off control
            self.LCD_DISPLAYON      = 0x04
            self.LCD_DISPLAYOFF     = 0x00
            self.LCD_CURSORON       = 0x02
            self.LCD_CURSOROFF      = 0x00
            self.LCD_BLINKON        = 0x01
            self.LCD_BLINKOFF       = 0x00
            # flags for display/cursor shift
            self.LCD_DISPLAYMOVE    = 0x08
            self.LCD_CURSORMOVE     = 0x00
            self.LCD_MOVERIGHT      = 0x04
            self.LCD_MOVELEFT       = 0x00
            # flags for function set
            self.LCD_8BITMODE       = 0x10
            self.LCD_4BITMODE       = 0x00
            self.LCD_JAPANESE       = 0x00
            self.LCD_EUROPEAN_I     = 0x01
            self.LCD_RUSSIAN        = 0x02
            self.LCD_EUROPEAN_II    = 0x03
            # initialize gpio expander and used IO's
            self.mcp      = MCP.MCP23017(0x20)
            self.RS_PIN   = self.mcp.GPA7
            self.RW_PIN   = self.mcp.GPA6
            self.EN_PIN   = self.mcp.GPA5
            self.D4_PIN   = self.mcp.GPB4
            self.D5_PIN   = self.mcp.GPB5
            self.D6_PIN   = self.mcp.GPB6
            self.D7_PIN   = self.mcp.GPB7
            self.BUSY_PIN = self.D7_PIN
            # initialize display control, function and mode registers
            self.displaycontrol = self.LCD_DISPLAYON | self.LCD_CURSOROFF | self.LCD_BLINKOFF
            self.displayfunction = self.LCD_4BITMODE
            self.displaymode = self.LCD_ENTRYLEFT | self.LCD_ENTRYSHIFTDEC
            # Offset for up to 4 rows
            self.LCD_ROW_OFFSETS = (0x00, 0x40, 0x14, 0x54)

        def writeRegister(self, register, value):
            self.mcp._i2c.write8(register, value)

        def readRegister(self, register):
            return self.mcp._i2c.readU8(register)

        def pulseEnable(self):
            self.gpioA = self.readRegister(self.mcp.GPIOA)
            # set EnablePin
            self.gpioA = self.gpioA | 0x20
            self.writeRegister(self.mcp.GPIOA, self.gpioA)
            self._delay_microseconds(50)
            # clear EnablePin
            self.gpioA = self.gpioA & 0xDF
            self.writeRegister(self.mcp.GPIOA, self.gpioA)

        def write4bits(self, value):
            regValue = value & 0x0F
            regValue = regValue << 4
            self.writeRegister(self.mcp.GPIOB, regValue)
            self._delay_microseconds(50)
            self.pulseEnable()

        def send(self, value, mode):
            if mode > 0:
                self.writeRegister(self.mcp.GPIOA, 0x80)
            else:
                self.writeRegister(self.mcp.GPIOA, 0x00)
            self.write4bits(value>>4)
            self.write4bits(value)

        def command(self, value):
            self.send(value, 0)
            self.waitForReady()

        def write(self, value):
            self.send(value, 1)
            self.waitForReady()

        def waitForReady(self):
            self.busy = 1
            self.mcp.setup(self.BUSY_PIN, ArduinoBoard.gpio.INPUT)
            self.writeRegister(self.mcp.GPIOA, 0x40)
            while self.busy > 0:
                self.writeRegister(self.mcp.GPIOA, 0x60)
                self._delay_microseconds(10)
                self.busy = self.mcp.input(self.BUSY_PIN)
                self.writeRegister(self.mcp.GPIOA, 0x40)
                self.pulseEnable()
            self.mcp.setup(self.BUSY_PIN, ArduinoBoard.gpio.OUTPUT)
            self.writeRegister(self.mcp.GPIOA, 0x00)

        def _delay_microseconds(self, microseconds):
            end = time.time() + (microseconds/1000000.0)
            while time.time() < end:
                pass

        def message(self, text):
            for char in text:
                if char == '\n':
                    self.currline += 1
                    # Move to left or right side depending on text direction
                    col = 0 if self.displaymode & self.LCD_ENTRYLEFT > 0 else self.numcols - 1
                    self.setCursor(col, self.currline)
                else:
                    self.write(ord(char))

        def begin(self, cols, lines):
            self.numcols = cols
            self.numlines = lines
            self.currline = 0
            # define every IO of the mcp as output
            self.writeRegister(self.mcp.IODIRA, 0x00)
            self.writeRegister(self.mcp.IODIRB, 0x00)
            self.writeRegister(self.mcp.GPIOA, 0x00)
            self._delay_microseconds(50000)
            self.writeRegister(self.mcp.GPIOB, 0x00)
            # initialize display
            self.write4bits(0x03)
            self._delay_microseconds(5000)
            self.write4bits(0x08)
            self._delay_microseconds(5000)
            self.write4bits(0x02)
            self._delay_microseconds(5000)
            self.write4bits(0x02)
            self._delay_microseconds(5000)
            self.write4bits(0x08)
            self._delay_microseconds(5000)
            self.command(self.LCD_DISPLAYCONTROL | self.LCD_DISPLAYOFF)
            self._delay_microseconds(5000)
            self.command(self.LCD_CLEARDISPLAY)
            self._delay_microseconds(5000)
            self.command(self.LCD_ENTRYMODESET | self.displaymode)
            self._delay_microseconds(5000)
            self.command(self.LCD_RETURNHOME)
            self._delay_microseconds(5000)
            self.command(self.LCD_DISPLAYCONTROL | self.displaycontrol)

        def setCursor(self, col, row):
            # Write to first line if out off bounds
            if row >= self.numlines:
                row = 0
            # set location
            self.command(self.LCD_SETDDRAMADDR | (col + self.LCD_ROW_OFFSETS[row]))

        def home(self):
            self.command(self.LCD_RETURNHOME)

        def clear(self):
            self.command(self.LCD_CLEARDISPLAY)

        def noDisplay(self):
            self.displaycontrol &= ~self.LCD_DISPLAYON
            self.command(self.LCD_DISPLAYCONTROL | self.displaycontrol)

        def display(self):
            self.displaycontrol |= self.LCD_DISPLAYON
            self.command(self.LCD_DISPLAYCONTROL | self.displaycontrol)

        def noCursor(self):
            self.displaycontrol &= ~self.LCD_CURSORON
            self.command(self.LCD_DISPLAYCONTROL | self.displaycontrol)

        def cursor(self):
            self.displaycontrol |= self.LCD_CURSORON
            self.command(self.LCD_DISPLAYCONTROL | self.displaycontrol)

        def noBlink(self):
            self.displaycontrol &= ~self.LCD_BLINKON
            self.command(self.LCD_DISPLAYCONTROL | self.displaycontrol)

        def blink(self):
            self.displaycontrol |= self.LCD_BLINKON
            self.command(self.LCD_DISPLAYCONTROL | self.displaycontrol)

        def scrollDisplayLeft(self):
            self.command(self.LCD_CURSORSHIFT | self.LCD_DISPLAYMOVE | self.LCD_MOVELEFT )

        def scrollDisplayRight(self):
            self.command(self.LCD_CURSORSHIFT | self.LCD_DISPLAYMOVE | self.LCD_MOVERIGHT )

        def leftToRight(self):
            self.displaymode |= self.LCD_ENTRYLEFT
            self.command(self.LCD_ENTRYMODESET | self.displaymode)

        def rightToLeft(self):
            self.displaymode &= ~self.LCD_ENTRYLEFT
            self.command(self.LCD_ENTRYMODESET | self.displaymode)

        def noAutoscroll(self):
            self.displaymode &= ~self.LCD_ENTRYSHIFTINC
            self.command(self.LCD_ENTRYMODESET | self.displaymode)

        def autoscroll(self):
            self.displaymode |= self.LCD_ENTRYSHIFTINC
            self.command(self.LCD_ENTRYMODESET | self.displaymode)


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
                dispatcher.send( signal=ArduinoBoard.SIGNAL_BUTTON_CHANGED, sender=self.id )
                if self.isPressed == 0:
                    dispatcher.send( signal=ArduinoBoard.SIGNAL_BUTTON_RELEASED, sender=self.id )
                    #print "Button %d is released" % self.id
                else:
                    dispatcher.send( signal=ArduinoBoard.SIGNAL_BUTTON_PRESSED, sender=self.id )
                    #print "Button %d is pressed" % self.id

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

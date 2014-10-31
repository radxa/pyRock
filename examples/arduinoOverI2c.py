#!/usr/bin/env python
"""Communicate with an Arduino over I2C
   (Take care of the voltage levels!)
   
   Use the following sketch for the Arduino:

   #include <Wire.h>

   #define SLAVE_ADDRESS 0x04
   int number = 0;

   void setup()
   {
     pinMode(13, OUTPUT);
     Serial.begin(9600);
     Wire.begin(SLAVE_ADDRESS);
     Wire.onReceive(receiveData);
     Wire.onRequest(sendData);
     Serial.println("Ready!");
   }

   void loop()
   {
     delay(100);
   }

   // function is called, when master writes data to Arduino-slave
   void receiveData(int byteCount)
   {
     while(Wire.available())
     {
       number = Wire.read();
       Serial.print("data received: ");
       Serial.println(number);
     }
   }

   // function is called, when master reads data from Arduino-slave
   void sendData()
   {
     Wire.write(number);
   }


"""

import os
import sys

if not os.getegid() == 0:
    sys.exit('Script must be run as root')

from time import sleep

import smbus
import pyRock.I2C as I2C

# initialize i2c-device
arduinoSlave = I2C.Device(0x04, 0)

try:
    print ("Press CTRL+C to exit")

    while True:
    	var = input("Enter 1 - 9: ")
    	if not var:
        	continue

    	arduinoSlave.writeRaw8(var)
    	print "Radxa: Hi Arduino, I sent you ", var
    	# sleep one second
    	sleep(1)

    	number = arduinoSlave.readRaw8()
    	print "Arduino: Hey Radxa, I received a digit ", number
    	print

except KeyboardInterrupt:
    print ("Goodbye.")

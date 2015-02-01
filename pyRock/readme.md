Description
===========
Overview of the different python packages and modules

gpio
----
Tom Cubie's python module to handle the GPIO's of the radxa device.  
example usage: pyRock/examples/blink_led.py

utilities
---------
Probably some useful stuff :smiley:

I2C.py
------
python module based on python-smbus to handle the i2c bus. It is nearly entirely copied from
[Adafruit_Python_GPIO](https://github.com/adafruit/Adafruit_Python_GPIO). If it shouldn't work
for you blame me. If you like it, thank to Adafruit's team.  
example usage: pyRock/examples/arduinoOverI2c.py 

MCP230xx.py
-----------
python module based on the I2C.py module from above. It supports i2c gpio expander mcp23017 and mcp23008.
As the I2C.py, this module is copied from [Adafruit_Python_GPIO](https://github.com/adafruit/Adafruit_Python_GPIO) 
and slightly modified.  
example usage: pyRock/examples/mcp23017.py

radxa_gpio.py
-------------
Wrapper class for gpio module from gruuvinrob. It takes care of the gpio initialisation and the root permission.
Further, the gpio pins can be accessed by it's physical location (Header/headerpin), e.g. .j8p19 instead of .PIN0PD7  
example usage: pyRock/examples/radxaGpioBlinkLed.py

arduinoBoard.py
---------------
Class to handle the [Arduino Shield Rev.A](http://talk.radxa.com/topic/839/radxa-rock-arduino-board-rev-a). It makes
use of the radxa_gpio.py (using the gpio library) to interact with the buttons and the leds of the board. It
also uses the MCP230xx.py (using the I2C.py) to communicate over the mcp23017 i2c gpio expander to the oled display.
The button events and actions are decoupled by using the publish/subscriber-pattern. For this purpose, the python 
module pydispatch is used. Unfortunatly, you have to install this seperatly: pip install PyDispatcher. Sorry for that!    
example usage: pyRock/examples/testArduinoBoard.py

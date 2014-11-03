Description
===========
Overview of the different python packages and modules

gpio
----
Tom Cubie's python module to handle the GPIO's of the radxa device.

utilities
---------
Probably some useful stuff :smiley:

I2C.py
------
python module based on python-smbus to handle the i2c bus. It is nearly entirely copied from
[Adafruit_Python_GPIO](https://github.com/adafruit/Adafruit_Python_GPIO). If it shouldn't work
for you blame me. If you like it, thank to Adafruit's team.

MCP230xx.py
-----------
python module based on the I2C.py module from above. It supports i2c gpio expander mcp23017 and mcp23008.
As the I2C.py, this module is copied from [Adafruit_Python_GPIO](https://github.com/adafruit/Adafruit_Python_GPIO) 
and slightly modified.

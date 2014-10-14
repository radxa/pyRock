This package provide methods for controlling GPIO pins on rockchip platform.
This is written for radxa rock/rock pro/rock lite, but it can be used with other 
rockchip boards. If you do this we cannot guarantee proper operation of the module.
Before using this package we recommend reading the article at radxa wiki:

http://radxa.com/Rock/GPIO
http://radxa.com/Rock/extension_header

When using GPIO make sure that the desired gpio is not used by another periphery.

INSTALL
============
    sudo apt-get install gcc python-dev
    python setup.py install

UNINSTALL
============
    rm -rf /usr/local/lib/python2.7/dist-packages/pyRock*

GPIO METHODS
============

    init()      -   Make initialization of the module. Always must be called first.
    input()     -   Return current value of gpio.
    output()    -   Set output value.
    getmux()    -   Read current configuration of gpio.
    setmux()    -   Write configuration to gpio.


The available constants are:

    NAME        -   EQUALS TO
    ====            =========
    HIGH        ->      1
    LOW         ->      0
    INPUT       ->      0
    OUPTUT      ->      1
    PULLUP      ->      1
    PULLDOWN    ->      2


The gpio are named in following way:

    By pin name in upper case or lower case:
    PIN0PA0, PIN1PB1, PIN3PD7, or
    pin0pa0, pin1pb1, pin3pd7 etc
    These can be imported from port module:

    >>> from pyRock.gpio import gpio
    >>> print gpio.PIN0PA0

Generally these constants are just an offset in the memory from the base GPIO address, so they can
be assigned to a number type variable.

    >>> led = gpio.PIN0PB7
    >>> print led
    15

It's important that you run your python script as root!

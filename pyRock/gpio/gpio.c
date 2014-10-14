/* GPIO python extension for rockchip soc.
 *
 * Copyright (c) 2014 Radxa Limited.
 * http://radxa.com
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License version 2 as
 * published by the Free Software Foundation.
 */


#include "Python.h"
#include "gpio_lib.h"

/**
 * Set output value of GPIO. Pin must be configured as output or else raises
 * exception. For high output level - 1, low - 0.
 * 
 * @param self
 * @param args Tuple that holds GPIO number and value 
 * @return none
 */
static PyObject* py_output(PyObject* self, PyObject* args) {

    int gpio;
    int value;

    /* Parse arguments. Two integers are required. */
    if (!PyArg_ParseTuple(args, "ii", &gpio, &value))
        return NULL;

    /* Set output value and check return status. */
    if (rockchip_gpio_output(gpio, value) < 0) {
        return PyErr_SetFromErrno(PyExc_IOError);
    }
    
    Py_RETURN_NONE;
}

/**
 * Read value of the pin configured as input. If its output raises exception.
 * 
 * @param self
 * @param args GPIO number
 * @return value of the given pin
 */
static PyObject* py_input(PyObject* self, PyObject* args) {

    int gpio;
    int ret;

    /* Parse argument. One integer is required */
    if (!PyArg_ParseTuple(args, "i", &gpio))
        return NULL;
    
    /* Read value */
    ret = rockchip_gpio_input(gpio);
    if (ret < 0) {
        return PyErr_SetFromErrno(PyExc_IOError);
    }

    /* Return read value */
    return Py_BuildValue("i", ret);
}

/**
 * Set pin multiplexing. See rockchip datasheet for correct values.
 * 
 * @param self
 * @param args GPIO number and configuration value
 * @return none
 */
static PyObject* py_setmux(PyObject* self, PyObject* args) {

    unsigned int gpio;
    unsigned int mux;

    /* Parse arguments. Require two integers for GPIO number and configuration */
    if (!PyArg_ParseTuple(args, "ii", &gpio, &mux))
        return NULL;
    
    /* Set multiplexing and check return status */
    if (rockchip_gpio_set_mux(gpio, mux) < 0) {
        return PyErr_SetFromErrno(PyExc_IOError);
    }

    Py_RETURN_NONE;
}

/**
 * Read current pin multiplexing.
 * 
 * @param self
 * @param args GPIO number
 * @return current multiplexing
 */
static PyObject* py_getmux(PyObject* self, PyObject* args) {

    int gpio;
    int ret;

    /* Parse arguments */
    if (!PyArg_ParseTuple(args, "i", &gpio))
        return NULL;

    /* Read configuration*/
    ret = rockchip_gpio_get_mux(gpio);
    if (ret < 0) {
        return PyErr_SetFromErrno(PyExc_IOError);
    }

    /* Return configuration */
    return Py_BuildValue("i", ret);
}

/**
 * 
 * Make initial initialization of the extention. This is done by map physical
 * memory to the virtual and thus gaining access to the memory. From there we
 * can do anything. 
 * 
 * @return none
 */
static PyObject* py_init(PyObject* self, PyObject* args) {

    if(rockchip_gpio_init() < 0){
        return PyErr_SetFromErrno(PyExc_IOError);
    }

    Py_RETURN_NONE;
}

/**
 *  Set pull-up/pull-down on pin defined as input.
 * 
 * @param self
 * @param args
 * @return 
 */
static PyObject* py_pullup(PyObject* self, PyObject* args) {
    
    int gpio;
    int pull;
    
    /* Parse arguments */
    if(!PyArg_ParseTuple(args, "ii", &gpio, &pull))
        return NULL;
    
    /* Set pull-up */
    if(rockchip_gpio_pullup(gpio, pull) < 0){
        return PyErr_SetFromErrno(PyExc_IOError);
    }
    
    Py_RETURN_NONE;
}


/* Define module methods */
static PyMethodDef module_methods[] = {
    {"init",    py_init,        METH_NOARGS,    "Initialize module"},
    {"setmux",  py_setmux,      METH_VARARGS,   "Set pin function"},
    {"getmux",  py_getmux,      METH_VARARGS,   "Get pin function"},
    {"output",  py_output,      METH_VARARGS,   "Set output state"},
    {"pullup",  py_pullup,      METH_VARARGS,   "Set pull-up/pull-down"},
    {"input",   py_input,       METH_VARARGS,   "Get input state"},
    {NULL, NULL, 0, NULL}
};

#if PY_MAJOR_VERSION >= 3
static struct PyModuleDef module_def = {
    PyModuleDef_HEAD_INIT,
    "gpio",
    NULL,
    -1,
    module_methods
};
#endif

PyMODINIT_FUNC
#if PY_MAJOR_VERSION >= 3
    PyInit_gpio(void) {
#else
    initgpio(void) {
#endif

    PyObject* module = NULL;


#if PY_MAJOR_VERSION >= 3
    module = PyModule_Create(&module_def);
#else
    module = Py_InitModule("gpio", module_methods);
#endif


    if (module == NULL)
#if PY_MAJOR_VERSION >= 3
        return NULL;
#else
        return;
#endif
	/* Build the pin names and some value */
	int bank, i;
	char name[8];
	int pin = 0;
	char x;

	for(bank = 0; bank < 4; bank++) {
		for(x = 0; x < 4; x++) {
			for(i = 0; i < 8; i++) {
			
				sprintf(name, "pin%dp%c%d", bank, x+'a', i);
				PyModule_AddObject(module, name, Py_BuildValue("i", pin));

				sprintf(name, "PIN%dP%c%d", bank, x+'A', i);
				PyModule_AddObject(module, name, Py_BuildValue("i", pin));

				pin++;
			}
		}
	}

    PyModule_AddObject(module, "HIGH", Py_BuildValue("i", 1));
    PyModule_AddObject(module, "LOW", Py_BuildValue("i", 0));
    PyModule_AddObject(module, "INPUT", Py_BuildValue("i", ROCKCHIP_GPIO_INPUT));
    PyModule_AddObject(module, "OUTPUT", Py_BuildValue("i", ROCKCHIP_GPIO_OUTPUT));

    PyModule_AddObject(module, "PULLUP", Py_BuildValue("i", ROCKCHIP_PULL_UP));
    PyModule_AddObject(module, "PULLDOWN", Py_BuildValue("i", ROCKCHIP_PULL_DOWN));


    #if PY_MAJOR_VERSION >= 3
        return module;
    #else
        return;
    #endif
}

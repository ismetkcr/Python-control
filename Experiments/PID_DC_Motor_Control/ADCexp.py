# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 10:15:29 2024

@author: ismt
"""

import utime
import machine
from openLooputils import ml2pwm_pump1, ml2pwm_pump2
from ulab import numpy as np
from motorDrivers import LN298
from easy_comms import Easy_comms
from PIDcontrollerclass import PIDcontroller
from PCF8591 import PCF8591

sda = machine.Pin(18)
scl = machine.Pin(19)
i2c = machine.I2C(1,sda=sda,scl=scl)

PCF = PCF8591(0x48, i2c)
if PCF.begin():
    print("PCF8591 found")
    
while True:
    val = (PCF.voltage_read(PCF8591.AIN2))
    print(val)
    utime.sleep_ms(50)

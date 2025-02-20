import utime
from machine import Pin as pin, PWM
from openLooputils import ml2pwm_pump1, ml2pwm_pump2
from ulab import numpy as np
from motorDrivers import LN298
from easy_comms import Easy_comms
from PIDcontrollerclass import PIDcontroller
from PCF8591 import PCF8591
import time
def read_vol():
    buf = []
    for i in range(10):
        buf.append(PCF.voltage_read(PCF8591.AIN0))
        utime.sleep_ms(10)

    buf.sort()
    avgValue = np.mean((buf[2:8]))
    
    print("sensor = ", avgValue)
    
    return avgValue
adc_pin = machine.ADC(28)

sda = machine.Pin(18)
scl = machine.Pin(19)
i2c = machine.I2C(1,sda=sda,scl=scl, freq=400000)
i = 0
PCF = PCF8591(0x48, i2c)
if PCF.begin():
    print("PCF8591 found")
while True:
    
    val = read_vol()
    pot = PCF.voltage_read(PCF8591.AIN3)
    phValue = (-5.70 * val + 21.34) / 5 * 3
    if i % 5 == 0:
        print('val', phValue,'pot',  pot)
    i += 1
    time.sleep(0.5)

    
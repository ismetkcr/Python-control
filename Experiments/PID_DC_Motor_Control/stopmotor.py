import utime
import machine

from motorDrivers import HW039
pwmpin  = 12
enablepin = 5

prop = HW039(pwmpin, enablepin)
prop.displayPins()

prop.motorpwm.duty_u16(0)
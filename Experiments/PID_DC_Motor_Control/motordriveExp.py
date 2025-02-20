from machine import  Pin,  PWM
import time
def checkdenum(denum, inc):
    if denum < 1:
        inc = True
        
    elif denum > 6:
        inc = False
        
    else:
        pass
    if inc == True:
        denum = denum + 0.25
    else:
        denum =denum - 0.25
        
    return denum, inc



pwmpin  = 12
enablepin1 = 6
enablepin2 = 7 
motoren1 = Pin(enablepin1, Pin.OUT)
motoren2 = Pin(enablepin2, Pin.OUT)
motorpwm = PWM(Pin(pwmpin))
motorpwm.freq(4000)
motoren1.value(0)
motoren2.value(0)
maxpwm = 65535
val = 1
chg = True

            
        
   
   
while True:
    time.sleep(.1)
    val, chg = checkdenum(val, chg)
    print(val)
    motorpwm.duty_u16(int(maxpwm / val))
    





















    



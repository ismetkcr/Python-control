from machine import  Pin,  PWM
import time
import utime

from encoder import rotaryEncoder


pwmpin  = 12
enablepin2 = 5
motoren2 = Pin(enablepin2, Pin.OUT)
motorpwm = PWM(Pin(pwmpin))
motorpwm.freq(5000)
motoren2.value(0)
maxpwm = 65535 / 2
val = 1
chg = True
def checkdenum(denum, inc):
    if denum < 1:
        inc = True
        
    elif denum > 5:
        inc = False
        
    else:
        pass
    if inc == True:
        denum = denum + 0.01
    else:
        denum =denum - 0.01
        
    return denum, inc


        
last_enc_counter1 = 0
enc_counter1 = 0
last_qtr_counter1 = 0
qtr_counter1 = 0
error1 = 0

last_enc_counter2 = 0
enc_counter2 = 0
last_qtr_counter2 = 0
qtr_counter2 = 0
error2 = 0

enc1 = rotaryEncoder(15, 14)
enc1.displayPins()
enc1.resetCounter()

enc2 = rotaryEncoder(10, 11) 
enc2.displayPins()
enc2.resetCounter()

while True:
    
    #val, chg = checkdenum(val, chg)
    #print(val)
    #motorpwm.duty_u16(int(maxpwm/3))
    motorpwm.duty_u16(int(qtr_counter2))
    
    start_time = utime.ticks_ms()
    start_pulse_count = enc1.enc_counter
    utime.sleep_ms(500)
    end_time = utime.ticks_ms()
    elapsed_time = end_time - start_time
    # Calculate RPM
    pulse_difference = enc1.enc_counter - start_pulse_count
    rpm = (pulse_difference / elapsed_time) * (60000 / 1600)  # RPM calculation
    
    print("RPM:", round(rpm))

    
    qtr_counter2 = round(enc2.enc_counter * 100) #may or may noy want to divide 4 for motor shaft encoder
    if qtr_counter2 != last_qtr_counter2:
        print("from set", qtr_counter2)
        last_enc_counter2 = enc2.enc_counter
        last_qtr_counter2 = qtr_counter2


    




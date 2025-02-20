
import utime
import machine
from ulab import numpy as np
from encoder import rotaryEncoder
from motorDrivers import HW039
from controlutilspico import PIDcontroller
from easy_comms import Easy_comms

pwmpin  = 12
enablepin = 5

prop = HW039(pwmpin, enablepin)
prop.displayPins()

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

unew = 12500
com1 = Easy_comms(0, 9600)
cum_elapsed_time = 0
while True:
    
    
    start_time = utime.ticks_ms()
    start_pulse_count = enc1.enc_counter
    utime.sleep_ms(50)
    
    end_time = utime.ticks_ms()
    elapsed_time = end_time - start_time
    # Calculate RPM
    pulse_difference = enc1.enc_counter - start_pulse_count
    rpm = (pulse_difference / elapsed_time) * (60000 / 1600)  # RPM calculation
    cum_elapsed_time += elapsed_time
    print("RPM:", round(rpm))
    
    
    
    
    qtr_counter2 = round(enc2.enc_counter / 4)
    if qtr_counter2<=40:
            qtr_counter2 = 0
     #may or may noy want to divide 4 for motor shaft encoder
    if qtr_counter2 != last_qtr_counter2:
        print("setPoint", qtr_counter2)
        last_enc_counter2 = enc2.enc_counter                
        last_qtr_counter2 = qtr_counter2
     
    
    rk = qtr_counter2
    
    
    time_sec = cum_elapsed_time / 1000
    if time_sec>=10:
        unew = 25000
    dead_bit = '00'
    com1.send(f'{dead_bit}, {time_sec:.1f}, {rpm:.1f}, {unew:.1f}, {rk:.1f}')
    prop.motorpwm.duty_u16(int(unew))
    
    
    
    print(" u = ", unew)
    
    
    
    
    
        
        
        
        
        
        
        
        
        
        

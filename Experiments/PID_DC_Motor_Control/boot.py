
import utime
import machine
from ulab import numpy as np
from encoder import R_Encoder
from motorDrivers import HW039
from controlutilspico import PIDcontroller
from easy_comms import Easy_comms
from machine import I2C
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

I2C_ADDR     = 39
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16
i2c = I2C(1, sda=machine.Pin(6), scl=machine.Pin(7), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

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

enc1 = R_Encoder(15, 14)
enc1.DisplayPins()
enc1.Reset_Counter()

enc2 = R_Encoder(10, 11) 
enc2.DisplayPins()
enc2.Reset_Counter()

controller = PIDcontroller(0.1)
#controller.assign_PID_parameters(70,0.06,0.0015)
controller.assign_PID_parameters(62.56,0.05,2e-5) #cohencoon param

yprev, yprev2, uprev, uprev2 = 0, 0, 0, 0
eprev = 0
umin, umax = 0, 65535 / 2
u_bias = 0
sprev, ubackprev, PID_backprev = 0, 0, 0

# com1 = Easy_comms(0, 9600)

rk = 0
unew = 0
rpm = 0
cum_elapsed_time = 0
time_sec = 0
diff = 0

counter_prev = 0
while True:
    
    
    start_time = utime.ticks_ms()
    start_pulse_count = enc1.enc_counter
    utime.sleep_ms(100)
    end_time = utime.ticks_ms()
    elapsed_time = end_time - start_time
    cum_elapsed_time += elapsed_time
    # Calculate RPM
    pulse_difference = enc1.enc_counter - start_pulse_count
    rpm = (pulse_difference / elapsed_time) * (60000 / 1600)  # RPM calculation
        
    qtr_counter2 = round(enc2.enc_counter / 4)
    diff = enc2.enc_counter - counter_prev
     #may or may noy want to divide 4 for motor shaft encoder
#     if qtr_counter2 != last_qtr_counter2:
#         #print("setPoint", rk)
#         last_enc_counter2 = enc2.enc_counter                
#         last_qtr_counter2 = qtr_counter2
#         counter_prev = enc2.enc_counter
#         if diff==0:
#             rk = 0
#         elif diff > 0:
#             if enc2.enc_counter>0 and enc2.enc_counter<=50:
#                 rk = 50
#                 enc2.enc_counter = enc2.enc_counter + (50*4) 
#             else:
#                 rk = qtr_counter2
#         elif diff < 0:
#             if enc2.enc_counter>0 and enc2.enc_counter<=(200):
#                 rk = 0
#                 enc2.enc_counter = 0
#             else:
#                  rk = qtr_counter2
#         if rk<=0:
#             rk = 0
#         print('currentset', rk)
#         
#         if enc2.enc_counter<0:
#             enc2.enc_counter = 0
    
            
    formatted_rpm = "{:.0f}".format(rpm)
    string_rpm = str("RPM: " + formatted_rpm)
    lcd.move_to(0,0)
    lcd.putstr(string_rpm)
            
    ynew = round(rpm)
    
    unew, error, s, uback, PID_back = controller.calculate_output(rk, ynew, eprev, umin, umax, uprev, sprev, ubackprev, PID_backprev,
                                      antiwindup= 'conditionalintegral', tt = None)
    
    
   
    
    #print(unew)
    prop.motorpwm.duty_u16(int(unew))
    
    eprev = error
    
    
    yprev2 = yprev
    yprev = ynew
    uprev2 = uprev
    uprev = unew
    
    sprev = s
    ubackprev = uback
    PID_backprev = PID_back
    time_sec = cum_elapsed_time / 1000
    print(time_sec)
    dead_bit = '00'
    com1.send(f'{dead_bit}, {time_sec:.1f}, {ynew:.1f}, {unew:.1f}, {rk:.1f}')    
    
#     sp = com1.read()
#     if sp is not None:
#         #print(f"message received: {message}")
#         datacomes = (sp)
    
    
    
    
    #print("qtr = ", qtr_counter2, "rk = ", rk, "diff = ", diff, 'enc2counter = ', enc2.enc_counter, 'prevcount = ', counter_prev)
    
           
    
    
    #rk = float(datacomes)
    rk = 220
    if rk == 0:
        rk = -50
    #------------------------------
    #q = np.array([rk])
    #print(np.mean(q))
        
        
        
        
        
        
        
        
        
        
from machine import  Pin as pin, PWM
import time



#ON/OFF led açıp kapamak için gerekli atamalar..
pinled = 15
led = pin(pinled, pin.OUT)
while True:
#     led.value(0)
    time.sleep(0.5)
    led.value(1)
    

#PWM olarak kullanmak için atamalar..

# pwmpin = 16
# pwm = PWM(pin(pwmpin))
# pwm.freq(5000)
# N = 65535
# for i in range(N):
#     pwm.duty_u16(i)
#     time.sleep(0.001)
#     
#     if i % 5000 == 0:
#         print(i)
        
        
    
# pwm.duty_u16(0) #turn of led

  

  
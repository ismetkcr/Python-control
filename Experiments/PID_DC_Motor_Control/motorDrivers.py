from machine import  Pin,  PWM


class LN298:
    def __init__(self,pinEN,pinIN1, pinIN2):
        self.pinEN = pinEN
        self.pinIN1 = pinIN1
        self.pinIN2 = pinIN2
        
        self.setupIN()
        
    def setupIN(self):
        print("XYZ")
        pwmpin  = self.pinEN
        enablepin1 = self.pinIN1
        enablepin2 = self.pinIN2 
        self.motoren1 = Pin(enablepin1, Pin.OUT)
        self.motoren2 = Pin(enablepin2, Pin.OUT)
        self.motorpwm = PWM(Pin(pwmpin))
        self.motorpwm.freq(5000)
        
    def displayPins(self):
        print("pin EN: ", self.pinEN, "pin IN1: ", self.IN1, "pin IN2: ", self.IN2)
        
class HW039:
    def __init__(self, pinRPWM, pinLPWM):
        self.pinRPWM = pinRPWM
        self.pinLPWM = pinLPWM
        self.setupIN()
    
        
    def displayPins(self):
        print("pin RPWM: ", self.pinRPWM, "pin LPWM: ", self.pinLPWM)
    
    def setupIN(self):
        print("XYZ")
                
        self.motoren = Pin(self.pinLPWM, Pin.OUT)
        self.motorpwm = PWM(Pin(self.pinRPWM))
        self.motorpwm.freq(1000)
        self.motoren.value(0)
    
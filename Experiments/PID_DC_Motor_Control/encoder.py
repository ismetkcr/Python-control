from machine import Pin,PWM




class rotaryEncoder:
    def __init__(self, Apin, Bpin):
        self.Apin = Apin
        self.Bpin = Bpin
        self.enc_counter = 0
        self.encAstate = 0
        self.encAstateold = 0
        self.encBstate = 0
        self.encBstateold = 0
        self.error = 0        
        self.setupIrq()
        
    def displayPins(self):
        print("pin A: ", self.Apin, "pin B: ", self.Bpin)
        
    def resetCounter(self):
        self.enc_counter = 0
        
    def encHandler(self, Source):
        self.encAstate = self.encApin.value()
        self.encBstate = self.encBpin.value()
        
        if self.encAstate == self.encBstateold and self.encBstate == self.encBstateold:
            self.error += 1
        elif (self.encAstate == 1 and self.encBstateold == 0) or (self.encAstate == 0 and self.encBstateold == 1):
            self.enc_counter += 1
        elif (self.encAstate == 1 and self.encBstateold == 1) or (self.encAstate == 0 and self.encBstateold == 0):
            self.enc_counter += -1
        else:
            self.error += 1
            
        self.encAstateold = self.encAstate
        self.encBstateold = self.encBstate
        
    def setupIrq(self):
        print('XYZ')
        self.encApin = machine.Pin(self.Apin, machine.Pin.IN, machine.Pin.PULL_DOWN)
        self.encApin.irq(trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING, handler=self.encHandler) #source sayesinde olabilir bi bak
        self.encBpin = machine.Pin(self.Bpin, machine.Pin.IN, machine.Pin.PULL_DOWN)
        self.encBpin.irq(trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING, handler=self.encHandler)
        
        self.encAstateold = self.encApin.value()
        self.encBstateold = self.encBpin.value()


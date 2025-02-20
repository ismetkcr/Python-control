# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 20:34:48 2024

@author: ismt
"""

class PIDcontroller(object):
    def __init__(self, dt):
        self.dt = dt
        self.eprev, self.eprev2 = 0, 0        
        self.uprev = 0
        self.ise = 0
        self.iae = 0
        self.s = 0
        self.veloutput = 0
        self.ubackprev = 0
        self.PID_backprev = 0
        self.umin = 0
        self.umax = 124
        self.ise = 0
        self.iae = 0
        self.controlerrormatrix = []
        
    def assignPIDparameters(self, KC, TI, TD):
        self.Kc = KC
        self.Ti = TI
        self.Td = TD
        
    def calculateoutput(self, r, ynew, antiwindup = 'CI', tt = None, vel = False):
        self.error = r - ynew       
        P_out = self.Kc * self.error
        D_out = self.Kc * self.Td * (self.error - self.eprev) / self.dt
        
        if vel == False:
            if antiwindup is None:
                self.s += (self.Kc / self.Ti) * self.error * self.dt
                I_out = self.s    
                self.PID_out = P_out + I_out + D_out
                self.PID_out = max(self.umin, min(self.PID_out, self.umax))
                
            if antiwindup == 'CI' :
                if self.umin < self.uprev < self.umax:
                    self.s += (self.Kc / self.Ti) * self.error * self.dt
                I_out = self.s    
                self.PID_out = P_out + I_out + D_out            
                self.PID_out = max(self.umin, min(self.PID_out, self.umax))
                
            if antiwindup == 'BC':
                self.tt = tt
                self.s += ((1 / self.tt) * (self.ubackprev - self.PID_backprev) + (self.Kc / self.Ti) * self.error) * self.dt
                I_out = self.s    
                PID_back = P_out + I_out + D_out            
                if PID_back <= self.umin:
                    self.uback = self.umin
                elif PID_back >= self.umax:
                    self.uback = self.umax
                else:
                    self.uback = PID_back             
                self.PID_out = PID_back            
                self.PID_out = max(self.umin, min(self.PID_out, self.umax))
                
                self.ubackprev = self.uback
                self.PID_backprev = PID_back
            
        if vel == True:
           
            a0 = self.Kc * (1 + (self.dt / self.Ti) + (self.Td / self.dt))
            a1 = self.Kc * (-1  - (2 * (self.Td / self.dt)))
            a2 = (self.Kc * self.Td) / self.dt
            self.veloutput += (a0 * self.error) + (a1 * self.eprev) + (a2 * self.eprev2) 
            self.veloutput = max(self.umin, min(self.veloutput, self.umax))
            self.PID_out = self.veloutput            
            #self.PID_out = max(self.umin, min(self.PID_out, self.umax))
        
            
        self.eprev2 = self.eprev
        self.eprev = self.error
        self.uprev = self.PID_out
        
        return self.PID_out
        
    def trackvalues(self, track=False):
        if track == True:                        
            self.controlerrormatrix.append(self.error)                        
            self.ise +=  self.error**2*self.dt
            self.iae +=  abs(self.error)*self.dt     
        
            
        
class calculatePIDparameters:
    def __init__(self, Kp, Tau, delay, KU, PU):
        self.Kp = Kp
        self.Tau = Tau
        self.delay = delay
        self.KU = KU
        self.PU = PU
        
    def zieglernicholas(self):
        KC = self.KU / 1.7
        TI = self.PU / 2.0
        TD = self.PU / 8.0
    
        return KC, TI, TD
        
    
    def tyreusluyben(self):
        KC = self.KU / 2.2
        TI = self.PU * 2.0
        TD = self.PU / 6.3
        
        return KC, TI, TD
    
    def cohencoon(self):
        KC = (self.Tau/(self.Kp*self.delay)) * ((16 + (3*self.delay/self.Tau))/12)
        TI = (self.delay * (32 + (6*self.delay/self.Tau))) / (13 + (8*self.delay/self.Tau))
        TD = (4*self.delay) / (11 + (2*self.delay/self.Tau))
        
        return KC, TI, TD
        
    
    def itaedist(self):
        KC = (1.357 * (self.delay / self.Tau) ** (-0.947)) / self.Kp
        TI = (self.Tau) / (0.842 * (self.delay / self.Tau) ** (-0.738))
        TD = self.Tau * 0.381 * (self.delay / self.Tau) ** 0.995
        
        return KC, TI, TD        
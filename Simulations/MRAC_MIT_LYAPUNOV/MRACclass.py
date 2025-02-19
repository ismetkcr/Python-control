# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 19:27:14 2024

@author: ismt
"""


class MRAC(object):
    def __init__(self, w0, gamma, tau_model, dt):
        self.gamma = gamma
        self.Krprev = w0[0]
        self.Kxprev = w0[1]
        self.model_TAU = tau_model
        self.am = -1 / self.model_TAU
        self.bm = 1 / self.model_TAU
        self.dt = dt
        self.yprev = 0
        self.ymprev = 0
        self.yfprev = 0
        self.rfprev = 0
        self.ise = 0
        self.iae = 0
        self.umin = 0
        self.umax = 125
        self.weightmatrix=[]
        self.weightmatrix.append(w0)
        self.modelerrormatrix = []
        self.controlerrormatrix = []
        
    def calculate_output(self,r, ynew, update = 'lyapunov'):
        self.unew = (self.Krprev * r) - (self.Kxprev*self.yprev)  
        self.unew = max(self.umin, min(self.unew, self.umax))
        self.ym = self.ymprev + (self.dt * (self.am*self.ymprev + self.bm*r))        
        self.model_error = ynew - self.ym
        self.control_error = r - ynew
        
        if update == 'lyapunov':
            self.Kr = self.Krprev + self.dt*(-self.gamma*r*self.model_error)
            self.Kx = self.Kxprev + self.dt*(self.gamma * ynew * self.model_error)
                        
        elif update == 'mit':
            self.rf = self.rfprev + (self.am* self.rfprev + (-self.am*r))
            self.yf = self.yfprev + (self.am* self.yfprev + (-self.am*ynew))
            self.Kr = self.Krprev + self.dt* (-self.gamma * self.rf * self.model_error)
            self.Kx = self.Kxprev + self.dt* (self.gamma * self.yf * self. model_error)
            self.rfprev = self.rf
            self.yfprev = self.yf
            
        self.Kxprev = self.Kx
        self.Krprev = self.Kr
        self.yprev = ynew
        self.ymprev = self.ym
        self.row = (self.Kr, self.Kx)
    
    def trackvalues(self, track=False):
        if track == True:
            self.weightmatrix.append(self.row)
            self.modelerrormatrix.append(self.model_error)
            self.controlerrormatrix.append(self.control_error)                        
            
        
        
        
        
        
            
            
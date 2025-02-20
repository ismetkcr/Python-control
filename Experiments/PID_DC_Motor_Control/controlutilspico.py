from ulab import numpy as np

class PIDcontroller():
    def __init__(self, dt):
        self.dt = dt
    
    def assign_PID_parameters(self, Kc, Ti, Td):
        self.Kc = Kc
        self.Ti = Ti
        self.Td = Td
        
    
    def calculate_output(self, r, y, eprev, umin, umax, uprev, s, ubackprev, PID_backprev,  antiwindup = None, tt = None ):
        error = r - y
        P_out = self.Kc * error
        D_out = self.Kc * self.Td * (error - eprev) / self.dt
        
        
        
        if antiwindup is None:
            s += (self.Kc / self.Ti) * error * self.dt
            I_out = s    
            PID_out = P_out + I_out + D_out
            uback = 0
            PID_back = 0
            
            PID_out = max(umin, min(PID_out, umax))
            
            
    
        if antiwindup == 'conditionalintegral':
            if umin < uprev < umax:
                s += (self.Kc / self.Ti) * error * self.dt
            I_out = s    
            PID_out =  P_out + I_out + D_out
            uback = 0
            PID_back = 0
            # Clamp output within [umin, umax]
            PID_out = max(umin, min(PID_out, umax))
                
                
    
        if antiwindup == 'backcalculation':
            s += ((1 / tt) * (ubackprev - PID_backprev) + (self.Kc / self.Ti) * error) * self.dt
            I_out = s    
            PID_back = P_out + I_out + D_out
            
            if PID_back <= umin:
                uback = umin
            elif PID_back >= umax:
                uback = umax
            else:
                uback = PID_back 
            
            PID_out = PID_back
            
            PID_out = max(umin, min(PID_out, umax))
            
        return PID_out, error, s, uback, PID_back
    
    
    
    
        

    
        


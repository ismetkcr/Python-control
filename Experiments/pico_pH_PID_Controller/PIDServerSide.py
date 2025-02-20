import utime
import machine
from openLooputils import ml2pwm_acid, ml2pwm_base, read_vol, vol_2_pH, customFilter
from ulab import numpy as np
from motorDrivers import LN298
from easy_comms import Easy_comms
from PIDcontrollerclass import PIDcontroller
import json
from MRACclass import MRAC

pwmpinbase  = 15
pwmpinacid = 11

pumpbase = LN298(pwmpinbase, freq=75) #baz 
pumpacid = LN298(pwmpinacid, freq=200) #asit

t = 0
dt = 0.5 #saniye
#KC, TI, TD = 32.44, 29.2, 3.53
KC, TI, TD = 20.69, 120, 5
#KC, TI, TD = 25.69, 60.02, 3

controller = PIDcontroller(dt)
controller.assignPIDparameters(KC, TI, TD)



comm = Easy_comms(0, 115200)


x_array = None
pH_f = 0
base_flow = 0
base_flowc = 0
acid_flowc = 0

pumpacid.motorpwm.duty_u16(int(0))
pumpbase.motorpwm.duty_u16(int(0))
maxpwm = 65535

while True:
    t += dt
    val = read_vol()
    pH = vol_2_pH(val)
    pH_f, x_array = customFilter(pH,x_array)
    

   
    comm_result = comm.read()
    
    if comm_result is not None:
        uc, acid_flowc = comm_result
        uc = float(uc)
        acid_flowc = float(acid_flowc)
               
    else:
       
        pass
           
        
    base_flow = controller.calculateoutput(uc, pH_f, antiwindup = 'CI', tt=None, vel=False)
    pumpacid.motorpwm.duty_u16(int(ml2pwm_acid(acid_flowc)))
    pumpbase.motorpwm.duty_u16(int(ml2pwm_base(base_flow)))
    
    data = {
    "time": round(t, 2),#buraya dikkat et.
    "pH": round(pH, 2),
    "base_flow": round(float(base_flow), 2),
    "pHF": round(pH_f,2)
    }

    json_data = json.dumps(data)
    comm.send_json_data(data)
    utime.sleep_ms(390)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    



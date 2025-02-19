# -*- coding: utf-8 -*-
"""
Created on Sat Feb  3 12:32:49 2024

@author: ismt
"""

import numpy as np
from Modelclass import TF, ParametricModel
from controlutils import  Plotter, Tablo, generateNoise, customFilter
from PIDcontrollerclass import PIDcontroller, calculatePIDparameters


dt = 0.5
dt = 0.5 
Kp = 0.2571
Tau = 52.98
delay =  6

yprev, yprev2, uprev, uprev2 = 5, 5, 0, 0
ynew = yprev
modelTF = TF(yprev, uprev)
PM = ParametricModel(yprev, uprev)

PIDparameters = calculatePIDparameters(Kp, Tau, delay, 100, 24)
KC, TI, TD = PIDparameters.tyreusluyben()
#KC, TI, TD = 50, 45, 1
controller = PIDcontroller(dt)

controller.assignPIDparameters(KC, TI, TD)


# -----------------------------------------------

#İnitialize simulation parameters
t = 0
tfinal = 3500
ft = int(tfinal/dt)

r = 7
x_array = None
yrec = np.array([yprev])
rrec = np.array([r])
trec = np.zeros((1,1))
urec = np.zeros((1,1))
errors = np.zeros((1,2))
# -----------------------------------------------
dist = 0
#start sim
for k in range(ft):
    t += dt
    tf = int('{:.0f}'.format(t))
    if tf==1000:
        r = 8.5
    elif tf ==2000:
        r = 7
    if tf == 3000:
        dist = -1
    elif tf == 3060:
        dist = 0
    
    unew = controller.calculateoutput(r, ynew, antiwindup = 'CI', tt=10, vel=False)
    
    controller.trackvalues(track=True)
    #unew = 10
    #TF output
    #ynew = modelTF.evaluate(unew) + generateNoise(-0.0001, 0.0001) + dist
    # #PM output
    ynew = PM.output(unew) + generateNoise(-0.01, 0.01) + dist
    #ynew, x_array = customFilter(ynew,x_array)               
    trec = np.append(trec, t)
    yrec = np.append(yrec, ynew)
    rrec = np.append(rrec, r)
    urec = np.append(urec, unew)
            

#  PLOT-----------------------------------------------   
#y- grafik    
plotter = Plotter(xlabel = 'time, [s]',
                  ylabel = 'out',
                  title = 'PID - CI')
plotter.addplot(trec, yrec, label = 'processout')
plotter.addplot(trec, rrec, label = 'setpoint')
plotter.show()


plotter3 = Plotter(xlabel = 'time, [s]',
                    ylabel = 'u',
                    title = 'u') 
plotter3.addplot(trec, urec, label = 'flowrate')
plotter3.show()


ise = controller.ise
iae = controller.iae    
tablo = Tablo("method"  , "ise"                , "iae")
tablo.adddata('PID', '{:.2f}'.format(ise), '{:.2f}'.format(iae))
tablo.show() 




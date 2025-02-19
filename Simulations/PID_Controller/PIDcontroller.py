# -*- coding: utf-8 -*-
"""
Created on Sat Feb  3 12:32:49 2024

@author: ismt
"""

import numpy as np
from Modelclass import TF, ParametricModel, Network
from controlutils import  Plotter, Tablo, generateNoise, customFilter
from PIDcontrollerclass import PIDcontroller, calculatePIDparameters



dt = 0.5 
# Kp = 0.09262
# Tau = 24.3
# delay =  12

def calculate_performance_metrics(time, target, yest):
    
    delta_t = np.diff(time, prepend=0)  

    # Hata hesaplaması
    error = target - yest

    # İstenen performans ölçütlerini hesaplayalım
    ise = np.sum(error**2 * delta_t)
    iae = np.sum(np.abs(error) * delta_t)
    itae = np.sum(time * np.abs(error) * delta_t)
    itse = np.sum(time * error**2 * delta_t)

    return ise, iae, itse, itae
Kp = 0.1831
Tau = 55.48
delay = 13 


yprev, yprev2, uprev, uprev2 = 6, 6, 0, 0
ynew = yprev
modelTF = TF(yprev, uprev)
PM = ParametricModel(yprev, uprev)


PIDparameters = calculatePIDparameters(Kp, Tau, delay, 125,18)
KC, TI, TD = PIDparameters.cohencoon()
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
    if tf == 2750:
        dist = -1
    elif tf == 2770:
        dist = 0
    
    unew = controller.calculateoutput(r, ynew, antiwindup = 'CI' , tt=15, vel=False)
    
    controller.trackvalues(track=True)
    #unew = 10
    #TF output
    # ynew = modelTF.evaluate(unew) + generateNoise(-0.001, 0.001) + dist
    # #PM output
    ynew = PM.output(unew) + generateNoise(-0.001, 0.001) + dist
    
    #ynew, x_array = customFilter(ynew,x_array)               
    trec = np.append(trec, t)
    yrec = np.append(yrec, ynew)
    rrec = np.append(rrec, r)
    urec = np.append(urec, unew)
            
ise, iae, itse, itae = calculate_performance_metrics(trec, rrec, yrec) 
#  PLOT-----------------------------------------------   
#y- grafik    
plotter = Plotter(xlabel = 'time, [s]',
                  ylabel = 'out',
                  title = 'PID Kontrol Model - Deney')
plotter.addplot(trec, rrec, label = 'set noktası')
plotter.addplot(trec, yrec, label = 'CC')
plotter.show()


plotter2 = Plotter(xlabel = 'time, [s]',
                    ylabel = 'Baz Akış Hızı, [ml/dk]',
                    title = 'Baz Akış Hızı, Model - Deney') 
plotter2.addplot(trec, urec, label = 'CC')
plotter2.show()




tablo = Tablo(""  , "ise", "iae", "itse", "itae")
tablo.adddata('ZNCL', '{:.2f}'.format(ise),'{:.2f}'.format(iae), '{:.2f}'.format(itse), '{:.2f}'.format(itae) )
tablo.show() 

tablo2 = Tablo("", "KC", "TI", "TD")
tablo2.adddata('ZNCL', '{:.2f}'.format(KC), '{:.2f}'.format(TI), '{:.2f}'.format(TD))
tablo2.show()


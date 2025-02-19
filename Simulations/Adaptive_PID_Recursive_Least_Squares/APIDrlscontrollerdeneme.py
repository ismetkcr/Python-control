# -*- coding: utf-8 -*-
"""
Created on Sat Feb  3 12:32:49 2024

@author: ismt
"""

import numpy as np
from controlutils import  Plotter, customFilter, Tablo, Subplotter
from RLSclass import RecursiveLeastSquares
from Modelclass import TF, ParametricModel
from PIDcontrollerclass import PIDcontroller, calculatePIDparameters
#from subplotdenemesil import Subplotter



dt = 0.5
dt = 0.5 
Kp = 0.1588
Tau = 37.95
delay =  3

yprev, yprev2, uprev, uprev2 = 5, 5, 0, 0
ynew = yprev
modelTF = TF(yprev, uprev)
PM = ParametricModel(yprev, uprev)
# -----------------------------------------------


KU = 1
PU = 1


PIDparameters = calculatePIDparameters(Kp, Tau, delay, KU, PU)
KC, TI, TD = PIDparameters.cohencoon()
controller = PIDcontroller(dt) 
controller.assignPIDparameters(KC, TI, TD)
# controller.Kc = 20
# controller.Ti = 40
# controller.Td = 2
# -----------------------------------------------

#İnitialize simulation parameters
t = 0
tfinal = 1000

eprev, eprev2  = 0, 0
uprevvel = 0

umin, umax = 0, 100
iseprev, iaeprev = 0, 0
u_bias = 0
sprev, ubackprev, PID_backprev = 0, 0, 0
ft = int(tfinal/dt)
r = 0
yrec = np.array([yprev])
rrec = np.array([r])
trec = np.zeros((1,1))
urec = uprev
errors = np.zeros((1,2))
# -----------------------------------------------

#wprev = np.random.randn(3, 1)
#a0, a1, a2 = wprev
wprev = np.array([[299, -514, 218]]).T
Pprev = 0.001 * np.eye(3)
R = 0.5 * np.eye(1) # like forgetting factor..
I = np.eye(len(wprev))
RLS = RecursiveLeastSquares(wprev, Pprev, R)
deltauprev = 0
x_array = None
rfprev = 0
#start sim
for k in range(ft):
    if k == 0:
        r = 7
    t += dt
    if t % 500 == 0:
        if r<7.2:
            r = 8
        elif r>7.2:
            r = 7
    
    
    
    rf, x_array = customFilter(r, x_array)
    
    # controller.calculateoutput(rf, yprev, antiwindup = None, tt=None, vel=False)
    # controller.trackvalues(track=True)
    # unew = controller.PID_out
    
    
    #--RLS-- direk a0, a1 ,a2 ile tahmin..
    
    error = rf - yprev
    data_matris = np.array([[error, eprev, eprev2]])    
    RLS.predict(deltauprev, data_matris)
    RLS.trackvalues(track=True)
    deltauestimated = RLS.estimated_measurement
    unewvel = uprevvel + deltauestimated
    unew = max(umin, min(unewvel, umax))    
    currentdeltau = unew - uprev     
    uprevvel = unewvel
    deltauprev = currentdeltau
    eprev2 = eprev
    eprev = error
    

    #TF output
    #ynew = modelTF.evaluate(unew) + generateNoise(-0.1, 0.1) + dist
    #PM output
    ynew = PM.output(unew) #+ generateNoise(-0.01, 0.01) + dist
    yprev = ynew 
    
    uprev2 = uprev
    uprev = unew
    
    

    
    
    #data record
    trec = np.append(trec, t)
    yrec = np.append(yrec, ynew)
    rrec = np.append(rrec, rf)
    urec = np.append(urec, unew)
    


    


  # PLOT-----------------------------------------------   

#y- grafik    
plotter = Plotter(xlabel = 'time, [s]',
                  ylabel = 'out',
                  title = 'PID.')
plotter.addplot(trec, yrec, label = 'processout')
plotter.addplot(trec, rrec, label = 'setpoint')
plotter.show()



plotter3 = Plotter(xlabel = 'time, [s]',
                   ylabel = 'u',
                   title = 'u') 
plotter3.addplot(trec, urec, label = 'flowrate')
plotter3.show()


RLS.weightmatrix = np.array(RLS.weightmatrix)
KCrec = RLS.weightmatrix[:,0]
KIrec = RLS.weightmatrix[:,1]
KDrec = RLS.weightmatrix[:,2]
plotter2 = Subplotter(4)
plotter2.addsubplot([trec], [KCrec], title='a0', xlabel='Time', ylabel='a 0')
plotter2.addsubplot([trec], [KIrec], title='a1', xlabel='Time', ylabel='a 1')
plotter2.addsubplot([trec], [KDrec], title='a2', xlabel='Time', ylabel='a 2')
plotter2.show()


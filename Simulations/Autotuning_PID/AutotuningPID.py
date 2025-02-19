# -*- coding: utf-8 -*-
"""
Created on Sat Feb  3 12:32:49 2024

@author: ismt
"""

import numpy as np

from controlutils import ( calculatePIDparameters, relayoutput,
                          checkgrad,collectedmatris, 
                          update_PIDparameters,  customFilter,
                          generateNoise, Plotter, Tablo, lowpass_filter_single_value)



import numpy as np
from Modelclass import TF, ParametricModel
from controlutils import  (Plotter, Tablo, generateNoise, customFilter, checkgrad, relayoutput,update_PIDparameters,
generateNoise)
from PIDcontrollerclass import PIDcontroller, calculatePIDparameters
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

dt = 0.5 
Kp = 0.09262
Tau = 24.3
delay =   7 


# Kp = 0.2104
# Tau = 37.92
# delay =   9 


yprev, yprev2, uprev, uprev2 = 6, 6, 0, 0
ynew = yprev
modelTF = TF(yprev, uprev)
PM = ParametricModel(yprev, uprev)


PIDparameters = calculatePIDparameters(Kp, Tau, delay, 125,18)
KC, TI, TD = PIDparameters.cohencoon()
#KC, TI, TD = 50, 45, 1
controller = PIDcontroller(dt)

controller.assignPIDparameters(KC, TI, TD)


r = 7
umin, umax = 0, 125
yf, yfprev = 0, 0
yrec = np.array([yprev])
yfrec = np.array([yfprev])
rrec = np.array([r])
trec = np.zeros((1,1))
urec = np.zeros((1,1))
errors = np.zeros((1,2))

#tuning states
pastValues = None
mtrec = None
ttrec = None
x_array = None
last_peak_value = None
last_peak_time = None
founded_peak = 0
ft = int(3500/dt)
t = 0
number = 0
dist = 0

peaktimematris = []
peakvaluematris = []
ytunematris = np.empty(0)
utunematris = np.empty(0)
tuneMode = True
bias = 0.125
#start sim
for k in range(ft):
    t += dt
    tf = int('{:.0f}'.format(t))
    if tf==1000:
        r = 8.5
    elif tf ==2000:
        r = 7
    if tf == 2750:
        dist = -5
    elif tf == 2770:
        dist = 0
    yf, x_array = customFilter(yprev, x_array)
    #controller output
    if tuneMode == False:
        controller.calculateoutput(r, yprev, antiwindup='CI', tt=None, vel=False)
        controller.trackvalues(track=True)
        unew = controller.PID_out
        #error = controller.error
        # ytunematris = np.empty(0) # sürekli çalışırken açılacak..
        # utunematris = np.empty(0)
        #mtrec ile ttrec matrislerinin temizlenmesi lazım..
        #peakvaluematris, peaktimematrisin temizlenmesi lazım..
    if tuneMode == True:
        unew, error, s, uback, PID_back = relayoutput(r, yprev, umin, umax, bias, uprev)
        mtrec, ttrec, last_peak_value, last_peak_time, founded_peak = checkgrad(yf, yfprev, yprev, dt, number, t, mtrec, ttrec, last_peak_value, last_peak_time, founded_peak)        
        peaktimematris = collectedmatris(last_peak_time, peaktimematris)
        peakvaluematris = collectedmatris(last_peak_value, peakvaluematris)
        ytunematris = np.append(ytunematris ,yprev)
        utunematris = np.append(utunematris, unew)
        
        if founded_peak == 15:
            KC, TI, TD, tuneMode = update_PIDparameters(peakvaluematris, peaktimematris, umin, umax, ytunematris, utunematris,
                                                        method='zieglernicholas')
            tuneMode = False
            # KC, TI, TD = 52, 15 , 2.5
            controller.assignPIDparameters(KC, TI, TD)
    
    #-------------TF model output ----------
    #TF output
    #ynew = modelTF.evaluate(unew) + generateNoise(-0.0001, 0.0001) 
    # #PM output
    ynew = PM.output(unew) + dist + generateNoise(-0.001, 0.001) 
    
   
    
    #Assign new states
    #eprev = error
    uprev = unew
    yprev = ynew
    yfprev = yf
    
        
    #data record
    trec = np.append(trec, t)
    yrec = np.append(yrec, ynew)
    yfrec = np.append(yfrec, yf)
    rrec = np.append(rrec, r)
    urec = np.append(urec, unew)
            

#  ------------------------------PLOT----------------------------------------------- 

ise, iae, itse, itae = calculate_performance_metrics(trec, rrec, yrec) 


# plotter = Plotter(xlabel = 'time, [s]',
#                   ylabel = 'pH',
#                   title = 'time-pH')
# plotter.addplot(trec, rrec, label = 'set noktası')
# plotter.addplot(trec, yrec, label = 'ZNCL')

# #plotter.addplot(trec, yfrec, label = 'yf')
# #plt.scatter(peaktimematris, peakvaluematris)# peak kaçarsa başıma bela olabilir..
# plotter.show()

# plotter2 = Plotter(xlabel = 'time, [s]',
#                     ylabel = 'Baz Akış Hızı, [ml/dk]',
#                     title = 'Baz Akış Hızı')
# plotter2.addplot(trec,urec, label ='Baz Akış Hızı ZNCL')
# plotter2.show()
# # -----------------------------------------------to table


# # -----------------------------------------------

# tablo = Tablo(""  , "ise", "iae", "itse", "itae")
# tablo.adddata('ZNCL', '{:.2f}'.format(ise),'{:.2f}'.format(iae), '{:.2f}'.format(itse), '{:.2f}'.format(itae) )
# tablo.show() 



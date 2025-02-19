# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 19:26:41 2024

@author: ismt
"""
import numpy as np
from Modelclass import TF, ParametricModel
from controlutils import  Plotter, Tablo, generateNoise, calculate_performance_metrics
from MRACclass import MRAC



dt = 0.5 
Kp = 0.09262
Tau = 24.3   
delay = 7 


yprev, yprev2, uprev, uprev2 = 5, 5, 0, 0
ynew = yprev
modelTF = TF(yprev, uprev)
PM = ParametricModel(yprev, uprev)

a = -1/Tau
b = Kp/Tau

t = 0
tfinal = 7500

model_TAU = 20
am = -1 / model_TAU
bm = 1 / model_TAU

ymprev = 0
Krprev = 0
Kxprev = 0
Kxprev = -(am-a)/b
Krprev = (bm/b)


gamma = 0.1
r = 7
yrec = np.array([yprev])
rrec = np.array([r])
trec = np.zeros((1,1))
urec = np.zeros((1,1))
ymrec = np.array([ymprev])
ft = int(tfinal/dt)

#w0 = 5.163424124513619, -2.618677042801557
# w0 = 76.38993149931426, 69.08707136434387
w0 = 0, 0
dist = 0
controller = MRAC(w0, gamma, model_TAU, dt)

for k in range(ft):
    if k == 0:
        r = 7
    t += dt
    if t == 1500:
        r = 7
    if t == 2000:
        r = 8.5
    
    if t == 3000:
        r = 7
    
    if t == 3750:
        dist = -5
    elif t == 3770:
        dist = 0
    if t == 5000:
        r = 8
    if t == 6000:
        r = 7
    
   
    controller.calculate_output(r, yprev, update = 'lyapunov')
    controller.trackvalues(track=True)
    unew = controller.unew
    #unew = max(0, min(unew, 125))
    #TF output
    # ynew = modelTF.evaluate(unew)
    ynew = PM.output(unew) + generateNoise(-0.001, 0.001) + dist

    yprev = ynew
        
    trec = np.append(trec, t)
    yrec = np.append(yrec, ynew)
    rrec = np.append(rrec, r)
    urec = np.append(urec, unew)
    ymrec = np.append(ymrec, controller.ym) 
        
# -- PLOT --    
controller.weightmatrix = np.array(controller.weightmatrix)
Krrec, Kxrec = controller.weightmatrix[:,0], controller.weightmatrix[:,1]
ise, iae, itse, itae = calculate_performance_metrics(trec, rrec, yrec) 

#y-ym-r grafik    
plotter = Plotter(xlabel = 'zaman, [s]',
                  ylabel = 'pH',
                  title = f'mrac-lyap, gamma = {gamma}')
plotter.addplot(trec, rrec, label = 'set noktası')
plotter.addplot(trec, ymrec, label= 'model çıkış değeri')
plotter.addplot(trec, yrec, label='pH')

plotter.show()
    
plotter3 = Plotter(xlabel = 'zaman, [s]',
                    ylabel = 'Baz Akış Hızı, [ml/dk]',
                    title = f'Baz Akış Hızı, gamma = {gamma}') 
plotter3.addplot(trec, urec, label = 'Baz Akış Hızı')
plotter3.show()   

#Kr - Kx grafik
plotter2 = Plotter(xlabel = 'Zaman, [s]',
                    ylabel = 'Kontrol Parametreleri',
                    title = f'Kontrol Edici Parametreleri, gamma = {gamma}')
plotter2.addplot(trec,Krrec, label = 'Kr')
plotter2.addplot(trec,Kxrec, label = 'Kx')
plotter2.show()    

tablo = Tablo("gamma"  , "ise", "iae", "itse", "itae")
tablo.adddata('{:.4f}'.format(gamma), '{:.2f}'.format(ise),'{:.2f}'.format(iae), '{:.2f}'.format(itse), '{:.2f}'.format(itae) )
tablo.show() 

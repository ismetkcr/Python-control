# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 19:26:41 2024

@author: ismt
"""
import numpy as np
from controlutils import  Plotter, Tablo, generateNoise
from MRACclass import MRAC
from Modelclass import TF, ParametricModel

dt = 0.5 # bunu farklı yerden vermeyi düşüneceğim..
#--------------construct model with TF-----------
dt = 0.5
Kp = 0.1285
Tau = 26.54
delay = 7

#--------------construct model with TF-----------



yprev, yprev2, uprev, uprev2 = 5, 5, 0, 0

ynew = yprev
modelTF = TF(yprev, uprev)
PM = ParametricModel(yprev, uprev)


a = -1/Tau
b = Kp/Tau


t = 0
tfinal = 4500

model_TAU = 20
am = -1 / model_TAU
bm = 1 / model_TAU





ymprev = 5
rfprev = 0
yfprev = 0

r = 7
yrec = np.array([yprev])
rrec = np.array([r])
trec = np.zeros((1,1))
urec = np.zeros((1,1))
ymrec = np.array([ymprev])


ft = int(tfinal/dt)

Kr, Kx = 25.410351928364168, 20
#Kr, Kx = 145.20546, 137.9052174267673
#Kr, Kx = 0, 0
P = 1 #from lyap
Gamma = 50
Wunc_proces = np.array([[0.1], [0.05]]) * 0.0
M = 50
dist = 0
What_app = np.random.randn(M, 1)*5
kernels = np.random.randint(-10, 11, size=(M, 1))
weights = np.random.rand(M, 1) * 1

def unc_proces(W, x):
    beta = np.array([[x**3], [np.sin(x)]])
    return W.T @ beta


def unc_handle(Wapp, weights, x):
    app_func = np.exp(-weights *  (np.abs(x+kernels))**2)
    return  Wapp.T @ app_func, app_func

for k in range(ft):
    if k == 0:
        r = 7
    t += dt
    if t == 1500:
        r = 7
    if t == 2000:
        r = 8

    if t == 3000:
        r = 7

    if t == 3750:
        dist = -5
    elif t == 3770:
        dist = 0

    u_n = Kr*r - Kx*yprev
    u_hand, app_func = unc_handle(What_app, weights, yprev)
    unew = u_n - u_hand
    unew = float(unew)
    unew = max(0, min(unew, 100))

    What_app += dt*((Gamma*(yprev-ymprev)*P*b) * app_func ) ;

    #model output
    ym = ymprev + dt*(am*ymprev + bm*r)

    #system output
    system_unc = unc_proces(Wunc_proces, yprev)

    #ynew = modelTF.evaluate(unew)
    ynew = PM.output(unew + float(system_unc)) + generateNoise(-0.001, 0.001) +dist
    ynew = float(ynew)


    #modelTF.TF.evaluate(dt,unew)
    #ynew = modelTF.TF.ynew
    yprev = ynew
    ymprev = ym

    trec = np.append(trec, t)
    yrec = np.append(yrec, ynew)
    rrec = np.append(rrec, r)
    urec = np.append(urec, unew)
    ymrec = np.append(ymrec, ym)

# -- PLOT --


#y-ym-r grafik
plotter = Plotter(xlabel = 'time, [s]',
                  ylabel = 'out',
                  title = 'mrac-lyap')
plotter.addplot(trec, yrec, label = 'processout')
plotter.addplot(trec, rrec, label = 'setpoint')
plotter.addplot(trec, ymrec, label= 'modelout')
plotter.show()



plotter3 = Plotter(xlabel = 'time, [s]',
                   ylabel = 'u',
                   title = 'u')
plotter3.addplot(trec, urec, label = 'flowrate')
plotter3.show()





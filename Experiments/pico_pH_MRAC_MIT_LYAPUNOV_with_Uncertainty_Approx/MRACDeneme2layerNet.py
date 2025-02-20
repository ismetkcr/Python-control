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



yprev, yprev2, uprev, uprev2 = 3, 0, 0, 0

ynew = yprev
modelTF = TF(yprev, uprev)
PM = ParametricModel(yprev, uprev)


a = -1/Tau
b = Kp/Tau


t = 0
tfinal = 4000

model_TAU = 20
am = -1 / model_TAU
bm = 1 / model_TAU





ymprev = 0
rfprev = 0
yfprev = 0

r = 7
yrec = np.array([yprev])
rrec = np.array([r])
trec = np.zeros((1,1))
urec = np.zeros((1,1))
ymrec = np.array([ymprev])


ft = int(tfinal/dt)

#Kr, Kx = 5.163424124513619, -2.618677042801557 # kr = 2.91, Kx = 1.92
# Kr, Kx = 16.504009880668733, 9.18104387520711
Kr, Kx = 0, 0
P = 1 #from lyap


Wunc_proces = np.array([[0.1], [0.05]]) * 0.0
M = 30
W1 = np.random.randn(M)
b1 = np.random.randn(M)
W2 = np.random.randn(M)
b2 = 0
regularization = 0.0001
learning_rate = 0.0001
def unc_proces(W, x):
    beta = np.array([[x**3], [np.sin(x)]])
    return W.T @ beta

def forward(X, W1, b1, W2, b2):
    X = np.array(X)
    #Z = 1 / (1 + np.exp(-(X.dot(W1) + b1))) #sigmoid
    #Z = np.tanh(X.dot(W1) + b1) #tanh
    Z = X.dot(W1) + b1 #relu
    Z = Z * (Z > 0) #relu

    Y = Z.dot(W2) + b2
    return Z, Y

def derivative_W2(Z, Y, Yhat):
    err = np.array([Y-Yhat])
    return err*(Z)

def derivative_b2(Y, Yhat):
    err = np.array([Y-Yhat])
    return (err)

def derivative_W1(X, Z, Y, Yhat, W2):
    X = np.array([X])
    #dZ = np.outer(Y-Yhat, W2) * Z * (1 - Z) #sigmoid activation grad
    #dZ = np.outer(Y-Yhat, W2) * (1 - Z * Z) #tanh activation grad
    dZ = np.outer(Y-Yhat, W2) * (Z > 0) # relu activation grad
    return X.T.dot(dZ)

def derivative_b1(Z, Y, Yhat, W2):
    #dZ = np.outer(Y-Yhat, W2) * Z * (1 - Z) #sigmoid activation grad
    #dZ = np.outer(Y-Yhat, W2) * (1 - Z * Z) #tanh activation grad
    dZ = np.outer(Y-Yhat, W2) * (Z > 0) # relu activation grad
    return dZ.sum(axis=0)

for k in range(ft):
    if k == 0:
        r = 7
    t += dt
    if t == 500:
        r = 7
    if t == 1000:
        r = 7

    u_n = Kr*r - Kx*yprev
    Z, Y = forward(yprev, W1, b1, W2, b2)
    u_hand = Y
    #u_hand = 0
    unew = u_n - u_hand
    unew = float(unew)
    unew = max(0, min(unew, 100))

    W2 += learning_rate * derivative_W2(Z, yprev, ymprev) - regularization * np.abs(W2)
    b2 += learning_rate * derivative_b2(yprev, ymprev) - regularization * np.abs(b2)
    W1 += learning_rate * derivative_W1(yprev, Z, yprev, ymprev, W2) - regularization * np.abs(W1)
    b1 += learning_rate * derivative_b1(Z, yprev, ymprev, W2) - regularization * np.abs(b1)

    #model output
    ym = ymprev + dt*(am*ymprev + bm*r)

    #system output
    system_unc = unc_proces(Wunc_proces, yprev)



    #ynew = modelTF.evaluate(unew)
    ynew = PM.output(unew + float(system_unc)) + generateNoise(-0.01, 0.01)
    ynew = float(ynew)

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



































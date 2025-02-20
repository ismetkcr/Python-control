# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 19:26:41 2024

@author: ismt
"""
import numpy as np
from Modelclass import TF, ParametricModel
from controlutils import  Plotter, Tablo, generateNoise, calculate_performance_metrics
from MRACclass import MRAC
from MRACUNCclass import Lyap_UNC, Radial_UNC, ANN_UNC


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
tfinal = 2500

model_TAU = 20
am = -1 / model_TAU
bm = 1 / model_TAU

ymprev = 5
Krprev = 0
Kxprev = 0
Kxprev = -(am-a)/b
Krprev = (bm/b)



r = 7
yrec = np.array([yprev])
rrec = np.array([r])
trec = np.zeros((1,1))
urec = np.zeros((1,1))
uhrec = np.zeros((1,1))
unrec = np.zeros((1,1))


ymrec = np.array([ymprev])
ft = int(tfinal/dt)


ft = int(tfinal/dt)
#Kr, Kx = 0, 0
#⌡Kr, Kx = 145.20546, 137.9052174267673
Kr, Kx = 23.745411358237963, 16.151392787734831
w0 = Kr, Kx
gamma = 0.00
gamma_uncl = 0.00001
gamma_uncr = 1
gamma_unca = 0.05

dist = 0
controller = MRAC(w0, gamma, model_TAU, dt, ymprev)
dist = 0
M = 30
Wunc_proces = np.array([[0.000], [0.0]]) * 0
#UNC = Lyap_UNC(gamma_uncl)
#UNC = Radial_UNC(gamma_uncr, M)
UNC = ANN_UNC(gamma_unca, M)
def unc_proces(W, x):
    beta = np.array([[x**3], [np.sin(x)]])
    return W.T @ beta

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
        dist = -1
    elif t == 3770:
        dist = 0
    if t == 5000:
        r = 8.5
    if t == 6000:
        r = 7
    
    unominal = controller.calculate_output(r, yprev, update = 'lyapunov')
    controller.trackvalues(track=True)
    #uhand = UNC.calculate_uhand(yprev, unominal) # Lyapunov
    uhand = UNC.calculate_uhand(yprev) # Radial, ANN

    
    
    What = UNC.update_weights(yprev, ymprev)
    unew = float(unominal - uhand)
    unew = max(0, min(unew, 125))
    #system unc
    system_unc = unc_proces(Wunc_proces, ynew)
    #unew = max(0, min(unew, 125))
    #TF output
    # ynew = modelTF.evaluate(unew)
    ynew = PM.output(unew + float(system_unc)) + generateNoise(-0.001, 0.001) +dist
    ym = controller.ym
   
    
    
    
            
    #TF output    
    #ynew = modelTF.evaluate(unew + float(system_unc))
    
    #PM output
    
    
    yprev = ynew    
    ymprev = ym
        
    trec = np.append(trec, t)
    yrec = np.append(yrec, ynew)
    rrec = np.append(rrec, r)
    urec = np.append(urec, unew)
    ymrec = np.append(ymrec, ym)
    uhrec = np.append(uhrec, uhand)
    unrec = np.append(unrec, unominal) 

        
# -- PLOT --    

# weightmatrix_array = np.vstack(UNC.weightmatrix)
# w1 = weightmatrix_array[:, 0]
# w2 = weightmatrix_array[:, 1]
# w3 = weightmatrix_array[:, 2]
# w4 = weightmatrix_array[:, 3]
# w5 = weightmatrix_array[:, 4]
# w6 = weightmatrix_array[:, 5]
#w7 = weightmatrix_array[:, 6]
ise, iae, itse, itae = calculate_performance_metrics(trec, rrec, yrec)
controller.weightmatrix = np.array(controller.weightmatrix) 
Krrec, Kxrec = controller.weightmatrix[:,0], controller.weightmatrix[:,1]

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
plotter3.addplot(trec, urec, label = 'U_aug')
plotter3.addplot(trec, unrec, label = 'U_nominal')
plotter3.addplot(trec, uhrec, label = 'U_handle')


plotter3.show()  

plotter2 = Plotter(xlabel = 'Zaman, [s]',
                    ylabel = 'Kontrol Parametreleri',
                    title = f'Kontrol Edici Parametreleri, gamma = {gamma}')
plotter2.addplot(trec,Krrec, label = 'Kr')
plotter2.addplot(trec,Kxrec, label = 'Kx')
plotter2.show()   

tablo = Tablo("gamma"  , "ise", "iae", "itse", "itae")
tablo.adddata('{:.4f}'.format(gamma), '{:.2f}'.format(ise),'{:.2f}'.format(iae), '{:.2f}'.format(itse), '{:.2f}'.format(itae) )
tablo.show() 

    

# -*- coding: utf-8 -*-
"""
Created on Sun Jul  7 19:55:47 2024

@author: ismt
"""
import numpy as np
from utils import (generate_random_steps, calculate_performance_metrics, ProcessModel, Plotter)
from RLSclass import RecursiveLeastSquares

def sigmoid(A):
    return 1 / (1 + np.exp(-A))

Model = ProcessModel(3, 1.12)
wprev = np.array([[0, 0, 0]]).T
Pprev = 1 * np.eye(3)
R = 0.998 * np.eye(1)
rls = RecursiveLeastSquares(wprev, Pprev, R)
CB_minus_1 = 1.12
CB_minus_2 = 1.12
CB_minus_3 = 1.12
F_minus_1 = 34.3
dt = 1
#dt = 1

r = 1.245
v_k_1 = 0
v_k_2 = 0
ksi = 2
learning_rate = 0.2
I_inc = 1.0001
I_dec = 0.9995
threshold = 1
step = 0
filter_param = sigmoid(ksi)
CB_list = []
F_list = []
y_hat_jitl_list = []
y_hat_rls_list = []
step_list = []
model_error_list = []
filter_param_list = []
r_list = []
K = 0.05
print(filter_param)
prev_J = None

for k in range(2000):
    CB = Model.model_output(F_minus_1)    
    # RLS system identification
    data_matris = np.array([[CB_minus_2, CB_minus_1, F_minus_1]]).flatten()
    y_hat = rls.predict(CB, data_matris).flatten()
    a2, a1, b1 = rls.wnew
    
    #calculate u
    model_error = CB - y_hat
    v = r - (model_error)
    F = (filter_param * F_minus_1) + ((1 - filter_param) / (b1)) * (v - (a1 * v_k_1) - (a2 * v_k_2))
    F = float(F)
    F = max(0 , min(F, 100))
    
    # update filter_param with gradient descent method
    grad_djdu =  (-2.0*(r - y_hat) * b1) +  (F - F_minus_1) * 2 * K
    grad_dudfilt = F_minus_1 - ((v - (a1 * v_k_1) - (a2 * v_k_2)) / b1)
    grad_dfiltdksi = filter_param * (1 - filter_param)
    grad_dksidt = grad_djdu * grad_dudfilt * grad_dfiltdksi
    
    J = np.square([r - y_hat]) + K * np.square([F - F_minus_1])
    
    if prev_J is not None:
        delta_J = J - prev_J
        if delta_J > threshold:
            learning_rate *= I_dec
        elif 0 < delta_J <= threshold:
            ksi -= learning_rate * grad_dksidt * dt
        elif delta_J <= 0:
            if abs(delta_J) < threshold:
                ksi -= learning_rate * grad_dksidt * dt
                learning_rate *= I_inc
            
           
    #print(J)
    
    # update states
    filter_param = sigmoid(ksi) 
    CB_minus_3 = CB_minus_2
    CB_minus_2 = CB_minus_1
    CB_minus_1 = CB
    F_minus_1 = F
    v_k_2 = v_k_1
    v_k_1 = v
    prev_J = J
    step = step + 1
    
    CB_list.append(CB)
    # y_hat_jitl_list.append(y_hat)
    y_hat_rls_list.append(y_hat)
    step_list.append(step)
    filter_param_list.append(filter_param)
    model_error_list.append(model_error)
    r_list.append(r)
    F_list.append(F)
    
# Plot model output, JITL and RLS predictions
plotter = Plotter(xlabel='iter', ylabel='output', title='Model and Predict Comparison')
plotter.addplot(step_list, CB_list, label='model_output')
# plotter.addplot(step_list, y_hat_jitl_list, label='y_hat_jitl')
plotter.addplot(step_list, y_hat_rls_list, label='y_hat_rls')
plotter.show(time=[0, 2000])    
    
plotter = Plotter(xlabel='iter', ylabel='output', title='AIMC')
plotter.addplot(step_list, CB_list, label='model_output')
plotter.addplot(step_list, r_list, label='set_point')
plotter.show(time=[0, 2000])        

plotter = Plotter(xlabel='iter', ylabel='output', title='F')
plotter.addplot(step_list, F_list, label='F')
plotter.show(time=[0, 2000])        

plotter = Plotter(xlabel='iter', ylabel='filter_param', title='filter_param')
plotter.addplot(step_list, filter_param_list, label='Filter')
plotter.show(time=[0, 2000])  

print('learning_Rate',learning_rate)
print('filter_param',filter_param)
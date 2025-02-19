import numpy as np
from utils import (generate_random_steps, calculate_performance_metrics,ProcessModel, Plotter)
from JITL_class import JITL
from RLSclass import RecursiveLeastSquares

Model = ProcessModel(3, 1.12)
jitl = JITL(1.12, 34.3)
wprev = np.array([[0, 0, 0]]).T
Pprev = 1000 * np.eye(3)
R = 1 * np.eye(1) 
rls = RecursiveLeastSquares(wprev, Pprev, R)

CB_list = []
y_hat_jitl_list = []
y_hat_rls_list = []
step_list = []
error_jitl_list = []
error_rls_list = []

cumulative_error_jitl = 0
cumulative_error_rls = 0

F = generate_random_steps(length=5005, min_step=40, max_step=120, switch_prob=0.01)
step = 0
CB_minus_1 = 1.12
CB_minus_2 = 1.12
CB_minus_3 = 1.12
F_minus_1 = 34.3

for k in range(1000):
    CB = Model.model_output(F[k])
    data_matris = np.array([[CB_minus_2, CB_minus_1, F_minus_1]])
    y_hat_rls = rls.predict(CB, data_matris).flatten()
    y_hat_jitl = jitl.predict(CB, F[k])
    
    error_jitl = np.abs(CB - y_hat_jitl)[0]
    error_rls = np.abs(CB - y_hat_rls)[0]
    
    cumulative_error_jitl += error_jitl
    cumulative_error_rls += error_rls
    
    CB_minus_3 = CB_minus_2
    CB_minus_2 = CB_minus_1
    CB_minus_1 = CB
    F_minus_1 = F[k]
    step = step + 1
  
    if step % 100 == 0:
        print(f"Iteration {step}: Cumulative error_jitl = {cumulative_error_jitl:.6f}, Cumulative error_rls = {cumulative_error_rls:.6f}")
    
    CB_list.append(CB)
    y_hat_jitl_list.append(y_hat_jitl)
    y_hat_rls_list.append(y_hat_rls)
    step_list.append(step)
    error_jitl_list.append(error_jitl)
    error_rls_list.append(error_rls)
    
# Plot model output, JITL and RLS predictions
plotter = Plotter(xlabel='iter', ylabel='output', title='JITL and RLS Comparison')
plotter.addplot(step_list, CB_list, label='model_output')
plotter.addplot(step_list, y_hat_jitl_list, label='y_hat_jitl')
plotter.addplot(step_list, y_hat_rls_list, label='y_hat_rls')
plotter.show(time = [50, 1000])

# Plot model input
plotter2 = Plotter(xlabel='iter', ylabel='u', title='Input')
plotter2.addplot(step_list, F[:step], label='u')
plotter2.show(time = [50, 1000])

# Plot individual errors (not cumulative)
plotter3 = Plotter(xlabel='iter', ylabel='error', title='JITL and RLS Errors')
plotter3.addplot(step_list, error_jitl_list, label='JITL error')
plotter3.addplot(step_list, error_rls_list, label='RLS error')
plotter3.show(time = [50, 1000])

isej, iaej, itsej, itaej = calculate_performance_metrics(step_list, CB_list, y_hat_jitl_list)
iser, iaer, itser, itaer = calculate_performance_metrics(step_list, CB_list, y_hat_rls_list)
print("JITL Performance Metrices:")
print(f"ISE:  {isej:.4f}")
print(f"IAEJ  {iaej:.4f}")
print(f"ITSEJ {itsej:.4f}")
print(f"ITAE: {itaej:.4f}")

print("\nRLS Performance Metrices:")
print(f"ISE:  {iser:.4f}")
print(f"IAE:  {iaer:.4f}")
print(f"ITSE: {itser:.4f}")
print(f"ITAE: {itaer:.4f}")

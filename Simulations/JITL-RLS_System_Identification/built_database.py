# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 10:03:02 2024

@author: ismt
"""

import matplotlib.pyplot as plt
import random
import numpy as np

def generate_random_steps(length=5005, min_step=10, max_step=150, switch_prob=0.1):
    steps = []
    current_step = random.randint(min_step, max_step)
    
    for _ in range(length):
        if random.random() < switch_prob:
            current_step = random.randint(min_step, max_step)
        steps.append(current_step)
    
    return steps

k1, k2, k3 = 50, 100, 10
CA_f = 10
V = 1
F = 34.3 # to compute nominal values..
random_steps = generate_random_steps() # to build data_set
#random_steps = generate_random_steps(length=2001, min_step=40, max_step=120, switch_prob=0.01) # to build data_set

# CA, CB = 0, 0 # to compute nominal values.
CA, CB = 3, 1.12 # nominal values
CA_list = [CA]
CB_list = [CB]
F_list = [random_steps[0]]  # Initialize F_list with the first F value
dt = 0.00001
steps = 0
st_list = [steps]
for k in range(5000):
    F = random_steps[k]
    dCA_dt = -k1 * CA - (k3 * (CA ** 2)) + ((F / V) * (CA_f - CA))
    dCB_dt = (k1 * CA) - (k2 * CB) - ((F / V) * CB)
    CA += (dCA_dt) * dt
    CB += (dCB_dt) * dt
    
    steps += 1
    CA_list.append(CA)
    CB_list.append(CB)
    F_list.append(F)  # Append F to F_list
    st_list.append(steps)

# Create DataList z(k-1) = [CB(k-1), CB(k-2), F(k-1) ].T

z_list = []
for k in range(2, len(CB_list)):
    z_k_minus_1 = [CB_list[k-2], CB_list[k-1], F_list[k-1]]
    z_list.append(z_k_minus_1)
    
z_list = np.array(z_list)
print(z_list.shape)  # Should print (1999, 3)
zT_list = z_list.T
print("transposeZ shape" , zT_list.shape)

database = []
for k in range(2, len(CB_list)):
    database_entry = [CB_list[k], z_list[k-2][0], z_list[k-2][1], z_list[k-2][2]]
    database.append(database_entry)

database = np.array(database)
print(database.shape)
database_T = database.T
print("transposeD shape" , database_T.shape)

#save database
np.save('database.npy', database)


plt.plot(st_list, CB_list)
plt.figure()
plt.plot(st_list, F_list)











import numpy as np
import matplotlib.pyplot as plt
from RLSclass import RecursiveLeastSquares


# True value of the parameters that will be estimated 
initialPosition = 10
initialVelocity = -2
acceleration = 5
noisestd = 3

wprev = np.random.randn(3, 1) #random değerler copy ile hesaplanmalı
Pprev = 100 * np.eye(3)
R = 1 * np.eye(1)
I = np.eye(len(wprev))
position_matrix = []

# Simulation time
simulationTime = np.linspace(0, 15, 2000)

# Create a Recursive Least Squares object
RLS = RecursiveLeastSquares(wprev, Pprev, R)

for i in simulationTime[:500]:
    data_matris = np.array([[1, i, (i**2) / 2]])
    current_measurement = initialPosition + (initialVelocity * i) + (acceleration * i**2) / 2
    positionNoise = current_measurement + noisestd * np.random.randn(1)
    RLS.predict(positionNoise, data_matris)
    RLS.trackvalues(track=True)
    position_matrix.append(positionNoise)

# Plotting the results
estimated_positions = [estimate[0][0] for estimate in RLS.estimated_measurements]
initPositionestimates = [estimate[0][0] for estimate in RLS.weightmatrix]
initVelocityestimates = [estimate[1][0] for estimate in RLS.weightmatrix]
accestimates = [estimate[2][0] for estimate in RLS.weightmatrix]


plt.figure(figsize=(10, 6))
plt.plot(simulationTime[1:500], position_matrix[1:500], label='Gerçek Değerler')
plt.plot(simulationTime[1:500], estimated_positions[1:500], label='Tahmin Edilen Değerler')
plt.xlabel('Zaman')
plt.ylabel('Pozisyon')
plt.title('Gerçek ve Tahmin Edilen Pozisyonlar')
plt.legend()
plt.grid(True)
plt.show()


plt.figure(figsize=(10, 6))

# Initial Position Estimates
plt.subplot(3, 1, 1)
plt.plot(simulationTime[1:500], initPositionestimates[1:500], label='Initial Position Estimates')
plt.plot(simulationTime[1:500], [initialPosition]*499, 'r--', label='True Initial Position')
plt.xlabel('Time')
plt.ylabel('Position')
plt.title('Initial Position Estimates')
plt.legend()
plt.grid(True)

# Initial Velocity Estimates
plt.subplot(3, 1, 2)
plt.plot(simulationTime[1:500], initVelocityestimates[1:500], label='Initial Velocity Estimates')
plt.plot(simulationTime[1:500], [initialVelocity]*499, 'r--', label='True Initial Velocity')
plt.xlabel('Time')
plt.ylabel('Velocity')
plt.title('Initial Velocity Estimates')
plt.legend()
plt.grid(True)

# Acceleration Estimates
plt.subplot(3, 1, 3)
plt.plot(simulationTime[1:500], accestimates[1:500], label='Acceleration Estimates')
plt.plot(simulationTime[1:500], [acceleration]*499, 'r--', label='True Acceleration')
plt.xlabel('Time')
plt.ylabel('Acceleration')
plt.title('Acceleration Estimates')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()


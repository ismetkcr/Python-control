# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 10:52:50 2024

@author: ismt
"""

import random
import numpy as np
import matplotlib.pyplot as plt


class ProcessModel(object):
    def __init__(self, CA_0, CB_0):
        self.dt = 0.0001
        self.k1 = 50
        self.k2 = 100
        self.k3 = 10
        self.V =  1
        self.CA = CA_0
        self.CB = CB_0
        self.CA_f = 10 
    def model_output(self, F):
        dCA_dt = -self.k1 * self.CA - (self.k3 * (self.CA ** 2)) + ((F / self.V) * (self.CA_f - self.CA))
        dCb_dt = (self.k1 * self.CA) - (self.k2 * self.CB) - ((F / self.V) * self.CB)
        self.CA += (dCA_dt)*self.dt
        self.CB += (dCb_dt)*self.dt
        
        return self.CB
        

# TO GENERATE DATA BASE..         
def generate_random_steps(length=2001, min_step=10, max_step=150, switch_prob=0.1):
    steps = []
    current_step = random.randint(min_step, max_step)
    
    for _ in range(length):
        if random.random() < switch_prob:
            current_step = random.randint(min_step, max_step)
        steps.append(current_step)
    
    return steps


class Plotter:
    def __init__(self, xlabel='X Ekseni', ylabel='Y Ekseni', title=None):
        self.x_data = []
        self.y_data = []
        self.labels = []
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.title = title
        plt.style.use('seaborn-dark')  

    def addplot(self, x, y, label=None):
        """
        Verilen x ve y verilerini, belirtilen etiketle birlikte grafik üzerine çizer.

        Parametreler:
        x (list): x eksenindeki değerlerin listesi.
        y (list): y eksenindeki değerlerin listesi.
        label (str, optional): Veri setinin etiketi. Varsayılan olarak None.

        Dönüş:
        None
        """
        self.x_data.append(x)
        self.y_data.append(y)
        self.labels.append(label)

    def show(self, time=None):
        """
        Önceden eklenen tüm veri setlerini tek bir grafik üzerine çizer.

        Parametreler:
        time (list, optional): x ekseninin çizdirileceği zaman aralığı. 
                              Varsayılan olarak None (tüm veri setini çizer).

        Dönüş:
        None
        """
        plt.figure(figsize=(10, 4))
        for i in range(len(self.x_data)):
            if time:
                # Zaman aralığına göre x verilerini filtrele
                start, end = time
                x_subset = []
                y_subset = []
                for idx, val in enumerate(self.x_data[i]):
                    if start <= val <= end:
                        x_subset.append(val)
                        y_subset.append(self.y_data[i][idx])
                plt.plot(x_subset, y_subset, label=self.labels[i])
            else:
                plt.plot(self.x_data[i], self.y_data[i], label=self.labels[i])
        
        plt.xlabel(self.xlabel, fontsize=14)
        plt.ylabel(self.ylabel, fontsize=14)
        plt.title(self.title, fontsize=14)
        plt.tick_params(axis='both', which='major', labelsize=15)
        plt.grid(visible=True)
        plt.legend(fontsize=12)
        
        # Zaman aralığına göre x eksenini ayarla
        if time:
            plt.xlim(time)
        plt.show()

def calculate_performance_metrics(time, target, yest):
    time, target, yest = np.array(time), np.array(target), np.array(yest)
    delta_t = 1  

    # Hata hesaplaması
    error = target - yest

    # İstenen performans ölçütlerini hesaplayalım
    ise = np.sum(error**2 * delta_t)
    iae = np.sum(np.abs(error) * delta_t)
    itae = np.sum(time * np.abs(error) * delta_t)
    itse = np.sum(time * error**2 * delta_t)

    return ise, iae, itse, itae

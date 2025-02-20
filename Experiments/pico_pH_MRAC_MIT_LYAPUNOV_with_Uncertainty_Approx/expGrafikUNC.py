# -*- coding: utf-8 -*-
"""
Created on Thu May 16 20:31:37 2024

@author: ismt
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from controlutils import Plotter, Tablo
def calculate_performance_metrics(time, target, yest):
    
    delta_t = 0.5 

    # Hata hesaplaması
    error = target - yest

    # İstenen performans ölçütlerini hesaplayalım
    ise = np.sum(error**2 * delta_t)
    iae = np.sum(np.abs(error) * delta_t)
    itae = np.sum(time * np.abs(error) * delta_t)
    itse = np.sum(time * error**2 * delta_t)

    return ise, iae, itse, itae


g1 = pd.read_excel('2305mraclyapunc001tau20Gamma1e6.xlsx', header=None)
psi = 1e-6
t1 = g1.iloc[:, 0].to_numpy()
y1 = g1.iloc[:, 1].to_numpy()
ym1 = g1.iloc[:, 2].to_numpy()
setp1 = g1.iloc[:, 3].to_numpy()




Kr1 = g1.iloc[:, 5].to_numpy()
Kx1 = g1.iloc[:, 6].to_numpy()

#lyap
uh = g1.iloc[:, 15].to_numpy()
un = g1.iloc[:, 16].to_numpy()
up = g1.iloc[:, 7].to_numpy()
w1 = g1.iloc[:, 9].to_numpy()
w2 = g1.iloc[:, 10].to_numpy()
w3 = g1.iloc[:, 11].to_numpy()
w4 = g1.iloc[:, 12].to_numpy()
w5 = g1.iloc[:, 13].to_numpy()
w6 = g1.iloc[:, 14].to_numpy()

#radial
# up = g1.iloc[:, 7].to_numpy()
# uh = g1.iloc[:, 9].to_numpy()
# un = g1.iloc[:, 10].to_numpy()
# uh = -uh
#myss
# t1 = t1[1:]
# y1 = y1[1:]
# ym1 = ym1[1:]
# #up = up[1:]
# setp1 = setp1[1:]

# t1 = np.flip(t1)
# y1 = np.flip(y1)
# ym1 = np.flip(ym1)
# #up = np.flip(up)
# setp1 = np.flip(setp1)


ise, iae, itse, itae = calculate_performance_metrics(t1[1000:7000], setp1[1000:7000], y1[1000:7000])
 
plotter = Plotter(xlabel = 'Zaman, [s]',
                  ylabel = 'pH',
                  title = 'RMRAC Model Zaman Sabiti Karşılaştırma')
plotter.addplot(t1, setp1, label = 'Set Noktası')
plotter.addplot(t1, ym1, label = 'pH, Model')
plotter.addplot(t1, y1, label = 'pH, Proses, RMRAC, Model Zaman Sabiti = 20')
plotter.show()

plotter2 = Plotter(xlabel = 'Zaman, [s]',
                  ylabel = 'Baz Akış Hızı, [ml/dk]',
                  title = 'RMRAC, Baz Akış Hızı, [ml/dk]')

plotter2.addplot(t1, up, label = 'Baz Akış Hızı, Proses')
plotter2.addplot(t1, -uh, label = 'Baz Akış Hızı, Radyal Yakınsama')
plotter2.addplot(t1, un, label = 'Baz Akış Hızı, Nominal')
plotter2.show()


# plotter3 = Plotter(xlabel = 'Zaman, [s]',
#                   ylabel = 'Nominal Kontrol Parametreleri',
#                   title = 'RMRAC, Model Zaman Sabiti 20 iken Nominal Kontrol Edici Parametreleri')
# plotter3.addplot(t1, Kr1, label = 'Kr')
# plotter3.addplot(t1, Kx1, label = 'Kx')
# plotter3.show()

# plotter4 = Plotter(xlabel = 'Zaman, [s]',
#                   ylabel = 'Polinomial Fonksiyon Ağırlık Değerleri',
#                   title = f'LMRAC psi = {psi} iken Polinomial Fonksiyon Ağırlık Değerleri ')
# plotter4.addplot(t1, w1, label = 'w1')
# plotter4.addplot(t1, w2, label = 'w2')
# plotter4.addplot(t1, w3, label = 'w3')
# plotter4.addplot(t1, w4, label = 'w4')
# plotter4.addplot(t1, w5, label = 'w5')
# plotter4.addplot(t1, w6, label = 'w6')
# plotter4.show()


tablo = Tablo("Zaman Sabiti"  , "ise", "iae", "itse", "itae")
tablo.adddata('20', '{:.2f}'.format(ise),'{:.2f}'.format(iae), '{:.2f}'.format(itse), '{:.2f}'.format(itae))
tablo.show() 















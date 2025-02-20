# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 18:28:14 2024

@author: ismt
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from controlutils import Plotter, Tablo

df = pd.read_excel('PIDwithlowvals.xlsx')
#MATLAB POS
# tcc = df.iloc[:, 0].to_numpy()
# ycc = df.iloc[:, 1].to_numpy()
# ucc = df.iloc[:, 3].to_numpy()
# set_p = df.iloc[:, 8].to_numpy()
# yccf = df.iloc[:, 5].to_numpy()

# Python POS
tcc = df.iloc[:, 0].to_numpy()
ycc = df.iloc[:, 1].to_numpy()
ucc = df.iloc[:, 2].to_numpy()
set_p = df.iloc[:, 4].to_numpy()
yccf = df.iloc[:, 5].to_numpy()

tcc = np.flip(tcc)
ycc = np.flip(ycc)
ucc = np.flip(ucc)
set_p = np.flip(set_p)
yccf = np.flip(yccf)

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


plotter = Plotter(xlabel = 'Zaman, [s]',
                  ylabel = 'pH',
                  title = 'PID, Düşük Maliyetli Sistem pH Değeri')
plotter.addplot(tcc, set_p, label = 'Set Noktası')
plotter.addplot(tcc, ycc, label = 'pH')
#plotter.addplot(tcc, yccf, label = 'Filtreli veriler')


#plotter.addplot(trec, yrec, label = 'Model Çıktısı') # burası PID controllerden geldi..
plotter.show()

plotter2 = Plotter(xlabel = 'Zaman, [s]',
                  ylabel = 'Baz Akış Hızı[ml/dk]',
                  title = 'PID, Düşük Maliyetli Sistem, Baz Akış Hızı')
plotter2.addplot(tcc, ucc, label = 'Baz Akış Hızı, PID')
#plotter2.addplot(trec, urec, label = 'Baz Akış Hızı, Model')
plotter2.show()

ise, iae, itse, itae = calculate_performance_metrics(tcc[1000:7000], set_p[1000:7000], ycc[1000:7000]) 


# df2 = pd.read_excel('0205PIDcohen.xlsx')
# tcc2 = df2.iloc[:, 0].to_numpy()
# ycc2 = df2.iloc[:, 1].to_numpy()
# yccf2 = df2.iloc[:, 5].to_numpy()
# set_p2 = df2.iloc[:, 8].to_numpy()

# ucc2 = df2.iloc[:, 3].to_numpy()


# isecc, iaecc, itsecc, itaecc = calculate_performance_metrics(tcc2, set_p2, ycc2) 



# plotter3 = Plotter(xlabel = 'Zaman, [s]',
#                   ylabel = 'pH',
#                   title = 'PID-Cohen-Coon')
# plotter3.addplot(tcc2, set_p2, label = 'Set Noktası')
# plotter3.addplot(tcc2, ycc2, label = 'Deney Sonucu')
# #plotter.addplot(tcc2, yccf2, label = 'Filtreli veriler')


# #plotter.addplot(trec, yrec, label = 'Model Çıktısı') # burası PID controllerden geldi..
# plotter3.show()

# plotter4 = Plotter(xlabel = 'Zaman, [s]',
#                   ylabel = 'Baz Akış Hızı[ml/dk]',
#                   title = 'PID-Cohen-Coon - Baz Akış Hızı' )
# plotter4.addplot(tcc2, ucc2, label = 'Baz Akış Hızı, Deneysel')
# #plotter.addplot(trec, urec, label = 'Baz Akış Hızı, Model')
# plotter4.show()

# plotter5 = Plotter(xlabel = 'Zaman, [s]',
#                   ylabel = 'pH',
#                   title = 'PID-Cohen-Coon - ZNCL' )
# plotter5.addplot(tcc, set_p, label = 'Set Noktası')
# plotter5.addplot(tcc, ycc, label = 'ZNCL')
# plotter5.addplot(tcc2, ycc2, label = 'CC')
# plotter5.show()

# plotter6 = Plotter(xlabel = 'Zaman, [s]',
#                   ylabel = 'Baz Akış Hızı, [ml/dk]',
#                   title = 'PID-Cohen-Coon - ZNCL' )

# plotter6.addplot(tcc, ucc, label = 'ZNCL')
# plotter6.addplot(tcc2, ucc2, label = 'CC')
# plotter6.show()


tablo = Tablo("Method"  , "ise", "iae", "itse", "itae")
tablo.adddata('Cohen-Coon', '{:.2f}'.format(ise),'{:.2f}'.format(iae), '{:.2f}'.format(itse), '{:.2f}'.format(itae))
# #tablo.adddata('CC', '{:.2f}'.format(isecc),'{:.2f}'.format(iaecc), '{:.2f}'.format(itsecc), '{:.2f}'.format(itaecc) )

tablo.show() 


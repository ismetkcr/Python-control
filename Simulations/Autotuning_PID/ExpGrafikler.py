# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 18:28:14 2024

@author: ismt
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from controlutils import Plotter, Tablo

df = pd.read_excel('autoZNCL2.xlsx')
tzn = df.iloc[:, 0].to_numpy()
yzn = df.iloc[:, 2].to_numpy()
uzn = df.iloc[:, 6].to_numpy()

set_pzn = df.iloc[:, 1].to_numpy()

KC = df.iloc[:, 3].to_numpy()
TI = df.iloc[:, 4].to_numpy()
TD = df.iloc[:, 5].to_numpy()



def calculate_performance_metrics(time, target, yest):
    
    delta_t = np.diff(time, prepend=0)  

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
                  title = 'AutotuningPID-ZNCL')
plotter.addplot(tzn, set_pzn, label = 'Set Noktası')
plotter.addplot(tzn, yzn, label = 'Deney Sonucu')
#plotter.addplot(tcc, yccf, label = 'Filtreli veriler')


#plotter.addplot(trec, yrec, label = 'Model Çıktısı') # burası PID controllerden geldi..
plotter.show()

plotter2 = Plotter(xlabel = 'Zaman, [s]',
                  ylabel = 'Baz Akış Hızı[ml/dk]',
                  title = 'AutotuningPID-ZNCL- Baz Akış Hızı')
plotter2.addplot(tzn, uzn, label = 'Baz Akış Hızı, Deneysel')
#plotter.addplot(trec, urec, label = 'Baz Akış Hızı, Model')
plotter2.show()

isezn, iaezn, itsezn, itaezn = calculate_performance_metrics(tzn[1000:6600], set_pzn[1000:6600], yzn[1000:6600]) 


df2 = pd.read_excel('autoCC.xlsx')
tcc = df2.iloc[:, 0].to_numpy()
ycc = df2.iloc[:, 2].to_numpy()

set_pcc = df2.iloc[:, 1].to_numpy()

ucc = df2.iloc[:, 6].to_numpy()


isecc, iaecc, itsecc, itaecc = calculate_performance_metrics(tcc[1000:6600], set_pcc[1000:6600], ycc[1000:6600]) 



plotter3 = Plotter(xlabel = 'Zaman, [s]',
                  ylabel = 'pH',
                  title = 'PID-Cohen-Coon')
plotter3.addplot(tcc, set_pcc, label = 'Set Noktası')
plotter3.addplot(tcc, ycc, label = 'Deney Sonucu')
#plotter.addplot(tcc2, yccf2, label = 'Filtreli veriler')


#plotter.addplot(trec, yrec, label = 'Model Çıktısı') # burası PID controllerden geldi..
plotter3.show()

plotter4 = Plotter(xlabel = 'Zaman, [s]',
                  ylabel = 'Baz Akış Hızı[ml/dk]',
                  title = 'AutotuningPID-CC- Baz Akış Hızı' )
plotter4.addplot(tcc, ucc, label = 'Baz Akış Hızı, Deneysel')
#plotter.addplot(trec, urec, label = 'Baz Akış Hızı, Model')
plotter4.show()

plotter5 = Plotter(xlabel = 'Zaman, [s]',
                  ylabel = 'pH',
                  title = 'APID-Cohen-Coon - ZNCL' )
plotter5.addplot(tcc, set_pcc, label = 'Set Noktası')
plotter5.addplot(tzn, yzn, label = 'ZNCL')
plotter5.addplot(tcc, ycc, label = 'CC')
plotter5.show()

plotter6 = Plotter(xlabel = 'Zaman, [s]',
                  ylabel = 'Baz Akış Hızı, [ml/dk]',
                  title = 'PID-Cohen-Coon - ZNCL' )


plotter6.addplot(tcc, ucc, label = 'CC')
plotter6.addplot(tzn, uzn, label = 'ZNCL')
plotter6.show()


tablo = Tablo(""  , "ise", "iae", "itse", "itae")
tablo.adddata('ZNCL', '{:.2f}'.format(isezn),'{:.2f}'.format(iaezn), '{:.2f}'.format(itsezn), '{:.2f}'.format(itaezn))
tablo.adddata('CC', '{:.2f}'.format(isecc),'{:.2f}'.format(iaecc), '{:.2f}'.format(itsecc), '{:.2f}'.format(itaecc) )

tablo.show() 
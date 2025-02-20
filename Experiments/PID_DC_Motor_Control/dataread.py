# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 09:37:09 2024

@author: ismt
"""

import serial
import time
import matplotlib.pyplot as plt

def read_data(ser):
    data = ser.readline().decode('latin-1').strip()
    return data
    

    
def plottingFunc(xvector, yvector,
                 titlestr, xstr, ystr, labelstr):
    
    plt.plot(xvector, yvector, color='blue', linewidth=2, label=labelstr)
    plt.title(titlestr, fontsize=14)
    plt.xlabel(xstr, fontsize=14)
    plt.ylabel(ystr, fontsize=14)
    plt.tick_params(axis='both', which='major', labelsize=15)
    plt.grid(visible=True)
    plt.legend(fontsize=14)
# Seri port ayarları, baudrate mikrodenetleyicinizle uyumlu olmalıdır
ser = serial.Serial('COM5', 9600)  # Seri port adını ve baudrate'i uygun şekilde değiştirin

# Veri okuma döngüsü
while True:
    # Mikrodenetleyiciden gelen veriyi oku
    data = read_data(ser)  # Veriyi oku, decode et ve baştaki ve sondaki boşlukları sil
    if data:
        # Gelen veriyi ayrıştır
        ynew, unew = map(str, data.split(','))  # Veriyi virgülle ayır ve integer'a çevir
        print("unew:", unew, "ynew:", ynew)
        
        # Buraya gelen veriyi işlemek için gerekli kodu ekleyin
    time.sleep(1)  # Küçük bir bekleme ekleyerek işlemciyi yormayın
    
    
#sil bunu



    

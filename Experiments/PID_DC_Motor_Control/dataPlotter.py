# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 15:03:59 2024

@author: ismt
"""

import serial
import time
import matplotlib.pyplot as plt
import numpy as np
def read_data(ser):
    data = ser.readline().decode('latin-1').strip()
    return data
    
    








yrec = np.empty(0)
urec = np.empty(0)
trec = np.empty(0)
rrec = np.empty(0)
dt = 0.1
t = 0


ser = serial.Serial('COM5', 9600)


# Matplotlib için grafik ayarları
plt.ion()  # Etkileşimli modu aç
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)  # İki alt grafik oluştur

# İlk grafik için ayarlar
line1, = ax1.plot(trec, yrec, label='rpm')  # Başlangıçta boş bir çizgi oluştur
line3, = ax1.plot(trec, rrec, label='setpoint')  # setpoint için çizgi oluştur
ax1.set_ylabel('rpm')
ax1.legend()  # Etiketleri göster
ax1.grid()
# İkinci grafik için ayarlar
line2, = ax2.plot(trec, urec)  # Başlangıçta boş bir çizgi oluştur
ax2.set_ylabel('pwm')
ax2.set_xlabel('time,s')

setpoint = 50

while True:
    try:
        data = read_data(ser)        
        rk, ynew, unew  = map(float, data.split(','))
        
        
                        
        yrec = np.append(ynew, yrec)
        urec = np.append(unew, urec)
        trec = np.append(t, trec)
        rrec = np.append(float(rk), rrec)
        
        # İlk grafik güncelleme
        line1.set_data(trec, yrec)  # Verileri güncelle
        line3.set_data(trec, rrec)  # setpoint verilerini güncelle
        ax1.relim()  # Eksen sınırlarını güncelle
        ax1.autoscale_view()  # Eksenlerin otomatik ölçeklendirilmesini sağla
        
        # İkinci grafik güncelleme
        line2.set_data(trec, urec)  # Verileri güncelle
        ax2.relim()  # Eksen sınırlarını güncelle
        ax2.autoscale_view()  # Eksenlerin otomatik ölçeklendirilmesini sağla
        
        plt.pause(0.05)  # Grafik penceresini güncelle
       
        
        time.sleep(0.05)
        t += dt# Bekleme süresi
            
        
                      

    except KeyboardInterrupt:
        print("Ctrl+C algılandı..")
        
        
        command = input("Komut girin (quit/step): ")
        if command == "quit":
            print("Program sonlandırılıyor...")
            ser.close()            
            break
            
        elif command == "step":
            setpoint_input = input("set değerini girin: ")
            try:
                setpoint = float(setpoint_input)
                ser.write((str(setpoint) + '\n').encode())
            except ValueError:
                print("Geçersiz giriş! Lütfen bir sayı girin.")
        


plt.ioff()  # Etkileşimli modu kapat
plt.show()  
#sil duruma göre..
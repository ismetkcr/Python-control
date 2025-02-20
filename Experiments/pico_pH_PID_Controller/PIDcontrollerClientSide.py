# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 13:24:46 2024

@author: ismt
"""


import serial
import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json

ser = serial.Serial('COM8', 115200)  
def read_data(ser):
    try:
        data = ser.readline().decode().strip()
        #print("Received data:", data)  # Print received data for debugging
        return data if data else None
    except UnicodeDecodeError:
        print("UnicodeDecodeError: Unable to decode data.")
        return None

yrec = np.empty(0)
yfrec = np.empty(0)
urec = np.empty(0)
trec = np.empty(0)
rrec = np.empty(0)
arec = np.empty(0)

plt.ion()  
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

# İlk grafik için ayarlar
line1, = ax1.plot(trec, yrec, label='pH')  
line3, = ax1.plot(trec, rrec, label='setpoint')  
ax1.set_ylabel('pH')
ax1.legend()  
ax1.grid()
# İkinci grafik için ayarlar
line2, = ax2.plot(trec, urec)  
ax2.set_ylabel('baseflow')
ax2.set_xlabel('time,s')

plt.figure(fig)

time_value = 0
error = 0
set_value =7
acid_flow = 60
base_flow =0
contMode = 0
counter_value = 0
while True:
    try:
        
        ser.write((str(set_value) + ',' + str(acid_flow) +'\n').encode())       
        try:
            data = read_data(ser)
            if data:
                parsed_data = json.loads(data)                
            else:
                print("Received empty data.")
        except json.JSONDecodeError as e:
            print("JSONDecodeError:", e)
       
        if time_value==1000:
            set_value=int(8.5)
        if time_value==2000:
            set_value=int(7)
        
        time_value = float(parsed_data["time"])
        pH = float(parsed_data["pH"])
        base_flow = float(parsed_data["base_flow"])
        pHFiltered = float(parsed_data["pHF"])
        print(f'time: {time_value}s,  pH: {pH}, Acid: {acid_flow}ml/min, Base: {base_flow}ml/min')
        
        yrec = np.append(pH, yrec)
        yfrec = np.append(pHFiltered, yfrec)

        urec = np.append(base_flow, urec)
        trec = np.append(time_value, trec)
        rrec = np.append(set_value, rrec)
        arec = np.append(acid_flow, arec)
                
        # İlk grafik güncelleme
        line1.set_data(trec, yfrec)  
        line3.set_data(trec, rrec)  
        ax1.relim()  # Eksen sınırlarını güncelle
        ax1.autoscale_view()  # Eksenlerin otomatik ölçeklendirilmesini sağla
        
        # İkinci grafik güncelleme
        line2.set_data(trec, urec)  # Verileri güncelle
        ax2.relim()  # Eksen sınırlarını güncelle
        ax2.autoscale_view()  # Eksenlerin otomatik ölçeklendirilmesini sağla
                
        plt.pause(0.01)  # Grafik penceresini güncelle
        # print(pH, time_total, base_flow)       
        time.sleep(0.1)
        
        #to read
        #df = pd.read_excel(excel_file_path)
        #column_data = df['Column_Name']
        #ya da 
        #column_data = df.iloc[:, column_index]
        
    except KeyboardInterrupt:
        print("Ctrl+C algılandı..")
        command = input("Komut girin QUIT, SetValue, AcidFLow, BaseFlow, contMode: q, s, a, b, c ")
        if command == "q":
            ser.close() 
            plt.ioff()
            df = pd.DataFrame({
                'time': trec,
                'pH': yrec,
                'baseflow': urec,
                'acidflow': arec,
                'set': rrec,
                'pHfiltered': yfrec
            })
            excel_file = 'output.xlsx'
            df.to_excel(excel_file, index=False)
            print("Program sonlandırılıyor...")
           
            break
            
        elif command == "s":
            set_value = input(("setValue:"))
                    
        elif command == "a":
            acid_flow = input(("asitFLow"))
                       
        elif command == "b":
            base_flow = input(("baseFLow"))
            base_flow = float(base_flow)
                                         
        else:
            pass
            
            
            


        
    
import serial
import time
import matplotlib.pyplot as plt
import numpy as np


ser = serial.Serial('COM5', 9600)  
def read_data(ser):
    data = ser.readline().decode().strip()
    return data



setpoint_input = 0
yrec = np.empty(0)
urec = np.empty(0)
trec = np.empty(0)
rrec = np.empty(0)



plt.ion()  
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)


# İlk grafik için ayarlar
line1, = ax1.plot(trec, yrec, label='rpm')  
line3, = ax1.plot(trec, rrec, label='setpoint')  
ax1.set_ylabel('rpm')
ax1.legend()  
ax1.grid()
# İkinci grafik için ayarlar
line2, = ax2.plot(trec, urec)  
ax2.set_ylabel('pwm')
ax2.set_xlabel('time,s')

# plt.figure(fig)
dt = 0.1
error = 0
while True:
    try:
        
       
        ser.write((str(setpoint_input) + '\n').encode())
        data = read_data(ser)
        parts = data.split(',')
        if len(parts)>=5:
            elapsedTime  = float(parts[1])
            rpmvalue  = float(parts[2])
            pwmvalue = float(parts[3])
            set_value = float(parts[4])
            if set_value <=0:
                set_value = 0
        else:
            error = error + 1
            pass
        print(elapsedTime)
        
        
        
        yrec = np.append(rpmvalue, yrec)
        time_val = len(yrec) * dt
        urec = np.append(pwmvalue, urec)
        trec = np.append(elapsedTime, trec)
        rrec = np.append(set_value, rrec)
        
        
        # İlk grafik güncelleme
        line1.set_data(trec, yrec)  
        line3.set_data(trec, rrec)  
        ax1.relim()  # Eksen sınırlarını güncelle
        ax1.autoscale_view()  # Eksenlerin otomatik ölçeklendirilmesini sağla
        
        # İkinci grafik güncelleme
        line2.set_data(trec, urec)  # Verileri güncelle
        ax2.relim()  # Eksen sınırlarını güncelle
        ax2.autoscale_view()  # Eksenlerin otomatik ölçeklendirilmesini sağla
        
        
        plt.pause(0.01)  # Grafik penceresini güncelle
        time.sleep(0.04)
        
        
    except KeyboardInterrupt:
        print("Ctrl+C algılandı..")
        
        
        command = input("Komut girin (quit/step): ")
        if command == "quit":
            print("Program sonlandırılıyor...")
            ser.close() 
            plt.ioff()
            break
            
        elif command == "step":
            setpoint_input = input(("set değerini girin:"))
            setpoint_input = str(setpoint_input)
            #ser.write((str(setpoint_input) + '\n').encode())
            # ser.write((str(setpoint_input) + '\n').encode())
            
            

        
    
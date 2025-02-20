# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 22:13:39 2025

@author: ismt
"""

from superlogics_comm_class import DAQSystem, AnalogInput, AnalogOutput, CurrentOutput
from SignalGenerator_class import SignalGenerator
from real_time_plotter_class import EnhancedRealTimePlot
import time
import pandas as pd
import matplotlib.pyplot as plt
from utils_class import change_flow, pH_calib, acid_pump_calib, base_pump_calib

if __name__ == "__main__":
    # Initialize data storage
    experiment_data = []
    start_time = time.time()
    
    # Initialize DAQ system
    daq = DAQSystem("COM3", 19200)
    daq.open(enabled_analog_inputs=[False, False, True, False, False, False, False, False])
    time.sleep(0.5)
    
    # Initialize plots
    time_vs_latest = EnhancedRealTimePlot(experiment_data, 'time', 'pH', 
                                 'Time (seconds)', 'pH', 1000)
    time_vs_acid = EnhancedRealTimePlot(experiment_data, 'time', 'acid_flow',
                               'Time (seconds)', 'Acid Flow', 1000)
    time_vs_base = EnhancedRealTimePlot(experiment_data, 'time', 'base_flow',
                               'Time (seconds)', 'Base Flow', 1000)

    # Initialize generator with 100 Hz sample rate
    gen = SignalGenerator(sample_rate=1)
    
    # Generate PRBS7 signal
    prbs = gen.generate_prbs(
        sequence_length=7,
        min_val=0,
        max_val=150,
        num_samples=5000
    )
    # Generate square wave (0.5Hz, 50% duty cycle)
    square = gen.generate_square(
        high_duration=15.0,  # 1 second high
        low_duration=15.0,   # 1 second low
        min_val=0,
        max_val=1,
        total_duration=5000   # 20 second signal
    )
    square[:50] = 0
    prbs[:50] = 0
    # Create interfaces
    input_ch2 = AnalogInput(daq, 2)
    output_ch0 = AnalogOutput(daq, 0)
    output_ch1 = AnalogOutput(daq, 1)
    acid_flow = 50
    base_flow = 0
    i = 0
    try:
        running = True
        while running:
            try:
                loop_start = time.time()
                
                # Read data and calculate elapsed time
                latest_value = input_ch2.read()
                #base_flow = float(prbs[i])
                pH = pH_calib(latest_value)
                elapsed_time = time.time() - start_time
                #print(f"square_signal_value = {square[i]}")
                i+=1
                # Apply updated flow values
                base_voltage = base_pump_calib(base_flow)
                acid_voltage = acid_pump_calib(acid_flow)
                
                # Store data
                experiment_data.append({
                    "time": elapsed_time,
                    "latest_value": latest_value,
                    "pH": pH,
                    "acid_flow": acid_flow,
                    "base_flow": base_flow,
                    "acid_voltage": acid_voltage,
                    "base_voltage": base_voltage
                })
                
                # Update plots
                time_vs_latest.update()
                time_vs_acid.update()
                time_vs_base.update()
                
                # Print status
                timestamp = time.strftime("%H:%M:%S", time.localtime())
                if latest_value is not None:
                    print(f"[{timestamp}] pH: {pH:.2f} | Acid: {acid_flow} | Base: {base_flow}")
                else:
                    print(f"[{timestamp}] No data available")
                
                output_ch0.write(base_voltage)
                output_ch1.write(acid_voltage)
                
                # Maintain 1s interval
                elapsed = time.time() - loop_start
                time.sleep(max(0, 1 - elapsed))
    
            except KeyboardInterrupt:
                print("\nCtrl+C detected.")
                while True:  # Keep prompting until a valid choice is made
                    choice = input("Do you want to quit or change flow values? (quit/change): ").strip().lower()
                    if choice == 'quit':
                        running = False  # Stop the loop
                        break  # Exit prompt and stop program
                    elif choice == 'change':
                        flow_type, new_value = change_flow()
                        if flow_type == 'base':
                            base_flow = new_value
                        elif flow_type == 'acid':
                            acid_flow = new_value
                        print(f"{flow_type}_flow updated to {new_value}. Continuing experiment...")
                        break  # Exit prompt and continue loop
                    else:
                        print("Invalid input. Please enter 'quit' or 'change'.")
    
    finally:
        # Cleanup
        output_ch0.write(0.0)
        output_ch1.write(0.0)
        daq.close()
        time_vs_latest.close()
        time_vs_acid.close()
        time_vs_base.close()
        plt.ioff()

# Save data
df = pd.DataFrame(experiment_data)
df.to_excel("experiment_values_random_vals.xlsx", index=False)
print("Experiment data saved to experiment_values_random_vals.xlsx")
import serial
import json
import time
from comm_pi_side import comm_pi

def main():
    while True:
        # Initialize communication with the Pico
        uart_comm = comm_pi(port='COM4', baud_rate=115200)
        
        try:
            # Step 1: Get user input
            C2 = float(input("Enter desired molarity (mol/L): "))
            V2 = float(input("Enter desired volume (mL): "))
            
            # Step 2: Perform calculations
            C1 = 0.2  # Stock solution molarity (mol/L)
            V1 = (C2 * V2) / C1  # Stock solution needed (mL)
            V_pure_water = V2 - V1  # Pure water volume needed (mL)
            
            # Convert to pump run times based on flow rate
            flow_rate_1 = 50   # Flow rate in mL/min
            flow_rate_2 = 30
            pump1_time = (V1 / flow_rate_1) * 60  # Pump 1 run time in seconds
            pump2_time = (V_pure_water / flow_rate_2) * 60  # Pump 2 run time in seconds
            # pump1_time = 60  #baz mavi
            # pump2_time= 60 #saf su gri 
            
            print("CALCULATES VALUES FOR mL and seconds:")
            print(f"  Stack solution (V1): {V1:.2f} mL")
            print(f"  Pure water (V_pure_water): {V_pure_water:.2f} mL")
            print(f"  Pump 1 run time: {pump1_time:.2f} seconds")
            print(f"  Pump 2 run time: {pump2_time:.2f} seconds")
            
            # Step 3: Send data to Pico
            data_to_send = {
                "pump1_time": pump1_time,
                "pump2_time": pump2_time
            }
            uart_comm.send(data_to_send)
            print("Sent data to Pico.")
            
            # Step 4: Wait for Pico responses
            countdown_started = False
            while True:
                response = uart_comm.read()
                if response:
                    try:
                        if "flag" in response:
                            prep_flag = response["flag"]
                            if not prep_flag and not countdown_started:
                                print("Preparation in progress...")
                                countdown_started = True
                            elif prep_flag:
                                print("Solution preparation is complete!")
                                break
                        elif "countdown" in response:
                            print(f"Countdown: {response['countdown']} seconds remaining")
                        else:
                            print("Unknown response:", response)
                    except Exception as e:
                        print(f"Error processing response: {e}")
                time.sleep(1)
            
            # Step 5: Ask if user wants to prepare another solution
            repeat = input("Prepare another solution? (y/n): ").lower()
            if repeat != 'y':
                break
        finally:
            uart_comm.ser.close()  # Ensure the serial port is closed after each iteration

if __name__ == "__main__":
    main()

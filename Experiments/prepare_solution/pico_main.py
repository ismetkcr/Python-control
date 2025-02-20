from comm_pico_side import pico_comm
from motorDrivers import LN298
import json
import utime

# Function to run the pump with countdown
def run_pump_with_countdown(uart_comm, pump: LN298, duration: float, duty_cycle: int = 30000):
    """Run the pump for a specified duration with countdown."""
    pump.set_duty_cycle(duty_cycle)
    
    # Countdown loop
    for remaining in range(int(duration), 0, -1):
        uart_comm.send({"countdown": remaining})
        utime.sleep(1)
    
    pump.stop()

def main():
    # Initialize UART and pumps
    uart_comm = pico_comm(uart_id=0, baud_rate=115200)
    pump1 = LN298(pinEN=15)
    pump2 = LN298(pinEN=11)
    
    print("Pico communication initialized")
    
    while True:
        # Wait for a message from the computer
        print("Waiting for message...")
        message = uart_comm.read()
        
        if message:
            print(f"Received message: {message}")
            try:
                # Extract pump run times directly from the dictionary
                pump1_time = message["pump1_time"]
                pump2_time = message["pump2_time"]
                
                print(f"Pump times - Pump1: {pump1_time}, Pump2: {pump2_time}")
                
                # Send preparation flag
                uart_comm.send({"flag": False})
                utime.sleep(1)  # Optional delay for processing
                print(f"pump1 runtime is {pump1_time:.2f}, pump2 runtime is {pump2_time:.2f}")
                
                # Run pumps with countdown
                run_pump_with_countdown(uart_comm, pump1, pump1_time)
                run_pump_with_countdown(uart_comm, pump2, pump2_time)
                
                # Send completion flag
                uart_comm.send({"flag": True})
            except KeyError as e:
                print(f"Missing key in message: {e}")
                uart_comm.send({"error": f"Missing key: {e}"})
            except Exception as e:
                print(f"Error processing message: {e}")
                uart_comm.send({"error": str(e)})
        
        # Add a small delay to prevent tight looping
        utime.sleep(0.5)

# Run the main loop
if __name__ == "__main__":
    main()
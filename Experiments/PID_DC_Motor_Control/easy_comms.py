from machine import UART, Pin
from time import time_ns
import utime

class Easy_comms:
    uart_id = 0
    baud_rate = 9600
    timeout = 1000 #milisec
    
    def __init__(self, uart_id:int, baud_rate:int=None):
        self.uart_id = uart_id
        if baud_rate: self.baud_rate = baud_rate
        
        #set the baudrate
        self.uart = UART(self.uart_id, self.baud_rate)
        self.uart.init()
        print("UART ID:",self.uard_id, "BAUDRATE: ", self.baud_rate )
        
    
    def send(self, message:str):
        #print(f'sending message: {message}')
        message = message + '\n'
        self.uart.write(bytes(message, 'utf-8'))
        
    def read(self) -> float:
        start_time = time_ns()
        current_time = start_time
        new_line = False
        message = bytearray()
        while (not new_line) or (current_time) <= (start_time + self.timeout):
            if (self.uart.any() > 0):
                received_bytes = self.uart.read(self.uart.any())
                try:
                    message.extend(received_bytes.decode('utf-8'))
                except UnicodeError:
                    # Handle decoding errors gracefully
                    pass
                    
                if b'\n' in received_bytes:
                    new_line = True
                    message_str = message.decode('utf-8').strip('\n')
                    try:
                        float_value = float(message_str)
                        return float_value
                    except ValueError:
                        # Handle conversion to float error gracefully
                        pass
            else:
                utime.sleep_ms(10)  # Add a small delay to avoid busy waiting
                current_time = time_ns()
        return None




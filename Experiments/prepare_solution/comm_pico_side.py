from machine import Pin, UART
import utime
import json  # json modülünü içe aktar

class pico_comm:
    def __init__(self, uart_id: int, baud_rate: int = 9600):
        self.uart_id = uart_id
        self.baud_rate = baud_rate

        # Set the baudrate
        self.uart = UART(self.uart_id, self.baud_rate)
        self.uart.init()

    def send(self, message: dict):
        json_message = json.dumps(message) + '\n'
        self.uart.write(json_message.encode('utf-8'))

    def read(self):
        if self.uart.any():
            try:
                data = self.uart.readline().decode('utf-8').strip()
                if data:
                    return json.loads(data)
            except ValueError as e:
                print(f"Failed to read/parse data: {e}")
        return None

import serial
import time
import json

class comm_pi:
    def __init__(self, port='/dev/ttyUSB0', baud_rate=115200):
        self.ser = serial.Serial(port, baud_rate, timeout=1.0)
        time.sleep(3)
        self.ser.reset_input_buffer()
        print("Serial OK.")
    
    def send(self, message: dict):
        json_message = json.dumps(message) + '\n'
        self.ser.write(json_message.encode('utf-8'))
    
    def read(self):
        try:
            line = self.ser.readline().decode('utf-8').strip()
            if line:
                return json.loads(line)
            else:
                return None
        except json.JSONDecodeError:
            print("Received data is not in valid JSON format.")
            return None
        except Exception as e:
            print(f"An error occurred while reading: {e}")
            return None
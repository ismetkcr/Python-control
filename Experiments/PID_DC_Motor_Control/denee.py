import machine
import time

adc = machine.ADC(27)  # GP26 is ADC pin



while True:
    reading = adc.read_u16()
    voltage = reading * (3.3 / 65535)  # Convert ADC reading to voltage
    print("Voltage:", voltage)
    time.sleep(1)

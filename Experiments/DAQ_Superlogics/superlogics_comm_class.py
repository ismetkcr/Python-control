# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 11:03:03 2025

@author: ismt
"""
import serial
import threading
import time
from collections import deque
from typing import List, Dict

class DAQSystem:
    """Central class managing serial port and background sampling"""
    def __init__(self, port: str, baud_rate: int):
        self.port = port
        self.baud_rate = baud_rate
        self.ser = serial.Serial()
        self.lock = threading.Lock()
        self.running = False
        self.sampling_thread = None
        self.sample_buffers: Dict[int, deque] = {}
        self.sampling_interval = 0.5  # 500ms default

    def open(self, enabled_analog_inputs: List[bool] = [True]*8):
        """Open connection and start background sampling"""
        try:
            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.baud_rate,
                timeout=0.1
            )
            # Initialize buffers for enabled channels
            self.sample_buffers = {i: deque(maxlen=10)  # Buffer size for 10 samples (1 second at 100ms intervals)
                                  for i, enabled in enumerate(enabled_analog_inputs) 
                                  if enabled}
            self.running = True
            self.sampling_thread = threading.Thread(target=self._sampling_loop)
            self.sampling_thread.start()
            return True
        except Exception as e:
            raise RuntimeError(f"Connection failed: {e}")

    def close(self):
        """Stop sampling and close connection"""
        self.running = False
        if self.sampling_thread:
            self.sampling_thread.join()
        if self.ser.is_open:
            self.ser.close()

    def _sampling_loop(self):
        """Background thread for continuous analog input sampling"""
        while self.running:
            start_time = time.time()
            with self.lock:
                for ch in self.sample_buffers.keys():
                    self.ser.write(f"#{ch:03d}\r".encode())
                    response = self.ser.readline().decode().strip()
                    if response.startswith('>'):
                        try:
                            value = float(response[1:])
                            self.sample_buffers[ch].append(value)
                        except ValueError:
                            pass
            elapsed = time.time() - start_time
            time.sleep(max(0, self.sampling_interval - elapsed))

    def get_latest_value(self, channel: int):
        """Get the latest value from the buffer for the specified channel"""
        with self.lock:
            buffer = self.sample_buffers.get(channel, deque())
            if len(buffer) == 0:
                return None
            return buffer[-1]  # Return the most recent value

class AnalogInput:
    """Analog input channel interface"""
    def __init__(self, daq: DAQSystem, channel: int):
        self.daq = daq
        self.channel = channel

    def read(self) -> float:
        """Read the latest value from the channel"""
        return self.daq.get_latest_value(self.channel)

class AnalogOutput:
    """Analog voltage output (0-10V)"""
    def __init__(self, daq: DAQSystem, channel: int):
        self.daq = daq
        self.channel = channel
        self.cmd_prefix = f"#03{channel}"

    def write(self, voltage: float):
        """Write voltage to output channel"""
        voltage = max(min(voltage, 10.0), 0)
        with self.daq.lock:
            cmd = f"{self.cmd_prefix}{voltage:+07.3f}\r"
            self.daq.ser.write(cmd.encode())
            _ = self.daq.ser.readline()  # Read confirmation

class CurrentOutput:
    """4-20mA current output"""
    def __init__(self, daq: DAQSystem, channel: int):
        self.daq = daq
        self.channel = channel
        self.cmd_prefix = f"#02{channel}"

    def write(self, current: float):
        """Write current to output channel"""
        current = max(min(current, 20.0), 0.0)
        with self.daq.lock:
            cmd = f"{self.cmd_prefix}{current:+07.3f}\r"
            self.daq.ser.write(cmd.encode())
            _ = self.daq.ser.readline()  # Read confirmation


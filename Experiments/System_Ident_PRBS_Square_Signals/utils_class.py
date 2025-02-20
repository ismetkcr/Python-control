# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 15:06:18 2025

@author: ismt
"""

def change_flow():
    while True:
        flow_type = input("Which flow do you want to change? (base/acid): ").strip().lower()
        if flow_type in ['base', 'acid']:
            try:
                new_value = float(input(f"Enter new value for {flow_type}_flow: "))
                return flow_type, new_value
            
            
            except ValueError:
                print("Please enter a valid number.")
        else:
            print("Invalid input. Please enter 'base' or 'acid'.")
 
           
def pH_calib(voltage: float) -> float:
    """Calibrates a voltage reading from a pH sensor to a pH value.

    Args:
        voltage (float): Voltage reading from the pH sensor in volts

    Returns:
        float: Calibrated pH value

    Raises:
        TypeError: If input is not numeric
    """
    if not isinstance(voltage, (int, float)):
        raise TypeError("Input voltage must be numeric")
    
    calibrated_pH = (1.40 * float(voltage)) + 0.044
    return calibrated_pH


def acid_pump_calib(acid_flow: float) -> float:
    """Converts desired acid flow rate to control voltage for pump calibration.

    Args:
        acid_flow (float): Desired acid flow rate in mL/min

    Returns:
        float: Corresponding control voltage in volts

    Raises:
        TypeError: If input is not numeric
        ValueError: If flow rate is negative
    """
    if not isinstance(acid_flow, (int, float)):
        raise TypeError("Flow rate must be numeric")
    if acid_flow < 0:
        raise ValueError("Flow rate cannot be negative")
    if acid_flow == 0:
        return 0
    control_voltage = (0.0361 * float(acid_flow)) + 0.3898
    return round(control_voltage, 4)


def base_pump_calib(base_flow: float) -> float:
    """Converts desired base flow rate to control voltage for pump calibration.

    Args:
        base_flow (float): Desired base flow rate in mL/min

    Returns:
        float: Corresponding control voltage in volts

    Raises:
        TypeError: If input is not numeric
        ValueError: If flow rate is negative
    """
    if not isinstance(base_flow, (int, float)):
        raise TypeError("Flow rate must be numeric")
    if base_flow < 0:
        raise ValueError("Flow rate cannot be negative")
    if base_flow == 0:
        return 0

    control_voltage = (0.0401 * float(base_flow)) + 0.1396
    return round(control_voltage, 4)
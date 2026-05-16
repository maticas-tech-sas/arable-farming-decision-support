import numpy as np
import scipy.integrate as integrate
import datetime

def calculate_cummulative_thermal_time(base_temperature: float,
                                       temperatures: np.ndarray,
                                       times: np.ndarray, 
                                       initial_thermal_time: float = 0.0,
                                       method: str = 'trapz') -> np.ndarray:
        
    """Calculate the cummulative thermal time given a set of temperatures and times, 
    and base temperature.

    Args:
        thermal_time (float): The accumulated thermal time required for emergence.
        base_temperature (float): The base temperature below which development does not occur.
        temperatures (np.ndarray): An array of timely temperatures.
        times (np.ndarray): An array of corresponding times for the temperatures. Could be unix timestamp or datetime objects.
        initial_thermal_time (float): The initial thermal time to start with, in °C-days. Default is 0.
        method (str): The integration method to use ('trapz' or 'simps').

    Returns:
        np.ndarray: An array of cumulative thermal time values corresponding to the input times, in °C-days.
    """

    # Calculate the thermal time for each time step
    thermal_time_steps = np.maximum(0, temperatures - base_temperature)

    # Ensure that the lengths of temperatures and times match
    if len(thermal_time_steps) != len(times):
        raise ValueError("The lengths of temperatures and times must match.")
    
    # Check if unix timestamps or datetime objects are used and convert to seconds if necessary
    if isinstance(times[0], datetime.datetime):
        times = np.array([t.timestamp() for t in times])

    # Integrate the thermal time over the time steps
    if method == 'trapz':
        current_thermal_time = integrate.cumulative_trapezoid(thermal_time_steps, times, initial=initial_thermal_time * 86400)
    elif method == 'simps':
        current_thermal_time = integrate.cumulative_simpson(thermal_time_steps, times, initial=initial_thermal_time * 86400)
    else:
        raise ValueError("Invalid method. Use 'trapz' or 'simps'.")

    # Convert to °C-days 
    current_thermal_time = current_thermal_time / 86400  # Convert seconds to days
    return current_thermal_time
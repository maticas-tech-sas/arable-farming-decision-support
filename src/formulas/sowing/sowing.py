from src.formulas.general import *

def calculate_thermal_time_to_emergence(current_thermal_time: float, required_thermal_time: float) -> float:
    """Calculate the remaining thermal time to emergence.

    Args:
        current_thermal_time (float): The current accumulated thermal time in °C-days.
        required_thermal_time (float): The total thermal time required for emergence in °C-days.

    Returns:
        float: The remaining thermal time to emergence in °C-days. If negative, emergence has already occurred.
    """
    remaining_thermal_time = required_thermal_time - current_thermal_time
    return remaining_thermal_time

def find_emergence_date(required_thermal_time: float,
                        cummulative_thermal_time: np.ndarray,
                        times: np.ndarray) -> datetime.datetime:
    """Find the emergence date based on the required thermal time and cumulative thermal time.
    Args:
        required_thermal_time (float): The total thermal time required for emergence in °C-days.
        cummulative_thermal_time (np.ndarray): An array of cumulative thermal time values corresponding to the input times, in °C-days.
        times (np.ndarray): An array of corresponding times for the cumulative thermal time. Could be unix timestamp or datetime objects.
    Returns:
        datetime.datetime: The estimated emergence date.
    """
    emergence_time_index = np.where(cummulative_thermal_time >= required_thermal_time)[0]
    if len(emergence_time_index) == 0:
        raise ValueError("The required thermal time for emergence is not reached within the provided cumulative thermal time.")
    emergence_time = times[emergence_time_index[0]]
    emergence_time = datetime.datetime.fromtimestamp(emergence_time)
    return emergence_time

def estimate_emergence_date(current_thermal_time: float,
                            required_thermal_time: float, 
                            temperatures: np.ndarray,
                            times: np.ndarray, 
                            base_temperature: float, 
                            method: str = 'trapz') -> datetime.datetime:

    """Estimate the emergence date based on current thermal time and future temperature projections.

    Args:
        current_thermal_time (float): The current accumulated thermal time in °C-days.
        required_thermal_time (float): The total thermal time required for emergence in °C-days.
        temperatures (np.ndarray): An array of future temperature projections.
        times (np.ndarray): An array of corresponding times for the future temperatures. Could be unix timestamp or datetime objects.
        base_temperature (float): The base temperature below which development does not occur.
        method (str): The integration method to use ('trapz' or 'simps').

    Returns:
        datetime.datetime: The estimated emergence date.
    """

    # Calculate the cumulative thermal time for the future temperatures
    cumulative_thermal_time = calculate_cummulative_thermal_time(base_temperature,
                                                                 temperatures,
                                                                 times,
                                                                 initial_thermal_time=current_thermal_time,
                                                                 method=method)

    # Find the emergence date based on the cumulative thermal time
    emergence_time = find_emergence_date(required_thermal_time, cumulative_thermal_time, times)
    return emergence_time

def calculate_seeding_rate(mass_per_seed: float,
                           desired_plant_density: float,
                           seed_viability_fraction: float,
                           viable_seeds_that_become_plants_fraction: float) -> float:
    """Calculate the seeding rate based on seed mass, desired plant density, and viability factors.
    Args:
        mass_per_seed (float): The mass of a single seed in miligrams (mg).
        desired_plant_density (float): The desired plant density in plants per square meter (plants
        seed_viability_fraction (float): The fraction of seeds that are viable (between 0 and 1).
        viable_seeds_that_become_plants_fraction (float): The fraction of viable seeds that actually become plants (between 0 and 1).
    Returns:
        float: The required seeding rate in kilograms per hectare (kg/ha).
    """

    #check that the input values are valid
    if not (0 < seed_viability_fraction <= 1):
        raise ValueError("seed_viability_fraction must be between 0 and 1.")
    if not (0 < viable_seeds_that_become_plants_fraction <= 1):
        raise ValueError("viable_seeds_that_become_plants_fraction must be between 0 and 1.")

    # Calculate the seeding rate in mg/m^2
    seeding_rate_mg_per_m2 = (desired_plant_density * mass_per_seed) / (seed_viability_fraction * viable_seeds_that_become_plants_fraction)

    # Convert seeding rate to kg/ha
    seeding_rate_kg_per_ha = seeding_rate_mg_per_m2 * 10  # Convert mg/m^2 to kg/ha (1 mg/m^2 = 10 kg/ha)

    return seeding_rate_kg_per_ha


def suggest_sowing_depth_1(seed_size: float) -> float:
    """Suggest sowing depth based on seed size using a simple rule of thumb.

    Args:
        seed_size (float): The size of the seed in millimeters (mm).

    Returns:
        float: The suggested sowing depth in millimeters (mm).
    """
    # A common rule of thumb is to plant seeds at a depth of 2 to 3 times their size
    suggested_depth = seed_size * 2.5  # Using the average of 2 and 3 times the seed size
    return suggested_depth

def suggest_maximum_sowing_depth(seed_mass: float,
                                 scaling_factor: float = 27.3) -> float:
    """Suggest maximum sowing depth based on seed mass using a simple empirical relationship, allometric formula based on seed mass was developed by Bond et al. (1999)

    Args:
        seed_mass (float): The mass of the seed in milligrams (mg).
        scaling_factor (float): An optional scaling factor to adjust the suggested depth. Default is 27.3 as per paper.

    Returns:
        float: The suggested maximum sowing depth in millimeters (mm).
    """
    # An empirical relationship could be that the maximum sowing depth is proportional to the cube root of the seed mass
    suggested_depth = scaling_factor * (seed_mass ** (1/3)) 
    return suggested_depth


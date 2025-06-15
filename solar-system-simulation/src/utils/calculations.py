def calculate_orbital_period(semi_major_axis, gravitational_constant, mass_sun):
    """
    Calculate the orbital period of a planet using Kepler's third law.
    
    Parameters:
    semi_major_axis (float): The semi-major axis of the orbit in meters.
    gravitational_constant (float): The gravitational constant (6.67430e-11 m^3 kg^-1 s^-2).
    mass_sun (float): The mass of the sun in kilograms (1.989e30 kg).
    
    Returns:
    float: The orbital period in seconds.
    """
    return 2 * 3.14159 * ((semi_major_axis**3) / (gravitational_constant * mass_sun))**0.5

def calculate_gravitational_force(mass1, mass2, distance):
    """
    Calculate the gravitational force between two masses.
    
    Parameters:
    mass1 (float): The mass of the first object in kilograms.
    mass2 (float): The mass of the second object in kilograms.
    distance (float): The distance between the centers of the two masses in meters.
    
    Returns:
    float: The gravitational force in newtons.
    """
    gravitational_constant = 6.67430e-11  # m^3 kg^-1 s^-2
    return gravitational_constant * (mass1 * mass2) / (distance**2)
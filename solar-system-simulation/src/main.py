# Solar System Simulation

import json
from models.planet import Planet
from utils.calculations import calculate_orbital_period

def load_solar_system_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def initialize_planets(data):
    planets = []
    for planet_data in data['planets']:
        planet = Planet(
            name=planet_data['name'],
            mass=planet_data['mass'],
            radius=planet_data['radius'],
            distance_from_sun=planet_data['distance_from_sun']
        )
        planets.append(planet)
    return planets

def run_simulation(planets):
    for planet in planets:
        orbital_period = calculate_orbital_period(planet.distance_from_sun)
        print(f"{planet.name} has an orbital period of {orbital_period:.2f} Earth years.")

def main():
    solar_system_data = load_solar_system_data('src/data/solar_system.json')
    planets = initialize_planets(solar_system_data)
    run_simulation(planets)

if __name__ == "__main__":
    main()

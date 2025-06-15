class Planet:
    def __init__(self, name, mass, radius, distance_from_sun):
        self.name = name
        self.mass = mass
        self.radius = radius
        self.distance_from_sun = distance_from_sun

    def calculate_gravity(self):
        G = 6.67430e-11  # gravitational constant
        return G * self.mass / (self.radius ** 2)

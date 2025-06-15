"""Simple 3D solar system simulation using vpython.

This script displays the planets orbiting around the sun in a 3D scene.
You can rotate the view with the mouse to observe the orbits from any angle.
"""

from math import cos, sin, pi, sqrt

from vpython import canvas, color, rate, sphere, vector

# Physical constants
G = 6.67430e-11  # m^3 kg^-1 s^-2
SUN_MASS = 1.989e30  # kg
AU = 1.496e11  # Astronomical unit in meters
DAY = 24 * 3600  # One day in seconds

# Scaling factors for the display
DIST_SCALE = AU / 50       # Reduce orbital radius for better visibility
RADIUS_SCALE = 7e6         # Reduce planet radii
TIME_SCALE = 5000          # Simulation speed multiplier


def orbital_period(semi_major_axis: float) -> float:
    """Return the orbital period in seconds using Kepler's third law."""
    return 2 * pi * sqrt(semi_major_axis**3 / (G * SUN_MASS))


class Planet:
    def __init__(self, name: str, distance: float, radius: float, body_color):
        self.name = name
        self.distance = distance / DIST_SCALE
        self.radius = max(radius / RADIUS_SCALE, 0.2)
        self.angle = 0.0
        self.period = orbital_period(distance)
        self.angular_speed = 2 * pi / self.period
        self.sphere = sphere(
            pos=vector(self.distance, 0, 0),
            radius=self.radius,
            color=body_color,
            make_trail=True,
            retain=200,
        )

    def update(self, dt: float) -> None:
        self.angle += self.angular_speed * dt
        x = self.distance * cos(self.angle)
        z = self.distance * sin(self.angle)
        self.sphere.pos = vector(x, 0, z)


def create_planets():
    return [
        Planet("Mercury", 0.387 * AU, 2_439_000, color.gray(0.5)),
        Planet("Venus", 0.723 * AU, 6_052_000, color.orange),
        Planet("Earth", 1.0 * AU, 6_371_000, color.blue),
        Planet("Mars", 1.524 * AU, 3_389_000, color.red),
        Planet("Jupiter", 5.203 * AU, 69_911_000, color.white),
        Planet("Saturn", 9.537 * AU, 58_232_000, color.yellow),
        Planet("Uranus", 19.191 * AU, 25_362_000, color.cyan),
        Planet("Neptune", 30.07 * AU, 24_622_000, color.blue),
    ]


def main() -> None:
    canvas(width=800, height=600, background=color.black)
    sun = sphere(pos=vector(0, 0, 0), radius=696_340_000 / RADIUS_SCALE, color=color.yellow)
    planets = create_planets()

    dt = DAY
    while True:
        rate(120)
        for planet in planets:
            planet.update(dt * TIME_SCALE)


if __name__ == "__main__":
    main()

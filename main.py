"""Simple 2D solar system simulation using pygame."""

from dataclasses import dataclass, field
from typing import List, Tuple
import math
import pygame

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulación del Sistema Solar")

# Colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)
BLACK = (0, 0, 0)


@dataclass
class Planet:
    """Representa un planeta o el sol dentro de la simulación."""

    x: float
    y: float
    radius: int
    color: Tuple[int, int, int]
    mass: float
    x_vel: float = 0.0
    y_vel: float = 0.0
    sun: bool = False
    distance_to_sun: float = 0.0
    orbit: List[Tuple[float, float]] = field(default_factory=list)

    AU = 149.6e6 * 1000  # Astronomical Unit in meters
    G = 6.67428e-11  # Gravitational constant
    SCALE = 80 / AU  # 1AU = 80 pixels
    TIMESTEP = 3600 * 24  # 1 day in seconds

    def draw(self, win: pygame.Surface) -> None:
        """Draw the planet and its orbit on the given surface."""
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = []
            for x_point, y_point in self.orbit:
                x_point = x_point * self.SCALE + WIDTH / 2
                y_point = y_point * self.SCALE + HEIGHT / 2
                updated_points.append((x_point, y_point))

            pygame.draw.lines(win, self.color, False, updated_points, 2)

        pygame.draw.circle(win, self.color, (int(x), int(y)), self.radius)

    def attraction(self, other: "Planet") -> Tuple[float, float]:
        """Calculate gravitational force exerted by another body."""
        distance_x = other.x - self.x
        distance_y = other.y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets: List["Planet"]) -> None:
        """Update velocity and position based on gravitational forces."""
        if self.sun:
            return

        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))


def create_planets() -> List[Planet]:
    """Create the planets with initial positions and velocities."""
    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30, sun=True)
    mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, 3.30 * 10**23, y_vel=-47.4 * 1000)
    venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**24, y_vel=-35.02 * 1000)
    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24, y_vel=29.783 * 1000)
    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23, y_vel=24.077 * 1000)
    jupiter = Planet(-5.2 * Planet.AU, 0, 22, (222, 184, 135), 1.898 * 10**27, y_vel=13.06 * 1000)
    saturn = Planet(9.5 * Planet.AU, 0, 20, (238, 232, 170), 5.683 * 10**26, y_vel=-9.68 * 1000)
    uranus = Planet(-19.2 * Planet.AU, 0, 18, (173, 216, 230), 8.681 * 10**25, y_vel=6.80 * 1000)
    neptune = Planet(30.1 * Planet.AU, 0, 18, (0, 0, 139), 1.024 * 10**26, y_vel=-5.43 * 1000)
    return [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]


def main() -> None:
    """Run the main simulation loop."""
    clock = pygame.time.Clock()
    planets = create_planets()
    run = True

    while run:
        clock.tick(60)
        WIN.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()

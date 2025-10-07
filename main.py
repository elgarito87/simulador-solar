"""Simple 2D solar system simulation using pygame."""

from dataclasses import dataclass, field
from typing import List, Optional, Tuple
import math
import pygame

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulación del Sistema Solar")

# Colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)
BLACK = (0, 0, 0)
PANEL_BG = (18, 24, 38)
PANEL_BORDER = (45, 60, 90)

FONT_TITLE = pygame.font.SysFont("arial", 22, bold=True)
FONT_TEXT = pygame.font.SysFont("arial", 16)


@dataclass
class Planet:
    """Representa un cuerpo celeste dentro de la simulación."""

    name: str
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

    def draw(self, win: pygame.Surface, selected: bool = False) -> None:
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

        if selected:
            pygame.draw.circle(win, WHITE, (int(x), int(y)), self.radius + 4, 2)

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

    def screen_position(self) -> Tuple[float, float]:
        """Return the current screen coordinates of the planet."""
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2
        return x, y

    def info_lines(self) -> List[str]:
        """Return formatted information lines for the info panel."""
        lines = [self.name]
        if self.sun:
            lines.append("Tipo: Estrella")
            lines.append(f"Masa: {self.mass:.2e} kg")
            return lines

        distance_au = self.distance_to_sun / self.AU if self.distance_to_sun else abs(math.sqrt(self.x**2 + self.y**2) / self.AU)
        speed = math.sqrt(self.x_vel**2 + self.y_vel**2) / 1000
        lines.extend(
            [
                "Tipo: Planeta",
                f"Distancia al Sol: {distance_au:.2f} AU",
                f"Masa: {self.mass:.2e} kg",
                f"Velocidad orbital: {speed:.2f} km/s",
            ]
        )
        return lines


def draw_info_panel(win: pygame.Surface, selected: Optional[Planet]) -> None:
    """Draw a side panel with information about the selected planet."""

    panel_width = 280
    panel_rect = pygame.Rect(WIDTH - panel_width - 20, 20, panel_width, 220)
    pygame.draw.rect(win, PANEL_BG, panel_rect, border_radius=10)
    pygame.draw.rect(win, PANEL_BORDER, panel_rect, width=2, border_radius=10)

    if selected is None:
        title_surface = FONT_TITLE.render("Información", True, WHITE)
        win.blit(title_surface, (panel_rect.x + 16, panel_rect.y + 16))
        message = "Haz clic en un planeta\npara ver sus datos"
        for i, line in enumerate(message.split("\n")):
            text_surface = FONT_TEXT.render(line, True, WHITE)
            win.blit(text_surface, (panel_rect.x + 16, panel_rect.y + 60 + i * 24))
        return

    lines = selected.info_lines()
    title_surface = FONT_TITLE.render(lines[0], True, WHITE)
    win.blit(title_surface, (panel_rect.x + 16, panel_rect.y + 16))

    for i, line in enumerate(lines[1:]):
        text_surface = FONT_TEXT.render(line, True, WHITE)
        win.blit(text_surface, (panel_rect.x + 16, panel_rect.y + 60 + i * 24))


def create_planets() -> List[Planet]:
    """Create the planets with initial positions and velocities."""
    sun = Planet("Sol", 0, 0, 30, YELLOW, 1.98892 * 10**30, sun=True)
    mercury = Planet("Mercurio", 0.387 * Planet.AU, 0, 8, DARK_GREY, 3.30 * 10**23, y_vel=-47.4 * 1000)
    venus = Planet("Venus", 0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**24, y_vel=-35.02 * 1000)
    earth = Planet("Tierra", -1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24, y_vel=29.783 * 1000)
    mars = Planet("Marte", -1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23, y_vel=24.077 * 1000)
    jupiter = Planet("Júpiter", -5.2 * Planet.AU, 0, 22, (222, 184, 135), 1.898 * 10**27, y_vel=13.06 * 1000)
    saturn = Planet("Saturno", 9.5 * Planet.AU, 0, 20, (238, 232, 170), 5.683 * 10**26, y_vel=-9.68 * 1000)
    uranus = Planet("Urano", -19.2 * Planet.AU, 0, 18, (173, 216, 230), 8.681 * 10**25, y_vel=6.80 * 1000)
    neptune = Planet("Neptuno", 30.1 * Planet.AU, 0, 18, (0, 0, 139), 1.024 * 10**26, y_vel=-5.43 * 1000)
    return [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]


def main() -> None:
    """Run the main simulation loop."""
    clock = pygame.time.Clock()
    planets = create_planets()
    selected_planet: Optional[Planet] = planets[0]
    run = True

    while run:
        clock.tick(60)
        WIN.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for planet in planets:
                    x, y = planet.screen_position()
                    distance = math.hypot(mouse_x - x, mouse_y - y)
                    if distance <= planet.radius + (6 if planet.sun else 0):
                        selected_planet = planet
                        break

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN, selected=planet is selected_planet)

        draw_info_panel(WIN, selected_planet)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()

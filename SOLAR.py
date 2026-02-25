import pygame
import math

pygame.init()

clock = pygame.time.Clock()

WIDTH = 2000
HEIGHT = 1000
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (176,224,230)
RED = (255, 0, 0)
BROWN = (150, 75, 0)
GREEN = (119, 116, 81)
ORANGE = (255, 165, 0)
TAN = (210, 180, 140)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (0, 0, 139)

screen = pygame.display.set_mode((WIDTH, HEIGHT)) #Width, height in tuple
 
pygame.display.set_caption("The Solar System")

class Planet:
    AU = 1.496e11           # 1 AU in meters
    G = 6.674e-11           # Gravitational constant
    SCALE = 250 / (1.496e11)  # Pixels per meter (200 pixels = 1 AU)
    TIMESTEP = 86400        # 1 day in seconds

    def __init__(self, name, color, mass, x, y, radius, y_vel=0 ):
        self.name = name
        self.color = color
        self.mass = mass
        self.x = x
        self.y = y
        self. radius = radius
        self.x_vel = 0
        self.y_vel = y_vel

sun_body = ("Sun", YELLOW, 1.989e30, 0, 0, 30)
mercury = Planet("Mercury", BROWN, 3.301e23, 0.387 * Planet.AU, 0, 8, 35020 )


planets = [
    sun_body,
    mercury, venus, earth, mars, jupiter, saturn, uranus, neptune,
    ceres, pluto, haumea, makemake, eris,]


running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    for planet in planets:
        planet.draw(screen)


    pygame.display.update()

    clock.tick(60)

pygame.quit()
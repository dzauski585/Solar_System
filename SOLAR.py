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
        self.radius = radius
        self.x_vel = 0
        self.y_vel = y_vel
        self.sun = False
    
    def draw(self, surface):
        screen_x = self.x * self.SCALE + WIDTH / 2
        screen_y = self.y * self.SCALE + HEIGHT / 2
        pygame.draw.circle(surface, self.color, (int(screen_x), int(screen_y)), self.radius)
        
    def attraction():
        '''
        METHOD attraction(other):
            dx = other.x - self.x
            dy = other.y - self.y
            distance = sqrt(dx^2 + dy^2)
            force = G * self.mass * other.mass / distance^2
            angle = atan2(dy, dx)
            RETURN (cos(angle) * force, sin(angle) * force)

        '''
        

sun_body = Planet("Sun", YELLOW, 1.989e30, 0, 0, 30)
sun_body.sun = True

mercury = Planet("Mercury", BROWN, 3.301e23, 0.387 * Planet.AU, 0, 8, 47360 )
venus    = Planet("Venus", GREEN, 4.867e24, 0.723 * Planet.AU, 0, 14, 35020)
earth    = Planet("Earth", BLUE, 5.972e24, 1.0 * Planet.AU, 0, 16, 29780)
mars     = Planet("Mars", RED, 6.417e23, 1.524 * Planet.AU, 0, 12, 24070)
jupiter  = Planet("Jupiter", ORANGE, 1.899e27, 5.203 * Planet.AU, 0, 28, 13070)
saturn   = Planet("Saturn", TAN, 5.685e26, 9.537 * Planet.AU, 0, 24, 9680)
uranus   = Planet("Uranus", LIGHT_BLUE, 8.681e25, 19.19 * Planet.AU, 0, 18, 6800)
neptune  = Planet("Neptune", DARK_BLUE, 1.024e26, 30.07 * Planet.AU, 0, 18, 5430)

ceres    = Planet("Ceres", (169, 169, 169), 9.39e20, 2.77 * Planet.AU, 0, 6, 17900)
pluto    = Planet("Pluto", (210, 180, 140), 1.303e22, 29.66 * Planet.AU, 0, 8, 6100)
haumea   = Planet("Haumea", (180, 160, 150), 4.006e21, 34.72 * Planet.AU, 0, 6, 5520)
makemake = Planet("Makemake", (160, 120, 100), 3.1e21, 38.59 * Planet.AU, 0, 6, 5240)
eris     = Planet("Eris", (200, 200, 210), 1.66e22, 37.91 * Planet.AU, 0, 8, 5580)

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
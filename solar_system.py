import pygame
import math
 
# Initialize pygame 
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
    def __init__(self, color, orbit_radius, planet_radius, speed, name):

        self.color = color
        self.orbit_radius = orbit_radius
        self.radius = planet_radius
        self.speed = speed  
        self.angle = 0
        self.name = name  
    
    def info(self):
        print(f"{self.name}: orbit = {self.orbit_radius}, speed = {self.speed}")
      '''  
    def attraction(self, other):
    # What are we calculating here?
    other_x, other_y = other.x, other.y
    distance_x = other_x - self.x
    distance_y = other_y - self.y
    
    # What is this calculating? What's the formula?
    distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
    
    # What special case is this handling?
    if other.sun:
        self.distance_to_sun = distance
    
    # What physics formula is this?
    force = self.G * self.mass * other.mass / distance ** 2
    
    # What are theta, force_x, and force_y?
    theta = math.atan2(distance_y, distance_x)
    force_x = math.cos(theta) * force
    force_y = math.sin(theta) * force
    
    return force_x, force_y

    '''
    def update(self):

        self.angle += self.speed
    
    def draw(self, surface, center_x, center_y):

        x = center_x + self.orbit_radius * math.cos(self.angle)
        y = center_y + self.orbit_radius * math.sin(self.angle)
        
        pygame.draw.circle(surface, self.color, (int(x), int(y)), self.radius)
        
    def draw_orbit(self, surface, center_x, center_y):
        pygame.draw.circle(surface, self.color, (center_x, center_y), self.orbit_radius, 1)  # 1 = line width (not filled)
    


def sun(surface, color, center_x, center_y, radius):
    x = center_x
    y = center_y
    
    
    pygame.draw.circle(surface, color, (x, y), radius)

mercury = Planet(BROWN, 60, 4, .02 / .24, "Mercury")
venus = Planet(GREEN, 100, 6, .02 / .62, "Venus")
earth = Planet(BLUE, 150, 6, .02, "Earth")
mars = Planet(RED, 250, 5, .02/1.88, "Mars")
jupiter = Planet(ORANGE, 350, 15, .02 / 11.86, "Jupiter")
saturn = Planet(TAN, 420, 12, .02 / 29.46, "Saturn")
uranus = Planet(LIGHT_BLUE, 470, 8, .02 / 84.01, "Uranus")
neptune = Planet(DARK_BLUE, 490, 8, .02 / 164.8, "Neptune")

planets = [mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]
    
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    screen.fill(BLACK)
 
    center_x = WIDTH // 2  # What operation finds the middle?
    center_y = HEIGHT // 2
    
    sun(screen, YELLOW, center_x, center_y, 30)
    
    for planet in planets:
        planet.draw_orbit(screen, center_x, center_y)
        planet.update()
        planet.draw(screen, center_x, center_y)
    
    

    pygame.display.update()
    clock.tick(60)  # Limits to 60 frames per second

pygame.quit()

import pygame
import math
 
angle = 0  # Starting angle in radians
earth_orbit_radius = 150  # Distance from center
mars_orbit_radius = 250
mars_angle = 0
 
# Initialize pygame 
pygame.init()

clock = pygame.time.Clock()

WIDTH = 2000
HEIGHT = 1000
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (176,224,230)
RED = (255, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT)) #Width, height in tuple
 
pygame.display.set_caption("The Solar System")


def sun(surface, color, center_x, center_y, radius):
    x = center_x
    y = center_y
    
    pygame.draw.circle(surface, color, (x, y), radius)

def planet(surface, color, center_x, center_y, orbit_radius, angle, radius):
    x = center_x + orbit_radius * math.cos(angle)
    y = center_y + orbit_radius * math.sin(angle)
    
    pygame.draw.circle(surface, color, (int((x)),int((y))), radius)
    return x, y

def orbit_path(surface, color, center_x, center_y, orbit_radius ):
    pygame.draw.circle(surface, color, (center_x, center_y), orbit_radius, 1)  # 1 = line width (not filled)

mars_trail = []
MAX_TRAIL = 590
def past_orbit_path():
    pass
    
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    screen.fill(BLACK)
 
    center_x = WIDTH // 2  # What operation finds the middle?
    center_y = HEIGHT // 2
    
    sun_radius = 30
    mercury_radius = 4
    venus_radius = 6
    earth_radius = 6
    mars_radius = 5
    jupiter_radius = 15
    saturn_radius = 12
    uranus_radius = 8
    neptune_radius = 8
    
    #pygame.draw.circle(screen, YELLOW, (center_x, center_y), sun_radius)
    sun(screen, YELLOW, center_x, center_y, sun_radius)

    #earth_x = center_x + orbit_radius * math.cos(angle)
    #earth_y = center_y + orbit_radius * math.sin(angle)
    
   #pygame.draw.circle(screen, BLUE, (int((earth_x)),int((earth_y))), earth_radius)
    earth_x, earth_y = planet(screen, BLUE, center_x, center_y, earth_orbit_radius, angle, earth_radius)
    orbit_path(screen, BLUE, center_x, center_y, earth_orbit_radius)
    mars_x, mars_y = planet(screen, RED, center_x, center_y, mars_orbit_radius, mars_angle, mars_radius)
    mars_trail.append((int (mars_x), int (mars_y)))
    if len (mars_trail) > MAX_TRAIL:
        mars_trail.pop(0)
    if len(mars_trail) > 1:
        pygame.draw.lines(screen, RED, False, mars_trail, 1)
    #mars_x = center_x + mars_orbit_radius * math.cos(mars_angle)
    #mars_y = center_y + mars_orbit_radius * math.sin(mars_angle)
    
    #pygame.draw.circle(screen, RED, (int((mars_x)), int((mars_y))), mars_radius)
    
    # Make it move - increase the angle slightly each frame
    angle += .02  
    mars_angle += .02/1.88 # mars year is 1.88 earth year




    pygame.display.update()
    clock.tick(60)  # Limits to 60 frames per second

pygame.quit()

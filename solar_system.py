import pygame
import math
 
angle = 0  # Starting angle in radians
orbit_radius = 150  # Distance from center

 
# Initialize pygame 
pygame.init()
 
WIDTH = 2000
HEIGHT = 1000
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (176,224,230)

screen = pygame.display.set_mode((WIDTH, HEIGHT)) #Width, height in tuple
 
pygame.display.set_caption("The Solar System")
 
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
    
    pygame.draw.circle(screen, YELLOW, (center_x, center_y), sun_radius)

    earth_x = center_x + orbit_radius * math.cos(angle)
    earth_y = center_y + orbit_radius * math.sin(angle)
    
    pygame.draw.circle(screen, BLUE, (int((earth_x)),int((earth_y))), earth_radius)
    
    # Make it move - increase the angle slightly each frame
    angle += .02  





    clock = pygame.time.Clock()
    clock.tick(60)  # Limits to 60 frames per second


    pygame.display.update()
 

pygame.quit()

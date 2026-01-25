import pygame
 
# Initialize pygame 
pygame.init()
 
WIDTH = 500
HEIGHT = 500
screen = pygame.display.set_mode((2000, 1000))
 
pygame.display.set_caption("The Solar System")
 
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


pygame.display.update()
 

pygame.quit()

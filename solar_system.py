import pygame
 
# Initialize pygame 
pygame.init()
 
WIDTH = 500
HEIGHT = 500
screen = pygame.display.set_mode((500, 500))
 
pygame.display.set_caption("The Solar System")
 
running = True
while running:
    for event in pygame.event.get():

    # Update the display - what function refreshes the screen?
        pygame.display.update()
 
# Clean up - what should you call when done with pygame?
pygame.quit()

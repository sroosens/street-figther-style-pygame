import pygame

# Init pygame
pygame.init()

# Configure screen size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Configure screen title
pygame.display.set_caption("Street Fighter Style")

# Configure background
bg_image = pygame.image.load("")

# Game loop
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

# Exit game
pygame.quit()
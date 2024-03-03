import pygame
from fighter import Fighter

# Init pygame
pygame.init()

# Configure screen size
SCREEN_WIDTH = 768
SCREEN_HEIGHT = 494

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Configure screen title
pygame.display.set_caption("Street Fighter Style")

# Set frame rate
clock = pygame.time.Clock()
FPS = 60

# Configure background
bg_image = pygame.image.load("assets/images/background/japan_1.png").convert_alpha()

# Function for drawing background
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0,0))

# Create instances of fighter
fighter_1 = Fighter(100, 280)
fighter_2 = Fighter(600, 280)

# Game loop
run = True
while run:

    clock.tick(FPS)

    # Draw background
    draw_bg()

    # Move fighters
    fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT)
    fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT)

    # Draw fighters
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Update display
    pygame.display.update()

# Exit game
pygame.quit()
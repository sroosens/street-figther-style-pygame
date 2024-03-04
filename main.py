import pygame
from fighter import Fighter

# Init pygame
pygame.init()

# Defines
SCREEN_WIDTH = 768
SCREEN_HEIGHT = 494
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
FONT = pygame.font.Font("assets/fonts/VCR_OSD_MONO_1.001.ttf", 30)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Configure screen title
pygame.display.set_caption("Street Fighter Style")

# Set frame rate
clock = pygame.time.Clock()
FPS = 60

# Game variables
score = [0, 0]
round_over = False

# Configure background
bg_image = pygame.image.load("assets/images/background/japan_1.png").convert_alpha()

# Function for drawing background
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0,0))

# Function for drawing fighter health bars
def draw_health_bar(health, x, y):
  ratio = health / 100
  pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 204, 34))
  pygame.draw.rect(screen, BLUE, (x, y, 200 * ratio, 30))

# Function for drawing texts
def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))

# Create instances of fighter
fighter_1 = Fighter(100, 280, 1)
fighter_2 = Fighter(600, 280, 2)

# Game loop
run = True
while run:

    clock.tick(FPS)

    # Draw background and HUD
    draw_bg()
    draw_health_bar(fighter_1.health, 20, 20)
    draw_health_bar(fighter_2.health, 544, 20)
    draw_text("P1: " + str(score[0]), FONT, WHITE, 20, 60)
    draw_text("P2: " + str(score[1]), FONT, WHITE, 580, 60)

    # Move fighters
    fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
    fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)

    # Update fighters logic
    fighter_1.update()
    fighter_2.update()

    # Draw fighters
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    # Manage rounds
    if round_over == False:
        if fighter_1.alive == False: # Increment P2 score and end the round
            score[1] += 1
            round_over = True
        if fighter_2.alive == False: # Increment P1 score and end the round
            score[0] += 1
            round_over = True

    # Event handlera
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Update display
    pygame.display.update()

# Exit game
pygame.quit()
import pygame

class Fighter():
    def __init__(self, x, y):
        self.rect = pygame.Rect((x, y, 80, 180))

    def move(self):
        # Speed
        SPEED = 5
        # Delta change
        dx = 0
        dy = 0
        # Keyboard
        key = pygame.key.get_pressed()
        # Movement
        if key[pygame.K_q]:
            dx = -SPEED
        if key[pygame.K_d]:
            dx = SPEED
        # Update fighter position
        self.rect.x += dx
        self.rect.y += dy

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)
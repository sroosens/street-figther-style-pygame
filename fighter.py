import pygame

class Fighter():
    def __init__(self, x, y):
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.jump = False

    def move(self, screen_width, screen_height):
        # Defines
        SPEED = 5
        GRAVITY = 2
        # Delta change
        dx = 0
        dy = 0
        # Keyboard
        key = pygame.key.get_pressed()
        # Movement
        if key[pygame.K_q]: # Left
            dx = -SPEED
        if key[pygame.K_d]: # Right
            dx = SPEED
        if key[pygame.K_z] and self.jump == False: # Jump
            self.vel_y = -30
            self.jump = True

        # Apply gravity
        self.vel_y += GRAVITY
        dy += self.vel_y 

        # Ensure fighter stays on screen
        if self.rect.left + dx < 0:                     # Left limit
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:         # Right limit
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 30:  # Bottom limit
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 30 - self.rect.bottom
        
        # Update fighter position
        self.rect.x += dx
        self.rect.y += dy

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)
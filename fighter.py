import pygame

class Fighter():
    def __init__(self, controls, flip, x, y):
        self.rect = pygame.Rect(x, y, 80, 180)
        self.vel_y = 0
        self.jump = False
        self.health = 100
        self.hit = False
        self.alive = True
        self.flip = flip
        self.attacking = False
        self.attack_cooldown = 0
        self.attack_type = 0 # 1: punch ; 2: kick
        self.controls = controls
        
    def move(self, screen_width, screen_height, debug_surf, target, round_over):
        # Defines
        SPEED = 5
        GRAVITY = 2
        # Delta change
        dx = 0
        dy = 0

        # Get key pressed
        key = pygame.key.get_pressed()

        if key[self.controls['left']]:
            dx = -SPEED
        elif key[self.controls['right']]:
            dx = SPEED
        elif key[self.controls['jump']] and not self.jump:
            self.vel_y = -30
            self.jump = True
        elif key[self.controls['attack1']] or key[self.controls['attack2']]:
            if key[self.controls['attack1']]:
                self.attack_type = 1
            if key[self.controls['attack2']]:
                self.attack_type = 2
            self.attack(debug_surf, target)

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

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

    def attack(self, debug_surf, target):
        if self.attack_cooldown == 0:
            self.attacking = True
            if self.attack_type == 1:
                print("punch")
                self.attack_cooldown = 10
                attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, self.rect.width * 2, self.rect.height / 2)
            elif self.attack_type == 2:
                print("kick")
                self.attack_cooldown = 15
                attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.centery, self.rect.width * 2, self.rect.height / 2)
            else:
                print("no attack")
                attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, self.rect.width * 2, self.rect.height)
        
            if attacking_rect.colliderect(target.rect):
                target.health -= 10
                target.hit = True
            pygame.draw.rect(debug_surf, (0, 255, 0), attacking_rect)

    def draw(self, surface, color):
        pygame.draw.rect(surface, color, self.rect)

    def update(self):
        if self.health <= 0:
            self.health = 0
            self.alive = False
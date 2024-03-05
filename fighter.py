import pygame

class Fighter():
    def __init__(self, controls, flip, x, y, sprite_sheet, animation_steps):
        self.rect = pygame.Rect(x, y, 70, 160)
        self.vel_y = 0
        self.size_x = 70
        self.size_y = 80
        self.image_scale = 2
        self.animation_list = self.fetch_sprites(sprite_sheet, animation_steps)
        self.action = 1
        self.offset = [15, 0]
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.health = 100
        self.hit = False
        self.alive = True
        self.flip = flip
        self.running = False
        self.jumping = False
        self.attacking = False
        self.punching = False
        self.crouching = False
        self.attack_cooldown = 0
        self.attack_type = 0 # 1: punch ; 2: kick
        self.controls = controls

    def fetch_sprites(self, sprite_sheet, animation_steps):
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size_x, y * self.size_y, self.size_x, self.size_y)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size_x * self.image_scale, self.size_y * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list

    def move(self, screen_width, screen_height, debug_surf, target, round_over):
        # Defines
        SPEED = 5
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        self.crouching = False
        self.rect.height = 160

        # Get key pressed
        key = pygame.key.get_pressed()

        if key[self.controls['left']]:
            dx = -SPEED
            self.running = True
        elif key[self.controls['right']]:
            dx = SPEED
            self.running = True
        elif key[self.controls['jump']] and not self.jumping:
            self.vel_y = -30
            self.jumping = True
        elif key[self.controls['crouch']]:
            self.crouching = True
            self.rect.height = 80
            self.rect.y = screen_height - 30
        elif key[self.controls['attack1']] or key[self.controls['attack2']]:
            if key[self.controls['attack1']]:
                self.attack_type = 1
            if key[self.controls['attack2']]:
                self.attack_type = 2
            self.attack(debug_surf, target)

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        else:
            self.punching = False
            self.attacking = False

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
            self.jumping = False
            dy = screen_height - 30 - self.rect.bottom
        
        # Update fighter position
        self.rect.x += dx
        self.rect.y += dy

    def attack(self, debug_surf, target):
        if self.attack_cooldown == 0 and not self.attacking:
            self.attacking = True
            if self.attack_type == 1:
                print("punch")
                self.attack_cooldown = 15
                self.punching = True
                attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y + 10, self.rect.width, self.rect.height / 4)
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
        img = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))

    def update(self):

        # Update actions
        if self.running:
            self.update_action(3)
        elif self.jumping:
            self.update_action(8)
        elif self.punching:
            self.update_action(2)
        elif self.crouching:
            self.update_action(9)
        else:
            self.update_action(1)

        # Update animation frames
        animation_cooldown = 100
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

        # Check if still alive
        if self.health <= 0:
            self.health = 0
            self.alive = False

    # Update current action with requested one
    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
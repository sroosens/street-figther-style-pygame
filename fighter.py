import pygame
import random

class Fighter():
    # Defines
    SPEED = 5
    GRAVITY = 2

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
        self.blocking = False
        self.attack_cooldown = 0
        self.attack_type = 0 # 1: punch ; 2: kick
        self.controls = controls

    @property
    def binx(self):
        return int(self.rect.centerx/64)

    def fetch_sprites(self, sprite_sheet, animation_steps):
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size_x, y * self.size_y, self.size_x, self.size_y)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size_x * self.image_scale, self.size_y * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list

    def move_player(self, screen_width, screen_height, debug_surf, target, round_over):
        # Reset variables
        dx = 0
        dy = 0
        self.running = False
        self.blocking = False
        self.attack_type = 0

        # Get key pressed
        key = pygame.key.get_pressed()

        if not self.attacking and self.alive and not round_over:
            if key[self.controls['crouch']]:
                self.blocking = True
            elif key[self.controls['left']]:
                dx = -self.SPEED
                self.running = True
            elif key[self.controls['right']]:
                dx = self.SPEED
                self.running = True
            elif key[self.controls['jump']] and not self.jumping:
                self.vel_y = -30
                self.jumping = True
            
            # Allow attack while doing movements    
            if key[self.controls['attack1']] or key[self.controls['attack2']]:
                self.attack(debug_surf, target)
                if key[self.controls['attack1']]:
                    self.attack_type = 1
                if key[self.controls['attack2']]:
                    self.attack_type = 2
        
        self.update_movement(dx, dy, screen_width, screen_height, target)

    def move_agent(self, screen_width, screen_height, debug_surf, target, round_over, action):
        # Reset variables
        dx = 0
        dy = 0
        self.running = False
        self.blocking = False
        self.rect.height = 160
        self.offset = [15, 0]

        # Get key pressed
        key = pygame.key.get_pressed()

        if not self.attacking and self.alive and not round_over:
            if action == 0: #left
                dx = -self.SPEED
                self.running = True
            if action == 1: # right
                dx = self.SPEED
                self.running = True
            if action == 2 and not self.jumping:
                self.vel_y = -30
                self.jumping = True
            if action == 3:
                self.blocking = True

            # Allow attack while doing movements    
            if action == 4 or action == 5:
                if action == 4:
                    self.attack_type = 1
                if action == 5:
                    self.attack_type = 2
                self.attack(debug_surf, target)
        
        self.update_movement(dx, dy, screen_width, screen_height, target)

    def move_basic_ai(self, screen_width, screen_height, debug_surf, target, round_over):
        dx = 0
        dy = 0
        self.running = False
        self.blocking = False
        self.attack_type = 0
        self.rect.height = 160
        self.offset = [15, 0]

        if not self.attacking and self.alive and not round_over:

            # Déterminer la direction vers laquelle l'IA doit se déplacer
            if target.rect.centerx > self.rect.centerx:
                dx = 3
            else:
                dx = -3

            # Sauter si trop proche du joueur
            if abs(target.rect.centerx - self.rect.centerx) > 100 and not self.jumping:
                self.vel_y = -30
                self.jumping = True

            # If close enough
            if abs(target.rect.centerx - self.rect.centerx) < 80:
                ran = random.random()
                if target.attack_cooldown > 0: # If opponent is attacking, block
                    self.blocking = True
                else: # Otherwise attack
                    self.attack_type = 1
                    self.attack(debug_surf, target)

        self.update_movement(dx, dy, screen_width, screen_height, target)

    def update_movement(self, dx, dy, screen_width, screen_height, target):
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True
    
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # Apply gravity
        self.vel_y += self.GRAVITY
        dy += self.vel_y 

        # Avoid figther to collide into target
        if self.rect.colliderect(target.rect):
            if self.rect.centerx < target.rect.centerx:
                self.rect.right = target.rect.left
            else:
                self.rect.left = target.rect.right

        # Ensure fighter stays on screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 30:
            self.vel_y = 0
            self.jumping = False
            dy = screen_height - 30 - self.rect.bottom

        # Update figther's position
        self.rect.x += dx
        self.rect.y += dy

    def attack(self, debug_surf, target):
        if self.attack_cooldown == 0: # and not self.attacking and not self.hit:
            self.attacking = True
            attacking_rect = pygame.Rect(self.rect.centerx - (self.rect.width * self.flip), self.rect.y + 10, self.rect.width, self.rect.height / 4)

            if attacking_rect.colliderect(target.rect):
                if not target.blocking:
                    target.health -= 10
                    target.hit = True
            pygame.draw.rect(debug_surf, (0, 255, 0), attacking_rect)

    def draw(self, surface, color):
        #pygame.draw.rect(surface, color, self.rect)
        img = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))

    def update(self):

        # Update actions
        # Check if still alive
        if self.health <= 0:
            self.health = 0
            self.alive = False
        elif self.hit:
            self.update_action(7)
        elif self.attacking:
            self.update_action(2)
        elif self.running:
            self.update_action(3)
        elif self.jumping:
            self.update_action(8)
        elif self.blocking:
            self.update_action(6)
        else:
            self.update_action(1)

        animation_cooldown = 50

        # Update image
        self.image = self.animation_list[self.action][self.frame_index]
        # Check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
            # Check if the animation has finished
        if self.frame_index >= len(self.animation_list[self.action]):
            # If the player is dead then end the animation
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                if self.action == 6:
                    self.frame_index = len(self.animation_list[self.action]) - 1
                else:
                    self.frame_index = 0
                # Check if an attack was executed
                if self.action == 2:
                    self.attacking = False
                    self.attack_cooldown = 40
                # Check if damage was taken
                if self.action == 7:
                    self.hit = False
                    # If the player was in the middle of an attack, then the attack is stopped
                    self.attacking = False
                    self.attack_cooldown = 30

        
    # Update current action with requested one
    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
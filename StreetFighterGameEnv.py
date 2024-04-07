import gym
from gym import spaces
from gym.spaces import Box, Dict
import numpy as np
import pygame
from fighter import Fighter

# Defines
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
ORANGE = (255, 127, 39)
PURPLE = (196, 0, 249)
FONT = 0
CHARA_ANIMATION_STEPS = [5, 3, 3, 5, 1, 1, 1, 1, 7, 1]

# Action keys
controls_p1 = {
            'left': pygame.K_q,
            'right': pygame.K_d,
            'jump': pygame.K_z,
            'crouch': pygame.K_s,
            'attack1': pygame.K_a,
            'attack2': pygame.K_e
        }

controls_p2 = {
            'left': pygame.K_k,
            'right': pygame.K_m,
            'jump': pygame.K_o,
            'crouch' : pygame.K_l,
            'attack1': pygame.K_i,
            'attack2': pygame.K_p
        }

class SFGameEnv(gym.Env):

    def __init__(self):
        super(SFGameEnv, self).__init__()

        pygame.init()

        # Configure screen
        pygame.display.set_caption("Street Fighter Style")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        # Configure background
        self.bg_image = pygame.image.load("assets/images/background/japan_1.png").convert_alpha()
        # Load sprite sheets
        self.chara_sheet_p1 = pygame.image.load("assets/sprites/ken.png").convert_alpha()
        self.chara_sheet_p2 = pygame.image.load("assets/sprites/ken_2.png").convert_alpha()
        self.font = pygame.font.Font("assets/fonts/VCR_OSD_MONO_1.001.ttf", 30)

        # Set frame rate
        #self.clock = pygame.time.Clock()
        #self.FPS = 60

        self.score = [0, 0]

        # Setup available actions
        self.action_space = spaces.Discrete(5)
        # Setup available observations
        self.observation_space = spaces.MultiDiscrete([10+1, 10+1, 10+1, 10+1], dtype=int) #health p1, health p2, p1.x, p2.x, p1.endattack
    
    # Function for drawing background
    def draw_bg(self):
        scaled_bg = pygame.transform.scale(self.bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.blit(scaled_bg, (0,0))

    # Function for drawing fighter health bar
    def draw_health_bar(self, health, x, y, flip):
        ratio = health / 100
        bar_width = 200 * ratio
        if flip:
            pygame.draw.rect(self.screen, WHITE, (x, y - 2, 204, 34))
            pygame.draw.rect(self.screen, RED, (x + 202 - bar_width, y, bar_width, 30))
        else:
            pygame.draw.rect(self.screen, WHITE, (x - 2, y - 2, 204, 34))
            pygame.draw.rect(self.screen, PURPLE, (x, y, bar_width, 30))

    # Function for drawing texts
    def draw_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self.screen.blit(img, (x, y))

    def reset(self):
        # Game variables
        self.round_over = False
        # Create instances of fighter
        self.fighter_1 = Fighter(controls_p1, False, 100, 280, self.chara_sheet_p1, CHARA_ANIMATION_STEPS)
        self.fighter_2 = Fighter(controls_p2, True, 600, 280, self.chara_sheet_p2, CHARA_ANIMATION_STEPS)

        return self._get_obs(), self._get_info()
        

    def step(self, action):
        self.fighter_1.move_basic_ai(SCREEN_WIDTH, SCREEN_HEIGHT, self.screen, self.fighter_2, self.round_over)
        #self.fighter_2.move_basic_ai(SCREEN_WIDTH, SCREEN_HEIGHT, self.screen, self.fighter_1, self.round_over)
        self.fighter_2.move_agent(SCREEN_WIDTH, SCREEN_HEIGHT, self.screen, self.fighter_1, self.round_over, action)

        info = self._get_info()
        obs = self._get_obs()

        # Manage rounds
        if self.round_over == False:
            if self.fighter_1.alive == False: # Increment P2 score and end the round
                self.score[1] += 1
                self.round_over = True
            if self.fighter_2.alive == False: # Increment P1 score and end the round
                self.score[0] += 1
                self.round_over = True

        reward = self.compute_reward()

        #if self.render_mode == "human":
        self.render()

        return obs, reward, self.round_over, info
    
    def compute_reward(self):
        reward = -10
        if self.round_over:
            if self.fighter_2.alive:
                print("win")
                reward +=500
            else:
                print("loose")
                reward -=500
        elif self.fighter_2.health < self.fighter_1.health:
            reward -= 10
        elif self.fighter_2.health > self.fighter_1.health:
            reward +=10

        distance = abs(self.fighter_1.binx - self.fighter_2.binx)
        reward += (1 / (distance+1)) * 50

        if (self.fighter_1.binx < 1) or (SCREEN_WIDTH / 64) - self.fighter_1.binx < 1:
            reward -= 20

        return reward
    
    def _get_info(self):
        return {}
    
    def _get_obs(self):
        return np.array([ round(self.fighter_1.health / 10), 
                          round(self.fighter_2.health / 10), 
                          self.fighter_1.binx, 
                          self.fighter_2.binx])
                          #(self.fighter_1.attack_cooldown > 5)])


    def render(self):
        # Draw background and HUD
        self.draw_bg()
        self.draw_health_bar(self.fighter_1.health, 20, 20, True)
        self.draw_health_bar(self.fighter_2.health, 406, 20, False)
        self.draw_text("P1: " + str(self.score[0]), self.font, WHITE, 50, 60)
        self.draw_text("AGENT : " + str(self.score[1]), self.font, WHITE, 400, 60)
        self.draw_text("KO", self.font, RED, 300, 20)
        # Update fighters logic
        self.fighter_1.update()
        self.fighter_2.update()
        # Draw fighters
        self.fighter_1.draw(self.screen, RED)
        self.fighter_2.draw(self.screen, BLUE)

        pygame.display.update()

    def close(self):
        print("close")
        pygame.quit()

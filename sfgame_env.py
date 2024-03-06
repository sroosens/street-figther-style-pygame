import gym
from gym import spaces
from gym.spaces import Box, Dict
import numpy as np
import pygame
from fighter import Fighter

# Defines
SCREEN_WIDTH = 768
SCREEN_HEIGHT = 494
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
ORANGE = (255, 127, 39)
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
        self.chara_sheet = pygame.image.load("assets/sprites/ken.png").convert_alpha()
        self.font = pygame.font.Font("assets/fonts/VCR_OSD_MONO_1.001.ttf", 30)

        # Set frame rate
        #self.clock = pygame.time.Clock()
        #self.FPS = 60

        self.reset()

        # Setup available actions
        self.action_space = spaces.Discrete(5)

        spaces_obs = {
            'score_p1': Box(low=0, high=10, shape=(9,), dtype=np.int32),
            'score_p2': Box(low=0, high=10, shape=(9,), dtype=np.int32),
            'pos_x_p1': Box(low=0, high=1000, shape=(999,), dtype=np.int32),
            'pos_x_p2': Box(low=0, high=1000, shape=(999,), dtype=np.int32),
            'health_p1': Box(low=0, high=100, shape=(99,), dtype=np.int32),
            'health_p2': Box(low=0, high=100, shape=(99,), dtype=np.int32),
            }
        # Setup observations infos
        self.observation_space = Dict(spaces_obs)
    
    # Function for drawing background
    def draw_bg(self):
        scaled_bg = pygame.transform.scale(self.bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.blit(scaled_bg, (0,0))

    # Function for drawing fighter health bar
    def draw_health_bar(self, health, x, y, flip):
        ratio = health / 100
        bar_width = 340 * ratio
        if flip:
            pygame.draw.rect(self.screen, WHITE, (x, y - 2, 344, 34))
            pygame.draw.rect(self.screen, ORANGE, (x + 342 - bar_width, y, bar_width, 30))
        else:
            pygame.draw.rect(self.screen, WHITE, (x - 2, y - 2, 344, 34))
            pygame.draw.rect(self.screen, ORANGE, (x, y, bar_width, 30))

    # Function for drawing texts
    def draw_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self.screen.blit(img, (x, y))

    def reset(self):
        print("reset")
        # Game variables
        self.score = [0, 0]
        self.round_over = False
        # Create instances of fighter
        self.fighter_1 = Fighter(controls_p1, False, 100, 280, self.chara_sheet, CHARA_ANIMATION_STEPS)
        self.fighter_2 = Fighter(controls_p2, True, 600, 280, self.chara_sheet, CHARA_ANIMATION_STEPS)

    def step(self, action):
        self.fighter_1.move_player(SCREEN_WIDTH, SCREEN_HEIGHT, self.screen, self.fighter_2, self.round_over)
        self.fighter_2.move_basic_ai(SCREEN_WIDTH, SCREEN_HEIGHT, self.screen, self.fighter_1, self.round_over)
        #self.fighter_2.move_agent(SCREEN_WIDTH, SCREEN_HEIGHT, self.screen, self.fighter_1, self.round_over, action)

        reward = self.compute_reward()
        obs = self.compute_obs()

        # Manage rounds
        if self.round_over == False:
            if self.fighter_1.alive == False: # Increment P2 score and end the round
                self.score[1] += 1
                self.round_over = True
            if self.fighter_2.alive == False: # Increment P1 score and end the round
                self.score[0] += 1
                self.round_over = True
        
        return obs, reward, self.round_over, {}
    
    def compute_reward(self):
        reward = 0
        return reward
    
    def compute_obs(self):
        # Update observations
        obs = {
            'score_p1': self.score[0],
            'score_p2': self.score[1],
            'pos_x_p1' : self.fighter_1.rect.centerx,
            'pos_x_p2' : self.fighter_2.rect.centerx,
            'health_p1': self.fighter_1.health,
            'health_p2': self.fighter_2.health
            }
        return obs


    def render(self):
        # Draw background and HUD
        self.draw_bg()
        self.draw_health_bar(self.fighter_1.health, 20, 20, True)
        self.draw_health_bar(self.fighter_2.health, 406, 20, False)
        self.draw_text("P1: " + str(self.score[0]), self.font, WHITE, 50, 60)
        self.draw_text("P2: " + str(self.score[1]), self.font, WHITE, 620, 60)
        self.draw_text("KO", self.font, RED, 366, 20)
        # Update fighters logic
        self.fighter_1.update()
        self.fighter_2.update()
        # Draw fighters
        self.fighter_1.draw(self.screen, RED)
        self.fighter_2.draw(self.screen, BLUE)

        pygame.display.update()

    def close(self):
        print("close")
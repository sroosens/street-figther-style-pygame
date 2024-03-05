import gym
from gym import spaces
import numpy as np
import pygame
from fighter import Fighter

# Defines
SCREEN_WIDTH = 768
SCREEN_HEIGHT = 494
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
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

    def __init__(self, test):
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

        # Game variables
        self.score = [0, 0]
        self.round_over = False

        # Create instances of fighter
        self.fighter_1 = Fighter(controls_p1, False, 100, 280, self.chara_sheet, CHARA_ANIMATION_STEPS)
        self.fighter_2 = Fighter(controls_p2, True, 600, 280, self.chara_sheet, CHARA_ANIMATION_STEPS)

        # Setup available actions
        self.action_space = spaces.Discrete(5)
        # Setup observations infos
        self.observation_space = spaces.Discrete(2)
    
    # Function for drawing background
    def draw_bg(self):
        scaled_bg = pygame.transform.scale(self.bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.blit(scaled_bg, (0,0))

    # Function for drawing fighter health bar
    def draw_health_bar(self, health, x, y):
        ratio = health / 100
        pygame.draw.rect(self.screen, WHITE, (x - 2, y - 2, 204, 34))
        pygame.draw.rect(self.screen, BLUE, (x, y, 200 * ratio, 30))

    # Function for drawing texts
    def draw_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self.screen.blit(img, (x, y))

    def reset(self):
        print("reset")

    def step(self, action):
        self.fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, self.screen, self.fighter_2, self.round_over)
        self.fighter_2.move_agent(SCREEN_WIDTH, SCREEN_HEIGHT, self.screen, self.fighter_1, self.round_over, action)

        if action == 0:
            print("action 0")
        elif action == 1: 
            print("action 1")
        elif action == 2:
            print("action 2")
        elif action == 3:
            print("action 3")
        print("step")
        reward = 1.0
        done = True
        return 0, reward, done, {}

    def render(self):
        print("render")
        # Draw background and HUD
        self.draw_bg()
        self.draw_health_bar(self.fighter_1.health, 20, 20)
        self.draw_health_bar(self.fighter_2.health, 544, 20)
        self.draw_text("P1: " + str(self.score[0]), self.font, WHITE, 20, 60)
        self.draw_text("P2: " + str(self.score[1]), self.font, WHITE, 580, 60)
        # Update fighters logic
        self.fighter_1.update()
        self.fighter_2.update()
        # Draw fighters
        self.fighter_1.draw(self.screen, RED)
        self.fighter_2.draw(self.screen, BLUE)

        pygame.display.update()

    def close(self):
        print("close")
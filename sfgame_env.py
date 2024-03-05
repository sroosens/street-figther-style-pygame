import gym
from gym import spaces
import numpy as np
import pygame


class SFGameEnv(gym.Env):
    def __init__(self, test):
        super(SFGameEnv, self).__init__()

        pygame.init()

        # Defines
        SCREEN_WIDTH = 768
        SCREEN_HEIGHT = 494
        RED = (255, 0, 0)
        BLUE = (0, 0, 255)
        WHITE = (255, 255, 255)
        FONT = pygame.font.Font("assets/fonts/VCR_OSD_MONO_1.001.ttf", 30)

        # Configure screen
        pygame.display.set_caption("Street Fighter Style")
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        # Set frame rate
        clock = pygame.time.Clock()
        FPS = 60

        # Game variables
        score = [0, 0]
        round_over = False

        # Configure background
        bg_image = pygame.image.load("assets/images/background/japan_1.png").convert_alpha()
        # Load sprite sheets
        chara_sheet = pygame.image.load("assets/sprites/ken.png").convert_alpha()
        # Define number of steps in each animation
        CHARA_ANIMATION_STEPS = [5, 3, 3, 5, 1, 1, 1, 1, 7, 1]

        # Setup available actions
        self.action_space = spaces.Discrete(5)
        # Setup observations infos
        self.observation_space = spaces.Discrete(2)

#            spaces.Dict(
#            {
#                "figher_1_health" : spaces.Box(0, score, dtype=int),
#                "score": spaces.Box(0, score, dtype=int),
#            }
#        )
    
    def reset(self):
        print("reset")

    def step(self, action):
        if action == 0:
            print("action 0")
        elif action == 1: 
            print("action 1")
        elif action == 2:
            print("action 2")
        elif action == 3:
            print("action 3")
        print("step")

    def render(self):
        print("render")
        pygame.display.update()

    def close(self):
        print("close")
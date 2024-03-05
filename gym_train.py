import gym
from sfgame_env import SFGameEnv
import pygame

# Register the environment
gym.register(
    id='SFGame-v0',
    entry_point='sfgame_env:SFGameEnv', 
    kwargs={'test': None} 
)

test = [0]

# Test the environment
env = gym.make('SFGame-v0', test=test)
obs = env.reset()
env.render()

# Set frame rate
clock = pygame.time.Clock()
FPS = 60

done = False
run = True
while run:
    clock.tick(FPS)
    action = env.action_space.sample()  # Random action selection
    obs, reward, done, _ = env.step(action)
    env.render()
    print('Reward:', reward)
    print('Done:', done)

    # Event handlera
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #pygame.time.wait(10)
    
# Exit game
pygame.quit()
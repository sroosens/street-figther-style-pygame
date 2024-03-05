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

done = False
while True:
    pygame.event.get()
    action = env.action_space.sample()  # Random action selection
    obs, reward, done, _ = env.step(action)
    env.render()
    print('Reward:', reward)
    print('Done:', done)

    pygame.time.wait(200)
import gym
from game_environment import GameEnv

# Register the environment
gym.register(
    id='SFGame-v0',
    entry_point='game_environment:GameEnv', 
    kwargs={'test': None} 
)

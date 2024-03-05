import gym
from sfgame_env import SFGameEnv

# Register the environment
gym.register(
    id='SFGame-v0',
    entry_point='sfgame_env:SFGameEnv', 
    kwargs={'test': None} 
)

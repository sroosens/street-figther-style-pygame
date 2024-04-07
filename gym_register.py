import gym
from StreetFighterGameEnv import SFGameEnv

# Register the environment
gym.register(
    id='SFGame-v0',
    entry_point='StreetFighterGameEnv:SFGameEnv', 
    kwargs={'test': None} 
)

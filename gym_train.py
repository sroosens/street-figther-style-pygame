import gym
from sfgame_env import SFGameEnv
import pygame

# Register the environment
gym.register(
    id='SFGame-v0',
    entry_point='sfgame_env:SFGameEnv', 
    kwargs={} 
)

test = [0]

# Test the environment
env = gym.make('SFGame-v0')
obs_t = env.reset()
env.render()

# Set frame rate
clock = pygame.time.Clock()
FPS = 60

done = False

# Run the session X times
for i in range(1, 10):
    print(f"Episode: {i}")
    obs_t = env.reset()
    done = False

    # Train
    while not done:
        clock.tick(FPS)
        action = env.action_space.sample()  # Random action selection
        obs, reward, done, _ = env.step(action)
        env.render()

        #print('Reward:', reward)
        #print('Done:', done)
        #print('Observations:', obs)

        # Event handlera
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        #pygame.time.wait(10)
            
print("Game terminated")
# Exit game
pygame.quit()
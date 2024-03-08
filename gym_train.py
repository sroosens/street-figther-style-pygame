import gym
from sfgame_env import SFGameEnv
import pygame
import numpy as np
import random

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
stop = False

#
# Q Table implementation
#
q_table = np.zeros([len(env.observation_space.spaces), env.action_space.n])

# Hyperparameters
alpha = 0.1
gamma = 0.6
epsilon = 0.1

# For plotting metrics
all_epochs = []
all_penalties = []

print("Beging training.\n")

# Run the session X times
for i in range(1, 10):
    print(f"Episode: {i}")
    state = env.reset()

    epochs, penalties, reward, = 0, 0, 0

    done = False
    
    if stop:
        break

    # Train
    while not done:
        clock.tick(FPS)

        # action = env.action_space.sample()

        if random.uniform(0, 1) < epsilon:
            action = env.action_space.sample() # Explore action space
        else:
            action = np.argmax(q_table[state]) # Exploit learned values

        next_state, reward, done, info = env.step(action)

        old_value = q_table[state, action]
        next_max = np.max(q_table[next_state])
        
        new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
        q_table[state, action] = new_value

        if reward < 0:
            penalties += 1

        state = next_state
        epochs += 1
        
        print(f"Observations: {info}, Reward: {reward}")

        # Event handlera
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop = True
                done = True

        #pygame.time.wait(10)

print("Training finished.\n")
print("Penalties incurred: {}".format(penalties))

# Exit game
pygame.quit()
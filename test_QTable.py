import gym
from game_environment import GameEnv
import pygame
import numpy as np
import matplotlib.pyplot as plt

# Register the environment
gym.register(
    id='SFGame-v0',
    entry_point='game_environment:GameEnv', 
    kwargs={} 
)

# Load the trained Q-table
q_table = np.load('weights/QLearning/q_table_v1.npy')

# Test the environment
env = gym.make('SFGame-v0')
obs_t = env.reset()
env.render()

# Set frame rate
clock = pygame.time.Clock()
FPS = 120

done = False
stop = False

# For plotting metrics
rewards_per_episode = []
winrate_per_episode = []

print("Begin testing.\n")

# Run the session
for i in range(1, 100):
    print(f"Episode: {i}")
    state = env.reset()[0]
    epochs, penalties, reward = 0, 0, 0
    done = False
    
    if stop:
        break

    while not done:
        clock.tick(FPS)
        action = np.argmax(q_table[np.ravel_multi_index(state, env.observation_space.nvec)])
        next_state, reward, done, _ = env.step(action)
        state = next_state
        epochs += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop = True
                done = True

    # Append the reward and win rate for this episode
    rewards_per_episode.append(reward)
    if env.score[0] != 0:
        winrate_per_episode.append(env.score[1] / env.score[0])
    else:
        winrate_per_episode.append(env.score[1])
    print("K/D Ratio: ", winrate_per_episode[-1])

print("Testing finished.\n")

# Plot rewards per episode
plt.plot(rewards_per_episode)
plt.xlabel('Episode')
plt.ylabel('Reward')
plt.title('Reward per Episode')
plt.show()

# Plot winrate per episode
plt.plot(winrate_per_episode)
plt.xlabel('Episode')
plt.ylabel('K/D Ratio')
plt.title('K/D Ratio per Episode')
plt.show()

print("Scores: ", env.score)
print("Penalties incurred: {}".format(penalties))

# Exit game
pygame.quit()
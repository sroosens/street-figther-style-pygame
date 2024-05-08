import gym
from game_environment import GameEnv
import pygame
import numpy as np
import matplotlib.pyplot as plt

#
# Q Table Learning
# Q-Table is just a fancy name for a simple lookup table where we calculate the maximum expected future rewards for action at each state. 
# Basically, this table will guide us to the best action at each state.
#

# Register the environment
gym.register(
    id='SFGame-v0',
    entry_point='game_environment:GameEnv', 
    kwargs={} 
)

#q_table = np.load('q_table_v1.npy')

# Test the environment
env = gym.make('SFGame-v0')
obs_t = env.reset()
env.render()

# Set frame rate
clock = pygame.time.Clock()
FPS = 120

done = False
stop = False

#
# Q Table implementation
#
q_table = np.zeros((env.observation_space.nvec.prod(), env.action_space.n))
print("Q-Table shape:", q_table.shape)

# Q-learning parameters
alpha = 0.1  # Learning rate
gamma = 0.99  # Discount factor
epsilon = 0.1  # Exploration rate

# For plotting metrics
all_epochs = []
all_penalties = []

print("Beging training.\n")

rewards_per_episode = []
winrate_per_episode = []

# Run the session X times
for i in range(1, 1000):
    print(f"Episode: {i}")
    state = env.reset()[0]
    epochs, penalties, reward = 0, 0, 0
    done = False
    
    if stop:
        break

    # Train
    while not done:
        clock.tick(FPS)
        # Epsilon-greedy action selection
        if np.random.rand() < epsilon:
            action = env.action_space.sample()  # Explore action space
        else:
            action = np.argmax(q_table[np.ravel_multi_index(state, env.observation_space.nvec)])  # Exploit learned values

        next_state, reward, done, _ = env.step(action)

        best_next_action = np.argmax(q_table[np.ravel_multi_index(next_state, env.observation_space.nvec)])
        td_target = reward + gamma * q_table[np.ravel_multi_index(next_state, env.observation_space.nvec)][best_next_action]
        td_error = td_target - q_table[np.ravel_multi_index(state, env.observation_space.nvec)][action]
        q_table[np.ravel_multi_index(state, env.observation_space.nvec)][action] += alpha * td_error

        state = next_state
        epochs += 1

        # Event handlera
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop = True
                done = True

        #pygame.time.wait(10)
    
    # Append the reward and win rate for this episode
    rewards_per_episode.append(reward)
    if env.score[0] != 0:
        winrate_per_episode.append(env.score[1] / env.score[0])
    else :
        winrate_per_episode.append(env.score[1])
    print("K/D Ratio: ", winrate_per_episode[-1])

print("Training finished.\n")

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

print(q_table.shape)
#for i in range(q_table.shape[0]):
#    if np.sum(q_table[i,:]):
#        print(q_table[i,:])

for i in range(q_table.shape[1]):
    print("action", i, ":",np.sum(q_table[:,i]))

print("Scores: ", env.score)
print("Penalties incurred: {}".format(penalties))

# Save q table trained
np.save('weights/QLearning/q_table_v2.npy', q_table)

# Exit game
pygame.quit()
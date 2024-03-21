import gym
from sfgame_env import SFGameEnv
import pygame
import numpy as np

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
FPS = 320

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

# Run the session X times
for i in range(1, 500):
    print(f"Episode: {i}")
    state = env.reset()[0]
    epochs, penalties, reward, = 0, 0, 0
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

print("Training finished.\n")

print(q_table.shape)
for i in range(q_table.shape[0]):
    if np.sum(q_table[i,:]):
        print(q_table[i,:])

for i in range(q_table.shape[1]):
    print("action", i, ":",np.sum(q_table[:,i]))


print("Scores: ", env.score)
print("Penalties incurred: {}".format(penalties))

# Exit game
pygame.quit()
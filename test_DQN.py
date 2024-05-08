import gym
import pygame
import numpy as np
import matplotlib.pyplot as plt
from game_environment import GameEnv
from agent_DQN import DQNAgent

# Register the environment
gym.register(
    id='SFGame-v0',
    entry_point='game_environment:GameEnv', 
    kwargs={} 
)

# Test the environment
env = gym.make('SFGame-v0')
obs_t = env.reset()
env.render()

# Set frame rate
clock = pygame.time.Clock()
FPS = 120

done = False
stop = False

# Load model
load_path = "weights/DQN/StreetFighter-v1.ckpt"

agent = DQNAgent(  n_y=env.action_space.n,
                    n_x=env.observation_space.shape[0],
                    learning_rate=0.01,
                    replace_target_iter=100,
                    memory_size=250,
                    batch_size=32,
                    epsilon_max=0.9,
                    epsilon_greedy_increment=0.001,
                    load_path = load_path
                )

# For plotting metrics
all_epochs = []
all_penalties = []

agent.saver.restore(agent.sess, load_path)

print("Beging Testing.\n")

rewards_per_episode = []
winrate_per_episode = []

# Run the session X times
for i in range(1, 100):
    print(f"Episode: {i}")
    observation = env.reset()[0]
    epochs, penalties, reward = 0, 0, 0
    done = False
    
    if stop:
        break

    # Train
    while True:
        clock.tick(FPS)
        
        # Choose one action based on observation
        action = agent.choose_action(observation)
        # Pass the chosen action in the environment
        observation_, reward, done, info = env.step(action)

        if done:
            # Append the reward and win rate for this episode
            rewards_per_episode.append(reward)
            if env.score[0] != 0:
                winrate_per_episode.append(env.score[1] / env.score[0])
            else :
                winrate_per_episode.append(env.score[1])
            print("K/D Ratio: ", winrate_per_episode[-1])
            break

        # Save observation
        observation = observation_

        # Event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop = True
                done = True

print("Testing finished.\n")

# Plot winrate per episode
plt.plot(winrate_per_episode)
plt.xlabel('Episode')
plt.ylabel('K/D Ratio')
plt.title('K/D Ratio per Episode')
plt.show()

print("Scores: ", env.score)
print("Penalties incurred: {}".format(penalties))

agent.plot_cost()

# Exit game
pygame.quit()
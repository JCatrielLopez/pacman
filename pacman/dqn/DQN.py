import os
import random
import time

import numpy as np
from tqdm import tqdm

from dqn.Agent import DQNAgent
from game import GameEnv

DISCOUNT = 0.99
REPLAY_MEMORY_SIZE = 50_000  # How many last steps to keep for model training
MINIBATCH_SIZE = 64  # How many steps (samples) to use for training
UPDATE_TARGET_EVERY = 5  # Terminal states (end of episodes)
MODEL_NAME = '2x256'
MIN_REWARD = 0  # For model save
MEMORY_FRACTION = 0.20

# Environment settings
EPISODES = 600

# Exploration settings
epsilon = 1  # not a constant, going to be decayed
EPSILON_DECAY = 0.99975
MIN_EPSILON = 0.001

#  Stats settings
AGGREGATE_STATS_EVERY = 50

# For stats
ep_rewards = [-200]

# For more repetitive results
random.seed(1)
np.random.seed(1)

# Create models folder
if not os.path.isdir('models'):
    os.makedirs('models')

agent = DQNAgent()
env = GameEnv()

# Iterate over episodes
for episode in tqdm(range(1, EPISODES + 1), ascii=True, unit='episodes'):

    agent.tensorboard.step = episode

    episode_reward = 0
    step = 1

    current_state = env.reset()

    done = False
    while not done:
        # print(f"\rSteps: {step}", end='')
        if np.random.random() > epsilon:
            action = np.argmax(agent.get_qs(current_state))
        else:
            action = np.random.randint(0, agent.action_space)

        new_state, reward, done = env.step(action)

        episode_reward += reward

        # env.render()

        # print("update replay memory...")
        agent.update_replay_memory((current_state, action, reward, new_state, done))
        # print("training...")
        agent.train(done, step)

        current_state = new_state
        step += 1

    ep_rewards.append(episode_reward)
    if not episode % AGGREGATE_STATS_EVERY or episode == 1:

        average_reward = sum(ep_rewards[-AGGREGATE_STATS_EVERY:]) / len(ep_rewards[-AGGREGATE_STATS_EVERY:])
        min_reward = min(ep_rewards[-AGGREGATE_STATS_EVERY:])
        max_reward = max(ep_rewards[-AGGREGATE_STATS_EVERY:])
        # print("update stats...")
        agent.tensorboard.update_stats(reward_avg=average_reward, reward_min=min_reward, reward_max=max_reward,
                                       epsilon=epsilon)

        if min_reward >= MIN_REWARD:
            agent.model.save(
                f'models/{MODEL_NAME}__{max_reward:_>7.2f}max_{average_reward:_>7.2f}avg_{min_reward:_>7.2f}min__{int(time.time())}.model')

    # Decay epsilon
    if epsilon > MIN_EPSILON:
        epsilon *= EPSILON_DECAY
        epsilon = max(MIN_EPSILON, epsilon)

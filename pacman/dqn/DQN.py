import logging
import os
import random

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tensorflow.python.summary.summary_iterator import summary_iterator
from tqdm import tqdm

from pacman.dqn.Agent import DQNAgent
from pacman.game import GameEnv

logging.basicConfig(
    filename="logs/logfile.log", format="%(levelname)s:%(name)s:%(message)s)"
)
logging.getLogger("matplotlib").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class DQN:
    def __init__(self, render):
        self.model_name = "pacman-v1"
        self.min_reward = 0

        self.episodes = 600

        self.epsilon = 1
        self.epsilon_decay = 0.99975
        self.min_epsilon = 0.001

        self.aggregate_stats_every = 5
        self.ep_rewards = [self.min_reward]

        self.max_steps_per_episode = 2500
        random.seed(21022020)
        np.random.seed(21022020)

        if not os.path.isdir("models"):
            os.makedirs("models")

        if not os.path.isdir("logs"):
            os.makedirs("logs")

        self.agent = DQNAgent()
        self.render_scene = render
        self.env = GameEnv()

    def run(self, show_metrics=False):

        metrics_df = pd.DataFrame(
            index=[np.arange(0, self.episodes // self.aggregate_stats_every)],
            columns=("episode", "avg_reward", "max_reward", "min_reward"),
        )
        row_index = 0

        for episode in tqdm(range(1, self.episodes + 1), ascii=True, unit="episodes"):

            self.agent.tensorboard.step = episode

            episode_reward = 0
            step = 1

            current_state = self.env.reset()

            done = False
            while not done:
                if np.random.random() > self.epsilon:
                    action = np.argmax(self.agent.get_qs(current_state))
                else:
                    action = np.random.randint(0, self.agent.action_space)

                new_state, reward, done = self.env.step(action)

                episode_reward += reward

                if self.render_scene:
                    self.env.render()

                self.agent.update_replay_memory(
                    (current_state, action, reward, new_state, done)
                )

                self.agent.train(done, step)

                current_state = new_state
                step += 1

                done = done or (step >= self.max_steps_per_episode)

            self.ep_rewards.append(episode_reward)
            if not episode % self.aggregate_stats_every or episode == 1:

                average_reward = sum(
                    self.ep_rewards[-self.aggregate_stats_every:]
                ) / len(self.ep_rewards[-self.aggregate_stats_every:])
                min_reward = min(self.ep_rewards[-self.aggregate_stats_every:])
                max_reward = max(self.ep_rewards[-self.aggregate_stats_every:])

                metrics_df.iloc[row_index] = [
                    episode,
                    average_reward,
                    max_reward,
                    min_reward,
                ]
                row_index += 1

                if show_metrics:
                    plt.plot(
                        "episode",
                        "max_reward",
                        data=metrics_df,
                        marker="o",
                        color="green",
                        linewidth=2,
                        label="max",
                    )
                    plt.plot(
                        "episode",
                        "avg_reward",
                        data=metrics_df,
                        marker="o",
                        color="yellow",
                        linewidth=3,
                        label="avg",
                    )
                    plt.plot(
                        "episode",
                        "min_reward",
                        data=metrics_df,
                        marker="o",
                        color="red",
                        linewidth=2,
                        label="min",
                    )
                    plt.legend()
                    plt.show()

                self.agent.tensorboard.update_stats(
                    reward_avg=average_reward,
                    reward_min=min_reward,
                    reward_max=max_reward,
                    epsilon=self.epsilon,
                )

                if average_reward >= self.min_reward:
                    self.agent.model.save(
                        f"models/{self.model_name}__{average_reward:_>7.2f}avg.model"
                    )
                    self.min_reward = average_reward

            if self.epsilon > self.min_epsilon:
                self.epsilon *= self.epsilon_decay
                self.epsilon = max(self.min_epsilon, self.epsilon)

    def get_metrics(self, path):
        for summary in summary_iterator(path):
            for v in summary.summary.value:
                if v.tag == "loss" or v.tag == "accuracy":
                    print(v.tag, ": ", v.simple_value)


if __name__ == "__main__":
    network = DQN(False)
    network.run(show_metrics=True)

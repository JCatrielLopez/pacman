import logging
import os
import pickle
import random

import numpy as np
from tqdm import tqdm

from pacman.dqn.Agent import DQNAgent
from pacman.game import GameEnv

logging.basicConfig(
    filename="logs/logfile.log", format="%(levelname)s:%(name)s:%(message)s)"
)
logging.getLogger("matplotlib").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

random.seed(21022020)
np.random.seed(21022020)


class DQN:
    def __init__(self, render=False, episodes=600, model_name="", model_path=None):
        self.render_scene = render
        self.episodes = episodes
        self.model_name = model_name

        self.epsilon = 1
        self.epsilon_decay = 0.99975
        self.min_epsilon = 0.001

        self.aggregate_stats_every = 5
        self.max_steps_per_episode = 2500

        if not os.path.isdir("models"):
            os.makedirs("models")

        if not os.path.isdir("logs"):
            os.makedirs("logs")

        self.agent = DQNAgent(model_path)
        self.env = GameEnv()

    def run(self, show_metrics=False):

        # TODO yield
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

            if (
                    (not episode % self.aggregate_stats_every
                     or episode == 1)
                    and show_metrics
            ):
                self.agent.get_plot()

            if self.epsilon > self.min_epsilon:
                self.epsilon *= self.epsilon_decay
                self.epsilon = max(self.min_epsilon, self.epsilon)

            if episode % 100 == 0:
                self.agent.model.save(f"models/{self.model_name}__{episode}ep.model")


        with open('models/training_history.pickle', 'rb') as f:
            pickle.dump(self.agent.history, f)


if __name__ == "__main__":
    pass

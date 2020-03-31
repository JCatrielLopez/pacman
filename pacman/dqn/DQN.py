import logging
import os
import pickle
import random
import datetime
import time
import matplotlib.pyplot as plt

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
    def __init__(self, render=False, episodes=600, model_name="", model_path=None, update_episodes=None):
        self.render_scene = render
        self.episodes = episodes
        self.model_name = model_name
        self.update_episodes = update_episodes

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

    def run(self, show_metrics=False, end_of_train_screen=None):

        plt.ion()
        plt.show()

        # TODO quitar esto
        # for i in range(5):
        #     print(i)
        #     time.sleep(1)
        #     self.update_episodes(i, self.episodes)
        #
        #
        #
        # if end_of_train_screen is not None:
        #     end_of_train_screen('models/Pacmanv3__250ep.model')
        #     return

        if self.update_episodes is not None:
            self.update_episodes(0, self.episodes)

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


            # if (
            #         (not episode % self.aggregate_stats_every
            #          or episode == 1)
            #         and show_metrics
            # ):
            #     self.agent.get_plot()

            if (show_metrics):
                self.agent.get_plot()

            if self.epsilon > self.min_epsilon:
                self.epsilon *= self.epsilon_decay
                self.epsilon = max(self.min_epsilon, self.epsilon)

            if episode % 100 == 0:
                string_date = str(datetime.datetime.now().strftime("%m-%d-%Y - %H:%M"))
                self.agent.model.save(f"models/{self.model_name}__{episode}ep - {string_date}.model")

            if self.update_episodes is not None:
                self.update_episodes(episode, self.episodes)

        string_date = str(datetime.datetime.now().strftime("%m-%d-%Y - %H:%M"))

        filepath = f"models/{self.model_name}__{self.episodes}ep - {string_date}.model"
        self.agent.model.save(filepath)
        print('Training finish! - model saved in: ', filepath)

        with open('models/training_history.pickle', 'wb') as f:
            pickle.dump(self.agent.history, f)

        if end_of_train_screen is not None:
            end_of_train_screen(filepath)


if __name__ == "__main__":
    pass

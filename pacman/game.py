import logging
import sys

import numpy as np
import pygame as pg

from pacman import scene

logging.basicConfig(
    level=logging.DEBUG, format="%(module)s:%(threadName)s:%(message)s"
)  # level=10

logger = logging.getLogger()


class GameEnv:
    def __init__(self):
        self.episode_step = 0

        # self.active_scene = scene.GameScene("../../res/map/01_level.npz")
        # self.active_scene.init_scene()
        # self.active_scene.toggle_sprites()

        self.frame_skip = 4

    def render(self):
        self.active_scene.render()

    def step(self, action):
        self.episode_step += 1

        reward = 0
        done = False
        obs = []

        for _ in range(0, self.frame_skip):
            self.active_scene.process_action(action)
            reward += self.active_scene.get_reward()
            done = self.active_scene.is_finish()

            obs.append(np.array(self.active_scene.get_state()))

        obs = np.stack(obs, axis=2)
        return obs, reward, done

    def reset(self):
        # self.active_scene.terminate()
        self.active_scene = scene.GameScene("../../res/map/01_level.npz")
        self.active_scene.init_scene()

        obs = []
        for _ in range(0, self.frame_skip):
            obs.append(np.array(self.active_scene.get_state()))

        obs = np.stack(obs, axis=2)
        return obs

    def close(self):
        self.active_scene.terminate()
        pg.quit()
        sys.exit()

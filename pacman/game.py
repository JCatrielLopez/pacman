import logging

import numpy as np
import pygame as pg

import pacman.constants as constants
from pacman import scene

logging.basicConfig(
    level=logging.DEBUG, format="%(module)s:%(threadName)s:%(message)s"
)  # level=10

logger = logging.getLogger()


class Game:
    clock = None
    high_score_text = None
    score_text = None
    lives_text = None

    scenes_path = None
    display = None

    def __init__(self, display):

        self.clock = pg.time.Clock()
        self.display = display
        # self.scenes_path = [
        #     "../res/map/01_level.npz",
        #     "../res/map/02_level.npz",
        #     "../res/map/03_level.npz",
        #     "../res/map/04_level.npz",
        #     "../res/map/05_level.npz",
        # ]
        self.scenes_path = ["../res/map/01_level.npz"]

    def __str__(self):
        return repr(self)

    def __new__(cls, display):
        if not hasattr(cls, "instance"):
            cls.instance = super(Game, cls).__new__(cls)
        return cls.instance

    def run(self):
        quit_game = False
        for scene_path in self.scenes_path:
            active_scene = scene.GameScene(self.display, scene_path)

            active_scene.init_scene()
            logger.debug(f"Active scene: {active_scene}")

            while not active_scene.is_finish():
                filtered_events = []
                for event in pg.event.get():

                    if event.type == pg.QUIT or pg.key.get_pressed()[pg.K_ESCAPE]:
                        active_scene.terminate()
                        quit_game = True

                    if pg.key.get_pressed()[pg.K_r]:  # Reset
                        active_scene.terminate()
                        active_scene = scene.GameScene(self.display, scene_path)
                        active_scene.init_scene()

                    if pg.key.get_pressed()[pg.K_h]:
                        filtered_events.append(event)
                    if pg.key.get_pressed()[pg.K_BACKSPACE]:
                        filtered_events.append(event)
                    if pg.key.get_pressed()[pg.K_LEFT]:
                        filtered_events.append(event)
                    if pg.key.get_pressed()[pg.K_RIGHT]:
                        filtered_events.append(event)
                    if pg.key.get_pressed()[pg.K_UP]:
                        filtered_events.append(event)
                    if pg.key.get_pressed()[pg.K_DOWN]:
                        filtered_events.append(event)
                    if pg.key.get_pressed()[pg.K_f]:
                        filtered_events.append(event)

                active_scene.process_input(filtered_events)

                active_scene.render()

                self.clock.tick(constants.FPS)

            if quit_game:
                break


class GameEnv:

    def __init__(self):
        self.episode_step = 0

        self.active_scene = scene.GameScene("../../res/map/01_level.npz")
        self.active_scene.init_scene()

    def render(self):
        self.active_scene.render()

    def step(self, action):
        self.episode_step += 1

        self.active_scene.process_action(action)

        new_observation = np.array(self.active_scene.get_state())
        reward = self.active_scene.get_reward()
        done = self.active_scene.is_finish()

        return new_observation, reward, done

    def reset(self):
        self.active_scene.terminate()
        self.active_scene = scene.GameScene("../../res/map/01_level.npz")
        self.active_scene.init_scene()

        return np.array(self.active_scene.get_state())

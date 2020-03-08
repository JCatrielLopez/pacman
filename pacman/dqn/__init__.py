import os
import pickle

import pygame as pg

from pacman.game import GameEnv


class Game:

    def __init__(self, episodes=100):
        self.episodes = episodes
        self.env = GameEnv()

        if not os.path.isdir("replay"):
            os.makedirs("replay")
        self.replay_memory = []

    def save_replay_memory(self):
        with open('replay/replay_memory.pkl', 'ab') as f:
            for i in self.replay_memory:
                pickle.dump(i, f, protocol=pickle.HIGHEST_PROTOCOL)

    def run(self):
        for _ in range(0, self.episodes):
            current_state = self.env.reset()
            done = False

            print(f"\rReplay memory length: {len(self.replay_memory)}", end='')
            while not done:
                action = -1

                pg.event.get()

                if pg.key.get_pressed()[pg.K_UP]:
                    action = 0
                if pg.key.get_pressed()[pg.K_LEFT]:
                    action = 1
                if pg.key.get_pressed()[pg.K_DOWN]:
                    action = 2
                if pg.key.get_pressed()[pg.K_RIGHT]:
                    action = 3

                new_state, reward, done = self.env.step(action)

                self.env.render()

                self.update_replay_memory(
                    (current_state, action, reward, new_state, done)
                )

                current_state = new_state

            self.save_replay_memory()
        self.env.close()

    def update_replay_memory(self, param):
        self.replay_memory.append(param)


if __name__ == "__main__":
    import cProfile

    game = Game(episodes=1)

    cProfile.run('game.run()')
    # game.run()

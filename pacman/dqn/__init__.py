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
        else:
            with open("replay/replay_memory.pkl", 'rb') as f:  # TODO Jugar y subirlo para agregar mas datos.
                self.replay_memory = pickle.load(f)

    def save_replay_memory(self):
        with open('replay/replay_memory.pkl', 'ab') as f:  # TODO Probar si se puede hacer el append con ab!
            pickle.dump(self.replay_memory, f, protocol=pickle.HIGHEST_PROTOCOL)

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
    game = Game(episodes=10)
    game.run()

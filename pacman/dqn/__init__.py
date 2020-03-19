import pygame as pg

from pacman.dqn.Agent import DQNAgent
from pacman.dqn.DQN import DQN
from pacman.game import GameEnv


class Game:
    def __init__(self, episodes=100):
        self.episodes = episodes
        self.env = GameEnv()

    def run(self, render=False):
        for _ in range(0, self.episodes):
            self.env.reset()
            done = False

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
                if pg.key.get_pressed()[pg.K_h]:
                    self.env.active_scene.toggle_sprites()

                self.env.active_scene.process_action(action)

                if render:
                    self.env.render()

        self.env.close()


if __name__ == "__main__":
    g = Game(episodes=1)
    g.run(render=True)

    #
    # network = DQN(render=True, episodes=12000, model_name="Pacmanv4")
    # network.run(show_metrics=True)
    #
    # with open('models/training_history.pickle', 'rb') as f:
    #     h = pickle.load(f)
    #
    # avg_acc = []
    # for i in range(0, len(h["accuracy"]) - 1000, 1000):
    #     avg_acc.append(np.average(h['accuracy'][i:i + 1000]))
    #
    # avg_val_acc = []
    # for i in range(0, len(h["val_accuracy"]) - 1000, 1000):
    #     avg_val_acc.append(np.average(h['val_accuracy'][i:i + 1000]))
    #
    # plt.plot(avg_acc)
    # plt.plot(avg_val_acc)
    # plt.title("model accuracy")
    # plt.ylabel("accuracy")
    # plt.xlabel("epoch")
    # plt.legend(["train", "test"], loc="upper left")
    # plt.show()

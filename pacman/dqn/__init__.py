import os

import pygame as pg
import pygameMenu

from pacman import constants
from pacman.dqn.Agent import DQNAgent
from pacman.dqn.DQN import DQN
from pacman.game import GameEnv

render = False
show_metrics = False
episodes = 12000


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
                if pg.key.get_pressed()[pg.K_ESCAPE]:
                    done = True

                self.env.active_scene.process_action(action)

                if render:
                    self.env.render()

                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        done = True

        self.env.close()


def play():
    g = Game(episodes=1)
    g.run(render=True)


def autoplay(render=False, episodes=12000, show_metrics=True):
    network = DQN(render=render, episodes=episodes, model_name="Pacman")
    network.run(show_metrics=show_metrics)


def bg_fun():
    global surface
    surface.fill(constants.BLACK)


def set_render(value, c=None, **kwargs):
    global render
    render = value[1]


def set_metrics(value, c=None, **kwargs):
    global show_metrics
    show_metrics = value[1]


def set_episodes(value, c=None, **kwargs):
    global episodes
    try:
        episodes = int(value[1])
    except ValueError:
        pass  # Queda el valor por defecto.


if __name__ == "__main__":

    pg.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    global surface
    surface = pg.display.set_mode((constants.WIDTH, constants.HEIGHT))

    pg.display.set_caption('PACMAN - IntroDL 2020')
    clock = pg.time.Clock()

    about_menu = pygameMenu.TextMenu(surface,
                                     bgfun=bg_fun,
                                     color_selected=constants.WHITE,
                                     font=pygameMenu.font.FONT_BEBAS,
                                     font_color=constants.WHITE,
                                     font_size=30,
                                     menu_alpha=100,
                                     menu_color=constants.RED,
                                     menu_height=int(constants.HEIGHT * 0.9),
                                     menu_width=int(constants.WIDTH * 0.9),
                                     onclose=pygameMenu.events.DISABLE_CLOSE,
                                     option_shadow=False,
                                     title='About',
                                     window_height=constants.HEIGHT,
                                     window_width=constants.WIDTH
                                     )

    about_menu.add_line(pygameMenu.locals.TEXT_NEWLINE)

    about_menu.add_line("Carpintero, Bautista")
    about_menu.add_line("Lopez, Catriel")
    about_menu.add_line("Severino, Natalia")

    about_menu.add_option('Return to menu', pygameMenu.events.BACK)

    train_menu = pygameMenu.Menu(surface,
                                 bgfun=bg_fun,
                                 color_selected=constants.WHITE,
                                 font=pygameMenu.font.FONT_BEBAS,
                                 font_color=constants.WHITE,
                                 font_size=30,
                                 menu_alpha=100,
                                 menu_color=constants.RED,
                                 menu_height=int(constants.HEIGHT * 0.9),
                                 menu_width=int(constants.WIDTH * 0.9),
                                 onclose=pygameMenu.events.DISABLE_CLOSE,
                                 option_shadow=False,
                                 title='Training',
                                 window_height=constants.HEIGHT,
                                 window_width=constants.WIDTH
                                 )

    train_menu.add_selector('Render', [('True', True), ('False', False)], onchange=set_render)
    train_menu.add_text_input('Episodes ', default=12000, maxchar=7, input_underline=".", onchange=set_episodes)
    train_menu.add_selector('Metrics', [('Show', True), ('Hide', False)], onchange=set_metrics)
    train_menu.add_option('Start', autoplay, render, episodes, show_metrics)

    main_menu = pygameMenu.Menu(surface,
                                bgfun=bg_fun,
                                color_selected=constants.WHITE,
                                font=pygameMenu.font.FONT_BEBAS,
                                font_color=constants.WHITE,
                                font_size=30,
                                menu_alpha=100,
                                menu_color=constants.RED,
                                menu_height=int(constants.HEIGHT * 0.9),
                                menu_width=int(constants.WIDTH * 0.9),
                                onclose=pygameMenu.events.DISABLE_CLOSE,
                                option_shadow=False,
                                title='Pacman',
                                window_height=constants.HEIGHT,
                                window_width=constants.WIDTH
                                )

    main_menu.add_option('Play',
                         play)

    main_menu.add_option('Train',
                         train_menu)
    main_menu.add_option('About', about_menu)
    main_menu.add_option('Quit', pygameMenu.events.EXIT)

    main_menu.set_fps(constants.FPS)

    while True:
        clock.tick(constants.FPS)

        bg_fun()

        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                exit()

        main_menu.mainloop(events)

        pg.display.flip()

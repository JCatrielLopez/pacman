import os

import pygame as pg
import pygameMenu
from pygameMenu import locals

from pacman import constants
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


def close():
    # TODO esto ya no funciona
    print('close')
    exit()


def build_training_menu(font=pygameMenu.font.FONT_BEBAS, text_fontsize=30):

    training_menu = pygameMenu.TextMenu(surface,
                                        bgfun=bg_fun,
                                        color_selected=constants.WHITE,
                                        font=font,
                                        font_title=pygameMenu.font.FONT_BEBAS,
                                        font_color=constants.WHITE,
                                        font_size=30,
                                        text_fontsize=text_fontsize,
                                        menu_alpha=100,
                                        menu_color=constants.RED,
                                        menu_height=int(constants.HEIGHT * 0.9),
                                        menu_width=int(constants.WIDTH * 0.9),
                                        onclose=close,
                                        option_shadow=False,
                                        title='Training...',
                                        window_height=constants.HEIGHT,
                                        window_width=constants.WIDTH
                                        )

    training_menu.add_line(pygameMenu.locals.TEXT_NEWLINE)
    return training_menu


def update_episodes(episode, episodes):
    training_menu = build_training_menu()
    msg = "Episode:    " + str(episode) + "      of      " + str(episodes)
    training_menu.add_line(msg)
    training_menu.mainloop(disable_loop=True)


def return_to_train_menu():
    reset_variables()
    create_menus()
    start_main_menu()


def end_of_train_screen(filepath):
    training_menu = build_training_menu(font=pygameMenu.font.FONT_HELVETICA, text_fontsize=20)
    training_menu.add_line('Training finish!')
    training_menu.add_line('The model is save in the file: ')
    training_menu.add_line(filepath)
    training_menu.add_line(pygameMenu.locals.TEXT_NEWLINE)
    training_menu.add_button('- Back -', return_to_train_menu)
    training_menu.mainloop()


def autoplay_train():

    global show_metrics_train
    global episodes_train

    network = DQN(render=False, episodes=episodes_train, model_name="Pacman", model_path=None, update_episodes=update_episodes)
    network.run(show_metrics=show_metrics_train, end_of_train_screen=end_of_train_screen)


def autoplay_test():
    global episodes_test
    global model_path_test

    network = DQN(render=True, episodes=episodes_test, model_name="Pacman", model_path=model_path_test)
    network.run(show_metrics=False)


def bg_fun():
    global surface
    surface.fill(constants.BLACK)


def set_metrics_train(value, c=None, **kwargs):
    global show_metrics_train
    show_metrics_train = not show_metrics_train


def set_episodes_train(value, c=None, **kwargs):
    global episodes_train
    try:
        episodes_train = int(value)
    except ValueError as error:
        pass # Queda el valor por defecto.


def set_episodes_test(value, c=None, **kwargs):
    global episodes_test
    try:
        episodes_test = int(value)
    except ValueError as error:
        pass  # Queda el valor por defecto.


def set_model_path_test(value, c=None, **kwargs):
    global model_path_test
    try:
        model_path_test = value
    except ValueError:
        pass  # Queda el valor por defecto.


def reset_variables():
    global show_metrics_train
    show_metrics_train = True

    global episodes_train
    episodes_train = 12000

    global episodes_test
    episodes_test = 12000

    global model_path_test
    model_path_test = 'models/Pacmanv3__250ep.model'

    global surface
    surface = pg.display.set_mode((constants.WIDTH, constants.HEIGHT))


def start_main_menu():
    while True:
        clock.tick(constants.FPS)

        bg_fun()
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                exit()

        main_menu.mainloop(events)

        pg.display.flip()


def create_menus():
    global about_menu
    global train_menu
    global test_menu
    global main_menu

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

    about_menu.add_line("Carpintero,    Bautista")
    about_menu.add_line("Lopez,    Catriel")
    about_menu.add_line("Severino,    Natalia")
    about_menu.add_line(pygameMenu.locals.TEXT_NEWLINE)
    about_menu.add_button('- Back -', pygameMenu.events.BACK)

    train_menu = pygameMenu.TextMenu(surface,
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

    train_menu.add_text_input('Episodes:    ', default=12000, maxchar=7, onchange=set_episodes_train,
                              align=locals.ALIGN_LEFT)
    train_menu.add_selector('Metrics:     ', [('Show', True), ('Hide', False)], onchange=set_metrics_train,
                            align=locals.ALIGN_LEFT)
    train_menu.add_button('Start', autoplay_train)
    train_menu.add_button('- Back -', pygameMenu.events.BACK)

    test_menu = pygameMenu.Menu(surface,
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
                                title='Test',
                                window_height=constants.HEIGHT,
                                window_width=constants.WIDTH
                                )

    test_menu.add_text_input('Episodes:           ', default=12000, maxchar=7, onchange=set_episodes_test,
                             align=locals.ALIGN_LEFT)
    test_menu.add_text_input('Model Path:    ', default=model_path_test, maxwidth=12, onchange=set_model_path_test,
                             align=locals.ALIGN_LEFT)
    test_menu.add_button('Start', autoplay_test)
    test_menu.add_button('- Back -', pygameMenu.events.BACK)

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
                                onclose=close,
                                option_shadow=False,
                                title='Pacman',
                                window_height=constants.HEIGHT,
                                window_width=constants.WIDTH,
                                back_box=False
                                )

    main_menu.add_button('Play', play)
    main_menu.add_button('Train', train_menu)
    main_menu.add_button('Test', test_menu)
    main_menu.add_button('About', about_menu)
    main_menu.add_button('Quit', pygameMenu.events.EXIT)

    main_menu.set_fps(constants.FPS)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    show_metrics_train = True
    episodes_train = 12000

    episodes_test = 12000
    model_path_test = 'models/Pacmanv3__250ep.model'

    pg.init()
    programIcon = pg.image.load('../../res/icon.png')
    pg.display.set_icon(programIcon)

    os.environ['SDL_VIDEO_CENTERED'] = '1'

    global surface
    surface = pg.display.set_mode((constants.WIDTH, constants.HEIGHT))

    pg.display.set_caption('PACMAN - IntroDL 2020')
    clock = pg.time.Clock()

    about_menu = None
    train_menu = None
    test_menu = None
    main_menu = None

    create_menus()
    start_main_menu()

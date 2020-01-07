import os

import pygame as pg

import pacman
import pacman.constants as constants
import pacman.display as display
import pacman.scene as scene
import pygameMenu


class Game:
    clock = None
    highscore_text = None
    score_text = None
    lives_text = None

    def __init__(self):
        self.clock = pg.time.Clock()

    def __str__(self):
        return repr(self)

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Game, cls).__new__(cls)
        return cls.instance

    def run(self, active_scene):

        while active_scene is not None:

            filtered_events = []
            for event in pg.event.get():
                if event.type == pg.QUIT or pg.key.get_pressed()[pg.K_ESCAPE]:
                    active_scene.terminate()
                if pg.key.get_pressed()[pg.K_r]:
                    filtered_events.append(event)
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

            active_scene.process_input(filtered_events)

            active_scene.render()

            active_scene = active_scene.next
            self.clock.tick(constants.FPS)


def main(display):
    g = Game()

    first_level = scene.FirstLevel(display, "../res/map/01_level.npz", 0)
    g.run(first_level)


def bg_fun():
    global surface
    surface.fill(constants.PURPLE)


if __name__ == "__main__":

    #
    #
    # import cProfile
    #
    dis = display.Display((constants.WIDTH, constants.HEIGHT))
    # cProfile.run("main(dis)")

    # -------------------------------------------------------------------------
    # Init pygame
    # -------------------------------------------------------------------------
    pg.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    # Create pygame screen and objects
    global surface
    surface = pg.display.set_mode((constants.WIDTH, constants.HEIGHT))
    pg.display.set_caption('PACMAN - IntroDL 20209')
    clock = pg.time.Clock()

    # -------------------------------------------------------------------------
    # Create menus
    # -------------------------------------------------------------------------

    about_menu = pygameMenu.TextMenu(surface,
                                     bgfun=bg_fun,
                                     color_selected=constants.WHITE,
                                     font=pygameMenu.font.FONT_BEBAS,
                                     font_color=constants.BLACK,
                                     font_size=30,
                                     menu_alpha=100,
                                     menu_color=constants.RED,
                                     menu_height=int(constants.HEIGHT * 0.7),
                                     menu_width=int(constants.WIDTH * 0.7),
                                     onclose=pygameMenu.events.DISABLE_CLOSE,
                                     option_shadow=False,
                                     title='About',
                                     window_height=constants.HEIGHT,
                                     window_width=constants.WIDTH
                                     )

    about_menu.add_line(pygameMenu.locals.TEXT_NEWLINE)
    about_menu.add_line("Pacman - IntroDL")
    about_menu.add_line(f"Version: {pacman.__version__}")
    about_menu.add_line("Authors: ")
    for author in pacman.__author__:
        about_menu.add_line(author)
    # about_menu.add_line(pygameMenu.locals.TEXT_NEWLINE)
    about_menu.add_option('Return to menu', pygameMenu.events.BACK)

    # Main menu
    main_menu = pygameMenu.Menu(surface,
                                bgfun=bg_fun,
                                color_selected=constants.WHITE,
                                font=pygameMenu.font.FONT_BEBAS,
                                font_color=constants.BLACK,
                                font_size=30,
                                menu_alpha=100,
                                menu_color=constants.RED,
                                menu_height=int(constants.HEIGHT * 0.7),
                                menu_width=int(constants.WIDTH * 0.7),
                                onclose=pygameMenu.events.DISABLE_CLOSE,
                                option_shadow=False,
                                title='Pacman',
                                window_height=constants.HEIGHT,
                                window_width=constants.WIDTH
                                )

    main_menu.add_option('Start',
                         main,
                         dis)
    main_menu.add_option('About', about_menu)
    main_menu.add_option('Quit', pygameMenu.events.EXIT)

    # Configure main menu
    main_menu.set_fps(constants.FPS)

    # -------------------------------------------------------------------------
    # Main loop
    # -------------------------------------------------------------------------
    while True:

        # Tick
        clock.tick(constants.FPS)

        # Paint background
        bg_fun()

        # Application events
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                exit()

        # Main menu
        main_menu.mainloop(events)

        # Flip surface
        pg.display.flip()

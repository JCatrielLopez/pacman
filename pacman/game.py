import pygame as pg

import pacman.constants as constants
import pacman.display as display
import pacman.scene as scene


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


if __name__ == "__main__":
    import cProfile

    dis = display.Display((constants.WIDTH, constants.HEIGHT))
    cProfile.run('main(dis)')

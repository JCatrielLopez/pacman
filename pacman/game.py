import pygame as pg
import logging
import pacman.constants as constants
import pacman.display as display
from pacman import scene

logging.basicConfig(level=logging.DEBUG,
                    format="%(module)s:%(threadName)s:%(message)s")  # level=10

logger = logging.getLogger(name=None)

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
        self.scenes_path = [
            "../res/map/01_level.npz",
            "../res/map/02_level.npz",
            "../res/map/03_level.npz",
            "../res/map/04_level.npz",
            "../res/map/05_level.npz",
        ]

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


def main(display):
    g = Game(display)
    g.run()


if __name__ == "__main__":
    # import cProfile
    # dis = display.Display((constants.WIDTH, constants.HEIGHT))
    # cProfile.run('main(dis)', sort="cumtime")

    dis = display.Display((constants.WIDTH, constants.HEIGHT))
    main(dis)

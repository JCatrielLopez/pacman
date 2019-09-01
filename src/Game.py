import pygame as pg

from src.Blinky import Blinky
from src.Bonus import Bonus
from src.Event import Event  # from src.MapLoader import MapLoader
from src.MapLoader import MapLoader
from src.Pacman import Pacman


class Game:
    def __init__(self):

        self._map = MapLoader('../res/Maze1.txt', '../res/Distances1.txt')

        self.HEIGHT, self.WIDTH = self._map.get_shape()
        self.TILESIZE = 20

        self._window = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        pg.display.set_caption("Pacman")

        # Variables del juego
        self._clock = pg.time.Clock()
        self.FPS = 10

        # Defino los jugadores
        self._pacman = Pacman(3, 3, "../res/pacman", 1)
        self._blinky = Blinky(5, 5, "../res/ghosts", 1)
        self._bonus = Bonus(80, 80, "../res/bonus", 10)

        self._bonus.observe("pacman got a bonus", self._bonus.add)
        self._blinky.observe("pacman moved", self._blinky.next_position)

        # Inicio
        pg.init()

    def draw(self):

        # self._window.fill(self.BLACK)
        #
        # for x in range(0, self.WIDTH, self.TILESIZE):
        #     pg.draw.line(
        #         self._window, (240, 255, 255), (x, 0), (x, self.HEIGHT)
        #     )
        # for y in range(0, self.HEIGHT, self.TILESIZE):
        #     pg.draw.line(
        #         self._window, (240, 255, 255), (0, y), (self.WIDTH, y)
        #     )

        img = pg.image.load("../res/map/Map1.2.png")
        img = pg.transform.scale(img, (self.WIDTH, self.HEIGHT))
        self._window.blit(img, (0, 0))
        pg.display.flip()

        pg.draw.circle(
            self._window,
            (255, 0, 0),
            (self._pacman.get_pos()[0], self._pacman.get_pos()[1]),
            2,
        )

        self._window.blit(
            pg.transform.scale(self._bonus.get_sprite(), (24, 24)),
            self._bonus.get_pos(),
        )
        self._window.blit(
            pg.transform.scale(self._blinky.get_sprite(), (32, 32)),
            self._blinky.get_pos(),
        )
        self._window.blit(
            pg.transform.scale(self._pacman.get_sprite(), (32, 32)),
            self._pacman.get_pos(),
        )
        pg.display.update()

    # Main loop
    def run(self):
        running = True

        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if pg.key.get_pressed()[pg.K_RIGHT] and self._map.is_valid(self._pacman.get_pos()):
                    self._pacman.move_right()
                if pg.key.get_pressed()[pg.K_UP] and self._map.is_valid(self._pacman.get_pos()):
                    self._pacman.move_up()
                if pg.key.get_pressed()[pg.K_DOWN] and self._map.is_valid(self._pacman.get_pos()):
                    self._pacman.move_down()
                if pg.key.get_pressed()[pg.K_LEFT] and self._map.is_valid(self._pacman.get_pos()):
                    self._pacman.move_left()

            Event(
                "pacman got a bonus",
                self._pacman.get_pos() == self._bonus.get_pos(),
            )
            Event("pacman moved", self._pacman.get_pos())
            self._blinky.move()

            self.draw()
            self._clock.tick(self.FPS)

        pg.quit()


if __name__ == "__main__":
    Game().run()

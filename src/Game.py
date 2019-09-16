import pygame as pg

from src.Blinky import Blinky
from src.Bonus import Bonus
from src.MapLoader import MapLoader
from src.Pacman import Pacman


class Game:
    def __init__(self):

        self._map = MapLoader('../res/map/Maze1.json')

        self.HEIGHT, self.WIDTH = self._map.get_shape()
        self.TILESIZE = self._map.get_tilesize()

        self._window = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        pg.display.set_caption("Pacman")

        # Variables del juego
        self._clock = pg.time.Clock()
        self.FPS = 60

        # Defino los jugadores
        self._pacman = Pacman(255, 460, "../res/pacman", 1)
        self._blinky = Blinky(265, 460, "../res/ghosts", 1)
        self._bonus = Bonus(80, 80, "../res/bonus", 10)

        # Sounds
        pg.mixer.init()
        self.effect = pg.mixer.Sound('../res/sounds/PacmanWakaWaka04.wav')

        self._bonus.observe("pacman got a bonus", self._bonus.add)
        self._blinky.observe("pacman moved", self._blinky.next_position)

        # Inicio
        pg.init()
        self.myfont = pg.font.SysFont("monospace", 15)

        # render text

    def draw(self):

        img = pg.image.load("../res/map/Map1.2.png")
        img = pg.transform.scale(img, (self.WIDTH, self.HEIGHT))
        self._window.blit(img, (0, 0))

        for x in range(0, self.WIDTH, self.TILESIZE):
            pg.draw.line(
                self._window, (240, 255, 255), (x, 0), (x, self.HEIGHT)
            )
        for y in range(0, self.HEIGHT, self.TILESIZE):
            pg.draw.line(
                self._window, (240, 255, 255), (0, y), (self.WIDTH, y)
            )

        # for i in range(0, self.WIDTH, self.TILESIZE):
        #     for j in range(0, self.HEIGHT, self.TILESIZE):
        #         if self._map.get_value(i, j) == 0:
        #             label = self.myfont.render(str(self._map.get_value(i, j)), 1, (255, 0, 0))
        #         else:
        #             label = self.myfont.render(str(self._map.get_value(i, j)), 1, (255, 255, 0))
        #         self._window.blit(label, (i + 5, j + 5))

        self._window.blit(
            pg.transform.scale(self._bonus.get_sprite(), (24, 24)),
            self._bonus.get_pos()
        )
        self._window.blit(
            self._blinky.get_sprite(),
            self._blinky.get_pos()
        )
        self._window.blit(
            self._pacman.get_sprite(),
            self._pacman.get_pos()
        )

        # pg.draw.rect(self._window, (255, 0, 0), self._blinky.get_hitbox(), 5)
        pg.draw.rect(self._window, (0, 0, 255), self._pacman.get_hitbox(), 2)

        pg.display.update()

    # Main loop
    def run(self):
        running = True

        self._pacman.move()

        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if pg.key.get_pressed()[pg.K_RIGHT]:
                    self._pacman.move_right()
                if pg.key.get_pressed()[pg.K_UP]:
                    self._pacman.move_up()
                if pg.key.get_pressed()[pg.K_DOWN]:
                    self._pacman.move_down()
                if pg.key.get_pressed()[pg.K_LEFT]:
                    self._pacman.move_left()

                if pg.key.get_pressed()[pg.K_m]:
                    self.effect.play()
                if pg.key.get_pressed()[pg.K_n]:
                    pg.mixer.pause()

            if self._pacman.hit(self._blinky.get_hitbox()):
                print("Rip Pacman")
                # TODO Matar al pacman.

            # Event(
            #     "pacman got a bonus",
            #     self._pacman.get_pos() == self._bonus.get_pos(),
            # )
            #
            # Event("pacman moved", self._pacman.get_pos())

            self._blinky.move()

            self.draw()

            # Clock tick
            self._clock.tick(self.FPS)

        pg.quit()


if __name__ == "__main__":
    Game().run()

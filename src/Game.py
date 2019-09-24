import pygame as pg

from src.Blinky import Blinky
from src.Bonus import Bonus
from src.MapLoader import MapLoader
from src.Pacman import Pacman


class Game:
    def __init__(self):

        self.map = MapLoader('../res/map/Maze1.json')

        self.HEIGHT, self.WIDTH = self.map.get_shape()
        self.TILESIZE = self.map.get_tilesize()

        self.window = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        pg.display.set_caption("Pacman")

        # Variables del juego
        self.clock = pg.time.Clock()
        self.FPS = 60
        self.dots = [-1] * 868

        # Defino los jugadores
        self.pacman = Pacman(255, 460, "../res/pacman", 1)
        self.blinky = Blinky(265, 460, "../res/ghosts", 1)
        self.bonus = Bonus(80, 80, "../res/bonus", 10)

        # Sounds
        pg.mixer.init()
        self.effect = pg.mixer.Sound('../res/sounds/PacmanWakaWaka04.wav')

        self.bonus.observe("pacman got a bonus", self.bonus.add)
        self.blinky.observe("pacman moved", self.blinky.next_position)

        for i in range(0, self.WIDTH, self.TILESIZE):
            for j in range(0, self.HEIGHT, self.TILESIZE):
                x, y = self.map.get_grid((i, j))
                value = self.map.get_value(x, y)
                if value == 1:
                    self.add_dot((x, y), 10)
                elif value == 3:
                    self.add_dot((x, y), 30)
        # Inicio
        pg.init()

    def add_dot(self, pos, score):
        self.dots[pos[0] * 31 + pos[1]] = score

    def get_dot(self, pos):
        try:
            return self.dots[pos[0] * 31 + pos[1]]
        except IndexError:
            return -1

    def draw(self):

        img = pg.image.load("../res/map/Map1.2.png")
        img = pg.transform.scale(img, (self.WIDTH, self.HEIGHT))
        self.window.blit(img, (0, 0))

        for x in range(0, self.WIDTH, self.TILESIZE):
            pg.draw.line(
                self.window, (240, 255, 255), (x, 0), (x, self.HEIGHT)
            )
        for y in range(0, self.HEIGHT, self.TILESIZE):
            pg.draw.line(
                self.window, (240, 255, 255), (0, y), (self.WIDTH, y)
            )

        for i in range(0, self.WIDTH, self.TILESIZE):
            for j in range(0, self.HEIGHT, self.TILESIZE):
                x, y = self.map.get_grid((i, j))
                value = self.get_dot((x, y))
                if value == 10:
                    pg.draw.circle(self.window, (255, 255, 0), (i + 10, j + 10), 3)
                elif value == 30:
                    pg.draw.circle(self.window, (255, 255, 0), (i + 10, j + 10), 6)

        self.window.blit(
            self.blinky.get_sprite(),
            self.blinky.get_pos()
        )
        self.window.blit(
            self.pacman.get_sprite(),
            self.pacman.get_pos()
        )

        # pg.draw.rect(self._window, (255, 0, 0), self._blinky.get_hitbox(), 5)
        # pg.draw.rect(self.window, (0, 0, 255), self.pacman.get_hitbox(), 2)

        pg.display.update()

    # Main loop
    def run(self):
        running = True

        self.pacman.move()

        score = 0

        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if pg.key.get_pressed()[pg.K_RIGHT]:
                    self.pacman.move_right()
                if pg.key.get_pressed()[pg.K_UP]:
                    self.pacman.move_up()
                if pg.key.get_pressed()[pg.K_DOWN]:
                    self.pacman.move_down()
                if pg.key.get_pressed()[pg.K_LEFT]:
                    self.pacman.move_left()

                if pg.key.get_pressed()[pg.K_m]:
                    self.effect.play()
                if pg.key.get_pressed()[pg.K_n]:
                    pg.mixer.pause()

            if self.pacman.hit(self.blinky.get_hitbox()):
                print("Rip Pacman")
                # TODO Matar al pacman.

            grid_score = self.get_dot(self.pacman.get_grid_pos())

            if grid_score != -1:
                score += grid_score
                print(f"Score: {score}")
                self.add_dot(self.pacman.get_grid_pos(), -1)

            # Event(
            #     "pacman got a bonus",
            #     self._pacman.get_pos() == self._bonus.get_pos(),
            # )
            #
            # Event("pacman moved", self._pacman.get_pos())

            self.blinky.move()

            self.draw()

            # Clock tick
            self.clock.tick(self.FPS)

        pg.quit()


if __name__ == "__main__":
    Game().run()

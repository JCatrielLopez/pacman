import pygame as pg

from src import Colors
from src.Blinky import Blinky
from src.Map import Map
from src.Pacman import Pacman


class Wall(pg.sprite.Sprite):

    def __init__(self, x, y, width, height, color=Colors.WHITE):
        super().__init__()

        self.image = pg.Surface([width, height])
        self.image.fill(color)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


class Game:
    def __init__(self):

        self.map_number = 2
        self.bg_image = pg.image.load(f"../res/map/map{self.map_number}.png")
        self.map = Map(f"../res/map/map{self.map_number}.json")
        self.height, self.width = self.map.get_shape()
        self.tilesize = self.map.get_tilesize()
        self.sprites_hidden = False

        self.window = pg.display.set_mode((self.width, self.height))
        pg.display.set_caption("Pacman")
        self.clock = pg.time.Clock()
        self.FPS = 60
        pg.init()

        self.wall_list = pg.sprite.Group()
        for i in range(0, self.map.get_cols()):
            for j in range(0, self.map.get_rows()):
                value = self.map.get_value(i, j)
                if value == 0 or value == 4:
                    wall = Wall(i * self.tilesize, j * self.tilesize, self.tilesize, self.tilesize, Colors.GRAY)
                    self.wall_list.add(wall)

        # todo use speeds like 2,4,8,16
        self.blinky = Blinky(216, 176, self.map, self.wall_list, 2)
        self.pacman = Pacman(216, 272, self.map, self.wall_list, 2)
        self.pacman.add_ghost(self.blinky)
        self.movingsprites = pg.sprite.Group()
        self.movingsprites.add(self.pacman)
        self.movingsprites.add(self.blinky)

    def draw(self):
        self.window.fill(Colors.BLACK)
        self.wall_list.draw(self.window)
        self.movingsprites.draw(self.window)
        if not self.sprites_hidden:
            self.window.blit(self.bg_image, (0, 0))
            self.window.blit(self.pacman.get_sprite(), self.pacman.get_sprite_pos())
            self.window.blit(self.blinky.get_sprite(), self.blinky.get_sprite_pos())
        pg.display.update()

    # Main loop
    def run(self):
        running = True

        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

                if pg.key.get_pressed()[pg.K_UP]:
                    self.pacman.move_up()
                if pg.key.get_pressed()[pg.K_DOWN]:
                    self.pacman.move_down()
                if pg.key.get_pressed()[pg.K_LEFT]:
                    self.pacman.move_left()
                if pg.key.get_pressed()[pg.K_RIGHT]:
                    self.pacman.move_right()
                if pg.key.get_pressed()[pg.K_h]:
                    self.sprites_hidden = not self.sprites_hidden

            self.pacman.move()
            self.blinky.move()
            self.draw()

            # Clock tick
            self.clock.tick(self.FPS)

        pg.quit()


if __name__ == "__main__":
    Game().run()

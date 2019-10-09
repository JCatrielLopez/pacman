import pygame as pg

from src import Colors, Spritesheet
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
        self.rect.x = x
        self.rect.y = y


class Pellet(pg.sprite.Sprite):

    def __init__(self, x, y, tilesize, is_energizer, sprites):
        super().__init__()

        self.tilesize = tilesize
        self.is_energizer = is_energizer
        self.sprites = sprites
        self.image = pg.Surface([tilesize, tilesize])
        if is_energizer:
            self.image.fill(Colors.WHITE)
        else:
            self.image.fill(Colors.LIGHT_GRAY)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def get_sprite(self):
        if self.is_energizer:
            return self.sprites[0]
        return self.sprites[1]

    def get_sprite_pos(self):
        return self.rect.x, self.rect.y


class Game:
    def __init__(self):

        self.map_number = 1
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

        sp_pellets = Spritesheet.Spritesheet("../res/map/dots.png")
        coord = []
        for i in range(5):
            coord.append((0, i * self.map.get_tilesize(), self.map.get_tilesize(), self.map.get_tilesize()))
            coord.append((self.map.get_tilesize(), i * self.map.get_tilesize(), self.map.get_tilesize(),
                          self.map.get_tilesize()))

        sprites_pellets = [sprite for sprite in sp_pellets.images_at(coord, -1)]


        self.wall_group = pg.sprite.Group()
        self.pellet_group = pg.sprite.Group()

        pellet_pos = (self.map_number-1) * 2
        energizer_pellet_pos = pellet_pos + 1
        for i in range(0, self.map.get_cols()):
            for j in range(0, self.map.get_rows()):
                value = self.map.get_value(i, j)
                if value == 0 or value == 4:
                    wall = Wall(i * self.tilesize, j * self.tilesize, self.tilesize, self.tilesize, Colors.DARK_GRAY)
                    self.wall_group.add(wall)

                if value == 1 or value == 3:
                    is_energizer = True
                    if value == 1:
                        is_energizer = False
                    pellet = Pellet(i * self.tilesize, j * self.tilesize, self.tilesize, is_energizer, [sprites_pellets[pellet_pos],sprites_pellets[energizer_pellet_pos]])
                    self.pellet_group.add(pellet)

        # todo use speeds like 2,4,8,16
        self.blinky = Blinky(216, 176, self.map, self.wall_group, 2)
        self.pacman = Pacman(216, 272, self.map, self.wall_group, 2)
        self.pacman.add_ghost(self.blinky)
        self.moving_sprites = pg.sprite.Group()
        self.moving_sprites.add(self.pacman)
        self.moving_sprites.add(self.blinky)


    def draw(self):
        self.window.fill(Colors.BLACK)
        self.wall_group.draw(self.window)
        self.pellet_group.draw(self.window)
        self.moving_sprites.draw(self.window)
        if not self.sprites_hidden:
            self.window.blit(self.bg_image, (0, 0))
            for pellet in self.pellet_group:
                self.window.blit(pellet.get_sprite(), pellet.get_sprite_pos())
            self.window.blit(self.pacman.get_sprite(), self.pacman.get_sprite_pos())
            self.window.blit(self.blinky.get_sprite(), self.blinky.get_sprite_pos())


        pg.display.update()

    # Main loop
    def run(self):
        running = True

        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT or pg.key.get_pressed()[pg.K_ESCAPE]:
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

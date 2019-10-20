import pygame as pg

from src import Colors, Spritesheet
from src.Blinky import Blinky
from src.Map import Map
from src.Pacman import Pacman
from src.Pellet import Pellet


class Wall(pg.sprite.Sprite):

    def __init__(self, x, y, width, height, color=Colors.WHITE):
        super().__init__()

        self.image = pg.Surface([width, height])
        self.image.fill(color)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Game:

    def __init__(self, map, score, lives, flags):

        self.map_number = map
        self.map = Map(f"../res/map/map{self.map_number}.json")
        self.bg_image = pg.image.load(f"../res/map/{self.map.get_bg()}")
        self.height, self.width = self.map.get_shape()
        margin_bottom = 50
        self.height += margin_bottom
        self.tilesize = self.map.get_tilesize()
        self.sprites_hidden = False

        self.window = pg.display.set_mode((self.width, self.height), flags=flags)
        pg.display.set_caption("Pacman")
        self.clock = pg.time.Clock()
        self.FPS = 60

        self.score = score
        self.highscore = self.score

        pg.init()

        sp_pellets = Spritesheet.Spritesheet("../res/map/Dots.png")
        coord = []
        for i in range(5):
            coord.append((0, i * self.map.get_tilesize(), self.map.get_tilesize(), self.map.get_tilesize()))
            coord.append((self.map.get_tilesize(), i * self.map.get_tilesize(), self.map.get_tilesize(),
                          self.map.get_tilesize()))

        sprites_pellets = [sprite for sprite in sp_pellets.images_at(coord, -1)]

        self.wall_group = pg.sprite.Group()
        self.pellet_group = pg.sprite.Group()

        pellet_pos = (self.map_number - 1) * 2
        energizer_pellet_pos = pellet_pos + 1
        for i in range(0, self.map.get_cols()):
            for j in range(0, self.map.get_rows()):
                value = self.map.get_value(i, j)
                if value == 0 or value == 4:
                    wall = Wall(i * self.tilesize, j * self.tilesize, self.tilesize, self.tilesize, Colors.DARK_GRAY)
                    self.wall_group.add(wall)

                if value == 1 or value == 3:
                    is_energizer = value != 1
                    pellet = Pellet(i * self.tilesize, j * self.tilesize, self.tilesize, is_energizer,
                                    [sprites_pellets[pellet_pos], sprites_pellets[energizer_pellet_pos]])
                    self.pellet_group.add(pellet)

        # Characters
        self.start_pos_pacman = (216, 272)
        self.blinky = Blinky(216, 176, self.map, self.wall_group, 2)
        self.pacman = Pacman(self.start_pos_pacman, self.map, self.wall_group, 2, lives)
        self.pacman.add_ghost(self.blinky)
        self.moving_sprites = pg.sprite.Group()
        self.moving_sprites.add(self.pacman)
        self.moving_sprites.add(self.blinky)

        # On screen text
        pg.font.init()
        self.font = pg.font.SysFont('default', 25, bold=True)
        self.text_highscore = self.font.render(f"HIGH SCORE: {self.highscore}", False, Colors.WHITE)
        self.text_score = self.font.render(f"SCORE: {self.score}", False, Colors.WHITE)
        self.text_lives = self.font.render(f"x{self.pacman.get_lives()}", False, Colors.WHITE)
        self.fullscreen = False

    def change_map(self, new_map):
        if self.fullscreen:
            self.__init__(new_map, self.score, self.pacman.get_lives(), pg.FULLSCREEN)
        else:
            self.__init__(new_map, self.score, self.pacman.get_lives(), pg.NOFRAME)

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        screen = pg.display.get_surface()
        tmp = screen.convert()
        caption = pg.display.get_caption()
        flags = screen.get_flags()
        bits = screen.get_bitsize()

        pg.display.quit()
        pg.display.init()

        screen = pg.display.set_mode((self.width, self.height), flags + pg.FULLSCREEN, bits)
        screen.blit(tmp, (0, 0))
        pg.display.set_caption(*caption)

        pg.key.set_mods(0)

        return screen

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
        self.window.blit(self.text_highscore, (15, 510))
        self.window.blit(self.text_lives, (self.width - 75, 510))
        self.window.blit(self.text_score, (self.width / 2 - 20, 510))
        pg.display.update()

    def restart(self):
        self.pacman.restart()

    # Main loop
    def run(self):
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT or pg.key.get_pressed()[pg.K_ESCAPE]:
                    running = False

                if pg.key.get_pressed()[pg.K_f]:
                    self.window = self.toggle_fullscreen()
                if pg.key.get_pressed()[pg.K_UP]:
                    self.pacman.move_up()
                if pg.key.get_pressed()[pg.K_DOWN]:
                    self.pacman.move_down()
                if pg.key.get_pressed()[pg.K_LEFT]:
                    self.pacman.move_left()
                if pg.key.get_pressed()[pg.K_RIGHT]:
                    self.pacman.move_right()

                if pg.key.get_pressed()[pg.K_r]:
                    self.restart()
                if pg.key.get_pressed()[pg.K_1]:
                    self.change_map(1)
                if pg.key.get_pressed()[pg.K_2]:
                    self.change_map(2)
                if pg.key.get_pressed()[pg.K_3]:
                    self.change_map(3)
                if pg.key.get_pressed()[pg.K_4]:
                    self.change_map(4)
                if pg.key.get_pressed()[pg.K_5]:
                    self.change_map(5)

                if pg.key.get_pressed()[pg.K_h]:
                    self.sprites_hidden = not self.sprites_hidden

            # Pellets
            colliding_idx = self.pacman.rect.collidelistall(self.pellet_group.sprites())
            colliding = [self.pellet_group.sprites()[i] for i in colliding_idx]

            if len(colliding) != 0:
                self.pellet_group.remove(colliding[0])
                self.score += colliding[0].score()
                self.highscore = max(self.score, self.highscore)
                self.text_highscore = self.font.render(f"HIGH SCORE: {self.highscore}", False, Colors.WHITE)
                self.text_score = self.font.render(f"SCORE: {self.score}", False, Colors.WHITE)

            if len(self.pellet_group.sprites()) == 0:
                if self.map_number < 5:
                    self.change_map(self.map_number + 1)
                else:
                    self.change_map(1)

            self.pacman.move()
            self.text_lives = self.font.render(f"x{self.pacman.get_lives()}", False, Colors.WHITE)
            # self.blinky.move()
            self.draw()

            # Clock tick
            self.clock.tick(self.FPS)

        pg.quit()


if __name__ == "__main__":
    pass

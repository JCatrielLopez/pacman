import pygame as pg

from src import Colors
from src.characters.Blinky import Blinky
from src.characters.Pacman import Pacman
from src.game import windowmanager
from src.game.map import Map


class Game:

    def __init__(self, index):

        # Pygame init
        pg.init()

        self.map_index = index
        map = Map(f"../res/map/map{index}.json", index)  # TODO Cambiar nombres para no tener map = map.map()

        margin_x = 0
        margin_y = 50
        original_size = map.get_shape()
        map_size = (original_size[1] + margin_x, original_size[0] + margin_y)

        # Window
        self.wm = windowmanager.WindowManager(map_size, color=Colors.BLACK, image=f"../res/map/{map.get_bg()}")
        self.wm.set_caption("Pacman")
        self.wm.set_icon("../res/icon.png")

        # Game variables
        self.clock = pg.time.Clock()
        self.FPS = 60

        self.score = 0
        self.highscore = 0

        # Walls
        map.init_map_elements()
        self.wall_group = map.get_walls()

        # Pellets
        self.pellet_group = map.get_pellets()

        # Characters
        start_pos_pacman = (216, 272)
        self.blinky = Blinky(216, 176, map, self.wall_group, 2)
        self.pacman = Pacman(start_pos_pacman, map, 2, 3)
        self.pacman.add_ghost(self.blinky)
        self.moving_sprites = pg.sprite.Group()
        self.moving_sprites.add(self.pacman)
        self.moving_sprites.add(self.blinky)

        # On screen text
        self.text_highscore = f"HIGH SCORE: {self.highscore}"
        self.text_score = f"SCORE: {self.score}"
        self.text_lives = f"x{self.pacman.get_lives()}"

        # Sprites -> WindowManager
        self.wm.add_group(self.wall_group)
        self.wm.add_group(self.pellet_group)
        self.wm.add_group(self.moving_sprites)

    def change_map(self, new_index):
        new_map = Map(f"../res/map/map{new_index}.json", new_index)
        new_map.init_map_elements()

        self.wall_group = new_map.get_walls()
        self.pellet_group = new_map.get_pellets()
        new_groups = [self.wall_group, self.pellet_group, self.moving_sprites]

        # self.pacman.set_walls(self.wall_group)
        self.pacman.set_map(new_map)
        self.pacman.restart()
        self.wm.change_map(f"../res/map/{new_map.get_bg()}", new_groups)
        self.map_index = new_index

    def draw(self):
        self.wm.draw()
        self.wm.render_text(self.text_highscore, False, Colors.WHITE, (15, 510))
        self.wm.render_text(self.text_lives, False, Colors.WHITE, (496 - 75, 510))
        self.wm.render_text(self.text_score, False, Colors.WHITE, (496 / 2 - 50, 510))
        self.wm.update()

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
                    self.wm.toggle_fullscreen()
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
                    self.wm.hide_sprites()

            # Pellets
            colliding_idx = self.pacman.rect.collidelistall(self.pellet_group.sprites())
            colliding = [self.pellet_group.sprites()[i] for i in colliding_idx]

            if len(colliding) != 0:
                self.pellet_group.remove(colliding[0])
                self.score += colliding[0].score()
                self.highscore = max(self.score, self.highscore)
                self.text_highscore = f"HIGH SCORE: {self.highscore}"
                self.text_score = f"SCORE: {self.score}"

            if len(self.pellet_group.sprites()) == 0:
                if self.map_index != 5:
                    self.change_map(self.map_index + 1)
                else:
                    self.change_map(1)

            self.pacman.move()
            self.text_lives = f"x{self.pacman.get_lives()}"
            # self.blinky.move()
            self.draw()

            # Clock tick
            self.clock.tick(self.FPS)

        pg.quit()


if __name__ == "__main__":
    pass

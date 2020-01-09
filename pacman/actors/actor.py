import pygame as pg

from .. import constants, spritesheet as sp


class Actor(pg.sprite.Sprite):
    rect = None
    image = None

    def __init__(self, x, y, width, height, color, *groups):
        super().__init__(*groups)

        self.image = pg.Surface([width, height])
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.timer = 0.0

    def in_collision(self, hitbox):
        pass


class MovingActor(Actor):
    direction = None
    sprites_up = None
    sprites_down = None
    sprites_left = None
    sprites_right = None
    current_sprite = None

    timer = None
    increment = 1 / constants.FPS

    def __init__(self, x, y, width, height, color, res_path, current_map, *groups):
        super().__init__(x, y, width, height, color, *groups)

        self.set_spritesheet(res_path)
        self.current_sprite = 0
        self.direction = constants.LEFT
        self.next_dir = constants.LEFT

        self.original_x = x
        self.original_y = y

        self.current_map = current_map

    def restart(self):
        self.rect.x = self.original_x
        self.rect.y = self.original_y
        self.direction = constants.LEFT

    def set_spritesheet(self, path):
        coord = []
        sprites_dim = constants.TILE_SIZE * 2
        for i in range(8):
            coord.append((i * sprites_dim, 0, sprites_dim, sprites_dim))

        sp_left = sp.Spritesheet(f"{path}/spritesheet_left.png")
        sp_right = sp.Spritesheet(f"{path}/spritesheet_right.png")
        sp_up = sp.Spritesheet(f"{path}/spritesheet_up.png")
        sp_down = sp.Spritesheet(f"{path}/spritesheet_down.png")

        self.sprites_left = [sprite for sprite in sp_left.images_at(coord, -1)]
        self.sprites_right = [sprite for sprite in sp_right.images_at(coord, -1)]
        self.sprites_up = [sprite for sprite in sp_up.images_at(coord, -1)]
        self.sprites_down = [sprite for sprite in sp_down.images_at(coord, -1)]

    def get_sprite(self):
        out_index = self.current_sprite
        self.current_sprite += 1
        self.current_sprite = self.current_sprite % len(self.sprites_left)

        out_sprite = None
        if self.direction == constants.UP:
            out_sprite = self.sprites_up[out_index]
        if self.direction == constants.DOWN:
            out_sprite = self.sprites_down[out_index]
        if self.direction == constants.LEFT:
            out_sprite = self.sprites_left[out_index]
        if self.direction == constants.RIGHT:
            out_sprite = self.sprites_right[out_index]

        return out_sprite

    def get_pos(self):
        return (
            self.rect.centerx - constants.TILE_SIZE,
            self.rect.centery - constants.TILE_SIZE,
        )

    def move_up(self):
        if self.direction != constants.UP:
            if self.direction == constants.DOWN:
                self.direction = constants.UP
                self.next_dir = None
            else:
                self.next_dir = constants.UP

    def move_down(self):
        if self.direction != constants.DOWN:
            if self.direction == constants.UP:
                self.direction = constants.DOWN
                self.next_dir = None
            else:
                self.next_dir = constants.DOWN

    def move_left(self):
        if self.direction != constants.LEFT:
            if self.direction == constants.RIGHT:
                self.direction = constants.LEFT
                self.next_dir = None
            else:
                self.next_dir = constants.LEFT

    def move_right(self):
        if self.direction != constants.RIGHT:
            if self.direction == constants.LEFT:
                self.direction = constants.RIGHT
                self.next_dir = None
            else:
                self.next_dir = constants.RIGHT

    def move(self):

        if (
                self.rect.x % constants.TILE_SIZE == 0
                and self.rect.y % constants.TILE_SIZE == 0
                and self.next_dir is not None
        ):
            j = int(self.rect.x / constants.TILE_SIZE)
            i = int(self.rect.y / constants.TILE_SIZE)
            j += self.next_dir[0]
            i += self.next_dir[1]

            if self.current_map.is_valid((j, i)) or self.current_map.get_value((j, i)) == 4:
                self.direction = self.next_dir
                self.next_dir = None

        self.rect.x += self.direction[0]
        if 0 < self.rect.x < constants.COLS * constants.TILE_SIZE:
            self.rect.y += self.direction[1]
        self.adjust_movement()
        self.add_timer()

        # ghosts_hit_list = pg.sprite.spritecollide(self, self.ghosts, False)
        # for ghost in ghosts_hit_list:
        #     print("Hit", ghost.name, "at:", ghost.rect.x, ",", ghost.rect.y)

        # if len(ghosts_hit_list) > 0:
        #     self.restart()

        self.check_limits()

    def check_limits(self):

        if self.rect.x == -constants.TILE_SIZE:
            self.rect.x = constants.TILE_SIZE * constants.COLS
        if self.rect.x == (constants.COLS + 1) * constants.TILE_SIZE:
            self.rect.x = -constants.TILE_SIZE

    def adjust_movement(self):

        if self.direction == constants.LEFT or self.direction == constants.RIGHT:
            block_hit_list = pg.sprite.spritecollide(
                self, self.current_map.wall_group, False
            )
            for block in block_hit_list:
                if self.direction == constants.RIGHT:
                    self.rect.right = block.rect.left
                else:
                    self.rect.left = block.rect.right
        else:
            block_hit_list = pg.sprite.spritecollide(
                self, self.current_map.wall_group, False
            )
            for block in block_hit_list:
                if self.direction == constants.DOWN:
                    self.rect.bottom = block.rect.top
                else:
                    self.rect.top = block.rect.bottom

    def get_direction(self):
        return self.direction

    def add_timer(self):
        self.timer += self.increment

    def get_timer(self):
        return self.timer

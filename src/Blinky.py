import pygame as pg

import src.Spritesheet
from src import Colors


class Blinky(pg.sprite.Sprite):

    def __init__(self, x, y, map, walls, resources_path=None, speed=2):
        super().__init__()

        self.map = map
        self.walls = walls
        self.speed = speed

        self.up = [0, -self.speed]
        self.down = [0, self.speed]
        self.left = [-self.speed, 0]
        self.right = [self.speed, 0]
        self.stop = [0, 0]

        self.direction = self.right
        self.next_dir = None

        self.image = pg.Surface([map.get_tilesize(), map.get_tilesize()])
        self.image.fill(Colors.RED)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

        coord = []
        for i in range(8):
            coord.append((i * map.get_tilesize() * 2, 0, map.get_tilesize() * 2, map.get_tilesize() * 2))

        self.name = "Blinky"
        resources_path = f"../res/ghosts/{self.name}"
        sp_left = src.Spritesheet.Spritesheet(f"{resources_path}/spritesheet_left.png")
        sp_right = src.Spritesheet.Spritesheet(f"{resources_path}/spritesheet_right.png")
        sp_up = src.Spritesheet.Spritesheet(f"{resources_path}/spritesheet_up.png")
        sp_down = src.Spritesheet.Spritesheet(f"{resources_path}/spritesheet_down.png")
        sp_frightened = src.Spritesheet.Spritesheet(f"../res/ghosts/frightened_spritesheet.png")
        sp_frightened_white = src.Spritesheet.Spritesheet(f"../res/ghosts/frightened_white_spritesheet.png")

        self.sprites_left = [sprite for sprite in sp_left.images_at(coord, -1)]
        self.sprites_right = [sprite for sprite in sp_right.images_at(coord, -1)]
        self.sprites_up = [sprite for sprite in sp_up.images_at(coord, -1)]
        self.sprites_down = [sprite for sprite in sp_down.images_at(coord, -1)]
        self.sprites_frightened = [sprite for sprite in sp_frightened.images_at(coord, -1)]
        self.sprites_frightened_white = [sprite for sprite in sp_frightened_white.images_at(coord, -1)]

        self.current_sprite = 0

    def adjust_movement(self):

        if self.direction == self.left or self.direction == self.right:
            # Did this update cause us to hit a wall?
            block_hit_list = pg.sprite.spritecollide(self, self.walls, False)
            for block in block_hit_list:
                # If we are moving right, set our right side to the left side of
                # the item we hit
                if self.direction == self.right:
                    self.rect.right = block.rect.left
                else:
                    # Otherwise if we are moving left, do the opposite.
                    self.rect.left = block.rect.right
        else:
            # Check and see if we hit anything
            block_hit_list = pg.sprite.spritecollide(self, self.walls, False)
            for block in block_hit_list:
                # Reset our position based on the top/bottom of the object.
                if self.direction == self.down:
                    self.rect.bottom = block.rect.top
                else:
                    self.rect.top = block.rect.bottom

    def get_sprite_pos(self):
        return self.rect.centerx - self.map.get_tilesize(), self.rect.centery - self.map.get_tilesize()

    def get_sprite(self):
        out_index = self.current_sprite
        self.current_sprite += 1
        self.current_sprite = self.current_sprite % len(self.sprites_left)

        out_sprite = self.sprites_frightened[out_index]
        if self.direction == self.up:
            out_sprite = self.sprites_up[out_index]
        if self.direction == self.down:
            out_sprite = self.sprites_down[out_index]
        if self.direction == self.left:
            out_sprite = self.sprites_left[out_index]
        if self.direction == self.right:
            out_sprite = self.sprites_right[out_index]

        return out_sprite

    def check_limits(self):
        tilesize = self.map.get_tilesize()
        cols = self.map.get_cols()

        if self.rect.x == -tilesize:
            self.rect.x = tilesize * cols
        if self.rect.x == (cols + 1) * tilesize:
            self.rect.x = -tilesize

    def move(self, target):
        tilesize = self.map.get_tilesize()
        cols = self.map.get_cols()

        self.direction = self.get_dir(target)

        if self.rect.x % tilesize == 0 and self.rect.y % tilesize == 0 and self.next_dir is not None:
            j = int(self.rect.x / tilesize)
            i = int(self.rect.y / tilesize)
            j += int(self.next_dir[0] / self.speed)
            i += int(self.next_dir[1] / self.speed)
            if self.map.is_valid([j, i]):
                self.direction = self.next_dir
                self.next_dir = None

        self.rect.x += self.direction[0]
        if 0 < self.rect.x < cols * tilesize:  # The pacman could be passing through a tunnel
            self.rect.y += self.direction[1]
        self.adjust_movement()

        self.check_limits()

    def move_up(self):
        if self.direction != self.up:  # If we are changing direction
            if self.direction == self.down:
                self.direction = self.up
                self.next_dir = None
            else:
                self.next_dir = self.up

    def move_down(self):
        if self.direction != self.down:
            if self.direction == self.up:
                self.direction = self.down
                self.next_dir = None
            else:
                self.next_dir = self.down

    def move_left(self):
        if self.direction != self.left:
            if self.direction == self.right:
                self.direction = self.left
                self.next_dir = None
            else:
                self.next_dir = self.left

    def move_right(self):
        if self.direction != self.right:
            if self.direction == self.left:
                self.direction = self.right
                self.next_dir = None
            else:
                self.next_dir = self.right

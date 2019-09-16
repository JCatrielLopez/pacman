import pygame as pg

import src.Spritesheet
from src.MapLoader import MapLoader


class Character(object):
    def __init__(self, pos_x, pos_y, resources_path=".", speed=1):

        self._map = MapLoader('../res/map/Maze1.json')
        self.MAP_HEIGHT, self.MAP_WIDTH = self._map.get_shape()
        self.MAP_TILESIZE = 20

        self.XLIMIT = int(self.MAP_WIDTH)
        self.YLIMIT = int(self.MAP_HEIGHT)

        self.pos = [pos_x, pos_y]

        self.hitbox = pg.Rect(pos_x, pos_y, self.MAP_TILESIZE, self.MAP_TILESIZE)

        coord = [
            (0, 0, 16, 16),
            (16, 0, 16, 16),
            (32, 0, 16, 16),
            (48, 0, 16, 16),
            (64, 0, 16, 16),
            (80, 0, 16, 16),
            (96, 0, 16, 16),
            (112, 0, 16, 16),
            (128, 0, 16, 16),
        ]

        self.sp_left = src.Spritesheet.spritesheet(
            f"{resources_path}/spritesheet_left.png"
        )
        self.sp_right = src.Spritesheet.spritesheet(
            f"{resources_path}/spritesheet_right.png"
        )
        self.sp_up = src.Spritesheet.spritesheet(
            f"{resources_path}/spritesheet_up.png"
        )
        self.sp_down = src.Spritesheet.spritesheet(
            f"{resources_path}/spritesheet_down.png"
        )

        self.sprites_left = [
            sprite for sprite in self.sp_left.images_at(coord, -1)
        ]
        self.sprites_right = [
            sprite for sprite in self.sp_right.images_at(coord, -1)
        ]
        self.sprites_up = [sprite for sprite in self.sp_up.images_at(coord, -1)]
        self.sprites_down = [
            sprite for sprite in self.sp_down.images_at(coord, -1)
        ]

        self.current_sprite = 0

        self.speed = speed

        self.up = [0, -self.speed]
        self.down = [0, self.speed]
        self.left = [-self.speed, 0]
        self.right = [self.speed, 0]

        self.direction = self.right

    def get_sprite(self):
        out_index = self.current_sprite
        self.current_sprite += 1
        self.current_sprite = self.current_sprite % len(self.sprites_left)

        self.move()

        if self.direction == self.up:
            return pg.transform.scale(self.sprites_up[out_index], (32, 32))
        if self.direction == self.down:
            return pg.transform.scale(self.sprites_down[out_index], (32, 32))
        if self.direction == self.left:
            return pg.transform.scale(self.sprites_left[out_index], (32, 32))
        if self.direction == self.right:
            return pg.transform.scale(self.sprites_right[out_index], (32, 32))

    def move_up(self):
        self.direction = self.up

    def move_down(self):
        self.direction = self.down

    def move_left(self):
        self.direction = self.left

    def move_right(self):
        self.direction = self.right

    def get_pos(self):
        return self.hitbox.centerx - 16, self.hitbox.centery - 16

    def get_grid_pos(self):
        sprite_center = self.pos[0] + 10, self.pos[1] + 10
        return int(sprite_center[0] / self.MAP_TILESIZE), int(sprite_center[1] / self.MAP_TILESIZE)

    def check_pos(self):
        if self.pos[0] >= self.XLIMIT:
            self.pos[0] = 0
        elif self.pos[0] < 0:
            self.pos[0] = self.XLIMIT
        elif self.pos[1] >= self.YLIMIT:
            self.pos[1] = 0
        elif self.pos[1] < 0:
            self.pos[1] = self.YLIMIT

    def move(self):
        current_pos = self.get_pos()
        next_pos = current_pos[0] + self.direction[0] * 10, current_pos[1] + self.direction[1] * 10
        new_grid = self._map.get_grid(next_pos)


        if self._map.is_valid(new_grid):
            self.pos[0] = next_pos[0]
            self.pos[1] = next_pos[1]
            self.check_pos()

            self.hitbox.move_ip(self.direction[0], self.direction[1])

    def get_hitbox(self):
        return self.hitbox

    def hit(self, hitbox):
        return self.hitbox.colliderect(hitbox)

import pygame as pg

import src.game.spritesheet
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
        self.moves = [self.up, self.down, self.right, self.left]

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
        sp_left = src.game.spritesheet.Spritesheet(f"{resources_path}/spritesheet_left.png")
        sp_right = src.game.spritesheet.Spritesheet(f"{resources_path}/spritesheet_right.png")
        sp_up = src.game.spritesheet.Spritesheet(f"{resources_path}/spritesheet_up.png")
        sp_down = src.game.spritesheet.Spritesheet(f"{resources_path}/spritesheet_down.png")
        sp_frightened = src.game.spritesheet.Spritesheet(f"../res/ghosts/frightened_spritesheet.png")
        sp_frightened_white = src.game.spritesheet.Spritesheet(f"../res/ghosts/frightened_white_spritesheet.png")

        self.sprites_left = [sprite for sprite in sp_left.images_at(coord, -1)]
        self.sprites_right = [sprite for sprite in sp_right.images_at(coord, -1)]
        self.sprites_up = [sprite for sprite in sp_up.images_at(coord, -1)]
        self.sprites_down = [sprite for sprite in sp_down.images_at(coord, -1)]
        self.sprites_frightened = [sprite for sprite in sp_frightened.images_at(coord, -1)]
        self.sprites_frightened_white = [sprite for sprite in sp_frightened_white.images_at(coord, -1)]

        self.current_sprite = 0

        self.corner = self.image.get_rect()
        self.corner.x = 16
        self.corner.y = 16

        self.chase = True

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

        # self.direction = self.get_dir(target)
        if self.chase:
            self.next_dir = self.next_position(target)
        else:
            self.next_dir = self.next_position(self.corner)

        if self.rect.x % tilesize == 0 and self.rect.y % tilesize == 0 and self.next_dir is not None:
            j = int(self.rect.x / tilesize)
            i = int(self.rect.y / tilesize)
            j += int(self.next_dir[0] / self.speed)
            i += int(self.next_dir[1] / self.speed)
            if self.map.is_valid([j, i]):
                self.direction = self.next_dir
                self.next_dir = None

        self.rect.x += self.direction[0]
        if 0 < self.rect.x < cols * tilesize:  # Could be passing through a tunnel
            self.rect.y += self.direction[1]

        # self.adjust_movement()

        self.check_limits()


    def reverse(self):
        reverse = [0, 0]
        if self.direction[0] != 0:
            reverse[0] = -self.direction[0]
        elif self.direction[1] != 0:
            reverse[1] = -self.direction[1]
        return reverse

    def get_positions(self):
        positions = []
        for move in self.moves:
            index = self.get_pos_index(move)
            if self.map.is_valid(index) and move != self.reverse():
                positions.append(move)
        return positions

    def get_pos_index(self, pos):

        j = int(self.rect.x / self.map.tilesize)
        i = int(self.rect.y / self.map.tilesize)
        if pos is not None:
            j += int(pos[0] / self.speed)
            i += int(pos[1] / self.speed)

        return [j, i]

    def next_position(self, target):
        positions = self.get_positions()
        if len(positions) == 1:
            return positions[0]
        elif len(positions) > 1:
            next = positions[0]
            index_target = self.map.get_index(self.get_pos_value(target))
            for pos in positions:
                if self.map.is_valid(pos):
                    if self.map.get_distance(
                            [self.map.get_index(self.get_pos_index(pos)), index_target]) < self.map.get_distance(
                            [self.map.get_index(self.get_pos_index(next)), index_target]):
                        next = pos
            return next

    def get_pos_value(self, value):
        return [int(value[1] / self.map.tilesize), int(value[0] / self.map.tilesize)]

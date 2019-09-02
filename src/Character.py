import src.Spritesheet
from src.MapLoader import MapLoader


class Character(object):
    def __init__(self, pos_x, pos_y, resources_path=".", speed=1):

        self._map = MapLoader('maze1.json')
        self.MAP_HEIGHT, self.MAP_WIDTH = self._map.get_shape()
        self.MAP_TILESIZE = 20

        self.XLIMIT = int(self.MAP_WIDTH / self.MAP_TILESIZE)
        self.YLIMIT = int(self.MAP_HEIGHT / self.MAP_TILESIZE)

        self.pos = [pos_x, pos_y]

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
            sprite for sprite in self.sp_left.images_at(coord)
        ]
        self.sprites_right = [
            sprite for sprite in self.sp_right.images_at(coord)
        ]
        self.sprites_up = [sprite for sprite in self.sp_up.images_at(coord)]
        self.sprites_down = [
            sprite for sprite in self.sp_down.images_at(coord)
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

        self.pos[0] += self.direction[0]
        self.pos[1] += self.direction[1]
        self.check_pos()

        if self.direction == self.up:
            return self.sprites_up[out_index]
        if self.direction == self.down:
            return self.sprites_down[out_index]
        if self.direction == self.left:
            return self.sprites_left[out_index]
        if self.direction == self.right:
            return self.sprites_right[out_index]

    def move_up(self):
        self.direction = self.up

    def move_down(self):
        self.direction = self.down

    def move_left(self):
        self.direction = self.left

    def move_right(self):
        self.direction = self.right

    def get_pos(self):
        return self.pos[0] * self.MAP_TILESIZE, self.pos[1] * self.MAP_TILESIZE

    def check_pos(self):
        if self.pos[0] > self.XLIMIT:
            self.pos[0] = 0
        elif self.pos[0] < 0:
            self.pos[0] = self.XLIMIT
        elif self.pos[1] > self.YLIMIT:
            self.pos[1] = 0
        elif self.pos[1] < 0:
            self.pos[1] = self.YLIMIT

import numpy as np
import pygame as pg

from . import constants
from .actors import pellet
from .actors import wall


class Map:
    # PEP8: Constants are usually defined on a module level and written in all capital letters with underscores
    #       separating words.
    # PEP8: Use one leading underscore only for non-public methods and instance variables.

    map_index = None
    bg_image = None
    wall_group = None
    pellet_group = None
    index = None

    def __init__(self, path, index):
        loaded = np.load(path, allow_pickle=True)

        self.maze = loaded["maze"]
        self.indexes = loaded["indexes"].item()
        self.distances = loaded["distances"].transpose()
        self.bg_image = str(loaded["bg_image"])
        self.index = int(loaded["index"])
        print(self.index)
        self.map_index = index
        self.wall_group = pg.sprite.Group()
        self.pellet_group = pg.sprite.Group()

        for i in range(0, constants.COLS):
            for j in range(0, constants.ROWS):
                value = self.get_value((i, j))

                if value in [0, 4]:
                    wall.Wall(
                        i * constants.TILE_SIZE,
                        j * constants.TILE_SIZE,
                        constants.TILE_SIZE,
                        constants.TILE_SIZE,
                        self.wall_group,
                    )
                elif value in [1, 3]:
                    pellet.Pellet(
                        i * constants.TILE_SIZE,
                        j * constants.TILE_SIZE,
                        constants.TILE_SIZE,
                        constants.TILE_SIZE,
                        value != 1,
                        self.map_index,
                        self.pellet_group,
                    )

    def __new__(cls, path, index):
        if not hasattr(cls, "instance"):
            cls.instance = super(Map, cls).__new__(cls)
        return cls.instance

    def is_valid(self, position):
        value = self.get_value(position)
        return value in [1, 2, 3]

    def get_value(self, position):
        try:
            return self.maze[position[0]][position[1]]
        except IndexError:
            return -1

    def get_grid(self, position):
        x = int(np.ceil(position[0] / constants.TILE_SIZE))
        y = int(np.ceil(position[1] / constants.TILE_SIZE))

        return x, y

    def get_distance(self, begin, end):
        try:
            row = self.indexes[begin]
            col = self.indexes[end]
        except KeyError:
            # Estamos en un tunel!
            return 0

        return self.distances[row][col]

    def get_walls(self):
        return self.wall_group

    def get_pellets(self):
        return self.pellet_group

    def get_background(self):
        return self.bg_image


if __name__ == "__main__":
    pass

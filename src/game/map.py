import json

import numpy as np
import pygame as pg

from src import Colors
from src.Pellet import Pellet
from src.game import spritesheet
from src.game.wall import Wall


class Map:

    def __init__(self, input_file, index):

        self.ind = index
        with open(input_file, 'r') as file:
            f = json.load(file)

        nodes = f["costsMatrixSize"]
        self.rows = f['mazeRows']
        self.cols = f['mazeCols']
        self.map = np.fromstring(f["maze"], dtype=int, sep=',').reshape((self.rows, self.cols), order='C').transpose()
        self.distances = np.fromstring(f["costsMatrix"], dtype=int, sep=',').reshape((nodes, nodes), order='C')

        self.indexDict = f["indexDictionary"]

        self.tilesize = f['tileSize']
        self.bg_path = f["bg_image"]

        self.wall_group = pg.sprite.Group()
        self.pellet_group = pg.sprite.Group()
                    
    def is_valid(self, position):
        try:
            v = self.get_value(position[0], position[1])
            return v in [1, 2, 3]
        except IndexError:
            return False

    def get_distance(self, position):
        return self.distances[position[0], position[1]]

    def get_index(self, position):
        return int(self.indexDict[f"{position[0]}-{position[1]}"])

    def get_bg(self):
        return self.bg_path

    def get_shape(self):
        return self.rows * self.tilesize, self.cols * self.tilesize

    def get_value(self, x, y):
        return self.map[x, y]

    def get_grid(self, position):
        return int((position[0]) / self.tilesize), int((position[1]) / self.tilesize)

    def get_tilesize(self):
        return self.tilesize

    def get_rows(self):
        return self.rows

    def get_cols(self):
        return self.cols

    def init_map_elements(self):
        sp_pellets = spritesheet.Spritesheet("../res/map/Dots.png")
        coord = []
        for i in range(5):
            coord.append((0, i * self.get_tilesize(), self.get_tilesize(), self.get_tilesize()))
            coord.append((self.get_tilesize(), i * self.get_tilesize(), self.get_tilesize(),
                          self.get_tilesize()))

        sprites_pellets = [sprite for sprite in sp_pellets.images_at(coord, -1)]

        pellet_pos = (self.ind - 1) * 2
        energizer_pellet_pos = pellet_pos + 1
        tilesize = self.get_tilesize()
        for i in range(0, self.get_cols()):
            for j in range(0, self.get_rows()):
                value = self.get_value(i, j)
                if value == 0 or value == 4:
                    wall = Wall(i * tilesize, j * tilesize, tilesize, tilesize, Colors.DARK_GRAY)
                    self.wall_group.add(wall)

                if value in [1, 3]:
                    is_energizer = value != 1
                    pellet = Pellet(i * tilesize, j * tilesize, tilesize, is_energizer,
                                    [sprites_pellets[pellet_pos], sprites_pellets[energizer_pellet_pos]])
                    self.pellet_group.add(pellet)

    def get_walls(self):
        return self.wall_group

    def get_pellets(self):
        return self.pellet_group


if __name__ == '__main__':
    pass

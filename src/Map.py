import json

import numpy as np


class Map:

    def __init__(self, input_file):
        with open(input_file, 'r') as file:
            f = json.load(file)

        nodes = f["costsMatrixSize"]
        self.rows = f['mazeRows']
        self.cols = f['mazeCols']
        self.map = np.fromstring(f["maze"], dtype=int, sep=',').reshape((self.rows, self.cols), order='C').transpose()
        self.distances = np.fromstring(f["costsMatrix"], dtype=int, sep=',').reshape((nodes, nodes), order='C')

        self.tilesize = f['tileSize']

    def is_valid(self, position):
        try:
            v = self.get_value(position[0], position[1])
            return v == 1 or v == 2 or v == 3
        except IndexError:
            print("index error")
            return False

    def get_distance(self, position):
        return self.distances[position[0], position[1]]

    def get_shape(self):
        return self.rows * self.tilesize, self.cols * self.tilesize

    def get_value(self, x, y):
        return self.map[x, y]

    def get_grid(self, position):
        return int((position[0] + 15) / self.tilesize), int((position[1] + 15) / self.tilesize)

    def get_tilesize(self):
        return self.tilesize

    def get_rows(self):
        return self.rows

    def get_cols(self):
        return self.cols


if __name__ == '__main__':
    pass

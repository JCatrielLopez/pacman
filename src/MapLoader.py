import json

import numpy as np


class MapLoader:

    def __init__(self, input_file):
        with open(input_file, 'r') as file:
            f = json.load(file)

        nodes = f["costsMatrixSize"]
        self.ROWS = f['mazeRows']
        self.COLS = f['mazeCols']
        self._map = np.fromstring(f["maze"], dtype=int, sep=',').reshape((31, 28), order='C').transpose()
        self._distances = np.fromstring(f["costsMatrix"], dtype=int, sep=',').reshape((nodes, nodes), order='C')

        self.tilesize = f["tileSize"]

    def is_valid(self, position):
        try:
            v = self.get_value(position[0], position[1])
            return v == 1 or v == 2 or v == 3
        except IndexError:
            return True

    def get_distance(self, position):
        return self._distances[position[0], position[1]]

    def get_shape(self):
        return self.ROWS * self.tilesize, self.COLS * self.tilesize

    def get_value(self, x, y):
        return self._map[x, y]

    def get_grid(self, position):
        return int((position[0] + 15) / self.tilesize), int((position[1] + 15) / self.tilesize)

    def get_tilesize(self):
        return self.tilesize


if __name__ == '__main__':
    pass

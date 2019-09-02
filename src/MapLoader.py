import json

import numpy as np


class MapLoader:

    def __init__(self, input_file):
        with open(input_file, 'r') as file:
            f = json.load(file)

        nodes = len(f["graph"])
        self.ROWS = f['ROWS']
        self.COLS = f['COLS']
        self._map = np.fromstring(f["maze"], dtype=int, sep=',').reshape((31, 28), order='C')
        self._distances = np.fromstring(f["costs-matrix"], dtype=int, sep=',').reshape((nodes, nodes), order='C')

    def is_valid(self, position):
        grid_x, grid_y = int(position[0] / 20), int(position[1] / 20)
        return self._map[grid_x, grid_y] == 1 | self._map[grid_x, grid_y] == 2

    def get_distance(self, position):
        return self._distances[position[0], position[1]]

    def get_shape(self):
        return self.ROWS * 20, self.COLS * 20

    def get_value(self, position):
        grid_x, grid_y = int(position[0] / 20), int(position[1] / 20)
        return self._map[grid_x, grid_y]


if __name__ == '__main__':
    ml = MapLoader('maze1.json')

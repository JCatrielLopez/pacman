import numpy as np


class MapLoader:

    def __init__(self, map_path, dist_path):
        self._map = np.genfromtxt(map_path, dtype=None, delimiter=1, skip_header=0)
        # self._distances = np.genfromtxt(dist_path, dtype=None, delimiter=1, skip_header=0)
        self._roads = {}

    def is_valid(self, position):
        return f"{position[0]}-{position[1]}" in self._roads.keys()

    def get_distance(self, position):
        return self._distances[position[0], position[1]]

    def get_shape(self):
        return self._map.shape[0]*20, self._map.shape[1]*20


if __name__ == '__main__':
    ml = MapLoader('Maze1.txt')
    # print(ml.is_valid((0, 0)))

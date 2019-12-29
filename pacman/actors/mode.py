import random

from .. import constants


class Mode:
    target_position = None
    options = [constants.UP, constants.DOWN, constants.LEFT, constants.RIGHT]

    def __init__(self):
        pass

    def get_target_tile(self):
        return self.target_position

    def set_target_tile(self, target):
        pass

    def get_next_dir(self, current, back, map):
        current_grid = map.get_grid(current)
        new_dir = None
        min_distance = 10000

        for opt in self.options:
            new_position = (current_grid[0] + opt[0], current_grid[1] + opt[1])
            if map.is_valid(new_position):
                new_distance = map.get_distance(
                    new_position, map.get_grid(self.target_position)
                )
                if new_distance < min_distance and opt != back:
                    min_distance = new_distance
                    new_dir = opt

        return new_dir


class Chase(Mode):
    def set_target_tile(self, target):
        self.target_position = target

    def next_mode(self):
        return Scatter()


class Frightened(Mode):
    def get_next_dir(self, current, back, map):
        opt = random.choice(self.options)
        while map.is_valid((current[0] + opt[0], current[1] + opt[1])):
            opt = random.choice(self.options)
        return opt


class Scatter(Mode):
    def set_target_tile(self, target):
        pass

    def next_mode(self):
        return Chase()

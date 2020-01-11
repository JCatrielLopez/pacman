import random

from .. import constants

SCATTER = 0
CHASE = 1
FRIGHTENED = 2
DEAD = 3


class Mode:
    target_position = None
    options = [constants.UP, constants.LEFT, constants.DOWN, constants.RIGHT]

    def __init__(self, options):
        if options is not None:
            self.options = options

    def set_options(self, options):
        self.options = options

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


class Frightened(Mode):

    def back(self, current_dir):
        return -current_dir[0], -current_dir[1]

    def get_next_dir(self, current_position, back, map):
        current_grid = map.get_grid(current_position)

        valid_options = []
        for opt in self.options:
            new_position = (current_grid[0] + opt[0], current_grid[1] + opt[1])
            if map.is_valid(new_position):
                valid_options.append(opt)

        if len(valid_options) == 2 and self.back(valid_options[0]) == valid_options[1]:
            return None

        opt = random.choice(valid_options)
        return opt

    def print_mode(self, name):
        print(name, " - mode: Frightened")

    def get_mode(self):
        return FRIGHTENED


class Dead(Mode):

    def set_target_tile(self, target):
        self.target_position = (208, 208)

    def print_mode(self, name):
        print(name, " - mode: Dead")

    def get_mode(self):
        return DEAD

    def get_next_dir(self, current_position, back, map):
        current_grid = map.get_grid(current_position)
        new_dir = None
        min_distance = 10000

        for opt in self.options:
            new_position = (current_grid[0] + opt[0], current_grid[1] + opt[1])
            if map.is_valid(new_position) or map.get_value(new_position) == 4:
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

    def set_target_corner(self, target_corner):
        pass

    def print_mode(self, name):
        print(name, " - mode: Chase")

    def get_mode(self):
        return CHASE


class Scatter(Mode):

    def set_target_tile(self, target):
        pass

    def set_target_corner(self, target_corner):
        self.target_position = target_corner

    def print_mode(self, name):
        print(name, " - mode: Scatter")

    def get_mode(self):
        return SCATTER

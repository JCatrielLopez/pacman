import numpy as np

from . import actor, mode
from .. import constants


class Ghost(actor.MovingActor):
    mode = None
    next_tile = None
    name = None
    mode_timer = 0
    scare_timer = 5.0
    scared = False
    score = 800
    pacman = None
    target_corner = None
    resources_path = None

    def __init__(
            self, x, y, width, height, res_path, pacman, current_map=None, *groups
    ):
        super().__init__(
            x, y, width, height, constants.RED, res_path, current_map, *groups
        )

        self.resources_path = res_path
        self.pacman = pacman
        self.mode = mode.Chase()
        self.mode_timer = 20.0
        self.mode.get_target_tile()

    def back(self, current_dir):
        return -current_dir[0], -current_dir[1]

    def check_mode(self):

        if (self.timer - self.last_timer) >= self.scare_timer:
            self.mode = mode.Chase()
            self.scared = False
            self.set_spritesheet(self.resources_path)
            self.last_timer = self.timer

        if (self.timer - self.last_timer) >= self.mode_timer:
            self.mode = self.mode.next_mode()
            self.last_timer = self.timer

    def scare(self):
        self.mode = mode.Frightened()
        self.scared = True
        self.last_timer = self.timer
        self.set_spritesheet("../res/ghosts/scared")

    def is_scared(self):
        return self.scared

    def get_score(self):
        return self.score

    def restart(self):
        pass


class Blinky(Ghost):
    def __init__(self, x, y, width, height, res_path, pacman, *groups):
        super().__init__(x, y, width, height, res_path, pacman, *groups)
        self.target_corner = (432, 0)

    def move(self):
        self.check_mode()
        self.mode.set_target_tile(self.pacman.get_pos())

        self.next_dir = self.mode.get_next_dir(
            self.get_pos(), self.back(self.direction), self.current_map
        )
        super().move()


class Pinky(Ghost):
    def __init__(self, x, y, width, height, res_path, pacman, *groups):
        super().__init__(x, y, width, height, res_path, pacman, *groups)

        self.target_corner = (0, 0)

    def move(self):
        self.check_mode()
        pacman_position = self.pacman.get_pos()
        pacman_direction = self.pacman.get_direction()
        new_target = (
            pacman_position[0] + pacman_direction[0] * constants.TILE_SIZE * 4 + 8,
            pacman_position[1] + pacman_direction[1] * constants.TILE_SIZE * 4 + 8,
        )

        self.mode.set_target_tile(new_target)
        self.next_dir = self.mode.get_next_dir(
            self.get_pos(), self.back(self.direction), self.current_map
        )
        super().move()


class Inky(Ghost):
    def __init__(self, x, y, width, height, res_path, pacman, blinky, *groups):
        super().__init__(x, y, width, height, res_path, pacman, *groups)
        self.blinky = blinky

        self.target_corner = (432, 480)

    def move(self):
        self.check_mode()
        pacman_position = self.pacman.get_pos()
        blinky_position = self.blinky.get_pos()

        pacman_direction = self.pacman.get_direction()

        aux = (
            pacman_position[0] + pacman_direction[0] * constants.TILE_SIZE * 2 + 8,
            pacman_position[1] + pacman_direction[1] * constants.TILE_SIZE * 2 + 8,
        )

        vector = np.array(blinky_position) - np.array(aux)

        distance = np.sqrt(np.power(vector[0], 2) + np.power(vector[1], 2))

        new_target = self.get_pos()
        new_target = (new_target[0] + distance, new_target[1] + distance)

        self.mode.set_target_tile(new_target)
        self.next_dir = self.mode.get_next_dir(
            self.get_pos(), self.back(self.direction), self.current_map
        )
        super().move()


class Clyde(Ghost):
    def __init__(self, x, y, width, height, res_path, pacman, *groups):
        super().__init__(x, y, width, height, res_path, pacman, *groups)
        self.target_corner = (0, 480)

    def move(self):
        self.check_mode()

        pacman_grid = self.current_map.get_grid(self.pacman.get_pos())
        clyde_grid = self.current_map.get_grid(self.get_pos())

        if self.current_map.get_distance(pacman_grid, clyde_grid) < 8:
            self.mode.set_target_tile(self.target_corner)
        else:
            self.mode.set_target_tile(self.pacman.get_pos())

        self.next_dir = self.mode.get_next_dir(
            self.get_pos(), self.back(self.direction), self.current_map
        )
        super().move()

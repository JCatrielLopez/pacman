import numpy as np

from . import actor, mode
from .. import constants


class Ghost(actor.MovingActor):
    # TODO agregar comer fantasmas y que vuelvan a la casa - que inicien en la casa

    scared = False
    score = 800
    last_timer_mode = None
    last_timer_scare = None

    def __init__(
            self, x, y, width, height, res_path, pacman, current_map=None, *groups
    ):
        super().__init__(
            x, y, width, height, constants.RED, res_path, current_map, *groups
        )

        self.next_tile = None
        self.name = None
        self.target_corner = None
        self.options = None

        self.last_timer_mode = 0.0
        self.last_timer_scare = 0.0

        self.scare_timer = 6.0
        self.mode_timer = 5.0

        self.scatter_time_list = [7.0, 7.0, 5.0, 5.0]
        self.chase_time_list = [20.0, 20.0, 20.0, 20.0]
        self.scatter_time_index = 0
        self.chase_time_index = 0

        self.mode_timer = self.scatter_time_list[self.scatter_time_index]
        self.scatter_time_index += 1
        self.mode = mode.Scatter(self.options)
        self.last_mode = self.mode

        self.resources_path = res_path
        self.pacman = pacman

        self.color = constants.RED

    def back(self, current_dir):
        return -current_dir[0], -current_dir[1]

    def check_mode(self):

        if self.mode.get_mode() != mode.DEAD:

            if (self.timer - self.last_timer_scare) >= self.scare_timer and self.mode.get_mode() == mode.FRIGHTENED:
                self.scared = False
                self.pacman.power_up = False
                self.image.fill(self.color)
                self.set_spritesheet(self.resources_path)
                self.last_timer_scare = self.timer
                self.mode = self.last_mode
                self.mode.print_mode(self.name)

            if (self.timer - self.last_timer_mode) >= self.mode_timer:

                if self.mode.get_mode() == mode.SCATTER:
                    if self.chase_time_index < len(self.chase_time_list):
                        self.mode = mode.Chase(self.options)
                        self.mode_timer = self.chase_time_list[self.chase_time_index]
                        self.chase_time_index += 1

                else:
                    if self.scatter_time_index < len(self.scatter_time_list):
                        self.mode = mode.Scatter(self.options)
                        print("corner: " + str(self.target_corner))
                        self.mode.set_target_corner(self.target_corner)
                        self.mode_timer = self.scatter_time_list[self.scatter_time_index]
                        self.scatter_time_index += 1

                self.last_timer_mode = self.timer
                self.mode.print_mode(self.name)

    def scare(self):
        self.last_mode = self.mode
        self.mode_timer += self.scare_timer
        self.mode = mode.Frightened(self.options)
        self.scared = True
        self.image.fill(constants.BLUE)
        self.last_timer_scare = self.timer
        self.set_spritesheet("../res/ghosts/scared")
        self.mode.print_mode(self.name)

    def eaten(self):
        self.mode = mode.Dead(self.options)
        self.mode.print_mode(self.name)

    def is_scared(self):
        return self.scared

    def get_score(self):
        return self.score


class Blinky(Ghost):
    def __init__(self, x, y, width, height, res_path, pacman, *groups):
        super().__init__(x, y, width, height, res_path, pacman, *groups)
        self.target_corner = (416, 64)
        self.mode.set_target_corner(self.target_corner)
        self.color = constants.RED
        self.image.fill(self.color)
        self.name = "Blinky"
        self.options = [constants.UP, constants.RIGHT, constants.DOWN, constants.LEFT]
        self.mode.set_options(self.options)

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
        self.target_corner = (16, 64)
        self.mode.set_target_corner(self.target_corner)
        self.color = constants.PINK
        self.image.fill(self.color)
        self.name = "Pinky"
        self.options = [constants.UP, constants.LEFT, constants.DOWN, constants.RIGHT]
        self.mode.set_options(self.options)

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
        self.target_corner = (416, 464)
        self.mode.set_target_corner(self.target_corner)
        self.color = constants.LIGHT_BLUE
        self.image.fill(self.color)
        self.name = "Inky"
        self.options = [constants.UP, constants.RIGHT, constants.DOWN, constants.LEFT]
        self.mode.set_options(self.options)

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
        self.target_corner = (16, 464)
        self.mode.set_target_corner(self.target_corner)
        self.color = constants.ORANGE
        self.image.fill(self.color)
        self.name = "Clyde"
        self.options = [constants.UP, constants.LEFT, constants.DOWN, constants.RIGHT]
        self.mode.set_options(self.options)

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

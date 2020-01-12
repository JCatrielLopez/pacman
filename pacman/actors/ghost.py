import numpy as np

from pacman.actors.state import State
from . import actor, mode
from .. import constants


class Ghost(actor.MovingActor):
    # TODO agregar comer fantasmas y que vuelvan a la casa - que inicien en la casa

    score = 800
    state = None
    home_door_position = (216, 176)

    def __init__(
            self, x, y, width, height, res_path, pacman, current_map=None, *groups
    ):
        super().__init__(
            x, y, width, height, constants.RED, res_path, current_map, *groups
        )

        self.name = None
        self.resources_path = res_path
        self.pacman = pacman
        self.home_position = (0, 0)

        self.color = constants.RED

    def back(self, current_dir):
        return -current_dir[0], -current_dir[1]

    def die(self):
        if self.get_current_state() != State.DEAD:
            self.state.change_to_dead()
            self.image.fill(constants.GREEN)
            self.set_spritesheet("../res/ghosts/dead")

    def get_state(self):
        return self.state

    def get_current_state(self):
        return self.state.get_state()

    def fright(self):
        if self.get_current_state() != State.DEAD:
            self.image.fill(constants.BLUE)
            self.set_spritesheet("../res/ghosts/scared")

    def restart_sprite(self):
        self.image.fill(self.color)
        self.set_spritesheet(self.resources_path)

    def get_score(self):
        return self.score

    def restart(self):
        super().restart()
        self.state = State(self.options)
        self.state.set_target_corner(self.target_corner)
        self.restart_sprite()

    def tp(self):
        self.rect.x = self.home_position[0]
        self.rect.y = self.home_position[1]
        self.direction = constants.LEFT


class Blinky(Ghost):
    def __init__(self, x, y, width, height, res_path, pacman, *groups):
        super().__init__(x, y, width, height, res_path, pacman, *groups)

        self.color = constants.RED
        self.image.fill(self.color)
        self.name = "Blinky"

        self.target_corner = (416, 64)
        self.home_position = Ghost.home_door_position
        self.options = [constants.UP, constants.RIGHT, constants.DOWN, constants.LEFT]
        self.state = State(self.options)
        self.state.set_target_corner(self.target_corner)

    def move(self):
        self.state.set_target_position(self.pacman.get_pos())
        self.next_dir = self.state.get_next_dir(
            self.get_pos(), self.back(self.direction), self.current_map
        )
        super().move()


class Pinky(Ghost):
    def __init__(self, x, y, width, height, res_path, pacman, *groups):
        super().__init__(x, y, width, height, res_path, pacman, *groups)

        self.color = constants.PINK
        self.image.fill(self.color)
        self.name = "Pinky"

        self.target_corner = (16, 64)
        self.home_position = (216, 224)
        self.options = [constants.UP, constants.LEFT, constants.DOWN, constants.RIGHT]
        self.state = State(self.options)
        self.state.set_target_corner(self.target_corner)

    def move(self):
        # self.check_mode()
        pacman_position = self.pacman.get_pos()
        pacman_direction = self.pacman.get_direction()
        target_position = (
            pacman_position[0] + pacman_direction[0] * constants.TILE_SIZE * 4 + 8,
            pacman_position[1] + pacman_direction[1] * constants.TILE_SIZE * 4 + 8,
        )

        self.state.set_target_position(target_position)
        self.next_dir = self.state.get_next_dir(
            self.get_pos(), self.back(self.direction), self.current_map
        )
        super().move()


class Inky(Ghost):
    def __init__(self, x, y, width, height, res_path, pacman, blinky, *groups):
        super().__init__(x, y, width, height, res_path, pacman, *groups)

        self.color = constants.LIGHT_BLUE
        self.image.fill(self.color)
        self.name = "Inky"
        self.blinky = blinky

        self.target_corner = (416, 464)
        self.home_position = (184, 224)
        self.options = [constants.UP, constants.RIGHT, constants.DOWN, constants.LEFT]
        self.state = State(self.options)
        self.state.set_target_corner(self.target_corner)

    def move(self):
        pacman_position = self.pacman.get_pos()
        pacman_direction = self.pacman.get_direction()
        blinky_position = self.blinky.get_pos()

        aux = (
            pacman_position[0] + pacman_direction[0] * constants.TILE_SIZE * 2,
            pacman_position[1] + pacman_direction[1] * constants.TILE_SIZE * 2
        )

        vector = np.array(blinky_position) - np.array(aux)

        target_position = self.get_pos()
        target_position = (target_position[0] + vector[0] * 2, target_position[1] + vector[1] * 2)

        self.state.set_target_position(target_position)
        self.next_dir = self.state.get_next_dir(
            self.get_pos(), self.back(self.direction), self.current_map
        )

        super().move()


class Clyde(Ghost):
    def __init__(self, x, y, width, height, res_path, pacman, *groups):
        super().__init__(x, y, width, height, res_path, pacman, *groups)

        self.color = constants.ORANGE
        self.image.fill(self.color)
        self.name = "Clyde"

        self.target_corner = (16, 464)
        self.home_position = (248, 224)
        self.options = [constants.UP, constants.LEFT, constants.DOWN, constants.RIGHT]
        self.state = State(self.options)
        self.state.set_target_corner(self.target_corner)

    def move(self):
        # self.check_mode()

        pacman_grid = self.current_map.get_grid(self.pacman.get_pos())
        clyde_grid = self.current_map.get_grid(self.get_pos())

        if self.current_map.get_distance(pacman_grid, clyde_grid) < 8:
            self.state.set_target_position(self.state.get_target_corner())
        else:
            self.state.set_target_position(self.pacman.get_pos())

        self.next_dir = self.state.get_next_dir(
            self.get_pos(), self.back(self.direction), self.current_map
        )
        super().move()

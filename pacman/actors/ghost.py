import numpy as np

from pacman.actors.state import State
from . import actor
from .. import constants


class Ghost(actor.MovingActor):
    # TODO agregar comer fantasmas y que vuelvan a la casa - que inicien en la casa

    score = 800
    state = None
    home_door_position = (216, 176)

    def __init__(
            self, x, y, width, height, spritesheet_path, spritesheet_chase_path, spritesheet_scatter_path, pacman,
            current_map=None, *groups
    ):
        super().__init__(
            x, y, width, height, constants.RED, spritesheet_path, current_map, *groups
        )

        self.name = None
        self.pacman = pacman
        self.home_position = (0, 0)
        self.pellet_counter = 0
        self.pellet_limit = 0
        self.global_pellet_limit = 0
        self.global_pellet_counter = 0
        self.count_pellets = True

        self.color = constants.RED
        self.spritesheet_path = spritesheet_path
        self.spritesheet_chase_path = spritesheet_chase_path
        self.spritesheet_scatter_path = spritesheet_scatter_path
        self.spritesheet_dead_path = "../res/ghosts/State_dead"
        self.spritesheet_frightened_path = "../res/ghosts/State_scared"

    def back(self, current_dir):
        return -current_dir[0], -current_dir[1]

    # def die(self):
    #     if self.get_current_state() != State.DEAD:
    #         self.state.change_to_dead()
    #         self.image.fill(constants.GREEN)
    #         self.set_spritesheet(self.spritesheet_dead_path)

    def get_state(self):
        return self.state

    def get_current_state(self):
        return self.state.get_state()

    def fright(self):
        if self.get_current_state() != State.DEAD:
            self.image.fill(constants.BLUE)
            self.set_spritesheet(self.spritesheet_frightened_path)

    def get_score(self):
        return self.score

    def restart_state(self):
        self.state = State(self.options)
        self.state.set_notify_state_change(self.notify_state_change)
        self.state.set_target_corner(self.target_corner)
        self.notify_state_change()

    def tp(self, new_location):
        self.rect.x = new_location[0]
        self.rect.y = new_location[1]
        self.direction = constants.LEFT

    def move(self):
        if self.get_current_state() == State.DEAD:
            current_position = self.current_map.get_grid(self.get_pos())
            target = self.current_map.get_grid(self.home_door_position)
            distance = self.current_map.get_distance(current_position, target)

            if distance < 2:
                self.tp(self.home_position)
                self.state.register_as_in_home()
                State.change_to_in_home()  # TODO Cambiar esto de lugar
            else:
                super().move()
        elif self.get_current_state() != State.IN_HOME:
            super().move()

    def set_pellet_count(self, amount):
        if self.get_current_state() == State.IN_HOME:
            self.state.add_pellets_counted(amount)

    def get_counter(self):
        return self.state.get_pellets_counted()

    # TODO
    def check_pellet_limits(self):
        if self.count_pellets:
            if self.pellet_counter > self.pellet_limit:
                self.tp(self.home_door_position)
                self.state.change_to_scatter_chase()
        else:
            if self.global_pellet_counter > self.global_pellet_limit:
                self.tp(self.home_door_position)
                self.state.change_to_scatter_chase()

    def die(self):
        if self.get_current_state() != State.DEAD and self.get_current_state() != State.IN_HOME:
            self.state.change_to_dead()
            self.image.fill(constants.GREEN)
            self.set_spritesheet(self.spritesheet_dead_path)

    def notify_state_change(self):

        if self.get_current_state() == State.SCATTER:
            self.set_spritesheet(self.spritesheet_scatter_path)

        elif self.get_current_state() == State.CHASE:
            self.set_spritesheet(self.spritesheet_chase_path)

        elif self.get_current_state() == State.DEAD:
            self.set_spritesheet(self.spritesheet_dead_path)

        elif self.get_current_state() == State.FRIGHTENED:
            self.set_spritesheet(self.spritesheet_frightened_path)

        elif self.state.get_state() == State.IN_HOME:
            self.set_spritesheet(self.spritesheet_path)

    def can_be_fright(self):
        return self.state.can_be_fright()

    def set_state(self, st):
        self.state.update_state(st)
        self.notify_state_change()


class Blinky(Ghost):
    def __init__(self, x, y, width, height, spritesheet_path, spritesheet_chase_path, spritesheet_scatter_path, pacman,
                 *groups):
        super().__init__(x, y, width, height, spritesheet_path, spritesheet_chase_path, spritesheet_scatter_path,
                         pacman, *groups)

        self.color = constants.RED
        self.image.fill(self.color)
        self.name = "Blinky"

        self.target_corner = (416, 64)
        self.home_position = Ghost.home_door_position
        self.options = [constants.UP, constants.RIGHT, constants.DOWN, constants.LEFT]
        self.state = State(self.options)
        self.state.set_target_corner(self.target_corner)
        self.pellet_limit = 0
        self.global_pellet_limit = 0

        self.state.set_notify_state_change(self.notify_state_change)
        self.notify_state_change()

    def move(self):
        self.state.set_target_position(self.pacman.get_pos())
        self.next_dir = self.state.get_next_dir(
            self.get_pos(), self.back(self.direction), self.current_map
        )
        super().move()


class Pinky(Ghost):
    def __init__(self, x, y, width, height, spritesheet_path, spritesheet_chase_path, spritesheet_scatter_path, pacman,
                 *groups):
        super().__init__(x, y, width, height, spritesheet_path, spritesheet_chase_path, spritesheet_scatter_path,
                         pacman, *groups)

        self.color = constants.PINK
        self.image.fill(self.color)
        self.name = "Pinky"

        self.target_corner = (16, 64)
        self.home_position = (216, 224)
        self.options = [constants.UP, constants.LEFT, constants.DOWN, constants.RIGHT]
        self.state = State(self.options)
        self.state.set_target_corner(self.target_corner)
        self.pellet_limit = 0
        self.global_pellet_limit = 7

        self.state.set_notify_state_change(self.notify_state_change)
        self.notify_state_change()

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
    def __init__(self, x, y, width, height, spritesheet_path, spritesheet_chase_path, spritesheet_scatter_path, pacman,
                 blinky, *groups):
        super().__init__(x, y, width, height, spritesheet_path, spritesheet_chase_path, spritesheet_scatter_path,
                         pacman, *groups)

        self.color = constants.LIGHT_BLUE
        self.image.fill(self.color)
        self.name = "Inky"
        self.blinky = blinky

        self.target_corner = (416, 464)
        self.home_position = (184, 224)
        self.options = [constants.UP, constants.RIGHT, constants.DOWN, constants.LEFT]
        self.state = State(self.options)
        self.state.set_target_corner(self.target_corner)
        self.pellet_limit = 30
        self.global_pellet_limit = 17

        self.state.set_notify_state_change(self.notify_state_change)
        self.notify_state_change()

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
    def __init__(self, x, y, width, height, spritesheet_path, spritesheet_chase_path, spritesheet_scatter_path, pacman,
                 *groups):
        super().__init__(x, y, width, height, spritesheet_path, spritesheet_chase_path, spritesheet_scatter_path,
                         pacman, *groups)

        self.color = constants.ORANGE
        self.image.fill(self.color)
        self.name = "Clyde"

        self.target_corner = (16, 464)
        self.home_position = (248, 224)
        self.options = [constants.UP, constants.LEFT, constants.DOWN, constants.RIGHT]
        self.state = State(self.options)
        self.state.set_target_corner(self.target_corner)
        self.pellet_limit = 60
        self.global_pellet_limit = 32

        self.state.set_notify_state_change(self.notify_state_change)
        self.notify_state_change()

    def move(self):

        # print(f"{self.name}:: State: {self.get_current_state()}")
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

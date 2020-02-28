from threading import Lock

import numpy as np

import actor
import constants
from pacman.actors.state import State


# logger = logging.getLogger()


class Ghost(actor.MovingActor):
    score = 800
    state = None
    home_door_position = (216, 176)

    threadLock = Lock()

    def __init__(
            self,
            x=None,
            y=None,
            width=None,
            height=None,
            spritesheet_path=None,
            spritesheet_chase_path=None,
            spritesheet_scatter_path=None,
            current_map=None,
            pacman=None,
            groups=None,
    ):
        super().__init__(
            x, y, width, height, constants.RED, spritesheet_path, current_map, *groups
        )

        self.name = None
        self.pacman = pacman
        # self.home_position = (0, 0)

        self.color = constants.RED
        self.spritesheet_path = spritesheet_path
        self.spritesheet_chase_path = spritesheet_chase_path
        self.spritesheet_scatter_path = spritesheet_scatter_path
        self.spritesheet_dead_path = "../res/ghosts/State_dead"
        self.spritesheet_frightened_path = "../res/ghosts/State_scared"

    def back_direction(self, current_dir):
        return -current_dir[0], -current_dir[1]

    def get_current_state(self):
        return self.state.get_current_state()

    def get_score(self):
        return self.score

    def teleport(self, new_location):
        # logger.debug(f"teleport to {new_location}")
        self.rect.x = new_location[0]
        self.rect.y = new_location[1]
        self.direction = constants.LEFT

        self.state.notify(self)

    def move(self):
        if self.get_current_state() == State.DEAD:
            current_position = self.current_map.get_grid(self.get_pos())
            target = self.current_map.get_grid(self.home_door_position)
            distance = self.current_map.get_distance(current_position, target)

            if distance < 2:
                self.teleport(self.home_position)
            else:
                super().move()
        elif self.get_current_state() != State.IN_HOME:
            super().move()

    def update_spritesheet(self):

        if self.get_current_state() == State.SCATTER:
            self.set_spritesheet(self.spritesheet_scatter_path)

        elif self.get_current_state() == State.CHASE:
            self.set_spritesheet(self.spritesheet_chase_path)

        elif self.get_current_state() == State.DEAD:
            self.set_spritesheet(self.spritesheet_dead_path)

        elif self.get_current_state() == State.FRIGHTENED:
            self.set_spritesheet(self.spritesheet_frightened_path)

        elif self.state.get_current_state() == State.IN_HOME:
            self.set_spritesheet(self.spritesheet_path)

    def can_be_frightened(self):
        return self.state.can_be_frightened()

    def can_be_consumed(self):
        return self.state.can_be_consumed()

    def can_be_ignored(self):
        return self.state.can_be_ignored()

    def set_state(self, st):
        self.threadLock.acquire(blocking=True)
        # logger.debug(f"{self.name} -> set_state({st})")
        if self.state.current_state == State.IN_HOME:
            self.teleport(self.home_door_position)

        self.state.update_state(st)
        self.update_spritesheet()
        self.threadLock.release()


class Blinky(Ghost):
    def __init__(
            self,
            width=None,
            height=None,
            spritesheet_path=None,
            spritesheet_chase_path=None,
            spritesheet_scatter_path=None,
            notify_in_home=None,
            pacman=None,
            map=None,
            groups=None,
    ):
        self.home_position = Ghost.home_door_position
        super().__init__(
            x=self.home_position[0],
            y=self.home_position[1],
            width=width,
            height=height,
            spritesheet_path=spritesheet_path,
            spritesheet_chase_path=spritesheet_chase_path,
            spritesheet_scatter_path=spritesheet_scatter_path,
            current_map=map,
            pacman=pacman,
            groups=groups,
        )

        self.color = constants.RED
        self.image.fill(self.color)
        self.name = "Blinky"

        self.target_corner = (416, 64)
        self.options = [constants.UP, constants.RIGHT, constants.DOWN, constants.LEFT]
        self.state = State(self.options)
        self.state.set_target_corner(self.target_corner)
        self.state.set_notify_teleport(notify_in_home)

        self.set_state(State.SCATTER)
        self.pellet_limit = 0
        self.global_pellet_limit = 0

        self.priority = 0

        self.update_spritesheet()

    def move(self):
        self.state.set_target_position(self.pacman.get_pos())
        self.next_dir = self.state.get_next_dir(
            self.get_pos(), self.back_direction(self.direction), self.current_map
        )
        super().move()


class Pinky(Ghost):
    def __init__(
            self,
            width=None,
            height=None,
            spritesheet_path=None,
            spritesheet_chase_path=None,
            spritesheet_scatter_path=None,
            notify_in_home=None,
            pacman=None,
            map=None,
            groups=None,
    ):
        self.home_position = (216, 224)
        super().__init__(
            x=self.home_position[0],
            y=self.home_position[1],
            width=width,
            height=height,
            spritesheet_path=spritesheet_path,
            spritesheet_chase_path=spritesheet_chase_path,
            spritesheet_scatter_path=spritesheet_scatter_path,
            current_map=map,
            pacman=pacman,
            groups=groups,
        )

        self.color = constants.PINK
        self.image.fill(self.color)
        self.name = "Pinky"

        self.target_corner = (16, 64)
        self.options = [constants.UP, constants.LEFT, constants.DOWN, constants.RIGHT]
        self.state = State(self.options)
        self.state.set_target_corner(self.target_corner)
        self.state.set_notify_teleport(notify_in_home)
        self.pellet_limit = 0
        self.global_pellet_limit = 7

        self.priority = 1

        # self.state.set_notify_state_change(self.change_spritesheet)
        self.update_spritesheet()

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
            self.get_pos(), self.back_direction(self.direction), self.current_map
        )
        super().move()


class Inky(Ghost):
    def __init__(
            self,
            width=None,
            height=None,
            spritesheet_path=None,
            spritesheet_chase_path=None,
            spritesheet_scatter_path=None,
            notify_in_home=None,
            pacman=None,
            blinky=None,
            map=None,
            groups=None,
    ):
        self.home_position = (184, 224)
        super().__init__(
            x=self.home_position[0],
            y=self.home_position[1],
            width=width,
            height=height,
            spritesheet_path=spritesheet_path,
            spritesheet_chase_path=spritesheet_chase_path,
            spritesheet_scatter_path=spritesheet_scatter_path,
            current_map=map,
            pacman=pacman,
            groups=groups,
        )

        self.color = constants.LIGHT_BLUE
        self.image.fill(self.color)
        self.name = "Inky"
        self.blinky = blinky

        self.target_corner = (416, 464)
        self.options = [constants.UP, constants.RIGHT, constants.DOWN, constants.LEFT]
        self.state = State(self.options)
        self.state.set_target_corner(self.target_corner)
        self.state.set_notify_teleport(notify_in_home)
        self.pellet_limit = 30
        self.global_pellet_limit = 17

        self.priority = 2

        # self.state.set_notify_state_change(self.change_spritesheet)
        self.update_spritesheet()

    def move(self):
        pacman_position = self.pacman.get_pos()
        pacman_direction = self.pacman.get_direction()
        blinky_position = self.blinky.get_pos()

        aux = (
            pacman_position[0] + pacman_direction[0] * constants.TILE_SIZE * 2,
            pacman_position[1] + pacman_direction[1] * constants.TILE_SIZE * 2,
        )

        vector = np.array(blinky_position) - np.array(aux)

        target_position = self.get_pos()
        target_position = (
            target_position[0] + vector[0] * 2,
            target_position[1] + vector[1] * 2,
        )

        self.state.set_target_position(target_position)
        self.next_dir = self.state.get_next_dir(
            self.get_pos(), self.back_direction(self.direction), self.current_map
        )

        super().move()


class Clyde(Ghost):
    def __init__(
            self,
            width=None,
            height=None,
            spritesheet_path=None,
            spritesheet_chase_path=None,
            spritesheet_scatter_path=None,
            notify_in_home=None,
            pacman=None,
            map=None,
            groups=None,
    ):
        self.home_position = (248, 224)
        super().__init__(
            x=self.home_position[0],
            y=self.home_position[1],
            width=width,
            height=height,
            spritesheet_path=spritesheet_path,
            spritesheet_chase_path=spritesheet_chase_path,
            spritesheet_scatter_path=spritesheet_scatter_path,
            current_map=map,
            pacman=pacman,
            groups=groups,
        )
        self.color = constants.ORANGE
        self.image.fill(self.color)
        self.name = "Clyde"

        self.target_corner = (16, 464)
        self.options = [constants.UP, constants.LEFT, constants.DOWN, constants.RIGHT]
        self.state = State(self.options)
        self.state.set_target_corner(self.target_corner)
        self.state.set_notify_teleport(notify_in_home)
        self.pellet_limit = 60
        self.global_pellet_limit = 32

        self.priority = 3

        # self.state.set_notify_state_change(self.change_spritesheet)
        self.update_spritesheet()

    def move(self):
        pacman_grid = self.current_map.get_grid(self.pacman.get_pos())
        clyde_grid = self.current_map.get_grid(self.get_pos())

        if self.current_map.get_distance(pacman_grid, clyde_grid) < 8:
            self.state.set_target_position(self.state.get_target_corner())
        else:
            self.state.set_target_position(self.pacman.get_pos())

        self.next_dir = self.state.get_next_dir(
            self.get_pos(), self.back_direction(self.direction), self.current_map
        )
        super().move()

import random

from pacman import constants
from pacman.my_timer import MyTimer


class State:
    SCATTER = 0
    CHASE = 1
    FRIGHTENED = 2
    DEAD = 3

    frightened_register = []

    current_state = None
    dual_state = None
    dual_timer: MyTimer = None

    frightened_timer: MyTimer = None
    frightened_timeout = 6

    scatter_time_list = [7.0, 7.0, 5.0, 5.0]
    chase_time_list = [20.0, 20.0, 20.0, 20.0]
    dual_time_index = 0

    next_dir_function = None

    target_corner = None
    target_position = None
    options = [constants.UP, constants.LEFT, constants.DOWN, constants.RIGHT]

    def __init__(self, options):

        self.current_state = State.SCATTER
        self.next_dir_function = self.get_next_dir_scatter_chase
        self.target_corner = (0, 0)
        self.target_position = (0, 0)
        if options is not None:
            self.options = options

        State.dual_state = State.SCATTER
        State.dual_timer = MyTimer(State.scatter_time_list[State.dual_time_index], State.switch_scatter_chase)
        State.dual_timer.start()

    def set_target_corner(self, target_corner):
        self.target_corner = target_corner

    def set_target_position(self, target_position):
        self.target_position = target_position

    @staticmethod
    def switch_scatter_chase(self):
        if State.dual_state == State.SCATTER:
            State.dual_state = State.CHASE
        else:
            if State.dual_time_index <= 3:
                State.dual_state = State.SCATTER
                State.dual_time_index += 1

        State.dual_timer = MyTimer(State.scatter_time_list[State.dual_time_index], self.switch_scatter_chase)
        State.dual_timer.start()

    def register_as_frightened(self):
        if self.current_state != State.DEAD:
            State.frightened_register.append(self)

    @staticmethod
    def change_to_fright():
        State.dual_timer.pause()
        for state in State.frightened_register:
            state.current_state = State.FRIGHTENED
            state.next_dir_function = state.get_next_dir_frightened
        State.frightened_timer = MyTimer(State.frightened_timeout, State.end_of_fright_timeout)

    @staticmethod
    def end_of_fright_timeout(self):
        State.dual_timer.resume()
        for state in State.frightened_register:
            state.current_state = State.dual_state
            state.next_dir_function = state.get_next_dir_scatter_chase

    def change_to_dead(self):
        if self.current_state == State.FRIGHTENED:
            State.frightened_register.remove(self)
            self.current_state = State.DEAD
            self.next_dir_function = self.get_next_dir_dead

    def get_state(self):
        return self.current_state

    def get_next_dir(self, current_position, back, map):
        return self.next_dir_function(current_position, back, map)

    def get_next_dir_scatter_chase(self, current_position, back, map):
        current_grid = map.get_grid(current_position)
        new_dir = None
        min_distance = 10000

        target = self.target_corner
        if self.current_state == State.CHASE:
            target = self.target_position

        for opt in self.options:
            new_position = (current_grid[0] + opt[0], current_grid[1] + opt[1])
            if map.is_valid(new_position) or map.get_value(new_position) == 4:
                new_distance = map.get_distance(
                    new_position, map.get_grid(target)
                )
                if new_distance < min_distance and opt != back:
                    min_distance = new_distance
                    new_dir = opt

        return new_dir

    def get_next_dir_frightened(self, current_position, back, map):
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

    def get_next_dir_dead(self, current_position, back, map):
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

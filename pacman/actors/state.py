import random

from pacman import constants
from pacman.my_timer import MyTimer


class State:
    # TODO hacer la integracion de todo esto
    # TODO posible nuevo estado del los fantasmas adentro de la casa

    SCATTER = 0
    CHASE = 1
    FRIGHTENED = 2
    DEAD = 3
    IN_HOME = 4

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

    notify_dual_state_change = None
    notify_out_of_frightened = None

    def __init__(self, options):

        self.current_state = State.SCATTER
        self.next_dir_function = self.get_next_dir_scatter_chase
        self.target_corner = (0, 0)
        self.target_position = (0, 0)
        if options is not None:
            self.options = options

        if State.dual_state is None:
            State.dual_state = State.SCATTER
            State.dual_timer = MyTimer(State.scatter_time_list[State.dual_time_index], State.switch_scatter_chase)
            State.dual_timer.start()

    @staticmethod
    def restart():
        State.dual_state = State.SCATTER
        State.dual_timer.cancel()
        State.dual_time_index = 0
        State.dual_timer = MyTimer(State.scatter_time_list[State.dual_time_index], State.switch_scatter_chase)
        State.dual_timer.start()

    def set_target_corner(self, target_corner):
        self.target_corner = target_corner

    def get_target_corner(self):
        return self.target_corner

    def set_target_position(self, target_position):
        self.target_position = target_position

    @staticmethod
    def set_notify_dual_state_change(notify_dual_state_change):
        State.notify_dual_state_change = notify_dual_state_change

    @staticmethod
    def set_notify_out_of_frightened(notify_out_of_frightened):
        State.notify_out_of_frightened = notify_out_of_frightened

    @staticmethod
    def switch_scatter_chase():
        # print("switch_scatter_chase: STATE: ", State.dual_state)
        if State.dual_state == State.SCATTER:
            State.dual_state = State.CHASE
            State.dual_timer.cancel()
            State.dual_timer.set_timeout(State.chase_time_list[State.dual_time_index])
            State.dual_timer = MyTimer(State.chase_time_list[State.dual_time_index], State.switch_scatter_chase)
        else:
            if State.dual_time_index <= 3:
                State.dual_state = State.SCATTER
                State.dual_time_index += 1
            State.dual_timer.cancel()
            State.dual_timer.set_timeout(State.scatter_time_list[State.dual_time_index])
            State.dual_timer = MyTimer(State.scatter_time_list[State.dual_time_index], State.switch_scatter_chase)

        State.notify_dual_state_change()
        State.dual_timer.start()

    def register_as_frightened(self):
        if self.current_state != State.DEAD:
            if self not in State.frightened_register:
                State.frightened_register.append(self)

    @staticmethod
    def change_to_fright():

        if not State.dual_timer.is_on_pause():
            State.dual_timer.pause()
            for state in State.frightened_register:
                state.current_state = State.FRIGHTENED
                state.next_dir_function = state.get_next_dir_frightened
            State.frightened_timer = MyTimer(State.frightened_timeout, State.end_of_fright_timeout)
            State.frightened_timer.start()

    @staticmethod
    def end_of_fright_timeout():
        State.frightened_timer.cancel()
        State.dual_timer.resume()
        for state in State.frightened_register:
            state.change_to_scatter_chase()

        State.frightened_register.clear()
        State.notify_out_of_frightened()

    def change_to_scatter_chase(self):
        self.current_state = State.dual_state
        self.next_dir_function = self.get_next_dir_scatter_chase

    def change_to_dead(self):
        if self.current_state == State.FRIGHTENED:
            State.frightened_register.remove(self)
            self.current_state = State.DEAD
            self.next_dir_function = self.get_next_dir_dead

    def change_to_home(self):
        if self.current_state == State.DEAD:
            self.current_state = State.IN_HOME

    def get_state(self):
        return self.current_state

    def get_next_dir(self, current_position, back, map):
        return self.next_dir_function(current_position, back, map)

    def get_next_dir_scatter_chase(self, current_position, back, map):
        current_grid = map.get_grid(current_position)
        new_dir = None
        min_distance = 10000

        if self.current_state == State.CHASE:
            target = self.target_position
        else:
            target = self.target_corner

        for opt in self.options:
            new_position = (current_grid[0] + opt[0], current_grid[1] + opt[1])
            if map.is_valid(new_position):
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

        target = (224, 224)  # Posicion en la casa

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

    def back(self, current_dir):
        return -current_dir[0], -current_dir[1]

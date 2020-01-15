import random

from pacman import constants


class State:
    # TODO hacer la integracion de todo esto
    # TODO posible nuevo estado del los fantasmas adentro de la casa

    SCATTER = 0
    CHASE = 1
    FRIGHTENED = 2
    DEAD = 3
    IN_HOME = 4

    next_dir_function = None

    target_corner = None
    target_position = None
    options = [constants.UP, constants.LEFT, constants.DOWN, constants.RIGHT]

    def __init__(self, options):

        self.current_state = State.IN_HOME
        self.next_dir_function = self.get_next_dir_scatter_chase
        self.target_corner = (0, 0)
        self.target_position = (0, 0)
        self.count_pellets = True
        self.pellets_counted = 0

        self.notify_teleport = None

        if options is not None:
            self.options = options

    def set_count_pellets(self, value):
        self.count_pellets = value

    def set_target_position(self, target_position):
        self.target_position = target_position

    def set_target_corner(self, target_corner):
        self.target_corner = target_corner

    def get_pellets_counted(self):
        return self.pellets_counted

    def get_target_corner(self):
        return self.target_corner

    def get_current_state(self):
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
                new_distance = map.get_distance(new_position, map.get_grid(target))
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

        if valid_options:
            opt = random.choice(valid_options)
            return opt
        else:
            return None

    def back(self, current_dir):
        return -current_dir[0], -current_dir[1]

    def get_next_dir_dead(self, current_position, back, map):
        current_grid = map.get_grid(current_position)
        new_dir = None
        min_distance = 10000

        target = (224, 224)  # Posicion en la casa

        for opt in self.options:
            new_position = (current_grid[0] + opt[0], current_grid[1] + opt[1])
            if map.is_valid(new_position) or map.get_value(new_position) == 4:
                new_distance = map.get_distance(new_position, map.get_grid(target))
                if new_distance < min_distance and opt != back:
                    min_distance = new_distance
                    new_dir = opt

        return new_dir

    def get_next_dir_in_home(self, current_position, back, map):
        return None

    def add_pellets_counted(self, amount):
        self.pellets_counted += amount

    def can_be_frightened(self):
        return not (
                self.current_state == State.DEAD or self.current_state == State.IN_HOME
        )

    def can_be_consumed(self):
        return self.current_state == State.FRIGHTENED

    def can_be_ignored(self):
        return self.current_state == State.DEAD or self.current_state == State.IN_HOME

    def update_state(self, st):
        self.current_state = st
        self.update_next_dir_function()

    def update_next_dir_function(self):
        if self.current_state == State.SCATTER:
            self.next_dir_function = self.get_next_dir_scatter_chase

        if self.current_state == State.CHASE:
            self.next_dir_function = self.get_next_dir_scatter_chase

        if self.current_state == State.DEAD:
            self.next_dir_function = self.get_next_dir_dead

        if self.current_state == State.FRIGHTENED:
            self.next_dir_function = self.get_next_dir_frightened

        if self.current_state == State.IN_HOME:
            self.next_dir_function = self.get_next_dir_in_home

    def set_notify_teleport(self, function):
        self.notify_teleport = function

    def notify(self, ghost):
        self.notify_teleport(ghost)

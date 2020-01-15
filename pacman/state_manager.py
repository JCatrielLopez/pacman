from pacman.actors.state import State
from pacman.my_timer import MyTimer


# TODO Si necesitan saber donde se llamo una funcion, pongan este pedazo de codigo en esa funcion:
# print("---------------------------------------------------------------------------------------------------------")
# import traceback
# for line in traceback.format_stack():
#     print(line.strip())
# print("---------------------------------------------------------------------------------------------------------")

class StateManager:
    BLINKY_INDEX = 0
    PINKY_INDEX = 1
    INKY_INDEX = 2
    CLYDE_INDEX = 3

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(StateManager, cls).__new__(cls)
        return cls.instance

    def __init__(self):

        self.ghosts = None

        self.scatter_time_list = [7.0, 7.0, 5.0, 5.0]
        self.chase_time_list = [20.0, 20.0, 20.0, 20.0]
        self.dual_time_index = 0

        self.dual_state = State.SCATTER
        self.dual_timer = MyTimer(
            self.scatter_time_list[self.dual_time_index], self.switch_scatter_chase
        )
        self.dual_timer.start()

        self.frightened_timer: MyTimer = None
        self.frightened_timeout = 6
        self.notify_pacman = None
        self.notify_pacman_arg = None

        # Blinky, Pinky, Inky, Clyde
        self.pellet_ghost_counter_values = [0, 0, 0, 0]
        self.pellet_ghost_counter_limits = [0, 0, 30, 60]
        self.pellet_ghost_counter = True

        self.pellet_global_counter_value = 0
        self.pellet_global_counter_limits = [0, 0, 17, 32]
        self.pellet_global_counter = False

        self.last_pellet_timeout = 4
        self.last_pellet_timer = MyTimer(
            self.last_pellet_timeout, self.resurrect_by_timer
        )

    def set_ghosts(self, ghosts):
        # Los arreglos en Python no tienen un orden asegurado, asi que la ordeno cuando la seteo por prioridad.
        # Blinky: 0 Pinky: 1 Inky: 2 Clyde: 3
        self.ghosts = ghosts
        self.ghosts.sort(key=lambda x: x.priority)

    def switch_scatter_chase(self):
        if self.dual_state == State.SCATTER:
            self.dual_state = State.CHASE
            self.dual_timer.cancel()
            self.dual_timer.set_timeout(self.chase_time_list[self.dual_time_index])
            self.dual_timer = MyTimer(
                self.chase_time_list[self.dual_time_index], self.switch_scatter_chase
            )
        else:
            if self.dual_time_index <= 3:
                self.dual_state = State.SCATTER
                self.dual_time_index += 1
            self.dual_timer.cancel()
            self.dual_timer.set_timeout(self.scatter_time_list[self.dual_time_index])
            self.dual_timer = MyTimer(
                self.scatter_time_list[self.dual_time_index], self.switch_scatter_chase
            )

        for ghost in self.ghosts:
            if not ghost.can_be_ignored():
                ghost.set_state(self.dual_state)
        self.dual_timer.start()

    def change_to_frightened(self):
        if not self.dual_timer.is_on_pause():
            self.dual_timer.pause()
            for ghost in self.ghosts:
                if ghost.can_be_frightened():
                    ghost.set_state(State.FRIGHTENED)

            self.frightened_timer = MyTimer(
                self.frightened_timeout, self.end_of_fright_timeout
            )
            self.frightened_timer.start()

    def end_of_fright_timeout(self):
        self.frightened_timer.cancel()
        self.dual_timer.resume()
        for ghost in self.ghosts:
            if ghost.get_current_state() == State.FRIGHTENED:
                ghost.set_state(self.dual_state)
        self.notify_pacman(self.notify_pacman_arg)

    def change_to_dead(self, ghost):
        if ghost.get_current_state() == State.FRIGHTENED:
            ghost.set_state(State.DEAD)

    def change_to_in_home(self, ghost):
        if ghost.get_current_state() == State.DEAD:
            ghost.set_state(State.IN_HOME)

            if self.last_pellet_timer.is_on_pause():
                self.last_pellet_timer.start()

    def resurrect_by_timer(self):
        for index in range(0, len(self.ghosts)):
            if self.ghosts[index].get_current_state() == State.IN_HOME:
                self.ghosts[index].set_state(self.dual_state)
                return True

        self.last_pellet_timer.cancel()
        return False

    def resurrect_by_limit(self, index):
        if self.ghosts[index].get_current_state() == State.IN_HOME:
            if (
                    self.pellet_ghost_counter_values[index]
                    >= self.pellet_ghost_counter_limits[index]
            ):
                self.ghosts[index].set_state(self.dual_state)
                return True
        return False

    def resurrect_by_global_limit(self):
        for index in range(0, len(self.ghosts)):
            if self.ghosts[index].get_current_state() == State.IN_HOME:
                if (
                        index == 3
                        and self.pellet_ghost_counter_values[index]
                        == self.pellet_global_counter_limits[index]
                ):
                    self.set_global_counter(False)
                    return False
                elif (
                        self.pellet_ghost_counter_values[index]
                        == self.pellet_global_counter_limits[index]
                ):
                    self.ghosts[index].set_state(self.dual_state)
                    return True

        self.last_pellet_timer.cancel()
        return False

    def set_global_counter(self, value):
        self.pellet_global_counter = value

    # TODO Hacer esto bien! El pacman tiene que saber cuando se termina el frightened.
    def set_notify_pacman(self, function, argument):
        self.notify_pacman = function
        self.notify_pacman_arg = argument

    def activate_time_limit(self):
        self.last_pellet_timer.start()

    def update_pellet_counter_values(self, amount):
        if self.pellet_ghost_counter:

            for index in range(0, len(self.ghosts)):
                if self.ghosts[index].get_current_state() == State.IN_HOME:
                    self.pellet_ghost_counter_values[index] += amount
                    self.resurrect_by_limit(index)
                    return True
        return False

    def update_pellet_global_counter(self, amount):
        if self.pellet_global_counter:
            self.pellet_global_counter_value += amount
            self.resurrect_by_global_limit()

    def check_collision(self, ghost_collided):
        for ghost in ghost_collided:
            if ghost.get_current_state() == State.FRIGHTENED:
                ghost.set_state(State.DEAD)

    def restart(self):
        self.dual_state = State.SCATTER
        self.dual_timer.cancel()
        self.dual_time_index = 0
        self.dual_timer = MyTimer(
            self.scatter_time_list[self.dual_time_index], self.switch_scatter_chase
        )
        self.dual_timer.start()
        for ghost in self.ghosts:
            ghost.set_state(self.dual_state)

    def terminate(self):
        if self.frightened_timer is not None:
            self.frightened_timer.cancel()
        if self.dual_timer is not None:
            self.dual_timer.cancel()
        if self.last_pellet_timer is not None:
            self.last_pellet_timer.cancel()

    def get_global_counter_value(self):
        return self.pellet_global_counter_value

    def get_pellet_counter_value(self):
        return str(self.pellet_ghost_counter_values)
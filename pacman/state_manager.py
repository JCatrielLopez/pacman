from pacman.actors.state import State
from pacman.my_timer import MyTimer


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
        self.dual_timer = MyTimer(State.scatter_time_list[State.dual_time_index], State.switch_scatter_chase)
        self.dual_timer.start()

        self.frightened_timer: MyTimer = None
        self.frightened_timeout = 6

        # Blinky, Pinky, Inky, Clyde
        self.pellet_counter = [0, 0, 0, 0]
        self.pellet_limits = [0, 0, 30, 60]

        self.last_pellet_timeout = 4
        self.last_pellet_timer = MyTimer(self.last_pellet_timeout, self.resurrect_by_timer)

    def set_ghost(self, ghosts):
        self.ghosts = ghosts

    def switch_scatter_chase(self):
        if self.dual_state == State.SCATTER:
            self.dual_state = State.CHASE
            self.dual_timer.cancel()
            self.dual_timer.set_timeout(self.chase_time_list[self.dual_time_index])
            self.dual_timer = MyTimer(self.chase_time_list[self.dual_time_index], self.switch_scatter_chase)
        else:
            if self.dual_time_index <= 3:
                self.dual_state = State.SCATTER
                self.dual_time_index += 1
            self.dual_timer.cancel()
            self.dual_timer.set_timeout(self.scatter_time_list[self.dual_time_index])
            self.dual_timer = MyTimer(self.scatter_time_list[self.dual_time_index], self.switch_scatter_chase)

        # TODO Esto va a ser necesario????
        # self.notify_dual_state_change()
        self.dual_timer.start()

    def change_to_fright(self):
        if not self.dual_timer.is_on_pause():
            self.dual_timer.pause()
            for ghost in self.ghosts:
                if ghost.can_be_fright():
                    ghost.set_state(State.FRIGHTENED)

            self.frightened_timer = MyTimer(self.frightened_timeout, self.end_of_fright_timeout)
            self.frightened_timer.start()

    def end_of_fright_timeout(self):
        self.frightened_timer.cancel()
        self.dual_timer.resume()
        for ghost in self.ghosts:
            if ghost.get_current_state() == State.FRIGHTENED:
                ghost.set_state(self.dual_state)

    def change_to_dead(self, ghost):
        if ghost.get_current_state() == State.FRIGHTENED:
            ghost.set_state(State.DEAD)

    def change_to_in_home(self, ghost):
        if ghost.get_current_state() == State.DEAD:
            ghost.set_state(State.IN_HOME)

            if self.last_pellet_timer.is_on_pause():
                self.last_pellet_timer.start()

    # TODO Revisar: Es pause() o cancel()?
    def resurrect_by_timer(self):
        for index in range(0, len(self.ghosts)):
            if self.ghosts[index].get_current_state() == State.IN_HOME:
                self.ghosts[index].set_state(self.dual_state)
                return

        self.last_pellet_timer.pause()

    def resurrect_by_limit(self):
        for index in range(0, len(self.ghosts)):
            if self.ghosts[index].get_current_state() == State.IN_HOME:
                if self.pellet_counter[index] >= self.pellet_limits[index]:
                    self.ghosts[index].set_state(self.dual_state)
                    return

    def restart(self):
        self.dual_state = State.SCATTER
        self.dual_timer.cancel()
        self.dual_time_index = 0
        self.dual_timer = MyTimer(State.scatter_time_list[self.dual_time_index], self.switch_scatter_chase)
        self.dual_timer.start()

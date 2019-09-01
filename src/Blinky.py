from src.Character import Character
from src.Observer import Observer


class Blinky(Character, Observer):
    def __init__(self, pos_x, pos_y, resources_path, speed):
        self.character = super()
        self.character.__init__(pos_x, pos_y, resources_path, speed)

        Observer.__init__(self)
        self.limit_x = 485
        self.limit_y = 485

    def next_position(self, value):
        # print(f"Pacman se movio a: {value}")
        pass

    def move(self):

        pos = self.character.get_pos()
        if pos[0] >= self.limit_x:
            self.character.move_left()
        elif pos[0] < 15:
            self.character.move_right()

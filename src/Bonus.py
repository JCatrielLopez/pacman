import src.Spritesheet
from src.Observer import Observer


class Bonus(Observer):
    def __init__(self, pos_x, pos_y, resources_path, value):
        self.pos = (pos_x, pos_y)
        self._value = value

        Observer.__init__(self)
        self.sp = src.Spritesheet.Spritesheet(f"{resources_path}/fruit 1.gif")

    def add(self, condition):
        if condition:
            print("Pacman obtuvo un bonus!")

    def get_sprite(self):
        return self.sp.image_at((0, 0, 16, 16))

    def get_pos(self):
        return self.pos

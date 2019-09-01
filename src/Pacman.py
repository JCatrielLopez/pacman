from src.Character import Character


class Pacman(Character):
    def __init__(self, pos_x, pos_y, resources_path, speed):
        super().__init__(pos_x, pos_y, resources_path, speed)

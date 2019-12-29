from . import actor
from .. import constants


class Pacman(actor.MovingActor):
    direction = constants.LEFT
    next_dir = None
    lives = 3
    score = 0
    current_map = None
    pellets_consumed = 0

    sprites_left = None
    sprites_right = None
    sprites_up = None
    sprites_down = None
    current_sprite = 0

    def __init__(self, x, y, width, height, current_map=None, *groups):
        super().__init__(
            x, y, width, height, constants.YELLOW, "../res/pacman", current_map, *groups
        )

    def check_consumed(self, pellet_list):
        energizer_consumed = False
        colliding = [i for i in pellet_list.sprites() if self.rect.colliderect(i)]

        score = 0
        if len(colliding):
            for i in colliding:
                if i.is_energizer():
                    energizer_consumed = True
                score += i.get_score()
                pellet_list.remove(i)

        self.pellets_consumed += len(colliding)
        return score, pellet_list, energizer_consumed

    def add_score(self, score):
        self.score += score

    def get_score(self):
        return self.score

    def get_lives(self):
        return self.lives

    def check_collision(self, hitboxes):
        hits = []
        collided = False
        for hitbox in hitboxes:
            if self.rect.colliderect(hitbox):
                collided = True
                hits.append(hitbox)

        return collided, hits

    def get_consumed_amount(self):
        return self.pellets_consumed

    def set_lives(self, param):
        self.lives = param

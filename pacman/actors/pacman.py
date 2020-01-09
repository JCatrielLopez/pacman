from . import actor
from .. import constants


class Pacman(actor.MovingActor):
    direction = constants.LEFT
    next_dir = None
    lives = 3
    score = 0
    current_map = None
    pellets_consumed = 0
    power_up = False

    sprites_left = None
    sprites_right = None
    sprites_up = None
    sprites_down = None
    current_sprite = 0

    # Updates
    notify_scores = None
    notify_lives = None
    notify_pellets_in_map_change = None

    def __init__(self, x, y, width, height, current_map, notify_scores, notify_lives, notify_pellets_in_map_change,
                 *groups):
        super().__init__(
            x, y, width, height, constants.YELLOW, "../res/pacman", current_map, *groups
        )
        self.notify_scores = notify_scores
        self.notify_lives = notify_lives
        self.notify_pellets_in_map_change = notify_pellets_in_map_change

    def check_collision_pellets(self, pellet_list):
        colliding = [i for i in pellet_list.sprites() if self.rect.colliderect(i)]
        score = 0
        if len(colliding):
            for i in colliding:
                if i.is_energizer():
                    self.power_up = True
                score += i.get_score()
                pellet_list.remove(i)

            self.pellets_consumed += len(colliding)
            self.add_score(score)
            self.notify_pellets_in_map_change(pellet_list)

    def check_collision_ghosts(self, ghosts_hitboxes):
        hits = []
        collided = False
        for hitbox in ghosts_hitboxes:
            if self.rect.colliderect(hitbox):
                collided = True
                hits.append(hitbox)

        return collided, hits

    def add_score(self, score):
        self.score += score
        self.notify_scores()

    def get_score(self):
        return self.score

    def decrement_lives(self):
        self.lives -= 1
        self.notify_lives()

    def get_lives(self):
        return self.lives

    def get_consumed_amount(self):
        return self.pellets_consumed

    def set_lives(self, param):
        self.lives = param

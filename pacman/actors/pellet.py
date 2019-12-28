import pygame as pg

from . import actor
from .. import constants
from .. import spritesheet


class Pellet(actor.Actor):
    energizer = None
    sprite = None
    score = None

    def __init__(self, x, y, width, height, energizer, index, *groups):
        self.energizer = energizer

        sp_pellets = spritesheet.Spritesheet(
            "/home/catriel/PycharmProjects/pac-man/res/map/Dots.png"
        )

        if self.energizer:
            super().__init__(x, y, width, height, constants.WHITE, *groups)
            self.sprite = sp_pellets.image_at(
                pg.Rect(0, index * constants.TILE_SIZE, constants.TILE_SIZE, constants.TILE_SIZE)
            )
            self.score = 10
        else:
            super().__init__(x, y, width, height, constants.LIGHT_GRAY, *groups)
            self.sprite = sp_pellets.image_at(
                pg.Rect(constants.TILE_SIZE, index * constants.TILE_SIZE, constants.TILE_SIZE, constants.TILE_SIZE)
            )
            self.score = 30

    def get_sprite(self):
        return self.sprite

    def get_score(self):
        return self.score

    def get_pos(self):
        return self.rect.x, self.rect.y

    def is_energizer(self):
        return self.energizer

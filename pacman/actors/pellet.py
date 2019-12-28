import configparser

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

        config = configparser.ConfigParser()
        config.read("../settings.conf")
        tile_size = config.getint("GAME", "tile_size")

        if self.energizer:
            super().__init__(x, y, width, height, constants.WHITE, *groups)
            self.sprite = sp_pellets.image_at(
                pg.Rect(0, index * tile_size, tile_size, tile_size)
            )
            self.score = 10
        else:
            super().__init__(x, y, width, height, constants.LIGHT_GRAY, *groups)
            self.sprite = sp_pellets.image_at(
                pg.Rect(tile_size, index * tile_size, tile_size, tile_size)
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

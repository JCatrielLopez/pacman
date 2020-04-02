import pygame as pg

from . import actor
from .. import constants


class Wall(actor.Actor):
    def __init__(self, x, y, width, height, *groups):
        super().__init__(x, y, width, height, constants.DARK_GRAY, *groups)

    def get_pos(self):
        return self.rect.x, self.rect.y

    def get_sprite(self):
        return pg.Surface((0, 0))

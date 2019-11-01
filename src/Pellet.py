import pygame as pg

from src import Colors


class Pellet(pg.sprite.Sprite):

    def __init__(self, x, y, tilesize, is_energizer, sprites):
        super().__init__()

        self.tilesize = tilesize
        self.is_energizer = is_energizer
        self.sprites = sprites
        self.image = pg.Surface([tilesize, tilesize])
        if is_energizer:
            self.image.fill(Colors.WHITE)
        else:
            self.image.fill(Colors.LIGHT_GRAY)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def get_sprite(self):
        if self.is_energizer:
            return self.sprites[0]
        return self.sprites[1]

    def get_sprite_pos(self):
        return self.rect.x, self.rect.y

    def score(self):
        if self.is_energizer:
            return 50
        else:
            return 10

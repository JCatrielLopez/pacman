import pygame as pg

from . import constants


class Display:
    # PEP8: https://www.python.org/dev/peps/pep-0008/#constants
    surface = None
    bg_color = None
    bg_image = None
    hide_sprites = False
    show_values = False
    full_screen = False
    font = None
    groups = None

    def __init__(self, size):
        self.surface = pg.display.set_mode(size)

        self.bg_color = constants.BLACK

        pg.font.init()
        self.font = pg.font.SysFont("default", 20, bold=False)

        self.static_sprites = []
        self.moving_sprites = []

    def __str__(self):
        return repr(self) + f" {self.surface.get_size()}"

    def __new__(cls, size):
        if not hasattr(cls, "instance"):
            cls.instance = super(Display, cls).__new__(cls)
        return cls.instance

    def add_static_sprites(self, group):
        if isinstance(group, pg.sprite.Group):
            return self.static_sprites.append(group)

    def add_moving_sprites(self, group):
        if isinstance(group, pg.sprite.Group):
            return self.moving_sprites.append(group)

    def set_background(self, image_path):
        self.bg_image = pg.image.load(image_path)

    def draw(self):
        self.surface.fill(constants.BLACK)

        if self.hide_sprites:
            for group in self.static_sprites:
                group.draw(self.surface)
            for group in self.moving_sprites:
                group.draw(self.surface)
        else:
            self.surface.blit(self.bg_image, (0, 0))
            for group in self.moving_sprites:
                for sprite in group:
                    self.surface.blit(sprite.get_sprite(), sprite.get_pos())

    def render_text(self, text, antialias, color, position):
        s = self.font.render(text, antialias, color)
        self.surface.blit(s, position)

    def update(self):
        pg.display.update()

    def clean(self):
        self.static_sprites = []
        self.moving_sprites = []

    def toggle_sprites(self):
        self.hide_sprites = not self.hide_sprites

    def toggle_fullscreen(self):
        self.full_screen = not self.full_screen

    def is_fullscreen(self):
        return self.full_screen


if __name__ == "__main__":
    pass

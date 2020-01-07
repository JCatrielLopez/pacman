import pygame as pg

from . import constants


class Display:
    # PEP8: https://www.python.org/dev/peps/pep-0008/#constants
    surface = None
    bg_color = None
    bg_image = None
    hide_sprites = False
    show_values = False
    fullscreen = False
    font = None
    groups = None

    def __init__(self, size):
        flags = pg.DOUBLEBUF
        self.surface = pg.display.set_mode(size, flags)

        self.bg_color = constants.BLACK

        pg.font.init()
        self.font = pg.font.SysFont("default", 20, bold=False)

        self.groups = []

    def __str__(self):
        return repr(self) + f" {self.surface.get_size()}"

    def __new__(cls, size):
        if not hasattr(cls, "instance"):
            cls.instance = super(Display, cls).__new__(cls)
        return cls.instance

    def add(self, group):
        if isinstance(group, pg.sprite.Group):
            return self.groups.append(group)

    def remove(self, group):
        if isinstance(group, pg.sprite.Group):
            self.groups.remove(group)

    def set_background(self, image_path):
        self.bg_image = pg.image.load(image_path)

    def draw(self):
        self.surface.fill(self.bg_color)

        for group in self.groups:
            group.draw(self.surface)

        # display_dim = self.surface.get_size()
        # for x in range(0, display_dim[0], 16):
        #     pg.draw.line(self.surface, (240, 255, 255), (x, 0), (x, display_dim[1]))
        # for y in range(0, display_dim[1], 16):
        #     pg.draw.line(self.surface, (240, 255, 255), (0, y), (display_dim[0], y))

        if not self.hide_sprites:
            self.surface.blit(self.bg_image, (0, 0))
            for group in self.groups:
                for sprite in group:
                    self.surface.blit(sprite.get_sprite(), sprite.get_pos())

    def render_text(self, text, antialias, color, position):
        s = self.font.render(text, antialias, color)
        self.surface.blit(s, position)

    def update(self):
        pg.display.update()

    def clean(self):
        self.groups = []

    def toggle_sprites(self):
        self.hide_sprites = not self.hide_sprites

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen

    def is_fullscreen(self):
        return self.fullscreen

    def draw_image(self, path):
        self.surface.blit(pg.image.load(path).convert(), (0, 0))
        self.update()


if __name__ == "__main__":
    pass

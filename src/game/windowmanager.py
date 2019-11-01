import pygame as pg


class WindowManager:
    """

    WindowManager class
    src.game.WindowManager(self, size, color=(0, 0, 0), image=None): return WindowManager

    """

    def __init__(self, size, color=(0, 0, 0), image=None):
        """

        :param size: Height x Length dimensions of the windows to be created.
        :param color: Background color to fill the windows with. Default color is BLACK.
        :param image: Background image to fill the windows with. Default is None.

        I
        """
        self.display = pg.display
        self.surface = self.display.set_mode(size)
        self.background_color = color
        self.background_image = pg.image.load(image)
        self.sprites_hidden = False
        self.groups = []
        self.fullscreen = False

        pg.font.init()
        self.font = pg.font.SysFont('default', 25, bold=True)

    def set_caption(self, label):
        """

        :param label: A string value to set as the window's caption.
        :return None:
        """
        self.display.set_caption(label)

    def set_icon(self, icon):
        """

        :param icon: The path to the icon image to set as the window's icon.
        :return: None
        """
        self.display.set_icon(pg.image.load(icon))

    def draw(self):
        """
        draw all sprites onto the surface
        :return: None
        """
        self.surface.fill(self.background_color)

        for group in self.groups:
            group.draw(self.surface)

        if not self.sprites_hidden:
            self.surface.blit(self.background_image, (0, 0))
            for group in self.groups:
                for sprite in group:
                    try:
                        self.surface.blit(sprite.get_sprite(), sprite.get_sprite_pos())
                    except AttributeError:
                        continue

    def render_text(self, text, antialias=False, color=(255, 255, 255), pos=(0, 0)):
        """
        draw text on a new Surface
        :param text: str
        :param antialias:
        :param color: tuple. Default value is WHITE.
        :param pos: The x,y coordinates to blit the text  on screen.
        :return: None
        """
        s = self.font.render(text, antialias, color)
        self.surface.blit(s, pos)

    def update(self):
        """
        Update portions of the screen for software displays
        :return:
        """
        self.display.update()

    def hide_sprites(self):
        """
        defines if the sprites are blit on the surface.
        :return: None
        """
        self.sprites_hidden = not self.sprites_hidden

    def add_group(self, group):
        """
        appends group to the end of the container list.
        :param group: pygame.sprite.Group container class for many sprites.
        :return: None
        """
        if isinstance(group, pg.sprite.Group):
            return self.groups.append(group)
        raise TypeError("")  # TODO Poner mensaje de error

    def remove_group(self, group):
        """
        removes group from container list.
        :param group: pygame.sprite.Group container class for many sprites.
        :return:
        """
        return self.groups.remove(group)

    def toggle_fullscreen(self):
        """
        sets the screen to fullscreen or windowed move.
        :return: None
        """
        self.fullscreen = not self.fullscreen
        self.display.toggle_fullscreen()

    def is_fullscreen(self):
        """
        returns True if the screen is in fullscreen mode.
        :return: boolean
        """
        return self.fullscreen

    def change_map(self, image, new_groups):
        """
        Changes the background image and the group of sprites to display on surface.
        :param image: A string path to the new background image
        :param new_groups: A list of pygame.sprite.Groups of sprites
        :return: None
        """
        self.background_image = pg.image.load(image)
        self.groups = new_groups

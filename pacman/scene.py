import pygame as pg

from . import map, constants
from .actors import pacman, ghost


class BaseScene:
    next = None
    display = None
    characters = None
    pacman = None
    ghosts = None
    highscore_value = 0
    score_value = 0
    lives_value = 0

    def __init__(self, display, path, index):
        self.next = self
        self.display = display
        self.display.clean()
        self.highscore_text = "HIGH SCORE: 0"
        self.score_text = "SCORE: 0"
        self.lives_text = "x"
        self.ghosts = []

        self.map = map.Map(path, index)
        self.display.set_background(self.map.get_background())

        self.characters = pg.sprite.Group()
        self.pacman = pacman.Pacman(
            216,
            272,
            constants.TILE_SIZE,
            constants.TILE_SIZE,
            self.map,
            self.characters,
        )

        blinky = ghost.Blinky(
            216,
            176,
            constants.TILE_SIZE,
            constants.TILE_SIZE,
            "../res/ghosts/Blinky",
            self.pacman,
            self.map,
            self.characters,
        )
        self.ghosts.append(blinky)

        self.ghosts.append(
            ghost.Pinky(
                206,
                176,
                constants.TILE_SIZE,
                constants.TILE_SIZE,
                "../res/ghosts/Pinky",
                self.pacman,
                self.map,
                self.characters,
            )
        )

        self.ghosts.append(
            ghost.Inky(
                206,
                176,
                constants.TILE_SIZE,
                constants.TILE_SIZE,
                "../res/ghosts/Inky",
                self.pacman,
                blinky,
                self.map,
                self.characters,
            )
        )

        self.ghosts.append(
            ghost.Clyde(
                206,
                176,
                constants.TILE_SIZE,
                constants.TILE_SIZE,
                "../res/ghosts/Clide",
                self.pacman,
                self.map,
                self.characters,
            )
        )

        self.characters.add(*self.ghosts)

        self.display.clean()
        self.display.add(self.map.get_walls())
        self.display.add(self.map.get_pellets())
        self.display.add(self.characters)

    def process_input(self, events):
        pass

    def _update(self):
        self.pacman.move()

        score, remaining, energizer = self.pacman.check_consumed(self.map.get_pellets())

        for ghost in self.ghosts:
            if energizer:
                ghost.scare()
            ghost.move()

        self.map.pellet_group = remaining
        self.pacman.add_score(score)

        # Si la longitud es cero, entonces hay que cambiar de nivel.
        level_completed = not len(remaining)

        self.score_value = self.get_score()
        self.score_text = f"SCORE: {self.score_value}"
        if self.score_value > self.highscore_value:
            self.highscore_value = self.score_value
        self.highscore_text = f"HIGH SCORE: {self.highscore_value}"
        self.lives_text = f"x{self.pacman.get_lives()}"

        return level_completed

    def render(self):
        self.display.draw()
        self.display.render_text(self.highscore_text, False, constants.WHITE, (15, 510))
        self.display.render_text(
            self.lives_text, False, constants.WHITE, (496 - 75, 510)
        )
        self.display.render_text(
            self.score_text, False, constants.WHITE, (496 / 2 - 50, 510)
        )
        self.display.update()

    def switch(self, scene):
        self.next = scene

    def terminate(self):
        self.next = None

    def get_score(self):
        return self.pacman.get_score()


class FirstLevel(BaseScene):
    def __init__(self, display, path, index):
        super().__init__(display, path, index)

    def process_input(self, events):
        for event in events:
            if event.type == 2:  # Key pressed
                if event.dict["key"] == 104:
                    self.display.toggle_sprites()
                elif event.dict["key"] == 8:
                    self.switch(SecondLevel(self.display, "../res/map/02_level.npz", 1))
                elif event.dict["key"] == 114:
                    self.switch(FirstLevel(self.display, "../res/map/01_level.npz", 0))
                elif event.dict["key"] == 273:
                    self.pacman.move_up()
                elif event.dict["key"] == 274:
                    self.pacman.move_down()
                elif event.dict["key"] == 275:
                    self.pacman.move_right()
                elif event.dict["key"] == 276:
                    self.pacman.move_left()
            else:
                print(event.type)
        self.update()

    def update(self):
        if super()._update():
            self.switch(SecondLevel(self.display, "../res/map/02_level.npz", 1))

        collided, eaten = self.pacman.check_collision(self.ghosts)

        if collided:
            if not self.ghosts[0].is_scared():
                self.switch(FirstLevel(self.display, "../res/map/01_level.npz", 0))
            else:
                for ghost in eaten:
                    self.score_value += ghost.get_score()
                    ghost.restart()


class SecondLevel(BaseScene):
    def __init__(self, display, path, index):
        super().__init__(display, path, index)

    def process_input(self, events):
        for event in events:
            if event.type == 2:  # Key pressed
                if event.dict["key"] == 104:
                    self.display.toggle_sprites()
                elif event.dict["key"] == 8:
                    self.switch(ThirdLevel(self.display, "../res/map/03_level.npz", 2))
                elif event.dict["key"] == 114:
                    self.switch(SecondLevel(self.display, "../res/map/02_level.npz", 1))
                elif event.dict["key"] == 273:
                    self.pacman.move_up()
                elif event.dict["key"] == 274:
                    self.pacman.move_down()
                elif event.dict["key"] == 275:
                    self.pacman.move_right()
                elif event.dict["key"] == 276:
                    self.pacman.move_left()
            else:
                print(event.type)
        self.update()

    def update(self):
        if super()._update():
            self.switch(ThirdLevel(self.display, "../res/map/03_level.npz", 2))

        collided, eaten = self.pacman.check_collision(self.ghosts)

        if collided:
            if not self.ghosts[0].is_scared():
                self.switch(FirstLevel(self.display, "../res/map/02_level.npz", 1))
            else:
                self.score_value += self.ghosts[0].get_score()


class ThirdLevel(BaseScene):
    def __init__(self, display, path, index):
        super().__init__(display, path, index)

    def process_input(self, events):
        for event in events:
            if event.type == 2:  # Key pressed
                if event.dict["key"] == 104:
                    self.display.toggle_sprites()
                elif event.dict["key"] == 8:
                    self.switch(FourthLevel(self.display, "../res/map/04_level.npz", 3))
                elif event.dict["key"] == 114:
                    self.switch(ThirdLevel(self.display, "../res/map/03_level.npz", 2))
                elif event.dict["key"] == 273:
                    self.pacman.move_up()
                elif event.dict["key"] == 274:
                    self.pacman.move_down()
                elif event.dict["key"] == 275:
                    self.pacman.move_right()
                elif event.dict["key"] == 276:
                    self.pacman.move_left()
            else:
                print(event.type)
        self.update()

    def update(self):
        if super()._update():
            self.switch(FourthLevel(self.display, "../res/map/04_level.npz", 3))

        collided, eaten = self.pacman.check_collision(self.ghosts)

        if collided:
            if not self.ghosts[0].is_scared():
                self.switch(ThirdLevel(self.display, "../res/map/03_level.npz", 2))
            else:
                self.score_value += self.ghosts[0].get_score()


class FourthLevel(BaseScene):
    def __init__(self, display, path, index):
        super().__init__(display, path, index)

    def process_input(self, events):
        for event in events:
            if event.type == 2:  # Key pressed
                if event.dict["key"] == 104:
                    self.display.toggle_sprites()
                elif event.dict["key"] == 8:
                    self.switch(FifthLevel(self.display, "../res/map/05_level.npz", 4))
                elif event.dict["key"] == 114:
                    self.switch(FourthLevel(self.display, "../res/map/04_level.npz", 3))
                elif event.dict["key"] == 273:
                    self.pacman.move_up()
                elif event.dict["key"] == 274:
                    self.pacman.move_down()
                elif event.dict["key"] == 275:
                    self.pacman.move_right()
                elif event.dict["key"] == 276:
                    self.pacman.move_left()
            else:
                print(event.type)
        self.update()

    def update(self):
        if super()._update():
            self.switch(FifthLevel(self.display, "../res/map/05_level.npz", 4))

        collided, eaten = self.pacman.check_collision(self.ghosts)

        if collided:
            if not self.ghosts[0].is_scared():
                self.switch(FourthLevel(self.display, "../res/map/04_level.npz", 3))
            else:
                self.score_value += self.ghosts[0].get_score()


class FifthLevel(BaseScene):
    def __init__(self, display, path, index):
        super().__init__(display, path, index)

    def process_input(self, events):
        for event in events:
            if event.type == 2:  # Key pressed
                if event.dict["key"] == 104:
                    self.display.toggle_sprites()
                elif event.dict["key"] == 8:
                    self.switch(FirstLevel(self.display, "../res/map/01_level.npz", 0))
                elif event.dict["key"] == 114:
                    self.switch(FifthLevel(self.display, "../res/map/05_level.npz", 4))
                elif event.dict["key"] == 273:
                    self.pacman.move_up()
                elif event.dict["key"] == 274:
                    self.pacman.move_down()
                elif event.dict["key"] == 275:
                    self.pacman.move_right()
                elif event.dict["key"] == 276:
                    self.pacman.move_left()
            else:
                print(event.type)
        self.update()

    def update(self):
        if super()._update():
            self.switch(FirstLevel(self.display, "../res/map/01_level.npz", 0))

        collided, eaten = self.pacman.check_collision(self.ghosts)

        if collided:
            if not self.ghosts[0].is_scared():
                self.switch(FifthLevel(self.display, "../res/map/05_level.npz", 4))
            else:
                self.score_value += self.ghosts[0].get_score()

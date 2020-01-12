import pygame as pg

from pacman.actors.state import State
from . import map, constants
from .actors import pacman, ghost, mode


class GameScene:
    display = None
    characters = None
    pacman = None
    ghosts = None
    high_score_value = 0
    score_value = 0
    lives_value = 0
    finish = None
    map_path = None

    def __init__(self, display, path):
        self.finish = False
        self.display = display
        self.high_score_text = "HIGH SCORE: 0"
        self.score_text = "SCORE: 0"
        self.lives_text = "x"
        self.ghosts = []


        self.map_path = path
        self.map = map.Map(path)
        print("Scene: ", self.map)

        self.characters = pg.sprite.Group()
        self.pacman = pacman.Pacman(
            216,
            272,
            constants.TILE_SIZE,
            constants.TILE_SIZE,
            self.map,
            self.notify_scores,
            self.notify_lives,
            self.notify_pellets_in_map_change,
            self.characters,
        )
        self.notify_lives()

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
        State.set_notify_dual_state_change(self.notify_dual_state_change)
        State.set_notify_out_of_frightened(self.notify_out_of_frightened)

    def init_scene(self):
        self.display.clean()
        self.display.set_background(self.map.get_background())
        self.display.add_static_sprites(self.map.get_walls())
        self.display.add_moving_sprites(self.map.get_pellets())
        self.display.add_moving_sprites(self.characters)

    def notify_scores(self):
        self.score_value = self.get_score()
        self.score_text = f"SCORE: {self.score_value}"
        if self.score_value > self.high_score_value:
            self.high_score_value = self.score_value
            self.high_score_text = f"HIGH SCORE: {self.high_score_value}"

    def notify_lives(self):
        self.lives_text = f"x{self.pacman.get_lives()}"
        if self.pacman.get_lives() <= 0:
            self.terminate()

    def notify_pellets_in_map_change(self, remaining):
        self.map.pellet_group = remaining
        self.check_level_completed()

        if self.pacman.power_up:
            for ghost in self.ghosts:
                ghost.get_state().register_as_frightened()
                ghost.fright()

            State.change_to_fright()

    def notify_out_of_frightened(self):
        for ghost in self.ghosts:
            if ghost.get_current_state() != State.DEAD:
                ghost.restart_sprite()
        self.pacman.power_up = False

    def notify_dual_state_change(self):
        for ghost in self.ghosts:
            ghost.get_state().change_to_scatter_chase()

    def pacman_lose(self):
        return self.pacman.get_lives() <= 0

    def process_input(self, events):
        pass

    def check_level_completed(self):

        # Si la longitud es cero, entonces hay que cambiar de nivel.
        level_completed = not len(self.map.pellet_group)
        if level_completed:
            self.terminate()

    def render(self):
        self.display.draw()
        self.display.render_text(self.high_score_text, False, constants.WHITE, (15, 510))
        self.display.render_text(
            self.lives_text, False, constants.WHITE, (496 - 75, 510)
        )
        self.display.render_text(
            self.score_text, False, constants.WHITE, (496 / 2 - 50, 510)
        )
        self.display.update()

        # pg.image.save(self.display.surface, f"../res/screenshots/frame - {time.time()}")

    def terminate(self):
        self.finish = True
        self.display.clean()

    def is_finish(self):
        return self.finish

    def get_score(self):
        return self.pacman.get_score()

    def process_input(self, events):
        for event in events:
            if event.type == 2:  # Key pressed
                if event.dict["key"] == 104:
                    self.display.toggle_sprites()
                elif event.dict["key"] == 8:  # next level
                    self.terminate()
                elif event.dict["key"] == 273:
                    self.pacman.move_up()
                elif event.dict["key"] == 274:
                    self.pacman.move_down()
                elif event.dict["key"] == 275:
                    self.pacman.move_right()
                elif event.dict["key"] == 276:
                    self.pacman.move_left()

        self.update()

    def update(self):
        self.pacman.move()

        # print("Distance: ", self.map.get_distance(self.map.get_grid(self.pacman.get_pos()), (14, 14)))
        for ghost in self.ghosts:
            ghost.move()


        self.pacman.check_collision_pellets(self.map.get_pellets())

        collided, collided_ghosts = self.pacman.check_collision_ghosts(self.ghosts)

        if collided:
            if not self.pacman.power_up:
                self.pacman.decrement_lives()

                for ghost in self.ghosts:
                    ghost.restart()
                self.pacman.restart()
                State.restart()

            else:
                for ghost in collided_ghosts:
                    if ghost.get_current_state() != State.DEAD:
                        ghost.die()
                        self.score_value += ghost.get_score()

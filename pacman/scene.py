import numpy as np
import pygame as pg
from PIL import Image, ImageOps

import pacman.display as display
import pacman.map as map
from pacman import constants
from pacman.actors import ghost
from pacman.actors.pacman import Pacman
from pacman.actors.state_manager import StateManager


# logger = logging.getLogger()


class GameScene:
    display = None
    characters = None
    pacman = None
    ghosts = None
    high_score_value = 0
    score_value = 0
    finish = None
    map_path = None

    def __init__(self, path):
        self.finish = False
        # os.environ["SDL_VIDEODRIVER"] = "dummy"
        self.display = display.Display((constants.WIDTH, constants.HEIGHT))
        self.high_score_text = "HIGH SCORE: 0"
        self.score_text = "SCORE: 0"
        self.lives_text = "x3"
        self.global_pellets_text = "CONT_GLOBAL: 0"
        self.ghost_counter = "CONT_GHOSTS: []"
        self.ghosts = []

        self.reward = 0

        self.map_path = path
        self.map = map.Map(path)

        self.characters = pg.sprite.Group()
        self.state_manager = StateManager()

        self.pacman = Pacman(
            216,
            272,
            constants.TILE_SIZE,
            constants.TILE_SIZE,
            self.map,
            self.update_texts,
            self.notify_lives,
            self.notify_pellets_in_map_change,
            self.characters,
        )

        self.blinky = ghost.Blinky(
            width=constants.TILE_SIZE,
            height=constants.TILE_SIZE,
            spritesheet_path="../../res/ghosts/Blinky",
            spritesheet_chase_path="../../res/ghosts/State_chase/Blinky",
            spritesheet_scatter_path="../../res/ghosts/State_scatter/Blinky",
            notify_in_home=self.state_manager.change_to_in_home,
            pacman=self.pacman,
            map=self.map,
            groups=tuple(),
        )
        self.ghosts.append(self.blinky)

        self.pinky = ghost.Pinky(
            width=constants.TILE_SIZE,
            height=constants.TILE_SIZE,
            spritesheet_path="../../res/ghosts/Pinky",
            spritesheet_chase_path="../../res/ghosts/State_chase/Pinky",
            spritesheet_scatter_path="../../res/ghosts/State_scatter/Pinky",
            notify_in_home=self.state_manager.change_to_in_home,
            pacman=self.pacman,
            map=self.map,
            groups=tuple(),
        )
        self.ghosts.append(self.pinky)

        self.inky = ghost.Inky(
            width=constants.TILE_SIZE,
            height=constants.TILE_SIZE,
            spritesheet_path="../../res/ghosts/Inky",
            spritesheet_chase_path="../../res/ghosts/State_chase/Inky",
            spritesheet_scatter_path="../../res/ghosts/State_scatter/Inky",
            notify_in_home=self.state_manager.change_to_in_home,
            pacman=self.pacman,
            blinky=self.blinky,
            map=self.map,
            groups=tuple(),
        )
        self.ghosts.append(self.inky)

        self.clyde = ghost.Clyde(
            width=constants.TILE_SIZE,
            height=constants.TILE_SIZE,
            spritesheet_path="../../res/ghosts/Clide",
            spritesheet_chase_path="../../res/ghosts/State_chase/Clide",
            spritesheet_scatter_path="../../res/ghosts/State_scatter/Clide",
            notify_in_home=self.state_manager.change_to_in_home,
            pacman=self.pacman,
            map=self.map,
            groups=tuple(),
        )
        self.ghosts.append(self.clyde)

        self.characters.add(*self.ghosts)

        # State manager
        self.state_manager.set_ghosts(self.ghosts)
        self.state_manager.set_notify_pacman(self.pacman.set_power_up, False)

        self.pacman_moves = [
            self.pacman.move_up,
            self.pacman.move_left,
            self.pacman.move_down,
            self.pacman.move_right,
        ]

        self.clock = pg.time.Clock()

        self.state_value = "[]"
        self.pacman_ate = False
        self.pacman_energizer = False
        self.steps = 0

    def init_scene(self):
        self.display.clean()
        self.display.set_background(self.map.get_background())
        self.display.add_static_sprites(self.map.get_walls())
        self.display.add_moving_sprites(self.map.get_pellets())
        self.display.add_moving_sprites(self.characters)

    def notify_lives(self):
        self.lives_text = f"x{self.pacman.get_lives()}"
        # print(" - Rip pacman")
        if self.pacman.get_lives() <= 0:
            self.terminate()

    def notify_pellets_in_map_change(self, remaining, pellets_eaten, ate_an_energizer):
        self.map.pellet_group = remaining
        self.is_level_done()

        if ate_an_energizer:
            # logger.debug("Pacman ate an energizer")
            self.state_manager.change_to_frightened()

        self.state_manager.update_pellet_global_counter_values(pellets_eaten)
        self.state_manager.update_pellet_ghost_counter_values(pellets_eaten)
        self.state_manager.reset_last_pellet_timer()

        self.pacman_ate = pellets_eaten > 0
        self.pacman_energizer = ate_an_energizer
        self.steps = 0

    def render(self):
        self.display.draw()
        self.display.render_text(
            self.high_score_text, False, constants.WHITE, (15, 510)
        )
        self.display.render_text(self.lives_text, False, constants.WHITE, (421, 510))
        self.display.render_text(self.score_text, False, constants.WHITE, (198, 510))
        self.display.render_text(self.state_value, False, constants.YELLOW, (10, 550))

        # self.display.render_text(
        #     self.global_pellets_text, False, constants.YELLOW, (300, 525)
        # )
        #
        # self.display.render_text(self.ghost_counter, False, constants.YELLOW, (15, 530))
        self.display.update()

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

    def toggle_sprites(self):
        self.display.toggle_sprites()

    def process_action(self, action):
        if action == 0:
            self.pacman.move_up()
        elif action == 1:
            self.pacman.move_left()
        elif action == 2:
            self.pacman.move_down()
        elif action == 3:
            self.pacman.move_right()

        return self.update()

    def update(self):

        self.pacman.move()

        for ghost in self.ghosts:
            ghost.move()

        self.pacman_ate = False
        self.pacman_energizer = False

        self.pacman.check_collision_pellets(self.map.get_pellets())

        exists_collision, ghosts_collided = self.pacman.check_collision_ghosts(
            self.ghosts
        )

        if exists_collision:
            for ghost in ghosts_collided:
                if not (ghost.can_be_consumed() or ghost.can_be_ignored()):
                    self.pacman.decrement_lives()
                    self.restart()
                    self.reward = -100

                    if self.pacman.get_lives() < 3:
                        self.state_manager.update_pellet_global_counter(True)
                        self.state_manager.update_pellet_ghost_counter(False)

            ghost_consumed_ghost = self.state_manager.check_collision(ghosts_collided)

            if ghost_consumed_ghost:
                self.reward = 100
        elif not self.pacman_ate:
            self.reward = 0
        else:
            if self.pacman_energizer:
                self.reward = 200
            else:
                self.reward = 100

        self.update_texts()
        self.clock.tick(constants.FPS)
        return exists_collision, self.get_score()

    def is_level_done(self):
        if not len(self.map.pellet_group):
            self.terminate()

    def terminate(self):
        self.finish = True
        self.display.clean()
        self.state_manager.terminate()

    def restart(self):
        self.state_manager.restart()
        for ghost in self.ghosts:
            ghost.restart_position()
            ghost.update_spritesheet()

        self.pacman.restart()

    def is_finish(self):
        return self.finish

    def update_texts(self):
        self.score_value = self.get_score()
        self.score_text = f"SCORE: {self.score_value}"
        if self.score_value > self.high_score_value:
            self.high_score_value = self.score_value
            self.high_score_text = f"HIGH SCORE: {self.high_score_value}"
        self.global_pellets_text = (
            f"CONT_GLOBAL: {self.state_manager.get_global_counter_value()}"
        )
        self.ghost_counter = (
            f"CONT_GHOSTS: {self.state_manager.get_pellet_counter_value()}"
        )

    def get_state(self):
        state = np.zeros((32, 32, 3), dtype=np.uint8)
        for pellet in self.map.get_pellets():
            grid_position = self.map.get_grid(pellet.get_pos())
            state[grid_position[0]][grid_position[1]] = constants.WHITE

        for wall in self.map.get_walls():
            grid_position = self.map.get_grid(wall.get_pos())
            state[grid_position[0]][grid_position[1]] = constants.DARK_GRAY

        for ghost in self.ghosts:
            grid_position = self.map.get_grid(ghost.get_pos())
            x = min(grid_position[0], 27)
            y = min(grid_position[1], 30)

            state[x][y] = ghost.color

        pacman_position = self.map.get_grid(self.pacman.get_pos())
        x = min(pacman_position[0], 27)
        y = min(pacman_position[1], 30)

        state[x][y] = constants.YELLOW

        img = Image.fromarray(state).rotate(-90)
        img = ImageOps.grayscale(img)
        return img

    def get_reward(self):
        r = self.reward
        r = np.sign(r) * np.log(1 + abs(r))
        self.reward = 0
        return r

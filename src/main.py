import pygame as pg

from src.Game import Game

if __name__ == "__main__":
    game = Game(1, 0, 3, pg.NOFRAME)
    game.run()

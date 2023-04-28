import pygame as pg
from settings import *
Vec = pg.math.Vector2

class Movable(pg.sprite.Sprite):
    def __init__(self, init_pos, init_dir):
        pg.sprite.Sprite.__init__(self)
        self.direction = init_dir.normalize()
        self.pos = init_pos
        self.speed = 1
        self.window = pg.display.get_surface()

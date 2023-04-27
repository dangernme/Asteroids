import pygame as pg
from settings import *
Vec = pg.math.Vector2

class Movable(pg.sprite.Sprite):
    def __init__(self, init_pos, init_dir, init_acc_lim):
        pg.sprite.Sprite.__init__(self)
        self.direction = init_dir.normalize()
        self.pos = init_pos
        self.vel = Vec(0, 0)
        self.acc = Vec(0, 0)
        self.acc_lim = init_acc_lim
        self.window = pg.display.get_surface()

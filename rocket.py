from os.path import join
import pygame as pg
from movable import Movable
from settings import *
Vec = pg.math.Vector2

class Rocket(Movable):
    def __init__(self, init_pos, init_dir, init_acc_lim):
        super().__init__(init_pos, init_dir, init_acc_lim)
        self.image_0 = pg.image.load(join('assets', join('Ships', 'Main Ship Full health.png')))
        self.image_1 = pg.image.load(join('assets', join('Ships', 'Main Ship Slight damage.png')))
        self.image_2 = pg.image.load(join('assets', join('Ships', 'Main Ship Damaged.png')))

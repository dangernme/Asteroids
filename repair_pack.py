import pygame as pg
import random as rd
from os.path import join
import collectable_abstract
from settings import *

class Medi(collectable_abstract.Collectable_Abstract):
    def __init__(self, init_pos):
        super().__init__(init_pos)
        self.image = pg.image.load(join('assets', 'heart.png'))
        self.healh = rd.randint(1, 10)
        self.radius = 15
        self.rect = self.image.get_rect(x=self.pos.x, y=self.pos.y)
        
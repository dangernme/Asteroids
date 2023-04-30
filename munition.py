import pygame as pg
import random as rd
from os.path import join
import collectable_abstract
from settings import *

class Munition(collectable_abstract.Collectable_Abstract):
    def __init__(self, init_pos):
        super().__init__(init_pos)
        self.image = pg.image.load(join('assets', 'Ships', 'Weapons', 'Rocket.png'))
        self.image = pg.transform.scale_by(self.image, 3)
        self.amount = rd.randint(1, 10)
        self.radius = 15
        self.rect = self.image.get_rect(x=self.pos.x, y=self.pos.y)

from os.path import join
import random as rd
import pygame as pg
from settings import *
from asteroid_abstract import Asteroid_Abstract

class Asteroid_Small(Asteroid_Abstract):
    def __init__(self, init_pos):
        super().__init__(init_pos)
        self.speed = rd.randint(2, 3)
        self.damage = 5
        self.radius = 15
        self.path = join('assets', 'asteroids', 'small')
        self.images = [pg.image.load(join(self.path, "a30000.png")),
                       pg.image.load(join(self.path, "a30001.png")),
                       pg.image.load(join(self.path, "a30002.png")),
                       pg.image.load(join(self.path, "a30003.png")),
                       pg.image.load(join(self.path, "a30004.png")),
                       pg.image.load(join(self.path, "a30005.png")),
                       pg.image.load(join(self.path, "a30006.png")),
                       pg.image.load(join(self.path, "a30007.png")),
                       pg.image.load(join(self.path, "a30008.png")),
                       pg.image.load(join(self.path, "a30009.png")),
                       pg.image.load(join(self.path, "a30010.png")),
                       pg.image.load(join(self.path, "a30011.png")),
                       pg.image.load(join(self.path, "a30012.png")),
                       pg.image.load(join(self.path, "a30013.png")),
                       pg.image.load(join(self.path, "a30014.png")),
                       pg.image.load(join(self.path, "a30015.png"))]     
        self.rect = self.images[0].get_rect(x=self.pos.x, y=self.pos.y)
        
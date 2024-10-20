from os.path import join
import random as rd
import pygame as pg
from settings import *
from asteroids.asteroid_abstract import AsteroidAbstract

class AsteroidD3(AsteroidAbstract):
    def __init__(self, init_pos):
        super().__init__(init_pos)
        self.speed = rd.randint(1, 5)
        self.damage = 20
        self.points = 3
        self.path = join('assets', 'asteroids', 'medium')
        self.images = [pg.image.load(join(self.path, "d30000.png")).convert_alpha(),
                       pg.image.load(join(self.path, "d30001.png")).convert_alpha(),
                       pg.image.load(join(self.path, "d30002.png")).convert_alpha(),
                       pg.image.load(join(self.path, "d30003.png")).convert_alpha(),
                       pg.image.load(join(self.path, "d30004.png")).convert_alpha(),
                       pg.image.load(join(self.path, "d30005.png")).convert_alpha(),
                       pg.image.load(join(self.path, "d30006.png")).convert_alpha(),
                       pg.image.load(join(self.path, "d30007.png")).convert_alpha(),
                       pg.image.load(join(self.path, "d30008.png")).convert_alpha(),
                       pg.image.load(join(self.path, "d30009.png")).convert_alpha(),
                       pg.image.load(join(self.path, "d30010.png")).convert_alpha(),
                       pg.image.load(join(self.path, "d30011.png")).convert_alpha(),
                       pg.image.load(join(self.path, "d30012.png")).convert_alpha(),
                       pg.image.load(join(self.path, "d30013.png")).convert_alpha(),
                       pg.image.load(join(self.path, "d30014.png")).convert_alpha(),
                       pg.image.load(join(self.path, "d30015.png")).convert_alpha()]
        self.image = self.images[0]
        self.rect = self.image.get_rect()

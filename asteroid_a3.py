from os.path import join
import random as rd
import pygame as pg
from settings import *
from asteroid_abstract import AsteroidAbstract

class AsteroidA3(AsteroidAbstract):
    def __init__(self, init_pos):
        super().__init__(init_pos)
        self.speed = rd.randint(2, 3)
        self.damage = 5
        self.points = 1
        self.path = join('assets', 'asteroids', 'small')
        self.images = [pg.image.load(join(self.path, "a30000.png")).convert_alpha(),
                       pg.image.load(join(self.path, "a30001.png")).convert_alpha(),
                       pg.image.load(join(self.path, "a30002.png")).convert_alpha(),
                       pg.image.load(join(self.path, "a30003.png")).convert_alpha(),
                       pg.image.load(join(self.path, "a30004.png")).convert_alpha(),
                       pg.image.load(join(self.path, "a30005.png")).convert_alpha(),
                       pg.image.load(join(self.path, "a30006.png")).convert_alpha(),
                       pg.image.load(join(self.path, "a30007.png")).convert_alpha(),
                       pg.image.load(join(self.path, "a30008.png")).convert_alpha(),
                       pg.image.load(join(self.path, "a30009.png")).convert_alpha(),
                       pg.image.load(join(self.path, "a30010.png")).convert_alpha(),
                       pg.image.load(join(self.path, "a30011.png")).convert_alpha(),
                       pg.image.load(join(self.path, "a30012.png")).convert_alpha(),
                       pg.image.load(join(self.path, "a30013.png")).convert_alpha(),
                       pg.image.load(join(self.path, "a30014.png")).convert_alpha(),
                       pg.image.load(join(self.path, "a30015.png")).convert_alpha()]
        self.image = self.images[0]
        self.rect = self.image.get_rect()

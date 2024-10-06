from os.path import join
import random as rd
import pygame as pg
from settings import *
from asteroid_abstract import AsteroidAbstract

class AsteroidA1(AsteroidAbstract):
    def __init__(self, init_pos):
        super().__init__(init_pos)
        self.speed = rd.randint(1, 5)
        self.damage = 10
        self.path = join('assets', 'asteroids', 'medium')
        self.images = [pg.image.load(join(self.path, "a10000.png")).convert_alpha(),
                       pg.image.load(join(self.path, "a10001.png")).convert_alpha(),
                       pg.image.load(join(self.path, "a10002.png")).convert_alpha(),
                       pg.image.load(join(self.path, "a10003.png")).convert_alpha(),
                       pg.image.load(join(self.path, "a10004.png")).convert_alpha(),
                       pg.image.load(join(self.path, "a10005.png")).convert_alpha(),
                       pg.image.load(join(self.path, "a10006.png")).convert_alpha(),
                       pg.image.load(join(self.path, "a10007.png")).convert_alpha(),
                       pg.image.load(join(self.path, "a10008.png")).convert_alpha(),
                       pg.image.load(join(self.path, "a10009.png")).convert_alpha(),
                       pg.image.load(join(self.path, "a10010.png")).convert_alpha(),
                       pg.image.load(join(self.path, "a10011.png")).convert_alpha(),
                       pg.image.load(join(self.path, "a10012.png")).convert_alpha(),
                       pg.image.load(join(self.path, "a10013.png")).convert_alpha(),
                       pg.image.load(join(self.path, "a10014.png")).convert_alpha(),
                       pg.image.load(join(self.path, "a10015.png")).convert_alpha()]
        self.image = self.images[0]
        self.rect = self.image.get_rect()

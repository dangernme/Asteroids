from os.path import join
import random as rd
import pygame as pg
from settings import *
from asteroid_abstract import AsteroidAbstract

class AsteroidMedium(AsteroidAbstract):
    def __init__(self, init_pos):
        super().__init__(init_pos)
        self.speed = rd.randint(1, 5)
        self.damage = 10
        self.radius = 27
        self.path = join('assets', 'asteroids', 'medium')
        self.images = [pg.image.load(join(self.path, "a10000.png")),
                       pg.image.load(join(self.path, "a10001.png")),
                       pg.image.load(join(self.path, "a10002.png")),
                       pg.image.load(join(self.path, "a10003.png")),
                       pg.image.load(join(self.path, "a10004.png")),
                       pg.image.load(join(self.path, "a10005.png")),
                       pg.image.load(join(self.path, "a10006.png")),
                       pg.image.load(join(self.path, "a10007.png")),
                       pg.image.load(join(self.path, "a10008.png")),
                       pg.image.load(join(self.path, "a10009.png")),
                       pg.image.load(join(self.path, "a10010.png")),
                       pg.image.load(join(self.path, "a10011.png")),
                       pg.image.load(join(self.path, "a10012.png")),
                       pg.image.load(join(self.path, "a10013.png")),
                       pg.image.load(join(self.path, "a10014.png")),
                       pg.image.load(join(self.path, "a10015.png"))]
        self.rect = self.images[0].get_rect(x=self.pos.x, y=self.pos.y)
        self.image = self.images[0]

    def update(self):
        self.image = self.images[1]

from os.path import join
import random as rd
import pygame as pg
from settings import *
from asteroids.asteroid_abstract import AsteroidAbstract

class AsteroidA3(AsteroidAbstract):
    def __init__(self, init_pos):
        super().__init__(init_pos)
        self.speed = rd.randint(2, 3)
        self.damage = 5
        self.points = 1
        self.path = join('assets', 'asteroids', 'small')
        self.images = []
        for i in range(16):
            self.images.append(pg.image.load(join(self.path, f"a3{str(i).zfill(4)}.png")).convert_alpha())
        self.image = self.images[0]
        self.rect = self.image.get_rect()

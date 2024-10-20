from os.path import join
import random as rd
import pygame as pg
from settings import *
from asteroids.asteroid_abstract import AsteroidAbstract

class AsteroidD3(AsteroidAbstract):
    def __init__(self, init_pos):
        super().__init__(init_pos)
        self.damage = 20
        self.points = 3
        self.path = join('assets', 'asteroids', 'medium')
        self.images = []
        for i in range(16):
            self.images.append(pg.image.load(join(self.path, f"d3{str(i).zfill(4)}.png")).convert_alpha())
        self.image = self.images[0]
        self.rect = self.image.get_rect()

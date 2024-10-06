from os.path import join
import random as rd
import pygame as pg
from settings import *

class Munition(pg.sprite.Sprite):
    def __init__(self, init_pos):
        super().__init__()
        self.pos = init_pos
        self.image = pg.image.load(join('assets', 'Ships', 'Weapons', 'Rocket.png'))
        self.image = pg.transform.scale_by(self.image, 3)
        self.amount = rd.randint(1, 10)
        self.rect = self.image.get_rect(x=self.pos.x, y=self.pos.y)

    def draw(self, surface):
        pg.draw.rect(surface, (255, 0, 0), self.rect, 2)

import random as rd
import pygame as pg
from settings import *
from movable import Movable
Vec = pg.math.Vector2

class AsteroidAbstract(Movable):
    def __init__(self, init_pos):
        super().__init__(init_pos, Vec(rd.randint(-10, 10), rd.randint(1, 10)).normalize())
        self.animation_count = 0.0
        self.rect = None
        self.image = None

    def update(self):
        self.animation_count += 0.1
        self.pos += self.speed * self.direction.normalize()
        self.rect = self.images[int(self.animation_count) % 15].get_rect(x=self.pos.x, y=self.pos.y)
        self.image = self.images[int(self.animation_count) % 15]

        if self.pos.x + self.rect.width / 2 < TEXT_WIDTH:
            self.pos.x = TEXT_WIDTH - self.rect.width / 2
            self.direction.x *= -1
        if self.pos.x + self.rect.width / 2 > WIDTH:
            self.pos.x = WIDTH - self.rect.width / 2
            self.direction.x *= -1
        if self.pos.y + self.rect.height / 2 < 0:
            self.pos.y = -self.rect.height / 2
            self.direction.y *= -1
        if self.pos.y + self.rect.height / 2 > HEIGHT:
            self.pos.y = HEIGHT - self.rect.height / 2
            self.direction.y *= -1

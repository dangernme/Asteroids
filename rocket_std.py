from os.path import join
import pygame as pg
from settings import *
Vec = pg.math.Vector2

class RocketStd(pg.sprite.Sprite):
    def __init__(self, init_pos, init_dir):
        super().__init__()
        self.direction = init_dir.normalize()
        self.pos = init_pos
        self.speed = 1
        self.image = pg.image.load(join('assets', 'Ships', 'Weapons', 'rocket_std.png')).convert_alpha()
        self.image = pg.transform.rotate(self.image, self.direction.angle_to(Vec(0, -1)))
        self.rect = self.image.get_rect()
        self.speed = 12

    def update(self):
        mask = self.image.get_bounding_rect()
        self.image = self.image.subsurface(mask).copy()
        self.rect = self.image.get_rect(center=self.pos)
        self.pos += self.speed * self.direction.normalize()

    def draw(self, surface):
        pg.draw.rect(surface, (0, 255, 0), self.rect, 1)

from os.path import join
import pygame as pg
from settings import *
Vec = pg.math.Vector2

class Rocket(pg.sprite.Sprite):
    def __init__(self, init_pos, init_dir):
        super().__init__()
        self.direction = init_dir.normalize()
        self.pos = init_pos
        self.speed = 1
        self.image = pg.image.load(join('assets', 'Ships', 'Weapons', 'Rocket.png'))
        self.image = pg.transform.rotate(self.image, self.direction.angle_to(Vec(0, -1)))
        self.rect = self.image.get_rect(x=self.pos.x, y=self.pos.y)
        self.pos -= (self.rect.width // 2, self.rect.height // 2) # Correct start position of rocket to ships center
        self.speed = 10

    def update(self):
        self.rect = self.image.get_rect(x=self.pos.x, y = self.pos.y)
        self.pos += self.speed * self.direction.normalize()

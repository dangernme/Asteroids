import os
import pygame as pg
from settings import *
Vec = pg.math.Vector2

class Movable(pg.sprite.Sprite):
    def __init__(self, x_pos, y_pos, image_path):
        self.clean_image = pg.image.load(os.path.join('assets', image_path))
        self.image = self.clean_image
        self.orientation = 0
        self.pos = Vec(x_pos, y_pos)
        self.vel = Vec(0, 0)
        self.acc = Vec(0, 0)

    def rotate(self, image, angle):
        self.image = self.clean_image
        return pg.transform.rotate(image, angle)

    def update(self):
        if self.pos.x < 0:
            self.pos.x = 0
        if self.pos.x > WIDTH:
            self.pos.x = WIDTH
        if self.pos.y < 0:
            self.pos.y = 0
        if self.pos.y > HEIGHT:
            self.pos.y = HEIGHT
 
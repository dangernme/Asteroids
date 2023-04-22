import os
import pygame as pg
Vec = pg.math.Vector2

class Movable(pg.sprite.Sprite):
    def __init__(self, x_pos, y_pos, image_path):
        self.clean_image = pg.image.load(os.path.join('assets', image_path))
        self.image = self.clean_image
        self.orientation = 0
        self.pos = Vec(x_pos, y_pos)
        self.vel = Vec(0, 0)
        self.acc = Vec(0, 0)

    def rotate(self, image, angle, pos):
        rotated_image = pg.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center = image.get_rect(center = pos).center)

        return rotated_image, new_rect
    
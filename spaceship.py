from os.path import join
import pygame as pg
from settings import *
Vec = pg.math.Vector2

class Spaceship():
    def __init__(self, init_pos):
        self.clean_image = pg.image.load(join('assets', join('Ships', 'Main Ship Full health.png')))
        self.image = self.clean_image
        self.direction = Vec(1, 0).normalize()
        self.pos = init_pos
        self.vel = Vec(0, 0)
        self.acc = Vec(0, 0)
        self.acc_lim = 0.5

    def update(self):
        self.acc = Vec(0, 0)
        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT]:
            self.direction = self.direction.rotate(-5)
        if keys[pg.K_RIGHT]:
            self.direction = self.direction.rotate(+5)


        if self.pos.x < 0:
            self.pos.x = 0
            self.vel.x *= -1
            self.direction.x *= -1
        if self.pos.x > WIDTH:
            self.pos.x = WIDTH
            self.vel.x *= -1
            self.direction.x *= -1
        if self.pos.y < 0:
            self.pos.y = 0
            self.vel.y *= -1
            self.direction.y *= -1
        if self.pos.y > HEIGHT:
            self.pos.y = HEIGHT
            self.vel.y *= -1
            self.direction.y *= -1

        if keys[pg.K_UP]:
            self.acc += self.direction * self.acc_lim

        self.acc += self.vel * PLAYER_FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.image = pg.transform.rotate(self.clean_image, self.direction.angle_to(Vec(0, -1)))

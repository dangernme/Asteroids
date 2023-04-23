from os.path import join
import random as rd
import pygame as pg
from settings import *
Vec = pg.math.Vector2

class Spaceship():
    def __init__(self, init_pos):
        self.clean_image_0 = pg.image.load(join('assets', join('Ships', 'Main Ship Full health.png')))
        self.clean_image_1 = pg.image.load(join('assets', join('Ships', 'Main Ship Slight damage.png')))
        self.clean_image_2 = pg.image.load(join('assets', join('Ships', 'Main Ship Damaged.png')))
        self.clean_image_3 = pg.image.load(join('assets', join('Ships', 'Main Ship Very damaged.png')))
        self.image = self.clean_image_0
        self.direction = Vec(rd.randint(-10, 10), rd.randint(-10, 10)).normalize()
        self.pos = init_pos
        self.vel = Vec(0, 0)
        self.acc = Vec(0, 0)
        self.acc_lim = 0.5
        self.life_points = 100

    def update(self):
        self.acc = Vec(0, 0)
        keys = pg.key.get_pressed()

        # handle direction
        if keys[pg.K_LEFT]:
            self.direction = self.direction.rotate(-5).normalize()
        if keys[pg.K_RIGHT]:
            self.direction = self.direction.rotate(+5).normalize()

        # handle border collitions
        if self.pos.x < 0:
            self.pos.x = 0
            self.vel.x *= -1
            self.direction.x *= -1
            self.life_points -= 1
        if self.pos.x > WIDTH:
            self.pos.x = WIDTH
            self.vel.x *= -1
            self.direction.x *= -1
            self.life_points -= 1
        if self.pos.y < 0:
            self.pos.y = 0
            self.vel.y *= -1
            self.direction.y *= -1
            self.life_points -= 1
        if self.pos.y > HEIGHT:
            self.pos.y = HEIGHT
            self.vel.y *= -1
            self.direction.y *= -1
            self.life_points -= 1

        # handle movement
        if keys[pg.K_UP]:
            self.acc += self.direction * self.acc_lim
        if keys[pg.K_DOWN]:
            self.acc += self.vel * FRICTION * 2
        else:
            self.acc += self.vel * FRICTION

        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        # Change ship appearance
        if self.life_points > 80:
            self.image = pg.transform.rotate(self.clean_image_0, self.direction.angle_to(Vec(0, -1)))
        elif self.life_points <= 80 and  self.life_points > 50:
            self.image = pg.transform.rotate(self.clean_image_1, self.direction.angle_to(Vec(0, -1)))
        elif self.life_points <= 50 and  self.life_points > 20:
            self.image = pg.transform.rotate(self.clean_image_2, self.direction.angle_to(Vec(0, -1)))
        else:
            self.image = pg.transform.rotate(self.clean_image_3, self.direction.angle_to(Vec(0, -1)))

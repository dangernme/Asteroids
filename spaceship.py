from os.path import join
import random
import pygame as pg
from settings import *
from movable import Movable
Vec = pg.math.Vector2

class Spaceship(Movable):
    def __init__(self, x_pos, y_pos):
        super().__init__(x_pos, y_pos, join('Ships', 'Main Ship Full health.png'))

        self.life_points = random.randint(80, 100)
        self.attack_points = random.randint(1, 20)
        self.speed = random.randint(1,7)
        self.armor = random.randint(80, 100)

    def update(self):
        self.acc = Vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_UP]:
            self.acc.y = -PLAYER_ACC
        if keys[pg.K_DOWN]:
            self.acc.y = PLAYER_ACC

        if keys[pg.K_LEFT]:
            self.orientation += 2
        if keys[pg.K_RIGHT]:
            self.orientation -= 2
        self.image, _ = self.rotate(self.clean_image, self.orientation, self.pos)

        self.acc += self.vel * PLAYER_FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

from os.path import join
import random as rd
import pygame as pg
from settings import *
from movable import Movable
from rocket import Rocket
Vec = pg.math.Vector2


class Spaceship(Movable):
    def __init__(self, init_pos):
        super().__init__(init_pos, Vec(rd.randint(1, 10), rd.randint(1, 10)).normalize(), 0.5)
        self.window = pg.display.get_surface()
        self.clean_image_0 = pg.image.load(
            join('assets', join('Ships', 'Main Ship Full health.png')))
        self.clean_image_1 = pg.image.load(
            join('assets', join('Ships', 'Main Ship Slight damage.png')))
        self.clean_image_2 = pg.image.load(
            join('assets', join('Ships', 'Main Ship Damaged.png')))
        self.clean_image_3 = pg.image.load(
            join('assets', join('Ships', 'Main Ship Very damaged.png')))
        self.image = self.clean_image_0
        self.health = 100
        self.rockets = 50

    def update_ship_image(self):
        if self.health > 80:
            self.image = pg.transform.rotate(
                self.clean_image_0, self.direction.angle_to(Vec(0, -1)))
        elif self.health <= 80 and self.health > 50:
            self.image = pg.transform.rotate(
                self.clean_image_1, self.direction.angle_to(Vec(0, -1)))
        elif self.health <= 50 and self.health > 20:
            self.image = pg.transform.rotate(
                self.clean_image_2, self.direction.angle_to(Vec(0, -1)))
        else:
            self.image = pg.transform.rotate(
                self.clean_image_3, self.direction.angle_to(Vec(0, -1)))

    def handle_border_collition(self):
        if self.pos.x < TEXT_WIDTH:
            self.pos.x = TEXT_WIDTH
            self.vel.x *= -1
            self.direction.x *= -1
            self.health -= 1
        if self.pos.x > WIDTH:
            self.pos.x = WIDTH
            self.vel.x *= -1
            self.direction.x *= -1
            self.health -= 1
        if self.pos.y < 0:
            self.pos.y = 0
            self.vel.y *= -1
            self.direction.y *= -1
            self.health -= 1
        if self.pos.y > HEIGHT:
            self.pos.y = HEIGHT
            self.vel.y *= -1
            self.direction.y *= -1
            self.health -= 1

    def fire(self):
        if self.rockets > 0:
            self.rockets -= 1
            start_pos = Vec(self.pos.x, self.pos.y - int(self.image.get_height() / 2))
            # start_pos = Vec(self.pos.x - int(self.image.get_width() / 2), self.pos.y - int(self.image.get_height() / 2))
            return Rocket(start_pos , self.direction.copy(), self.acc_lim * 0.001)

    def update(self):
        self.acc = Vec(0, 0)
        keys = pg.key.get_pressed()

        # handle direction
        if keys[pg.K_LEFT]:
            self.direction = self.direction.rotate(-5).normalize()
        if keys[pg.K_RIGHT]:
            self.direction = self.direction.rotate(+5).normalize()

        # handle movement
        if keys[pg.K_UP]:
            self.acc += self.direction * self.acc_lim
        if keys[pg.K_DOWN]:
            self.acc += self.vel * FRICTION * 2
        else:
            self.acc += self.vel * FRICTION

        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.acc_lim = self.health / 200
        self.handle_border_collition()
        self.update_ship_image()

    def draw(self):
        self.window.blit(self.image, (self.pos.x - int(self.image.get_width() / 2),
                         self.pos.y - int(self.image.get_height() / 2)))
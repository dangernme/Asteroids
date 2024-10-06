from os.path import join
import random as rd
import pygame as pg
from settings import *
Vec = pg.math.Vector2

class Spaceship(pg.sprite.Sprite):
    def __init__(self, init_pos):
        super().__init__()
        self.images = [pg.image.load(join('assets', 'Ships', 'Ship Full health.png')).convert_alpha(),
                       pg.image.load(join('assets', 'Ships', 'Ship Slight damage.png')).convert_alpha(),
                       pg.image.load(join('assets', 'Ships', 'Ship Damaged.png')).convert_alpha(),
                       pg.image.load(join('assets', 'Ships', 'Ship Very damaged.png')).convert_alpha()]

        scale_factor = 1.4
        for index, img in enumerate(self.images.copy()):
            new_width = int(img.get_width() * scale_factor)
            new_height = int(img.get_height() * scale_factor)
            self.images[index] = pg.transform.scale(img, (new_width, new_height))

        self.image = self.images[0]
        self.health = 100
        self.rockets_amount = 50
        self.speed = 0.7
        self.acc = Vec(0, 0)
        if pg.joystick.get_count() == 1:
            self.gamepad = pg.joystick.Joystick(0)
            self.gamepad.init()

        self.rect = self.image.get_rect()
        self.pos = init_pos
        self.rect.topleft = (self.pos.x, self.pos.y)
        self.points = 0
        self.vel = Vec(0, 0)
        self.direction = Vec(rd.randint(-10, 10), rd.randint(1, 10)).normalize()

    def select_ship_img(self):
        ship_count = 0

        if self.health > 80:
            ship_count = 0
        elif self.health <= 80 and self.health > 50:
            ship_count = 1
        elif self.health <= 50 and self.health > 20:
            ship_count = 2
        else:
            ship_count = 3

        return ship_count

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

    def update(self):
        self.acc = Vec(0, 0)
        keys = pg.key.get_pressed()

        if pg.joystick.get_count() == 1:
            axis_x = self.gamepad.get_axis(0)
            axis_y = self.gamepad.get_axis(1)
        else:
            axis_x = 0
            axis_y = 0

        # handle direction
        if keys[pg.K_LEFT] or axis_x < -0.5:
            self.direction = self.direction.rotate(-3).normalize()
        if keys[pg.K_RIGHT] or axis_x > 0.5:
            self.direction = self.direction.rotate(+3).normalize()

        # handle movement
        if keys[pg.K_UP] or axis_y < -0.5:
            self.acc += self.direction * self.speed
        if keys[pg.K_DOWN] or axis_y > 0.5:
            self.acc += self.vel * FRICTION * 2
        else:
            self.acc += self.vel * FRICTION

        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.handle_border_collition()
        self.speed = self.health / 200

        self.image = pg.transform.rotate(self.images[self.select_ship_img()], self.direction.angle_to(Vec(0, -1)))
        mask = self.image.get_bounding_rect()
        self.image = self.image.subsurface(mask).copy()
        self.rect = self.image.get_rect(center=self.pos)

        self.health = max(self.health, 0)

    def draw(self, surface):
        surface.blit(self.image, (self.pos.x - self.image.get_width() // 2, self.pos.y - self.image.get_height() // 2))
        if DEBUG_MODE:
            pg.draw.rect(surface, (255, 0, 0), self.rect, 2)

        if DIRECTION_LASER:
            pg.draw.line(surface, RED, self.pos, self.direction * 20000, 1)

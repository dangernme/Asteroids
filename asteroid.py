from os.path import join
import random as rd
import pygame as pg
from settings import *
from movable import Movable
Vec = pg.math.Vector2

class Asteroid(Movable):
    def __init__(self, init_pos):
        super().__init__(init_pos, Vec(rd.randint(1, 10), rd.randint(1, 10)).normalize())
        self.speed = 2
        path = join('assets', 'asteroids', 'medium')
        self.images = [pg.image.load(join(path, "a10000.png")),
                       pg.image.load(join(path, "a10001.png")),
                       pg.image.load(join(path, "a10002.png")),
                       pg.image.load(join(path, "a10003.png")),
                       pg.image.load(join(path, "a10004.png")),
                       pg.image.load(join(path, "a10005.png")),
                       pg.image.load(join(path, "a10006.png")),
                       pg.image.load(join(path, "a10007.png")),
                       pg.image.load(join(path, "a10008.png")),
                       pg.image.load(join(path, "a10009.png")),
                       pg.image.load(join(path, "a10010.png")),
                       pg.image.load(join(path, "a10011.png")),
                       pg.image.load(join(path, "a10012.png")),
                       pg.image.load(join(path, "a10013.png")),
                       pg.image.load(join(path, "a10014.png")),
                       pg.image.load(join(path, "a10015.png"))]
        self.animation_count = 0.0
        self.rect = self.images[0].get_rect(x=self.pos.x, y=self.pos.y)
        
    def update(self):
        self.pos += self.speed * self.direction.normalize()

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
    
    def draw(self):
        self.window.blit(self.images[int(self.animation_count) % 15], self.pos)
        self.rect = self.images[int(self.animation_count) % 15].get_rect(x=self.pos.x, y=self.pos.y)
        self.animation_count += 0.1
        if SHOW_POSITIONS:
            pg.draw.circle(self.window, TEXT_COLOR_RED, self.pos, 3)
            pg.draw.circle(self.window, TEXT_COLOR_RED, self.rect.center, 3)
            pg.draw.circle(self.window, TEXT_COLOR_RED, self.rect.bottomright, 3)
        
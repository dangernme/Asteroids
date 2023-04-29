import pygame as pg
import random as rd
from os.path import join
from settings import *
Vec = pg.math.Vector2

class Medi(pg.sprite.Sprite):
    def __init__(self, init_pos):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(join('assets', 'hearts', 'heart 16x16.png'))
        self.pos = init_pos
        self.window = pg.display.get_surface()
        self.healh = rd.randint(1, 10)
        self.radius = 15
        self.rect = self.image.get_rect(x=self.pos.x, y=self.pos.y)
        
    def draw(self):
        if DEBUG_MODE:
            pg.draw.circle(self.window, GREEN, self.pos, 3)
            pg.draw.circle(self.window, RED, self.rect.center, self.radius)
            pg.draw.circle(self.window, BLUE, self.rect.bottomright, 3)
            
        self.window.blit(self.image, self.pos)
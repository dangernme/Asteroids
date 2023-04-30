import pygame as pg
import random as rd
from os.path import join
from settings import *

class Collectable_Abstract(pg.sprite.Sprite):
    def __init__(self, init_pos):
        pg.sprite.Sprite.__init__(self)
        self.pos = init_pos
        self.window = pg.display.get_surface()
        
    def draw(self):
        if DEBUG_MODE:
            pg.draw.circle(self.window, GREEN, self.pos, 3)
            pg.draw.circle(self.window, RED, self.rect.center, self.radius)
            pg.draw.circle(self.window, BLUE, self.rect.bottomright, 3)
            
        self.window.blit(self.image, self.pos)
        
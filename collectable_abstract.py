import pygame as pg
from settings import *

class CollectableAbstract(pg.sprite.Sprite):
    def __init__(self, init_pos):
        pg.sprite.Sprite.__init__(self)
        self.pos = init_pos

    def draw(self, surface):
        surface.blit(self.image, self.pos)

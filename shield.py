from os.path import join
import pygame as pg
from settings import *

class Shield(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load(join('assets', 'Ships', 'Shields', 'RoundShield.png')).convert_alpha()
        self.frame = 0
        self.current_image = self.image.subsurface(pg.Rect(0, 0, 64, 64))
        self.rect = self.current_image.get_rect()
        self.rect.center = (TEXT_WIDTH + (GAME_WIDTH // 2), HEIGHT // 2)
        self.last_update = pg.time.get_ticks()

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > FPS * 2:
            self.last_update = now
            self.frame = (self.frame) % 11
            x = self.frame * 64
            self.current_image = self.image.subsurface(pg.Rect(x, 0, 64, 64))
            self.rect = self.current_image.get_rect()

            mask = self.current_image.get_bounding_rect()
            self.current_image = self.current_image.subsurface(mask).copy()
            self.rect = self.current_image.get_rect(center=self.rect.center)

    def draw(self, surface):
        surface.blit(self.current_image, self.rect)
        if DEBUG_MODE:
            pg.draw.rect(surface, (255, 0, 0), self.rect, 2)
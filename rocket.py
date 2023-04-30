from os.path import join
import pygame as pg
import movable
from settings import *
Vec = pg.math.Vector2

class Rocket(movable.Movable):
    def __init__(self, init_pos, init_dir):
        super().__init__(init_pos, init_dir)
        self.image = pg.image.load(join('assets', 'Ships', 'Weapons', 'Rocket.png'))
        self.image = pg.transform.rotate(self.image, self.direction.angle_to(Vec(0, -1)))
        self.rect = self.image.get_rect(x=self.pos.x, y=self.pos.y)
        self.pos -= (self.rect.width // 2, self.rect.height // 2) # Correct start position of rocket to ships center
        self.speed = 10
        self.radius = 4

    def draw(self):
        self.rect = self.image.get_rect(x=self.pos.x, y = self.pos.y)
        self.window.blit(self.image, self.pos)
        
        if DEBUG_MODE:
            pg.draw.circle(self.window, GREEN, self.pos, 3)
            pg.draw.circle(self.window, RED, self.rect.center, self.radius)
            pg.draw.circle(self.window, BLUE, self.rect.bottomright, 3)
                
    def update(self):
        self.pos += self.speed * self.direction.normalize()    
        
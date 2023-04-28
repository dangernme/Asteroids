from os.path import join
import pygame as pg
from movable import Movable
from settings import *
Vec = pg.math.Vector2


class Rocket(Movable):
    def __init__(self, init_pos, init_dir):
        super().__init__(init_pos, init_dir)
        self.rocket_tiles = [pg.image.load(join('assets', 'Ships', 'Main ship weapon - Projectile - Rocket_0.png')),
                    pg.image.load(join('assets', 'Ships', 'Main ship weapon - Projectile - Rocket_1.png')),
                    pg.image.load(join('assets', 'Ships', 'Main ship weapon - Projectile - Rocket_2.png'))]
        self.images = []
        self.images.append(pg.transform.rotate(self.rocket_tiles[0], self.direction.angle_to(Vec(0, -1))))
        self.images.append(pg.transform.rotate(self.rocket_tiles[1], self.direction.angle_to(Vec(0, -1))))
        self.images.append(pg.transform.rotate(self.rocket_tiles[2], self.direction.angle_to(Vec(0, -1))))
        self.rect = self.rocket_tiles[0].get_rect(x=self.pos.x, y=self.pos.y)
        self.count = 0
        self.pos -= (self.rect.width // 2, self.rect.height // 2) # Correct start position of rocket to ships center
        self.interval = 0
        self.speed = 10
        self.radius = 4

    def draw(self):
        if self.interval == 10:
            self.count += 1
            self.interval = 0
    
        self.interval += 1
        
        index = self.count % 3
        image = self.images[index]
        self.rect = self.rocket_tiles[index].get_rect(x=self.pos.x, y = self.pos.y)
        
        self.window.blit(image, self.pos)
        if DEBUG_MODE:
            pg.draw.circle(self.window, GREEN, self.pos, 3)
            pg.draw.circle(self.window, RED, self.rect.center, self.radius)
            pg.draw.circle(self.window, BLUE, self.rect.bottomright, 3)
                
    def update(self):
        self.pos += self.speed * self.direction.normalize()    
        
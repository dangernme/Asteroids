from os.path import join
import pygame as pg
from movable import Movable
from settings import *
Vec = pg.math.Vector2


class Rocket(Movable):
    def __init__(self, init_pos, init_dir, init_acc_lim):
        super().__init__(init_pos, init_dir, init_acc_lim)
        rocket_tiles = [pg.image.load(join('assets', 'Ships', 'Main ship weapon - Projectile - Rocket_0.png')),
                    pg.image.load(join('assets', 'Ships', 'Main ship weapon - Projectile - Rocket_1.png')),
                    pg.image.load(join('assets', 'Ships', 'Main ship weapon - Projectile - Rocket_2.png'))]
        self.images = []
        self.images.append(pg.transform.rotate(rocket_tiles[0], self.direction.angle_to(Vec(0, -1))))
        self.images.append(pg.transform.rotate(rocket_tiles[1], self.direction.angle_to(Vec(0, -1))))
        self.images.append(pg.transform.rotate(rocket_tiles[2], self.direction.angle_to(Vec(0, -1))))
        self.out_of_limits = False
        self.count = 0
        self.rect = self.images[0].get_rect(center= (self.pos.x, self.pos.y))
        self.interval = 0
        self.pos -= self.rect.center
        self.acc += self.direction.normalize()

    def draw(self):
        if self.interval == 10:
            self.count += 1
            self.interval = 0
    
        self.interval += 1
        
        index = self.count % 3
        image = self.images[index]
        self.rect = image.get_rect(center= (self.pos.x, self.pos.y))
        
        self.window.blit(image, (self.pos.x, self.pos.y))
                
    def update(self):
        self.acc += self.direction * self.acc_lim
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
                
        if self.pos.x < TEXT_WIDTH or self.pos.x > WIDTH or self.pos.y < 0 or self.pos.y > HEIGHT:
            self.out_of_limits = True      
        
        


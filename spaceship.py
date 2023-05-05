from os.path import join
import random as rd
import pygame as pg
import logging
from settings import *
from movable import Movable
from rocket import Rocket
Vec = pg.math.Vector2


class Spaceship(Movable):
    def __init__(self, init_pos):
        super().__init__(init_pos, Vec(rd.randint(1, 10), rd.randint(1, 10)).normalize())
        self.clean_images = [pg.image.load(join('assets', join('Ships', 'Ship Full health.png'))),
                            pg.image.load(join('assets', join('Ships', 'Ship Slight damage.png'))),
                            pg.image.load(join('assets', join('Ships', 'Ship Damaged.png'))),
                            pg.image.load(join('assets', join('Ships', 'Ship Very damaged.png')))]
        self.image = self.clean_images[0]
        self.health = 100
        self.rockets = 50
        self.speed = 0.5
        self.acc = Vec(0, 0)
        self.active_rockets = []
        if pg.joystick.get_count() == 1:
            self.gamepad = pg.joystick.Joystick(0)
            self.gamepad.init()
        self.rect = self.image.get_rect(x=self.pos.x, y=self.pos.y)
        self.radius = 15
        self.points = 0
        self.vel = Vec(0, 0)
        pg.mixer.init()
        pg.mixer.fadeout(10)
        self.pew_sound = pg.mixer.Sound(join('assets', 'Sounds', "pew.wav"))
        self.pew_sound.set_volume(0.1)
        logging.debug(f"Ship created on {init_pos}")

    def select_ship_image(self):
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
            logging.debug(f"Border collition at {self.pos}")
            self.pos.x = TEXT_WIDTH
            self.vel.x *= -1
            self.direction.x *= -1
            self.health -= 1
        if self.pos.x > WIDTH:
            logging.debug(f"Border collition at {self.pos}")
            self.pos.x = WIDTH
            self.vel.x *= -1
            self.direction.x *= -1
            self.health -= 1
        if self.pos.y < 0:
            logging.debug(f"Border collition at {self.pos}")
            self.pos.y = 0
            self.vel.y *= -1
            self.direction.y *= -1
            self.health -= 1
        if self.pos.y > HEIGHT:
            logging.debug(f"Border collition at {self.pos}")
            self.pos.y = HEIGHT
            self.vel.y *= -1
            self.direction.y *= -1
            self.health -= 1

    def fire(self):
        logging.info("Rocket started")
        if self.rockets > 0 and len(self.active_rockets) < MAX_ACTIVE_ROCKETS: 
            self.rockets -= 1
            self.pew_sound.play()
            self.active_rockets.append(Rocket(self.pos.copy(), self.direction.copy()))

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
        if not DEBUG_MODE:
            self.speed = self.health / 200
            
        self.image = pg.transform.rotate(self.clean_images[self.select_ship_image()], self.direction.angle_to(Vec(0, -1)))
        self.rect = self.image.get_rect(center=self.pos)

        
        if self.health <= 0:
            logging.info(f"Game over due to health == 0")
            self.health = 0

    def draw(self):
        if DEBUG_MODE:
            pg.draw.circle(self.window, GREEN, self.pos, 3)
            pg.draw.circle(self.window, RED, self.rect.center, self.radius)
            pg.draw.circle(self.window, BLUE, self.rect.bottomright, 3)
        self.window.blit(self.image, (self.pos.x - self.image.get_width() // 2, self.pos.y - self.image.get_height() // 2))
        
        if DIRECTION_LASER:
            pg.draw.line(self.window, RED, self.pos, self.direction * 20000, 1)

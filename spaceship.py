from os.path import join
import random as rd
import pygame as pg
from settings import *
Vec = pg.math.Vector2

class Spaceship(pg.sprite.Sprite):
    def __init__(self):
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
        self.rockets_amount = MAX_SHIP_ROCKETS
        self.speed = 0.7
        self.acceleration = Vec(0, 0)
        self.rect = self.image.get_rect()
        self.rect.center = (TEXT_WIDTH + (GAME_WIDTH // 2), HEIGHT // 2)

        self.points = 0
        self.velocity = Vec(0, 0)
        self.direction = Vec(rd.randint(-10, 10), rd.randint(1, 10)).normalize()

    def activate_shield(self):
        pass
    def deactivate_shield(self):
        pass

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
        if self.rect.left < TEXT_WIDTH:
            self.rect.x = TEXT_WIDTH
            self.velocity.x *= -1
            self.direction.x *= -1
            self.health -= 1
        if self.rect.right > WIDTH:
            self.rect.x = WIDTH - self.rect.width
            self.velocity.x *= -1
            self.direction.x *= -1
            self.health -= 1
        if self.rect.top < 0:
            self.rect.y = 0
            self.velocity.y *= -1
            self.direction.y *= -1
            self.health -= 1
        if self.rect.bottom > HEIGHT:
            self.rect.y = HEIGHT - self.rect.height
            self.velocity.y *= -1
            self.direction.y *= -1
            self.health -= 1

    def turn_left(self):
        self.direction = self.direction.rotate(-3).normalize()

    def turn_right(self):
        self.direction = self.direction.rotate(+3).normalize()

    def accelerate(self):
        self.acceleration += self.direction * self.speed

    def decelerate(self):
        self.acceleration += self.velocity * FRICTION

    def brake(self):
        self.acceleration += self.velocity * FRICTION * 2

    def update(self):
        self.handle_border_collition()
        self.speed = self.health / 200

        self.velocity += self.acceleration
        self.rect.x += self.velocity.x + 0.5 * self.acceleration.x
        self.rect.y += self.velocity.y + 0.5 * self.acceleration.y

        self.image = pg.transform.rotate(self.images[self.select_ship_img()], self.direction.angle_to(Vec(0, -1)))
        mask = self.image.get_bounding_rect()
        self.image = self.image.subsurface(mask).copy()
        self.rect = self.image.get_rect(center=self.rect.center)

        self.health = max(self.health, 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        if DEBUG_MODE:
            pg.draw.rect(surface, (255, 0, 0), self.rect, 2)

        if DIRECTION_LASER:
            pg.draw.line(surface, RED, self.rect.center, self.direction * 20000, 1)

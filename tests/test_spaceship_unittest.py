import unittest
import pygame as pg
from settings import *
from spaceship import Spaceship
Vec = pg.math.Vector2

class TestSpaceship(unittest.TestCase):
    def setUp(self):
        pg.joystick.init()
        pg.init()
        self.screen = pg.display.set_mode(SIZE)
        self.ship = Spaceship()

    def test_ship_image_change(self):
        self.ship.health = 100
        self.assertEqual(self.ship.select_ship_img(), 0)
        self.ship.health = 81
        self.assertEqual(self.ship.select_ship_img(), 0)
        self.ship.health = 80
        self.assertEqual(self.ship.select_ship_img(), 1)
        self.ship.health = 51
        self.assertEqual(self.ship.select_ship_img(), 1)
        self.ship.health = 50
        self.assertEqual(self.ship.select_ship_img(), 2)
        self.ship.health = 21
        self.assertEqual(self.ship.select_ship_img(), 2)
        self.ship.health = 20
        self.assertEqual(self.ship.select_ship_img(), 3)

    def test_acceleration(self):
        self.ship.acceleration = Vec(0, 0)
        self.ship.accelerate()
        self.assertEqual(self.ship.acceleration, self.ship.direction * 0.7)

    def test_decceleration(self):
        self.ship.acceleration = Vec(2, 2)
        self.ship.velocity = Vec(2, 2)
        self.ship.decelerate()
        self.assertEqual(self.ship.acceleration, (Vec(2, 2) + self.ship.velocity *  FRICTION))

    def test_brake(self):
        self.ship.acceleration = Vec(2, 2)
        self.ship.velocity = Vec(2, 2)
        self.ship.brake()
        self.assertEqual(self.ship.acceleration, (Vec(2, 2) + self.ship.velocity *  FRICTION * 2))

    def test_turn_left(self):
        self.ship.direction = Vec(1, 0)
        self.ship.turn_left()
        self.assertEqual(self.ship.direction, Vec(1, 0).rotate(-3).normalize())

    def test_turn_right(self):
        self.ship.direction = Vec(1, 0)
        self.ship.turn_right()
        self.assertEqual(self.ship.direction, Vec(1, 0).rotate(+3).normalize())

    def test_border_collision_left(self):
        self.ship.shield_active = True
        self.ship.shield.rect = pg.Rect(TEXT_WIDTH - 1, HEIGHT // 2, 0, 0)
        self.ship.direction = Vec(-1, 0)
        self.ship.velocity = Vec(-1, 0)
        self.ship.handle_border_collition()
        self.assertEqual(self.ship.shield.rect.left, TEXT_WIDTH)
        self.assertEqual(self.ship.velocity.x, 1)
        self.assertEqual(self.ship.direction.x, 1)
        self.assertEqual(self.ship.health, 100)

        self.ship.shield_active = False
        self.ship.rect = pg.Rect(TEXT_WIDTH - 1, HEIGHT // 2, 0, 0)
        self.ship.direction = Vec(-1, 0)
        self.ship.velocity = Vec(-1, 0)
        self.ship.handle_border_collition()
        self.assertEqual(self.ship.rect.left, TEXT_WIDTH)
        self.assertEqual(self.ship.velocity.x, 1)
        self.assertEqual(self.ship.direction.x, 1)
        self.assertEqual(self.ship.health, 99)

    def test_border_collision_right(self):
        self.ship.shield_active = True
        self.ship.shield.rect = pg.Rect(WIDTH + 1, HEIGHT // 2, 0, 0)
        self.ship.direction = Vec(1, 0)
        self.ship.velocity = Vec(1, 0)
        self.ship.handle_border_collition()
        self.assertEqual(self.ship.shield.rect.right, WIDTH)
        self.assertEqual(self.ship.velocity.x, -1)
        self.assertEqual(self.ship.direction.x, -1)
        self.assertEqual(self.ship.health, 100)

        self.ship.shield_active = False
        self.ship.rect = pg.Rect(WIDTH + 1, HEIGHT // 2, 0, 0)
        self.ship.direction = Vec(1, 0)
        self.ship.velocity = Vec(1, 0)
        self.ship.handle_border_collition()
        self.assertEqual(self.ship.rect.right, WIDTH)
        self.assertEqual(self.ship.velocity.x, -1)
        self.assertEqual(self.ship.direction.x, -1)
        self.assertEqual(self.ship.health, 99)

    def test_border_collision_bottom(self):
        self.ship.shield_active = True
        self.ship.shield.rect = pg.Rect(WIDTH // 2, HEIGHT + 1, 0, 0)
        self.ship.direction = Vec(0, 1)
        self.ship.velocity = Vec(0, 1)
        self.ship.handle_border_collition()
        self.assertEqual(self.ship.shield.rect.bottom, HEIGHT)
        self.assertEqual(self.ship.velocity.y, -1)
        self.assertEqual(self.ship.direction.y, -1)
        self.assertEqual(self.ship.health, 100)

        self.ship.shield_active = False
        self.ship.rect = pg.Rect(WIDTH // 2, HEIGHT + 1, 0, 0)
        self.ship.direction = Vec(0, 1)
        self.ship.velocity = Vec(0, 1)
        self.ship.handle_border_collition()
        self.assertEqual(self.ship.rect.bottom, HEIGHT)
        self.assertEqual(self.ship.velocity.y, -1)
        self.assertEqual(self.ship.direction.y, -1)
        self.assertEqual(self.ship.health, 99)

    def test_border_collision_top(self):
        self.ship.shield_active = True
        self.ship.shield.rect = pg.Rect(WIDTH // 2, -1 , 0, 0)
        self.ship.direction = Vec(0, -1)
        self.ship.velocity = Vec(0, -1)
        self.ship.handle_border_collition()
        self.assertEqual(self.ship.shield.rect.top, 0)
        self.assertEqual(self.ship.velocity.y, 1)
        self.assertEqual(self.ship.direction.y, 1)
        self.assertEqual(self.ship.health, 100)

        self.ship.shield_active = False
        self.ship.rect = pg.Rect(WIDTH // 2, -1 , 0, 0)
        self.ship.direction = Vec(0, -1)
        self.ship.velocity = Vec(0, -1)
        self.ship.handle_border_collition()
        self.assertEqual(self.ship.rect.top, 0)
        self.assertEqual(self.ship.velocity.y, 1)
        self.assertEqual(self.ship.direction.y, 1)
        self.assertEqual(self.ship.health, 99)

if __name__ == '__main__':
    unittest.main()

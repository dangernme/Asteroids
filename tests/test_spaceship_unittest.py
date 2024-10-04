import unittest
import pygame as pg
import settings
from spaceship import Spaceship
Vec = pg.math.Vector2

class TestSpaceship(unittest.TestCase):
    def setUp(self):
        pg.joystick.init()
        self.ship = Spaceship(Vec(settings.WIDTH //2,settings.HEIGHT //2))

    def test_fire(self):
        self.ship.rockets_amount = 5
        self.ship.fire()
        self.assertEqual(self.ship.rockets_amount, 4)
        self.assertEqual(len(self.ship.active_rockets), 1)

    def test_collition_left(self):
        self.ship.health = 10
        self.ship.direction = Vec(-1,0)

        self.ship.pos.x = settings.TEXT_WIDTH - 10
        self.ship.pos.y = settings.HEIGHT // 2

        self.ship.handle_border_collition()

        self.assertEqual(self.ship.health, 9)
        self.assertEqual(self.ship.direction, Vec(1,0))

    def test_collition_right(self):
        self.ship.health = 10
        self.ship.direction = Vec(1,0)

        self.ship.pos.x = settings.WIDTH + 1
        self.ship.pos.y = settings.HEIGHT // 2

        self.ship.handle_border_collition()

        self.assertEqual(self.ship.health, 9)
        self.assertEqual(self.ship.direction, Vec(-1,0))

    def test_collition_top(self):
        self.ship.health = 10
        self.ship.direction = Vec(0,-1)

        self.ship.pos.x = settings.WIDTH // 2
        self.ship.pos.y = -1

        self.ship.handle_border_collition()

        self.assertEqual(self.ship.health, 9)
        self.assertEqual(self.ship.direction, Vec(0,1))

    def test_collition_bottom(self):
        self.ship.health = 10
        self.ship.direction = Vec(0, 1)

        self.ship.pos.x = settings.WIDTH // 2
        self.ship.pos.y = settings.HEIGHT +1

        self.ship.handle_border_collition()

        self.assertEqual(self.ship.health, 9)
        self.assertEqual(self.ship.direction, Vec(0, -1))

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


if __name__ == '__main__':
    unittest.main()

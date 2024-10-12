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

if __name__ == '__main__':
    unittest.main()

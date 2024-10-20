import random as rd
import pygame as pg
from settings import *
from asteroids.asteroid_a1 import AsteroidA1
from asteroids.asteroid_a3 import AsteroidA3
from asteroids.asteroid_d3 import AsteroidD3
Vec = pg.math.Vector2

class AsteroidFactory:
    @staticmethod
    def create_asteroid(asteroid):
        random_start = rd.randint(0,4)
        pos = None
        if random_start == 0: # left
            pos = Vec(0, rd.randint(0, HEIGHT))
        elif random_start == 1: # top
            pos = Vec(rd.randint(TEXT_WIDTH, WIDTH), 0)
        elif random_start == 2: #right
            pos = Vec(WIDTH, rd.randint(0, HEIGHT))
        else: #bottom
            pos = Vec(rd.randint(TEXT_WIDTH, WIDTH), HEIGHT)

        if isinstance(asteroid, AsteroidA1):
            return AsteroidA1(pos)
        if isinstance(asteroid, AsteroidA3):
            return AsteroidA3(pos)
        if isinstance(asteroid, AsteroidD3):
            return AsteroidD3(pos)
        print("Invalid asteroid type")
        return None

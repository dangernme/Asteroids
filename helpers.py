from asteroids.asteroid_a1 import AsteroidA1
from asteroids.asteroid_a3 import AsteroidA3
from asteroids.asteroid_d3 import AsteroidD3

def generate_asteroid(asteroid, pos):
    if isinstance(asteroid, AsteroidA1):
        return AsteroidA1(pos)
    if isinstance(asteroid, AsteroidA3):
        return AsteroidA3(pos)
    if isinstance(asteroid, AsteroidD3):
        return AsteroidD3(pos)
    print("Invalid asteroid type")
    return None

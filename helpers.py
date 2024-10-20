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

def scale_range (_input, old_min, old_max, new_min, new_max):
    return ( (_input - old_min) / (old_max - old_min) ) * (new_max - new_min) + new_min

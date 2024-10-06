from asteroid_1 import Asteroid1
from asteroid_3 import Asteroid3

def generate_asteroid(asteroid, pos):
    if isinstance(asteroid, Asteroid1):
        return Asteroid1(pos)
    if isinstance(asteroid, Asteroid3):
        return Asteroid3(pos)
    print("Invalid asteroid type")
    return None

def scale_range (_input, old_min, old_max, new_min, new_max):
    return ( (_input - old_min) / (old_max - old_min) ) * (new_max - new_min) + new_min

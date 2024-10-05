import asteroid_small
import asteroid_medium

def generate_asteroid(asteroid, pos):
    if isinstance(asteroid, asteroid_medium.Asteroid1):
        return asteroid_medium.Asteroid1(pos)
    if isinstance(asteroid, asteroid_small.Asteroid3):
        return asteroid_small.Asteroid3(pos)
    print("Invalid asteroid type")
    return None

def scale_range (_input, old_min, old_max, new_min, new_max):
    return ( (_input - old_min) / (old_max - old_min) ) * (new_max - new_min) + new_min

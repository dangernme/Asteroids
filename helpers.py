import logging
import asteroid_small
import asteroid_medium

def generate_asteroid(asteroid, pos):
    logging.info('Asteroid respawn at %s', pos)
    if isinstance(asteroid, asteroid_medium.AsteroidMedium):
        return asteroid_medium.AsteroidMedium(pos)
    if isinstance(asteroid, asteroid_small.AsteroidSmall):
        return asteroid_small.AsteroidSmall(pos)
    print("Invalid asteroid type")
    return None

def scale_range (_input, old_min, old_max, new_min, new_max):
    return ( (_input - old_min) / (old_max - old_min) ) * (new_max - new_min) + new_min

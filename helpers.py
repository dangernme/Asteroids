import asteroid_small
import asteroid_medium
import logging

def generate_asteroid(asteroid, pos):
    logging.info(f"Asteroid respawn at {pos}")
    if isinstance(asteroid, asteroid_medium.Asteroid_Medium):
        return asteroid_medium.Asteroid_Medium(pos)
    elif isinstance(asteroid, asteroid_small.Asteroid_Small):
        return asteroid_small.Asteroid_Small(pos)
    else:
        print("Invalid asteroid type")


def scale_range (input, old_min, old_max, new_min, new_max):
    return ( (input - old_min) / (old_max - old_min) ) * (new_max - new_min) + new_min
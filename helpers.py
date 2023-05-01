def scale_range (input, old_min, old_max, new_min, new_max):
    return ( (input - old_min) / (old_max - old_min) ) * (new_max - new_min) + new_min
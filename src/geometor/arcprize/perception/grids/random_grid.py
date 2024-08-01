import random
import numpy as np

def generate_grid(width, height, symbol_set):
    return np.random.choice(list(symbol_set), size=(width, height))


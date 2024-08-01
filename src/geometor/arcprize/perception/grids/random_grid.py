import random
import numpy as np

def generate_grid(size, symbol_set):
    return np.random.choice(list(symbol_set), size=(size, size))


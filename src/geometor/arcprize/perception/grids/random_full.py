import random
import numpy as np


def generate_grid(width, height, symbol_set):
    return np.random.choice(list(symbol_set), size=(width, height))


if __name__ == "__main__":
    from geometor.arcprize.perception.symbols import SYMBOL_SETS

    width, height = 5, 5
    symbol_set = SYMBOL_SETS["digits"]

    grid = generate_grid(width, height, symbol_set)
    print("Generated sparse grid:")
    print(grid)

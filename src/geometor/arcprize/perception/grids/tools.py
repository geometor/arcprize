import numpy as np
import random

def rotate_grid(grid, direction):
    if direction == "none":
        return grid
    elif direction == "right":
        return np.rot90(grid, k=-1)
    elif direction == "left":
        return np.rot90(grid, k=1)
    elif direction == "full":
        return np.rot90(grid, k=2)
    else:
        raise ValueError("Invalid rotation direction")


def introduce_errors(grid, error_chance, max_errors, symbol_set):
    errors_introduced = 0
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if random.random() < error_chance and errors_introduced < max_errors:
                grid[i, j] = random.choice(list(symbol_set))
                errors_introduced += 1
                if errors_introduced == max_errors:
                    return grid
    return grid


def grid_to_string(grid, row_delimiter="\n", cell_delimiter=" "):
    return row_delimiter.join(
        cell_delimiter.join(str(cell) for cell in row) for row in grid
    )

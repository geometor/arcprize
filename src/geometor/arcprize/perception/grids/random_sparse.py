import random
import numpy as np


def generate_grid(width, height, symbol_set):
    # Convert symbol_set to a list and shuffle it
    symbols = list(symbol_set)
    random.shuffle(symbols)

    # Use the first symbol to fill the entire grid
    background_symbol = symbols.pop(0)
    grid = np.full((height, width), background_symbol)

    # Create a list of all cell addresses and shuffle it
    cell_addresses = [(x, y) for y in range(height) for x in range(width)]
    random.shuffle(cell_addresses)

    # Determine the number of cells to fill
    num_cells_to_fill = max(width, height)

    # Fill random cells with the remaining symbols
    for i in range(min(num_cells_to_fill, len(cell_addresses), len(symbols))):
        x, y = cell_addresses.pop()
        symbol = symbols[i % len(symbols)]  # Cycle through remaining symbols if needed
        grid[y, x] = symbol

    return grid


# Example usage
if __name__ == "__main__":
    from geometor.arcprize.perception.symbols import SYMBOL_SETS

    width, height = 5, 5
    symbol_set = SYMBOL_SETS["digits"]

    grid = generate_grid(width, height, symbol_set)
    print("Generated sparse grid:")
    print(grid)

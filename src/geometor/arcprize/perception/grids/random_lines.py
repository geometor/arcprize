import random
import numpy as np

def generate_grid(width, height, symbol_set):
    # Convert symbol_set to a list and shuffle it
    symbols = list(symbol_set)
    random.shuffle(symbols)
    
    # Use the first symbol to fill the entire grid
    background_symbol = symbols.pop(0)
    grid = np.full((height, width), background_symbol)
    
    # Determine the number of lines to draw (max of width or height, minus 1 if odd)
    num_lines = max(width, height)
    if num_lines % 2 != 0:
        num_lines -= 1
    
    # Create a list of available rows and columns, excluding the center if odd
    available_rows = list(range(height))
    available_cols = list(range(width))
    
    if height % 2 != 0:
        available_rows.remove(height // 2)
    if width % 2 != 0:
        available_cols.remove(width // 2)
    
    # Shuffle the available rows and columns
    random.shuffle(available_rows)
    random.shuffle(available_cols)
    
    # Draw lines
    for i in range(min(num_lines, len(symbols))):
        symbol = symbols[i]
        if random.choice([True, False]) and available_rows:  # Draw horizontal line
            row = available_rows.pop()
            grid[row, :] = symbol
        elif available_cols:  # Draw vertical line
            col = available_cols.pop()
            grid[:, col] = symbol
    
    return grid

# Example usage
if __name__ == "__main__":
    from geometor.arcprize.perception.symbols import SYMBOL_SETS
    
    width, height = 5, 5
    symbol_set = SYMBOL_SETS["digits"]
    
    grid = generate_grid(width, height, symbol_set)
    print("Generated line grid:")
    print(grid)

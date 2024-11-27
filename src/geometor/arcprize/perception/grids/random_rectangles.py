import random
import numpy as np

def generate_grid(width, height, symbol_set):
    # Convert symbol_set to a list and shuffle it
    symbols = list(symbol_set)
    random.shuffle(symbols)
    
    # Use the first symbol as the background
    background_symbol = symbols.pop(0)
    grid = np.full((height, width), background_symbol)
    
    # Determine the number of rectangles to draw
    num_rectangles = min(len(symbols), max(2, (width + height) // 4))
    
    for symbol in symbols[:num_rectangles]:
        # Determine rectangle size and position
        rect_width = random.randint(1, max(1, width // 2))
        rect_height = random.randint(1, max(1, height // 2))
        x = random.randint(0, width - rect_width)
        y = random.randint(0, height - rect_height)
        
        # Draw the rectangle
        grid[y:y+rect_height, x:x+rect_width] = symbol
    
    return grid

# Example usage
if __name__ == "__main__":
    from geometor.arcprize.perception.symbols import SYMBOL_SETS
    
    width, height = 7, 7
    symbol_set = SYMBOL_SETS["digits"]
    
    grid = generate_grid(width, height, symbol_set)
    print("Generated rectangle grid:")
    for row in grid:
        print(" ".join(row))

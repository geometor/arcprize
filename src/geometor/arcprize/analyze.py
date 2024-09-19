from typing import List, Dict, Tuple
from collections import Counter
from geometor.arcprize.model import Grid, ARCPuzzle

def analyze_colors(puzzle: ARCPuzzle) -> Dict[str, Dict[int, Tuple[int, int, int]]]:
    """
    Analyze color usage in input and output grids of a puzzle.
    
    Returns a dictionary with 'input' and 'output' keys, each containing
    a dictionary of color counts and their differences.
    """
    def count_colors(grid: Grid) -> Counter:
        return Counter(cell.value for row in grid.cells for cell in row)
    
    input_colors = count_colors(puzzle.input)
    output_colors = count_colors(puzzle.output)
    
    all_colors = set(input_colors.keys()).union(set(output_colors.keys()))
    
    result = {
        'input': {},
        'output': {},
        'diff': {}
    }
    
    for color in all_colors:
        input_count = input_colors[color]
        output_count = output_colors[color]
        diff = output_count - input_count
        
        result['input'][color] = input_count
        result['output'][color] = output_count
        result['diff'][color] = diff
    
    return result

def analyze_size(puzzle: ARCPuzzle) -> Dict[str, Dict[str, int]]:
    """
    Analyze size characteristics of input and output grids of a puzzle.
    
    Returns a dictionary with 'input', 'output', and 'diff' keys, each containing
    width, height, and area information.
    """
    result = {
        'input': {
            'width': puzzle.input.width,
            'height': puzzle.input.height,
            'area': puzzle.input.width * puzzle.input.height
        },
        'output': {
            'width': puzzle.output.width,
            'height': puzzle.output.height,
            'area': puzzle.output.width * puzzle.output.height
        }
    }
    
    result['diff'] = {
        'width': result['output']['width'] - result['input']['width'],
        'height': result['output']['height'] - result['input']['height'],
        'area': result['output']['area'] - result['input']['area']
    }
    
    return result

def find_symmetry(grid: Grid) -> List[str]:
    """
    Identify symmetries in a grid.
    
    Returns a list of identified symmetries ('horizontal', 'vertical', 'diagonal').
    """
    symmetries = []
    
    # Check horizontal symmetry
    if all(grid.cells[i] == grid.cells[-i-1] for i in range(grid.height // 2)):
        symmetries.append('horizontal')
    
    # Check vertical symmetry
    if all(row[i] == row[-i-1] for row in grid.cells for i in range(grid.width // 2)):
        symmetries.append('vertical')
    
    # Check diagonal symmetry (top-left to bottom-right)
    if grid.width == grid.height and all(grid.cells[i][j] == grid.cells[j][i] for i in range(grid.height) for j in range(i)):
        symmetries.append('diagonal')
    
    return symmetries

def find_patterns(grid: Grid) -> List[Dict[str, any]]:
    """
    Identify common patterns in a grid.
    
    Returns a list of identified patterns with their descriptions.
    """
    patterns = []
    
    # Check for solid rectangles
    for y in range(grid.height):
        for x in range(grid.width):
            for h in range(1, grid.height - y + 1):
                for w in range(1, grid.width - x + 1):
                    if all(grid.cells[y+i][x+j].value == grid.cells[y][x].value 
                           for i in range(h) for j in range(w)):
                        patterns.append({
                            'type': 'solid_rectangle',
                            'x': x,
                            'y': y,
                            'width': w,
                            'height': h,
                            'color': grid.cells[y][x].value
                        })
    
    # Add more pattern recognition logic here (e.g., gradients, repeating patterns)
    
    return patterns

def analyze_puzzle(puzzle: ARCPuzzle) -> Dict[str, any]:
    """
    Perform a comprehensive analysis of an ARC puzzle.
    
    Returns a dictionary containing various analysis results.
    """
    return {
        'colors': analyze_colors(puzzle),
        'size': analyze_size(puzzle),
        'input_symmetry': find_symmetry(puzzle.input),
        'output_symmetry': find_symmetry(puzzle.output),
        'input_patterns': find_patterns(puzzle.input),
        'output_patterns': find_patterns(puzzle.output)
    }

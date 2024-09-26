## src/geometor/arcprize/__init__.py

```py
"""
arcprize
========

GEOMETOR
--------



"""
__author__ = "phiarchitect"
__maintainer__ = "GEOMETOR"
__email__ = "github@phiarchitect.com"
__version__ = "0.0.1"
__licence__ = "MIT"

```

## src/geometor/arcprize/__main__.py

```py
"""The package entry point into the application."""

from .app import run

if __name__ == "__main__":
    run()
```

## src/geometor/arcprize/analyze.py

```py
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

```

## src/geometor/arcprize/app.py

```py
"""
run the main app
"""
from .arcprize import Arcprize


def run() -> None:
    reply = Arcprize().run()
    print(reply)

```

## src/geometor/arcprize/img_gen.py

```py
import json
import os
import glob
from PIL import Image, ImageDraw

# Color mapping from arcprize.org
# 0 --white: #EEEEEE;
# 1 --blue: #1E93FF;
# 2 --red: #F93C31;
# 3 --green: #4FCC30;
# 4 --yellow: #FFDC00;
# 5 --gray: #555555;
#  --magenta-light: #ff7bcc;
# 6 --magenta: #E53AA3;
# 7 --orange: #FF851B;
# 8 --blue-light: #87D8F1;
# 9 --maroon: #921231;
#  --black: #000000;
#  --offwhite: #C0C0C0;
#  --gray-light: #999999;
# replaced Gray with Pink
# darkened red, orange, yellow
#  5: (255, 123, 204),  # Pink
COLOR_MAP = {
    0: (238, 238, 238),  # White
    1: (30, 147, 255),  # Blue
    2: (220, 50, 40),  # Red
    3: (79, 204, 48),  # Green
    4: (230, 200, 0),  # Yellow
    5: (85, 85, 85),  # Gray
    6: (229, 58, 163),  # Magenta
    7: (230, 120, 20),  # Orange
    8: (135, 216, 241),  # Azure
    9: (146, 18, 49),  # Maroon
}


def create_grid_image(grid, filename):
    cell_size = 8
    border = 1
    color_size = 6
    width = len(grid[0]) * cell_size
    height = len(grid) * cell_size

    image = Image.new("RGB", (width, height), color="black")
    draw = ImageDraw.Draw(image)

    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            color = COLOR_MAP.get(
                cell, (128, 128, 128)
            )  # Default to gray if color not found
            draw.rectangle(
                [
                    x * cell_size + border,
                    y * cell_size + border,
                    x * cell_size + color_size,
                    y * cell_size + color_size,
                ],
                fill=color,
            )

    image.save(filename)


def process_puzzle(puzzle_data, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    for i, example in enumerate(puzzle_data["train"]):
        create_grid_image(
            example["input"], os.path.join(output_dir, f"train_{i+1}_input.png")
        )
        create_grid_image(
            example["output"], os.path.join(output_dir, f"train_{i+1}_output.png")
        )

    for i, test in enumerate(puzzle_data["test"]):
        create_grid_image(
            test["input"], os.path.join(output_dir, f"test_{i+1}_input.png")
        )
        if "output" in test:
            create_grid_image(
                test["output"], os.path.join(output_dir, f"test_{i+1}_output.png")
            )


def process_all_puzzles(input_dir, output_base_dir):
    for json_file in glob.glob(os.path.join(input_dir, "*.json")):
        puzzle_name = os.path.splitext(os.path.basename(json_file))[0]
        output_dir = os.path.join(output_base_dir, puzzle_name)

        with open(json_file, "r") as f:
            puzzle_data = json.load(f)

        process_puzzle(puzzle_data, output_dir)
        print(f"Processed puzzle: {puzzle_name}")


def image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()


def main():
    input_dir = "."  # Directory containing JSON files
    output_base_dir = "images"  # Base directory for output images
    #  puzzle_images
    process_all_puzzles(input_dir, output_base_dir)
    print(f"All puzzles processed. Images generated in {output_base_dir}")


if __name__ == "__main__":
    main()

```

## src/geometor/arcprize/puzzle_player.py

```py
from geometor.arcprize.model import Puzzle, Grid
from typing import Tuple, List


class PuzzlePlayer:
    def __init__(self, puzzle: Puzzle):
        self.puzzle = puzzle
        self.current_output = None
        self.attempts = 0
        self.max_attempts = 3

    def get_examples(self) -> List[Tuple[Grid, Grid]]:
        return [(pair.input, pair.output) for pair in self.puzzle.train]

    def get_test_input(self) -> Grid:
        return self.puzzle.test[0].input

    def set_output_grid_size(self, width: int, height: int):
        self.current_output = Grid(
            [[0 for _ in range(width)] for _ in range(height)],
            self.puzzle.id,
            "test",
            0,
            "output",
        )

    def set_color(self, cells: List[Tuple[int, int]], color: int):
        if self.current_output is None:
            raise ValueError(
                "Output grid not initialized. Call set_output_grid_size first."
            )
        for x, y in cells:
            if (
                0 <= x < self.current_output.width
                and 0 <= y < self.current_output.height
            ):
                self.current_output.matrix[y, x] = color
            else:
                print(f"Warning: Cell ({x}, {y}) is out of bounds and will be skipped.")

    def fill_contiguous_region(self, start: Tuple[int, int], new_color: int):
        if self.current_output is None:
            raise ValueError(
                "Output grid not initialized. Call set_output_grid_size first."
            )

        x, y = start
        if not (
            0 <= x < self.current_output.width and 0 <= y < self.current_output.height
        ):
            raise ValueError(f"Starting point ({x}, {y}) is out of bounds.")

        old_color = self.current_output.matrix[y, x]
        if old_color == new_color:
            return  # No need to fill if the colors are the same

        points_to_fill = self.get_contiguous_points(start, old_color)
        self.set_color(list(points_to_fill), new_color)

    def get_contiguous_points(
        self, start: Tuple[int, int], target_color: int
    ) -> Set[Tuple[int, int]]:
        """
        Returns a set of points that are contiguous with the starting point and have the target color.
        This is a placeholder implementation and should be replaced with a more efficient algorithm.
        """
        if self.current_output is None:
            raise ValueError(
                "Output grid not initialized. Call set_output_grid_size first."
            )

        contiguous_points = set()
        stack = [start]
        width, height = self.current_output.width, self.current_output.height

        while stack:
            x, y = stack.pop()
            if (x, y) in contiguous_points:
                continue

            if (
                0 <= x < width
                and 0 <= y < height
                and self.current_output.matrix[y, x] == target_color
            ):
                contiguous_points.add((x, y))
                stack.extend([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])

        return contiguous_points

    def copy_input_to_output(self):
        input_grid = self.get_test_input()
        self.set_output_grid_size(input_grid.width, input_grid.height)
        self.current_output.matrix = input_grid.matrix.copy()

    def clear_output_grid(self):
        if self.current_output is None:
            raise ValueError(
                "Output grid not initialized. Call set_output_grid_size first."
            )
        self.current_output.matrix.fill(0)

    def submit_solution(self) -> bool:
        if self.current_output is None:
            raise ValueError("No solution to submit. Create an output grid first.")
        if self.attempts >= self.max_attempts:
            return False
        self.attempts += 1
        return self.check_solution()

    def check_solution(self) -> bool:
        expected_output = self.puzzle.test[0].output
        return (self.current_output.matrix == expected_output.matrix).all()

    def reset(self):
        self.current_output = None
        self.attempts = 0

```

## src/geometor/arcprize/render.py

```py
import os
import matplotlib.pyplot as plt
from geometor.render import Plotter
from geometor.arcprize.styles import ARC_STYLES
from model import PuzzleSet, Puzzle, PuzzlePair, Grid
from multiprocessing import Pool, cpu_count

class ARCRenderer:
    def __init__(self, output_dir, fig_w=16, fig_h=9):
        self.output_dir = output_dir
        self.fig_w = fig_w
        self.fig_h = fig_h
        os.makedirs(output_dir, exist_ok=True)

    def render_grid(self, grid: Grid):
        plotter = Plotter(grid.name, FIG_W=self.fig_w, FIG_H=self.fig_h)
        plotter.add_styles(ARC_STYLES)
        plotter.plot_model(grid.model)
        output_path = os.path.join(self.output_dir, f"{grid.name}.png")
        plt.savefig(output_path)
        plt.close()

    def render_pair(self, pair: PuzzlePair):
        self.render_grid(pair.input)
        if pair.output:
            self.render_grid(pair.output)

    def render_puzzle(self, puzzle: Puzzle):
        for pair in puzzle.train:
            self.render_pair(pair)
        for pair in puzzle.test:
            self.render_pair(pair)

    def render_puzzle_set(self, puzzle_set: PuzzleSet):
        num_workers = cpu_count()
        print(f"Using {num_workers} workers")

        with Pool(num_workers) as pool:
            pool.map(self.render_puzzle, puzzle_set.puzzles)

def process_puzzle_set(args):
    input_dir, output_dir = args
    puzzle_set = PuzzleSet(input_dir)
    renderer = ARCRenderer(output_dir)
    renderer.render_puzzle_set(puzzle_set)
    return f"Processed {len(puzzle_set.puzzles)} puzzles"

def main():
    input_dir = "../refs/ARC-800-tasks/training"
    output_dir = "./rendered_puzzles"

    args = (input_dir, output_dir)
    result = process_puzzle_set(args)
    print(result)

if __name__ == "__main__":
    main()

```

## src/geometor/arcprize/reports5.py

```py
"""
report engine for the ARC challenge
processes for gathering information from input output matrices
each challenge has several training samples and one test
values in the matrix are integers from 0 to 9 - which we may refer to as colors
"""

import json
import os
import glob
from collections import Counter

def load_data(file_path):
    """
    Load JSON data from a file.

    :param file_path: Path to the JSON file.
    :return: Parsed JSON data.
    """
    with open(file_path, "r") as file:
        data = json.load(file)
    return data

def analyze_colors(data, report):
    """
    Analyze the unique values and their counts in the input and output matrices.

    :param data: Parsed JSON data.
    :param report: List to which the report content is appended.
    """
    report.append(f"## Color Analysis\n")
    for idx, (input_matrix, output_matrix) in enumerate(
        [(sample["input"], sample["output"]) for sample in data["train"]]
    ):
        input_colors = Counter([val for row in input_matrix for val in row])
        output_colors = Counter([val for row in output_matrix for val in row])
        
        
        # Creating a markdown table for color counts
        # TODO add a diff column for output - input
        report.append(f"|Color|Input Count|Output Count|")
        report.append(f"|---|---|---|")
        all_colors = set(input_colors.keys()).union(set(output_colors.keys()))
        for color in sorted(all_colors):
            report.append(f"|{color}|{input_colors[color]}|{output_colors[color]}|")
        report.append("\n")

def analyze_sizes(data, report):
    """
    Analyze sizes of input and output matrices and add details to the report.

    :param data: Parsed JSON data.
    :param report: List to which the report content is appended.
    """
    report.append(f"## Train Sizes\n")
    for idx, (input_matrix, output_matrix) in enumerate(
        [(sample["input"], sample["output"]) for sample in data["train"]]
    ):
        report.append(f"|set|w|h|A|")
        report.append(f"|---|---|---|---|")

        input_width = len(input_matrix[0])
        input_height = len(input_matrix)
        input_area = input_width * input_height
        report.append(f"|input|{input_width}|{input_height}|{input_area}|")

        output_width = len(output_matrix[0])
        output_height = len(output_matrix)
        output_area = output_width * output_height
        report.append(f"|output|{output_width}|{output_height}|{output_area}|")
        report.append(
            f"|diff|{output_width - input_width}|{output_height - input_height}|{output_area - input_area}|"
        )
        report.append("\n")

def get_size_average(file_path):
    """
    Calculate the average size of the input and output matrices for training samples.

    :param file_path: Path to the JSON file.
    :return: Average size of the input and output matrices.
    """
    data = load_data(file_path)
    total_area = 0
    num_samples = len(data["train"])

    for sample in data["train"]:
        input_matrix = sample["input"]
        output_matrix = sample["output"]
        input_area = len(input_matrix) * len(input_matrix[0])
        output_area = len(output_matrix) * len(output_matrix[0])
        total_area += input_area + output_area

    return total_area / num_samples if num_samples > 0 else 0

def sort_filepaths(file_paths):
    """
    Sort the list of file paths based on the average size of their training samples.

    :param file_paths: List of paths to JSON files.
    :return: Sorted list of file paths.
    """
    return sorted(file_paths, key=get_size_average)

def generate_report(data, filename_prefix, output_dir):
    """
    Generate a consolidated report for all challenges in a file and save it to a markdown file.

    :param data: Parsed JSON data.
    :param filename_prefix: Prefix for the generated markdown file.
    :param output_dir: Directory where the markdown file will be saved.
    """
    report = []
    report.append(f"# {filename_prefix}")
    analyze_sizes(data, report)
    analyze_colors(data, report)

    report_content = "\n".join(report)
    filename = os.path.join(output_dir, f"{filename_prefix}.md")
    with open(filename, "w") as file:
        file.write(report_content)

def process_files(file_paths, output_dir):
    """
    Process multiple JSON files and generate a consolidated markdown report for each file.

    :param file_paths: List of paths to JSON files.
    :param output_dir: Directory where the markdown files will be saved.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    sorted_file_paths = sort_filepaths(file_paths)

    for idx, file_path in enumerate(sorted_file_paths):
        data = load_data(file_path)
        base_name = os.path.basename(file_path).split(".")[0]
        generate_report(data, f"{idx:03}-{base_name}", output_dir)

# Example usage
file_paths = glob.glob("./training/*.json")

output_directory = "./reports"
process_files(file_paths, output_directory)


```

## src/geometor/arcprize/styles.py

```py
from geometor.render.styles.z_levels import *

# Fixed color palette for classes 0 to 9
COLOR_PALETTE = [
    "#111111",  # 0: Dark grey (almost black) as requested
    "#FF0000",  # 1: Red
    "#00FF00",  # 2: Green
    "#0000FF",  # 3: Blue
    "#FF00FF",  # 4: Magenta
    "#FFFF00",  # 5: Yellow
    "#00FFFF",  # 6: Cyan
    "#FF8000",  # 7: Orange
    "#8000FF",  # 8: Purple
    "#00FF80",  # 9: Spring Green
]

def generate_class_style(class_num):
    color = COLOR_PALETTE[class_num]
    return {
        "point_inner": {
            "color": "w",
            "linestyle": "",
            "marker": ".",
            "markersize": 2,
            "zorder": Z_POINT_INNER,
        },
        "point_outer": {
            "color": "k",
            "linestyle": "",
            "marker": ".",
            "markersize": 5,
            "zorder": Z_POINT_OUTER,
        },
        "point_selected": {
            "color": "yellow",
            "linestyle": "",
            "fillstyle": "none",
            "marker": "o",
            "markersize": 24,
            "markeredgecolor": "yellow",
            "markeredgewidth": 2,
            "zorder": Z_SELECTED,
        },
        "point_highlight": {
            "color": color,
            "linestyle": "",
            "marker": "o",
            "markersize": 30,
            "markeredgecolor": color,
            "markeredgewidth": 3,
            "zorder": Z_POINT_HILITE,
        },
    }

# Generate styles for classes 0 to 9
# use plotter.add_styles(ARC_STYLES)
ARC_STYLES = {str(i): generate_class_style(i) for i in range(10)}



```

## src/geometor/arcprize/perception/__init__.py

```py



```

## src/geometor/arcprize/perception/data_export.py

```py
import csv

def export_to_csv(results, filename):
    if not results:
        print("No results to export.")
        return
    
    keys = results[0].keys()
    with open(filename, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(results)
    
    print(f"Results exported to {filename}")

```

## src/geometor/arcprize/perception/experiment_runner.py

```py
from rich import print
from datetime import datetime

from .puzzles.random_rotate import generate_puzzle_set
from .models.ollama import generate_response
from .grids.tools import grid_to_string


def test_individual_puzzles(puzzles, model):
    results = []
    for i, prompt, correct_answer, size, symbol_set, input_grid, output_grid in puzzles:
        input_grid_str = grid_to_string(input_grid)
        output_grid_str = grid_to_string(output_grid)
        print(f"\n {i} of {len(puzzles)} #####################################")
        print()
        print(input_grid_str)
        print()
        print(output_grid_str)
        result, processing_time = generate_response(prompt, model)

        response = result["response"].strip().lower()
        print(f"response: {response}")

        is_correct = response == correct_answer.lower()
        print(f"  answer: {correct_answer}", is_correct)

        print(f"    time: {processing_time:.2f} s")

        test_result = {
            "index": i,
            "size": size,
            "model_response": response,
            "correct_answer": correct_answer,
            "is_correct": is_correct,
            "processing_time": processing_time,
            "model": model,
            "symbol_set": symbol_set,
            "input_grid": grid_to_string(input_grid),
            "output_grid": grid_to_string(output_grid),
        }
        results.append(test_result)

    return results



```

## src/geometor/arcprize/perception/symbols.py

```py
SYMBOL_SETS = {
    "XO": "XO",
    "digits": "0123456789",
    "letters": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "symbols": "@#$%&*+=?!",
    "emoji": "😀😎🤔🙃😍🤨😮🤯🥳🤖",
    "geometric": "■□▲△○●★☆◆◇",
    "colored_blocks": "🟥🟧🟨🟩🟦🟪🟫⬛⬜",
}

```

## src/geometor/arcprize/perception/grids/__init__.py

```py

```

## src/geometor/arcprize/perception/grids/random_full.py

```py
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

```

## src/geometor/arcprize/perception/grids/random_lines.py

```py
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

```

## src/geometor/arcprize/perception/grids/random_rectangles.py

```py
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

```

## src/geometor/arcprize/perception/grids/random_sparse.py

```py
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

```

## src/geometor/arcprize/perception/grids/tools.py

```py
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

```

## src/geometor/arcprize/perception/models/__init__.py

```py

```

## src/geometor/arcprize/perception/models/ollama.py

```py
import requests
import time

def generate_response(prompt, model):
    url = "http://localhost:11434/api/generate"
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    
    start_time = time.time()
    response = requests.post(url, json=data)
    end_time = time.time()
    
    if response.status_code == 200:
        result = response.json()
        processing_time = end_time - start_time
        return result, processing_time
    else:
        return f"Error: {response.status_code}", 0

```

## src/geometor/arcprize/perception/puzzles/__init__.py

```py

```

## src/geometor/arcprize/perception/puzzles/random_rotate.py

```py

import random
import numpy as np
from jinja2 import Environment, PackageLoader


from geometor.arcprize.perception.grids.random_rectangles import generate_grid
from geometor.arcprize.perception.grids.tools import rotate_grid, introduce_errors, grid_to_string
from geometor.arcprize.perception.symbols import SYMBOL_SETS


def generate_puzzle(size=3, error_chance=0.1, max_errors=1, symbol_set_key="digits"):
    symbol_set = SYMBOL_SETS[symbol_set_key]
    input_grid = generate_grid(size, size, symbol_set)
    rotation = random.choice(["none", "right", "left", "full"])
    output_grid = rotate_grid(input_grid, rotation)

    output_grid = introduce_errors(output_grid, error_chance, max_errors, symbol_set)

    if not np.array_equal(output_grid, rotate_grid(input_grid, rotation)):
        rotation = "error"

    return input_grid, output_grid, rotation


def generate_prompt(input_grid, output_grid, row_delimiter="\n", cell_delimiter=" "):
    env = Environment(
            loader=PackageLoader("geometor.arcprize.perception", "puzzles"),
    )
    template_variables = {
        "input_grid": grid_to_string(input_grid, row_delimiter, cell_delimiter),
        "output_grid": grid_to_string(output_grid, row_delimiter, cell_delimiter),
    }
    template = env.get_template("random_rotate.txt.j2")
    prompt = template.render(template_variables)

    return prompt


def generate_puzzle_set(
    num_puzzles,
    min_size=3,
    max_size=5,
    error_chance=0.1,
    max_errors=1,
    symbol_set_key="digits",
    row_delimiter="\n",
    cell_delimiter=" ",
):
    puzzles = []
    for i in range(num_puzzles):
        size = random.randint(min_size, max_size)
        input_grid, output_grid, rotation = generate_puzzle(
            size, error_chance, max_errors, symbol_set_key
        )
        prompt = generate_prompt(input_grid, output_grid, row_delimiter, cell_delimiter)
        puzzles.append(
            (i, prompt, rotation, size, symbol_set_key, input_grid, output_grid)
        )
    return puzzles

```

## src/geometor/arcprize/perception/puzzles/random_rotate.txt.j2

```jinja
<instruction>
You are training your perceptual skills with puzzles.
Each puzzle contains two grids of values.
The input grid is generated with random symbols.
The output grid is a potential rotation of the input grid (right, left, full, none)
You are becoming exceptionally skilled at detecting rotations in these puzzles.
Analyze the following puzzle and determine the rotation applied:
</instruction>
<puzzle>
<input>
{{input_grid}}
</input>
<output>
{{output_grid}}
</output>
</puzzle>
<instruction>
Determine the rotation applied to transform the input grid into the output grid. 
Respond with exactly one of these words: `none`, `right`, `left`, `full`, or `error`.
Do not explain your answer.
</instruction>

Answer: 

```

## src/geometor/arcprize/perception/render/__init__.py

```py

```

## src/geometor/arcprize/perception/render/capture_test.py

```py
from playwright.sync_api import sync_playwright

# HTML content with a simple CSS animation and a timer
html_content = """
<!DOCTYPE html>
<html>
<head>
    <style>
        @keyframes move {
            0% { transform: translateX(0); }
            100% { transform: translateX(200px); }
        }
        .box {
            width: 50px;
            height: 50px;
            background-color: red;
            animation: move 2s infinite alternate;
        }
        #timer {
            font-size: 24px;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="box"></div>
    <div id="timer">0.00</div>
    <script>
        let startTime = Date.now();
        let timerElement = document.getElementById('timer');
        function updateTimer() {
            let elapsedTime = (Date.now() - startTime) / 1000;
            timerElement.textContent = elapsedTime.toFixed(2);
            if (elapsedTime < 10) {
                requestAnimationFrame(updateTimer);
            }
        }
        updateTimer();
    </script>
</body>
</html>
"""

def capture_animation_with_timer():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        
        # Start video recording
        context = browser.new_context(
            record_video_dir="./videos/",
            record_video_size={"width": 1920, "height": 1080}
        )
        
        page = context.new_page()
        
        # Set the content of the page directly
        page.set_content(html_content)
        # Wait for the timer to reach 5 seconds
        page.wait_for_function("() => parseFloat(document.getElementById('timer').textContent) >= 5")
        
        # Close the context to stop recording
        context.close()
        # Retrieve the path to the recorded video
        video_path = page.video.path()

        # Close the browser
        browser.close()

    print("Video captured as", video_path)

if __name__ == "__main__":
    capture_animation_with_timer()


```

## src/geometor/arcprize/perception/render/pw.py

```py
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
from jinja2 import Environment, FileSystemLoader

# Set up Jinja2 environment
env = Environment(loader=FileSystemLoader("."))
template = env.get_template("template4.html.j2")


def generate_puzzle_image(puzzle, output_dir, page, total_puzzles):
    # Generate HTML content using Jinja2 template
    puzzle["total_puzzles"] = total_puzzles
    html_content = template.render(puzzle)

    # Set content and wait for it to load
    page.set_content(html_content)
    page.wait_for_load_state("networkidle")

    # Capture screenshot
    output_path = output_dir / f"{puzzle['symbol_set']}_{puzzle['index']}.png"
    page.screenshot(path=str(output_path), full_page=True)
    print(f"Created {output_path}")

    output_path = output_dir / f"{puzzle['symbol_set']}_{puzzle['index']}.html"
    with open(output_path, "w") as f:
        f.write(html_content)
    print(f"Created {output_path}")


def visualize_puzzles(json_file, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(json_file, "r") as f:
        data = json.load(f)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1920, "height": 1080})

        total_puzzles = len(data["results"])

        for puzzle in data["results"]:
            generate_puzzle_image(puzzle, output_dir, page, total_puzzles)

        browser.close()


if __name__ == "__main__":
    json_file = "../../../../../demos/rotation_puzzle_results_20240802_084405.json"
    output_dir = "~/Sessions/rotation_test"
    visualize_puzzles(json_file, output_dir)

```

## src/geometor/arcprize/perception/render/pw2.py

```py
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
from jinja2 import Environment, FileSystemLoader

# Set up Jinja2 environment
env = Environment(loader=FileSystemLoader("."))
template = env.get_template("template3.html.j2")
animated_template = env.get_template("template4.html.j2")


def generate_puzzle_image(puzzle, output_dir, page):
    html_content = template.render(puzzle)

    # Set content and wait for it to load
    page.set_content(html_content)
    page.wait_for_load_state("networkidle")

    # Capture screenshot
    output_path = output_dir / f"{puzzle['title']}.png"
    page.screenshot(path=str(output_path), full_page=True)
    print(f"Created {output_path}")

    output_path = output_dir / f"{puzzle['symbol_set']}_{puzzle['index']}.html"
    with open(output_path, "w") as f:
        f.write(html_content)
    print(f"Created {output_path}")


def capture_puzzle_animation(puzzle, output_dir, page):
    html_content = animated_template.render(puzzle)

    page.set_content(html_content)

    # Wait for the animation to complete
    page.wait_for_function(
        f"() => parseFloat(document.getElementById('timer').textContent) >= {puzzle['processing_time']}"
    )

    video_path = page.video.path()
    new_video_path = (
        output_dir / f"{puzzle['title']}.webm"
    )
    video_path = Path(video_path).rename(new_video_path)
    print(f"created {video_path}")


def visualize_puzzles(json_file, puzzle_type):
    json_path = Path(json_file).expanduser().resolve()
    output_dir = Path.home() / "Sessions" / json_path.stem
    output_dir.mkdir(parents=True, exist_ok=True)

    with json_path.open("r") as f:
        data = json.load(f)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            record_video_dir=str(output_dir),
            record_video_size={"width": 1920, "height": 1080},
        )
        page = context.new_page()
        page.set_viewport_size({"width": 1920, "height": 1080})

        total_puzzles = len(data["results"])

        for puzzle in data["results"]:

            puzzle['title'] = f"{puzzle['symbol_set']}_{puzzle['index']}"
            puzzle["total_puzzles"] = total_puzzles
            puzzle["type"] = puzzle_type
            generate_puzzle_image(puzzle, output_dir, page)
            #  capture_puzzle_animation(puzzle, output_dir, page, total_puzzles)

            # Rename the video file

        context.close()
        browser.close()


if __name__ == "__main__":
    json_file = "../../../../../demos/rotation_puzzle_results_20240802_084405.json"
    visualize_puzzles(json_file, "ROTATION")

```

## src/geometor/arcprize/perception/render/svg.py

```py
import json
import svgwrite

def create_grid_svg(dwg, grid, start_x, start_y, cell_size, title):
    elements = []

    # Add title
    elements.append(
        dwg.text(
            title,
            insert=(start_x + len(grid[0]) * cell_size / 2, start_y - 10),
            text_anchor="middle",
            font_size=14,
            font_family="Arial",
            fill="gray",
        )
    )

    # Draw background
    elements.append(
        dwg.rect(
            insert=(start_x, start_y),
            size=(len(grid[0]) * cell_size, len(grid) * cell_size),
            fill="black",
        )
    )

    # Draw grid as text
    for y, row in enumerate(grid):
        elements.append(
            dwg.text(
                row,
                insert=(start_x + 5, start_y + (y + 0.7) * cell_size),
                font_size=14,
                font_family="monospace",
                fill="white",
            )
        )

    return elements

def create_puzzle_svg(puzzle, filename):
    input_grid = puzzle["input_grid"].split("\n")
    output_grid = puzzle["output_grid"].split("\n")

    cell_size = 20  # Adjusted for monospace font
    max_line_length = max(max(len(line) for line in input_grid), 
                          max(len(line) for line in output_grid))
    grid_width = max_line_length * cell_size
    grid_height = len(input_grid) * cell_size
    padding = 20
    total_width = grid_width * 2 + padding * 3
    total_height = grid_height + padding * 2

    dwg = svgwrite.Drawing(filename, size=(f"{total_width}px", f"{total_height}px"))

    # Create input grid
    input_elements = create_grid_svg(
        dwg, input_grid, padding, padding, cell_size, "Input Grid"
    )
    for element in input_elements:
        dwg.add(element)

    # Create output grid
    output_elements = create_grid_svg(
        dwg, output_grid, grid_width + padding * 2, padding, cell_size, "Output Grid"
    )
    for element in output_elements:
        dwg.add(element)

    # Add puzzle information
    info_text = f"Model: {puzzle['model']}, Response: {puzzle['model_response']}, Correct: {puzzle['correct_answer']}"
    dwg.add(
        dwg.text(
            info_text,
            insert=(padding, total_height - 10),
            font_size=12,
            font_family="Arial",
            fill="black",
        )
    )

    dwg.save()

def visualize_puzzles(json_file):
    with open(json_file, "r") as f:
        data = json.load(f)

    for i, puzzle in enumerate(data["results"]):
        filename = f"puzzle_{i+1}.svg"
        create_puzzle_svg(puzzle, filename)
        print(f"Created {filename}")

if __name__ == "__main__":
    json_file = "../../../../../demos/rotation_puzzle_results_20240802_084405.json"  # Replace with your JSON file name
    visualize_puzzles(json_file)


```

## src/geometor/arcprize/perception/render/template.html.j2

```jinja
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Puzzle Visualization</title>
    <style>
        html, body {
            height: 100%;
            margin: 0;
            padding: 0;
        }
        body {
            display: flex;
            flex-direction: column;
            font-family: Arial, sans-serif;
            background-color: black;
            color: white;
        }
        header, footer {
            height: 80px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #999;
        }
        main {
            flex-grow: 1;
            display: flex;
            justify-content: space-around;
            align-items: center;
            padding: 20px;
        }
        section {
            background-color: #111;
            color: #fff;
            padding: 20px;
            border-radius: 5px;
            width: 45%;
            height: 80%;
            display: flex;
            flex-direction: column;
        }
        section > h1 {
            text-align: center;
            color: #888;
            margin-top: 0;
            margin-bottom: 20px;
        }
        .grid-content {
            font-family: monospace;
            white-space: pre;
            flex-grow: 1;
            display: flex;
            align-items: center;
            justify-content: center;
        }
    </style>
</head>
<body>
    {% set rows = size %}
    {% set cols = input_grid.split('\n')|first|length %}
    {% set base_size = 500 %}  {# Adjust this value to change the overall scale #}
    {% set font_size = (base_size / (rows * cols)**0.5)|round|int %}
    
    <header><h1>{{model}} • {{symbol_set}}</h1></header>
    <main>
        <section>
            <h1>input</h1>
            <div class="grid-content" style="font-size: {{font_size}}px;">{{input_grid}}</div>
        </section>
        <section>
            <h1>output</h1>
            <div class="grid-content" style="font-size: {{font_size}}px;">{{output_grid}}</div>
        </section>
    </main>
    <footer>
        Response: {{model_response}} • Correct: {{correct_answer}}
    </footer>
</body>
</html>

```

## src/geometor/arcprize/perception/render/template2.html.j2

```jinja
{% set rows = size %}
{% set cols = input_grid.split('\n')|first|length %}
{% set base_size = 500 %}
{% set font_size = (base_size / (rows * cols)**0.5)|round|int %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Puzzle Visualization</title>
    <style>
        html, body {
            height: 100%;
            margin: 0;
            padding: 0;
        }
        p {
            margin: 0;
        }
        body {
            display: flex;
            flex-direction: column;
            font-family: Arial, sans-serif;
            background-color: black;
            color: white;
            /* padding: 1em; */
        }
        header, footer {
            height: 80px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 20px;
            background: #111;
            color: #999;
            font-size: 20px;
            margin: 1em;
        }
        header > div, footer > div {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        main {
            flex-grow: 1;
            display: flex;
            justify-content: space-around;
            align-items: center;
            padding: 20px;
            margin: 1em;
        }
        section {
            background-color: #111;
            color: #fff;
            padding: 20px;
            width: 45%;
            /* height: 80%; */
            display: flex;
            flex-direction: column;
        }
        section > h2 {
            text-align: center;
            color: #888;
            margin-top: 0;
            margin-bottom: 20px;
        }
        .grid-content {
            font-family: monospace;
            white-space: pre;
            flex-grow: 1;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .value {
            font-size: 1.5rem;
            color: white;
            font-weight: bold;
            padding: 20px;
        }
        .True {
            color: green;
        }
        .False {
            color: red;
        }
    </style>
</head>
<body>
    <header>
        <div class="index">{{index}}<hr>{{total_puzzles}}</div>
        <div class="title">TITLE<hr>{{size}} x {{size}}</div>
        <div>{{model}}<hr>{{symbol_set}}</div>
    </header>
    <main>
        <section>
            <h2>INPUT</h2>
            <div class="grid-content" style="font-size: {{font_size}}px;">{{input_grid}}</div>
        </section>
        <section>
            <h2>OUTPUT</h2>
            <div class="grid-content" style="font-size: {{font_size}}px;">{{output_grid}}</div>
        </section>
    </main>
    <footer>
        <div>
        <p>correct answer:</p>
        <p class="value">{{correct_answer|upper}}</p>
        </div>
        <div>
        <p>model response:</p>
        <p class="value">{{model_response|upper}}</p>
        </div>
        <div >
        <p class="value {{is_correct}}">{{is_correct|upper}}</p>
        </div>
        <div>
        <p>time:</p>
        <p class="value">{{'{0:0.2f}'.format(processing_time)}} s</p>
        </div>
    </footer>
</body>
</html>

```

## src/geometor/arcprize/perception/render/template3.html.j2

```jinja
{% set rows = size %}
{% set cols = input_grid.split('\n')|first|length %}
{% set base_size = 700 %}
{% set font_size = (base_size / (rows * cols)**0.5)|round|int %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Puzzle Visualization</title>
    <style>
        html, body {
            height: 100%;
            margin: 0;
            padding: 0;
        }
        p {
            margin: 0;
        }
        body {
            display: flex;
            flex-direction: column;
            font-family: Arial, sans-serif;
            background-color: black;
            color: white;
        }
        header, footer {
            height: 80px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 20px;
            background: #111;
            color: #999;
            font-size: 20px;
        }
        header > div, footer > div {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        main {
            flex-grow: 1;
            display: flex;
            justify-content: space-between;
            align-items: stretch;
            padding: 20px;
        }
        section {
            background-color: #111;
            color: #fff;
            padding: 20px;
            width: 48%;
            display: flex;
            flex-direction: column;
        }
        section > h2 {
            text-align: center;
            color: #888;
            margin-top: 0;
            margin-bottom: 20px;
        }
        .grid-content {
            font-family: monospace;
            white-space: pre;
            flex-grow: 1;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .value {
            font-size: 1.5rem;
            color: white;
            font-weight: bold;
            padding: 20px;
        }
        .True {
            color: green;
        }
        .False {
            color: red;
        }
    </style>
</head>
<body>
    <header>
        <div class="index">{{index}}<hr>{{total_puzzles}}</div>
        <div class="title">{{title}}<hr>{{type}}</div>
        <div>{{model}}<hr>{{size}} x {{size}}</div>
    </header>
    <main>
        <section>
            <h2>INPUT</h2>
            <div class="grid-content" style="font-size: {{font_size}}px;">{{input_grid}}</div>
        </section>
        <section>
            <h2>OUTPUT</h2>
            <div class="grid-content" style="font-size: {{font_size}}px;">{{output_grid}}</div>
        </section>
    </main>
    <footer>
        <div>
        <p>correct answer:</p>
        <p class="value">{{correct_answer|upper}}</p>
        </div>
        <div>
        <p>model response:</p>
        <p class="value">{{model_response|upper}}</p>
        </div>
        <div >
        <p class="value {{is_correct}}">{{is_correct|upper}}</p>
        </div>
        <div>
        <p>time:</p>
        <p class="value">{{'{0:0.2f}'.format(processing_time)}} s</p>
        </div>
    </footer>
</body>
</html>

```

## src/geometor/arcprize/perception/render/template4.html.j2

```jinja
{% set rows = size %}
{% set cols = input_grid.split('\n')|first|length %}
{% set base_size = 700 %}
{% set font_size = (base_size / (rows * cols)**0.5)|round|int %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Puzzle Visualization</title>
    <style>
        html, body {
            height: 100%;
            margin: 0;
            padding: 0;
        }
        p {
            margin: 0;
        }
        body {
            display: flex;
            flex-direction: column;
            font-family: Arial, sans-serif;
            background-color: black;
            color: white;
        }
        header, footer {
            height: 80px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 20px;
            background: #111;
            color: #999;
            font-size: 20px;
        }
        header > div, footer > div {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        main {
            flex-grow: 1;
            display: flex;
            justify-content: space-between;
            align-items: stretch;
            padding: 20px;
        }
        section {
            background-color: #111;
            color: #fff;
            padding: 20px;
            width: 48%;
            display: flex;
            flex-direction: column;
        }
        section > h2 {
            text-align: center;
            color: #888;
            margin-top: 0;
            margin-bottom: 20px;
        }
        .grid-content {
            font-family: monospace;
            white-space: pre;
            flex-grow: 1;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .value {
            font-size: 1.5rem;
            color: white;
            font-weight: bold;
            padding: 20px;
        }
        .True {
            color: green;
        }
        .False {
            color: red;
        }
        #timer {
            font-size: 48px;
            text-align: center;
            margin: 20px 0;
        }
        .hidden {
            visibility: hidden;
        }
    </style>
</head>
<body>
    <header>
        <div class="index">{{index}}<hr>{{total_puzzles}}</div>
        <div class="title">TITLE<hr>{{size}} x {{size}}</div>
        <div>{{model}}<hr>{{symbol_set}}</div>
    </header>
    <main>
        <section>
            <h2>INPUT</h2>
            <div class="grid-content" style="font-size: {{font_size}}px;">{{input_grid}}</div>
        </section>
        <section>
            <h2>OUTPUT</h2>
            <div class="grid-content" style="font-size: {{font_size}}px;">{{output_grid}}</div>
        </section>
    </main>
    <div id="timer">0.00</div>
    <footer>
        <div>
        <p>correct answer:</p>
        <p class="value hidden" id="correct-answer">{{correct_answer|upper}}</p>
        </div>
        <div>
        <p>model response:</p>
        <p class="value hidden" id="model-response">{{model_response|upper}}</p>
        </div>
        <div>
        <p class="value hidden {{is_correct}}" id="is-correct">{{is_correct|upper}}</p>
        </div>
        <div>
        <p>time:</p>
        <p class="value hidden" id="processing-time">{{'{0:0.2f}'.format(processing_time)}} s</p>
        </div>
    </footer>
    <script>
        let startTime = Date.now();
        let timerElement = document.getElementById('timer');
        let targetTime = {{processing_time}};

        function updateTimer() {
            let elapsedTime = (Date.now() - startTime) / 1000;
            timerElement.textContent = elapsedTime.toFixed(2);
            if (elapsedTime < targetTime) {
                requestAnimationFrame(updateTimer);
            } else {
                showResults();
            }
        }

        function showResults() {
            document.getElementById('correct-answer').classList.remove('hidden');
            document.getElementById('model-response').classList.remove('hidden');
            document.getElementById('is-correct').classList.remove('hidden');
            document.getElementById('processing-time').classList.remove('hidden');
        }

        updateTimer();
    </script>
</body>
</html>

```

## src/geometor/arcprize/puzzles/__init__.py

```py

```

## src/geometor/arcprize/puzzles/grid.py

```py
import numpy as np
from geometor.model import Model

class Grid:
    def __init__(self, matrix, puzzle_id, set_type, index, io_type):
        self.matrix = np.array(matrix, dtype=int)
        self.puzzle_id = puzzle_id
        self.set_type = set_type  # 'train' or 'test'
        self.index = index
        self.io_type = io_type  # 'input' or 'output'
        self._model = None

    @property
    def name(self):
        return f"{self.puzzle_id}-{self.set_type}-{self.index}-{self.io_type}"

    @property
    def height(self):
        return self.matrix.shape[0]

    @property
    def width(self):
        return self.matrix.shape[1]

    @property
    def size(self):
        return self.matrix.size

    @property
    def colors(self):
        return set(np.unique(self.matrix))

    @property
    def color_counts(self):
        unique, counts = np.unique(self.matrix, return_counts=True)
        return dict(zip(unique, counts))

    @property
    def model(self):
        if self._model is None:
            self._model = self._create_model()
        return self._model

    def _create_model(self):
        model = Model(self.name)
        for y in range(self.height):
            for x in range(self.width):
                val = self.matrix[y, x]
                model.set_point(x, y, classes=[str(val)], label=f"({x},{y})")
        return model

    def rotate(self, k=1):
        """
        Rotate the grid by 90 degrees k times.
        Positive k means clockwise rotation, negative k means counter-clockwise.
        """
        new_matrix = np.rot90(self.matrix, k=-k)
        return Grid(new_matrix, self.puzzle_id, self.set_type, self.index, f"{self.io_type}_rotated{k*90}")

    def flip(self, axis=0):
        """
        Flip the grid along the specified axis.
        axis=0 flips vertically, axis=1 flips horizontally.
        """
        new_matrix = np.flip(self.matrix, axis=axis)
        flip_type = "vertical" if axis == 0 else "horizontal"
        return Grid(new_matrix, self.puzzle_id, self.set_type, self.index, f"{self.io_type}_flipped_{flip_type}")

    def to_string(self, row_delimiter="\n", cell_delimiter=" "):
        return row_delimiter.join(
            cell_delimiter.join(str(cell) for cell in row) for row in self.matrix
        )


```

## src/geometor/arcprize/puzzles/puzzle.py

```py
import json
from pathlib import Path
from collections import Counter
from .grid import Grid


class PuzzlePair:
    def __init__(self, puzzle_id, set_type, index, input_grid, output_grid=None):
        self.input = Grid(input_grid, puzzle_id, set_type, index, "input")
        self.output = (
            Grid(output_grid, puzzle_id, set_type, index, "output")
            if output_grid is not None
            else None
        )

    @property
    def weight(self):
        return self.input.size + (self.output.size if self.output else 0)

    @property
    def size_change(self):
        if self.output is None:
            return None
        return {
            "width": self.output.width - self.input.width,
            "height": self.output.height - self.input.height,
            "total": self.output.size - self.input.size,
        }

    @property
    def colors(self):
        return self.input.colors.union(self.output.colors if self.output else set())

    @property
    def color_changes(self):
        if self.output is None:
            return None
        input_counts = self.input.color_counts
        output_counts = self.output.color_counts
        return {
            color: output_counts.get(color, 0) - input_counts.get(color, 0)
            for color in self.colors
        }


class Puzzle:
    def __init__(self, id, data):
        self.id = id
        self.train = [
            PuzzlePair(id, "train", i, pair["input"], pair["output"])
            for i, pair in enumerate(data["train"])
        ]
        self.test = [
            PuzzlePair(id, "test", i, test_input["input"], test_input.get("output"))
            for i, test_input in enumerate(data["test"])
        ]

    @property
    def all_pairs(self):
        return self.train + self.test

    @property
    def weight(self):
        return sum(pair.weight for pair in self.all_pairs)

    @property
    def colors(self):
        return set.union(*(pair.colors for pair in self.all_pairs))


class PuzzleSet:
    def __init__(self, folder_path="."):
        self.puzzles = self._load_puzzles(Path(folder_path))

    def _load_puzzles(self, folder_path):
        puzzles = []
        for file_path in folder_path.glob("*.json"):
            puzzle_id = file_path.stem  # Get filename without extension
            with file_path.open("r") as f:
                data = json.load(f)
                puzzles.append(Puzzle(puzzle_id, data))
        return puzzles

    def get_ordered_puzzles(self, key="weight", reverse=False):
        return sorted(self.puzzles, key=lambda p: getattr(p, key), reverse=reverse)

    def get_puzzles_by_color_count(self, count):
        return [p for p in self.puzzles if len(p.colors) == count]

    def get_puzzles_by_size_change(self, change_type="total", value=0):
        return [
            p
            for p in self.puzzles
            if any(
                pair.size_change and pair.size_change[change_type] == value
                for pair in p.all_pairs
            )
        ]

```

## src/geometor/arcprize/puzzles/report.py

```py
import json
from pathlib import Path
from collections import Counter
import numpy as np
from geometor.model import Model



# Usage example:
if __name__ == "__main__":
    puzzle_set = PuzzleSet("../../../refs/ARC-800-tasks/training")

    # Get puzzles ordered by weight
    ordered_puzzles = puzzle_set.get_ordered_puzzles()

    # Get puzzles with exactly 3 colors
    three_color_puzzles = puzzle_set.get_puzzles_by_color_count(3)

    # Get puzzles where at least one pair has no total size change
    no_size_change_puzzles = puzzle_set.get_puzzles_by_size_change("total", 0)

    # Print IDs of the first 5 puzzles
    for puzzle in puzzle_set.puzzles[:5]:
        print(f"Puzzle ID: {puzzle.id}")
        print(f"Number of training pairs: {len(puzzle.train)}")
        print(f"Number of test inputs: {len(puzzle.test)}")
        print(f"Number of test inputs with outputs: {sum(1 for test in puzzle.test if test.output is not None)}")
        print("---")

    # Example of using the rotation function and accessing the model
    if puzzle_set.puzzles:
        first_puzzle = puzzle_set.puzzles[0]
        first_train_pair = first_puzzle.train[0]
        rotated_input = first_train_pair.input.rotate()
        print(f"Original training input name: {first_train_pair.input.name}")
        print(f"Original training input:\n{first_train_pair.input.matrix}")
        print(f"Rotated training input name: {rotated_input.name}")
        print(f"Rotated training input:\n{rotated_input.matrix}")
        print(f"Original input model name: {first_train_pair.input.model.name}")
        print(f"Rotated input model name: {rotated_input.model.name}")
        
        if first_puzzle.test:
            first_test_pair = first_puzzle.test[0]
            rotated_test = first_test_pair.input.rotate()
            print(f"Original test input name: {first_test_pair.input.name}")
            print(f"Original test input:\n{first_test_pair.input.matrix}")
            print(f"Rotated test input name: {rotated_test.name}")
            print(f"Rotated test input:\n{rotated_test.matrix}")
            print(f"Original test input model name: {first_test_pair.input.model.name}")
            print(f"Rotated test input model name: {rotated_test.model.name}")
            if first_test_pair.output:
                print(f"Test output name: {first_test_pair.output.name}")
                print(f"Test output:\n{first_test_pair.output.matrix}")
                print(f"Test output model name: {first_test_pair.output.model.name}")

```


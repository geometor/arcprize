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

## src/geometor/arcprize/perception/__init__.py

```py

```

## src/geometor/arcprize/perception/grids/__init__.py

```py

```

## src/geometor/arcprize/perception/models/__init__.py

```py

```

## src/geometor/arcprize/perception/puzzles/__init__.py

```py

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

## src/geometor/arcprize/arcprize.py

```py
"""
arcprize
"""
```

## src/geometor/arcprize/model.py

```py
import json
from pathlib import Path
from collections import Counter
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

class PuzzlePair:
    def __init__(self, puzzle_id, set_type, index, input_grid, output_grid=None):
        self.input = Grid(input_grid, puzzle_id, set_type, index, "input")
        self.output = Grid(output_grid, puzzle_id, set_type, index, "output") if output_grid is not None else None

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
        self.train = [PuzzlePair(id, "train", i, pair["input"], pair["output"]) for i, pair in enumerate(data["train"])]
        self.test = [PuzzlePair(id, "test", i, test_input["input"], test_input.get("output")) for i, test_input in enumerate(data["test"])]

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
    def __init__(self, folder_path):
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
        return [p for p in self.puzzles if any(pair.size_change and pair.size_change[change_type] == value for pair in p.all_pairs)]

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

## src/geometor/arcprize/perception/__main__.py

```py
from datetime import datetime

from .experiment_runner import run_experiments
from .data_export import export_to_csv

if __name__ == "__main__":
    model = "phi3:mini"
    model = "phi3:medium"
    model = "llama3.1"
    symbol_sets_to_test = ["XO", "digits", "letters", "symbols"]
    results = run_experiments(
        symbol_sets_to_test, puzzles_per_set=10, min_size=3, max_size=5, model=model
    )

    export_to_csv(
        results,
        f"rotation_puzzle_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
    )

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


def test_individual_puzzles(puzzles, model):
    results = []
    for i, prompt, correct_answer, size, symbol_set, input_grid, output_grid in puzzles:
        print("\n#####################################")
        print(prompt)
        result, processing_time = generate_response(prompt, model)
        response = result["response"].strip().lower()
        print(response)

        is_correct = response == correct_answer.lower()
        print(is_correct, correct_answer)

        test_result = {
            "index": i,
            "size": size,
            "model_response": response,
            "correct_answer": correct_answer,
            "is_correct": is_correct,
            "processing_time": processing_time,
            "model": model,
            "symbol_set": symbol_set,
        }
        results.append(test_result)

    return results


def run_experiments(symbol_sets, puzzles_per_set, min_size, max_size, model):
    all_results = []

    for symbol_set in symbol_sets:
        puzzles = generate_puzzle_set(
            puzzles_per_set,
            min_size=min_size,
            max_size=max_size,
            symbol_set_key=symbol_set,
            cell_delimiter="",
        )

        print(f"\nTesting with {symbol_set} symbol set:")

        results = test_individual_puzzles(puzzles, model)
        all_results.extend(results)

        correct_count = sum(1 for r in results if r["is_correct"])
        print(f"Individual testing: {correct_count} out of {len(puzzles)} correct")

        print("\nDetailed results:")
        for r in results:
            print(
                f"{r['index']}: Size: {r['size']}, Response: {r['model_response']}, Correct: {r['is_correct']}, Time: {r['processing_time']:.2f}s"
            )

    return all_results

```

## src/geometor/arcprize/perception/grids/random_full.py

```py
import random
import numpy as np

def generate_grid(width, height, symbol_set):
    return np.random.choice(list(symbol_set), size=(width, height))


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

## src/geometor/arcprize/perception/puzzles/random_rotate.py

```py

import random
import numpy as np
from jinja2 import Environment, PackageLoader


from geometor.arcprize.perception.grids.random_full import generate_grid
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


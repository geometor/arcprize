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

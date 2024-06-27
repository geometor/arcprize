import json
import os
from collections import Counter



class Grid:
    def __init__(self, matrix):
        self.matrix = matrix
        self.height = len(matrix)
        self.width = len(matrix[0]) if self.height > 0 else 0

    @property
    def size(self):
        return self.width * self.height

    @property
    def colors(self):
        return set(val for row in self.matrix for val in row)

    @property
    def color_counts(self):
        return Counter(val for row in self.matrix for val in row)


class Puzzle:
    def __init__(self, data):
        self.id = data.get("id", "")
        self.input = Grid(data["input"])
        self.output = Grid(data["output"])

    @property
    def weight(self):
        return self.input.size + self.output.size

    @property
    def size_change(self):
        return {
            "width": self.output.width - self.input.width,
            "height": self.output.height - self.input.height,
            "total": self.output.size - self.input.size,
        }

    @property
    def colors(self):
        return self.input.colors.union(self.output.colors)

    @property
    def color_changes(self):
        input_counts = self.input.color_counts
        output_counts = self.output.color_counts
        return {
            color: output_counts[color] - input_counts[color] for color in self.colors
        }


    def get_size_average(file_path):
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

class PuzzleSet:
    def __init__(self, folder_path):
        self.puzzles = self._load_puzzles(folder_path)

    def _load_puzzles(self, folder_path):
        puzzles = []
        for filename in os.listdir(folder_path):
            if filename.endswith(".json"):
                with open(os.path.join(folder_path, filename), "r") as f:
                    data = json.load(f)
                    puzzles.extend([Puzzle(sample) for sample in data["train"]])
                    puzzles.extend([Puzzle(sample) for sample in data["test"]])
        return puzzles

    def get_ordered_puzzles(self, key="weight", reverse=False):
        return sorted(self.puzzles, key=lambda p: getattr(p, key), reverse=reverse)

    def get_puzzles_by_color_count(self, count):
        return [p for p in self.puzzles if len(p.colors) == count]

    def get_puzzles_by_size_change(self, change_type="total", value=0):
        return [p for p in self.puzzles if p.size_change[change_type] == value]


# Usage example:
if __name__ == "__main__":
    puzzle_set = PuzzleSet("path/to/puzzles/folder")

    # Get puzzles ordered by weight
    ordered_puzzles = puzzle_set.get_ordered_puzzles()

    # Get puzzles with exactly 3 colors
    three_color_puzzles = puzzle_set.get_puzzles_by_color_count(3)

    # Get puzzles where the total size doesn't change
    no_size_change_puzzles = puzzle_set.get_puzzles_by_size_change("total", 0)

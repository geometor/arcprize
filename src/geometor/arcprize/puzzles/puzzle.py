"""
tools to parse and render ARC puzzles from JSON

key elements:

- :class:`PuzzleSet <geometor.arcprize.puzzles.puzzle.PuzzleSet>`
- :class:`Puzzle <geometor.arcprize.puzzles.puzzle.Puzzle>`
- :class:`PuzzlePair <geometor.arcprize.puzzles.puzzle.PuzzlePair>`

"""
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

    def nice_json_layout(puzzle):
        def matrix_to_json_string(matrix):
            return (
                "[\n"
                + ",\n".join(f"          {row}" for row in matrix.tolist())
                + "\n        ]"
            )

        json_str = "{\n"
        json_str += f'  "id": "{puzzle.id}",\n'
        json_str += '  "train": [\n'
        for pair in puzzle.train:
            json_str += "    {\n"
            json_str += (
                '      "input": ' + matrix_to_json_string(pair.input.matrix) + ",\n"
            )
            json_str += (
                '      "output": ' + matrix_to_json_string(pair.output.matrix) + "\n"
            )
            json_str += "    },\n"
        json_str = json_str.rstrip(",\n") + "\n"
        json_str += "  ],\n"
        json_str += '  "test": [\n'
        for pair in puzzle.test:
            json_str += "    {\n"
            json_str += (
                '      "input": ' + matrix_to_json_string(pair.input.matrix) + ",\n"
            )
            if pair.output:
                json_str += (
                    '      "output": '
                    + matrix_to_json_string(pair.output.matrix)
                    + "\n"
                )
            else:
                json_str += '      "output": null\n'
            json_str += "    },\n"
        json_str = json_str.rstrip(",\n") + "\n"
        json_str += "  ]\n"
        json_str += "}"

        return json_str


class PuzzleSet:
    def __init__(self, folder_path="."):
        self.puzzles = self._load_puzzles(Path(folder_path))

    def _load_puzzles(self, folder_path):
        puzzles = []
        for file_path in sorted(folder_path.glob("*.json")):
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

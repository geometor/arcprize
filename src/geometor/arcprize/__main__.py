# src/geometor/arcprize/__main__.py

from geometor.arcprize.puzzles import PuzzleSet
from geometor.arcprize.img_gen import process_all_puzzles
from rich import print
from pathlib import Path
import json
import numpy as np


#  def matrix_to_json_string(matrix):
    #  return "[\n" + ",\n".join(f"        {row}" for row in matrix.tolist()) + "\n      ]"

def matrix_to_json_string(matrix):
    return "[\n" + ",\n".join(f"          {row}" for row in matrix.tolist()) + "\n        ]"


def generate_artifacts(puzzle_set, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for puzzle in puzzle_set.puzzles:
        puzzle_dir = output_dir / puzzle.id
        puzzle_dir.mkdir(exist_ok=True)

        # Generate folders and files for each train pair
        for i, pair in enumerate(puzzle.train, 1):
            pair_dir = puzzle_dir / f"train_{i}"
            pair_dir.mkdir(exist_ok=True)
            (pair_dir / "input.txt").write_text(pair.input.to_string())
            (pair_dir / "output.txt").write_text(pair.output.to_string())

        # Generate folders and files for each test pair
        for i, pair in enumerate(puzzle.test, 1):
            pair_dir = puzzle_dir / f"test_{i}"
            pair_dir.mkdir(exist_ok=True)
            (pair_dir / "input.txt").write_text(pair.input.to_string())
            if pair.output:
                (pair_dir / "output.txt").write_text(pair.output.to_string())

        # Generate JSON file
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
        json_path = puzzle_dir / f"{puzzle.id}.json"
        with json_path.open("w") as f:
            f.write(json_str)

    # Generate images
    process_all_puzzles(puzzle_set, output_dir)


def run():
    puzzle_set = PuzzleSet()
    print(f"Loaded {len(puzzle_set.puzzles)} puzzles")

    output_dir = Path("artifacts")
    generate_artifacts(puzzle_set, output_dir)
    print(f"Generated artifacts in {output_dir}")


if __name__ == "__main__":
    run()

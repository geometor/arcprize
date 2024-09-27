# src/geometor/arcprize/__main__.py

from geometor.arcprize.puzzles import PuzzleSet
from geometor.arcprize.img_gen import process_all_puzzles
from rich import print
from pathlib import Path
import json
import numpy as np

def matrix_to_json_string(matrix):
    return '[\n' + ',\n'.join(
        f'        {row}' for row in matrix.tolist()
    ) + '\n      ]'

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

        # Generate JSON file (unchanged)
        json_str = '{\n'
        # ... (rest of the JSON generation code remains the same)
        
        json_path = puzzle_dir / f"{puzzle.id}.json"
        with json_path.open('w') as f:
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

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
        print(
            f"Number of test inputs with outputs: {sum(1 for test in puzzle.test if test.output is not None)}"
        )
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

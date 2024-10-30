from geometor.arcprize.puzzles import Puzzle, PuzzleSet, Grid
from rich import print
from datetime import datetime
from pathlib import Path
import json
import numpy as np
import os
from gemini_reporter import Reporter
from gemini_solver import PuzzleSolver

#  def solve_all_puzzles(puzzle_set):
    #  output_dir = create_output_dir()
    #  print(f"Output directory: {output_dir}")

    #  for puzzle in puzzle_set.puzzles:
        #  solve_puzzle(puzzle, output_dir)


def run():
    puzzle_set = PuzzleSet()
    print(f"Loaded {len(puzzle_set.puzzles)} puzzles")

    #  output_dir = create_output_dir()
    #  solve_all_puzzles(puzzle_set)
    #  solve_puzzle(puzzle_set.puzzles[0], output_dir)
    solver = PuzzleSolver(puzzle_set.puzzles[0])
    solver.solve()


if __name__ == "__main__":
    run()


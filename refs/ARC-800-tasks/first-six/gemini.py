from geometor.arcprize.puzzles import Puzzle, PuzzleSet, Grid
from rich import print
from pathlib import Path
import json
import numpy as np
import os

import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])


def get_model():
    instruction = """You are now analyzing an ARC (Abstraction and Reasoning Corpus) puzzle.
        We will examine each training pair one at a time. For each pair:
        1. Look carefully at the input and output grids
        2. Share your observations about the transformation
        3. Note any patterns or relationships you notice

        After we review all pairs:
        1. Synthesize your observations into transformation rules
        2. Apply these rules to generate a solution for the test input

        Grid values represent colors using this mapping:
        """

    model = genai.GenerativeModel(
        "models/gemini-1.5-flash", system_instruction=instruction
    )

    return model


def matrix_to_json_string(matrix):
    return "[\n" + ",\n".join(f"          {row}" for row in matrix.tolist()) + "\n        ]"


def solve_all_puzzles(puzzle_set, output_dir):
    #  output_dir = Path(output_dir)
    #  output_dir.mkdir(parents=True, exist_ok=True)

    for puzzle in puzzle_set.puzzles:
        solve_puzzle(puzzle)


def solve_puzzle(puzzle):
    model = get_model()


    chat = model.start_chat(
        history=[
            {"role": "user", "parts": f"Begin puzzle: {puzzle.id}"},
            {"role": "model", "parts": "Ready"},
        ]
    )

    print('-' * 40)
    print(puzzle.id)
    # Generate folders and files for each train pair
    for i, pair in enumerate(puzzle.train, 1):
        prompt = [
            f"train_{i}\n\n",
            f"input\n\n",
            pair.input.to_string(),
            f"\n\n",
            pair.input.to_image(),
            f"output\n\n",
            pair.output.to_string(),
            f"\n\n",
            pair.output.to_image(),
            ]
        print(prompt)
        response = chat.send_message(prompt)
        print(response.text)
        print(response.usage_metadata)
        print(response)

    print( chat.history )
    # Generate folders and files for each test pair
    for i, pair in enumerate(puzzle.test, 1):
        pair = f"test_{i}"
        #  (pair_dir / "input.txt").write_text(pair.input.to_string())
        #  if pair.output:
            #  (pair_dir / "output.txt").write_text(pair.output.to_string())




def run():
    puzzle_set = PuzzleSet()
    print(f"Loaded {len(puzzle_set.puzzles)} puzzles")

    output_dir = Path("logs")
    #  solve_all_puzzles(puzzle_set, output_dir)
    solve_puzzle(puzzle_set.puzzles[0])
    print(f"puzzle logs in {output_dir}")


if __name__ == "__main__":
    run()

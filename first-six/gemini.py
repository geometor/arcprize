from geometor.arcprize.puzzles import Puzzle, PuzzleSet, Grid
from rich import print
from pathlib import Path
import json
import numpy as np
import os

import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])


def get_model():
    with open("gemini_instructions.md", "r") as f:
        instruction = f.read().strip()

    model = genai.GenerativeModel(
        "models/gemini-1.5-flash", system_instruction=instruction
    )

    return model


def solve_all_puzzles(puzzle_set, output_dir):
    #  output_dir = Path(output_dir)
    #  output_dir.mkdir(parents=True, exist_ok=True)

    for puzzle in puzzle_set.puzzles:
        solve_puzzle(puzzle)


def log_response(response):
    print("-" * 10)
    print(response.text)
    print(response.usage_metadata)


def solve_puzzle(puzzle):
    model = get_model()

    chat = model.start_chat(
        history=[
            {"role": "user", "parts": f"Begin puzzle: {puzzle.id}"},
            {"role": "model", "parts": "Ready"},
        ],
        #  enable_automatic_function_calling=True
    )

    print("-" * 40)
    print(puzzle.id)

    for i, pair in enumerate(puzzle.train, 1):
        prompt = [
            f"train_{i}\n",
            f"input\n",
            #  pair.input.to_string(),
            str(pair.input.grid),
            f"\n\n",
            pair.input.to_image(),
            f"\n\n",
            f"output\n",
            #  pair.output.to_string(),
            str(pair.output.grid),
            f"\n\n",
            pair.output.to_image(),
            f"\n\n",
            "you may generate and run code to closely examine the patterns and differences in the grids",
        ]
        for p in prompt:
            print(p)

        response = chat.send_message(prompt, tools="code_execution")
        log_response(response)

    prompt = [
            "summarize your observations to explain the transformation of the input to output",
            "you may generate and run code to closely examine the patterns and differences in the grids",
            ]
    response = chat.send_message(prompt, tools="code_execution")
    log_response(response)
    #  print(response)

    # test functions
    working_grid = []

    def initialize_output_from_input() -> str:
        """
        initialize the test output grid with a copy of the input grid
        """
        nonlocal working_grid
        from copy import copy
        working_grid = copy(puzzle.test[0].input)
        print("copy_input")
        return "input copied"

    def initilize_output_by_size(width: int, height: int, color: int = 0) -> str:
        """
        initialize the test output grid with a specific width and height filled with a color
        """
        # TODO: initialize grid with default color
        new_grid = np.full((int(height), int(width)), int(color))
        nonlocal working_grid
        working_grid = Grid(new_grid, puzzle.id, "test", 0, "output")
        print("set_grid")
        return "grid set"

    def set_pixel(row: int, column: int, color: int) -> str:
        """
        set grid value at coordinate
        """
        # TODO: set value in working_grid
        nonlocal working_grid
        working_grid.grid[int(row), int(column)] = color
        print("set_pixel")
        return "pixel set"

    def set_range(row1: int, column1: int, row2: int, column2: int, color: int) -> str:
        """
        set grid values for a range of pixels
        """
        nonlocal working_grid
        r1 = int(row1)
        c1 = int(column1)
        r2 = int(row2)
        c2 = int(column2)
        working_grid.matrix[r1:r2, c1:c2] = color
        print("set_range")
        return "range set"

    def set_contiguous(row: int, column: int, color: int) -> str:
        """
        set all contiguous pixels that are the same color as selected pixel 

        """
        # TODO: set contiguous values - find all pixels
        nonlocal working_grid
        #  working_grid.matrix[int(row), int(column)] = color
        print("set_contiguous")
        return "contiguous set"

    def submit() -> str:
        """
        set the working grid as complete and check for correctness
        """
        print("submit")
        return "submit"

    # parse the function call and run it
    def call_function(function_call, functions):
        function_name = function_call.name
        function_args = function_call.args
        return functions[function_name](**function_args)

    # test ##############################

    # present test input
    test_pair = puzzle.test[0]
    prompt = [
        f"test\n\n",
        f"input\n\n",
        test_pair.input.to_string(),
        f"\n\n",
        test_pair.input.to_image(),
        f"\n\n",
        "summarize your observations to explain the transformation of the input to output",
        "you may generate and run code to closely examine the patterns and differences in the grids",
    ]
    response = chat.send_message(
        prompt,
        tools="code_execution",
    )
    log_response(response)

    # initialize working grid
    prompt = [
        "initialize the working output grid",
    ]
    functions = {
        "initialize_output_from_input": initialize_output_from_input,
        "initilize_output_by_size": initilize_output_by_size,
    }
    response = chat.send_message(
        prompt,
        tools=functions.values(),
    )
    #  print(response)
    #  log_response(response)

    part = response.candidates[0].content.parts[0]
    if part.function_call:
        result = call_function(part.function_call, functions)

    print(result)

    # set pixels
    functions = {
        "set_pixel": set_pixel,
        "set_range": set_range,
        #  "set_contiguous": set_contiguous,
        "submit": submit,
        # TODO: add undo last
    }

    for _ in range(5):
        prompt = [
            f"working output grid\n\n",
            working_grid.to_string(),
            f"\n\n",
            working_grid.to_image(),
            f"\n\n",
            # TODO: better instructions
            "begin setting pixels on the grid to achieve the desired output to match the transformation rules",
            "when you think you have completed the output, call the submit function",
        ]

        response = chat.send_message(
            prompt,
            tools=functions.values(),
        )
        #  print(response)
        #  log_response(response)

        part = response.candidates[0].content.parts[0]
        if part.function_call:
            result = call_function(part.function_call, functions)

        if result == "submit":
            break

        print(result)

    print("\n\nHISTORY")
    print(chat.history)


def run():
    puzzle_set = PuzzleSet()
    print(f"Loaded {len(puzzle_set.puzzles)} puzzles")

    output_dir = Path("logs")
    #  solve_all_puzzles(puzzle_set, output_dir)
    solve_puzzle(puzzle_set.puzzles[0])
    #  print(f"puzzle logs in {output_dir}")


if __name__ == "__main__":
    run()

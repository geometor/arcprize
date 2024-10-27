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


def solve_all_puzzles(puzzle_set):
    for puzzle in puzzle_set.puzzles:
        solve_puzzle(puzzle)


def log_response(response):
    print("-" * 10)
    print(response.text)
    print(response.usage_metadata)


class PuzzleSolver:
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.working_grid = None

    def initialize_output_from_input(self) -> str:
        """
        Initialize the test output grid with a copy of the input grid.
        """
        from copy import deepcopy

        self.working_grid = deepcopy(self.puzzle.test[0].input)
        return "input copied"

    def initilize_output_by_size(self, width: int, height: int, color: int = 0) -> str:
        """
        Initialize the test output grid with a specific width and height filled
        with a color.  
        """
        new_grid = np.full((int(height), int(width)), int(color))
        self.working_grid = Grid(new_grid, self.puzzle.id, "test", 0, "output")
        return "grid set"

    def set_pixel(self, row: int, column: int, color: int) -> str:
        """
        Set grid value at a specific coordinate.
        """
        self.working_grid.grid[int(row), int(column)] = int(color)
        return "pixel set"

    #  def set_range(
        #  self, row1: int, column1: int, row2: int, column2: int, color: int
    #  ) -> str:
        #  """
        #  Set grid values for a range of pixels.
        #  """
        #  r1 = int(row1)
        #  c1 = int(column1)
        #  r2 = int(row2)
        #  c2 = int(column2)
        #  self.working_grid.grid[r1:r2, c1:c2] = int(color)
        #  breakpoint()
        #  print("set_range")
        #  return "range set"

    def set_range(self, row1: int, column1: int, row2: int, column2: int, color: int) -> str:
        """
        Set grid values for a range of pixels by iterating through each cell.

        Args:
            row1: Starting row (inclusive)
            column1: Starting column (inclusive)
            row2: Ending row (inclusive)
            column2: Ending column (inclusive)
            color: Color value to set
        """
        # Convert to int and ensure proper order
        r1, r2 = sorted([int(row1), int(row2)])
        c1, c2 = sorted([int(column1), int(column2)])

        # Add 1 to end indices to make them inclusive
        r2 += 1
        c2 += 1

        # Ensure we're within grid bounds
        height, width = self.working_grid.grid.shape
        r1 = max(0, min(r1, height))
        r2 = max(0, min(r2, height))
        c1 = max(0, min(c1, width))
        c2 = max(0, min(c2, width))

        # Iterate through each cell in the range
        for row in range(r1, r2):
            for col in range(c1, c2):
                self.working_grid.grid[row, col] = int(color)

        cells_modified = (r2 - r1) * (c2 - c1)
        print(f"set_range: {cells_modified} cells modified from ({r1},{c1}) to ({r2-1},{c2-1})")
        return "range set"


    def set_contiguous(self, row: int, column: int, color: int) -> str:
        """
        Set all contiguous pixels that are the same color as the selected pixel.
        """
        # Implement contiguous pixel setting
        print("set_contiguous")
        return "contiguous set"

    def submit(self) -> str:
        """
        Submit the working grid and check for correctness.
        """
        print("submit")
        return "submit"


def solve_puzzle(puzzle):
    model = get_model()
    conversation_log = []

    chat = model.start_chat(
        history=[
            {"role": "user", "parts": f"Begin puzzle: {puzzle.id}"},
            {"role": "model", "parts": "Ready"},
        ],
    )

    conversation_log.extend(chat.history)

    print("-" * 40)
    print(puzzle.id)

    # Process training examples
    for i, pair in enumerate(puzzle.train, 1):
        prompt = [
            f"train_{i}\ninput\n{str(pair.input.grid)}\n\n",
            pair.input.to_image(),
            f"\noutput\n{str(pair.output.grid)}\n\n",
            pair.output.to_image(),
            f"\n\n",
            "you may generate and run code to closely examine the patterns and differences in the grids",
        ]
        print(prompt)
        conversation_log.append({"role": "user", "content": prompt})

        response = chat.send_message(prompt, tools="code_execution")
        log_response(response)
        conversation_log.append({"role": "model", "content": response.text})

    # Summarize observations
    prompt = [
        "summarize your observations to explain the transformation of the input to output",
        "you may generate and run code to closely examine the patterns and differences in the grids",
    ]
    conversation_log.append({"role": "user", "content": prompt})
    response = chat.send_message(prompt, tools="code_execution")
    log_response(response)
    conversation_log.append({"role": "model", "content": response.text})

    # Initialize PuzzleSolver
    solver = PuzzleSolver(puzzle)

    # Define functions for initialization
    functions = {
        "initialize_output_from_input": solver.initialize_output_from_input,
        "initilize_output_by_size": solver.initilize_output_by_size,
    }

    # Present test input
    test_pair = puzzle.test[0]
    prompt = [
        f"test\n\n",
        f"input\n\n",
        str(test_pair.input.grid),
        f"\n\n",
        test_pair.input.to_image(),
        f"\n\n",
        "summarize your observations to explain the transformation of the input to output",
        "you may generate and run code to closely examine the patterns and differences in the grids",
    ]
    #  prompt_text = ''.join(prompt)
    response = chat.send_message(
        prompt,
        tools="code_execution",
    )
    log_response(response)
    #  conversation_log.append({'role': 'user', 'content': prompt})
    #  conversation_log.append({'role': 'model', 'content': response.text})

    # Initialize working grid
    prompt = [
        "initialize the working output grid",
    ]
    response = chat.send_message(
        prompt,
        tools=functions.values(),
    )
    #  log_response(response)
    #  conversation_log.append({'role': 'user', 'content': prompt})

    # Process function call
    function_call = response.candidates[0].content.parts[0].function_call
    if function_call:
        result = call_function(function_call, functions, conversation_log)

    print(result)

    # Define functions for setting pixels
    functions = {
        "set_pixel": solver.set_pixel,
        "set_range": solver.set_range,
        "set_contiguous": solver.set_contiguous,
        "submit": solver.submit,
        # TODO: add undo last
    }

    # Interaction loop
    for loop in range(5):
        print("LOOP:", loop)
        # first present the current working grid
        prompt = [
            f"working output grid\n\n",
            str(solver.working_grid.grid),
            f"\n\n",
            solver.working_grid.to_image(),
            f"\n\n",
            "assess current state",
            #  "you can use code execution to analyze",
        ]
        response = chat.send_message(
            prompt,
            #  tools="code_execution",
        )
        log_response(response)
        #  conversation_log.append({'role': 'user', 'content': prompt})

        # next select the function for next update
        prompt = [
            "select next function to update the working grid",
            "when you think you have completed the output, call the submit function",
        ]
        response = chat.send_message(
            prompt,
            tools=functions.values(),
        )
        #  conversation_log.append({'role': 'user', 'content': prompt})

        # Process function call
        function_call = response.candidates[0].content.parts[0].function_call
        print(function_call)
        if function_call:
            result = call_function(function_call, functions, conversation_log)

        print(result)
        if result == "submit":
            break

    print("\n\nHISTORY")
    print(chat.history)
    #  breakpoint()

    generate_report(chat.history, puzzle.id)

    # Save conversation log to JSON
    output_dir = Path("logs")
    output_dir.mkdir(parents=True, exist_ok=True)
    #  with open(output_dir / f"{puzzle.id}_conversation.json", "w") as f:
    #  json.dump(conversation_log, f, indent=2)
    #  with open(output_dir / f"{puzzle.id}_history.json", "w") as f:
    #  json.dump(chat.history, f, indent=2)


def call_function(function_call, functions, conversation_log):
    function_name = function_call.name
    function_args = function_call.args
    result = functions[function_name](**function_args)
    # Log the function call and result
    conversation_log.append(
        {
            "function_call": {
                "name": function_name,
                "args": function_args,
                "result": result,
            }
        }
    )
    return result


from jinja2 import Template
import os
import base64


def clean_base64(data):
    """Clean and format base64 data for HTML embedding"""
    if isinstance(data, bytes):
        # Convert raw bytes directly to base64
        return base64.b64encode(data).decode("utf-8")
    elif isinstance(data, str):
        if data.startswith("b'") or data.startswith('b"'):
            # Remove b prefix and quotes
            raw_str = data[2:-1]
            # Convert escaped bytes to actual bytes
            byte_str = bytes(raw_str, "utf-8").decode("unicode-escape").encode("latin1")
            # Convert to base64
            return base64.b64encode(byte_str).decode("utf-8")
    return data


def generate_report(chat_history, puzzle_id):
    """Generate HTML report from chat history"""
    # Read template
    template_path = "gemini_report_2.html.j2"
    with open(template_path) as f:
        template = Template(f.read())

    # Register the custom filter
    template.environment.filters["clean_base64"] = clean_base64

    # Render template
    html = template.render(history=chat_history)

    # Save report
    output_dir = "reports"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"puzzle_{puzzle_id}.html")

    with open(output_path, "w") as f:
        f.write(html)

    return output_path


def run():
    puzzle_set = PuzzleSet()
    print(f"Loaded {len(puzzle_set.puzzles)} puzzles")

    #  solve_all_puzzles(puzzle_set)
    solve_puzzle(puzzle_set.puzzles[1])


if __name__ == "__main__":
    run()

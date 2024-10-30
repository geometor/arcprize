from geometor.arcprize.puzzles import Puzzle, PuzzleSet, Grid
from rich import print
from datetime import datetime
from pathlib import Path
import json
import numpy as np
import os
from gemini_reporter import Reporter
from google.api_core import retry

import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

DEFAULT_MODEL = "models/gemini-1.5-flash"
#  DEFAULT_MODEL = "models/gemini-1.5-flash-002"
#  DEFAULT_MODEL = "models/gemini-1.5-pro-002"
DEFAULT_INSTRUCTIONS_FILE = "gemini_instructions.md"


def get_model(model_name=DEFAULT_MODEL, instructions_file=DEFAULT_INSTRUCTIONS_FILE):
    with open(instructions_file, "r") as f:
        instruction = f.read().strip()

    model = genai.GenerativeModel(
        model_name,
        system_instruction=instruction,
    )

    return model


def create_output_dir():
    """Create timestamped output directory for reports and logs"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path("outputs") / timestamp

    # Create main output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Create subdirectories for different types of output
    (output_dir / "reports").mkdir(exist_ok=True)
    (output_dir / "logs").mkdir(exist_ok=True)

    return output_dir


def solve_all_puzzles(puzzle_set):
    output_dir = create_output_dir()
    print(f"Output directory: {output_dir}")

    for puzzle in puzzle_set.puzzles:
        solve_puzzle(puzzle, output_dir)


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
        return "initialize_output_from_input()"

    def initialize_output_by_size(self, width: int, height: int, color: int = 0) -> str:
        """
        Initialize the test output grid with a specific width and height filled
        with a color.
        """
        width = int(width)
        height = int(height)
        color = int(color)
        new_grid = np.full((height, width), int(color))
        self.working_grid = Grid(new_grid, self.puzzle.id, "test", 0, "output")
        return f"initialize_output_by_size({width=}, {height=}, {color=})"

    def set_pixel(self, row: int, column: int, color: int) -> str:
        """
        Set grid value at a specific coordinate.
        """
        height, width = self.working_grid.grid.shape
        row = int(row)
        column = int(column)
        color = int(color)

        if not (0 <= row < height):
            raise ValueError(f"Row {row} is out of bounds. Grid height is {height}")

        if not (0 <= column < width):
            raise ValueError(f"Column {column} is out of bounds. Grid width is {width}")

        self.working_grid.grid[row, column] = color
        return f"set_pixel({row=}, {column=}, {color=})"

    def set_range(
        self, row1: int, column1: int, row2: int, column2: int, color: int
    ) -> str:
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

        # Check if any part of the range is within bounds
        if (r1 >= height and r2 >= height) or (c1 >= width and c2 >= width):
            raise ValueError(f"Entire range is outside grid bounds ({height}x{width})")

        r1 = max(0, min(r1, height))
        r2 = max(0, min(r2, height))
        c1 = max(0, min(c1, width))
        c2 = max(0, min(c2, width))

        # Iterate through each cell in the range
        for row in range(r1, r2):
            for col in range(c1, c2):
                self.working_grid.grid[row, col] = int(color)

        cells_modified = (r2 - r1) * (c2 - c1)
        print(
            f"set_range: {cells_modified} cells modified from ({r1},{c1}) to ({r2-1},{c2-1})"
        )
        return f"set_range({row1}, {column1}, {row2}, {column2}, {color}) -> str:"

    def set_contiguous(self, row: int, column: int, color: int) -> str:
        """
        Set all contiguous pixels that are the same color as the selected pixel.
        """
        # TODO: Implement contiguous pixel setting
        print("set_contiguous")
        return "contiguous set"

    def submit(self) -> str:
        """
        Submit the working grid and check for correctness.
        """
        print("submit")
        return "submit"


def solve_puzzle(puzzle, output_dir):
    model = get_model()

    history = [
        f"Begin puzzle: {puzzle.id}\n\n",
    ]

    # Process training examples
    for i, pair in enumerate(puzzle.train, 1):
        prompt = [
            f"# example_{i}\n",
            "## input:\n",
            str(pair.input.grid),
            "\n",
            pair.input.to_image(),
            "\n",
            "## output:\n",
            str(pair.output.grid),
            "\n",
            pair.output.to_image(),
            "\n",
            "## observations:\n",
        ]
        # TODO: seeking natural language patterns
        instructions = [
            "- review the example grids\n",
            "- check for differences and patterns\n",
        ]
        history = generate_content(
            model,
            history,
            prompt,
            instructions,
            tools="code_execution",
            functions=None,
            output_dir=output_dir,
        )

    # Summarize observations
    prompt = [
        "# examples summary: \n",
    ]
    instructions = [
        "- summarize your observations to explain the transformation of the input to output\n",
        "- use code_execution to investigate properties, patterns and differences in the grids",
    ]
    history = generate_content(
        model,
        history,
        prompt,
        instructions,
        tools="code_execution",
        functions=None,
        output_dir=output_dir,
    )

    solver = PuzzleSolver(puzzle)

    # Present test input
    test_pair = puzzle.test[0]
    prompt = [
        "# test\n",
        "## input\n",
        str(test_pair.input.grid),
        "\n",
        test_pair.input.to_image(),
        "\n",
        "## observations:\n",
    ]
    instructions = [
        "- generate report as per instructions\n",
        "- use code_execution to investigate properties",
    ]
    history = generate_content(
        model,
        history,
        prompt,
        instructions,
        tools="code_execution",
        functions=None,
        output_dir=output_dir,
    )

    # Initialize working grid
    init_functions = {
        "initialize_output_from_input": solver.initialize_output_from_input,
        "initialize_output_by_size": solver.initialize_output_by_size,
    }
    prompt = [
        "## initialize the working output grid\n",
    ]
    instructions = [
        "select a function to start:\n",
        "- initialize_output_from_input: good when examples show few differences between input and output\n",
        "- initialize_output_by_size: create a fresh grid from size and color\n",
    ]
    history = generate_content(
        model,
        history,
        prompt,
        instructions,
        tools=init_functions.values(),
        functions=init_functions,
        output_dir=output_dir,
    )

    # Define functions for setting pixels
    set_functions = {
        "set_pixel": solver.set_pixel,
        "set_range": solver.set_range,
        #  "set_contiguous": solver.set_contiguous,
        "submit": solver.submit,
        # TODO: add undo last
    }

    # Interaction loop
    for loop in range(5):
        print("LOOP:", loop)
        # first present the current working grid
        prompt = [
            "# working output grid\n",
            "updated with your changes\n",
            str(solver.working_grid.grid),
            "\n",
            solver.working_grid.to_image(),
            "\n",
        ]
        instructions = [
            "- take a moment to review that the changes are in keeping with the rule\n",
            "- use code_execution to investigate properties",
        ]
        history = generate_content(
            model,
            history,
            prompt,
            instructions,
            tools="code_execution",
            functions=None,
            output_dir=output_dir,
        )

        # next select the function for next update
        prompt = [
            "select the next function to update the working grid\n",
            "when you think you have completed the output, call the submit function\n",
        ]
        instructions = [
            "- take a moment to review that the changes are in keeping with the rule\n",
            "- use code_execution to investigate properties",
        ]
        history = generate_content(
            model,
            history,
            prompt,
            instructions,
            tools=set_functions.values(),
            functions=set_functions,
            output_dir=output_dir,
        )

        # TODO: still need to break on submit here


    reporter = Reporter()
    #  report_path = reporter.generate(chat.history, puzzle.id, output_dir=output_dir)
    #  print("report path:", report_path)


def call_function(function_call, functions):
    function_name = function_call.name
    function_args = function_call.args
    result = functions[function_name](**function_args)
    return result


def generate_content(model, history, prompt, instructions, tools=None, functions=None, output_dir=None):
    """
    Generate content from the model with standardized logging.

    Args:
        model: The Gemini model instance
        prompt_parts: List of content parts to send to model
        tools: Optional tools configuration
        output_dir: Optional output directory for logging

    Returns:
        The model's response
    """
    # Log the prompt
    print("=" * 40)
    print("PROMPT:")
    #  print("-" * 20)
    for part in prompt:
        print(part)

    total_prompt = history + prompt + instructions
    history = history + prompt
    try:
        # Generate the response
        response = model.generate_content(total_prompt, tools=tools, request_options={'retry':retry.Retry()})

        # TODO: part parser function
        response_parts = []
        if hasattr(response.candidates[0].content, "parts"):
            for part in response.candidates[0].content.parts:
                if part.text:
                    response_parts.append(part.text + "\n")
                if part.executable_code:
                    response_parts.append("code_execution:\n")
                    # TODO: set language
                    response_parts.append(
                        f"```python\n{ part.executable_code.code }\n```\n"
                    )
                if part.code_execution_result:
                    response_parts.append(
                        f"code_execution_result: {part.code_execution_result.outcome}\n"
                    )
                    response_parts.append(
                        f"```\n{ part.code_execution_result.output }\n```\n"
                    )
                if part.function_call:
                    response_parts.append("function_call:\n")
                    response_parts.append(part.function_call.name + "\n")
                    for arg, arg_value in part.function_call.args.items():
                        response_parts.append(part.function_call.name + "\n")
                    result = call_function(part.function_call, functions)
                    response_parts.append("\nresult:\n")
                    response_parts.append(result + "\n")

                    print(result)
                    if result == "submit":
                        break

        # Log the response
        print("\nRESPONSE:")
        print("-" * 20)
        print(f"{response_parts}")
        history = history + response_parts

        # Log detailed response data if output directory is provided
        if output_dir:
            timestamp = datetime.now().strftime("%y.%j.%H%M%S")
            log_file = output_dir / "logs" / f"response_{timestamp}.json"

            # Extract serializable data from response
            log_data = {
                "timestamp": timestamp,
                "usage": str(response.usage_metadata),
                "total_prompt": total_prompt,
                "response": response_parts,
            }

            log_data = serialize_for_log(total_prompt, response_parts)
            with open(log_file, "w") as f:
                json.dump(log_data, f, indent=2)

        return history

    except Exception as e:
        print(f"\nERROR generating content: {str(e)}")
        if output_dir:
            error_file = (
                output_dir
                / "logs"
                / f"error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            )
            with open(error_file, "w") as f:
                f.write(f"Error generating content: {str(e)}\n")
                f.write(f"Prompt:\n")
                for part in prompt:
                    f.write(f"{str(part)}\n")
        raise


def serialize_prompt_part(part):
    """
    Convert a prompt part into a serializable format.

    Args:
        part: A prompt part that could be string, PIL.Image, or other type

    Returns:
        A serializable representation of the part
    """
    import PIL.Image

    if isinstance(part, PIL.Image.Image):
        return f"<Image: size={part.size} mode={part.mode}>"
    elif isinstance(part, str):
        return part
    else:
        return str(part)


def serialize_for_log(prompt_parts, response_parts):
    """
    Prepare prompt and response data for JSON serialization.

    Args:
        prompt_parts: List of prompt parts
        response: Model response object

    Returns:
        Dict of serializable data
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    return {
        "timestamp": timestamp,
        "prompt": [serialize_prompt_part(p) for p in prompt_parts],
        "response": response_parts,
    }




def run():
    puzzle_set = PuzzleSet()
    print(f"Loaded {len(puzzle_set.puzzles)} puzzles")

    output_dir = create_output_dir()
    solve_all_puzzles(puzzle_set)
    #  solve_puzzle(puzzle_set.puzzles[0], output_dir)


if __name__ == "__main__":
    run()

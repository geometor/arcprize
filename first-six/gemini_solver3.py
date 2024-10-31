from rich import print
from datetime import datetime
from pathlib import Path
import json
import numpy as np
import os

from geometor.arcprize.puzzles import Puzzle, PuzzleSet, Grid

from gemini_client import GeminiClient as Client
from gemini_logger4 import Logger
#  from gemini_reporter import Reporter

#  DEFAULT_MODEL = "models/gemini-1.5-flash"
DEFAULT_MODEL = "models/gemini-1.5-flash-002"
#  DEFAULT_MODEL = "models/gemini-1.5-pro-002"
DEFAULT_INSTRUCTIONS_FILE = "gemini_instructions.md"


class PuzzleSolver:
    def __init__(
        self,
        puzzle,
        model_name: str = DEFAULT_MODEL,
        instructions_file: str = DEFAULT_INSTRUCTIONS_FILE,
        output_dir: str = ".",
        max_iterations: int = 5,
        timestamp: str = None,
        client: Client = None,
        logger: Logger = None,
    ):
        """
        Initialize the PuzzleSolver with all necessary components for solving and logging.

        Args:
            puzzle: The puzzle object to solve.
            model_name: Name of the Gemini model to use.
            instructions_file: Path to the instructions file.
            output_dir: Directory for output files and logs.
            max_iterations: Maximum number of iterations for solving.
            timestamp: Optional timestamp for logging (defaults to current time).
            client: An instance of Client.
            logger: An instance of Logger.
        """
        # Core components
        self.puzzle = puzzle
        self.model_name = model_name
        self.instructions_file = instructions_file
        self.max_iterations = max_iterations
        self.call_count = 0
        self.current_iteration = 0

        # Initialize GeminiClient
        self.client = client or Client(model_name, instructions_file)

        # Initialize timestamp
        self.timestamp = timestamp or datetime.now().strftime("%y.%j.%H%M%S")

        # Initialize Logger
        self.logger = logger or Logger(
            output_dir, puzzle.id, self.timestamp, 
        )

        # Initialize working state
        self.working_grid = None
        self.history = []

        # Initialize metadata for logging
        self.metadata = {
            "puzzle_id": puzzle.id,
            "model": model_name,
            "timestamp": self.timestamp,
            "max_iterations": max_iterations,
            "history": [],
            "grid_states": [],
            "function_calls": [],
        }

    def initialize_output_from_input(self) -> str:
        """Initialize the test output grid with a copy of the input grid."""
        from copy import deepcopy

        self.working_grid = deepcopy(self.puzzle.test[0].input)
        print(str(self.working_grid.grid))

        # Log the initialization
        #  self.logger.log_grid_state("initialization", "copy_input")
        return "initialize_output_from_input()"

    def initialize_output_by_size(self, width: int, height: int, color: int = 0) -> str:
        """Initialize the test output grid with specific dimensions."""

        width, height, color = int(width), int(height), int(color)
        new_grid = np.full((height, width), color)
        self.working_grid = Grid(new_grid, self.puzzle.id, "test", 0, "output")
        print(str(self.working_grid.grid))

        # Log the initialization
        #  self.logger.log_grid_state("initialization", f"new_grid_{width}x{height}")
        return f"initialize_output_by_size({width=}, {height=}, {color=})"

    def set_pixel(self, row: int, column: int, color: int) -> str:
        """Set grid value at a specific coordinate."""
        if self.working_grid is None:
            raise ValueError("Working grid not initialized")

        height, width = self.working_grid.grid.shape
        row, column, color = int(row), int(column), int(color)

        if not (0 <= row < height):
            raise ValueError(f"Row {row} is out of bounds. Grid height is {height}")
        if not (0 <= column < width):
            raise ValueError(f"Column {column} is out of bounds. Grid width is {width}")

        self.working_grid.grid[row, column] = color

        # Log the pixel change
        #  self.logger.log_grid_state("pixel_set", f"r{row}c{column}={color}")
        return f"set_pixel({row=}, {column=}, {color=})"

    def set_range(
        self, row1: int, column1: int, row2: int, column2: int, color: int
    ) -> str:
        """Set grid values for a range of pixels."""
        if self.working_grid is None:
            raise ValueError("Working grid not initialized")

        # Convert to int and ensure proper order
        r1, r2 = sorted([int(row1), int(row2)])
        c1, c2 = sorted([int(column1), int(column2)])
        color = int(color)

        # Add 1 to end indices to make them inclusive
        r2 += 1
        c2 += 1

        # Validate bounds
        height, width = self.working_grid.grid.shape
        if (r1 >= height and r2 >= height) or (c1 >= width and c2 >= width):
            raise ValueError(f"Entire range is outside grid bounds ({height}x{width})")

        r1 = max(0, min(r1, height))
        r2 = max(0, min(r2, height))
        c1 = max(0, min(c1, width))
        c2 = max(0, min(c2, width))

        # Set the range
        for row in range(r1, r2):
            for col in range(c1, c2):
                self.working_grid.grid[row, col] = color

        # Log the range change
        cells_modified = (r2 - r1) * (c2 - c1)
        #  self.logger.log_grid_state(
            #  "range_set", f"from_r{r1}c{c1}_to_r{r2-1}c{c2-1}={color}"
        #  )

        return f"set_range({row1}, {column1}, {row2}, {column2}, {color})"

    def submit(self) -> str:
        """Submit the working grid and check for correctness."""
        if self.working_grid is None:
            raise ValueError("No working grid to submit")

        # TODO: Implement actual submission logic and correctness checking
        #  self.logger.log_grid_state("submission", "final")
        return "submit"

    def solve(self):
        """
        Main method to orchestrate the puzzle solving workflow.
        Returns the working grid if solution is found, None otherwise.
        """
        try:
            # Initialize solving state
            self.history = [f"Begin puzzle: {self.puzzle.id}\n\n"]

            self._process_training_examples()
            self._summarize_observations()
            self._process_test_input()
            self._initialize_working_grid()
            self._run_solution_loop()

        except Exception as e:
            print(f"Solve failed: {str(e)}")
            self.logger.log_error(f"Solve failed: {str(e)}", self.history)
            raise

    def _process_training_examples(self):
        for i, pair in enumerate(self.puzzle.train, 1):
            prompt = [
                f"**example_{i}**\n",
                "**input**\n",
                str(pair.input.grid),
                "\n",
                pair.input.to_image(),
                "\n",
                "**output**\n",
                str(pair.output.grid),
                "\n",
                pair.output.to_image(),
                "\n",
                "**observations**\n",
            ]
            instructions = [
                "- review the example grids\n",
                "- check for differences and patterns\n",
            ]
            self._generate_content(
                prompt,
                instructions,
                tools="code_execution",
            )

    def _summarize_observations(self):
        prompt = [
            "**examples summary**\n",
        ]
        instructions = [
            "- summarize your observations to explain the transformation of the input to output\n",
            "- use code_execution to investigate properties, patterns and differences in the grids",
        ]
        self._generate_content(
            prompt,
            instructions,
            tools="code_execution",
        )

    def _process_test_input(self):
        test_pair = self.puzzle.test[0]
        prompt = [
            "**test**\n",
            "**input**\n",
            str(test_pair.input.grid),
            "\n",
            test_pair.input.to_image(),
            "\n",
            "**observations:**\n",
        ]
        instructions = [
            "- generate report as per instructions\n",
            "- use code_execution to investigate properties",
        ]
        self._generate_content(
            prompt,
            instructions,
            tools="code_execution",
        )

    def _initialize_working_grid(self):
        init_functions = {
            "initialize_output_from_input": self.initialize_output_from_input,
            "initialize_output_by_size": self.initialize_output_by_size,
        }
        prompt = [
                "**initialize the working output grid:**\n",
        ]
        instructions = [
            "use function_call to initialize the working output grid:\n",
            "- initialize_output_from_input: good when examples show few differences between input and output\n",
            "- initialize_output_by_size: create a fresh grid from size and color\n",
        ]
        self._generate_content(
            prompt,
            instructions,
            tools=init_functions.values(),
            functions=init_functions,
        )

    def _present_working_grid(self):
        prompt = [
            "**working output grid**\n",
            "updated with your changes\n",
            str(self.working_grid.grid),
            "\n",
            self.working_grid.to_image(),
            "\n",
        ]
        instructions = [
            "- take a moment to review that the changes in the working output grid are in keeping with the rule\n",
            "- use code_execution to investigate properties",
        ]
        self._generate_content(
            prompt,
            instructions,
            tools="code_execution",
        )

    def _run_solution_loop(self):
        """
        Run the main solution loop with proper submission handling.
        Returns the working grid if solution is found, None otherwise.
        """
        set_functions = {
            "set_pixel": self.set_pixel,
            "set_range": self.set_range,
            "submit": self.submit,
        }

        for iteration in range(self.max_iterations):
            self.current_iteration = iteration

            # Present and analyze current state
            self._present_working_grid()

            # Get next action
            result = self._get_next_action(set_functions)

            # Handle submission
            if result == "submit":
                print(f"Solution submitted after {iteration + 1} iterations")
                break

        print(f"Max iertions ({self.max_iterations}) reached without submission")
        return None

    def _get_next_action(self, functions):
        """
        Get and process the next action from the model.
        """
        prompt = ["**update working grid**\n"]
        instructions = [
            "- use function_call to set pixels on the grid to achieve the solution\n",
            "  - set_pixel: update one pixel at a time\n"
            "  - set_range: update a rectangular subset of pixel\n"
            "- when you think you have completed the output, call the submit function\n",
        ]

        return self._generate_content(
            prompt,
            instructions,
            tools=functions.values(),
            functions=functions,
        )

    def _generate_content(self, prompt, instructions, tools=None, functions=None):
        """
        Generate content from the model with standardized logging.
        """

        self.call_count += 1

        print("=" * 40)
        print("PROMPT:")
        for part in prompt:
            print(part)

        print("INSTRUCTIONS:")
        for part in instructions:
            print(part)

        self.logger.write_rst_log(prompt + instructions, "prompt", self.call_count)

        total_prompt = self.history + prompt + instructions
        self.history = self.history + prompt
        self.logger.write_rst_log(total_prompt, "history", self.call_count)

        try:
            # Generate the response
            response = self.client.generate_content(
                total_prompt,
                tools=tools,
            )
            # TODO: validate function call when expected

            response_parts = []
            last_result = None

            if hasattr(response.candidates[0].content, "parts"):
                for part in response.candidates[0].content.parts:
                    if part.text:
                        response_parts.append(part.text + "\n")
                    if part.executable_code:
                        response_parts.append("code_execution:\n")
                        response_parts.append(
                            f"```python\n{part.executable_code.code}\n```\n"
                        )
                    if part.code_execution_result:
                        response_parts.append(
                            f"code_execution_result: {part.code_execution_result.outcome}\n"
                        )
                        response_parts.append(
                            f"```\n{part.code_execution_result.output}\n```\n"
                        )
                    if part.function_call:
                        response_parts.append("function_call:\n")
                        response_parts.append(part.function_call.name + "\n")

                        result = self._call_function(part.function_call, functions)
                        last_result = result

                        response_parts.append("\nresult:\n")
                        response_parts.append(result + "\n")

                        if result == "submit":
                            break

            # Log the response
            print("\nRESPONSE:")
            print("-" * 20)
            for part in response_parts:
                print(part)
            self.history = self.history + response_parts

            self.logger.write_rst_log(response_parts, "response", self.call_count)

            return last_result

        except Exception as e:
            print(f"\nERROR generating content: {str(e)}")
            self.logger.log_error(str(e), prompt)
            raise

    def _call_function(self, function_call, functions):
        """Execute a function call and log it."""
        if not functions:
            raise ValueError("No functions provided")

        function_name = function_call.name
        function_args = function_call.args

        if function_name not in functions:
            raise ValueError(f"Unknown function: {function_name}")

        result = functions[function_name](**function_args)

        # Log the function call
        #  self.log_function_call(function_name, function_args, result)

        return result

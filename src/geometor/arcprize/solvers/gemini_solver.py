"""Dialogue-Based ARC Puzzle Solver

Implements a structured workflow for solving ARC puzzles through conversation
with LLMs, focusing on building understanding before attempting solutions.

The solver follows a systematic process:

1. Examine training examples individually
2. Build comprehensive observations
3. Validate understanding through pre-testing
4. Implement solution through standard operations

Key Features:

- Progressive observation building
- Code-validated pattern discovery
- Natural language program development
- Iterative refinement through dialogue
- Comprehensive session logging

The solver maintains a conversation history and working grid state, allowing
for cumulative understanding and step-by-step solution development.
"""

from rich import print
from datetime import datetime
from pathlib import Path
import json
import numpy as np
import os

from geometor.arcprize.puzzles import Puzzle, PuzzleSet, Grid

from geometor.arcprize.solvers.gemini_client import GeminiClient as Client
from geometor.arcprize.solvers.gemini_logger import Logger, PuzzleSession
import geometor.arcprize.solvers.gemini_solver_instructions as INST

#  DEFAULT_MODEL = "models/gemini-1.5-flash"
DEFAULT_MODEL = "models/gemini-1.5-flash-002"
#  DEFAULT_MODEL = "models/gemini-1.5-pro-002"
DEFAULT_INSTRUCTIONS_FILE = "gemini_instructions.md"


class PuzzleSolver:
    """
    Initialize the PuzzleSolver with all necessary components for solving and logging.


    parameters
    ----------
    puzzle : :class:`Puzzle <geometor.arcprize.puzzles.puzzle.Puzzle>`
        object containing all the elements of the Puzzle
    model_name : :class:`python:str`
        name of the Gemini model
    instructions_file : str
        path to file with system instructions
    output_dir : optional str
        default '.'
    max_iterations : int
        max loops in the test phase
    timestamp : optional :class:`python:str`
        in the format %y.%j.%H%M%S
    client : optional :class:`GeminiClient <geometor.arcprize.solvers.gemini_client.GeminiClient>`
        pass in client with previous context
    logger : optional :class:`Logger <geometor.arcprize.solvers.gemini_logger.Logger>`
        pass in previous logger

    attributes
    ----------
    start_time : datetime

    working_grid : :class:`Grid <geometor.arcprize.puzzles.grid.Grid>`

    """

    def __init__(
        self,
        puzzle: Puzzle,
        model_name: str = DEFAULT_MODEL,
        instructions_file: str = DEFAULT_INSTRUCTIONS_FILE,
        output_dir: str = ".",
        max_iterations: int = 5,
        timestamp: str = None,
        client: Client = None,
        session: PuzzleSession = None,
    ):
        # Initialize timestamp
        self.timestamp = timestamp or datetime.now().strftime("%y.%j.%H%M%S")

        # Initialize PuzzleSession
        self.session = session or PuzzleSession(output_dir, puzzle.id, self.timestamp)
        self.session.model_name = model_name
        self.session.max_iterations = max_iterations

        # Initialize GeminiClient
        self.client = client or Client(model_name, instructions_file)

        # Initialize Logger using the session
        self.logger = Logger(self.session)

        # Core components
        self.puzzle = puzzle
        self.model_name = model_name
        self.instructions_file = instructions_file
        self.max_iterations = max_iterations
        self.call_count = 0
        self.current_iteration = 0

        # Initialize working state
        self.working_grid = None

    def solve(self):
        """
        Main method to orchestrate the puzzle solving workflow.
        Returns the working grid if solution is found, None otherwise.
        """
        try:
            # Initialize solving state
            self.session.history.append(f"Begin puzzle: {self.puzzle.id}\n\n")

            self._show_examples()
            self._summarize_examples()
            self._show_test_input()
            #  self._initialize_working_grid()
            #  self._run_solution_loop()

        except Exception as e:
            print(f"Solve failed: {str(e)}")
            self.logger.log_error(f"Solve failed: {str(e)}", "\n".join(self.session.history))
            raise

    def _show_examples(self):
        """
        step 1 - show all training pairs
        """
        for i, pair in enumerate(self.puzzle.train, 1):
            self.logger.save_grid_image(
                pair.input.to_image(), self.call_count, f"example_{i}_input"
            )
            self.logger.save_grid_image(
                pair.output.to_image(), self.call_count, f"example_{i}_output"
            )

            prompt = [
                f"""
**example_{i}**

**input**

```
{str(pair.input.grid)}
```
**output**

```
{str(pair.output.grid)}
```

**images**

""",
                pair.input.to_image(),
                pair.output.to_image(),
                "\n\n**observations**\n",
            ]
            instructions = [INST.example_instructions]
            self._generate_content(
                prompt,
                instructions,
                #  tools="code_execution",
                description=f"example_{i}",
            )

    def _summarize_examples(self):
        """
        step 2 - summarize observations on pairs
        """
        prompt = [INST.examples_summary_prompt]
        instructions = [INST.examples_summary_instructions]
        self._generate_content(
            prompt,
            instructions,
            #  tools="code_execution",
            description=f"example_summary",
        )

    def _show_test_input(self):
        """
        step 3 - show test input for eval
        """
        test_pair = self.puzzle.test[0]
        self.logger.save_grid_image(
            test_pair.input.to_image(), self.call_count, f"test_input"
        )
        prompt = [
            f"""\
**test**

**input**

```
{ str(test_pair.input.grid) }
```

**image**

""",
            test_pair.input.to_image(),
            "\n",
            "\n**observations**\n",
        ]
        instructions = [INST.test_input_instructions]
        self._generate_content(
            prompt,
            instructions,
            #  tools="code_execution",
            description=f"test input",
        )

    def _initialize_working_grid(self):
        """
        step 4 - initialize the working grid for the desired output
        """
        functions = {
            "initialize_output_from_input": self.initialize_output_from_input,
            "initialize_output_by_size": self.initialize_output_by_size,
        }
        prompt = ["**initialize the working output grid:**\n"]
        instructions = [INST.init_working_grid_instructions]
        self._generate_content(
            prompt,
            instructions,
            tools=functions.values(),
            functions=functions,
            description=f"init working",
        )

    def _show_working_grid(self):
        self.logger.save_grid_image(
            self.working_grid.to_image(), self.call_count, f"working_grid"
        )
        prompt = [
            f"""\
**working output grid**

updated with your changes

```
{ str(self.working_grid.grid) }
```

**image**

""",
            self.working_grid.to_image(),
            "\n",
        ]
        instructions = [INST.show_working_grid_instructions]
        self._generate_content(
            prompt,
            instructions,
            #  tools="code_execution",
            description=f"review working",
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
            self._show_working_grid()

            # Get next action
            result = self._get_next_action(set_functions)

            # Handle submission
            if "submit" in result:
                print(f"Solution submitted after {iteration + 1} iterations")
                return

        print(f"Max iertions ({self.max_iterations}) reached without submission")
        return

    def _get_next_action(self, functions):
        """
        Get and process the next action from the model.
        """
        prompt = ["**update working grid**\n"]
        instructions = [INST.next_action_instructions]
        return self._generate_content(
            prompt,
            instructions,
            tools=functions.values(),
            functions=functions,
            description=f"set pixels",
        )

    def _generate_content(self, prompt, instructions, tools=None, functions=None, description=""):
        """
        Generate content from the model with standardized logging and function call handling.
        """
        MAX_RETRIES = 3
        self.call_count += 1

        # Logging the prompt and instructions
        self.session.history.extend(prompt)
        self.session.history.extend(instructions)

        log_data = {
            "call_count": self.call_count,
            "type": "prompt",
            "description": description,
            "content": [{"type": "markdown", "content": part} for part in prompt + instructions],
        }
        self.session.add_step(log_data)
        self.logger.write_rst_log(prompt + instructions, "prompt", self.call_count, description=description)

        # Generate content
        for attempt in range(MAX_RETRIES):
            try:
                response_start = datetime.now()
                response = self.client.generate_content("\n".join(self.session.history), tools=tools)
                response_end = datetime.now()
                response_time = (response_end - response_start).total_seconds()

                # Update timing metadata
                self.session.response_times.append(response_time)

                # Update token counts
                metadata = response.to_dict().get("usage_metadata", {})
                self.session.token_counts["prompt"] += metadata.get("prompt_token_count", 0)
                self.session.token_counts["candidates"] += metadata.get("candidates_token_count", 0)
                self.session.token_counts["total"] += metadata.get("total_token_count", 0)
                self.session.token_counts["cached"] += metadata.get("cached_content_token_count", 0)

                # Log response
                response_data = response.to_dict()
                response_data["token_totals"] = self.session.token_counts.copy()
                response_data["timing"] = {
                    "response_time": response_time,
                    "response_times": self.session.response_times.copy(),
                }

                self.logger.save_response(response_data, self.call_count)

                # Handle function calls in response
                # ... rest of the function ...

                return response

            except Exception as e:
                print(f"\nERROR generating content: {str(e)}")
                self.logger.log_error(str(e), "\n".join(self.session.history))
                raise
        # If we get here, we've exhausted retries without success
        error_msg = "Failed to get valid function call after maximum retries"
        print(f"\nERROR: {error_msg}")
        self.logger.log_error(error_msg, prompt)
        raise MaxRetriesExceededError(error_msg)

    def _call_function(self, function_call, functions):
        """Execute a function call with improved error handling."""
        if not functions:
            raise ValueError("No functions provided")

        function_name = function_call.name
        function_args = function_call.args

        if function_name not in functions:
            raise UnknownFunctionError(f"Unknown function: {function_name}")

        try:
            result = functions[function_name](**function_args)
            return result
        except TypeError as e:
            raise FunctionArgumentError(
                f"Invalid arguments for {function_name}: {str(e)}"
            )
        except Exception as e:
            raise FunctionExecutionError(f"Error executing {function_name}: {str(e)}")

    # TEST FUNCTIONS to call from model #################################
    def initialize_output_from_input(self) -> str:
        """
        Initialize the test output grid with a copy of the input grid.
        """
        from copy import deepcopy

        self.working_grid = deepcopy(self.puzzle.test[0].input)
        print(str(self.working_grid.grid))

        return True, "initialize_output_from_input()"

    def initialize_output_by_size(self, width: int, height: int, color: int = 0) -> str:
        """
        Initialize the test output grid with specific dimensions.
        """
        width, height, color = int(width), int(height), int(color)
        new_grid = np.full((height, width), color)
        self.working_grid = Grid(new_grid, self.puzzle.id, "test", 0, "output")
        print(str(self.working_grid.grid))

        return True, f"initialize_output_by_size({width=}, {height=}, {color=})"

    def set_pixel(self, row: int, column: int, color: int) -> str:
        """
        Set grid value at a specific coordinate.
        """
        return self.working_grid.set_pixel(row, column, color)

    def set_range(
        self, row1: int, column1: int, row2: int, column2: int, color: int
    ) -> str:
        """
        Set grid values for a range of pixels.
        """
        return self.working_grid.set_range(row1, column1, row2, column2, color)

    def submit(self) -> str:
        """
        Submit the working grid and check for correctness against the expected output.
        """
        if self.working_grid is None:
            raise ValueError("No working grid to submit")

        expected_output = self.puzzle.test[0].output

        # Perform the comparison and score each part
        score = self._evaluate_accuracy(self.working_grid, expected_output)

        # Create a log entry for the result
        final_log = [ f"""
**Final Submission Results**

:Size Correct: {score['size_correct']}
:Colors Correct: {score['colors_correct']}
:Unique Color Count Diff: {score['unique_color_difference']}
:Pixel Accuracy: {score['pixel_accuracy']}%

"""
        ]

        description = "final"
        self.logger.write_rst_log(
            final_log, "submission", self.call_count, description=description
        )

        # Generate detailed results page
        self.logger.indexer.write_detailed_results(self.logger.puzzle_dir)

        return True, "submit"

    def _evaluate_accuracy(self, working_grid: Grid, expected_grid: Grid) -> dict:
        """
        Evaluate the accuracy of the working grid against the expected grid.

        Parameters
        ----------
        working_grid : Grid
            The grid created during the solution process.
        expected_grid : Grid
            The expected output grid from the training data.

        Returns
        -------
        dict
            A dictionary containing scores for each evaluated aspect.
        """
        # Size Correctness
        size_correct = (
            working_grid.height == expected_grid.height
            and working_grid.width == expected_grid.width
        )

        # Colors Correctness
        working_colors = working_grid.colors
        expected_colors = expected_grid.colors
        colors_correct = working_colors == expected_colors

        # Quantities of Unique Pixel Colors
        working_color_counts = working_grid.color_counts
        expected_color_counts = expected_grid.color_counts
        unique_color_difference = {
            color: abs(
                working_color_counts.get(color, 0) - expected_color_counts.get(color, 0)
            )
            for color in set(working_color_counts) | set(expected_color_counts)
        }

        # Per-Pixel Accuracy
        total_pixels = working_grid.size
        correct_pixels = np.sum(working_grid.grid == expected_grid.grid)
        pixel_accuracy = (
            (correct_pixels / total_pixels) * 100 if total_pixels > 0 else 0
        )

        # Return results as a dictionary
        return {
            "size_correct": size_correct,
            "colors_correct": colors_correct,
            "unique_color_difference": unique_color_difference,
            "pixel_accuracy": pixel_accuracy,
        }


# Custom exceptions for better error handling
class MultipleFunctionCallsError(Exception):
    """Raised when multiple function calls are detected in a single response."""

    pass


class MaxRetriesExceededError(Exception):
    """Raised when maximum retry attempts are exhausted."""

    pass


class UnknownFunctionError(Exception):
    """Raised when an unknown function is called."""

    pass


class FunctionArgumentError(Exception):
    """Raised when invalid arguments are provided to a function."""

    pass


class FunctionExecutionError(Exception):
    """Raised when a function fails during execution."""

    pass

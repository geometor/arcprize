"""Dialogue-Based ARC Puzzle Solver

Implements a structured workflow for solving ARC puzzles through conversation
with LLMs, focusing on building understanding before attempting solutions.

The solver follows a systematic process:
1. Examine training examples individually
2. Build comprehensive observations
3. Validate understanding through pre-testing
4. Implement solution through standard operations

Designed to work within a Session context that handles logging and result tracking.
"""

from rich import print
from datetime import datetime
import numpy as np
from copy import deepcopy

from geometor.arcprize.puzzles import Puzzle, Grid
from geometor.arcprize.solvers.gemini_client import GeminiClient as Client
import geometor.arcprize.solvers.gemini_solver_instructions as INST

DEFAULT_MODEL = "models/gemini-1.5-flash-002"
DEFAULT_INSTRUCTIONS_FILE = "gemini_instructions.md"


class PuzzleSolver:
    """
    A dialogue-based puzzle solver that works within a Session context.

    parameters
    ----------
    puzzle : Puzzle
        The puzzle to solve
    model_name : str
        Name of the Gemini model to use
    instructions_file : str
        Path to system instructions file
    max_iterations : int
        Maximum solution attempts
    session
        The parent Session object that handles logging
    client : Client, optional
        Existing client with context
    """

    def __init__(
        self,
        puzzle: Puzzle,
        session,
        model_name: str = DEFAULT_MODEL,
        instructions_file: str = DEFAULT_INSTRUCTIONS_FILE,
        max_iterations: int = 5,
        client: Client = None,
    ):
        self.puzzle = puzzle
        self.session = session
        self.model_name = model_name
        self.max_iterations = max_iterations
        self.call_count = 0
        self.current_iteration = 0

        # Initialize or use existing client
        self.client = client or Client(model_name, instructions_file)

        # Initialize solving state
        self.working_grid = None
        self.history = []
        self.token_counts = {"prompt": 0, "candidates": 0, "total": 0, "cached": 0}

    def solve(self):
        """
        Main method to orchestrate the puzzle solving workflow.

        returns
        -------
        Grid or None
            The solution grid if found, None otherwise
        """
        try:
            self.history = [f"Begin puzzle: {self.puzzle.id}\n\n"]

            self._show_examples()
            self._summarize_examples()
            self._show_test_input()
            self._initialize_working_grid()
            return self._run_solution_loop()

        except Exception as e:
            print(f"Solve failed: {str(e)}")
            self.session._log_error(f"Solve failed: {str(e)}", self.history)
            raise

    def _generate_content(
        self, prompt, instructions, tools=None, functions=None, description=""
    ):
        """Generate content with model and track metrics."""
        MAX_RETRIES = 3
        self.call_count += 1

        # Log the prompt through session
        self.session.log_prompt(
            prompt + instructions,
            self.call_count,
            description,
            history=self.history + prompt + ["\n\n====\n\n"] + instructions,
        )

        # Update history
        self.history.extend(prompt)

        # Try to generate content with retries
        for attempt in range(MAX_RETRIES):
            try:
                # Generate content and track metrics
                response = self.client.generate_content(
                    self.history + prompt + ["\n\n====\n\n"] + instructions,
                    tools=tools,
                )

                # Process response
                response_parts, function_result = self._process_response(
                    response, functions
                )

                # Log response through session
                self.session.log_response(
                    response_parts, self.call_count, description, response.to_dict()
                )

                # Update history
                self.history.extend(response_parts)

                return function_result

            except Exception as e:
                if attempt < MAX_RETRIES - 1:
                    print(
                        f"\nRetrying after error: {str(e)} (attempt {attempt + 2}/{MAX_RETRIES})"
                    )
                    continue
                raise

    def _process_response(self, response, functions=None):
        """Process model response and handle function calls."""
        response_parts = []
        function_result = None
        function_call_found = False

        # Extract all parts from response
        for part in response.candidates[0].content.parts:
            if part.text:
                response_parts.append(part.text + "\n")
            if part.executable_code:
                response_parts.extend(
                    [
                        "code_execution:\n",
                        f"```python\n{part.executable_code.code}\n```\n",
                    ]
                )
            if part.code_execution_result:
                response_parts.extend(
                    [
                        f"code_execution_result: {part.code_execution_result.outcome}\n",
                        f"```\n{part.code_execution_result.output}\n```\n",
                    ]
                )
            if part.function_call:
                if function_call_found:
                    raise MultipleFunctionCallsError("Multiple function calls detected")

                function_call_found = True
                response_parts.extend(
                    ["function_call:\n", f"{part.function_call.name}\n"]
                )

                result, msg = self._call_function(part.function_call, functions)
                function_result = msg

                response_parts.extend(["\nresult:\n", f"{result}\n", f"{msg}\n"])

        return response_parts, function_result

    # Core solving steps remain similar but delegate logging to session
    def _show_examples(self):
        """Show training examples and gather observations."""
        for i, pair in enumerate(self.puzzle.train, 1):
            self.session.save_grid_image(
                pair.input.to_image(),
                self.call_count,
                f"example_{i}_input",
                self.puzzle.id,
            )
            self.session.save_grid_image(
                pair.output.to_image(),
                self.call_count,
                f"example_{i}_output",
                self.puzzle.id,
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
            self._generate_content(
                prompt,
                [INST.example_instructions],
                tools="code_execution",
                description=f"example_{i}",
            )

    def _summarize_examples(self):
        """Analyze and summarize patterns from training examples."""
        prompt = [INST.examples_summary_prompt]
        return self._generate_content(
            prompt,
            [INST.examples_summary_instructions],
            tools="code_execution",
            description="example_summary",
        )

    def _show_test_input(self):
        """Show and analyze the test input grid."""
        test_pair = self.puzzle.test[0]
        self.session.save_grid_image(
            test_pair.input.to_image(), self.call_count, "test_input", self.puzzle.id
        )

        prompt = [
            f"""\
**test**

**input**

```
{str(test_pair.input.grid)}
```

**image**

""",
            test_pair.input.to_image(),
            "\n",
            "\n**observations**\n",
        ]
        return self._generate_content(
            prompt,
            [INST.test_input_instructions],
            tools="code_execution",
            description="test input",
        )

    def _initialize_working_grid(self):
        """Initialize the working grid for solution development."""
        functions = {
            "initialize_output_from_input": self.initialize_output_from_input,
            "initialize_output_by_size": self.initialize_output_by_size,
        }
        prompt = ["**initialize the working output grid:**\n"]
        return self._generate_content(
            prompt,
            [INST.init_working_grid_instructions],
            tools=functions.values(),
            functions=functions,
            description="init working",
        )

    def _show_working_grid(self):
        """Display current state of working grid."""
        self.session.save_grid_image(
            self.working_grid.to_image(),
            self.call_count,
            "working_grid",
            self.puzzle.id,
        )

        prompt = [
            f"""\
**working output grid**

updated with your changes

```
{str(self.working_grid.grid)}
```

**image**

""",
            self.working_grid.to_image(),
            "\n",
        ]
        return self._generate_content(
            prompt,
            [INST.show_working_grid_instructions],
            tools="code_execution",
            description="review working",
        )

    def _run_solution_loop(self):
        """
        Execute the main solution loop with proper submission handling.

        returns
        -------
        Grid or None
            The working grid if solution found and submitted, None otherwise
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
            if result == "submit":
                print(f"Solution submitted after {iteration + 1} iterations")
                return self.working_grid

        print(f"Max iterations ({self.max_iterations}) reached without submission")
        return None

    def _get_next_action(self, functions):
        """Get and process the next action from the model."""
        prompt = ["**update working grid**\n"]
        return self._generate_content(
            prompt,
            [INST.next_action_instructions],
            tools=functions.values(),
            functions=functions,
            description="set pixels",
        )

    def _call_function(self, function_call, functions):
        """
        Execute a function call with comprehensive error handling.

        parameters
        ----------
        function_call :
            The function call from the model
        functions : dict
            Available functions mapping

        returns
        -------
        tuple
            (result, message) from the function execution

        raises
        ------
        ValueError
            If no functions are provided
        UnknownFunctionError
            If function name not in mapping
        FunctionArgumentError
            If invalid arguments provided
        FunctionExecutionError
            If function execution fails
        """
        if not functions:
            raise ValueError("No functions provided")

        name = function_call.name
        args = function_call.args

        if name not in functions:
            raise UnknownFunctionError(f"Unknown function: {name}")

        try:
            result = functions[name](**args)
            return result
        except TypeError as e:
            raise FunctionArgumentError(f"Invalid arguments for {name}: {str(e)}")
        except Exception as e:
            raise FunctionExecutionError(f"Error executing {name}: {str(e)}")

    def submit(self) -> tuple[bool, str]:
        """
        Submit and evaluate the current working grid solution.

        returns
        -------
        tuple[bool, str]
            Success status and submission message

        raises
        ------
        ValueError
            If no working grid exists
        """
        if self.working_grid is None:
            raise ValueError("No working grid to submit")

        expected = self.puzzle.test[0].output
        score = self._evaluate_accuracy(self.working_grid, expected)

        # Log results through session
        self.session.log_submission(self.puzzle.id, score, self.call_count)

        return True, "submit"

    def _evaluate_accuracy(self, working_grid: Grid, expected_grid: Grid) -> dict:
        """
        Evaluate solution accuracy against expected output.

        parameters
        ----------
        working_grid : Grid
            The proposed solution grid
        expected_grid : Grid
            The expected output grid

        returns
        -------
        dict
            Comprehensive accuracy metrics
        """
        # Size correctness
        size_correct = (
            working_grid.height == expected_grid.height
            and working_grid.width == expected_grid.width
        )

        # Colors correctness
        working_colors = working_grid.colors
        expected_colors = expected_grid.colors
        colors_correct = working_colors == expected_colors

        # Color distribution differences
        working_counts = working_grid.color_counts
        expected_counts = expected_grid.color_counts
        color_diff = {
            color: abs(working_counts.get(color, 0) - expected_counts.get(color, 0))
            for color in set(working_counts) | set(expected_counts)
        }

        # Pixel accuracy
        total_pixels = working_grid.size
        correct_pixels = np.sum(working_grid.grid == expected_grid.grid)
        pixel_accuracy = (
            (correct_pixels / total_pixels) * 100 if total_pixels > 0 else 0
        )

        return {
            "size_correct": size_correct,
            "colors_correct": colors_correct,
            "unique_color_difference": color_diff,
            "pixel_accuracy": pixel_accuracy,
        }

    # Grid manipulation functions
    def initialize_output_from_input(self) -> tuple[bool, str]:
        """Initialize output grid from input."""
        self.working_grid = deepcopy(self.puzzle.test[0].input)
        return True, "initialize_output_from_input()"

    def initialize_output_by_size(
        self, width: int, height: int, color: int = 0
    ) -> tuple[bool, str]:
        """Initialize output grid with dimensions."""
        width, height, color = int(width), int(height), int(color)
        self.working_grid = Grid(
            np.full((height, width), color), self.puzzle.id, "test", 0, "output"
        )
        return True, f"initialize_output_by_size({width=}, {height=}, {color=})"

    def set_pixel(self, row: int, column: int, color: int) -> tuple[bool, str]:
        """Set a single pixel value."""
        return self.working_grid.set_pixel(row, column, color)

    def set_range(
        self, row1: int, column1: int, row2: int, column2: int, color: int
    ) -> tuple[bool, str]:
        """Set a range of pixel values."""
        return self.working_grid.set_range(row1, column1, row2, column2, color)

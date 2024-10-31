from rich import print
from datetime import datetime
from pathlib import Path
import json
import numpy as np
import os
#  from gemini_client import GeminiClient as Client

from gemini_reporter import Reporter
from google.api_core import retry

import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

#  DEFAULT_MODEL = "models/gemini-1.5-flash"
DEFAULT_MODEL = "models/gemini-1.5-flash-002"
#  DEFAULT_MODEL = "models/gemini-1.5-pro-002"
DEFAULT_INSTRUCTIONS_FILE = "gemini_instructions.md"

class PuzzleSolver:
    def __init__(self,
                 puzzle,
                 model_name="models/gemini-1.5-flash-002",
                 instructions_file="gemini_instructions.md",
                 output_dir='.',
                 max_iterations=5,
                 log_prefix="puzzle",
                 timestamp=None):
        """
        Initialize the PuzzleSolver with all necessary components for solving and logging.

        Args:
            puzzle: The puzzle object to solve
            model_name: Name of the Gemini model to use
            instructions_file: Path to the instructions file
            output_dir: Directory for output files and logs
            max_iterations: Maximum number of iterations for solving
            log_prefix: Prefix for log files
            timestamp: Optional timestamp for logging (defaults to current time)
        """
        # Core components
        self.puzzle = puzzle
        self.model_name = model_name
        self.instructions_file = instructions_file
        self.max_iterations = max_iterations
        self.call_count = 0


        # Working state
        self.working_grid = None
        self.history = []
        self.current_iteration = 0

        # Logging setup
        self.timestamp = timestamp or datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_prefix = log_prefix

        if output_dir:
            self.output_dir = Path(output_dir)
            self.logs_dir = self.output_dir / "logs" / self.timestamp / self.puzzle.id
            #  self.reports_dir = self.output_dir / "reports"

            # Ensure directories exist
            self.logs_dir.mkdir(parents=True, exist_ok=True)
            #  self.reports_dir.mkdir(parents=True, exist_ok=True)
        else:
            self.output_dir = None

        # Initialize empty metadata for logging
        self.metadata = {
            "puzzle_id": puzzle.id,
            "model": model_name,
            "timestamp": self.timestamp,
            "max_iterations": max_iterations,
            "history": [],
            "grid_states": [],
            "function_calls": []
        }

    def initialize_output_from_input(self) -> str:
        """Initialize the test output grid with a copy of the input grid."""
        from copy import deepcopy
        self.working_grid = deepcopy(self.puzzle.test[0].input)
        print(str(self.working_grid.grid))

        # Log the initialization
        self._log_grid_state("initialization", "copy_input")
        return "initialize_output_from_input()"

    def initialize_output_by_size(self, width: int, height: int, color: int = 0) -> str:
        """Initialize the test output grid with specific dimensions."""
        import numpy as np

        width, height, color = int(width), int(height), int(color)
        new_grid = np.full((height, width), color)
        self.working_grid = Grid(new_grid, self.puzzle.id, "test", 0, "output")
        print(str(self.working_grid.grid))

        # Log the initialization
        self._log_grid_state("initialization", f"new_grid_{width}x{height}")
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
        self._log_grid_state("pixel_set", f"r{row}c{column}={color}")
        return f"set_pixel({row=}, {column=}, {color=})"

    def set_range(self, row1: int, column1: int, row2: int, column2: int, color: int) -> str:
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
        self._log_grid_state("range_set", f"from_r{r1}c{c1}_to_r{r2-1}c{c2-1}={color}")

        return f"set_range({row1}, {column1}, {row2}, {column2}, {color})"

    def submit(self) -> str:
        """Submit the working grid and check for correctness."""
        if self.working_grid is None:
            raise ValueError("No working grid to submit")

        # TODO: Implement actual submission logic and correctness checking
        self._log_grid_state("submission", "final")
        return "submit"

    def _log_grid_state(self, action_type: str, description: str):
        """Log the current state of the grid with metadata."""
        if not self.output_dir:
            return

        state = {
            "timestamp": datetime.now().isoformat(),
            "iteration": self.current_iteration,
            "action_type": action_type,
            "description": description,
            "grid_shape": list(self.working_grid.grid.shape),
            "grid_values": self.working_grid.grid.tolist()
        }

        # Add to metadata
        self.metadata["grid_states"].append(state)

        # Write current state to log file
        log_file = self.logs_dir / f"{self.log_prefix}_{self.puzzle.id}_{self.timestamp}_states.jsonl"
        #  with open(log_file, "a") as f:
            #  #  breakpoint()
            #  f.write(json.dumps(state) + "\n")

    def log_function_call(self, function_name: str, args: dict, result: str):
        """Log details of function calls."""
        if not self.output_dir:
            return

        call_info = {
            "timestamp": self.timestamp,
            "iteration": self.current_iteration,
            "function": function_name,
            "arguments": args,
            "result": result
        }

        # Add to metadata
        self.metadata["function_calls"].append(call_info)

        # Write to log file
        log_file = self.logs_dir / f"{self.log_prefix}_{self.puzzle.id}_{self.timestamp}_calls.jsonl"
        #  with open(log_file, "a") as f:
            #  f.write(json.dumps(call_info) + "\n")

    def save_metadata(self):
        """Save all metadata to a JSON file."""
        if not self.output_dir:
            return

        import json
        metadata_file = self.output_dir / f"{self.log_prefix}_{self.puzzle.id}_{self.timestamp}_metadata.json"
        #  with open(metadata_file, "w") as f:
            #  json.dump(self.metadata, f, indent=2)

    def solve(self):
        """
        Main method to orchestrate the puzzle solving workflow.
        """
        #  import google.generativeai as genai
        #  from google.api_core import retry

        # Initialize model
        with open(self.instructions_file, "r") as f:
            instruction = f.read().strip()

        model = genai.GenerativeModel(
            self.model_name,
            system_instruction=instruction,
        )

        # Start solving history
        self.history = [
            f"Begin puzzle: {self.puzzle.id}\n\n",
        ]

        # Process training examples
        for i, pair in enumerate(self.puzzle.train, 1):
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
            instructions = [
                "- review the example grids\n",
                "- check for differences and patterns\n",
            ]
            self._generate_content(
                model,
                prompt,
                instructions,
                tools="code_execution",
            )

        # Summarize observations
        prompt = [
            "# examples summary: \n",
        ]
        instructions = [
            "- summarize your observations to explain the transformation of the input to output\n",
            "- use code_execution to investigate properties, patterns and differences in the grids",
        ]
        self._generate_content(
            model,
            prompt,
            instructions,
            tools="code_execution",
        )

        # Present test input
        test_pair = self.puzzle.test[0]
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
        self._generate_content(
            model,
            prompt,
            instructions,
            tools="code_execution",
        )

        # Initialize working grid
        init_functions = {
            "initialize_output_from_input": self.initialize_output_from_input,
            "initialize_output_by_size": self.initialize_output_by_size,
        }
        prompt = [
            "## initialize the working output grid\n",
        ]
        instructions = [
            "use function_call to initialize the working output grid:\n",
            "- initialize_output_from_input: good when examples show few differences between input and output\n",
            "- initialize_output_by_size: create a fresh grid from size and color\n",
        ]
        self._generate_content(
            model,
            prompt,
            instructions,
            tools=init_functions.values(),
            functions=init_functions,
        )

        # Define functions for setting pixels
        set_functions = {
            "set_pixel": self.set_pixel,
            "set_range": self.set_range,
            "submit": self.submit,
        }

        # Main solution loop
        for iteration in range(self.max_iterations):
            self.current_iteration = iteration

            # Present current working grid
            prompt = [
                "# working output grid\n",
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
                model,
                prompt,
                instructions,
                tools="code_execution",
            )

            # Get next action
            prompt = [
                    "## update working grid\n"
            ]
            instructions = [
                "- use function_call to set pixels on the grid to achieve the solution\n",
                "  - set_pixel: update one pixel at a time\n"
                "  - set_range: update a rectangular subset of pixel\n"
                "- when you think you have completed the output, call the submit function\n",
            ]
            result = self._generate_content(
                model,
                prompt,
                instructions,
                tools=set_functions.values(),
                functions=set_functions,
            )

            # Check if submission was made
            if result and "submit" in str(result):
                break

        # Save final state
        self.save_metadata()

        return self.working_grid

    def _generate_content(self, model, prompt, instructions, tools=None, functions=None):
        """
        Generate content from the model with standardized logging.
        """
        from datetime import datetime

        self.call_count += 1

        print("=" * 40)
        print("PROMPT:")
        for part in prompt:
            print(part)

        print("INSTRUCTIONS:")
        for part in instructions:
            print(part)

        self._write_markdown_log(prompt + instructions, "prompt")

        total_prompt = self.history + prompt + instructions
        self.history = self.history + prompt
        self._write_markdown_log(total_prompt, "total_prompt")

        try:
            # Generate the response
            response = model.generate_content(
                total_prompt,
                tools=tools,
                request_options={"retry": retry.Retry()}
            )

            response_parts = []
            last_result = None

            if hasattr(response.candidates[0].content, "parts"):
                for part in response.candidates[0].content.parts:
                    if part.text:
                        response_parts.append(part.text + "\n")
                    if part.executable_code:
                        response_parts.append("code_execution:\n")
                        response_parts.append(f"```python\n{part.executable_code.code}\n```\n")
                    if part.code_execution_result:
                        response_parts.append(f"code_execution_result: {part.code_execution_result.outcome}\n")
                        response_parts.append(f"```\n{part.code_execution_result.output}\n```\n")
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

            self._write_markdown_log(response_parts, "response")

            return last_result

        except Exception as e:
            print(f"\nERROR generating content: {str(e)}")
            if self.output_dir:
                self._log_error(str(e), prompt)
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

    def _write_markdown_log(self, log_list, log_type):
        """Write prompt and response to markdown log."""
        from datetime import datetime

        log_file = self.logs_dir / f"{self.call_count}-{log_type}.md"

        with open(log_file, "w") as f:
            for part in log_list:
                if isinstance(part, str):
                    f.write(f"{part}\n")
                else:
                    f.write(f"[{type(part).__name__}]\n")

    def _log_error(self, error_message, prompt):
        """Log errors to a file."""
        from datetime import datetime

        error_file = self.logs_dir / f"error_{self.puzzle.id}_{self.timestamp}_{self.current_iteration}.md"

        with open(error_file, "w") as f:
            f.write("# Error Log\n\n")
            f.write(f"## Error Message\n\n{error_message}\n\n")
            f.write("## Prompt Content\n\n")
            for part in prompt:
                f.write(f"{str(part)}\n")

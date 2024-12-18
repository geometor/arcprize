the following are python modules from geometor.arcprize.solvers

the code runs test sessions on the Gemini API and logs the results to the sphinx
website




./gemini_solver.py
```
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
from geometor.arcprize.solvers.gemini_logger import Logger
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
        logger: Logger = None,
    ):
        self.start_time = datetime.now()
        self.response_times = []  # Track individual response times

        # Initialize Jinja environment using DictLoader for direct string templates
        #  self.env = Environment(
        #  loader=DictLoader({"example_prompt": INST.example_prompt})
        #  )

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
            output_dir,
            puzzle.id,
            self.timestamp,
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
            "start_time": self.start_time.isoformat(),
            "response_times": [],
            "total_elapsed": None,
        }

        # Initialize token tracking
        self.token_counts = {"prompt": 0, "candidates": 0, "total": 0, "cached": 0}

    def solve(self):
        """
        Main method to orchestrate the puzzle solving workflow.
        Returns the working grid if solution is found, None otherwise.
        """
        try:
            # Initialize solving state
            self.history = [f"Begin puzzle: {self.puzzle.id}\n\n"]

            self._show_examples()
            self._summarize_examples()
            self._show_test_input()
            self._initialize_working_grid()
            self._run_solution_loop()

        except Exception as e:
            print(f"Solve failed: {str(e)}")
            self.logger.log_error(f"Solve failed: {str(e)}", self.history)
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
                tools="code_execution",
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
            tools="code_execution",
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
            tools="code_execution",
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
            tools="code_execution",
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

    def _generate_content(
        self, prompt, instructions, tools=None, functions=None, description=""
    ):
        """
        Generate content from the model with standardized logging and function call handling.
        """
        MAX_RETRIES = 3
        self.call_count += 1

        print(f"{self.call_count} • PROMPT")
        print("=" * 80)

        for part in prompt:
            print(part)

        instructions.insert(0, "\nINSTRUCTIONS:\n\n")
        for part in instructions:
            print(part)

        # write the prompt file
        self.logger.write_rst_log(
            prompt + instructions, "prompt", self.call_count, description=description
        )

        # write history file
        total_prompt = self.history + prompt + ["\n\n====\n\n"] + instructions
        self.history = self.history + prompt
        self.logger.write_rst_log(
            total_prompt, "history", self.call_count, description=description
        )

        for attempt in range(MAX_RETRIES):
            try:
                response_start = datetime.now()
                response = self.client.generate_content(
                    total_prompt,
                    tools=tools,
                )
                response_end = datetime.now()
                response_time = (response_end - response_start).total_seconds()

                # Update timing metadata
                self.response_times.append(response_time)
                total_elapsed = (response_end - self.start_time).total_seconds()

                # Update token counts immediately
                metadata = response.to_dict().get("usage_metadata", {})
                self.token_counts["prompt"] += metadata.get("prompt_token_count", 0)
                self.token_counts["candidates"] += metadata.get(
                    "candidates_token_count", 0
                )
                self.token_counts["total"] += metadata.get("total_token_count", 0)
                self.token_counts["cached"] += metadata.get(
                    "cached_content_token_count", 0
                )

                # Save response with current totals
                response_data = response.to_dict()
                response_data["token_totals"] = self.token_counts.copy()
                response_data["timing"] = {
                    "response_time": response_time,
                    "total_elapsed": total_elapsed,
                    "response_times": self.response_times.copy(),
                }

                self.logger.save_response(response_data, self.call_count)

                response_parts = []
                function_call_found = False
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
                            #  if function_call_found:
                            #  # More than one function call found - this should trigger a retry
                            #  raise MultipleFunctionCallsError(
                            #  "Multiple function calls detected"
                            #  )

                            function_call_found = True
                            response_parts.append("function_call:\n")
                            response_parts.append(part.function_call.name + "\n")

                            result, msg = self._call_function(
                                part.function_call, functions
                            )
                            last_result = msg

                            response_parts.append("\nresult:\n")
                            response_parts.append(f"{result}\n")
                            response_parts.append(f"{msg}\n")

                            if msg == "submit":
                                break

                # If functions were provided but no function call was found
                if functions and not function_call_found and attempt < MAX_RETRIES - 1:
                    retry_prompt = total_prompt + [
                        "\nNo function call found in your response. Please provide exactly one function call using the available functions.\n"
                    ]
                    total_prompt = retry_prompt
                    print(
                        f"\nRetrying function call request (attempt {attempt + 2}/{MAX_RETRIES})"
                    )
                    continue

                # Log the response
                print(f"{self.call_count} • RESPONSE")
                print("-" * 80)
                for part in response_parts:
                    print(part)
                self.history = self.history + response_parts

                self.logger.write_rst_log(
                    response_parts,
                    "response",
                    self.call_count,
                    {
                        "current": metadata,
                        "totals": self.token_counts,
                        "timing": {
                            "response_time": response_time,
                            "total_elapsed": total_elapsed,
                        },
                        "model": self.model_name,
                    },
                    description=description,
                )

                return last_result

            except MultipleFunctionCallsError as e:
                if attempt < MAX_RETRIES - 1:
                    retry_prompt = total_prompt + [
                        "\nPlease provide exactly one function call in your response.\n"
                    ]
                    total_prompt = retry_prompt
                    print(
                        f"\nRetrying due to multiple function calls (attempt {attempt + 2}/{MAX_RETRIES})"
                    )
                    continue
                else:
                    print(f"\nERROR: {str(e)} - Max retries exceeded")
                    self.logger.log_error(str(e), prompt)
                    raise

            except Exception as e:
                print(f"\nERROR generating content: {str(e)}")
                self.logger.log_error(str(e), prompt)
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
```


./gemini_logger.py
```
from datetime import datetime
from pathlib import Path
import json
from m2r2 import convert
from jinja2 import Environment, PackageLoader


class Indexer:
    """
    Manages the creation and updating of session, puzzle, and main index files.
    """

    def __init__(self, output_dir: str, puzzle_id: str, timestamp: str):
        self.output_dir = Path(output_dir)
        self.puzzle_id = puzzle_id
        self.timestamp = timestamp

        # Ensure required directories exist
        self._ensure_directory_structure()

        # Set up Jinja environment
        self.env = Environment(
            loader=PackageLoader("geometor.arcprize.solvers", "templates"),
        )

    def _ensure_directory_structure(self):
        """Create required directories if they don't exist."""
        self.sessions_dir = self.output_dir / "sessions"
        self.session_dir = self.sessions_dir / self.timestamp
        self.puzzle_dir = self.session_dir / self.puzzle_id

        self.sessions_dir.mkdir(parents=True, exist_ok=True)
        self.session_dir.mkdir(parents=True, exist_ok=True)
        self.puzzle_dir.mkdir(parents=True, exist_ok=True)
        (self.puzzle_dir / "_images").mkdir(parents=True, exist_ok=True)
        (self.puzzle_dir / "_responses").mkdir(parents=True, exist_ok=True)

    def update_session_results(self):
        """Generate and update session results summary."""
        puzzles = []
        
        for puzzle_dir in sorted(self.session_dir.iterdir()):
            if puzzle_dir.is_dir():
                puzzle_data = {
                    'id': puzzle_dir.name,
                    'submitted': False,
                    'size_correct': '',
                    'colors_correct': '',
                    'color_diff': '',
                    'pixel_accuracy': ''
                }
                
                # Look for submission files
                submission_files = list(puzzle_dir.glob('*-submission.rst'))
                if submission_files:
                    puzzle_data['submitted'] = True
                    with open(submission_files[0]) as f:
                        content = f.read()
                        
                        # Extract metrics using regex
                        import re
                        size_match = re.search(r':Size Correct: (True|False)', content)
                        colors_match = re.search(r':Colors Correct: (True|False)', content)
                        diff_match = re.search(r':Unique Color Count Diff: (\{.*?\})', content)
                        accuracy_match = re.search(r':Pixel Accuracy: ([\d\.]+)%', content)
                        
                        puzzle_data.update({
                            'size_correct': size_match.group(1) if size_match else '',
                            'colors_correct': colors_match.group(1) if colors_match else '',
                            'color_diff': diff_match.group(1) if diff_match else '',
                            'pixel_accuracy': f"{accuracy_match.group(1)}%" if accuracy_match else ''
                        })
                
                puzzles.append(puzzle_data)
        
        # Render template
        template = self.env.get_template('session_results.j2')
        content = template.render(
            title=f"Session Results: {self.timestamp}",
            puzzles=puzzles
        )
        
        # Write results file
        results_path = self.session_dir / 'results.rst'
        with open(results_path, 'w') as f:
            f.write(content)

    def update_indices(self):
        """Update all indices including results summary."""
        self._write_sessions_index()
        self._write_session_index()
        self._write_puzzle_index()
        self.update_session_results()
    def _write_sessions_index(self):
        """Regenerate the main sessions index using Jinja2."""
        index_path = self.sessions_dir / "index.rst"
        template = self.env.get_template("sessions_index.j2")
        session_list = [
            {"session_name": session_dir.name}
            for session_dir in sorted(self.sessions_dir.iterdir())
            if session_dir.is_dir()
        ]
        content = template.render(title="sessions", sessions=session_list)

        with open(index_path, "w") as f:
            f.write(content)

    def _write_session_index(self):
        """Regenerate the session index using Jinja2."""
        index_path = self.session_dir / "index.rst"
        puzzle_list = []
        total_time = 0
        total_tokens = 0
        total_steps = 0

        for puzzle_dir in sorted(self.session_dir.iterdir()):
            if puzzle_dir.is_dir():
                puzzle_id = puzzle_dir.name
                response_dir = puzzle_dir / "_responses"

                if response_dir.exists():
                    responses = sorted(response_dir.glob("*-response.json"))
                    steps = len(responses)
                    time = sum(
                        json.load(open(resp_file))
                        .get("timing", {})
                        .get("response_time", 0)
                        for resp_file in responses
                    )
                    tokens = (
                        json.load(open(responses[-1]))
                        .get("token_totals", {})
                        .get("total", 0)
                        if responses
                        else 0
                    )

                    puzzle_list.append(
                        {
                            "puzzle_id": puzzle_id,
                            "steps": steps,
                            "total_time": f"{time:.2f}s",
                            "total_tokens": f"{tokens:,}",
                        }
                    )

                    total_steps += steps
                    total_time += time
                    total_tokens += tokens

        template = self.env.get_template("session_index.j2")
        content = template.render(
            title=f"{self.timestamp}",
            puzzles=puzzle_list,
            total_steps=total_steps,
            total_time=f"{total_time:.2f}s",
            total_tokens=f"{total_tokens:,}",
        )

        with open(index_path, "w") as f:
            f.write(content)

    def _write_puzzle_index(self):
        """Regenerate the puzzle index using Jinja2."""
        index_path = self.puzzle_dir / "index.rst"
        prompt_files = sorted(self.puzzle_dir.glob("[0-9][0-9][0-9]-prompt.rst"))
        submission_files = sorted(self.puzzle_dir.glob("*-submission.rst"))  
        steps = []
        total_response_time = 0
        total_tokens = 0

        # Extract step details from prompt and response files
        for prompt_file in prompt_files:
            call_num = prompt_file.stem[:3]
            response_file = self.puzzle_dir / "_responses" / f"{call_num}-response.json"

            if response_file.exists():
                response_data = json.load(open(response_file))
                response_time = response_data.get("timing", {}).get("response_time", 0)
                token_data = response_data.get("token_totals", {}).get("total", 0)
                total_response_time += response_time
                total_tokens += token_data

                # Get description from the prompt file
                with open(prompt_file) as f:
                    content = f.read()
                    description = next(
                        (
                            line.split(":description:")[1].strip()
                            for line in content.split("\n")
                            if line.startswith(":description:")
                        ),
                        "Step",
                    )

                # Append step details for rendering
                steps.append(
                    {
                        "call_num": call_num,
                        "description": description,
                        "response_time": f"{response_time:.2f}s",
                        "tokens_used": f"{token_data:,}",
                    }
                )

        # Add submission entries to the steps list if submission files exist
        for submission_file in submission_files:
            submission_call_num = submission_file.stem.split("-")[0]
            steps.append(
                {
                    "call_num": submission_call_num,
                    "description": "evaluation",
                    "response_time": "N/A",
                    "tokens_used": "N/A",
                }
            )

        # Use Jinja template to render the index content
        template = self.env.get_template("puzzle_index.j2")
        content = template.render(
            title=f"{self.puzzle_id}",
            steps=steps,
            total_response_time=f"{total_response_time:.2f}s",
            total_tokens=f"{total_tokens:,}",
        )

        # Write the rendered content to the index file
        with open(index_path, "w") as f:
            f.write(content)

        # Append toctree entries to include all steps, including the final submission(s)
        with open(index_path, "a") as f:
            f.write("\n.. toctree::\n   :hidden:\n   :maxdepth: 1\n\n")
            for step in steps:
                if "evaluation" in step["description"]:
                    f.write(f"   {step['call_num']}-submission\n")
                #  else:
                    #  f.write(f"   {step['call_num']}-prompt\n")


class Logger:
    def __init__(self, output_dir: str, puzzle_id: str, timestamp: str):
        self.output_dir = Path(output_dir)
        self.puzzle_id = puzzle_id
        self.timestamp = timestamp

        self._ensure_directory_structure()

        self.indexer = Indexer(output_dir, puzzle_id, timestamp)
        self.image_registry = {}

    def _ensure_directory_structure(self):
        """Create required directories if they don't exist."""
        # Setup directory structure
        self.sessions_dir = self.output_dir / "sessions"
        self.session_dir = self.sessions_dir / self.timestamp
        self.puzzle_dir = self.session_dir / self.puzzle_id
        self.images_dir = self.puzzle_dir / "_images"
        self.responses_dir = self.puzzle_dir / "_responses"

        self.sessions_dir.mkdir(parents=True, exist_ok=True)
        self.session_dir.mkdir(parents=True, exist_ok=True)
        self.puzzle_dir.mkdir(parents=True, exist_ok=True)
        self.images_dir.mkdir(parents=True, exist_ok=True)
        self.responses_dir.mkdir(parents=True, exist_ok=True)

    def save_response(self, response: dict, call_count: int):
        """Save raw response data as JSON."""
        response_file = self.responses_dir / f"{call_count:03d}-response.json"

        with open(response_file, "w") as f:
            json.dump(response, f, indent=2)

        self.indexer.update_indices()

    def save_grid_image(self, grid_image, call_count: int, context: str) -> Path:
        """
        Save a grid image with deduplication.

        parameters
        ----------
        grid_image :
            PIL Image to save
        call_count :
            Current call number
        context :
            Image context (e.g., 'example_1_input', 'working')

        returns
        -------
        rel_path : Path
            Relative path to the image file
        """
        # Use image content as key for deduplication
        image_bytes = grid_image.tobytes()

        if image_bytes in self.image_registry:
            return self.image_registry[image_bytes]

        # Create new file if image hasn't been saved before
        filename = f"{call_count:03d}-{context}.png"
        image_path = self.images_dir / filename
        grid_image.save(image_path)

        # Store relative path for RST references
        rel_path = image_path.relative_to(self.puzzle_dir)
        self.image_registry[image_bytes] = rel_path

        #  self.indexer.update_indices()
        return rel_path

    def write_rst_log(
        self,
        log_list: list,
        log_type: str,
        call_count: int,
        usage_data=None,
        description="",
    ):
        """Write log as RST file and handle any images.

        parameters
        ----------
        log_list : list
            The list of log content parts (strings, images, etc.)
        log_type : str
            The type of log (e.g., "prompt", "response")
        call_count : int
            The call count for naming the log file
        usage_data : dict, optional
            Data related to model usage (e.g., token counts, timing)
        """
        # Prepare data for the template
        parts = []
        for part in log_list:
            if isinstance(part, str):
                if part.startswith("[["):  # Grid display - preserve as code block
                    parts.append({"type": "code", "content": part})
                else:
                    try:
                        # Convert markdown to RST
                        rst_content = convert(part, escape_html=True)
                        parts.append({"type": "markdown", "content": rst_content})
                    except Exception as e:
                        print(f"Warning: Markdown conversion failed: {str(e)}")
                        parts.append({"type": "markdown", "content": part})

            elif hasattr(part, "save"):  # PIL Image object
                rel_path = self.save_grid_image(
                    part, call_count, f"grid_{len(self.image_registry)}"
                )
                parts.append({"type": "image", "path": str(rel_path)})

            else:
                parts.append({"type": "unknown", "content": f"[{type(part).__name__}]"})

        # Prepare usage data for the template
        timing = None
        token_usage = []

        if usage_data:
            if "timing" in usage_data:
                timing = usage_data["timing"]

            if "current" in usage_data and "totals" in usage_data:
                current = usage_data["current"]
                totals = usage_data["totals"]
                token_usage = [
                    {
                        "label": "Prompt",
                        "current": current["prompt_token_count"],
                        "total": totals["prompt"],
                    },
                    {
                        "label": "Response",
                        "current": current["candidates_token_count"],
                        "total": totals["candidates"],
                    },
                    {
                        "label": "Total",
                        "current": current["total_token_count"],
                        "total": totals["total"],
                    },
                    {
                        "label": "Cached",
                        "current": current["cached_content_token_count"],
                        "total": totals["cached"],
                    },
                ]

        # Render the content with Jinja2
        template = self.indexer.env.get_template("log_entry.j2")
        title = f"{call_count:03d} • {log_type.title()}"
        content = template.render(
            puzzle_id=self.puzzle_id,
            timestamp=self.timestamp,
            call_count=call_count,
            title=title,
            log_list=parts,
            usage_data=usage_data,
            timing=timing,
            token_usage=token_usage,
            description=description,
        )

        # Write the rendered content to the file
        log_file = self.puzzle_dir / f"{call_count:03d}-{log_type}.rst"
        with open(log_file, "w") as f:
            f.write(content)

        # Update indices after writing the log
        self.indexer.update_indices()

    def _get_image_count(self, call_count: int) -> int:
        """
        Get the next available image number for this call.

        parameters
        ----------

        """
        pattern = f"{call_count:03d}-*.png"
        existing_images = list(self.images_dir.glob(pattern))
        return len(existing_images) + 1

    def _add_navigation_links(self, file, log_type: str, call_count: int):
        """Add appropriate navigation links based on log type."""
        file.write("\n.. seealso::\n\n")
        if log_type == "prompt":
            file.write(f"   - :doc:`{call_count:03d}-history`\n")
            file.write(f"   - :doc:`{call_count:03d}-response`\n\n")
        elif log_type == "response":
            file.write(f"   - :doc:`{call_count:03d}-history`\n")
            file.write(f"   - :doc:`{call_count:03d}-prompt`\n\n")
        elif log_type == "history":
            file.write(f"   - :doc:`{call_count:03d}-prompt`\n")
            file.write(f"   - :doc:`{call_count:03d}-response`\n\n")

    def log_error(self, error_message: str, context: str = ""):
        """Log an error message to a file.

        parameters
        ----------
        error_message : str
            The error message to be logged.
        context : str
            Additional context or history information to provide.

        """
        error_log_file = self.session_dir / "error_log.txt"
        with open(error_log_file, "a") as f:
            f.write(f"[{datetime.now().isoformat()}] ERROR: {error_message}")
            if context:
                f.write(f"Context: {context}")
            f.write(" ")
```


./gemini_client.py
```
"""Google Gemini Model Interface for ARC Challenge

Provides a streamlined interface to Google's Gemini model, configured specifically
for the dialogue-based ARC solving approach.

Features:
    
- Structured conversation management
- Code execution capabilities
- Function calling support
- System instruction integration
- Error handling and retry logic

The client is designed to maintain consistent context while allowing for
flexible interaction patterns including code exploration and function calls.
"""

import os
from pathlib import Path
import google.generativeai as genai
from google.api_core import retry


class GeminiClient:
    """
    Initialize the GeminiClient with model configuration and system instructions.

    parameters
    ----------
    model_name : :class:`python:str`
        Name of the Gemini model to use.
    instructions_file : :class:`python:str`
        Path to the instructions file.
    """

    def __init__(self, model_name: str, instructions_file: str):
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        self.model_name = model_name

        script_dir = Path(__file__).parent.absolute()
        instructions_file = script_dir / instructions_file

        with open(instructions_file, "r") as f:
            instruction = f.read().strip()

        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            system_instruction=instruction,
        )

    def generate_content(self, prompt: list, tools=None) -> object:
        """
        Generate content from the Gemini model based on the provided prompt.

        parameters
        ----------
        prompt : list
            The prompt to send to the model.
        tools : str or list
            Optional tools or functions the model can use.
            "code_execution"

        returns
        -------
        response : GeminiResponse
            the model's response.

        """
        try:
            if tools and tools != "code_execution":
                tool_config = {"function_calling_config": {"mode": "ANY"}}
            else:
                tool_config = None

            response = self.model.generate_content(
                prompt,
                tools=tools,
                request_options={"retry": retry.Retry()},
                tool_config=tool_config,
            )
            return response
        except Exception as e:
            # TODO: Handle exceptions as needed
            raise e
```



# Refactoring and Logging/Reporting Guidelines

Introduce a Session Object as a Single Source of Truth
- Implement a Session class or structure that holds all state, puzzle references, timestamps, and incremental results. The Session object will be the authoritative runtime record and can serialize its current state to disk at any point.

Incremental, Structured Logging
- After each interaction (prompt-response cycle or code execution), immediately write out a structured JSON file capturing:

Prompt text and metadata
- Response text and metadata
- Timing and token usage information
- Any intermediate grid states or images
- This ensures that even if an error interrupts the process, partial, structured logs remain.

Defer Index Generation
- Move index and summary generation (RST reports, aggregated metrics) to a separate pass that runs after all puzzle steps or after the session concludes. If a catastrophic failure occurs mid-session, you still have raw JSON logs from which you can generate a partial report.
- 
Structured Data Over Parsing
- Store key metrics—such as size correctness, pixel accuracy, and color differences—directly in JSON right after evaluation. Avoid reliance on regex or parsing RST files for metrics. This makes indexing scripts simpler and more robust.

Leverage Python’s Logging and Exception Handling
- Use Python’s built-in logging module for developer-facing runtime logs (info, warnings, errors) and structured JSON files for puzzle-solving details. On catastrophic errors, a top-level exception handler should:

Log the error.
- Force a session.save() call to ensure all current data is preserved.
- Flexible, Post-hoc Report Generation
By separating the raw data capture from report generation, you can:

Easily regenerate summaries and indexes from existing JSON logs without re-running the solver.
- Experiment with new reporting templates or metrics as needed without changing the puzzle-solving code.
- Validation and Testing
- Periodically test and validate JSON logs to ensure integrity. Keeping data well-structured and validated helps ensure that the indexing scripts can reliably produce final reports, even if a run was interrupted.

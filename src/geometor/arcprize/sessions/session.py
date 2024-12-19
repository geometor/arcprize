"""Session management module for ARC puzzle solving.

This module provides the Session class which manages the solving process for a set of ARC puzzles,
including logging, indexing, and result tracking. It coordinates the solving workflow and maintains
session state across multiple puzzles.
"""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import json
import numpy as np

from jinja2 import Environment, PackageLoader
from PIL import Image

from geometor.arcprize.puzzles import PuzzleSet, Puzzle
from geometor.arcprize.solvers.gemini_client import GeminiClient
from geometor.arcprize.solvers.gemini_solver import PuzzleSolver


@dataclass
class SessionMetrics:
    """Tracks metrics for a puzzle-solving session."""

    total_time: float = 0.0
    total_tokens: int = 0
    total_steps: int = 0
    puzzles_attempted: int = 0
    puzzles_solved: int = 0
    average_accuracy: float = 0.0
    token_counts: dict = field(
        default_factory=lambda: {"prompt": 0, "candidates": 0, "total": 0, "cached": 0}
    )


@dataclass
class PuzzleResult:
    """Stores the results of a single puzzle solution attempt."""

    puzzle_id: str
    success: bool
    accuracy: float
    solution_time: float
    total_steps: int
    token_usage: dict
    size_correct: bool
    colors_correct: bool
    color_differences: dict


class Session:
    """Manages a puzzle-solving session including logging, indexing, and result tracking.

    The Session class coordinates the solving of multiple puzzles within a PuzzleSet,
    maintaining state and logging comprehensive results. It handles directory structure,
    logging, and provides analysis of solving performance.

    parameters
    ----------
    puzzle_set : PuzzleSet
        The set of puzzles to be solved in this session
    output_dir : str
        Directory for storing session outputs and logs
    model_name : str, optional
        Name of the Gemini model to use
    max_iterations : int, optional
        Maximum iterations per puzzle attempt

    attributes
    ----------
    timestamp : str
        Unique session identifier based on start time
    metrics : SessionMetrics
        Tracks overall session performance metrics
    results : dict
        Stores results for each attempted puzzle
    """

    def __init__(
        self,
        puzzle_set: PuzzleSet,
        output_dir: str,
        model_name: str = "models/gemini-1.5-pro-002",
        max_iterations: int = 5,
    ):
        self.puzzle_set = puzzle_set
        self.output_dir = Path(output_dir)
        self.model_name = model_name
        self.max_iterations = max_iterations

        # Initialize session state
        self.timestamp = datetime.now().strftime("%y.%j.%H%M%S")
        self.metrics = SessionMetrics()
        self.results = {}

        # Initialize logging state
        self.current_puzzle_id = None
        self.current_call_count = 0
        self._image_registry = {}
        self._call_counters = {}  # Track call counts per puzzle

        # Set up environment
        self._setup_environment()

    def increment_call_count(self, puzzle_id: str) -> int:
        """
        Increment and return the call counter for a specific puzzle.

        parameters
        ----------
        puzzle_id : str
            Identifier of the puzzle

        returns
        -------
        int
            Updated call count
        """
        if puzzle_id not in self._call_counters:
            self._call_counters[puzzle_id] = 0
        self._call_counters[puzzle_id] += 1
        self.current_call_count = self._call_counters[puzzle_id]
        return self.current_call_count

    def _setup_environment(self):
        """Initialize directory structure and Jinja environment."""
        self.sessions_dir = self.output_dir / "sessions"
        self.session_dir = self.sessions_dir / self.timestamp

        # Create directories
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
        self.session_dir.mkdir(parents=True, exist_ok=True)

        # Initialize Jinja environment
        self.env = Environment(
            loader=PackageLoader("geometor.arcprize.sessions", "templates"),
        )

    def solve_puzzles(self) -> dict:
        """
        Solve all puzzles in the set, tracking results and updating metrics.

        returns
        -------
        dict
            Results for all attempted puzzles
        """
        start_time = datetime.now()

        for puzzle in self.puzzle_set.puzzles:
            result = self.solve_puzzle(puzzle)
            self.results[puzzle.id] = result
            self._update_metrics(result)

        self.metrics.total_time = (datetime.now() - start_time).total_seconds()
        self._generate_session_summary()

        return self.results

    def solve_puzzle(self, puzzle: Puzzle) -> PuzzleResult:
        """
        Attempt to solve a single puzzle and record results.

        parameters
        ----------
        puzzle : Puzzle
            The puzzle to solve

        returns
        -------
        PuzzleResult
            Comprehensive results of the solution attempt
        """
        puzzle_dir = self.session_dir / puzzle.id
        puzzle_dir.mkdir(exist_ok=True)

        # Set current puzzle context
        self.current_puzzle_id = puzzle.id
        self._image_registry.clear()  # Reset image registry for new puzzle

        # Initialize solver
        solver = PuzzleSolver(
            puzzle=puzzle,
            session=self,
            model_name=self.model_name,
            max_iterations=self.max_iterations,
        )

        # Attempt solution
        start_time = datetime.now()
        #  try:
            #  solution = solver.solve()
            #  success = True if solution else False
        #  except Exception as e:
            #  self._log_error(f"Error solving puzzle {puzzle.id}: {str(e)}")
            #  success = False
        solution = solver.solve()
        success = True if solution else False

        solve_time = (datetime.now() - start_time).total_seconds()

        # Calculate accuracy and create result
        accuracy = (
            self._calculate_accuracy(solver.working_grid, puzzle.test[0].output)
            if success
            else 0.0
        )

        result = PuzzleResult(
            puzzle_id=puzzle.id,
            success=success,
            accuracy=accuracy,
            solution_time=solve_time,
            total_steps=solver.call_count,
            token_usage=solver.token_counts.copy(),
            size_correct=solver.working_grid is not None,
            colors_correct=success,
            color_differences={},  # Populated if solution exists
        )

        self._save_puzzle_results(result)
        return result

    def _calculate_accuracy(self, solution_grid, expected_grid) -> float:
        """Calculate pixel-wise accuracy of solution."""
        if (
            solution_grid is None
            or solution_grid.grid.shape != expected_grid.grid.shape
        ):
            return 0.0
        return np.mean(solution_grid.grid == expected_grid.grid) * 100

    def _update_metrics(self, result: PuzzleResult):
        """Update session metrics with puzzle result."""
        self.metrics.puzzles_attempted += 1
        if result.success:
            self.metrics.puzzles_solved += 1

        # Update token counts
        for key, value in result.token_usage.items():
            self.metrics.token_counts[key] += value

        self.metrics.total_steps += result.total_steps

        # Update running accuracy average
        self.metrics.average_accuracy = (
            self.metrics.average_accuracy * (self.metrics.puzzles_attempted - 1)
            + result.accuracy
        ) / self.metrics.puzzles_attempted

    def _save_puzzle_results(self, result: PuzzleResult):
        """Save detailed puzzle results to file."""
        results_file = self.session_dir / f"{result.puzzle_id}_results.json"
        with open(results_file, "w") as f:
            json.dump(result.__dict__, f, indent=2)

    def _generate_session_summary(self):
        """Generate comprehensive session summary."""
        template = self.env.get_template("session_summary.j2")
        summary = template.render(
            timestamp=self.timestamp, metrics=self.metrics, results=self.results
        )

        with open(self.session_dir / "session_summary.rst", "w") as f:
            f.write(summary)

    def _log_error(self, error_msg: str, context: str = ""):
        """Log error message with timestamp and context."""
        error_log = self.session_dir / "error_log.txt"
        with open(error_log, "a") as f:
            f.write(f"[{datetime.now().isoformat()}] ERROR: {error_msg}\n")
            if context:
                f.write(f"Context: {context}\n")

    def get_summary_metrics(self) -> dict:
        """
        Get summary metrics for the session.

        returns
        -------
        dict
            Dictionary containing key session metrics
        """
        return {
            "timestamp": self.timestamp,
            "total_time": self.metrics.total_time,
            "puzzles_attempted": self.metrics.puzzles_attempted,
            "puzzles_solved": self.metrics.puzzles_solved,
            "average_accuracy": self.metrics.average_accuracy,
            "total_tokens": self.metrics.token_counts["total"],
            "total_steps": self.metrics.total_steps,
        }

    def save_grid_image(self, grid_image, call_count: int, context: str, puzzle_id: str) -> Path:
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

        if image_bytes in self._image_registry:
            return self._image_registry[image_bytes]

        # Create new file if image hasn't been saved before
        filename = f"{call_count:03d}-{context}.png"


        image_folder = self.session_dir / puzzle_id / "_images"
        image_folder.mkdir(parents=True, exist_ok=True)
        image_path = image_folder / filename
        grid_image.save(image_path)

        # Store relative path for RST references
        rel_path = image_path.relative_to(self.session_dir / puzzle_id)
        self._image_registry[image_bytes] = rel_path

        #  self.indexer.update_indices()
        return rel_path

    def log_prompt(self, content: list, call_count: int, description: str, history: list = None):
        """Log a prompt and related history to RST files.

        parameters
        ----------
        content : list
            Prompt content parts (text, images, etc.)
        call_count : int
            Current call sequence number
        description : str
            Brief description of prompt purpose
        history : list, optional
            Conversation history to include
        """
        puzzle_dir = self.session_dir / str(self.current_puzzle_id)

        # Process content for RST
        processed_content = self._process_content(content)

        # Generate prompt RST
        template = self.env.get_template("log_entry.j2")
        prompt_content = template.render(
            puzzle_id=self.current_puzzle_id,
            timestamp=self.timestamp,
            call_count=call_count,
            title=f"{call_count:03d} • Prompt",
            content=processed_content,
            description=description,
            metrics=None  # Prompts don't have metrics
        )

        # Write prompt file
        prompt_file = puzzle_dir / f"{call_count:03d}-prompt.rst"
        with open(prompt_file, "w") as f:
            f.write(prompt_content)

        # Handle history if provided
        if history:
            processed_history = self._process_content(history)
            history_content = template.render(
                puzzle_id=self.current_puzzle_id,
                timestamp=self.timestamp,
                call_count=call_count,
                title=f"{call_count:03d} • History",
                content=processed_history,
                description=description,
                metrics=None
            )

            history_file = puzzle_dir / f"{call_count:03d}-history.rst"
            with open(history_file, "w") as f:
                f.write(history_content)

    def log_response(self, content: list, call_count: int, description: str, response_data: dict):
        """Log model response with metrics.

        parameters
        ----------
        content : list
            Response content parts
        call_count : int
            Current call sequence number
        description : str
            Brief description of response purpose
        response_data : dict
            Raw response data including metrics
        """
        puzzle_dir = self.session_dir / str(self.current_puzzle_id)
        responses_dir = puzzle_dir / "_responses"
        responses_dir.mkdir(parents=True, exist_ok=True)

        # Save raw response data
        response_file = responses_dir / f"{call_count:03d}-response.json"
        with open(response_file, "w") as f:
            json.dump(response_data, f, indent=2)

        # Process content for RST
        processed_content = self._process_content(content)
        
        # Extract metrics from response data
        metrics = {
            "timing": response_data.get("timing", {}),
            "token_counts": response_data.get("token_totals", {}),
            "model": response_data.get("model", "unknown")
        }

        # Generate RST content
        template = self.env.get_template("log_entry.j2")
        rst_content = template.render(
            puzzle_id=self.current_puzzle_id,
            timestamp=self.timestamp,
            call_count=call_count,
            title=f"{call_count:03d} • Response",
            content=processed_content,
            description=description,
            metrics=metrics
        )

        # Write RST file
        rst_file = puzzle_dir / f"{call_count:03d}-response.rst"
        with open(rst_file, "w") as f:
            f.write(rst_content)

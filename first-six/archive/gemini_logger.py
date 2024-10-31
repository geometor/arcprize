import json
from datetime import datetime
from pathlib import Path


class Logger:
    def __init__(self, output_dir: str, puzzle_id: str, timestamp: str, log_prefix: str = "puzzle"):
        """
        Initialize the Logger with directory paths and file naming conventions.

        Args:
            output_dir: Directory for output files and logs.
            puzzle_id: Identifier for the puzzle.
            timestamp: Timestamp for log files.
            log_prefix: Prefix for log files.
        """
        self.output_dir = Path(output_dir)
        self.puzzle_id = puzzle_id
        self.timestamp = timestamp
        self.log_prefix = log_prefix

        self.logs_dir = self.output_dir / "logs" / self.timestamp / self.puzzle_id
        self.logs_dir.mkdir(parents=True, exist_ok=True)

    def log_grid_state(self, working_grid, action_type: str, description: str = "", iteration: int = 0):
        """
        Log the current state of the grid with metadata.

        Args:
            working_grid: The current working grid.
            action_type: Type of action performed.
            description: Description of the action.
            iteration: Current iteration number.
        """
        state = {
            "timestamp": datetime.now().isoformat(),
            "iteration": iteration,
            "action_type": action_type,
            "description": description,
            #  "grid_shape": list(working_grid.grid.shape),
            #  "grid_values": working_grid.grid.tolist(),
        }

        # Write current state to log file
        log_file = self.logs_dir / f"{self.log_prefix}_{self.puzzle_id}_{self.timestamp}_states.jsonl"
        #  with open(log_file, "a") as f:
            #  f.write(json.dumps(state) + "\n")

    def log_function_call(self, function_name: str, args: dict, result: str, iteration: int = 0):
        """
        Log details of function calls.

        Args:
            function_name: Name of the function called.
            args: Arguments passed to the function.
            result: Result returned by the function.
            iteration: Current iteration number.
        """
        call_info = {
            "timestamp": datetime.now().isoformat(),
            "iteration": iteration,
            "function": function_name,
            "arguments": args,
            "result": result,
        }

        # Write to log file
        log_file = self.logs_dir / f"{self.log_prefix}_{self.puzzle_id}_{self.timestamp}_calls.jsonl"
        #  with open(log_file, "a") as f:
            #  f.write(json.dumps(call_info) + "\n")

    def write_markdown_log(self, log_list: list, log_type: str, call_count: int):
        """
        Write prompt and response to a markdown log.

        Args:
            log_list: List of log entries.
            log_type: Type of log ('prompt' or 'response').
            call_count: The call count for naming the log file.
        """
        log_file = self.logs_dir / f"{call_count}-{log_type}.md"
        with open(log_file, "w") as f:
            for part in log_list:
                f.write(f"{part}\n")

    def log_error(self, error_message: str, prompt: list, iteration: int = 0):
        """
        Log errors to a file.

        Args:
            error_message: The error message to log.
            prompt: The prompt that caused the error.
            iteration: Current iteration number.
        """
        print("ERROR:")
        print(error_message)

        error_file = self.logs_dir / f"error_{self.puzzle_id}_{self.timestamp}_{iteration}.md"
        with open(error_file, "w") as f:
            f.write("# Error Log\n\n")
            f.write(f"## Error Message\n\n{error_message}\n\n")
            f.write("## Prompt Content\n\n")
            for part in prompt:
                f.write(f"{str(part)}\n")

    def save_metadata(self, metadata: dict):
        """
        Save all metadata to a JSON file.

        Args:
            metadata: The metadata dictionary to save.
        """
        metadata_file = self.output_dir / f"{self.log_prefix}_{self.puzzle_id}_{self.timestamp}_metadata.json"
        #  with open(metadata_file, "w") as f:
            #  json.dump(metadata, f, indent=2)


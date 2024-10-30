import json
from datetime import datetime
from pathlib import Path

class Logger:
    def __init__(self, output_dir: str, puzzle_id: str, timestamp: str):
        """Initialize logger with Sphinx RST file support."""
        self.output_dir = Path(output_dir)
        self.puzzle_id = puzzle_id
        self.timestamp = timestamp

        self.sessions_dir = self.output_dir / "sessions" 
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
        # TODO: check for index

        self.session_dir = self.sessions_dir / self.timestamp 
        self.session_dir.mkdir(parents=True, exist_ok=True)
        # TODO: check for index.rst - add to sessions toctree

        self.puzzle_dir = self.session_dir / self.puzzle_id
        self.puzzle_dir.mkdir(parents=True, exist_ok=True)
        # TODO: check for index.rst - add to session toctree

    def write_rst_log(self, log_list: list, log_type: str, call_count: int):
        """Write logs as RST files with proper Sphinx structure."""
        # Create filename
        log_file = self.logs_dir / f"{call_count:03d}-{log_type}.rst"

        with open(log_file, "w") as f:
            # Write title
            title = f"Puzzle {self.puzzle_id} - {log_type.title()} {call_count}"
            f.write(self._rst_header(title, "="))
            
            # Add metadata section
            f.write("\n.. meta::\n")
            f.write(f"   :puzzle_id: {self.puzzle_id}\n")
            f.write(f"   :timestamp: {self.timestamp}\n")
            f.write(f"   :call_count: {call_count}\n\n")

            # Add links to related files
            if log_type == "prompt":
                f.write(".. seealso::\n\n")
                f.write(f"   - :doc:`{call_count:03d}-history`\n")
                f.write(f"   - :doc:`{call_count:03d}-response`\n\n")

            # Write content
            for part in log_list:
                if isinstance(part, str):
                    # Handle code blocks
                    if part.startswith("```python"):
                        f.write("\n.. code-block:: python\n\n")
                        code = part.replace("```python", "").replace("```", "").strip()
                        for line in code.split("\n"):
                            f.write(f"    {line}\n")
                        f.write("\n")
                    # Handle ASCII art (grid displays)
                    elif "[[" in part or any(c.isdigit() for c in part):
                        f.write("\n.. code-block::\n\n")
                        for line in part.split("\n"):
                            f.write(f"    {line}\n")
                        f.write("\n")
                    else:
                        f.write(f"{part}\n")
                else:
                    f.write(f"[{type(part).__name__}]\n")

            # Add toctree for navigation if this is a prompt file
            if log_type == "prompt":
                f.write("\n.. toctree::\n")
                f.write("   :maxdepth: 1\n")
                f.write("   :hidden:\n\n")
                f.write(f"   {call_count:03d}-history\n")
                f.write(f"   {call_count:03d}-response\n")

    def _rst_header(self, text: str, char: str) -> str:
        """Create RST header with proper underline."""
        return f"{text}\n{char * len(text)}\n\n"

    def _create_index(self):
        """Create index.rst for the puzzle logs."""
        index_file = self.logs_dir / "index.rst"
        
        with open(index_file, "w") as f:
            # Write title
            title = f"Puzzle {self.puzzle_id} Solution Log"
            f.write(self._rst_header(title, "="))
            
            # Add puzzle metadata
            f.write(".. meta::\n")
            f.write(f"   :puzzle_id: {self.puzzle_id}\n")
            f.write(f"   :timestamp: {self.timestamp}\n\n")
            
            # Add introduction
            f.write(f"Solution attempt for puzzle {self.puzzle_id} at {self.timestamp}\n\n")
            
            # Add toctree
            f.write(".. toctree::\n")
            f.write("   :maxdepth: 2\n")
            f.write("   :caption: Solution Steps:\n\n")
            
            # Add all log files (will need to be updated as files are created)
            pattern = f"[0-9][0-9][0-9]-prompt.rst"
            for file in sorted(self.logs_dir.glob(pattern)):
                f.write(f"   {file.stem}\n")

    def update_index(self):
        """Update index.rst with any new files."""
        self._create_index()

    def log_error(self, error_message: str, prompt: list, iteration: int = 0):
        """Log errors as RST files."""
        print("ERROR:")
        print(error_message)

        error_file = self.logs_dir / f"error_{iteration:03d}.rst"
        with open(error_file, "w") as f:
            # Write title
            title = f"Error Log - Iteration {iteration}"
            f.write(self._rst_header(title, "="))
            
            # Write error message
            f.write("Error Message\n")
            f.write("-" * 12 + "\n\n")
            f.write(f"{error_message}\n\n")
            
            # Write prompt content
            f.write("Prompt Content\n")
            f.write("-" * 13 + "\n\n")
            for part in prompt:
                f.write(f"{str(part)}\n")

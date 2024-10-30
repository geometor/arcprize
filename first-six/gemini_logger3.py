import json
from datetime import datetime
from pathlib import Path


class Logger:
    def __init__(self, output_dir: str, puzzle_id: str, timestamp: str):
        self.output_dir = Path(output_dir)
        self.puzzle_id = puzzle_id
        self.timestamp = timestamp

        # Setup directory structure
        self.sessions_dir = self.output_dir / "sessions"
        self.session_dir = self.sessions_dir / self.timestamp
        self.puzzle_dir = self.session_dir / self.puzzle_id

        # Create directories and indices
        self._ensure_directory_structure()
        self._ensure_indices()

    def _ensure_directory_structure(self):
        """Create required directories if they don't exist."""
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
        self.session_dir.mkdir(parents=True, exist_ok=True)
        self.puzzle_dir.mkdir(parents=True, exist_ok=True)

    def _ensure_indices(self):
        """Create or update index files at each level."""
        self._ensure_sessions_index()
        self._ensure_session_index()
        self._ensure_puzzle_index()

    def _ensure_sessions_index(self):
        """Create/update main sessions index."""
        index_path = self.sessions_dir / "index.rst"
        if not index_path.exists():
            with open(index_path, "w") as f:
                f.write(self._rst_header("sessions", "="))
                f.write(".. toctree::\n")
                f.write("   :maxdepth: 2\n\n")

        # Add session to toctree if not present
        self._append_to_toctree(index_path, f"{self.timestamp}/index.rst")

    def _ensure_session_index(self):
        """Create/update session index."""
        index_path = self.session_dir / "index.rst"
        if not index_path.exists():
            with open(index_path, "w") as f:
                f.write(self._rst_header(f"{self.timestamp}", "="))
                f.write(".. toctree::\n")
                f.write("   :maxdepth: 2\n\n")

        # Add puzzle to toctree if not present
        self._append_to_toctree(index_path, f"{self.puzzle_id}/index.rst")

    def _ensure_puzzle_index(self):
        """Create/update puzzle index."""
        index_path = self.puzzle_dir / "index.rst"
        if not index_path.exists():
            with open(index_path, "w") as f:
                f.write(self._rst_header(f"{self.puzzle_id}", "="))
                f.write(".. toctree::\n")
                f.write("   :maxdepth: 2\n\n")

    def _append_to_toctree(self, index_path: Path, entry: str):
        """Add entry to toctree if not present."""
        with open(index_path, "r") as f:
            content = f.read()

        if entry not in content:
            # Find the toctree directive
            toctree_pos = content.find(".. toctree::")
            if toctree_pos != -1:
                # Find the end of the directive options
                pos = content.find("\n\n", toctree_pos)
                if pos != -1:
                    # Insert new entry
                    content = content[: pos + 2] + f"   {entry}\n" + content[pos + 2 :]
                    with open(index_path, "w") as f:
                        f.write(content)

    def write_rst_log(self, log_list: list, log_type: str, call_count: int):
        """Write log as RST file and update puzzle index if needed."""
        log_file = self.puzzle_dir / f"{call_count:03d}-{log_type}.rst"

        with open(log_file, "w") as f:
            title = f"Puzzle {self.puzzle_id} - {log_type.title()} {call_count}"
            title = f"{call_count:03d} • {log_type.title()}"
            f.write(self._rst_header(title, "="))

            # Add metadata section
            f.write("\n.. meta::\n")
            f.write(f"   :puzzle_id: {self.puzzle_id}\n")
            f.write(f"   :timestamp: {self.timestamp}\n")
            f.write(f"   :call_count: {call_count}\n\n")

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
                    #  elif "[[" in part or any(c.isdigit() for c in part):
                    elif part.startswith("[["):
                        f.write("\n.. code-block::\n\n")
                        for line in part.split("\n"):
                            f.write(f"    {line}\n")
                        f.write("\n")
                    else:
                        f.write(f"{part}\n")
                else:
                    f.write(f"[{type(part).__name__}]\n")

            # Add links to related files
            if log_type == "prompt":
                f.write("\n\n")
                f.write(".. seealso::\n\n")
                f.write(f"   - :doc:`{call_count:03d}-history`\n")
                f.write(f"   - :doc:`{call_count:03d}-response`\n\n")
            if log_type == "response":
                f.write("\n\n")
                f.write(".. seealso::\n\n")
                f.write(f"   - :doc:`{call_count:03d}-history`\n")
                f.write(f"   - :doc:`{call_count:03d}-prompt`\n\n")
            if log_type == "history":
                f.write("\n\n")
                f.write(".. seealso::\n\n")
                f.write(f"   - :doc:`{call_count:03d}-prompt`\n")
                f.write(f"   - :doc:`{call_count:03d}-response`\n\n")

        # Update puzzle index if this is a prompt or response
        if log_type in ["prompt", "response"]:
            self._update_puzzle_index()

    def write_rst_log(self, log_list: list, log_type: str, call_count: int):
        """Write log as RST file and update puzzle index if needed."""
        log_file = self.puzzle_dir / f"{call_count:03d}-{log_type}.rst"

        with open(log_file, "w") as f:
            # Write title
            title = f"{call_count:03d} • {log_type.title()}"
            f.write(self._rst_header(title, "="))

            # Add metadata section
            f.write("\n.. meta::\n")
            f.write(f"   :puzzle_id: {self.puzzle_id}\n")
            f.write(f"   :timestamp: {self.timestamp}\n")
            f.write(f"   :call_count: {call_count}\n\n")

            # Write content with proper RST formatting
            for part in log_list:
                if isinstance(part, str):
                    # Handle code blocks
                    if part.startswith("```python"):
                        f.write("\n.. code-block:: python\n\n")
                        code = part.replace("```python", "").replace("```", "").strip()
                        for line in code.split("\n"):
                            f.write(f"    {line}\n")
                        f.write("\n")

                    elif part.startswith("```"):
                        f.write("\n::\n\n")
                        code = part.replace("```", "").replace("```", "").strip()
                        for line in code.split("\n"):
                            f.write(f"    {line}\n")
                        f.write("\n")

                    # Handle grid displays
                    elif part.startswith("[["):
                        f.write("\n.. code-block::\n\n")
                        for line in part.split("\n"):
                            f.write(f"    {line}\n")
                        f.write("\n")

                    # Handle structured content with proper RST formatting
                    #  elif part.startswith("**") and ":" in part:
                        #  # This handles sections like "**input:**" or "**output:**"
                        #  section_title, content = part.split(":", 1)
                        #  f.write(f"\n{section_title}:\n")
                        #  # If there's content after the colon, format it properly
                        #  if content.strip():
                            #  for line in content.strip().split("\n"):
                                #  if line.strip():
                                    #  f.write(f"\n{line}\n")
                        #  f.write("\n")

                    # Handle bullet points
                    elif part.strip().startswith("- "):
                        # Ensure blank line before list
                        f.write("\n")
                        for line in part.split("\n"):
                            if line.strip():
                                # Preserve bullet point formatting
                                f.write(f"{line}\n")
                        f.write("\n")

                    # Handle regular text
                    else:
                        if part.strip():
                            f.write(f"{part.strip()}\n\n")

                else:
                    f.write(f"[{type(part).__name__}]\n\n")

            # Add links to related files
            if log_type == "prompt":
                f.write(".. seealso::\n\n")
                f.write(f"   - :doc:`{call_count:03d}-history`\n")
                f.write(f"   - :doc:`{call_count:03d}-response`\n\n")

            # Update puzzle index if needed
            if log_type in ["prompt", "response"]:
                self._update_puzzle_index()

    def _update_puzzle_index(self):
        """Update puzzle index with prompt/response pairs."""
        index_path = self.puzzle_dir / "index.rst"
        with open(index_path, "w") as f:
            f.write(self._rst_header(f"Puzzle {self.puzzle_id}", "="))
            f.write(".. toctree::\n")
            f.write("   :maxdepth: 2\n\n")

            # Add all prompt/response pairs
            for prompt_file in sorted(
                self.puzzle_dir.glob("[0-9][0-9][0-9]-prompt.rst")
            ):
                stem = prompt_file.stem[:-7]  # Remove '-prompt'
                f.write(f"   {stem}-prompt.rst\n")
                f.write(f"   {stem}-response.rst\n")

    def _rst_header(self, text: str, char: str) -> str:
        """Create RST header with proper underline."""
        return f"{text}\n{char * len(text)}\n\n"

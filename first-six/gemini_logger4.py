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
        
        # Create directory for images
        self.images_dir = self.puzzle_dir / "_images"
        self._ensure_directory_structure()
        self._ensure_indices()

    def _ensure_directory_structure(self):
        """Create required directories if they don't exist."""
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
        self.session_dir.mkdir(parents=True, exist_ok=True)
        self.puzzle_dir.mkdir(parents=True, exist_ok=True)
        self.images_dir.mkdir(parents=True, exist_ok=True)

    def write_rst_log(self, log_list: list, log_type: str, call_count: int):
        """Write log as RST file and handle any images."""
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

            # Process content
            for part in log_list:
                if isinstance(part, str):
                    if part == "[Image]":
                        # Skip placeholder - real image was handled in previous iteration
                        continue
                        
                    if part.startswith("```python"):
                        f.write("\n.. code-block:: python\n\n")
                        code = part.replace("```python", "").replace("```", "").strip()
                        for line in code.split("\n"):
                            f.write(f"    {line}\n")
                        f.write("\n")

                    elif part.startswith("[["):
                        # Grid display followed by image
                        f.write("\n.. code-block::\n\n")
                        for line in part.split("\n"):
                            f.write(f"    {line}\n")
                        f.write("\n")

                    else:
                        if part.strip():
                            f.write(f"{part.strip()}\n\n")

                elif hasattr(part, 'save'): # PIL Image object
                    # Save the image
                    image_filename = f"{call_count:03d}-{self._get_image_count(call_count)}.png"
                    image_path = self.images_dir / image_filename
                    part.save(image_path)
                    
                    # Add image directive to RST
                    f.write(f"\n.. image:: _images/{image_filename}\n")
                    f.write("   :alt: Grid visualization\n")
                    f.write("   :align: center\n\n")

                else:
                    f.write(f"[{type(part).__name__}]\n\n")

            # Add navigation links
            self._add_navigation_links(f, log_type, call_count)

             # Append to puzzle toctree if this is a prompt or response
            if log_type in ["prompt", "response"]:
                self._append_to_toctree(
                    self.puzzle_dir / "index.rst",
                    f"{call_count:03d}-{log_type}"  # No .rst extension in toctree
                )

    def _get_image_count(self, call_count: int) -> int:
        """Get the next available image number for this call."""
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

    #  def _append_to_toctree(self, index_path: Path, entry: str):
        #  """Add entry to toctree if not present."""
        #  with open(index_path, "r") as f:
            #  content = f.read()

        #  if entry not in content:
            #  # Find the toctree directive
            #  toctree_pos = content.find(".. toctree::")
            #  if toctree_pos != -1:
                #  # Find the end of the directive options
                #  pos = content.find("\n\n", toctree_pos)
                #  if pos != -1:
                    #  # Insert new entry
                    #  content = content[: pos + 2] + f"   {entry}\n" + content[pos + 2 :]
                    #  with open(index_path, "w") as f:
                        #  f.write(content)

    def _append_to_toctree(self, index_path: Path, entry: str):
        """Add entry to toctree if not present, maintaining order."""
        with open(index_path, "r") as f:
            content = f.read()

        if entry not in content:
            # Find the toctree directive
            toctree_pos = content.find(".. toctree::")
            if toctree_pos != -1:
                # Find the end of the directive options (look for :maxdepth: line)
                lines = content.split("\n")
                header_end = -1
                for i, line in enumerate(lines):
                    if ":maxdepth:" in line:
                        header_end = i
                        break

                if header_end != -1:
                    # Reconstruct the content
                    header = lines[:header_end + 1]
                    # Get existing entries, filtering out empty lines
                    entries = [line[3:] for line in lines[header_end + 1:]
                             if line.strip() and line.startswith("   ")]

                    # Add new entry and sort
                    entries.append(entry)
                    entries = sorted(set(entries))

                    # Rebuild content
                    new_content = "\n".join(header) + "\n\n"  # Keep original header
                    new_content += "\n".join(f"   {e}" for e in entries) + "\n"

                    with open(index_path, "w") as f:
                        f.write(new_content)

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

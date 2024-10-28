# reporter.py

from jinja2 import Template
import base64
import markdown
from pathlib import Path


class Reporter:
    def __init__(self, template_path="gemini_report_2.html.j2"):
        """Initialize reporter with template"""
        self.template_path = template_path
        self._load_template()

    def _load_template(self):
        """Load and configure Jinja template"""
        with open(self.template_path) as f:
            self.template = Template(f.read())

        # Register filters
        self.template.environment.filters["clean_base64"] = self._clean_base64
        self.template.environment.filters["markdown"] = self._markdown_filter

    @staticmethod
    def _clean_base64(data):
        """Clean and format base64 data for HTML embedding"""
        if isinstance(data, bytes):
            # Convert raw bytes directly to base64
            return base64.b64encode(data).decode("utf-8")
        elif isinstance(data, str):
            if data.startswith("b'") or data.startswith('b"'):
                # Remove b prefix and quotes
                raw_str = data[2:-1]
                # Convert escaped bytes to actual bytes
                byte_str = bytes(raw_str, "utf-8").decode("unicode-escape").encode("latin1")
                # Convert to base64
                return base64.b64encode(byte_str).decode("utf-8")
        return data

    @staticmethod
    def _markdown_filter(text):
        """Convert markdown to HTML"""
        return markdown.markdown(text)

    def generate(self, chat_history, puzzle_id, output_dir):
        """Generate HTML report from chat history"""
        # Render template
        html = self.template.render(
            history=chat_history,
            puzzle_id=puzzle_id,
            output_dir=output_dir
        )

        # Save report
        report_path = output_dir / "reports" / f"puzzle_{puzzle_id}.html"
        report_path.write_text(html)

        # Create index if this is the first report
        index_path = output_dir / "reports" / "index.html"
        if not index_path.exists():
            self._create_index(output_dir)

        return report_path

    def _create_index(self, output_dir):
        """Create an index.html file linking to all reports"""
        reports_dir = output_dir / "reports"
        puzzle_files = list(reports_dir.glob("puzzle_*.html"))
        
        index_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>ARC Puzzle Analysis Reports</title>
            <style>
                body {
                    font-family: system-ui;
                    line-height: 1.5;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    background: var(--bg-main);
                    color: var(--text-primary);
                }
                :root {
                    --bg-main: #1a1a1a;
                    --text-primary: #e0e0e0;
                    --link-color: #58a6ff;
                }
                h1 { margin-bottom: 1em; }
                .puzzle-link {
                    display: block;
                    padding: 10px;
                    margin: 5px 0;
                    background: #242424;
                    border-radius: 4px;
                    color: var(--link-color);
                    text-decoration: none;
                }
                .puzzle-link:hover {
                    background: #2d2d2d;
                }
            </style>
        </head>
        <body>
            <h1>ARC Puzzle Analysis Reports</h1>
            <div class="puzzle-list">
        """
        
        for file in sorted(puzzle_files):
            if file.name != "index.html":
                puzzle_id = file.stem.replace("puzzle_", "")
                index_html += f'<a class="puzzle-link" href="{file.name}">Puzzle {puzzle_id}</a>\n'
        
        index_html += """
            </div>
        </body>
        </html>
        """
        
        index_path = reports_dir / "index.html"
        index_path.write_text(index_html)

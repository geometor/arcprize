import json
from pathlib import Path
from playwright.sync_api import sync_playwright
from jinja2 import Environment, FileSystemLoader

# Set up Jinja2 environment
env = Environment(loader=FileSystemLoader("."))
template = env.get_template("template4.html.j2")


def generate_puzzle_image(puzzle, output_dir, page, total_puzzles):
    # Generate HTML content using Jinja2 template
    puzzle["total_puzzles"] = total_puzzles
    html_content = template.render(puzzle)

    # Set content and wait for it to load
    page.set_content(html_content)
    page.wait_for_load_state("networkidle")

    # Capture screenshot
    output_path = output_dir / f"{puzzle['symbol_set']}_{puzzle['index']}.png"
    page.screenshot(path=str(output_path), full_page=True)
    print(f"Created {output_path}")

    output_path = output_dir / f"{puzzle['symbol_set']}_{puzzle['index']}.html"
    with open(output_path, "w") as f:
        f.write(html_content)
    print(f"Created {output_path}")


def visualize_puzzles(json_file, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(json_file, "r") as f:
        data = json.load(f)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1920, "height": 1080})

        total_puzzles = len(data["results"])

        for puzzle in data["results"]:
            generate_puzzle_image(puzzle, output_dir, page, total_puzzles)

        browser.close()


if __name__ == "__main__":
    json_file = "../../../../../demos/rotation_puzzle_results_20240802_084405.json"
    output_dir = "~/Sessions/rotation_test"
    visualize_puzzles(json_file, output_dir)

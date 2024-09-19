import json
from pathlib import Path
from playwright.sync_api import sync_playwright
from jinja2 import Environment, FileSystemLoader

# Set up Jinja2 environment
env = Environment(loader=FileSystemLoader("."))
template = env.get_template("template3.html.j2")
animated_template = env.get_template("template4.html.j2")


def generate_puzzle_image(puzzle, output_dir, page):
    html_content = template.render(puzzle)

    # Set content and wait for it to load
    page.set_content(html_content)
    page.wait_for_load_state("networkidle")

    # Capture screenshot
    output_path = output_dir / f"{puzzle['title']}.png"
    page.screenshot(path=str(output_path), full_page=True)
    print(f"Created {output_path}")

    output_path = output_dir / f"{puzzle['symbol_set']}_{puzzle['index']}.html"
    with open(output_path, "w") as f:
        f.write(html_content)
    print(f"Created {output_path}")


def capture_puzzle_animation(puzzle, output_dir, page):
    html_content = animated_template.render(puzzle)

    page.set_content(html_content)

    # Wait for the animation to complete
    page.wait_for_function(
        f"() => parseFloat(document.getElementById('timer').textContent) >= {puzzle['processing_time']}"
    )

    video_path = page.video.path()
    new_video_path = (
        output_dir / f"{puzzle['title']}.webm"
    )
    video_path = Path(video_path).rename(new_video_path)
    print(f"created {video_path}")


def visualize_puzzles(json_file, puzzle_type):
    json_path = Path(json_file).expanduser().resolve()
    output_dir = Path.home() / "Sessions" / json_path.stem
    output_dir.mkdir(parents=True, exist_ok=True)

    with json_path.open("r") as f:
        data = json.load(f)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            record_video_dir=str(output_dir),
            record_video_size={"width": 1920, "height": 1080},
        )
        page = context.new_page()
        page.set_viewport_size({"width": 1920, "height": 1080})

        total_puzzles = len(data["results"])

        for puzzle in data["results"]:

            puzzle['title'] = f"{puzzle['symbol_set']}_{puzzle['index']}"
            puzzle["total_puzzles"] = total_puzzles
            puzzle["type"] = puzzle_type
            generate_puzzle_image(puzzle, output_dir, page)
            #  capture_puzzle_animation(puzzle, output_dir, page, total_puzzles)

            # Rename the video file

        context.close()
        browser.close()


if __name__ == "__main__":
    json_file = "../../../../../demos/rotation_puzzle_results_20240802_084405.json"
    visualize_puzzles(json_file, "ROTATION")

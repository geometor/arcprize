import json
import os
import glob
from PIL import Image, ImageDraw

# Color mapping from arcprize.org
# 0 --white: #EEEEEE;
# 1 --blue: #1E93FF;
# 2 --red: #F93C31;
# 3 --green: #4FCC30;
# 4 --yellow: #FFDC00;
# 5 --gray: #555555;
#  --magenta-light: #ff7bcc;
# 6 --magenta: #E53AA3;
# 7 --orange: #FF851B;
# 8 --blue-light: #87D8F1;
# 9 --maroon: #921231;
#  --black: #000000;
#  --offwhite: #C0C0C0;
#  --gray-light: #999999;
# replaced Gray with Pink
# darkened red, orange, yellow
#  5: (255, 123, 204),  # Pink
COLOR_MAP = {
    0: (238, 238, 238),  # White
    1: (30, 147, 255),  # Blue
    2: (220, 50, 40),  # Red
    3: (79, 204, 48),  # Green
    4: (230, 200, 0),  # Yellow
    5: (85, 85, 85),  # Gray
    6: (229, 58, 163),  # Magenta
    7: (230, 120, 20),  # Orange
    8: (135, 216, 241),  # Azure
    9: (146, 18, 49),  # Maroon
}


def create_grid_image(grid, filename):
    cell_size = 8
    border = 1
    color_size = 6
    width = len(grid[0]) * cell_size
    height = len(grid) * cell_size

    image = Image.new("RGB", (width, height), color="black")
    draw = ImageDraw.Draw(image)

    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            color = COLOR_MAP.get(
                cell, (128, 128, 128)
            )  # Default to gray if color not found
            draw.rectangle(
                [
                    x * cell_size + border,
                    y * cell_size + border,
                    x * cell_size + color_size,
                    y * cell_size + color_size,
                ],
                fill=color,
            )

    image.save(filename)


def process_puzzle(puzzle_data, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    for i, example in enumerate(puzzle_data["train"]):
        create_grid_image(
            example["input"], os.path.join(output_dir, f"train_{i+1}_input.png")
        )
        create_grid_image(
            example["output"], os.path.join(output_dir, f"train_{i+1}_output.png")
        )

    for i, test in enumerate(puzzle_data["test"]):
        create_grid_image(
            test["input"], os.path.join(output_dir, f"test_{i+1}_input.png")
        )
        if "output" in test:
            create_grid_image(
                test["output"], os.path.join(output_dir, f"test_{i+1}_output.png")
            )


def process_all_puzzles(input_dir, output_base_dir):
    for json_file in glob.glob(os.path.join(input_dir, "*.json")):
        puzzle_name = os.path.splitext(os.path.basename(json_file))[0]
        output_dir = os.path.join(output_base_dir, puzzle_name)

        with open(json_file, "r") as f:
            puzzle_data = json.load(f)

        process_puzzle(puzzle_data, output_dir)
        print(f"Processed puzzle: {puzzle_name}")


def image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()


def main():
    input_dir = "."  # Directory containing JSON files
    output_base_dir = "images"  # Base directory for output images
    #  puzzle_images
    process_all_puzzles(input_dir, output_base_dir)
    print(f"All puzzles processed. Images generated in {output_base_dir}")


if __name__ == "__main__":
    main()

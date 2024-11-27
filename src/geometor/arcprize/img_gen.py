import json
import os
from pathlib import Path
import glob
from PIL import Image, ImageDraw, ImageFont
from geometor.arcprize.puzzles import Puzzle, PuzzleSet, Grid
import numpy as np


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


def create_grid_image(grid, filename, cell_size=8, add_text=False):
    border = 1
    color_size = cell_size - 2 * border
    width = grid.width * cell_size
    height = grid.height * cell_size

    image = Image.new("RGB", (width, height), color="black")
    draw = ImageDraw.Draw(image)

    try:
        font_size = max(cell_size // 2, 8)  # Adjust font size based on cell size
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    for y in range(grid.height):
        for x in range(grid.width):
            color = COLOR_MAP.get(grid.matrix[y, x], (128, 128, 128))
            draw.rectangle(
                [
                    x * cell_size + border,
                    y * cell_size + border,
                    (x + 1) * cell_size - border,
                    (y + 1) * cell_size - border,
                ],
                fill=color,
            )

            if add_text:
                value = str(grid.matrix[y, x])
                text_bbox = draw.textbbox((0, 0), value, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]

                text_x = x * cell_size + (cell_size - text_width) // 2
                text_y = y * cell_size + (cell_size - text_height) // 2

                draw.text((text_x + 1, text_y - 1), value, fill="black", font=font)

    image.save(filename)


def text_to_grid(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    #  grid = [list(map(int, line.strip().split())) for line in lines]
    #  grid = [[int(num) for num in line.strip().split()] for line in lines]
    grid = []
    for line in lines:
        row = [int(num) for num in line.strip().split()]
        print(row)
        if row:  # Only add non-empty rows
            grid.append(row)

    return Grid(grid, "0", "test", 0, "output")


def text_to_image(input_file="proposed.txt", output_file="proposed.png"):
    grid = text_to_grid(input_file)
    print(grid)
    create_grid_image(grid, output_file, cell_size=16, add_text=True)


def create_puzzle_pair(input_grid, output_grid, output_dir: Path):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    def create_image_size(basename, grid):
        sizes = [8, 16, 32]
        for size in sizes:
            create_grid_image(
                grid, output_dir / f"{basename}_{size}.png", cell_size=size
            )
            if size in (16, 32):
                create_grid_image(
                    grid,
                    output_dir / f"{basename}_{size}_numbered.png",
                    cell_size=size,
                    add_text=True,
                )

    create_image_size("input", input_grid)
    create_image_size("output", output_grid)


def process_all_puzzles(puzzle_set: PuzzleSet, output_base_dir: Path):
    output_base_dir = Path(output_base_dir)

    # Create color map image and text file in root artifacts folder
    create_color_map_image(output_base_dir)
    create_color_map_text(output_base_dir)

    for puzzle in puzzle_set.puzzles:
        puzzle_dir = output_base_dir / str(puzzle.id)

        for i, pair in enumerate(puzzle.train, 1):
            pair_dir = puzzle_dir / f"train_{i}"
            pair_dir.mkdir(parents=True, exist_ok=True)
            create_puzzle_pair(pair.input, pair.output, pair_dir)

        for i, pair in enumerate(puzzle.test, 1):
            pair_dir = puzzle_dir / f"test_{i}"
            pair_dir.mkdir(parents=True, exist_ok=True)
            create_puzzle_pair(pair.input, pair.output, pair_dir)

        print(f"Processed puzzle: {puzzle.id}")


def image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

    from PIL import Image, ImageDraw, ImageFont


def create_color_map_image(output_dir: Path):
    swatch_size = 100
    font_size = 60  # This is now correctly used
    padding = 20
    text_width = 300

    image_width = swatch_size + padding * 3 + text_width
    image_height = (swatch_size + padding) * len(COLOR_MAP) + padding

    image = Image.new("RGB", (image_width, image_height), color="black")
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()
        font = font.font_variant(size=font_size)  # Resize the default font

    for i, (index, color) in enumerate(COLOR_MAP.items()):
        y = padding + i * (swatch_size + padding)

        # Draw color swatch
        draw.rectangle([padding, y, padding + swatch_size, y + swatch_size], fill=color)

        # Draw index number and color name
        text = f"{index}: {color_name(index)}"
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_height = text_bbox[3] - text_bbox[1]
        text_y = (
            y + (swatch_size - text_height) // 2
        )  # Center text vertically with swatch
        draw.text((padding * 2 + swatch_size, text_y), text, fill="white", font=font)

    image.save(output_dir / "color_map.png")


def create_color_map_text(output_dir: Path):
    with open(output_dir / "color_map.txt", "w") as f:
        f.write("COLOR_MAP = {\n")
        for index, color in COLOR_MAP.items():
            f.write(f"    {index}: {color},  # {color_name(index)}\n")
        f.write("}\n")


def color_name(index):
    names = [
        "White",
        "Blue",
        "Red",
        "Green",
        "Yellow",
        "Gray",
        "Magenta",
        "Orange",
        "Azure",
        "Maroon",
    ]
    return names[index] if index < len(names) else f"Color {index}"

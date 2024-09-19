import json
import svgwrite

def create_grid_svg(dwg, grid, start_x, start_y, cell_size, title):
    elements = []

    # Add title
    elements.append(
        dwg.text(
            title,
            insert=(start_x + len(grid[0]) * cell_size / 2, start_y - 10),
            text_anchor="middle",
            font_size=14,
            font_family="Arial",
            fill="gray",
        )
    )

    # Draw background
    elements.append(
        dwg.rect(
            insert=(start_x, start_y),
            size=(len(grid[0]) * cell_size, len(grid) * cell_size),
            fill="black",
        )
    )

    # Draw grid as text
    for y, row in enumerate(grid):
        elements.append(
            dwg.text(
                row,
                insert=(start_x + 5, start_y + (y + 0.7) * cell_size),
                font_size=14,
                font_family="monospace",
                fill="white",
            )
        )

    return elements

def create_puzzle_svg(puzzle, filename):
    input_grid = puzzle["input_grid"].split("\n")
    output_grid = puzzle["output_grid"].split("\n")

    cell_size = 20  # Adjusted for monospace font
    max_line_length = max(max(len(line) for line in input_grid), 
                          max(len(line) for line in output_grid))
    grid_width = max_line_length * cell_size
    grid_height = len(input_grid) * cell_size
    padding = 20
    total_width = grid_width * 2 + padding * 3
    total_height = grid_height + padding * 2

    dwg = svgwrite.Drawing(filename, size=(f"{total_width}px", f"{total_height}px"))

    # Create input grid
    input_elements = create_grid_svg(
        dwg, input_grid, padding, padding, cell_size, "Input Grid"
    )
    for element in input_elements:
        dwg.add(element)

    # Create output grid
    output_elements = create_grid_svg(
        dwg, output_grid, grid_width + padding * 2, padding, cell_size, "Output Grid"
    )
    for element in output_elements:
        dwg.add(element)

    # Add puzzle information
    info_text = f"Model: {puzzle['model']}, Response: {puzzle['model_response']}, Correct: {puzzle['correct_answer']}"
    dwg.add(
        dwg.text(
            info_text,
            insert=(padding, total_height - 10),
            font_size=12,
            font_family="Arial",
            fill="black",
        )
    )

    dwg.save()

def visualize_puzzles(json_file):
    with open(json_file, "r") as f:
        data = json.load(f)

    for i, puzzle in enumerate(data["results"]):
        filename = f"puzzle_{i+1}.svg"
        create_puzzle_svg(puzzle, filename)
        print(f"Created {filename}")

if __name__ == "__main__":
    json_file = "../../../../../demos/rotation_puzzle_results_20240802_084405.json"  # Replace with your JSON file name
    visualize_puzzles(json_file)


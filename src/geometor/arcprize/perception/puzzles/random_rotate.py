
import random
import numpy as np
from jinja2 import Environment, PackageLoader


from geometor.arcprize.perception.grids.random_rectangles import generate_grid
from geometor.arcprize.perception.grids.tools import rotate_grid, introduce_errors, grid_to_string
from geometor.arcprize.perception.symbols import SYMBOL_SETS


def generate_puzzle(size=3, error_chance=0.1, max_errors=1, symbol_set_key="digits"):
    symbol_set = SYMBOL_SETS[symbol_set_key]
    input_grid = generate_grid(size, size, symbol_set)
    rotation = random.choice(["none", "right", "left", "full"])
    output_grid = rotate_grid(input_grid, rotation)

    output_grid = introduce_errors(output_grid, error_chance, max_errors, symbol_set)

    if not np.array_equal(output_grid, rotate_grid(input_grid, rotation)):
        rotation = "error"

    return input_grid, output_grid, rotation


def generate_prompt(input_grid, output_grid, row_delimiter="\n", cell_delimiter=" "):
    env = Environment(
            loader=PackageLoader("geometor.arcprize.perception", "puzzles"),
    )
    template_variables = {
        "input_grid": grid_to_string(input_grid, row_delimiter, cell_delimiter),
        "output_grid": grid_to_string(output_grid, row_delimiter, cell_delimiter),
    }
    template = env.get_template("random_rotate.txt.j2")
    prompt = template.render(template_variables)

    return prompt


def generate_puzzle_set(
    num_puzzles,
    min_size=3,
    max_size=5,
    error_chance=0.1,
    max_errors=1,
    symbol_set_key="digits",
    row_delimiter="\n",
    cell_delimiter=" ",
):
    puzzles = []
    for i in range(num_puzzles):
        size = random.randint(min_size, max_size)
        input_grid, output_grid, rotation = generate_puzzle(
            size, error_chance, max_errors, symbol_set_key
        )
        prompt = generate_prompt(input_grid, output_grid, row_delimiter, cell_delimiter)
        puzzles.append(
            (i, prompt, rotation, size, symbol_set_key, input_grid, output_grid)
        )
    return puzzles

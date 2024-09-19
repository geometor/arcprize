from geometor.arcprize.model import Puzzle, Grid
from typing import Tuple, List


class PuzzlePlayer:
    def __init__(self, puzzle: Puzzle):
        self.puzzle = puzzle
        self.current_output = None
        self.attempts = 0
        self.max_attempts = 3

    def get_examples(self) -> List[Tuple[Grid, Grid]]:
        return [(pair.input, pair.output) for pair in self.puzzle.train]

    def get_test_input(self) -> Grid:
        return self.puzzle.test[0].input

    def set_output_grid_size(self, width: int, height: int):
        self.current_output = Grid(
            [[0 for _ in range(width)] for _ in range(height)],
            self.puzzle.id,
            "test",
            0,
            "output",
        )

    def set_color(self, cells: List[Tuple[int, int]], color: int):
        if self.current_output is None:
            raise ValueError(
                "Output grid not initialized. Call set_output_grid_size first."
            )
        for x, y in cells:
            if (
                0 <= x < self.current_output.width
                and 0 <= y < self.current_output.height
            ):
                self.current_output.matrix[y, x] = color
            else:
                print(f"Warning: Cell ({x}, {y}) is out of bounds and will be skipped.")

    def fill_contiguous_region(self, start: Tuple[int, int], new_color: int):
        if self.current_output is None:
            raise ValueError(
                "Output grid not initialized. Call set_output_grid_size first."
            )

        x, y = start
        if not (
            0 <= x < self.current_output.width and 0 <= y < self.current_output.height
        ):
            raise ValueError(f"Starting point ({x}, {y}) is out of bounds.")

        old_color = self.current_output.matrix[y, x]
        if old_color == new_color:
            return  # No need to fill if the colors are the same

        points_to_fill = self.get_contiguous_points(start, old_color)
        self.set_color(list(points_to_fill), new_color)

    def get_contiguous_points(
        self, start: Tuple[int, int], target_color: int
    ) -> Set[Tuple[int, int]]:
        """
        Returns a set of points that are contiguous with the starting point and have the target color.
        This is a placeholder implementation and should be replaced with a more efficient algorithm.
        """
        if self.current_output is None:
            raise ValueError(
                "Output grid not initialized. Call set_output_grid_size first."
            )

        contiguous_points = set()
        stack = [start]
        width, height = self.current_output.width, self.current_output.height

        while stack:
            x, y = stack.pop()
            if (x, y) in contiguous_points:
                continue

            if (
                0 <= x < width
                and 0 <= y < height
                and self.current_output.matrix[y, x] == target_color
            ):
                contiguous_points.add((x, y))
                stack.extend([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])

        return contiguous_points

    def copy_input_to_output(self):
        input_grid = self.get_test_input()
        self.set_output_grid_size(input_grid.width, input_grid.height)
        self.current_output.matrix = input_grid.matrix.copy()

    def clear_output_grid(self):
        if self.current_output is None:
            raise ValueError(
                "Output grid not initialized. Call set_output_grid_size first."
            )
        self.current_output.matrix.fill(0)

    def submit_solution(self) -> bool:
        if self.current_output is None:
            raise ValueError("No solution to submit. Create an output grid first.")
        if self.attempts >= self.max_attempts:
            return False
        self.attempts += 1
        return self.check_solution()

    def check_solution(self) -> bool:
        expected_output = self.puzzle.test[0].output
        return (self.current_output.matrix == expected_output.matrix).all()

    def reset(self):
        self.current_output = None
        self.attempts = 0

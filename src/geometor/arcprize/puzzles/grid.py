import numpy as np
from geometor.model import Model

class Grid:
    def __init__(self, matrix, puzzle_id, set_type, index, io_type):
        self.matrix = np.array(matrix, dtype=int)
        self.puzzle_id = puzzle_id
        self.set_type = set_type  # 'train' or 'test'
        self.index = index
        self.io_type = io_type  # 'input' or 'output'
        self._model = None

    @property
    def name(self):
        return f"{self.puzzle_id}-{self.set_type}-{self.index}-{self.io_type}"

    @property
    def height(self):
        return self.matrix.shape[0]

    @property
    def width(self):
        return self.matrix.shape[1]

    @property
    def size(self):
        return self.matrix.size

    @property
    def colors(self):
        return set(np.unique(self.matrix))

    @property
    def color_counts(self):
        unique, counts = np.unique(self.matrix, return_counts=True)
        return dict(zip(unique, counts))

    @property
    def model(self):
        if self._model is None:
            self._model = self._create_model()
        return self._model

    def _create_model(self):
        model = Model(self.name)
        for y in range(self.height):
            for x in range(self.width):
                val = self.matrix[y, x]
                model.set_point(x, y, classes=[str(val)], label=f"({x},{y})")
        return model

    def rotate(self, k=1):
        """
        Rotate the grid by 90 degrees k times.
        Positive k means clockwise rotation, negative k means counter-clockwise.
        """
        new_matrix = np.rot90(self.matrix, k=-k)
        return Grid(new_matrix, self.puzzle_id, self.set_type, self.index, f"{self.io_type}_rotated{k*90}")

    def flip(self, axis=0):
        """
        Flip the grid along the specified axis.
        axis=0 flips vertically, axis=1 flips horizontally.
        """
        new_matrix = np.flip(self.matrix, axis=axis)
        flip_type = "vertical" if axis == 0 else "horizontal"
        return Grid(new_matrix, self.puzzle_id, self.set_type, self.index, f"{self.io_type}_flipped_{flip_type}")

    def to_string(self, row_delimiter="\n", cell_delimiter=" "):
        return row_delimiter.join(
            cell_delimiter.join(str(cell) for cell in row) for row in self.matrix
        )


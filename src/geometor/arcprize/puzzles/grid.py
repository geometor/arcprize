import numpy as np
from geometor.model import Model

from PIL import Image, ImageDraw, ImageFont

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
        return Grid(
            new_matrix,
            self.puzzle_id,
            self.set_type,
            self.index,
            f"{self.io_type}_rotated{k*90}",
        )

    def flip(self, axis=0):
        """
        Flip the grid along the specified axis.
        axis=0 flips vertically, axis=1 flips horizontally.
        """
        new_matrix = np.flip(self.matrix, axis=axis)
        flip_type = "vertical" if axis == 0 else "horizontal"
        return Grid(
            new_matrix,
            self.puzzle_id,
            self.set_type,
            self.index,
            f"{self.io_type}_flipped_{flip_type}",
        )

    def to_string(self, row_delimiter="\n", cell_delimiter=" "):
        return row_delimiter.join(
            cell_delimiter.join(str(cell) for cell in row) for row in self.matrix
        )

    def to_image(grid, cell_size=32, add_text=False):
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
                color = COLOR_MAP.get(grid.matrix[y, x], (0, 0, 0))
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

        return image

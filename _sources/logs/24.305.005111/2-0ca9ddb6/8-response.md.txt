```python
import numpy as np

working_output = np.copy(test_input)

def add_cross(grid, row, col, color, pattern_color):
    rows, cols = grid.shape
    if row > 0 and grid[row-1, col] == 0: grid[row - 1, col] = pattern_color
    if row < rows - 1 and grid[row+1, col] == 0: grid[row + 1, col] = pattern_color
    if col > 0 and grid[row, col-1] == 0: grid[row, col - 1] = pattern_color
    if col < cols - 1 and grid[row, col+1] == 0: grid[row, col + 1] = pattern_color

rows, cols = np.where(working_output == 2)
for r, c in zip(rows, cols):
    add_cross(working_output, r, c, 2, 4)

rows, cols = np.where(working_output == 1)
for r, c in zip(rows, cols):
    add_cross(working_output, r, c, 1, 7)

print("Updated Working Output Grid:")
print(working_output)

submit_result = submit()
print(submit_result)

```


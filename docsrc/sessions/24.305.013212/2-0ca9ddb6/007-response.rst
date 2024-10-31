007 • Response
==============


.. meta::
   :puzzle_id: 2-0ca9ddb6
   :timestamp: 24.305.013212
   :call_count: 7

The working output grid is initialized correctly, matching the input grid.  Now, let's proceed with the transformations using `set_pixel()` in loops.


code_execution:
```python
import numpy as np

# Initialize the output grid (already done in the interface, but replicated here for completeness)
output_grid = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 1, 0, 0],
                        [0, 0, 2, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 8, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 6, 0, 0, 0, 0, 0, 2, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0]])

rows, cols = output_grid.shape


for r in range(rows):
  for c in range(cols):
      if output_grid[r, c] == 2:  # Red
          for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]: # Up, down, right, left
              nr, nc = r + dr, c + dc
              if 0 <= nr < rows and 0 <= nc < cols:
                  output_grid[nr, nc] = 4 # Yellow

      elif output_grid[r, c] == 1: #Blue
          for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]: # Up, down, right, left
              nr, nc = r + dr, c + dc
              if 0 <= nr < rows and 0 <= nc < cols:
                  output_grid[nr, nc] = 7  # Orange
                  
print(output_grid)
```

function_calls:
set_pixel 4 1 2
set_pixel 4 3 2
set_pixel 3 2 4
set_pixel 5 2 4
set_pixel 7 1 2
set_pixel 7 7 4
set_pixel 8 7 4
set_pixel 6 7 4
set_pixel 2 6 7
set_pixel 4 6 7
set_pixel 2 8 7

submit


.. seealso::

   - :doc:`007-history`
   - :doc:`007-prompt`


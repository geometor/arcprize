Here's a solution that uses `set_pixel` to add blue pixels adjacent to each azure block.  The strategy prioritizes adding the blue pixel to an unoccupied adjacent location to avoid creating larger blue blocks.  This approach directly modifies the grid using the provided API functions and avoids unnecessary array copies:

```python
import numpy as np

test_input = np.array([[0, 0, 0, 0, 0, 8, 8],
                     [8, 8, 0, 0, 0, 0, 8],
                     [8, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 8, 0, 0, 0],
                     [0, 0, 0, 8, 8, 0, 0],
                     [0, 8, 0, 0, 0, 0, 0],
                     [8, 8, 0, 0, 0, 0, 0]])

def find_azure_blocks(grid):
    rows, cols = grid.shape
    azure_blocks = []
    visited = np.zeros((rows, cols), dtype=bool)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 8 and not visited[r, c]:
                block = []
                q = [(r, c)]
                while q:
                    curr_r, curr_c = q.pop(0)
                    if 0 <= curr_r < rows and 0 <= curr_c < cols and grid[curr_r, curr_c] == 8 and not visited[curr_r, curr_c]:
                        block.append((curr_r, curr_c))
                        visited[curr_r, curr_c] = True
                        q.extend([(curr_r + 1, curr_c), (curr_r - 1, curr_c), (curr_r, curr_c + 1), (curr_r, curr_c - 1)])
                azure_blocks.append(block)
    return azure_blocks

azure_blocks = find_azure_blocks(test_input)

# Initialize the output grid.  We'll use an empty grid of the same size.
output_grid = np.zeros_like(test_input)


def set_pixel(color: int, column: int, row: int) -> dict:
    """Set grid value at a specific coordinate."""
    print(f"Setting pixel at ({row}, {column}) to {color}")
    global output_grid
    output_grid[row, column] = color
    return {"status": "success"}

for block in azure_blocks:
    for r, c in block:
        # Attempt to place blue pixel to the right
        if c + 1 < output_grid.shape[1] and output_grid[r, c + 1] == 0:
            set_pixel(color=1, column=c + 1, row=r)
            continue
        # Attempt to place blue pixel above
        if r - 1 >= 0 and output_grid[r - 1, c] == 0:
            set_pixel(color=1, column=c, row=r - 1)
            continue
        # Attempt to place blue pixel below
        if r + 1 < output_grid.shape[0] and output_grid[r + 1, c] == 0:
            set_pixel(color=1, column=c, row=r + 1)
            continue
        # Attempt to place blue pixel to the left
        if c - 1 >= 0 and output_grid[r, c - 1] == 0:
            set_pixel(color=1, column=c - 1, row=r)
            continue

print(f"{output_grid=}")

def submit() -> dict:
    """Submit the working grid and check for correctness."""
    print("Submitting solution...")
    # Replace this with the actual submission logic provided by the ARC-AGI system.
    return {"status": "submitted", "solution": output_grid.tolist()}

submission_result = submit()
print(f"{submission_result=}")

```

This code directly uses the provided `set_pixel` function and a placeholder `submit` function.  The output grid will be printed before submission, allowing for a final visual check. Remember to replace the placeholder `submit()` call with the actual submission function provided by the ARC-AGI system.  The solution's accuracy depends on the correctness of the `submit` function's implementation in the ARC-AGI system.




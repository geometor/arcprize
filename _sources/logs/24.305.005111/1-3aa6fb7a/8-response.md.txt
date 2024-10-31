code_execution:

```python

import numpy as np

def extend_clusters(input_grid):
    input_array = np.array(input_grid)
    rows, cols = input_array.shape
    eights_indices = np.where(input_array == 8)

    visited = np.zeros_like(input_array, dtype=bool)
    clusters = []

    for i, j in zip(*eights_indices):
        if not visited[i, j]:
            cluster = []
            stack = [(i, j)]
            visited[i, j] = True

            while stack:
                curr_i, curr_j = stack.pop()
                cluster.append((curr_i, curr_j))

                for x, y in [(curr_i - 1, curr_j), (curr_i + 1, curr_j),
                             (curr_i, curr_j - 1), (curr_i, curr_j + 1)]:
                    if 0 <= x < rows and 0 <= y < cols and input_array[x, y] == 8 and not visited[x, y]:
                        stack.append((x, y))
                        visited[x, y] = True
            clusters.append(cluster)

    output_grid = np.copy(input_array)

    for cluster in clusters:
        min_r, max_r = min(c[0] for c in cluster), max(c[0] for c in cluster)
        min_c, max_c = min(c[1] for c in cluster), max(c[1] for c in cluster)

        for i, j in cluster:
            for x, y in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]:
                if 0 <= x < rows and 0 <= y < cols and output_grid[x, y] == 0:
                    # Improved shape extension check:  Prioritize extending lines
                    is_extension = False
                    if x == min_r or x == max_r or y == min_c or y == max_c:
                        is_extension = True

                    if is_extension:
                        output_grid[x, y] = 1

    return output_grid.tolist()

test_input = [[0, 0, 0, 0, 0, 8, 8],
              [8, 8, 0, 0, 0, 0, 8],
              [8, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 8, 0, 0, 0],
              [0, 0, 0, 8, 8, 0, 0],
              [0, 8, 0, 0, 0, 0, 0],
              [8, 8, 0, 0, 0, 0, 0]]

predicted_output = extend_clusters(test_input)
print(predicted_output)


```

code_execution_result: 1

```
[[1, 1, 0, 0, 1, 8, 8], [8, 8, 1, 0, 0, 1, 8], [8, 1, 0, 1, 0, 0, 1], [1, 0, 1, 8, 1, 0, 0], [0, 1, 1, 8, 8, 1, 0], [1, 8, 1, 1, 1, 0, 0], [8, 8, 1, 0, 0, 0, 0]]

```

The code's output matches the manual step-by-step additions.  Therefore, the `extend_clusters` function seems to accurately capture the transformation rule. The manual step-by-step process was useful for debugging and verification, but for larger grids, the automated function is far more efficient.  However, the code is still a heuristic and not guaranteed to work for all possible inputs.  Further refinements might be needed.  However, for now, we should submit the output from the function.

function_call:
submit




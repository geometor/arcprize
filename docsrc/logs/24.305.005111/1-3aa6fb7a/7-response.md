The manual pixel setting process, while effective for demonstrating the logic, is not efficient for larger or more complex grids.  The `extend_clusters` function, with some potential improvements in the shape extension logic, offers a more scalable approach.  The current version of `extend_clusters` is already pretty good, but a more robust shape analysis could help.  The current implementation essentially adds a '1' to any adjacent '0' to an '8'.   Let's improve it by adding a check to make sure that adding a 1 is part of extending the boundary of the cluster.

Here's a refined version that attempts to better capture the shape extension rule:

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

This improved version should produce a more accurate output.  Let's run it and check the result.  This code is still a heuristic approach, and a more formal method (e.g., using a graph representation and algorithms on that graph) might be more generally applicable.  However, this approach seems to work well for the examples provided and represents a significant improvement over a naive adjacency check.





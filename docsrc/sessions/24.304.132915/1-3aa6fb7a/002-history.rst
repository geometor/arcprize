002 • History
=============


.. meta::
   :puzzle_id: 1-3aa6fb7a
   :timestamp: 24.304.132915
   :call_count: 2

Begin puzzle: 1-3aa6fb7a

**example_1**

**input**


.. code-block::

    [[0 0 0 0 0 0 0]
     [0 8 0 0 0 0 0]
     [0 8 8 0 0 0 0]
     [0 0 0 0 8 8 0]
     [0 0 0 0 0 8 0]
     [0 0 0 0 0 0 0]
     [0 0 0 0 0 0 0]]

[Image]

**output**


.. code-block::

    [[0 0 0 0 0 0 0]
     [0 8 1 0 0 0 0]
     [0 8 8 0 0 0 0]
     [0 0 0 0 8 8 0]
     [0 0 0 0 1 8 0]
     [0 0 0 0 0 0 0]
     [0 0 0 0 0 0 0]]

[Image]

**observations**

**example_1**

**input:**
```
width: 7
height: 7
colors:
  - 0: 43
  - 8: 5
objects:
  - a cluster of 8s, starting at (1,1) and extending to (3,3)
  - a cluster of 8s, starting at (3,4) and extending to (4,5)
```

**output:**
```
width: 7
height: 7
colors:
  - 0: 42
  - 8: 5
  - 1: 2
objects:
  - a cluster of 8s, starting at (1,1) and extending to (3,3)
  - a cluster of 8s, starting at (3,4) and extending to (4,5)
  - a blue pixel at (1,2)
  - a blue pixel at (4,4)

```

**differences:**
```
cells_changed: 2
colors_changed: two 0s changed to 1s (blue)
```

**transformation:**
```
-The transformation appears to involve changing some of the 0s (white) to 1s (blue).  Specifically, it looks like the 0s that are adjacent (horizontally or vertically) to an 8 are changed to 1s. The 0s that are diagonally adjacent to an 8 seem to remain unchanged.
```

To verify this hypothesis, let's examine additional examples.

**example_2**

**input**


.. code-block::

    [[0 0 0 0 8 8 0]
     [0 0 0 0 0 8 0]
     [0 0 8 0 0 0 0]
     [0 0 8 8 0 0 0]
     [0 0 0 0 0 0 0]
     [0 0 0 0 8 0 0]
     [0 0 0 8 8 0 0]]

[Image]

**output**


.. code-block::

    [[0 0 0 0 8 8 0]
     [0 0 0 0 1 8 0]
     [0 0 8 1 0 0 0]
     [0 0 8 8 0 0 0]
     [0 0 0 0 0 0 0]
     [0 0 0 1 8 0 0]
     [0 0 0 8 8 0 0]]

[Image]

**observations**


- review the example grids


- check for differences and patterns


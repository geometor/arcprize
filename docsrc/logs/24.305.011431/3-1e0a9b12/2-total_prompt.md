Begin puzzle: 3-1e0a9b12


# example_1

## input:

[[0 4 0 9]
 [0 0 0 0]
 [0 4 6 0]
 [1 0 0 0]]


[Image]


## output:

[[0 0 0 0]
 [0 0 0 0]
 [0 4 0 0]
 [1 4 6 9]]


[Image]


## observations:

Here's an analysis of example_1:

**input:**
  - width: 4
  - height: 4
  - colors:
    - 0: 10
    - 1: 1
    - 4: 2
    - 6: 1
    - 9: 1
  - objects:
    - Yellow (4):  Two separate single pixels located at (0,1) and (2,1).
    - Maroon (9): Single pixel at (0,3)
    - Blue (1): Single pixel at (3,0)
    - Magenta (6): Single pixel at (2,2)


**output:**
  - width: 4
  - height: 4
  - colors:
    - 0: 12
    - 1: 1
    - 4: 2
    - 6: 1
    - 9: 1
  - objects:
    - Yellow (4): Two single pixels located at (2,1) and (3,1).
    - Maroon (9): Single pixel at (3,3)
    - Blue (1): Single pixel at (3,0)
    - Magenta (6): Single pixel at (3,2)

**differences:**
  - cells_changed: 8
  - colors_changed: The non-zero colored pixels are moved to the bottom row, preserving their relative positions to each other.


**transformation:**
  - The non-zero colored pixels are collected and moved to the bottom-right corner of the grid, maintaining their relative positions to one another.  The rest of the grid is filled with white (0).  It appears to be a type of "gathering" or "collection" transformation.



# example_2

## input:

[[0 0 0 0 0 9]
 [0 0 0 8 0 0]
 [0 0 0 0 0 0]
 [4 0 0 0 0 0]
 [4 0 7 8 0 0]
 [4 0 7 0 0 0]]


[Image]


## output:

[[0 0 0 0 0 0]
 [0 0 0 0 0 0]
 [0 0 0 0 0 0]
 [4 0 0 0 0 0]
 [4 0 7 8 0 0]
 [4 0 7 8 0 9]]


[Image]


## observations:

- review the example grids

- check for differences and patterns


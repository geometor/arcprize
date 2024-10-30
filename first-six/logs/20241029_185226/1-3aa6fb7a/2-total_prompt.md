Begin puzzle: 1-3aa6fb7a


# example_1

## input:

[[0 0 0 0 0 0 0]
 [0 8 0 0 0 0 0]
 [0 8 8 0 0 0 0]
 [0 0 0 0 8 8 0]
 [0 0 0 0 0 8 0]
 [0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0]]


[Image]


## output:

[[0 0 0 0 0 0 0]
 [0 8 1 0 0 0 0]
 [0 8 8 0 0 0 0]
 [0 0 0 0 8 8 0]
 [0 0 0 0 1 8 0]
 [0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0]]


[Image]


## observations:

Here's an analysis of example_1:

**input:**

*   width: 7
*   height: 7
*   colors:
    *   0: (40)
    *   8: (6)
*   objects:
    *   A cluster of 6 azure pixels forming an irregular shape.

**output:**

*   width: 7
*   height: 7
*   colors:
    *   0: (38)
    *   8: (6)
    *   1: (2)
*   objects:
    *   The same azure cluster as in the input.
    *   Two blue pixels, one replacing an adjacent white pixel above a top azure pixel, one replacing a white pixel below a bottom azure pixel.


**differences:**

*   cells_changed: 2
*   colors_changed: Two white pixels changed to blue (1).

**transformation:**

*   The transformation appears to involve adding two blue pixels.  The positions of the added blue pixels seem to be determined by the positions of the existing azure pixels in the input. Specifically, a blue pixel is added directly above one of the azure pixels at the top of the cluster and one directly below an azure pixel at the bottom.  There may be some additional constraints, but this initial observation holds true.




# example_2

## input:

[[0 0 0 0 8 8 0]
 [0 0 0 0 0 8 0]
 [0 0 8 0 0 0 0]
 [0 0 8 8 0 0 0]
 [0 0 0 0 0 0 0]
 [0 0 0 0 8 0 0]
 [0 0 0 8 8 0 0]]


[Image]


## output:

[[0 0 0 0 8 8 0]
 [0 0 0 0 1 8 0]
 [0 0 8 1 0 0 0]
 [0 0 8 8 0 0 0]
 [0 0 0 0 0 0 0]
 [0 0 0 1 8 0 0]
 [0 0 0 8 8 0 0]]


[Image]


## observations:

- review the example grids

- check for differences and patterns


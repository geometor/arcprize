Puzzle 6-0520fde7 - History 2
=============================


.. meta::
   :puzzle_id: 6-0520fde7
   :timestamp: 24.304.091044
   :call_count: 2


.. code-block::

    Begin puzzle: 6-0520fde7
    
    


.. code-block::

    # example_1
    

## input:


.. code-block::

    [[1 0 0 5 0 1 0]
     [0 1 0 5 1 1 1]
     [1 0 0 5 0 0 0]]



[Image]


## output:


.. code-block::

    [[0 0 0]
     [0 2 0]
     [0 0 0]]



[Image]


## observations:


.. code-block::

    Here's an analysis of example_1:
    
    **input:**
      - width: 7
      - height: 3
      - colors:
        - 0: (11)
        - 1: (5)
        - 5: (3)
      - objects:
        - A vertical block of 5's in the center, 3x1
        -  Several scattered blue (1) pixels.
    
    
    **output:**
      - width: 3
      - height: 3
      - colors:
        - 0: (8)
        - 2: (1)
      - objects:
        - A single red (2) pixel in the center.
    
    
    **differences:**
      - cells_changed: 21  (The output is much smaller than the input)
      - colors_changed: The input has blue and gray pixels; the output only has red and white pixels.  The central 5 becomes a 2.
    
    
    **transformation:**
    - The transformation drastically reduces the size of the grid.
    - The central column of '5's in the input seems to be related to the central '2' in the output.  Possibly the central value from the largest continuous vertical block is extracted and transformed to a different color.  The surrounding pixels are all set to white.
    
    
    
    To confirm this hypothesis, more examples are needed to see how the transformation handles different input configurations and sizes.  Specifically, I'd like to see examples with varying sizes of vertical blocks, different central values, and  different surrounding colors.  Knowing how these elements affect the output will be key to discerning the underlying transformation.
    
    


.. code-block::

    # example_2
    

## input:


.. code-block::

    [[1 1 0 5 0 1 0]
     [0 0 1 5 1 1 1]
     [1 1 0 5 0 1 0]]



[Image]


## output:


.. code-block::

    [[0 2 0]
     [0 0 2]
     [0 2 0]]



[Image]


## observations:

- review the example grids

- check for differences and patterns


003 • Response
==============


.. meta::
   :puzzle_id: 3-1e0a9b12
   :timestamp: 24.305.013736
   :call_count: 3

**example_3**
input:
  width: 5
  height: 5
  colors:
    - 0: (18)
    - 1: (2)
    - 2: (1)
    - 3: (3)
    - 6: (1)
output:
  width: 5
  height: 5
  colors:
    - 0: (19)
    - 1: (2)
    - 2: (1)
    - 3: (3)
    - 6: (1)
differences:
  cells_changed: 5
  colors_changed: pixels shifted to last row
transformation:
  - non-zero pixels are shifted to the bottom row and left justified in order of appearance from top to bottom, left to right.


Ruminations:
The transformation rules appear consistent across all examples.  Non-zero pixels shift to the bottom row and are ordered based on their position from left to right, top to bottom in the input grid.  Empty positions are filled with zeros.


.. seealso::

   - :doc:`003-history`
   - :doc:`003-prompt`


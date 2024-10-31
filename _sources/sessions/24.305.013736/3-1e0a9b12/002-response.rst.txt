002 • Response
==============


.. meta::
   :puzzle_id: 3-1e0a9b12
   :timestamp: 24.305.013736
   :call_count: 2

**example_2**
input:
  width: 6
  height: 6
  colors:
    - 0: (28)
    - 4: (3)
    - 7: (2)
    - 8: (2)
    - 9: (1)
output:
  width: 6
  height: 6
  colors:
    - 0: (26)
    - 4: (3)
    - 7: (2)
    - 8: (2)
    - 9: (1)
differences:
  cells_changed: 2
  colors_changed: maroon moved from top right to bottom right. One azure has appeared bottom left
transformation:
  - maroon moves from top right to bottom right
  - azure appears on the bottom row as well.
  - seems as though the non-zero pixels again, "fall" to the bottom row and shift to the left


Ruminations:
It appears the transformation shifts all non-zero color pixels down to the last row.  They then shift left, ordered by their first appearance scanning top to bottom, left to right. Zeros are added to vacant cells.


.. seealso::

   - :doc:`002-history`
   - :doc:`002-prompt`


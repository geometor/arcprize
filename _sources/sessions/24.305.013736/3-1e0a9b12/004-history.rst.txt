004 • History
=============


.. meta::
   :puzzle_id: 3-1e0a9b12
   :timestamp: 24.305.013736
   :call_count: 4

Begin puzzle: 3-1e0a9b12

**example_1**

**input**


.. code-block::

    [[0 4 0 9]
     [0 0 0 0]
     [0 4 6 0]
     [1 0 0 0]]


.. image:: _images/004-1.png
   :alt: Grid visualization
   :align: center

**output**


.. code-block::

    [[0 0 0 0]
     [0 0 0 0]
     [0 4 0 0]
     [1 4 6 9]]


.. image:: _images/004-2.png
   :alt: Grid visualization
   :align: center

**observations**

**example_1**
input:
  width: 4
  height: 4
  colors:
    - 0: (9)
    - 1: (1)
    - 4: (2)
    - 6: (1)
    - 9: (1)
output:
  width: 4
  height: 4
  colors:
    - 0: (12)
    - 1: (1)
    - 4: (2)
    - 6: (1)
    - 9: (1)
differences:
  cells_changed: 4
  colors_changed: the non-zero color pixels have moved to the last row
transformation:
  - non-zero pixels shift down to the last row and left to ordered positions

**example_2**

**input**


.. code-block::

    [[0 0 0 0 0 9]
     [0 0 0 8 0 0]
     [0 0 0 0 0 0]
     [4 0 0 0 0 0]
     [4 0 7 8 0 0]
     [4 0 7 0 0 0]]


.. image:: _images/004-3.png
   :alt: Grid visualization
   :align: center

**output**


.. code-block::

    [[0 0 0 0 0 0]
     [0 0 0 0 0 0]
     [0 0 0 0 0 0]
     [4 0 0 0 0 0]
     [4 0 7 8 0 0]
     [4 0 7 8 0 9]]


.. image:: _images/004-4.png
   :alt: Grid visualization
   :align: center

**observations**

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

**example_3**

**input**


.. code-block::

    [[0 0 0 1 0]
     [0 3 0 0 0]
     [0 3 0 1 2]
     [6 0 0 0 0]
     [0 3 0 0 0]]


.. image:: _images/004-5.png
   :alt: Grid visualization
   :align: center

**output**


.. code-block::

    [[0 0 0 0 0]
     [0 0 0 0 0]
     [0 3 0 0 0]
     [0 3 0 1 0]
     [6 3 0 1 2]]


.. image:: _images/004-6.png
   :alt: Grid visualization
   :align: center

**observations**

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

**examples summary**

- summarize your observations to explain the transformation of the input to output

- use code_execution to investigate properties, patterns and differences in the grids


.. seealso::

   - :doc:`004-prompt`
   - :doc:`004-response`


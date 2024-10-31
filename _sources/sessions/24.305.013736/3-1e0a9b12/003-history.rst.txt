003 • History
=============


.. meta::
   :puzzle_id: 3-1e0a9b12
   :timestamp: 24.305.013736
   :call_count: 3

Begin puzzle: 3-1e0a9b12

**example_1**

**input**


.. code-block::

    [[0 4 0 9]
     [0 0 0 0]
     [0 4 6 0]
     [1 0 0 0]]


.. image:: _images/003-3.png
   :alt: Grid visualization
   :align: center

**output**


.. code-block::

    [[0 0 0 0]
     [0 0 0 0]
     [0 4 0 0]
     [1 4 6 9]]


.. image:: _images/003-4.png
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


.. image:: _images/003-5.png
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


.. image:: _images/003-6.png
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


.. image:: _images/003-7.png
   :alt: Grid visualization
   :align: center

**output**


.. code-block::

    [[0 0 0 0 0]
     [0 0 0 0 0]
     [0 3 0 0 0]
     [0 3 0 1 0]
     [6 3 0 1 2]]


.. image:: _images/003-8.png
   :alt: Grid visualization
   :align: center

**observations**

- review the example grids

- check for differences and patterns


.. seealso::

   - :doc:`003-prompt`
   - :doc:`003-response`


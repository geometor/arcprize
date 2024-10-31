002 • History
=============


.. meta::
   :puzzle_id: 3-1e0a9b12
   :timestamp: 24.305.013736
   :call_count: 2

Begin puzzle: 3-1e0a9b12

**example_1**

**input**


.. code-block::

    [[0 4 0 9]
     [0 0 0 0]
     [0 4 6 0]
     [1 0 0 0]]


.. image:: _images/002-3.png
   :alt: Grid visualization
   :align: center

**output**


.. code-block::

    [[0 0 0 0]
     [0 0 0 0]
     [0 4 0 0]
     [1 4 6 9]]


.. image:: _images/002-4.png
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


.. image:: _images/002-5.png
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


.. image:: _images/002-6.png
   :alt: Grid visualization
   :align: center

**observations**

- review the example grids

- check for differences and patterns


.. seealso::

   - :doc:`002-prompt`
   - :doc:`002-response`


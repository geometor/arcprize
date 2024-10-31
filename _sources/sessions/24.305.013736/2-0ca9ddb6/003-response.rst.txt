003 • Response
==============


.. meta::
   :puzzle_id: 2-0ca9ddb6
   :timestamp: 24.305.013736
   :call_count: 3

```text
input:
  width: 9
  height: 9
  colors:
    - 0: 79
    - 1: 1
    - 2: 1
    - 6: 1
output:
  width: 9
  height: 9
  colors:
    - 0: 73
    - 1: 1
    - 2: 1
    - 4: 4
    - 6: 1
    - 7: 5
differences:
  cells_changed: 9
  colors_changed:
    - introduced: 4, 7
    - removed: None
transformation:
  - a plus sign shape of yellow (4) is drawn above and below each red (2) pixel
  - another plus sign in orange (7) is drawn centered on each blue (1) pixel
  - pixels that are 6 remain the same.
```
The transformation observed in the first and second examples holds true in the third example as well. There is one blue (1) pixel and one red (2) pixel. Plus signs of orange (7) and yellow (4) are drawn around each of them, respectively, in the output. Also, pixels that are 6 remain unchanged.


.. seealso::

   - :doc:`003-history`
   - :doc:`003-prompt`


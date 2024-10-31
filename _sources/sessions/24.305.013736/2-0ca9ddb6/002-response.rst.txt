002 • Response
==============


.. meta::
   :puzzle_id: 2-0ca9ddb6
   :timestamp: 24.305.013736
   :call_count: 2

```text
input:
  width: 9
  height: 9
  colors:
    - 0: 77
    - 1: 2
    - 2: 2
    - 8: 1
output:
  width: 9
  height: 9
  colors:
    - 0: 63
    - 1: 2
    - 2: 2
    - 4: 6
    - 7: 7
    - 8: 1
differences:
  cells_changed: 13
  colors_changed:
    - introduced: 4, 7
    - removed: None
transformation:
  - a plus sign shape of yellow (4) is drawn above and below each red (2) pixel
  - another plus sign in orange (7) is drawn centered on each blue (1) pixel
```
The transformation observed in the first example holds true in the second example as well.  There are two 1s and two 2s in the second example input, and plus signs of 7 and 4 respectively are drawn around each of them in the output. Also, pixels that are 8 remain unchanged.


.. seealso::

   - :doc:`002-history`
   - :doc:`002-prompt`


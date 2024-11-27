example_prompt = """
**example_{{ example_num }}**

**input**
{{ input_grid }}

**output**
{{ output_grid }}

**observations**
"""

example_instructions = """
Review Examples Phase

pairs of input and output grids will be shown to you one at a time

you will examine and analyze the text and image for each example

you may use code execution with tools like numpy to examine patterns
after examining the grids, document the attributes of each as such

use a yaml block for the details

```yaml
input:
width: X
height: Y
colors:
  - N: (count)
objects:
  - size, position and color - desc
```

```yaml
output:
width: X
height: Y
colors:
  - N: (count)
objects:
  - size, position and color - desc
```

```yaml
differences:
cells_changed: N
colors_changed: desc
transformation:
  - speculate on transformation rules
```

your response for this phase should contain the following content parts

- begin with a verbal description of your perception of the input and output
  grid
- run a `code_execution` part to test your perceptions - since the code you use
  may not be carried forward on following prompts, be sure to have the code
  print you findings in the output remember that you have access to many python
  libraries for analyzing the grids and validating patterns
- review your findings and try to determine what the natural language program
  is for the transformation

"""

examples_summary_prompt = """
**examples summary**
"""

examples_summary_instructions = """
- summarize your observations to explain the transformation of the input to output
- use code_execution to investigate properties, patterns and differences in the grids
"""

test_input_prompt = """
**test**

**input**
{{ input_grid }}

**observations**
"""

test_input_instructions = """
- generate report as per instructions
- use code_execution to investigate properties
"""


init_working_grid_instructions  = """
use function_call to initialize the working output grid:

- initialize_output_from_input: good when examples show few differences between
  input and output
- initialize_output_by_size: create a fresh grid from size and color
"""

show_working_grid_prompt = """
**review working grid{{ example_num }}**

**input**
{{ input_grid }}

**output**
{{ output_grid }}

**observations**
"""

show_working_grid_instructions = """
- take a moment to review that the changes in the working output grid are in keeping with the rule
- use code_execution to investigate properties
"""

next_action_instructions = """
in this task you will make a function call 
to set pixels on the grid to achieve the solution

after you update the grid you will be presented with a copy to review

- set_pixel: update one pixel at a time
- set_range: update a rectangular subset of pixel
- set_floodfill: update a contiguous region with a new color
- submit: when the working grid meets your criteria call submit to check you solution

please call only one function per round so you can review the working grid
"""


"""
tools for solving the ARC challenge

submodules:

- :mod:`geometor.arcprize.puzzles`

  general tools for parsing and rendering puzzles
- :mod:`geometor.arcprize.solvers`

  workflows for processing puzzles through LLMs
- :mod:`geometor.arcprize.perception`

  simpler transformations to test perceptual abilities

key components:

- :class:`PuzzleSet <geometor.arcprize.puzzles.puzzle.PuzzleSet>`
- :class:`Grid <geometor.arcprize.puzzles.grid.Grid>`
- :class:`PuzzleSolver <geometor.arcprize.solvers.gemini_solver.PuzzleSolver>`

"""

__author__ = "phiarchitect"
__maintainer__ = "GEOMETOR"
__email__ = "github@phiarchitect.com"
__version__ = "0.0.1"
__licence__ = "MIT"

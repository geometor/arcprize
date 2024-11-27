This project is a collection of studies inspired by the ARC prize

https://arcprize.org

began my journey with ARC think that I it might be fun to build a system 

realized the intention in `On the Measure of Intelligence`_ is for an agent to address the puzzles with
no previous knowledge about the puzzles

if I were to design a system (if I could) then I would be demonstrating my
intelligence

So, the question becomes: can a machine properly ingest a puzzle in a way that
it is understood

.. _On the Measure of Intelligence: https://arxiv.org/pdf/1911.01547

.. |ytimg| image::  https://img.youtube.com/vi/CMr2NoIaZn8/2.jpg
   :target: https://www.youtube.com/watch?v=CMr2NoIaZn8


.. list-table::

   * - |ytimg|
     - https://www.youtube.com/watch?v=CMr2NoIaZn8 - 

       all the grids from the training puzzles in order of complexity

.. topic:: alert

   this is a topic

Overview
--------

The ARC (Abstraction and Reasoning Corpus) challenge presents a fundamental test
of machine intelligence through pattern recognition and reasoning. This project
provides a systematic approach to analyzing and solving ARC puzzles, with a focus
on geometric patterns and transformations.

Key Features
-----------

- **Puzzle Analysis**: Tools for decomposing and understanding ARC puzzle patterns
- **Visual Rendering**: Multiple visualization options for grid states
- **Model Integration**: Framework for testing various AI models on ARC tasks
- **Systematic Logging**: Comprehensive documentation of solution attempts
- **Perception Tests**: Specialized tools for testing basic pattern recognition

Project Structure
---------------

.. code-block:: text

    src/geometor/arcprize/
    ├── __init__.py           # Package initialization
    ├── __main__.py          # CLI entry point
    ├── analyze.py           # Puzzle analysis tools
    ├── app.py              # Main application runner
    ├── img_gen.py          # Image generation utilities
    ├── perception/         # Perception test framework
    ├── puzzles/           # Core puzzle handling
    ├── render/            # Visualization components
    └── solvers/           # Solution implementations

Installation
-----------

.. code-block:: bash

    pip install geometor.arcprize

Usage
-----

Basic Example
~~~~~~~~~~~~

.. code-block:: python

    from geometor.arcprize import PuzzleSet
    from geometor.arcprize.solvers import PuzzleSolver

    # Load puzzle set
    puzzle_set = PuzzleSet()

    # Create solver instance
    solver = PuzzleSolver(puzzle_set.puzzles[0])

    # Run solution attempt
    solver.solve()

Running Perception Tests
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from geometor.arcprize.perception import generate_puzzle_set
    from geometor.arcprize.perception.experiment_runner import test_individual_puzzles

    # Generate test puzzles
    puzzles = generate_puzzle_set(
        num_puzzles=10,
        min_size=3,
        max_size=5,
        symbol_set_key="digits"
    )

    # Run tests
    results = test_individual_puzzles(puzzles, model="phi-3")

Components
---------

Puzzle Module
~~~~~~~~~~~~
- ``Grid``: Represents individual puzzle grids with transformation capabilities
- ``PuzzlePair``: Manages input/output grid pairs
- ``Puzzle``: Encapsulates complete ARC puzzles
- ``PuzzleSet``: Handles collections of puzzles

Perception Module
~~~~~~~~~~~~~~~
- Tools for testing basic pattern recognition abilities
- Focus on rotation, symmetry, and other fundamental transformations
- Support for multiple symbol sets (digits, letters, geometric shapes)

Solver Module
~~~~~~~~~~~
- Framework for implementing different solution strategies
- Built-in support for various AI models
- Logging and analysis of solution attempts

Render Module
~~~~~~~~~~~
- Multiple visualization formats (PNG, SVG, HTML)
- Interactive grid displays
- Animation capabilities for solution steps

Development
----------

Prerequisites
~~~~~~~~~~~~
- Python 3.8+
- Poetry for dependency management
- Development dependencies: pytest, black, pylint

Setup Development Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    # Clone repository
    git clone https://github.com/geometor/arc.git
    cd arc

    # Install dependencies
    poetry install

    # Run tests
    poetry run pytest

Contributing
-----------

Contributions are welcome! Please read our Contributing Guidelines for details on
the process for submitting pull requests.

Areas for Contribution
~~~~~~~~~~~~~~~~~~~
- New perception test types
- Additional solver strategies
- Visualization improvements
- Documentation enhancements
- Performance optimizations

Project Philosophy
----------------

This project approaches the ARC challenge through the lens of fundamental geometric
principles and pattern recognition. Rather than treating each puzzle as an isolated
problem, we seek to understand the underlying patterns and transformations that
connect them.

Key principles:

- Focus on basic perception before complex reasoning
- Systematic documentation of observations
- Integration of geometric analysis
- Progressive refinement of solution strategies

License
-------

This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments
-------------

- François Chollet for creating the ARC challenge
- The GEOMETOR project community
- All contributors and testers

Contact
-------

:GitHub: `@phiarchitect <https://github.com/phiarchitect>`_
:Project: `GEOMETOR/ARC <https://github.com/geometor/arcprize>`_

.. note::
    This project is part of the GEOMETOR initiative, exploring fundamental
    patterns and relationships in mathematics and nature.

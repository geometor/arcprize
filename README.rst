investigations into the ARC challenge
-------------------------------------

.. image:: ./docsrc/_static/arc-banner.png

.. contents:: 
   :local:

This project is a collection of studies inspired by the Abstraction and
Reasoning Corpus (ARC) - a set of puzzles designed to be easy for humans
to solve - but difficult for AI. 

The ARC (Abstraction and Reasoning Corpus) challenge presents a fundamental test
of machine intelligence through pattern recognition and reasoning. This project
provides a systematic approach to analyzing and solving ARC puzzles, with a focus
on geometric patterns and transformations.


For more information on ARC and the current contest, check out https://arcprize.org

began my journey with ARC think that I it might be fun to build a system 

realized the intention in `On the Measure of Intelligence`_ is for an agent to address the puzzles with
no previous knowledge about the puzzles

if I were to design a system (if I could) then I would be demonstrating my
intelligence

So, the question becomes: can a machine properly ingest a puzzle in a way that
it is understood

.. _On the Measure of Intelligence: https://arxiv.org/pdf/1911.01547



mission
-------

We are guided by several important questions


- **Can an LLM solve an ARC puzzle?**

  We know the answer is yes, but can it solve any puzzle.

- **Can an LLM perceive the elements of the puzzle?**



- **Can an LLM discern the "story" of the puzzle?**


mission
-------

- build a system to facilitate the participation by an LLM 
- Focus on extracting a natural language program for 

priors
------

to successsfully tell the story, an intelligent system would need to be able to
perceive and discern the following:


    - Objectness

      Objects persist and cannot appear or disappear without reason. Objects can interact or not depending on the circumstances.

    - Goal-directedness

      Objects can be animate or inanimate. Some objects are "agents" - they have intentions and they pursue goals.

    - Numbers & counting

      Objects can be counted or sorted by their shape, appearance, or movement using basic mathematics like addition, subtraction, and comparison.

    - Basic geometry & topology

      Objects can be shapes like rectangles, triangles, and circles which can be
      mirrored, rotated, translated, deformed, combined, repeated, etc.
      Differences in distances can be detected.

    -- from https://arcprize.org/arc

code
----

- **puzzles**: 
  
  tools for reading source json for ARC puzzle and facilitating presentation

  also tools for sorting puzzle list by complexity

- **solvers**: 
  
  currently code for facilitating puzzle solutions with the Gemini API

  logging and client management

- **perception**





installation
-----------




.. code-block:: bash

    pip install -e .

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

.. |ytimg| image::  https://img.youtube.com/vi/CMr2NoIaZn8/2.jpg
   :target: https://www.youtube.com/watch?v=CMr2NoIaZn8


.. list-table::

   * - |ytimg|
     - https://www.youtube.com/watch?v=CMr2NoIaZn8 - 

       all the grids from the training puzzles in order of complexity

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

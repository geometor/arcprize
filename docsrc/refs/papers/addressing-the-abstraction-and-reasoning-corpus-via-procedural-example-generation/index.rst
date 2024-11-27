.. _addressing-the-abstraction-and-reasoning-corpus-via-procedural-example-generation:

Addressing the Abstraction and Reasoning Corpus via Procedural Example Generation
=================================================================================

:id: 2404.07353
:Authors: Michael Hodel
:Published: 2024-04-10
:arXiv: https://arxiv.org/abs/2404.07353
:PDF: https://arxiv.org/pdf/2404.07353
:DOI: N/A
:Journal Reference: N/A
:Primary Category: cs.LG
:Categories: cs.LG, cs.AI
:Comment: N/A

:github_url: _

abstract
--------
This work presents code to procedurally generate examples for the ARC
training tasks. For each of the 400 tasks, an example generator following the
transformation logic of the original examples was created. In effect, the
assumed underlying distribution of examples for any given task was reverse
engineered by implementing a means to sample from it. An attempt was made to
cover an as large as reasonable space of possible examples for each task. That
is, whenever the original examples of a given task may be limited in their
diversity e.g. by having the dimensions of the grids, the set of symbols or
number of objects constant or within tight bounds, even though the
transformation does not require it, such constraints were lifted. Having access
to not just a few examples per task, as the case for ARC, but instead very
many, should enable a wide range of experiments that may be important stepping
stones towards making leaps on the benchmark.

.. include:: premise.rst

.. include:: outline.rst

.. include:: quotes.rst

.. include:: notes.rst

.. include:: summary.rst

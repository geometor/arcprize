.. _dreamcoder-growing-generalizable-interpretable-knowledge-with-wake-sleep-bayesian-program-learning:

DreamCoder: Growing generalizable, interpretable knowledge with wake-sleep Bayesian program learning
====================================================================================================

:id: 2006.08381
:Authors: Kevin Ellis, Catherine Wong, Maxwell Nye, Mathias Sable-Meyer, Luc Cary, Lucas Morales, Luke Hewitt, Armando Solar-Lezama, Joshua B. Tenenbaum
:Published: 2020-06-15
:arXiv: https://arxiv.org/abs/2006.08381
:PDF: https://arxiv.org/pdf/2006.08381
:DOI: N/A
:Journal Reference: N/A
:Primary Category: cs.AI
:Categories: cs.AI, cs.LG
:Comment: N/A

:github_url: _

abstract
--------
Expert problem-solving is driven by powerful languages for thinking about
problems and their solutions. Acquiring expertise means learning these
languages -- systems of concepts, alongside the skills to use them. We present
DreamCoder, a system that learns to solve problems by writing programs. It
builds expertise by creating programming languages for expressing domain
concepts, together with neural networks to guide the search for programs within
these languages. A ``wake-sleep'' learning algorithm alternately extends the
language with new symbolic abstractions and trains the neural network on
imagined and replayed problems. DreamCoder solves both classic inductive
programming tasks and creative tasks such as drawing pictures and building
scenes. It rediscovers the basics of modern functional programming, vector
algebra and classical physics, including Newton's and Coulomb's laws. Concepts
are built compositionally from those learned earlier, yielding multi-layered
symbolic representations that are interpretable and transferrable to new tasks,
while still growing scalably and flexibly with experience.

.. include:: premise.rst

.. include:: outline.rst

.. include:: quotes.rst

.. include:: notes.rst

.. include:: summary.rst

.. _searching-latent-program-spaces:

Searching Latent Program Spaces
===============================

:id: 2411.08706
:Authors: Clément Bonnet, Matthew V Macfarlane
:Published: 2024-11-13
:arXiv: https://arxiv.org/abs/2411.08706
:PDF: https://arxiv.org/pdf/2411.08706
:DOI: N/A
:Journal Reference: N/A
:Primary Category: cs.LG
:Categories: cs.LG, cs.AI
:Comment: Code available at https://github.com/clement-bonnet/lpn

:github_url: _

abstract
--------
Program synthesis methods aim to automatically generate programs restricted
to a language that can explain a given specification of input-output pairs.
While purely symbolic approaches suffer from a combinatorial search space,
recent methods leverage neural networks to learn distributions over program
structures to narrow this search space significantly, enabling more efficient
search. However, for challenging problems, it remains difficult to train models
to perform program synthesis in one shot, making test-time search essential.
Most neural methods lack structured search mechanisms during inference, relying
instead on stochastic sampling or gradient updates, which can be inefficient.
In this work, we propose the Latent Program Network (LPN), a general algorithm
for program induction that learns a distribution over latent programs in a
continuous space, enabling efficient search and test-time adaptation. We
explore how to train these networks to optimize for test-time computation and
demonstrate the use of gradient-based search both during training and at test
time. We evaluate LPN on ARC-AGI, a program synthesis benchmark that evaluates
performance by generalizing programs to new inputs rather than explaining the
underlying specification. We show that LPN can generalize beyond its training
distribution and adapt to unseen tasks by utilizing test-time computation,
outperforming algorithms without test-time adaptation mechanisms.

.. include:: premise.rst

.. include:: outline.rst

.. include:: quotes.rst

.. include:: notes.rst

.. include:: summary.rst

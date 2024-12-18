.. _a-divide-align-conquer-strategy-for-program-synthesis:

A Divide-Align-Conquer Strategy for Program Synthesis
=====================================================

:id: 2301.03094
:Authors: Jonas Witt, Stef Rasing, Sebastijan Dumančić, Tias Guns, Claus-Christian Carbon
:Published: 2023-01-08
:arXiv: https://arxiv.org/abs/2301.03094
:PDF: https://arxiv.org/pdf/2301.03094
:DOI: N/A
:Journal Reference: N/A
:Primary Category: cs.AI
:Categories: cs.AI
:Comment: 11 pages, 9 figures

:github_url: _

abstract
--------
A major bottleneck in search-based program synthesis is the exponentially
growing search space which makes learning large programs intractable. Humans
mitigate this problem by leveraging the compositional nature of the real world:
In structured domains, a logical specification can often be decomposed into
smaller, complementary solution programs. We show that compositional
segmentation can be applied in the programming by examples setting to divide
the search for large programs across multiple smaller program synthesis
problems. For each example, we search for a decomposition into smaller units
which maximizes the reconstruction accuracy in the output under a latent task
program. A structural alignment of the constituent parts in the input and
output leads to pairwise correspondences used to guide the program synthesis
search. In order to align the input/output structures, we make use of the
Structure-Mapping Theory (SMT), a formal model of human analogical reasoning
which originated in the cognitive sciences. We show that decomposition-driven
program synthesis with structural alignment outperforms Inductive Logic
Programming (ILP) baselines on string transformation tasks even with minimal
knowledge priors. Unlike existing methods, the predictive accuracy of our agent
monotonically increases for additional examples and achieves an average time
complexity of $\mathcal{O}(m)$ in the number $m$ of partial programs for highly
structured domains such as strings. We extend this method to the complex
setting of visual reasoning in the Abstraction and Reasoning Corpus (ARC) for
which ILP methods were previously infeasible.

.. include:: premise.rst

.. include:: outline.rst

.. include:: quotes.rst

.. include:: notes.rst

.. include:: summary.rst

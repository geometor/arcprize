.. _planning-transformer-long-horizon-offline-reinforcement-learning-with-planning-tokens:

Planning Transformer: Long-Horizon Offline Reinforcement Learning with Planning Tokens
======================================================================================

:id: 2409.09513
:Authors: Joseph Clinton, Robert Lieck
:Published: 2024-09-14
:arXiv: https://arxiv.org/abs/2409.09513
:PDF: https://arxiv.org/pdf/2409.09513
:DOI: N/A
:Journal Reference: N/A
:Primary Category: cs.LG
:Categories: cs.LG, cs.AI, cs.CL
:Comment: 11 pages, 5 figures, Submitted to AAAI

:github_url: _

abstract
--------
Supervised learning approaches to offline reinforcement learning,
particularly those utilizing the Decision Transformer, have shown effectiveness
in continuous environments and for sparse rewards. However, they often struggle
with long-horizon tasks due to the high compounding error of auto-regressive
models. To overcome this limitation, we go beyond next-token prediction and
introduce Planning Tokens, which contain high-level, long time-scale
information about the agent's future. Predicting dual time-scale tokens at
regular intervals enables our model to use these long-horizon Planning Tokens
as a form of implicit planning to guide its low-level policy and reduce
compounding error. This architectural modification significantly enhances
performance on long-horizon tasks, establishing a new state-of-the-art in
complex D4RL environments. Additionally, we demonstrate that Planning Tokens
improve the interpretability of the model's policy through the interpretable
plan visualisations and attention map.

.. include:: premise.rst

.. include:: outline.rst

.. include:: quotes.rst

.. include:: notes.rst

.. include:: summary.rst

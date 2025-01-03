.. _learning-to-learn-at-test-time-rnns-with-expressive-hidden-states:

Learning to (Learn at Test Time): RNNs with Expressive Hidden States
====================================================================

:id: 2407.04620
:Authors: Yu Sun, Xinhao Li, Karan Dalal, Jiarui Xu, Arjun Vikram, Genghan Zhang, Yann Dubois, Xinlei Chen, Xiaolong Wang, Sanmi Koyejo, Tatsunori Hashimoto, Carlos Guestrin
:Published: 2024-07-05
:arXiv: https://arxiv.org/abs/2407.04620
:PDF: https://arxiv.org/pdf/2407.04620
:DOI: N/A
:Journal Reference: N/A
:Primary Category: cs.LG
:Categories: cs.LG, cs.AI, cs.CL
:Comment: N/A

:github_url: _

abstract
--------
Self-attention performs well in long context but has quadratic complexity.
Existing RNN layers have linear complexity, but their performance in long
context is limited by the expressive power of their hidden state. We propose a
new class of sequence modeling layers with linear complexity and an expressive
hidden state. The key idea is to make the hidden state a machine learning model
itself, and the update rule a step of self-supervised learning. Since the
hidden state is updated by training even on test sequences, our layers are
called Test-Time Training (TTT) layers. We consider two instantiations:
TTT-Linear and TTT-MLP, whose hidden state is a linear model and a two-layer
MLP respectively. We evaluate our instantiations at the scale of 125M to 1.3B
parameters, comparing with a strong Transformer and Mamba, a modern RNN. Both
TTT-Linear and TTT-MLP match or exceed the baselines. Similar to Transformer,
they can keep reducing perplexity by conditioning on more tokens, while Mamba
cannot after 16k context. With preliminary systems optimization, TTT-Linear is
already faster than Transformer at 8k context and matches Mamba in wall-clock
time. TTT-MLP still faces challenges in memory I/O, but shows larger potential
in long context, pointing to a promising direction for future research.

.. include:: premise.rst

.. include:: outline.rst

.. include:: quotes.rst

.. include:: notes.rst

.. include:: summary.rst

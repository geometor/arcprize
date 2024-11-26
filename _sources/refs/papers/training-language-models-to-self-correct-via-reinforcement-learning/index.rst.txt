.. _training-language-models-to-self-correct-via-reinforcement-learning:

Training Language Models to Self-Correct via Reinforcement Learning
===================================================================

:id: 2409.12917
:Authors: Aviral Kumar, Vincent Zhuang, Rishabh Agarwal, Yi Su, John D Co-Reyes, Avi Singh, Kate Baumli, Shariq Iqbal, Colton Bishop, Rebecca Roelofs, Lei M Zhang, Kay McKinney, Disha Shrivastava, Cosmin Paduraru, George Tucker, Doina Precup, Feryal Behbahani, Aleksandra Faust
:Published: 2024-09-19
:arXiv: https://arxiv.org/abs/2409.12917
:PDF: https://arxiv.org/pdf/2409.12917
:DOI: N/A
:Journal Reference: N/A
:Primary Category: cs.LG
:Categories: cs.LG
:Comment: N/A

:github_url: _

abstract
--------
Self-correction is a highly desirable capability of large language models
(LLMs), yet it has consistently been found to be largely ineffective in modern
LLMs. Current methods for training self-correction typically depend on either
multiple models, a more advanced model, or additional forms of supervision. To
address these shortcomings, we develop a multi-turn online reinforcement
learning (RL) approach, SCoRe, that significantly improves an LLM's
self-correction ability using entirely self-generated data. To build SCoRe, we
first show that variants of supervised fine-tuning (SFT) on offline
model-generated correction traces are often insufficient for instilling
self-correction behavior. In particular, we observe that training via SFT falls
prey to either a distribution mismatch between mistakes made by the
data-collection policy and the model's own responses, or to behavior collapse,
where learning implicitly prefers only a certain mode of correction behavior
that is often not effective at self-correction on test problems. SCoRe
addresses these challenges by training under the model's own distribution of
self-generated correction traces and using appropriate regularization to steer
the learning process into learning a self-correction behavior that is effective
at test time as opposed to fitting high-reward responses for a given prompt.
This regularization process includes an initial phase of multi-turn RL on a
base model to generate a policy initialization that is less susceptible to
collapse, followed by using a reward bonus to amplify self-correction. With
Gemini 1.0 Pro and 1.5 Flash models, we find that SCoRe achieves
state-of-the-art self-correction performance, improving the base models'
self-correction by 15.6% and 9.1% respectively on MATH and HumanEval.

.. include:: premise.rst

.. include:: outline.rst

.. include:: quotes.rst

.. include:: notes.rst

.. include:: summary.rst

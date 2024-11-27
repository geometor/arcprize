.. _procedural-knowledge-in-pretraining-drives-reasoning-in-large-language-models:

Procedural Knowledge in Pretraining Drives Reasoning in Large Language Models
=============================================================================

:id: 2411.12580
:Authors: Laura Ruis, Maximilian Mozes, Juhan Bae, Siddhartha Rao Kamalakara, Dwarak Talupuru, Acyr Locatelli, Robert Kirk, Tim Rocktäschel, Edward Grefenstette, Max Bartolo
:Published: 2024-11-19
:arXiv: https://arxiv.org/abs/2411.12580
:PDF: https://arxiv.org/pdf/2411.12580
:DOI: N/A
:Journal Reference: N/A
:Primary Category: cs.CL
:Categories: cs.CL, cs.LG
:Comment: N/A

:github_url: _

abstract
--------
The capabilities and limitations of Large Language Models have been sketched
out in great detail in recent years, providing an intriguing yet conflicting
picture. On the one hand, LLMs demonstrate a general ability to solve problems.
On the other hand, they show surprising reasoning gaps when compared to humans,
casting doubt on the robustness of their generalisation strategies. The sheer
volume of data used in the design of LLMs has precluded us from applying the
method traditionally used to measure generalisation: train-test set separation.
To overcome this, we study what kind of generalisation strategies LLMs employ
when performing reasoning tasks by investigating the pretraining data they rely
on. For two models of different sizes (7B and 35B) and 2.5B of their
pretraining tokens, we identify what documents influence the model outputs for
three simple mathematical reasoning tasks and contrast this to the data that
are influential for answering factual questions. We find that, while the models
rely on mostly distinct sets of data for each factual question, a document
often has a similar influence across different reasoning questions within the
same task, indicating the presence of procedural knowledge. We further find
that the answers to factual questions often show up in the most influential
data. However, for reasoning questions the answers usually do not show up as
highly influential, nor do the answers to the intermediate reasoning steps.
When we characterise the top ranked documents for the reasoning questions
qualitatively, we confirm that the influential documents often contain
procedural knowledge, like demonstrating how to obtain a solution using
formulae or code. Our findings indicate that the approach to reasoning the
models use is unlike retrieval, and more like a generalisable strategy that
synthesises procedural knowledge from documents doing a similar form of
reasoning.

.. include:: premise.rst

.. include:: outline.rst

.. include:: quotes.rst

.. include:: notes.rst

.. include:: summary.rst

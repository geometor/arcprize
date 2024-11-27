.. _alice-in-wonderland-simple-tasks-showing-complete-reasoning-breakdown-in-state-of-the-art-large-language-models:

Alice in Wonderland: Simple Tasks Showing Complete Reasoning Breakdown in State-Of-the-Art Large Language Models
================================================================================================================

:id: 2406.02061
:Authors: Marianna Nezhurina, Lucia Cipolina-Kun, Mehdi Cherti, Jenia Jitsev
:Published: 2024-06-04
:arXiv: https://arxiv.org/abs/2406.02061
:PDF: https://arxiv.org/pdf/2406.02061
:DOI: N/A
:Journal Reference: N/A
:Primary Category: cs.LG
:Categories: cs.LG, cs.AI, cs.CL
:Comment: v2.01. Minor edits. Further experiments on various AIW problem
  variations. AIW "Alice Female Power Boost", AIW Extension (AIW Ext).
  Including recent Claude 3.5 Sonnet and Qwen 2 72B Instruct results

:github_url: _

abstract
--------
Large Language Models (LLMs) are often described as being instances of
foundation models - that is, models that transfer strongly across various tasks
and conditions in few-show or zero-shot manner, while exhibiting scaling laws
that predict function improvement when increasing the pre-training scale. These
claims of excelling in different functions and tasks rely on measurements taken
across various sets of standardized benchmarks showing high scores for such
models. We demonstrate here a dramatic breakdown of function and reasoning
capabilities of state-of-the-art models trained at the largest available scales
which claim strong function, using a simple, short, conventional common sense
problem (AIW problem) formulated in concise natural language, easily solvable
by humans. The breakdown is dramatic, as models show strong fluctuations across
even slight problem variations that should not affect problem solving, also
expressing strong overconfidence in the wrong solutions, often backed up by
plausible sounding explanation-like confabulations. Various standard
interventions in an attempt to get the right solution, like various type of
enhanced prompting, or urging the models to reconsider the wrong solutions
again by multi step re-evaluation, fail. We take these initial observations to
the scientific and technological community to stimulate urgent re-assessment of
the claimed capabilities of current generation of LLMs. Such re-assessment also
requires common action to create standardized benchmarks that would allow
proper detection of such basic reasoning deficits that obviously manage to
remain undiscovered by current state-of-the-art evaluation procedures and
benchmarks. Code for reproducing experiments in the paper and raw experiments
data can be found at https://github.com/LAION-AI/AIW

.. include:: premise.rst

.. include:: outline.rst

.. include:: quotes.rst

.. include:: notes.rst

.. include:: summary.rst

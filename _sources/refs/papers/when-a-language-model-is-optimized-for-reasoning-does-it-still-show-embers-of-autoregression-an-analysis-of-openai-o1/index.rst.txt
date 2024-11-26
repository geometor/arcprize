.. _when-a-language-model-is-optimized-for-reasoning-does-it-still-show-embers-of-autoregression-an-analysis-of-openai-o1:

When a language model is optimized for reasoning, does it still show embers of autoregression? An analysis of OpenAI o1
=======================================================================================================================

:id: 2410.01792
:Authors: R. Thomas McCoy, Shunyu Yao, Dan Friedman, Mathew D. Hardy, Thomas L. Griffiths
:Published: 2024-10-02
:arXiv: https://arxiv.org/abs/2410.01792
:PDF: https://arxiv.org/pdf/2410.01792
:DOI: N/A
:Journal Reference: N/A
:Primary Category: cs.CL
:Categories: cs.CL, cs.AI
:Comment: 6 pages; updated to fix typo in Fig 4 caption

:github_url: _

abstract
--------
In "Embers of Autoregression" (McCoy et al., 2023), we showed that several
large language models (LLMs) have some important limitations that are
attributable to their origins in next-word prediction. Here we investigate
whether these issues persist with o1, a new system from OpenAI that differs
from previous LLMs in that it is optimized for reasoning. We find that o1
substantially outperforms previous LLMs in many cases, with particularly large
improvements on rare variants of common tasks (e.g., forming acronyms from the
second letter of each word in a list, rather than the first letter). Despite
these quantitative improvements, however, o1 still displays the same
qualitative trends that we observed in previous systems. Specifically, o1 --
like previous LLMs -- is sensitive to the probability of examples and tasks,
performing better and requiring fewer "thinking tokens" in high-probability
settings than in low-probability ones. These results show that optimizing a
language model for reasoning can mitigate but might not fully overcome the
language model's probability sensitivity.

.. include:: premise.rst

.. include:: outline.rst

.. include:: quotes.rst

.. include:: notes.rst

.. include:: summary.rst

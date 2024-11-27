.. _florence-2-advancing-a-unified-representation-for-a-variety-of-vision-tasks:

Florence-2: Advancing a Unified Representation for a Variety of Vision Tasks
============================================================================

:id: 2311.06242
:Authors: Bin Xiao, Haiping Wu, Weijian Xu, Xiyang Dai, Houdong Hu, Yumao Lu, Michael Zeng, Ce Liu, Lu Yuan
:Published: 2023-11-10
:arXiv: https://arxiv.org/abs/2311.06242
:PDF: https://arxiv.org/pdf/2311.06242
:DOI: N/A
:Journal Reference: N/A
:Primary Category: cs.CV
:Categories: cs.CV
:Comment: N/A

:github_url: _

abstract
--------
We introduce Florence-2, a novel vision foundation model with a unified,
prompt-based representation for a variety of computer vision and
vision-language tasks. While existing large vision models excel in transfer
learning, they struggle to perform a diversity of tasks with simple
instructions, a capability that implies handling the complexity of various
spatial hierarchy and semantic granularity. Florence-2 was designed to take
text-prompt as task instructions and generate desirable results in text forms,
whether it be captioning, object detection, grounding or segmentation. This
multi-task learning setup demands large-scale, high-quality annotated data. To
this end, we co-developed FLD-5B that consists of 5.4 billion comprehensive
visual annotations on 126 million images, using an iterative strategy of
automated image annotation and model refinement. We adopted a
sequence-to-sequence structure to train Florence-2 to perform versatile and
comprehensive vision tasks. Extensive evaluations on numerous tasks
demonstrated Florence-2 to be a strong vision foundation model contender with
unprecedented zero-shot and fine-tuning capabilities.

.. include:: premise.rst

.. include:: outline.rst

.. include:: quotes.rst

.. include:: notes.rst

.. include:: summary.rst

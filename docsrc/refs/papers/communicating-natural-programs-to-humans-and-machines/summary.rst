.. meta::
   :source_pdf: 2106.07824v4.Communicating_Natural_Programs_to_Humans_and_Machines.pdf
   :summary_date: 2024-11-25 20:40:06

summary
-------

1. Brief Overview
=================

This paper introduces LARC (Language-complete Abstraction and Reasoning Corpus), a dataset augmenting the existing ARC (Abstraction and Reasoning Corpus) dataset with natural language instructions for solving procedural tasks.  While ARC tasks are easy for humans, they pose significant challenges for state-of-the-art AI.  The authors propose that studying how humans communicate procedural knowledge through natural language can provide valuable insights for building more robust AI systems. They analyze these instructions as "natural programs," highlighting their differences from traditional computer programs in terms of primitives and communicative strategies.  They then evaluate the effectiveness of current program synthesis techniques on LARC, demonstrating the challenges presented by the complexity of natural language instructions and suggesting directions for future research in program synthesis.

2. Key Points
=================

* LARC augments 88% of ARC tasks with natural language instructions created through a human communication game.
* Human-generated instructions ("natural programs") in LARC differ from computer programs in their use of a wider range of primitives and communicative strategies beyond directly executable code.
* Current program synthesis techniques struggle to fully leverage LARC due to the complexity of natural programs.
* LARC can be used to study how humans communicate and interpret procedures, and to inform the design of future program synthesizers.
* A novel bandit algorithm was developed to efficiently collect the LARC dataset.
* Experiments demonstrate that while language improves program synthesis, current methods significantly underperform compared to human capabilities.


3. Notable Quotes
==================

No notable quotes were identified.


4. Primary Themes
===================

* **Human-Computer Communication:** The central theme explores the differences between how humans and machines communicate procedural instructions.
* **Program Synthesis:** The paper investigates the limitations of existing program synthesis techniques and proposes new directions based on insights from LARC.
* **Cognitive Modeling:**  LARC serves as a window into human cognitive processes involved in solving procedural tasks and communicating instructions.
* **Benchmarking AI:** LARC provides a challenging benchmark to evaluate the generalization capabilities of AI systems.



.. meta::
   :source_pdf: 2411.12580v1.Procedural_Knowledge_in_Pretraining_Drives_Reasoning_in_Large_Language_Models.pdf
   :summary_date: 2024-11-25 20:42:59

summary
-------

1. Brief overview
~~~~~~~~~~~~~~~~~

This paper investigates how large language models (LLMs) generalize when performing reasoning tasks.  The authors overcome the limitations of traditional train-test set separation by analyzing the pretraining data that influences model outputs for various reasoning and factual questions. They focus on three simple mathematical reasoning tasks and contrast them with factual questions, using influence functions to identify influential documents.  The research is conducted on two Cohere Command R models (7B and 35B parameters) and a subset of their pretraining data.


2. Key points
~~~~~~~~~~~~~

*   **Procedural knowledge drives reasoning:** Documents influencing reasoning traces often contain procedural knowledge (e.g., formulas or code demonstrating solution methods).  This suggests LLMs are generalizing strategies rather than simply retrieving answers.
*   **Models rely less on individual documents for reasoning:** The influence of individual documents on reasoning is weaker than on factual questions, indicating a reliance on a broader, more general set of documents.
*   **Factual answers are often found in influential data, reasoning answers rarely are:** Answers to factual questions frequently appear in highly influential pretraining documents. This is not the case for reasoning questions, nor for intermediate reasoning steps.
*   **Code plays a significant role in mathematical reasoning:** Code data is overrepresented among influential documents for reasoning tasks. This highlights the importance of high-quality procedural data in model pretraining.
*   **Larger models show stronger effects:**  The 35B parameter model exhibited more pronounced differences in influence between reasoning and factual questions compared to the 7B parameter model.


3. Notable quotes
~~~~~~~~~~~~~~~~~

No direct quotes were extracted as significantly important for future reference. The findings are primarily conveyed through the results and analysis.


4. Primary themes
~~~~~~~~~~~~~~~~~

*   **LLM Generalization:** The core theme is understanding how LLMs generalize to new reasoning tasks, moving beyond simple retrieval-based explanations.
*   **Interpretability:** The study uses influence functions to gain insights into the internal mechanisms of LLMs, exploring what parts of the training data are most influential for specific types of questions.
*   **Pretraining Data Impact:** A crucial theme is the role of pretraining data quality and composition in driving the success of LLMs on reasoning tasks.  The study suggests that focusing on high-quality procedural knowledge rather than comprehensive coverage of all possible cases might be a more effective approach for pretraining.



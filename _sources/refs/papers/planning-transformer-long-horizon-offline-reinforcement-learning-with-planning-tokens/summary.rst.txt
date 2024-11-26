.. meta::
   :source_pdf: 2409.09513v1.Planning_Transformer__Long_Horizon_Offline_Reinforcement_Learning_with_Planning_Tokens.pdf
   :summary_date: 2024-11-25 20:38:22

summary
-------

1. Brief Overview

The paper introduces the Planning Transformer (PT), a novel model for long-horizon offline reinforcement learning.  PT addresses the compounding error problem inherent in autoregressive models like the Decision Transformer (DT) by incorporating "Planning Tokens." These tokens provide high-level, long-timescale information about the agent's future, guiding the low-level policy and reducing error. This approach achieves state-of-the-art performance in complex D4RL environments and improves model interpretability through plan visualizations and attention maps.

2. Key Points

*   Introduces Planning Tokens to address compounding error in long-horizon offline reinforcement learning.
*   Combines strengths of Reinforcement Learning via Supervised Learning (RvS) and Hierarchical Reinforcement Learning (HRL) without HRL's drawbacks.
*   Achieves state-of-the-art (SOTA) performance on several D4RL benchmark tasks, particularly in long-horizon goal-conditioned environments.
*   Enhances interpretability through visualization of Plans and attention maps, offering insights into the model's decision-making process.
*   Employs a unified training pipeline for action and plan prediction, simplifying the model architecture.

3. Notable Quotes

None explicitly stated in the provided text.


4. Primary Themes

*   **Addressing Compounding Error in Offline RL:** The core theme is tackling the limitations of autoregressive models in long-horizon tasks by introducing a mechanism (Planning Tokens) for implicit planning.
*   **Improving Interpretability in RL:**  The paper highlights the increased interpretability offered by the visualization of generated plans and attention maps, which is a significant contribution to the field.
*   **Efficient Offline RL:** The model aims for efficient learning from fixed datasets, which is a crucial aspect of offline RL.
*   **Hybrid Approach to HRL:** The method leverages the benefits of both RvS and HRL approaches without the typical complexities and limitations of explicit HRL architectures.


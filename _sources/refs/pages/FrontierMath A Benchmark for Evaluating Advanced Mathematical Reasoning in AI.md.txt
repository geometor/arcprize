---
title: FrontierMath: A Benchmark for Evaluating Advanced Mathematical Reasoning in AI
pageTitle: FrontierMath: Evaluating Advanced Mathematical Reasoning in AI | Epoch AI | Epoch AI
created: 24.325.171206
tags: []
source: https://epoch.ai/frontiermath/the-benchmark
author: Tamay Besiroglu
---

# FrontierMath: Evaluating Advanced Mathematical Reasoning in AI | Epoch AI | Epoch AI
source: [](https://epoch.ai/frontiermath/the-benchmark)

> FrontierMath: a new benchmark of expert-level math problems designed to measure AI’s mathematical abilities. See how leading AI models perform against the collective mathematics community.


### Authors

We’re introducing FrontierMath, a benchmark of hundreds of original, expert-crafted mathematics problems designed to evaluate advanced reasoning capabilities in AI systems. These problems span major branches of modern mathematics—from computational number theory to abstract algebraic geometry—and typically require hours or days for expert mathematicians to solve.

Figure 1. While leading AI models now achieve near-perfect scores on traditional benchmarks like GSM-8k and MATH, they solve less than 2% of FrontierMath problems, revealing a substantial gap between current AI capabilities and the collective prowess of the mathematics community. MMLU scores shown are for the College Mathematics category of the benchmark.

To understand and measure progress in artificial intelligence, we need carefully designed benchmarks that can assess how well AI systems engage in complex scientific reasoning. Mathematics offers a unique opportunity for this assessment—it requires extended chains of precise reasoning, with each step building exactly on what came before. And, unlike many domains where evaluation requires subjective judgment or expensive tests, mathematical problems can be rigorously and automatically verified.

## The FrontierMath Benchmark

FrontierMath is a benchmark of hundreds of original mathematics problems spanning the breadth of modern mathematical research. These range from computationally intensive problems in number theory and real analysis to abstract questions in algebraic geometry and category theory. We developed it through collaboration with over 60 mathematicians from leading institutions, including professors, IMO question writers, and Fields medalists.

FrontierMath problems typically demand hours or even days for specialist mathematicians to solve. The following Fields Medalists shared their impressions after reviewing some of the research-level problems in the benchmark:

> “These are extremely challenging. I think that in the near term basically the only way to solve them, short of having a real domain expert in the area, is by a combination of a semi-expert like a graduate student in a related field, maybe paired with some combination of a modern AI and lots of other algebra packages…” —Terence Tao, Fields Medal (2006)

> “\[The questions I looked at\] were all not really in my area and all looked like things I had no idea how to solve…they appear to be at a different level of difficulty from IMO problems.” — Timothy Gowers, Fields Medal (2006)

FrontierMath features hundreds of advanced mathematics problems that require hours for expert mathematicians to solve. We release representative samples, which you may download [here](https://epoch.ai/files/sample_question_transcripts.zip).

_Definitions._ For a positive integer

, let

denote the largest integer

such that

. For a prime

and

, let

denote the smallest positive integer

such that

. For

, let

_Problem._ Let

denote the set of primes

for which

and let

denote the density

of

in the primes. Let

Compute

**Answer**: 367707

**MSC classification**: 11 Number theory

Construct a degree 19 polynomial

such that

has at least 3 (but not all linear) irreducible components over

. Choose

to be odd, monic, have real coefficients and linear coefficient -19 and calculate

.

**Answer**: 1876572071974094803391179

**MSC classification**: 14 Algebraic geometry; 20 Group theory and generalizations; 11 Number theory generalizations

Let

for

be the sequence of integers satisfying the recurrence formula

with initial conditions

for

. Find the smallest prime

for which the function

given by

can be extended to a continuous function on

.

**Answer**: 9811

**MSC classification**: 11 Number theory

Each problem is carefully designed to test genuine mathematical understanding. Problems must be novel and unpublished, with answers that can be automatically verified through computation—either as exact integers or mathematical objects like matrices and symbolic expressions in SymPy. A verification script checks submissions through exact matching or by confirming the submitted answer matches the known solution.

They are also designed to be “guessproof”—problems have large numerical answers or complex mathematical objects as solutions, with less than a 1% chance of guessing correctly without the mathematical work. Problems are reviewed specifically for this property, with reviewers checking that shortcuts or pattern matching generally cannot bypass the need for genuine understanding.

Each problem undergoes peer review by expert mathematicians who verify correctness, check for ambiguities, and assess difficulty ratings. Additionally, we conducted second reviews on a random subsample of problems, finding that approximately 1 in 20 problems had errors requiring correction—comparable to error rates in other major machine learning benchmarks [like ImageNet](https://arxiv.org/abs/2103.14749). We recognize the importance of benchmark accuracy and are expanding both our expert review process and error-bounty program to reduce this error rate.

## Current Performance on FrontierMath

To evaluate how well current AI models can tackle advanced mathematical problems, we provided them with extensive support to maximize their performance. Our evaluation framework grants models ample thinking time and the ability to experiment and iterate. Models interact with a Python environment where they can write and execute code to test hypotheses, verify intermediate results, and refine their approaches based on immediate feedback.

Figure 2. Performance of leading language models on FrontierMath. All models show consistently poor performance, with even the best models solving less than 2% of problems.

Despite this support framework, FrontierMath has proven exceptionally challenging for today’s AI systems. We evaluated six leading language models—including Claude 3.5 Sonnet, o1-preview, GPT-4o, and Gemini 1.5 Pro—and found that none could solve more than 2% of the problems. This is in sharp contrast to other popular mathematical benchmarks such as GSM-8K and MATH, where top models now achieve over 90% accuracy.

## Our next steps

FrontierMath represents a significant step toward evaluating whether AI systems possess research-level mathematical reasoning capabilities. While current models solve less than 2% of problems, we expect this benchmark to become increasingly valuable as AI systems advance.

Our next steps include:

-   **Regular evaluations**: Conducting and publishing ongoing assessments of leading AI models to provide a standardized measure of progress, and evaluating how advanced mathematical reasoning abilities improve over time and with scale.
-   **Benchmark expansion**: Adding more problems to FrontierMath while maintaining both our rigorous standards and the current distribution of problem types, difficulty levels, and mathematical domains.
-   **Public problem release**: Building on our initial release of five representative problems with solutions, we plan to release additional problems in the coming months to further engage the community and facilitate benchmarking.
-   **Enhanced quality assurance**: Strengthening our quality control through expanded expert review, increased error-bounties, and improved peer review processes.

## Conclusion

FrontierMath represents a significant step toward evaluating whether AI systems possess research-level mathematical reasoning capabilities. While current models solve less than 2% of problems—revealing a substantial gap between AI capabilities and the collective prowess of the mathematical community—we expect this benchmark to become increasingly valuable as AI systems advance.

We look forward to working with both the mathematics and the AI research community to refine and expand this benchmark. By regularly evaluating state-of-the-art models and collaborating with the AI research community, we aim to deepen our understanding of AI’s capabilities and limitations.

You can read more about FrontierMath in [our technical report](https://arxiv.org/abs/2411.04872). If you want to reach out to us about FrontierMath evaluations, please email us at [math\_evals@epochai.org](mailto:math_evals@epochai.org)

### About the authors

![](FrontierMath%20A%20Benchmark%20for%20Evaluating%20Advanced%20Mathematical%20Reasoning%20in%20AI/tamay-besiroglu.jpg)

Tamay Besiroglu is the associate director at Epoch AI. His work focuses on the economics of computing and big-picture trends in machine learning. Previously, he was a researcher at the Future Tech Lab at MIT, led strategy for Metaculus, consulted for the UK Government, and worked at the Future of Humanity Institute.

![](FrontierMath%20A%20Benchmark%20for%20Evaluating%20Advanced%20Mathematical%20Reasoning%20in%20AI/elliot-glazer.png)

Elliot Glazer holds a Ph.D. in Mathematics from Harvard under Hugh Woodin, with research in set theory and formal systems, especially paradoxes in the axiom of choice. He has recently worked on the foundations of proof assistants, and enjoys developing mathematical puzzles in both finite and infinite settings.

![](FrontierMath%20A%20Benchmark%20for%20Evaluating%20Advanced%20Mathematical%20Reasoning%20in%20AI/caroline-falkman-olsson.png)

Caroline Falkman Olsson is an Operations Associate at Epoch AI, with a background in Economics and Statistics. She has previously worked as a predoctoral researcher at LSE’s International Inequalities Institute (III) and as a data analyst at the Institute for International Economic Studies (IIES) at Stockholm University.

---
title: ARC Prize - What is ARC-AGI?
pageTitle: ARC Prize - What is ARC-AGI?
created: 24.270.192817
tags: []
source: https://arcprize.org/arc
author: 
---

# ARC Prize - What is ARC-AGI?
source: [](https://arcprize.org/arc)

> Learn more about the only AI benchmark that measures AGI progress.


## AGI progress has stalled.  
New ideas are needed.

Presented by ![Infinite Monkey](ARC%20Prize%20-%20What%20is%20ARC-AGI/im-logomark.svg) ![Lab42](ARC%20Prize%20-%20What%20is%20ARC-AGI/lab42-logo.svg)

In 2019, François Chollet - creator of Keras, an open-source deep learning library adopted by over 2.5M developers, and Software Engineer & AI Researcher at Google - published the influential paper "[On the Measure of Intelligence](https://arxiv.org/abs/1911.01547)" where he introduced a benchmark to measure the efficiency of AI skill-acquisition on unknown tasks:

**[Abstraction and Reasoning Corpus (ARC-AGI)](https://github.com/fchollet/ARC-AGI)**

<iframe src="https://www.youtube.com/embed/2W5D6J8om0c?si=3ABC-8-iim6FKKEU" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen=""></iframe>

### AGI Definition

To make deliberate progress towards more intelligent and human-like systems, we need to be following an appropriate feedback signal: We need to define and evaluate intelligence.

These definitions and evaluations turn into benchmarks to measure progress toward systems that can think and invent alongside us.

Consensus definition of AGI, "a system that can automate the majority of economically valuable work," while a useful goal, is an incorrect measure of intelligence.

Measuring task-specific skill is not a good proxy for intelligence.

Skill is heavily influenced by prior knowledge and experience: unlimited priors or unlimited training data allows developers to "buy" levels of skill for a system. This masks a system's own generalization power.

Intelligence lies in broad or general-purpose abilities; it is marked by _skill-acquisition_ and generalization, rather than skill itself.

**AGI is a system that can efficiently acquire _new_ skills outside of its training data.**

More formally:

> The intelligence of a system is a measure of its skill-acquisition efficiency over a scope of tasks, with respect to [priors](https://arcprize.org/arc#priors), experience, and generalization difficulty. - François Chollet, "On the Measure of Intelligence"

This means that a system is able to adapt to a new environment that it has not seen before and that its creators (developers) did not anticipate.

ARC-AGI is the only AI benchmark that measures progress towards general intelligence.

[See François explain intelligence.](https://www.youtube.com/watch?v=PUAdj3w3wO4&t=1591s)

### ARC-AGI Design

ARC-AGI consists of unique training and evaluation tasks. Each task contains input-output examples. The puzzle-like inputs and outputs present a grid where each square can be one of ten colors. A grid can be any height or width between 1x1 and 30x30.

![Example ARC-AGI Task](ARC%20Prize%20-%20What%20is%20ARC-AGI/arc-example-task.jpg)

To successfully solve a task, the test-taker must produce a pixel-perfect correct output grid for the final output. This includes picking the correct dimensions of the output grid.

_For more, see [ARC-AGI's data structure](https://arcprize.org/guide#data-structure)._

### Priors

ARC-AGI is explicitly designed to compare artificial intelligence with human intelligence. To do this, ARC-AGI explicitly lists the priors knowledge human have to provide a fair ground for comparing AI systems. These core knowledge priors are ones that humans naturally possess, even in childhood.

1.  **Objectness**  
    Objects persist and cannot appear or disappear without reason. Objects can interact or not depending on the circumstances.
2.  **Goal-directedness**  
    Objects can be animate or inanimate. Some objects are "agents" - they have intentions and they pursue goals.
3.  **Numbers & counting**  
    Objects can be counted or sorted by their shape, appearance, or movement using basic mathematics like addition, subtraction, and comparison.
4.  **Basic geometry & topology**  
    Objects can be shapes like rectangles, triangles, and circles which can be mirrored, rotated, translated, deformed, combined, repeated, etc. Differences in distances can be detected.

ARC-AGI avoids a reliance on any information that isn’t part of these priors, for example acquired or cultural knowledge, like language.

### Impact

Solving ARC-AGI represents a material stepping stone toward AGI.

At minimum, solving ARC-AGI would result in a new programming paradigm. It would allow anyone, even those without programming knowledge, to create programs simply by providing a few input-output examples of what they want.

This would dramatically expand who is able to leverage software and automation. Programs could automatically refine themselves when exposed to new data, similar to how humans learn.

If found, a solution to ARC-AGI would be more impactful than the discovery of the Transformer. The solution would open up a new branch of technology.

<iframe src="https://www.youtube.com/embed/ZyA_6sX4ATY?si=nsu288A-NvSI5YKc" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen=""></iframe>

### Competition History

**2019** - ARC-AGI was introduced in François Chollets 2019 paper, "On the Measure of Intelligence". At this point, François has the hypothesis that it could not easily be beaten.

**2020** - In order to test this, he hosted the first ARC-AGI competition on Kaggle in 2020. The winning team, "ice cuber," achieved a 21% success rate on the test set. This low score was the first strong evidence that François's ideas in On/Measure were correct.

**2021** - A New York University [study](https://cims.nyu.edu/~brenden/papers/JohnsonEtAl2021CogSci.pdf) (2021) found that most humans can solve, on average, 84% of the tasks in the ARC-AGI public training set.

**2022** - In 2022 François and Lab42 teamed up to host the ARCathon 2022, the first global AI competition to try and beat ARC-AGI. 118 teams from 47 countries participated. Michael Hodel, won the ARCathon and received his trophy at the Swiss Global AI Awards following the honoring of Demis Hassabis by Pascal Kaufmann, founder of Lab42, in Davos. Michael has developed one of the best ARC-AGI domain-specific languages (DSLs) to date.

**2023** - Then in 2023, the competition continued with ARCathon 2023. This time 265+ teams from 65 countries competed. First place was shared between Somayyeh Gholami and Mehran Kazeminia (Team SM) and Jack Cole (Team MindsAI) both reaching 30% on the private evaluation set.

**2024** - In 2024, Mike Knoop, François, and Lab42 teamed up to create ARC Prize 2024 with over a $1.1M prize pool.

#### Next

[Toggle Animation](https://arcprize.org/arc#)

---
title: ARC Prize - Official Guide
pageTitle: ARC Prize - Official Guide
created: 24.271.212715
tags: []
source: https://arcprize.org/guide
author: 
---

# ARC Prize - Official Guide
source: [](https://arcprize.org/guide)

> The official guide to ARC Prize.


## AGI progress has stalled.  
New ideas are needed.

Presented by ![Infinite Monkey](ARC%20Prize%20-%20Official%20Guide/im-logomark.svg) ![Lab42](ARC%20Prize%20-%20Official%20Guide/lab42-logo.svg)

Welcome to the official ARC Prize Guide!

This guide is designed help you get up to speed on ARC-AGI, establish your strategy, form a team (optional), and make progress toward winning prizes and eternal glory.

No matter who you are, where you come from, what you do for a living, you are welcome to join this competition. You can join forces with people who have complimentary skill sets or work alone. It's all up to you.

Let's get started!

#### Contents

### Overview

Before you dive into this guide, make sure to read the [Competition Details](https://arcprize.org/competition) and [ARC-AGI](https://arcprize.org/arc) pages.

The purpose of ARC Prize is to redirect more AI research focus toward architectures that might lead toward artificial general intelligence (AGI) and ensure that notable breakthroughs do not remain a trade secret at a big corporate AI lab.

ARC-AGI is the only AI benchmark that tests for general intelligence by testing not just for skill, but for _skill acquisition_.

**Your ambitious goal:** Submit a solution which scores 85% on the ARC-AGI private evaluation set and win $600K.

You are not alone in this goal. The ARC Prize community and official team are here to provide support and resources.

Plug into the community & get competition updates:

1.  [Subscribe to the newsletter](https://arcprize.ck.page/bc80575d89)
2.  [Join the Discord server](https://discord.gg/9b77dPAmcA)
3.  [Join the discussion on Kaggle](https://www.kaggle.com/competitions/arc-prize-2024)
4.  [Follow on Twitter](https://twitter.com/arcprize)
5.  [Subscribe on YouTube](https://www.youtube.com/channel/UC_rdrp-QkrZn-ce9uCE-0EA)

You can also reach our team at team@arcprize.org or message us on [Discord](https://discord.gg/9b77dPAmcA).

### Data Structure

So you want to solve ARC-AGI? Let's start by exploring how its data is structured.

This material is also covered in the [Explore ARC-AGI Data + Play](https://www.youtube.com/watch?v=LLxiPrIxdqs) tutorial video.

<iframe src="https://www.youtube.com/embed/LLxiPrIxdqs?si=-TVPVnpRjUsJx0BP" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen=""></iframe>

#### Tasks

ARC-AGI tasks are a series of three to five input and output tasks followed by a final task with only the input listed. Each task tests the utilization of a specific learned skill based on a minimal number of cognitive priors.

![ARC-AGI task](ARC%20Prize%20-%20Official%20Guide/arc-task-grids.jpg)

Tasks are represented as JSON lists of integers. These JSON objects can also be represented visually as a grid of colors using an ARC-AGI task viewer.

A successful submission is a pixel-perfect description (color and position) of the final task's output.

#### Task Data

The following datasets are associated with the ARC Prize competition:

1.  Public training set
2.  Public evaluation set
3.  Private evaluation set

_Outside of the competition, there is also a semi-private evaluation set used for the public leaderboard. [Learn more](https://arcprize.org/arc-agi-pub)._

#### Public

The publicly available data is to be used for training and evaluation.

The _public training set_ contains 400 task files you can use to train your algorithm.

The _public evaluation set_ contains 400 task files for to test the performance of your algorithm.

To ensure fair evaluation results, be sure not to leak information from the evaluation set into your algorithm (e.g., by looking at the tasks in the evaluation set yourself during development, or by repeatedly modifying an algorithm while using its evaluation score as feedback.)

The source of truth for this data is available on François Chollet's [ARC-AGI GitHub Repository](https://github.com/fchollet/ARC-AGI), which contains 800 total tasks.

#### Private

The _private evaluation set_ contains 100 task files.

The [ARC-AGI leaderboard](https://arcprize.org/leaderboard) is measured using 100 private evaluation tasks which are privately held on Kaggle. These tasks are private to ensure models may not be trained on them. These tasks are not included in the public tasks, but they do use the same structure and cognitive priors.

Please note that the public training set consists of simpler tasks whereas the public evaluation set is roughly the same level of difficulty as the private test set.

#### Set Difficulty

The public training set is significantly easier than the others (public evaluation and private evaluation set) since it contains many "curriculum" type tasks intended to demonstrate Core Knowledge systems.

For reference, here are scores across the different datasets from two community members participating in ARC Prize 2024.

| Name | Public Training Set | Public Evaluation Set | Private Evaluation |
| --- | --- | --- | --- |
| Zoltan | 53% | 38% | 24% |
| Kha Vo | 32% | 30% | 22% |

Please note that solutions that train on all public data can have a significant gap between public set scores and private evaluation set scores.

A future version of ARC-AGI will formally calibrate difficulty across evaluation sets.

#### Format

As mentioned above, tasks are stored in JSON format. Each JSON file consists of two key-value pairs.

`train`: a list of two to ten input/output pairs (typically three.) These are used for your algorithm to infer a rule.

`test`: a list of one to three input/output pairs (typically one.) Your model should apply the inferred rule from the `train` set and construct an output solution. You will have access to the output test solution on the public data. The output solution on the private evaluation set will not be revealed.

Here is an example of a simple ARC-AGI task that has three training pairs along with a single test pair. Each pair is shown as a 2x2 grid. There are four colors represented by the integers 1, 4, 6, and 8. Which actual color (red/green/blue/black) is applied to each integer is arbitrary and up to you.

```
{
  "train": [
    {"input": [[1, 0], [0, 0]], "output": [[1, 1], [1, 1]]},
    {"input": [[0, 0], [4, 0]], "output": [[4, 4], [4, 4]]},
    {"input": [[0, 0], [6, 0]], "output": [[6, 6], [6, 6]]}
  ],
  "test": [
    {"input": [[0, 0], [0, 8]], "output": [[8, 8], [8, 8]]}
  ]
}
```

### Development

#### Download

Download the ARC-AGI-1 data from the [official ARC-AGI repo](https://github.com/fchollet/ARC-AGI) on GitHub.

Please note that there will be future versions of the ARC-AGI dataset as it matures. We plan to keep improving the benchmark by adding more tasks and more novelty. Future versions will get versioned (ex: ARC-AGI-2) and future ARC Prize competitions may target newer versions.

#### View

There are multiple ways for humans to view the data:

-   Testing interface on the official repo ([instructions](https://github.com/fchollet/ARC-AGI/tree/master?tab=readme-ov-file#usage-of-the-testing-interface))
-   The [arcprize.org task viewer](https://arcprize.org/play)
-   [Community-created apps](https://github.com/neoneye/arc-notes/tree/main/awesome#editors)

#### Test

There are two ways to measure your progress on ARC-AGI tasks.

1.  _Correct / Incorrect:_ This evaluation method measures whether or not your model’s output answer is _identical_ to the validated solution. This means that the output shape, colors, and positions match. This evaluation method is used on the ARC-AGI private evaluation set.
    
2.  _Pixel correctness:_ The number of pixels that are correctly identified as a % of the total. Some teams use “Pixel Correctness” as another indicator for their score. Though this is not used in the competition, it can give more information about how your results are performing.
    

### Approaches

You're free to explore any path you like, but we'd love to save you time by catching you up on the four solution approaches that have led to the current state of the art. Join the [community discord](https://discord.gg/9b77dPAmcA) to find out more from people who have been working on ARC-AGI for years.

#### 1\. Discrete program search

This was the first domain of solutions that started working well in the original ARCathon competition in 2020 hosted by Lab42. It involves searching through a massive program space in a discrete, step-by-step manner.

#### 2\. Ensemble Solutions

This approach consists of piecing together existing publicly available solutions to correctly answer more tasks than any solution achieved alone. This is the approach that was used to get to the current high score.

One thing to consider in utilizing this approach: it's unlikely that an ensemble approach will be able to generalize to correctly solve tasks outside of the public datasets. If you've got your eyes on the Grand Prize, you'll want to create new and novel techniques.

#### 3\. Direct LLM Prompting

In this method, contestants use a traditional LLM (like GPT-4) and rely on prompting techniques to solve ARC-AGI tasks. This was found to perform poorly, scoring <5%. Fine-tuning a state-of-the-art (SOTA) LLM with millions of synthetic ARC-AGI examples scores ~10%.

"LLMs like Gemini or ChatGPT \[don't work\] because they're basically frozen at inference time. They're not actually learning anything." - François Chollet

Additionally, keep in mind that submissions to Kaggle will not have access to the internet. Using a 3rd-party, cloud-hosted LLM is not possible.

See templates for [fine-tuning Llama 3b](https://www.kaggle.com/code/hansuelijud/template-llama-3-8b-arc-prize-2024-finetuning), [open source LLM](https://www.kaggle.com/code/hansuelijud/template-llama-3-8b-arc-prize-2024-inference) (without fine-tuning it), and [using frontier models](https://www.kaggle.com/code/gregkamradt/using-frontier-models-on-arc-agi-via-langchain) ([Video tutorial](https://www.youtube.com/watch?v=crhrzhVjWog), [ARC-AGI-Pub](https://arcprize.org/arc-agi-pub) only).

#### 4\. Domain-Specific Language (DSL) Program Synthesis

This approach involves developing a domain-specific language (DSL). The DSL is designed to encapsulate common concepts such as rotation, mirroring, and other grid transformations that frequently occur in ARC tasks. By defining a set of primitives or basic functions that perform these transformations, solutions can be synthesized by composing these primitives into programs that solve specific tasks.

Program synthesis in this approach involves searching through possible compositions of the DSL primitives to find programs that correctly transform input grids into their corresponding output grids. This search can be brute-force or more sophisticated, but the key idea is to leverage the DSL to build task-specific programs efficiently.

See [Michael Hodel's example notebook](https://www.kaggle.com/code/michaelhodel/program-synthesis-starter-notebook) with this approach.

#### 5\. Active inference

More recently, solutions using pre-trained large language models (LLMs) have been attempted. The LLMs are additionally trained on code data, ARC-AGI data, and because there aren’t enough ARC-AGI tasks, you’ll augment this with synthetic ARC-AGI-like data.

The trick to making this LLM based solution work is using active inference. This is the idea that when you’re presented with a test task demonstration examples, fine tune the LLM on those examples. Of course, because there are only a couple of them, you’ll need to expand them artificially to have enough data points to fit your curve.

This unlocks the performance that we see with top solutions. Jack Cole's 34% solution utilizes this approach.

“The fact that this technique has an outsized impact is really interesting” - François Chollet

<iframe src="https://www.youtube.com/embed/Q96eFrtLB8U?si=-KFK7Zn1JwLhW07v" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen=""></iframe>

### Inspiration From Francois

Let's hear from François, the creator of ARC, about what he sees as the most promising approaches as well as general tips to help you compete in ARC Prize.

<iframe src="https://www.youtube.com/embed/VqMcfdzqedE?si=1BtgJQL0I-k68adh" title="
 video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen=""></iframe>

#### Promising Approaches

François believes that the most promising category of solutions is one that we haven't really seen in practice so far. His thought process…

> Discrete program search works really well. This is probably the easiest way to to solve ARC-AGI tasks. Now we also know that LLMs can develop good intuition about how to solve ARC-AGI tasks. The next step is going to be to augment discrete program search with deep learning driven intuition.

> When you're doing discrete program search, you have to sift through this massive program space. The problem you're facing here, of course, is combinatorial explosion.

> If you manage to get a \[deep learning\] model that has a pretty good sense of what an ARC-AGI task and solution is supposed to look like, then you can use the deep learning model to provide suggestions as to where to try next or what a sketch of your solution program look like.

> This is a category of approaches that a few people have tried. I'm very convinced that this is the domain from which you're gonna see the highest quality solutions.

Here more on this approach from [Francois with Dwarkesh](https://www.youtube.com/watch?v=UakqL6Pj9xo&t=2961s).

#### General Tips

1.  **Focus on skill acquisition and generalization:** The key idea behind ARC-AGI is that each task should be novel and not solvable by simply memorizing previous examples.
2.  **Take inspiration from human cognition:** François suggests looking to cognitive science and developmental psychology for insights. For example, the idea of "core knowledge" - a set of innate priors like objectness, numbers, geometry that underpin our ability to learn more complex concepts.
3.  **Embrace hybrid approaches:** François believes a hybrid approach combining symbolic and neural methods is promising. He gives the example of how humans solve ARC-AGI tasks - we consciously reason step-by-step (symbolic) but also rely heavily on unconscious intuition to quickly prune the search space (neural). Finding ways to combine the two could lead to a breakthrough.
4.  **Aim for generalizable abstractions:** A successful ARC-AGI solver needs to be able to form novel conceptual abstractions to tackle never-before-seen tasks. François suggests trying to make your system's priors/knowledge representation easily swappable and generalizable, rather than overfit to a particular domain. The faster your system can form useful new abstractions, the better it will perform.
5.  **Start small and scale up:** François suggests that the first "ARC-AGI solving" system doesn't need to be a full-fledged AGI from the get-go. A narrow AI system that can handle ARC-like problems in a constrained domain could still be a major breakthrough. Once you have a system that can efficiently learn and generalize in one domain, you can scale it up to more knowledge and problem domains over time.
6.  **Don’t be afraid to try something new:** Since ARC-AGI is still a relatively new and unexplored benchmark, François believes there are still lots of low-hanging fruit to be plucked in terms of novel approaches. Don't be afraid to try radically different ideas from what's been attempted before. Intellectual creativity and originality can go a long way.

### Submissions

ARC Prize 2024 submissions must be made through the Kaggle competition as a Kaggle notebook.

1.  Go to the [ARC Prize 2024 Kaggle page](https://www.kaggle.com/competitions/arc-prize-2024).
2.  If you haven't done so yet, register an account. If you have an account, log in.
3.  To format the output of your submission, view the detailed instructions on Kaggle evaluation.

Notes:

-   Kaggle submissions will not have internet access. Your solution must be able to run offline. This is to ensure that the private evaluation set is not leaked
-   You will only receive a final score across the entire private evaluation set, not a breakdown of which tasks you got (in)correct.
-   Submissions to ARC Prize 2024 will be constrained to the [code requirements](https://arcprize.org/guide#code-requirements). This is to ensure the spirit of "efficiency" is adhered to.
-   [ARC-AGI-Pub](https://arcprize.org/leaderboard) (secondary leaderboard measuring the public evaluation set) does not have compute or internet constraints. Close source, frontier models are welcome to participate.

See [submission templates](https://arcprize.org/guide#submission-templates) to get started quickly.

#### Grand Prize Goal

The Grand Prize is set at 85% to consider material progress towards ARC-AGI, but allow for acknowledgement that the benchmark is imperfect. The benchmark is intended to be a minimal test of general intelligence, something that early forms of artificial general intelligence will necessarily be able to do.

Every ARC-AGI task has been human-verified by at least 2 STEM professionals. Not all humans can solve all tasks, but all tasks can be solved by humans.

While average human performance does not impact the validity of ARC-AGI, it is interesting that the benchmark can function as a human intelligence test in addition to AI. A [2024 NYU study](https://arxiv.org/abs/2409.01374) found that 790 out of 800 (98.7%) of all public ARC tasks are solvable by at least one typical crowd-worker. The average human performance in the study was between 73.3% and 77.2% correct (public training set average: 76.2%; public evaluation set average: 64.2%.)

We plan to do further testing on future versions of ARC-AGI.

#### Scoring Methodology

This competition evaluates submissions on the percentage of correct predictions on the private evaluation set (100 tasks).

For each task, you should predict exactly **2 outputs** for every test input grid contained in the task. (Tasks can have more than one test input that needs a predicted output.)

Each task's test output has one ground truth.

For a given task output, if _any of the 2 predicted outputs_ matches the ground truth exactly (100% correct), you score 1 for that task test output, otherwise 0. The final score is the sum averaged of the highest score per task output divided by the total number of task test outputs. Ex: If there are two task outputs, and one is 100% correct and the other is 0% correct, your score is 0.5.

#### Submission format

Submissions should contain two dictionaries of predictions enclosed in a list, as is shown by the example below. When a task has multiple test outputs that need to be predicted (e.g., task 12997ef3 below), they must be in the same order as the corresponding test inputs.

```
{"00576224": [{"attempt_1": [[0, 0], [0, 0]], "attempt_2": [[0, 0], [0, 0]]}],
 "009d5c81": [{"attempt_1": [[0, 0], [0, 0]], "attempt_2": [[0, 0], [0, 0]]}],
 "12997ef3": [{"attempt_1": [[0, 0], [0, 0]], "attempt_2": [[0, 0], [0, 0]]},
              {"attempt_1": [[0, 0], [0, 0]], "attempt_2": [[0, 0], [0, 0]]}], ...
}
```

  
See more details on [Kaggle](https://arcprize.org/www.kaggle.com/competitions/arc-prize-2024/overview/evaluation).

#### Code Requirements

Submissions to this competition must be made through Notebooks. In order for the "Submit to Competition" button to be active after a commit, the following conditions must be met:

-   CPU Notebook <= 12 hours run-time
-   GPU Notebook <= 12 hours run-time
-   No internet access enabled
-   External data, freely & publicly available, is allowed, including pre-trained models
-   Submission file must be named submission.json

#### Hardware

The submitted notebooks will run on the same hardware that the base notebook was created with. They will be one of the following

-   CPU
    -   4 CPU Cores
    -   30 Gigabytes of RAM
-   P100 GPU
    -   1 Nvidia Tesla P100 GPI
    -   4 CPU cores
    -   29 Gigabytes of RAM
-   T4 2x GPU
    -   2 Nvidia Tesla T4 GPUs
    -   4 CPU cores
    -   29 Gigabytes of RAM

These are not expected to change anytime soon.

### Teams

Did you know that the highest performing ARC-AGI solutions are often made by teams?

Teams are a great way to combine ideas, learn from each other, and even make new friends who are passionate about solving ARC.

If you'd like to form a team, we encourage you to reach out to other participants, post on the [Discord server](https://discord.gg/9b77dPAmcA), post on the [Kaggle discussion board](https://www.kaggle.com/competitions/arc-prize-2024/discussion) or reach out to us at team@arcprize.org.

### ARC-AGI Resources

#### Submission Templates

-   [Brute force](https://www.kaggle.com/code/hansuelijud/template-arc2020-5-crop-tasks-by-brute-force) - Credits go to phunghieu & team. The original write-up and published notebook can be found here: [Write up](https://www.kaggle.com/c/abstraction-and-reasoning-challenge/discussion/154319) [Notebook](https://www.kaggle.com/code/user189546/5-crop-tasks-by-brute-force)
-   [Icecuber's 2020 winning submission](https://www.kaggle.com/code/hansuelijud/template-arc2020-1st-place-solution-by-icecuber) - Along with icecubers [great write up](https://www.kaggle.com/competitions/abstraction-and-reasoning-challenge/discussion/154597) about their submission
-   [Fine-tuning Llama 3b](https://www.kaggle.com/code/hansuelijud/template-llama-3-8b-arc-prize-2024-finetuning) - In this notebook, we will demonstrate how to fine-tune the instruct version of Llama 3 8B using Kaggle hardware.
-   [Using a fine-tuned Llama 3b](https://www.kaggle.com/code/hansuelijud/template-llama-3-8b-arc-prize-2024-inference) - In this notebook, we will demonstrate how to use a fine-tuned version of Llama 3 8B to solve ARC tasks. You can also experiment with the original version or other models compatible with Hugging Face’s infrastructure.

If you have a resource you'd like to share, [let us know about it](https://forms.gle/ngFoYzuQSuiupFbMA).

-   [On Measure of Intelligence](https://arxiv.org/abs/1911.01547)
-   [Videos](https://docs.google.com/spreadsheets/d/1fR4cgjY1kNKN_dxiidBQbyT6Gv7_Ko7daKOjlYojwTY/edit#gid=658867951) - Collection of ARC-AGI videos. Make sure to see [why AI can't pass this test](https://youtu.be/QrSCwxrLrRc?t=912) & [The Hardest Kaggle Challenge](https://www.youtube.com/watch?v=K5KDZLHsr1o)
-   [Repositories](https://docs.google.com/spreadsheets/d/1fR4cgjY1kNKN_dxiidBQbyT6Gv7_Ko7daKOjlYojwTY/edit#gid=167693902) - Collection of repositories of ARC-AGI attempts, synthetic data generation and ARC-AGI domain-specific languages
-   [Papers](https://docs.google.com/spreadsheets/d/1fR4cgjY1kNKN_dxiidBQbyT6Gv7_Ko7daKOjlYojwTY/edit#gid=756763742) - Collection of published papers around program synthesis, object-centric decision transformers and approaches
-   Other [hosted](https://docs.google.com/spreadsheets/d/1fR4cgjY1kNKN_dxiidBQbyT6Gv7_Ko7daKOjlYojwTY/edit#gid=438132109) [community maintain](https://github.com/neoneye/arc-notes/tree/main/awesome) resources

#### Discussions

-   2019-09-14 - [François Chollet: Deep Learning, and the Progress of AI | Lex Fridman Podcast #38](https://www.youtube.com/watch?v=Bo8MY4JpiXE)
-   2020-08-30 - [François Chollet: Measures of Intelligence | Lex Fridman Podcast #120](https://www.youtube.com/watch?v=PUAdj3w3wO4)
-   2021-04-16 - [#51 FRANCOIS CHOLLET - Intelligence and Generalisation](https://www.youtube.com/watch?v=J0p_thJJnoo)
-   2024-01-12 - [The Gradient Podcast - François Chollet: Keras and Measures of Intelligence](https://www.youtube.com/watch?v=g7xONZly9LM)
-   2024-06-11 - [Mike on No Priors](https://youtu.be/LFm_lSiMLm4)
-   2024-06-11 - [François with Dwarkesh](https://youtu.be/UakqL6Pj9xo)

#### LLM Performance on ARC

-   [Large Language Models Are Not Strong Abstract Reasoners](https://arxiv.org/pdf/2305.19555) - Reproduction of GPT-4 scoring 11.9% on ARC-AGI (section 4.1)
-   [Comparing Humans, GPT-4, and GPT-4V On Abstraction and Reasoning Tasks](https://openreview.net/pdf?id=3rGT5OkzpC) - Showing performance of SOTA models (at the time) on ConceptARC, a variation of ARC-AGI (Table 1)
-   [Large Language Models as General Pattern Machines](https://arxiv.org/pdf/2307.04721) - GPT-4 scoring 9% on ARC-AGI public data (Table 1). Note, public data may have been used to train GPT-4 which would artificially improve results
-   [LLMs and the Abstraction and Reasoning Corpus: Successes, Failures, and the Importance of Object-based Representations](https://arxiv.org/pdf/2305.18354v2) - Exploring different methods to solve ARC-AGI with LLMs. Using a less difficult subset of task and CoT, GPT-4 scores 46% with this subset(Table 3)

#### Notable Implementations

-   [ARC2023 - End to End - V7](https://www.kaggle.com/code/mehrankazeminia/arc2023-end-to-end-v7/notebook) - 31 of 100 private evaluation tasks solved
-   [Icecuber](https://www.kaggle.com/competitions/abstraction-and-reasoning-challenge/discussion/154597) - Write up behind the #1 solution in the 2020 Kaggle competition by [icecuber](https://www.kaggle.com/icecuber). 20 of 100 private evaluation tasks solved
-   [Alejandro De Miquel](https://www.kaggle.com/competitions/abstraction-and-reasoning-challenge/discussion/154391) - 2nd place solution in 2020 competition
-   [Ilia Larchenko](https://www.kaggle.com/competitions/abstraction-and-reasoning-challenge/discussion/154409) - Sample of the 3rd place solution in 2020 competition
-   [Alijs](https://www.kaggle.com/competitions/abstraction-and-reasoning-challenge/discussion/154377) - Quick 2020 5th place notes
-   [Zoltan](https://www.kaggle.com/competitions/abstraction-and-reasoning-challenge/discussion/154323) - 2020 6th place write up
-   [Hieu Phung](https://www.kaggle.com/competitions/abstraction-and-reasoning-challenge/discussion/154319) - 2020 9th place solution write up
-   [Alexander Fritzler](https://www.kaggle.com/competitions/abstraction-and-reasoning-challenge/discussion/154294) - 2020 10th place solution write up
-   [James Mcguigan](https://www.kaggle.com/competitions/abstraction-and-reasoning-challenge/discussion/154691) - Explanation of attempts in the 2020 competition

[Toggle Animation](https://arcprize.org/guide#)

---
title: Google - Gemini Long Context
pageTitle: Google - Gemini Long Context | Kaggle
created: 24.325.183443
tags: []
source: https://www.kaggle.com/competitions/gemini-long-context/overview
author: 
---

# Google - Gemini Long Context | Kaggle
source: [](https://www.kaggle.com/competitions/gemini-long-context/overview)

> Demonstrate interesting use cases for Gemini's long context window


Gemini 1.5 introduced a major breakthrough in AI with its notably large context window. It can process up to 2 million tokens at once vs. the typical 32,000 - 128,000 tokens. This is equivalent to being able to remember roughly 100,000 lines of code, 10 years of text messages, or 16 average English novels.

With large context windows, methods like vector databases and [RAG](https://arxiv.org/pdf/2005.11401) (that were built to overcome short context windows) become less important, and more direct methods such as [in-context retrieval](https://arxiv.org/pdf/2406.13121) become viable instead. Likewise, methods like [many-shot prompting](https://arxiv.org/pdf/2404.11018) where models are provided with hundreds or thousands of examples of a task as either a replacement or a supplement for fine-tuning also become possible.

In [initial tests](https://arxiv.org/pdf/2403.05530), the Google Deepmind team saw very promising results, with state-of-the-art performance in long-document QA, long-video QA, and long-context ASR. They [shared an entire code base](https://blog.google/technology/ai/long-context-window-ai-models/) with Gemini 1.5 and had it successfully create documentation. They also had the model "watch" the film Sherlock JR from 1924, and it answered questions correctly.

This competition challenges you to stress test Gemini 1.5’s long context window by building public Kaggle Notebooks and YouTube Videos that demonstrate creative use cases. We’re eager to see what you build!

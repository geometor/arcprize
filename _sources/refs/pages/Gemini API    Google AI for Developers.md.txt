---
title: Gemini API  |  Google AI for Developers
pageTitle: Gemini API  |  Google AI for Developers
created: 24.325.171312
tags: []
source: https://ai.google.dev/gemini-api/docs
author: 
---

# Gemini API  |  Google AI for Developers
source: [](https://ai.google.dev/gemini-api/docs)

> Gemini API Developer Docs and API Reference


-   On this page
-   [Meet the models](https://ai.google.dev/gemini-api/docs#meet-the-models)
-   [Explore the API](https://ai.google.dev/gemini-api/docs#explore-the-api)
    -   [Explore long context](https://ai.google.dev/gemini-api/docs#explore-long-context)
    -   [Solve tasks with fine-tuning](https://ai.google.dev/gemini-api/docs#solve-tasks-with-fine-tuning)
    -   [Generate structured outputs](https://ai.google.dev/gemini-api/docs#generate-structured-outputs)
    -   [Start building with the Gemini API](https://ai.google.dev/gemini-api/docs#start-building-with-the-gemini-api)

## Get started with the Gemini API

bookmark\_border Stay organized with collections Save and categorize content based on your preferences.

The Gemini API and Google AI Studio help you start working with Google's latest models and turn your ideas into applications that scale.

[Python](https://ai.google.dev/gemini-api/docs#python)[Node.js](https://ai.google.dev/gemini-api/docs#node.js)[REST](https://ai.google.dev/gemini-api/docs#rest)

```
<span>import</span> <span>google.generativeai</span> <span>as</span> <span>genai</span>

<span>genai</span><span>.</span><span>configure</span><span>(</span><span>api_key</span><span>=</span><span>"<devsite-var rendered="" translate="no" is-upgraded="" scope="YOUR_API_KEY" tabindex="0"><span><var spellcheck="false" is-upgraded="" data-title="Edit YOUR_API_KEY" aria-label="Edit YOUR_API_KEY">YOUR_API_KEY</var></span></devsite-var>"</span><span>)</span>
<span>model</span> <span>=</span> <span>genai</span><span>.</span><span>GenerativeModel</span><span>(</span><span>"gemini-1.5-flash"</span><span>)</span>
<span>response</span> <span>=</span> <span>model</span><span>.</span><span>generate_content</span><span>(</span><span>"Explain how AI works"</span><span>)</span>
<span>print</span><span>(</span><span>response</span><span>.</span><span>text</span><span>)</span>
```

1.5 Flash

Our most balanced multimodal model with great performance for most tasks

1.5 Flash-8B

Our fastest and most cost-efficient multimodal model with great performance for high-frequency tasks

1.5 Pro

Our best performing multimodal model with features for a wide variety of reasoning tasks

## Explore the API

### Explore long context

Input millions of tokens to Gemini models and derive understanding from unstructured images, videos, and documents.

### Solve tasks with fine-tuning

Modify the behavior of Gemini models to adapt to specific tasks, recognize data, and solve problems. Tune models with your own data to make production deployments more robust and reliable.

### Generate structured outputs

Constrain Gemini to respond with JSON, a structured data format suitable for automated processing.

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2024-11-14 UTC.

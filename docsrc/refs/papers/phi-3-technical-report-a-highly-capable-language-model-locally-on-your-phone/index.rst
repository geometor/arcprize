.. _phi-3-technical-report-a-highly-capable-language-model-locally-on-your-phone:

Phi-3 Technical Report: A Highly Capable Language Model Locally on Your Phone
=============================================================================

:id: 2404.14219
:Authors: Marah Abdin, Jyoti Aneja, Hany Awadalla, Ahmed Awadallah, Ammar Ahmad Awan, Nguyen Bach, Amit Bahree, Arash Bakhtiari, Jianmin Bao, Harkirat Behl, Alon Benhaim, Misha Bilenko, Johan Bjorck, Sébastien Bubeck, Martin Cai, Qin Cai, Vishrav Chaudhary, Dong Chen, Dongdong Chen, Weizhu Chen, Yen-Chun Chen, Yi-Ling Chen, Hao Cheng, Parul Chopra, Xiyang Dai, Matthew Dixon, Ronen Eldan, Victor Fragoso, Jianfeng Gao, Mei Gao, Min Gao, Amit Garg, Allie Del Giorno, Abhishek Goswami, Suriya Gunasekar, Emman Haider, Junheng Hao, Russell J. Hewett, Wenxiang Hu, Jamie Huynh, Dan Iter, Sam Ade Jacobs, Mojan Javaheripi, Xin Jin, Nikos Karampatziakis, Piero Kauffmann, Mahoud Khademi, Dongwoo Kim, Young Jin Kim, Lev Kurilenko, James R. Lee, Yin Tat Lee, Yuanzhi Li, Yunsheng Li, Chen Liang, Lars Liden, Xihui Lin, Zeqi Lin, Ce Liu, Liyuan Liu, Mengchen Liu, Weishung Liu, Xiaodong Liu, Chong Luo, Piyush Madan, Ali Mahmoudzadeh, David Majercak, Matt Mazzola, Caio César Teodoro Mendes, Arindam Mitra, Hardik Modi, Anh Nguyen, Brandon Norick, Barun Patra, Daniel Perez-Becker, Thomas Portet, Reid Pryzant, Heyang Qin, Marko Radmilac, Liliang Ren, Gustavo de Rosa, Corby Rosset, Sambudha Roy, Olatunji Ruwase, Olli Saarikivi, Amin Saied, Adil Salim, Michael Santacroce, Shital Shah, Ning Shang, Hiteshi Sharma, Yelong Shen, Swadheen Shukla, Xia Song, Masahiro Tanaka, Andrea Tupini, Praneetha Vaddamanu, Chunyu Wang, Guanhua Wang, Lijuan Wang, Shuohang Wang, Xin Wang, Yu Wang, Rachel Ward, Wen Wen, Philipp Witte, Haiping Wu, Xiaoxia Wu, Michael Wyatt, Bin Xiao, Can Xu, Jiahang Xu, Weijian Xu, Jilong Xue, Sonali Yadav, Fan Yang, Jianwei Yang, Yifan Yang, Ziyi Yang, Donghan Yu, Lu Yuan, Chenruidong Zhang, Cyril Zhang, Jianwen Zhang, Li Lyna Zhang, Yi Zhang, Yue Zhang, Yunan Zhang, Xiren Zhou
:Published: 2024-04-22
:arXiv: https://arxiv.org/abs/2404.14219
:PDF: https://arxiv.org/pdf/2404.14219
:DOI: N/A
:Journal Reference: N/A
:Primary Category: cs.CL
:Categories: cs.CL, cs.AI
:Comment: 24 pages

:github_url: _

abstract
--------
We introduce phi-3-mini, a 3.8 billion parameter language model trained on
3.3 trillion tokens, whose overall performance, as measured by both academic
benchmarks and internal testing, rivals that of models such as Mixtral 8x7B and
GPT-3.5 (e.g., phi-3-mini achieves 69% on MMLU and 8.38 on MT-bench), despite
being small enough to be deployed on a phone. Our training dataset is a
scaled-up version of the one used for phi-2, composed of heavily filtered
publicly available web data and synthetic data. The model is also further
aligned for robustness, safety, and chat format. We also provide
parameter-scaling results with a 7B, 14B models trained for 4.8T tokens, called
phi-3-small, phi-3-medium, both significantly more capable than phi-3-mini
(e.g., respectively 75%, 78% on MMLU, and 8.7, 8.9 on MT-bench). To enhance
multilingual, multimodal, and long-context capabilities, we introduce three
models in the phi-3.5 series: phi-3.5-mini, phi-3.5-MoE, and phi-3.5-Vision.
The phi-3.5-MoE, a 16 x 3.8B MoE model with 6.6 billion active parameters,
achieves superior performance in language reasoning, math, and code tasks
compared to other open-source models of similar scale, such as Llama 3.1 and
the Mixtral series, and on par with Gemini-1.5-Flash and GPT-4o-mini.
Meanwhile, phi-3.5-Vision, a 4.2 billion parameter model derived from
phi-3.5-mini, excels in reasoning tasks and is adept at handling both
single-image and text prompts, as well as multi-image and text prompts.

.. include:: premise.rst

.. include:: outline.rst

.. include:: quotes.rst

.. include:: notes.rst

.. include:: summary.rst

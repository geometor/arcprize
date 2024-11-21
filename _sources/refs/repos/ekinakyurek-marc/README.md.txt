# README.md

>📋 We are still in progress making this repo clean. Use it with caution and please report errors and questions to us.

# The Surprising Effectiveness of Test-Time Training for Abstract Reasoning

This repository is the official implementation of our paper:

[The Surprising Effectiveness of Test-Time Training for Abstract Reasoning](http://www.mit.edu/~akyurek/papers/ttt.pdf)

Ekin Akyürek, Mehul Damani, Linlu Qiu, Han Guo, Yoon Kim, Jacob Andreas

## Requirements

To install requirements, you can start a fresh conda environment, and install followings with pip:

```shell
git clone --recursive git://github.com/ekinakyurek/marc
cd marc/
# For TTT pipeline, we used a fork of torchtune library.
# You need to install it first
conda create -n arc python=3.10
conda activate arc
# Install torchtune with my specific fork
# We need this as editable because we actually use some files
# under third_party/torchtune/recipes/ which doesn't come
# if you just do pip install
cd third_party/torchtune
pip install -e .
# install other required libraries for torchtune
pip install torch torchao --pre --upgrade --index-url https://download.pytorch.org/whl/nightly/cu121

# Then we have simple requirements can be installed as:
pip install -r requirements.txt
```

>📋 You need download the ARC dataset from kaggle link https://www.kaggle.com/competitions/arc-prize-2024/data

>📋 You can reach out finetuned models and TTT checkpoints from the following links:
> - For Llama-3.x checkpoints: https://huggingface.co/meta-llama
> - For our finetuned Llama-3 8B checkpoints: https://huggingface.co/ekinakyurek/marc-8B-finetuned-llama3
> - For finetuned BARC checkpoints: https://huggingface.co/barc0/Llama-3.1-ARC-Potpourri-Transduction-8B
> - For our LoRA adapters for Llama-3 8B model: https://huggingface.co/ekinakyurek/marc-lora-adapters-8B-finetuned-llama3
> - For our Lora adapter for BARC model: https://huggingface.co/ekinakyurek/marc-lora-adapters-Llama-3.1-ARC-Potpourri-Transduction-8B


## Test Time Training

To train the model(s) in the paper, run this command:

```shell
# Specify data path
data_file=/kaggle/input/arc-prize-2024/arc-agi_evaluation_challenges.json
# Specify finetuned path
base_checkpoint_dir=/path/to/finetuned/model/folder/
# Specify where TTT adapters should be saved
ttt_folder=/path/to/ttt/folder
mkdir -p $ttt_folder


# You need show an initial config file that is compatible with torchtune configs
# This is provided in this repo
lora_config_file=configs/ttt/8B_lora_single_device.yaml
# lora_config_file=configs/ttt/8.1B_lora_single_device.yaml # for barc
# But you can override some of the variables
batch_size=2
epochs=2
learning_rate=5e-5
lora_rank=128
lora_alpha=16.0
lora_to_output=False # doesn't apply for Llama3.2 models for now.
# You can specify how many tasks you want train for.
num_tasks=15

# You can run the main script
python test_time_train.py --lora_config=$lora_config_file \
--base_checkpoint_dir=$base_checkpoint_dir \
--experiment_folder=$ttt_folder \
--data_file=$data_file \
--batch_size=$batch_size \
--epochs=$epochs \
--num_tasks=${num_tasks} \
--lora_rank=$lora_rank \
--lora_alpha=$lora_alpha \
--lora_to_output=$lora_to_output \
--new_format # use --barc_format for barc
```

> 📋 If you are using BARC checkpoints and unmask_outputs and if unmask_outputs=True in the program arguments
> then you need to uncomment these lines in my torchtune clone [here](https://github.com/ekinakyurek/torchtune/blob/efd85e000e83dcf6803c623cf83943e4a817377a/torchtune/models/llama3/_tokenizer.py#L51-L55)

>📋  TTT training will save adapter checkpints under `ttt_folder` you specified above.

## Inference

To do inference with TTT, you run `predict.py`

```shell
# Specify data path
data_file=/kaggle/input/arc-prize-2024/arc-agi_evaluation_challenges.json
# Tell where your Fintuned (named as base) and TTT checkpoints are
base_checkpoint_dir=/path/to/finetuned/model/folder/
ttt_folder=/path/to/ttt/folder

# if solution file is given predict will evaluate the model
solution_file=/kaggle/input/arc-prize-2024/arc-agi_evaluation_solutions.json


temperature=0
n_sample=1

# this should be same as your ttt
max_lora_rank=128
# You need to tell where predictions and submissions should be saved
tti_folder=/path/to/tti/folder
mkdir -p $tti_folder


python predict.py \
--experiment_folder=$tti_folder \
--pretrained_checkpoint=$base_checkpoint_dir \
--lora_checkpoints_folder=$ttt_folder \
--temperature=$temperature \
--n_sample=$n_sample \
--data_file=$data_file \
--solution_file=$solution_file \
--max_lora_rank=$max_lora_rank \
--include_n=1 \
--new_format
```

>📋  For Llama-3 and Llama-3.2 we used different versions of VLLM, and these are not compatible with torchtune version that we use. So, we give setup instructions for vllm for llama3 and vllm for llama3-2 for reproducibiltiy. We use seperate conda environments for inference pipeline.

```shell
# For Llama3 and 3.1 models
conda create -n vllm python=3.10
conda activate vllm
pip install vllm@git+https://github.com/ekinakyurek/vllm.git@ekin/torchtunecompat
pip install -r requirements
```

```shell
# For Llama3.2 models
conda create -n vllmnew python=3.10
conda activate vllmnew
pip install vllm@git+https://github.com/ekinakyurek/vllm.git@ekin/ekin/newvllm
pip install -r requirements
```
# Predictions from models
- For our finetuned Llama-3 8B + TTT predictions: https://huggingface.co/ekinakyurek/marc-predictions-8B-finetuned-ttted/
- For finetuned BARC + TTT predictions: https://huggingface.co/ekinakyurek/marc-predictions-Llama-3.1-ARC-Potpourri-Transduction-8B-tted/
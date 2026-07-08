# SciTrek: A Benchmark for Long-Context Language Models Based on Numerical Reasoning over Scientific Articles
[![arXiv](https://img.shields.io/badge/arxiv-2509.21028-lightgrey)](https://arxiv.org/pdf/2509.21028) [![dataset](https://img.shields.io/badge/dataset-SciTrek-orange)](https://huggingface.co/datasets/oaimli/SciTrek) [![code](https://img.shields.io/badge/GitHub-SciTrek-darkblue
)](https://github.com/oaimli/SciTrek)

The benchmark is based on long-context question answering over scientific articles, where the input is multiple full-text scientific articles and a question focused on numerical reasoning, and the output is the answer to the question. For more details on data curation, refer to the paper. 

Each sample in our data is composed of the following key-value pairs:
```text
# 'articles': article ids that comprise the context (corresponds to benchmark/article/papers_final.json)
# 'sample_level': the level of the sample and how we concatenate the articles, e.g., multi_ran_64, multi_dfs_64, and multi_bfs_64 (ran: random, bfs: breadth first traversal, dfs: depth first traversal)
# 'sql_type': corresponding reasoning skill, e.g., multi_graph_filtering (relational filtering)
# 'focus': the question focus, e.g, reference_count
# 'sql': the SQL query
# 'template': the original template of the SQL query
# 'question': the question generated from the SQL query
# 'answer': the answer from the SQL query execution
# 'label': the label of the sample, e.g., training, dev, test

# sql_type interpretation:
# "multi_graph_filtering" -> "Graph Filtering"
# "multi_ran_aggregating" -> "Aggregating"
# "multi_ran_filtering_foa" -> "Filtering+Aggregating"
# "multi_ran_filtering_foo" -> "Filtering+Sorting"
# "multi_ran_filtering_ofo" -> "Filtering"
# "multi_ran_organizing" -> "Sorting"

```
### What is in this repository
```
/
├── benchmark/              --> (Code for construction of our benchmark, and loading our benchmark data)
├── docs/                   --> (The website for the work)
├── eval_test/              --> (Code for evaluation in terms of EM and F1, and fine-grained analysis)
├── other/                  --> (Other analysis, e.g., failure patterns and question difficulty)
├── pilot_study/            --> (Pilot test of the models before the project got started)
├── prerequisite/           --> (Analysis to show our numerical reasoning is fundamental to real-world tasks, e.g., in LongBench v2)
├── results_test/           --> (Generations from the benchmarking models)   
├── test_full/              --> (The inference code of models based on full contexts)
├── test_meta/              --> (The inference code of models based on metadata contexts)
├── train_full/             --> (Post-training open-source models with SciTrek)   
└── README.md               --> (This readme file)
```

### Explanations on the prompt templates

All our prompt templates can be found in /SciTrek/benchmark/dataset/instructions. Basically, we have chain-of-thought (CoT) and non-reasoning (non-CoT) prompts for both metadata contexts and full contexts.

- instruction_full_scitrek.txt: prompt template on full contexts (models are prompted to directly generate the answer)
- instruction_meta_scitrek.txt: prompt template on metadata contexts (models are prompted to directly generate the answer)
- reasoning_instruction_full_scitrek.txt: chain-of-thought prompt template on full contexts
- reasoning_instruction_meta_scitrek.txt: chain-of-thought prompt template on metadata contexts

In model benchmarking, we used the CoT prompts for thinking models, while we used the non-CoT prompts for non-thinking models.

For post-training, we used CoT prompts for RLVR and non-CoT prompts for SFT for all models.

### Use the SciTrek dataset from Hugging Face
```python
from datasets import load_dataset

dataset = load_dataset("oaimli/scitrek")
train_dataset = dataset["train"]
dev_dataset = dataset["val"]
test_dataset = dataset["test"]
print(len(train_dataset), len(dev_dataset), len(test_dataset))

# full-text contexts, direct answer generation
for sample in test_dataset:
    prompt_full = sample["prompt_full"]
    question = prompt_full["question"]
    answer = prompt_full["answer"]
    context = prompt_full["context"]
    instruction = prompt_full["instruction_direct"]
    instruction = instruction.replace("<question>", question)
    prompt_content = instruction.replace("<articles>", context)
    conversation = [{"role": "user", "content": prompt_content}]

# full-text contexts, chain-of-thought prompting
for sample in test_dataset:
    prompt_full = sample["prompt_full"]
    question = prompt_full["question"]
    answer = prompt_full["answer"]
    context = prompt_full["context"]
    instruction = prompt_full["instruction_reasoning"]
    instruction = instruction.replace("<question>", question)
    prompt_content = instruction.replace("<articles>", context)
    conversation = [{"role": "user", "content": prompt_content}]

# metadata contexts, direct answer generation
for sample in test_dataset:
    prompt_meta = sample["prompt_meta"]
    question = prompt_meta["question"]
    answer = prompt_meta["answer"]
    table_articles_text = prompt_meta["table_articles_text"]
    table_article_author_text = prompt_meta["table_article_author_text"]
    table_citing_cited_text = prompt_meta["table_citing_cited_text"]

    instruction = prompt_meta["instruction_direct"]
    instruction = instruction.replace("<question>", question)
    instruction = instruction.replace("<table-articles>", table_articles_text)
    instruction = instruction.replace("<table-article_author>", table_article_author_text)
    instruction = instruction.replace("<table-citing_cited>", table_citing_cited_text)
    prompt_content = instruction
    conversation = [{"role": "user", "content": prompt_content}]

# metadata contexts, chain-of-thought prompting
for sample in test_dataset:
    prompt_meta = sample["prompt_meta"]
    question = prompt_meta["question"]
    answer = prompt_meta["answer"]
    table_articles_text = prompt_meta["table_articles_text"]
    table_article_author_text = prompt_meta["table_article_author_text"]
    table_citing_cited_text = prompt_meta["table_citing_cited_text"]

    instruction = prompt_meta["instruction_reasoning"]
    instruction = instruction.replace("<question>", question)
    instruction = instruction.replace("<table-articles>", table_articles_text)
    instruction = instruction.replace("<table-article_author>", table_article_author_text)
    instruction = instruction.replace("<table-citing_cited>", table_citing_cited_text)
    prompt_content = instruction
    conversation = [{"role": "user", "content": prompt_content}]

``` 

### Use the SciTrek dataset based on downloaded files

First, download the files from [Google Drive](https://drive.google.com/drive/folders/10LoC8ga5qoxK1axDYD_Hxpi9Pv0bz9KN?usp=sharing), including pdfs, clusters, and samples.

Replace the target folders with the downloaded ones:
- pdfs -> SciTrek/benchmark/pdfs
- clusters -> SciTrek/benchmark/dataset/clusters
- samples -> SciTrek/benchmark/dataset/samples

Then, you can load the data following the code in SciTrek/benchmark/dataset/data_loading.py


### Model generations and evaluation results

Download the results_test folder from the Google Drive link and replace the SciTrek/results_test with it, then you will see model generations in separate JSON Lines files for all experimental models.

These generation results are from SciTrek/test_full (on full contexts) and test_meta (on metadata contexts), running inference for different models.

You can see the evaluation pipeline in SciTrek/eval_test/evaluating_generations.py, and other analyses, including fine-grained error analysis in eval_test.

### Post-training open-weight LLMs on SciTrek

For post-training with supervised fine-tuning (SFT) and Reinforcement Learning with Verifiable Rewards (RLVR) on SciTrek, refer to the folder of train_full.


If you are going to use our dataset to test or train your model, please cite our paper:

[Li et al. 2025] Miao Li, Alexander Gurung, Irina Saparina, Mirella Lapata. "Who Gets Cited Most? Benchmarking Long-Context Numerical Reasoning on Scientific Articles". arXiv 2509.21028, 2025.
```
@inproceedings{scitrek_2025,
  title={Who Gets Cited Most? Benchmarking Long-Context Numerical Reasoning on Scientific Articles},
  author={Miao Li, Alexander Gurung, Irina Saparina, Mirella Lapata},
  booktitle={arXiv 2509.21028},
  year={2025}
}
```


If you have any questions about using our data, feel free to contact miao.li@ed.ac.uk.

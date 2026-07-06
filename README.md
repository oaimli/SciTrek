# SciTrek: A Benchmark for Long-Context Language Models Based on Numerical Reasoning over Scientific Articles
[![arXiv](https://img.shields.io/badge/arxiv-2509.21028-lightgrey)](https://arxiv.org/pdf/2509.21028) [![dataset](https://img.shields.io/badge/dataset-SciTrek-orange)](https://huggingface.co/datasets/oaimli/SciTrek) [![code](https://img.shields.io/badge/GitHub-SciTrek-darkblue
)](https://github.com/oaimli/SciTrek)

The benchmark is based on long-context question answering over scientific articles, where the input is multiple full-text scientific articles and a question focused on numerical reasoning, and the output is the answer to the question. For more details on data curation, refer to the paper. 

Each sample of our data is composed of the following key-value pairs:
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


### Use the constructed data from Hugging Face
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

### Construct the data based on local files

### Model generations and evaluation results

### Post-training open-weight LLMs with SciTrek

If you are interested in testing your model with our benchmark or using our constructed training data in your long-context post-training, our data is available on [Google Drive](https://drive.google.com/drive/folders/10LoC8ga5qoxK1axDYD_Hxpi9Pv0bz9KN?usp=sharing)

If you have any questions about using our data, feel free to contact miao.li@ed.ac.uk.

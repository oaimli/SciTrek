from datasets import load_dataset


dataset = load_dataset("oaimli/scitrek")
train_dataset = dataset["train"]
dev_dataset = dataset["val"]
test_dataset = dataset["test"]
print(len(train_dataset), len(dev_dataset), len(test_dataset))

# full contexts, direct answer generation
for sample in test_dataset:
    prompt_full = sample["prompt_full"]
    question = prompt_full["question"]
    context = prompt_full["context"]
    instruction = prompt_full["instruction_direct"]
    instruction = instruction.replace("<question>", question)
    prompt_content = instruction.replace("<articles>", context)
    conversation = [{"role": "user", "content": prompt_content}]

# full contexts, chain-of-thought prompting
for sample in test_dataset:
    prompt_full = sample["prompt_full"]
    question = prompt_full["question"]
    context = prompt_full["context"]
    instruction = prompt_full["instruction_reasoning"]
    instruction = instruction.replace("<question>", question)
    prompt_content = instruction.replace("<articles>", context)
    conversation = [{"role": "user", "content": prompt_content}]

# meta contexts, direct answer generation
for sample in test_dataset:
    prompt_meta = sample["prompt_meta"]
    question = prompt_meta["question"]
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

# meta contexts, chain-of-thought prompting
for sample in test_dataset:
    prompt_meta = sample["prompt_meta"]
    question = prompt_meta["question"]
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
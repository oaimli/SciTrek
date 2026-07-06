import sys
from tqdm import tqdm
from jsonlines import jsonlines
from datasets import load_dataset

sys.path.append("../../")
from benchmark.dataset.data_loading import load_train, load_test, load_articles, get_full_texts, get_tables


if __name__ == "__main__":
    train_data, dev_data = load_train(prefixes=["64k", "128k"], samples_folder= "../dataset/samples/final/", no_null=True, no_simple=True)
    test_64 = load_test(prefix="64k", samples_folder= "../dataset/samples/final/", no_null=True, no_simple=True)
    test_128 = load_test(prefix="128k", samples_folder= "../dataset/samples/final/", no_null=True, no_simple=True)
    test_512 = load_test(prefix="512k", samples_folder= "../dataset/samples/final/", no_null=True, no_simple=True)
    test_1024 = load_test(prefix="1024k", samples_folder= "../dataset/samples/final/", no_null=True, no_simple=True)
    print("train/dev/test", f"{len(train_data)}/{len(dev_data)}/{len(test_64)+len(test_128)+len(test_512)+len(test_1024)}")

    articles_all = load_articles(articles_folder="../article/")

    def process_data(samples):
        for sample_index, sample in tqdm(enumerate(samples), total=len(samples)):
            question = sample["question"]

            prompt_full = {}
            markdowns = get_full_texts(sample, articles_all)
            context = "\n".join(markdowns)
            instruction_reasoning = open("../dataset/instructions/reasoning_instruction_full_scitrek.txt").read()
            instruction_direct = open("../dataset/instructions/instruction_full_scitrek.txt").read()
            prompt_full["question"] = question
            prompt_full["context"] = context
            prompt_full["instruction_reasoning"] = instruction_reasoning
            prompt_full["instruction_direct"] = instruction_direct

            prompt_meta = {}
            table_articles, table_article_author, table_citing_cited = get_tables(sample, articles_all)
            table_articles_text = "\n".join([", ".join([str(tmp) for tmp in row]) for row in table_articles])
            table_article_author_text = "\n".join(
                [", ".join([str(tmp) for tmp in row]) for row in table_article_author])
            table_citing_cited_text = "\n".join(
                [", ".join([str(tmp) for tmp in row]) for row in table_citing_cited])
            instruction_reasoning = open("../dataset/instructions/reasoning_instruction_meta_scitrek.txt").read()
            instruction_direct = open("../dataset/instructions/instruction_meta_scitrek.txt").read()
            prompt_meta["question"] = question
            prompt_meta["table_articles_text"] = table_articles_text
            prompt_meta["table_article_author_text"] = table_article_author_text
            prompt_meta["table_citing_cited_text"] = table_citing_cited_text
            prompt_meta["instruction_reasoning"] = instruction_reasoning
            prompt_meta["instruction_direct"] = instruction_direct

            sample["prompt_full"] = prompt_full
            sample["prompt_meta"] = prompt_meta
            samples[sample_index] = sample

    process_data(train_data)
    process_data(dev_data)
    test_data = test_64 + test_128 + test_512 + test_1024
    process_data(test_data)

    with jsonlines.open("train.jsonl", "w") as writer:
        writer.write_all(train_data)
    with jsonlines.open("val.jsonl", "w") as writer:
        writer.write_all(dev_data)
    with jsonlines.open("test.jsonl", "w") as writer:
        writer.write_all(test_data)

    dataset = load_dataset("json", data_files={"train": "train.jsonl", "val": "val.jsonl", "test": "test.jsonl"})
    dataset.push_to_hub("oaimli/SciTrek")
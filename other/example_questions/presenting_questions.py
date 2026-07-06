import sys
import jsonlines
import random
sys.path.append("../../")
from bench.dataset.data_loading import load_train, load_articles, get_tables

if __name__ == "__main__":
    dataset_dir = "../../bench"
    articles_all = load_articles(articles_folder=dataset_dir + "/article/")
    samples_train_64k, _ = load_train(prefixes=["64k"], samples_folder=dataset_dir + "/dataset/samples/final/",
                                 no_null=True, no_simple=True)
    samples_train_64k = random.sample(samples_train_64k, 10)
    with jsonlines.open("64k_examples.jsonl", mode="w") as writer:
        writer.write_all(samples_train_64k)

    samples_train_128k, _ = load_train(prefixes=["128k"], samples_folder=dataset_dir + "/dataset/samples/final/",
                                      no_null=True, no_simple=True)
    samples_train_128k = random.sample(samples_train_128k, 10)
    with jsonlines.open("128k_examples.jsonl", mode="w") as writer:
        writer.write_all(samples_train_128k)

    samples_train_512k, _ = load_train(prefixes=["512k"], samples_folder=dataset_dir + "/dataset/samples/final/",
                                       no_null=True, no_simple=True)
    samples_train_512k = random.sample(samples_train_512k, 10)
    with jsonlines.open("512k_examples.jsonl", mode="w") as writer:
        writer.write_all(samples_train_512k)

    samples_train_1024k, _ = load_train(prefixes=["1024k"], samples_folder=dataset_dir + "/dataset/samples/final/",
                                       no_null=True, no_simple=True)
    samples_train_1024k = random.sample(samples_train_1024k, 10)
    with jsonlines.open("1024k_examples.jsonl", mode="w") as writer:
        writer.write_all(samples_train_1024k)

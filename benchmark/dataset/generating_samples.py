import json
import random
import copy
import jsonlines
from tqdm import tqdm
from typing import List
import itertools
import os
import sqlite3
def instantiating_sql(target_sql_dict, papers_all, cluster_article_ids):
    original_sql = target_sql_dict["sql"]
    cluster_articles = []
    for article_id in cluster_article_ids:
        article = papers_all[article_id]
        article["article_id"] = article_id
        cluster_articles.append(article)

    title_word_counts = []
    author_names_all = []
    article_title_words_all = []
    reference_counts = []
    author_counts_all = []
    for article in cluster_articles:
        reference_count = article["referenceCount"]
        author_names = article["authors"].split(",")
        article_title = article["title"]
        title_word_count = len(article_title.split())
        author_count = len(author_names)
        title_word_counts.append(title_word_count)
        for author_name in author_names:
            author_names_all.append(author_name.strip())
        article_title_words_all.extend(article_title.split())
        reference_counts.append(reference_count)
        author_counts_all.append(author_count)

    instantiated_sql = original_sql.replace("{title-word-count}", str(random.choice(title_word_counts)))
    instantiated_sql = instantiated_sql.replace("{article-title-fragment}", f"\'%{random.choice(article_title_words_all)}%\'")
    instantiated_sql = instantiated_sql.replace("{reference-count}", str(random.choice(reference_counts)))
    instantiated_sql = instantiated_sql.replace("{author-position}", str(random.choice(range(min(author_counts_all) - 1, max(author_counts_all)))))
    instantiated_sql = instantiated_sql.replace("{author-name}", f"\'{random.choice(author_names_all)}\'")
    instantiated_sql = instantiated_sql.replace("{author-count}", str(random.choice(author_counts_all)))

    return instantiated_sql


def generating_samples(clusters, papers_all, sql_queries):
    samples = []
    for cluster in clusters:
        cluster_article_ids = cluster["papers"] # a list of article ids
        cluster_level = cluster["level"] # single, multi_ran, multi_dfs, multi_bfs
        # sql sampling
        target_sqls = []
        target_sampling_count = 0
        if cluster_level.startswith("single"):
            target_sqls = []
            for sql_item in sql_queries:
                if sql_item["type"].startswith("multi_simple"):
                    target_sqls.append(sql_item)
            target_sampling_count = 2
        elif cluster_level.startswith("multi_ran"):
            target_sqls = []
            for sql_item in sql_queries:
                if sql_item["type"].startswith("multi_simple") or sql_item["type"].startswith("multi_ran"):
                    target_sqls.append(sql_item)
            target_sampling_count = 10
        elif cluster_level.startswith("multi_bfs"):
            target_sqls = []
            for sql_item in sql_queries:
                if sql_item["type"].startswith("multi_graph"):
                    target_sqls.append(sql_item)
            target_sampling_count = 10
        elif cluster_level.startswith("multi_dfs"):
            target_sqls = []
            for sql_item in sql_queries:
                if sql_item["type"].startswith("multi_graph"):
                    target_sqls.append(sql_item)
            target_sampling_count = 10
        else:
            print("Error in the type of the cluster level", cluster_level)
        assert len(target_sqls) > 0 and target_sampling_count > 0

        for target_sql in random.sample(target_sqls, target_sampling_count):
            instantiated_sql = instantiating_sql(target_sql, papers_all, cluster_article_ids)
            sample = {}
            sample["articles"] = cluster_article_ids
            sample["sample_level"] = cluster_level
            sample["sql_type"] = target_sql["type"]
            sample["focus"] = target_sql["focus"]
            sample["sql"] = instantiated_sql
            sample["template"] = target_sql["sql"]
            sample["question"] = ""
            sample["answer"] = ""
            samples.append(sample)
    return samples


def splitting_samples(samples):
    sql_types = []
    for sample in samples:
        sql_types.append(sample["sql_type"])
    focuses = []
    for sample in samples:
        focuses.append(sample["focus"])
    print(len(set(sql_types)), len(set(focuses)))
    samples_test = []
    samples_dev = []
    samples_training = []
    for sql_type in set(sql_types):
        for focus in set(focuses):
            category_samples_all = []
            for sample in samples:
                if sample["sql_type"] == sql_type and focus == sample["focus"]:
                    category_samples_all.append(sample)
            category_test_count = int(len(category_samples_all) * 0.1)
            category_dev_count = int(len(category_samples_all) * 0.05)
            category_samples_test_indexes = random.sample(range(len(category_samples_all)), category_test_count)
            for sample_test_index in category_samples_test_indexes:
                sample = category_samples_all[sample_test_index]
                sample["label"] = "test"
                samples_test.append(sample)
            category_samples_dev_training_indexes = []
            for sample_all_index in range(len(category_samples_all)):
                if sample_all_index not in category_samples_test_indexes:
                    category_samples_dev_training_indexes.append(sample_all_index)
            category_samples_dev_indexes = random.sample(category_samples_dev_training_indexes, category_dev_count)
            for sample_dev_index in category_samples_dev_indexes:
                sample = category_samples_all[sample_dev_index]
                sample["label"] = "dev"
                samples_dev.append(sample)
            for sample_index in category_samples_dev_training_indexes:
                if sample_index not in category_samples_dev_indexes:
                    sample = category_samples_all[sample_index]
                    sample["label"] = "training"
                    samples_training.append(sample)
    print(len(samples_test), len(samples_dev), len(samples_training))
    samples_split = samples_test + samples_dev + samples_training
    assert len(samples) == len(samples_split)

    return samples_split


if __name__ == "__main__":
    random.seed(42)
    with open("../article/papers_final.json") as f:
        papers_all = json.load(f)
    print("papers_all", len(papers_all))

    # sql queries
    with open("templates_human/sqls_multi_simple.json", "r") as f:
        sqls_multi_simple = json.load(f)
    with open("templates_human/sqls_multi_ran_aggregating.json", "r") as f:
        sqls_multi_ran_aggregating = json.load(f)
    with open("templates_human/sqls_multi_ran_organizing.json", "r") as f:
        sqls_multi_ran_organizing = json.load(f)
    with open("templates_human/sqls_multi_ran_filtering_ofo.json", "r") as f:
        sqls_multi_ran_filtering_ofo = json.load(f)
    with open("templates_human/sqls_multi_ran_filtering_foo.json", "r") as f:
        sqls_multi_ran_filtering_foo = json.load(f)
    with open("templates_human/sqls_multi_ran_filtering_foa.json", "r") as f:
        sqls_multi_ran_filtering_foa = json.load(f)
    with open("templates_human/sqls_multi_graph_filtering.json", "r") as f:
        sqls_multi_graph_filtering = json.load(f)

    sql_queries_all = sqls_multi_simple + sqls_multi_ran_organizing + sqls_multi_ran_aggregating + sqls_multi_ran_filtering_foa + sqls_multi_ran_filtering_foo + sqls_multi_ran_filtering_ofo + sqls_multi_graph_filtering
    print("sql_queries_all", len(sql_queries_all))


    clusters = []
    with jsonlines.open("clusters/single_clusters_all.jsonl") as reader:
        for line in reader:
            clusters.append(line)
    samples = generating_samples(clusters, papers_all, sql_queries_all)
    samples = splitting_samples(samples)
    random.shuffle(samples)
    # with jsonlines.open("samples/init/single_samples_all.jsonl", "w") as writer:
    #     writer.write_all(samples)
    print("samples single", len(samples))

    clusters = []
    with jsonlines.open("clusters/64k_clusters_all.jsonl") as reader:
        for line in reader:
            clusters.append(line)
    samples = generating_samples(clusters, papers_all, sql_queries_all)
    samples = splitting_samples(samples)
    random.shuffle(samples)
    # with jsonlines.open("samples/init/64k_samples_all.jsonl", "w") as writer:
    #     writer.write_all(samples)
    print("samples 64k", len(samples))

    clusters = []
    with jsonlines.open("clusters/128k_clusters_all.jsonl") as reader:
        for line in reader:
            clusters.append(line)
    samples = generating_samples(clusters, papers_all, sql_queries_all)
    samples = splitting_samples(samples)
    random.shuffle(samples)
    # with jsonlines.open("samples/init/128k_samples_all.jsonl", "w") as writer:
    #     writer.write_all(samples)
    print("samples 128k", len(samples))

    clusters = []
    with jsonlines.open("clusters/512k_clusters_all.jsonl") as reader:
        for line in reader:
            clusters.append(line)
    samples = generating_samples(clusters, papers_all, sql_queries_all)
    samples = splitting_samples(samples)
    random.shuffle(samples)
    # with jsonlines.open("samples/init/512k_samples_all.jsonl", "w") as writer:
    #     writer.write_all(samples)
    print("samples 512k", len(samples))

    clusters = []
    with jsonlines.open("clusters/1024k_clusters_all.jsonl") as reader:
        for line in reader:
            clusters.append(line)
    samples = generating_samples(clusters, papers_all, sql_queries_all)
    samples = splitting_samples(samples)
    random.shuffle(samples)
    # with jsonlines.open("samples/init/1024k_samples_all.jsonl", "w") as writer:
    #     writer.write_all(samples)
    print("samples 1024k", len(samples))
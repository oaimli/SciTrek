# data loading for training and testing
import os.path
import jsonlines
import json
from typing import List


def get_full_texts(sample, papers_all):
    cluster_papers = []
    for paper_id in sample["articles"]:
        paper = papers_all[paper_id]
        cluster_papers.append(paper)

    markdowns = []
    for i, paper in enumerate(cluster_papers):
        markdowns.append(paper["markdown"])

    return markdowns


def get_titles(sample, papers_all):
    cluster_papers = []
    for paper_id in sample["articles"]:
        paper = papers_all[paper_id]
        paper["article_id"] = paper_id
        cluster_papers.append(paper)

    titles = []
    for paper in cluster_papers:
        titles.append(paper["title"])
    return titles


def get_tables(sample, papers_all):
    cluster_papers = []
    for paper_id in sample["articles"]:
        paper = papers_all[paper_id]
        paper["article_id"] = paper_id
        cluster_papers.append(paper)

    simplified_ids = {}
    for i, paper in enumerate(cluster_papers):
        simplified_ids[paper["article_id"]] = f"article_{i}"

    # articles
    articles = []
    articles.append(["article_id", "article_title", "title_word_count", "author_count", "reference_count"])
    for paper in cluster_papers:
        article_id = simplified_ids[paper["article_id"]]
        article_title = paper["title"]
        title_word_count = len(article_title.split())
        author_count = len(paper["authors"].split(","))
        reference_count = paper["referenceCount"]
        articles.append([article_id, article_title, title_word_count, author_count, reference_count])

    # article-author
    article_author = []
    article_author.append(["article_id", "author_name", "author_position"])
    for paper in cluster_papers:
        article_id = simplified_ids[paper["article_id"]]
        paper_authors = [author.strip() for author in paper["authors"].split(",")]
        for order, author in enumerate(paper_authors):
            article_author.append([article_id, author, order])

    # citing_cited
    citing_cited = []
    citing_cited.append(["article_id_citing", "article_id_cited"])
    article_ids = []
    for paper in cluster_papers:
        article_ids.append(paper["article_id"])
    for paper in cluster_papers:
        article_id = paper["article_id"]
        paper_references = paper["references"]
        for paper_reference in paper_references:
            if paper_reference in article_ids:
                citing_cited.append([simplified_ids[article_id], simplified_ids[paper_reference]])

    return articles, article_author, citing_cited


def load_articles(articles_folder="../article/"):
    with open(os.path.join(articles_folder, "papers_final.json")) as f:
        articles_all = json.load(f)
    return articles_all


def load_test(prefix="64k", samples_folder="samples/final/", no_null=False, no_simple=False):
    # loading test data, one level of samples at each time
    assert prefix in ["single", "64k", "128k", "512k", "1024k"]

    samples_test = []
    save_file = os.path.join(samples_folder, f"{prefix}_samples_target.jsonl")

    with jsonlines.open(save_file) as reader:
        for line in reader:
            valid_sample = True
            if line["question"] == "":
                valid_sample = False
            if "database" in line["question"]:
                valid_sample = False
            if no_null and line["answer"] == "NULL":
                valid_sample = False
            if no_simple and line["sql_type"] == "multi_simple":
                valid_sample = False

            if valid_sample:
                if line["label"] == "test":
                    samples_test.append(line)
    print(prefix, len(samples_test))
    return samples_test


# load valid test data with full texts
def load_train(prefixes: List[str], samples_folder="samples/final/", no_null=False, no_simple=False):
    # loading training data, multiple levels of samples at each time
    assert len(set(prefixes)) == len(prefixes)
    assert  set(prefixes).issubset({"64k", "128k", "512k", "1024k"})

    samples_training = []
    samples_dev = []
    for prefix in prefixes:
        samples_training_tmp = []
        samples_dev_tmp = []
        with jsonlines.open(os.path.join(samples_folder, f"{prefix}_samples_target.jsonl")) as reader:
            for line in reader:
                valid_sample = True
                if line["question"] == "":
                    valid_sample = False
                if "database" in line["question"]:
                    valid_sample = False
                if no_null and line["answer"] == "NULL":
                    valid_sample = False
                if no_simple and line["sql_type"] == "multi_simple":
                    valid_sample = False

                if valid_sample:
                    if line["label"] == "training":
                        samples_training_tmp.append(line)

                    if line["label"] == "dev":
                        samples_dev_tmp.append(line)

        print(prefix, f"training={len(samples_training_tmp)}, dev={len(samples_dev_tmp)}")
        samples_training.extend(samples_training_tmp)
        samples_dev.extend(samples_dev_tmp)
    return samples_training, samples_dev


if __name__ == "__main__":
    data_path = "."
    train_data, dev_data = load_train(prefixes=["64k", "128k", "512k", "1024k"], no_null=True)
    test_64 = load_test(prefix="64k", no_null=True, no_simple=True)
    test_128 = load_test(prefix="128k", no_null=True, no_simple=True)
    test_512 = load_test(prefix="512k", no_null=True, no_simple=True)
    test_1024 = load_test(prefix="1024k", no_null=True, no_simple=True)
    print("train/dev/test", f"{len(train_data)}/{len(dev_data)}/{len(test_64)+len(test_128)+len(test_512)+len(test_1024)}")

    articles_all = load_articles(articles_folder="../article/")
    # 'title', 'year', 'url', 'authors', 'abstract', 'referenceCount', 'citations', 'references',
    # 'pdf_access', 'subtopic', 'length', 'references_original', 'citations_original', 'references_title', 'markdown'
    for article_id, article_content in articles_all.items():
        print(article_id, article_content.keys())
        break

    # data statistics
    questions = set([])
    templates = set([])
    sql_queries = set([])
    for sample in train_data:
        questions.add(sample["question"])
        templates.add(sample["template"])
        sql_queries.add(sample["sql"])
    print("unique questions", len(questions), "templates", len(templates), "SQL queries", len(sql_queries))

    # conversational prompt construction for different contexts

    # full contexts, direct answer generation
    for sample in test_64:
        print(sample["sample_level"])
        question = sample["question"]
        markdowns = get_full_texts(sample, articles_all)
        context = "\n".join(markdowns)
        instruction = open("instructions/instruction_full_scitrek.txt").read()
        instruction = instruction.replace("<question>", question)
        prompt_content = instruction.replace("<articles>", context)
        conversation = [{"role": "user", "content": prompt_content}]

    # full contexts, chain-of-thought prompting
    for sample in test_64:
        question = sample["question"]
        markdowns = get_full_texts(sample, articles_all)
        context = "\n".join(markdowns)
        instruction = open("instructions/reasoning_instruction_full_scitrek.txt").read()
        instruction = instruction.replace("<question>", question)
        prompt_content = instruction.replace("<articles>", context)
        conversation = [{"role": "user", "content": prompt_content}]

    # meta contexts, direct answer generation
    for sample in test_64:
        question = sample["question"]
        table_articles, table_article_author, table_citing_cited = get_tables(sample, articles_all)
        table_articles_text = "\n".join([", ".join([str(tmp) for tmp in row]) for row in table_articles])
        table_article_author_text = "\n".join(
            [", ".join([str(tmp) for tmp in row]) for row in table_article_author])
        table_citing_cited_text = "\n".join(
            [", ".join([str(tmp) for tmp in row]) for row in table_citing_cited])

        instruction = open("instructions/instruction_meta_scitrek.txt").read()
        instruction = instruction.replace("<question>", question)
        instruction = instruction.replace("<table-articles>", table_articles_text)
        instruction = instruction.replace("<table-article_author>", table_article_author_text)
        instruction = instruction.replace("<table-citing_cited>", table_citing_cited_text)
        prompt_content = instruction
        conversation = [{"role": "user", "content": prompt_content}]

    # meta contexts, chain-of-thought prompting
    for sample in test_64:
        question = sample["question"]
        table_articles, table_article_author, table_citing_cited = get_tables(sample, articles_all)
        table_articles_text = "\n".join([", ".join([str(tmp) for tmp in row]) for row in table_articles])
        table_article_author_text = "\n".join(
            [", ".join([str(tmp) for tmp in row]) for row in table_article_author])
        table_citing_cited_text = "\n".join(
            [", ".join([str(tmp) for tmp in row]) for row in table_citing_cited])

        instruction = open("instructions/reasoning_instruction_meta_scitrek.txt").read()
        instruction = instruction.replace("<question>", question)
        instruction = instruction.replace("<table-articles>", table_articles_text)
        instruction = instruction.replace("<table-article_author>", table_article_author_text)
        instruction = instruction.replace("<table-citing_cited>", table_citing_cited_text)
        prompt_content = instruction
        conversation = [{"role": "user", "content": prompt_content}]
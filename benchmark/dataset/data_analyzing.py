# get statistics for the constructed data
import numpy as np
from transformers import AutoTokenizer
from data_loading import load_train, load_test, get_full_texts, load_articles, get_tables
import matplotlib.pyplot as plt
import numpy as np
import os
import json
import jsonlines
import random
import sqlite3


def analyze_null_answers(samples):
    # input length
    input_lengths = set([])
    # question focus
    question_focuses = set([])
    # sql complexity
    sql_complexities = set([])
    # sql type
    sql_types = set([])

    for sample in samples:
        input_lengths.add(sample["sample_level"].split("_")[-1])
        question_focuses.add(sample["focus"])
        sql_complexities.add(len(sample["sql"].split()))
        sql_types.add(sample["sql_type"])

    print("input_lengths", input_lengths)
    print("question_focuses", question_focuses)
    print("sql_complexities", sql_complexities)
    print("sql_types", sql_types)

    # ground truth answer
    result_distribution = {}
    for input_length in input_lengths:
        for sample in samples:
            sample_level = sample["sample_level"].split("_")[-1]
            if input_length == sample_level and sample["answer"] == "NULL":
                result_distribution[sample_level] = result_distribution.get(sample_level, 0) + 1
    print("null answers in input lengths", result_distribution)

    result_distribution = {}
    for focus in question_focuses:
        for sample in samples:
            question_focus = sample["focus"]
            if question_focus == focus and sample["answer"] == "NULL":
                result_distribution[focus] = result_distribution.get(focus, 0) + 1
    print("null answers in question focuses", result_distribution)

    result_distribution = {}
    for sql_complexity in sql_complexities:
        for sample in samples:
            complexity = len(sample["sql"].split())
            if sql_complexity == complexity and sample["answer"] == "NULL":
                result_distribution[str(complexity)] = result_distribution.get(str(complexity), 0) + 1
    print("null answers in sql complexities", result_distribution)

    result_distribution = {}
    for sql_type in sql_types:
        for sample in samples:
            type = sample["sql_type"]
            if sql_type == type and sample["answer"] != "NULL":
                result_distribution[type] = result_distribution.get(type, 0) + 1
    print("null answers in sql types", result_distribution)


def constructing_db(cluster_papers):
    db_name = "tmp_analyzing.db"
    if os.path.exists(db_name):
        os.remove(db_name)
    con = sqlite3.connect(db_name)
    cur = con.cursor()

    # articles
    cur.execute(
        "CREATE TABLE articles (article_id, article_title, title_word_count, author_count, reference_count)")
    for paper in cluster_papers:
        article_id = paper["article_id"]
        article_title = paper["title"]
        title_word_count = len(article_title.split())
        author_count = len(paper["authors"].split(","))
        reference_count = paper["referenceCount"]
        cur.execute(
            "INSERT INTO articles (article_id, article_title, title_word_count, author_count, reference_count) VALUES (?, ?, ?, ?, ?)",
            (article_id, article_title, title_word_count, author_count, reference_count))
    # res = cur.execute("SELECT article_id FROM articles")
    # print(res.fetchall())

    # article-author
    cur.execute("CREATE TABLE article_author (relation_id, article_id, author_name, author_position)")
    article_authors = []
    for paper in cluster_papers:
        article_id = paper["article_id"]
        paper_authors = [author.strip() for author in paper["authors"].split(",")]
        for order, author in enumerate(paper_authors):
            article_authors.append((article_id, author, order))
    for i, pair in enumerate(article_authors):
        cur.execute(
            "INSERT INTO article_author (relation_id, article_id, author_name, author_position) VALUES (?, ?, ?, ?)",
            (f"relation_{i}", pair[0], pair[1], pair[2]))
    # res = cur.execute("SELECT relation_id FROM article_author")
    # print(res.fetchall())

    # citing_cited
    cur.execute("CREATE TABLE citing_cited (relation_id, article_id_citing, article_id_cited)")
    article_ids = []
    for paper in cluster_papers:
        article_ids.append(paper["article_id"])
    article_reference = []
    for paper in cluster_papers:
        article_id = paper["article_id"]
        paper_references = paper["references"]
        for paper_reference in paper_references:
            if paper_reference in article_ids:
                article_reference.append((article_id, paper_reference))
    for i, pair in enumerate(article_reference):
        cur.execute("INSERT INTO citing_cited (relation_id, article_id_citing, article_id_cited) VALUES (?, ?, ?)",
                    (f"relation_{i}", pair[0], pair[1]))
    # res = cur.execute("SELECT relation_id FROM article_reference")
    # print(res.fetchall())

    con.commit()
    cur.close()
    return con


def statistics_qa(samples_all):
    # lengths of the questions
    lengths_questions = []
    for sample in samples_all:
        lengths_questions.append(len(sample["question"].split()))

    # lengths of the answers
    lengths_answers = []
    for sample in samples_all:
        lengths_answers.append(len(sample["answer"].split()))

    # paper counts
    paper_counts = []
    for sample in samples_all:
        paper_counts.append(len(sample["articles"]))

    # lengths of the SQLs
    lengths_sqls = []
    for sample in samples_all:
        lengths_sqls.append(len(sample["sql"].split()))

    # numbers of SQL clauses in single SQL query and their distribution among questions
    sql_clauses = []
    with open("templates_human/clauses.txt", "r") as f:
        for line in f.readlines():
            sql_clauses.append(line.strip())

    def find_all(target, sub):
        result = []
        start = 0
        while True:
            start = target.find(sub, start)
            if start != -1:
                result.append(start)
                start += len(sub)  # use start += 1 to find overlapping matches
            else:
                break
        return result

    distribution_clauses = {}
    for clause in sql_clauses:
        distribution_clauses[clause] = 0
    numbers_clauses = []
    for sample in samples_all:
        sql = " ".join(sample["sql"].strip().split())
        clauses_tmp = []
        for clause in sql_clauses:
            matches = find_all(sql, clause)
            if len(matches) > 0:
                distribution_clauses[clause] = distribution_clauses.get(clause, 0) + 1
            clauses_tmp.append(len(matches))
        numbers_clauses.append(sum(clauses_tmp))
    distribution_questions_sorted = sorted(distribution_clauses.items(), key=lambda item: item[1], reverse=True)
    print("distribution_clauses")
    for item in distribution_questions_sorted:
        print(f"{item[0]}:", item[1])
    assert len(numbers_clauses) == len(lengths_questions) == len(lengths_sqls)

    combined = []
    for number_clause, length_question, length_sql, lengths_answer, paper_count in zip(numbers_clauses, lengths_questions, lengths_sqls, lengths_answers, paper_counts):
        combined.append((number_clause, length_question, length_sql, lengths_answer, paper_count))
    combined = sorted(combined, key=lambda item: item[0])

    numbers_clauses_sorted = []
    lengths_questions_sorted = []
    lengths_sqls_sorted = []
    lengths_answers_sorted = []
    paper_counts_sorted = []
    for item in combined:
        numbers_clauses_sorted.append(item[0])
        lengths_questions_sorted.append(item[1])
        lengths_sqls_sorted.append(item[2])
        lengths_answers_sorted.append(item[3])
        paper_counts_sorted.append(item[4])

    # numbers_clauses_sorted = [x/max(numbers_clauses_sorted) for x in numbers_clauses_sorted]
    # lengths_questions_sorted = [x/max(lengths_questions_sorted) for x in lengths_questions_sorted]
    # lengths_sqls_sorted = [x/max(lengths_sqls_sorted) for x in lengths_sqls_sorted]
    print("numbers_clauses_sorted", np.max(numbers_clauses_sorted), np.min(numbers_clauses_sorted),
          np.mean(numbers_clauses_sorted))
    print("lengths_questions_sorted", np.max(lengths_questions_sorted), np.min(lengths_questions_sorted), np.mean(lengths_questions_sorted))
    print("lengths_sqls_sorted", np.max(lengths_sqls_sorted), np.min(lengths_sqls_sorted), np.mean(lengths_sqls_sorted))
    print("lengths_answers_sorted", np.max(lengths_answers_sorted), np.min(lengths_answers_sorted), np.mean(lengths_answers_sorted))
    print("papers_counts", np.max(paper_counts_sorted), np.min(paper_counts_sorted), np.mean(paper_counts_sorted))


def table_length(samples_test):
    articles = load_articles(articles_folder="../article/")
    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-7B-Instruct-1M")
    table_lengths = []
    for sample in samples_test:
        table_articles, table_article_author, table_citing_cited = get_tables(sample, articles)
        rows = []
        for row in table_articles:
            rows.append(" ".join([str(tmp) for tmp in row]))
        for row in table_article_author:
            rows.append(" ".join([str(tmp) for tmp in row]))
        for row in table_citing_cited:
            rows.append(" ".join([str(tmp) for tmp in row]))
        text = "\n".join(rows)
        table_lengths.append(len(tokenizer.encode(text)))

    print("table_lengths", np.max(table_lengths), np.min(table_lengths), np.mean(table_lengths))



if __name__ == "__main__":
    sample_levels = ["64k", "128k"]

    samples_train, samples_dev = load_train(prefixes=sample_levels, no_null=True, no_simple=True)

    samples_test = []
    for sample_level in sample_levels:
        samples_test_tmp = load_test(prefix=sample_level, no_null=True, no_simple=True)
        print(sample_level, len(samples_test_tmp))
        samples_test.extend(samples_test_tmp)

    print("samples train", len(samples_train), "samples dev", len(samples_dev), "samples test", len(samples_test))

    statistics_qa(samples_test)
    table_length(samples_test)


    # statistics of SQL queries
    sql_templates = set([])
    sql_types = set([])
    question_focuses = set([])
    for sample in samples_test:
        # print(sample.keys())
        sql_templates.add(sample["template"])
        sql_types.add(sample["sql_type"])
        question_focuses.add(sample["focus"])
    print("sql_templates", len(sql_templates), "sql_types", len(sql_types), "question_focuses", len(question_focuses))
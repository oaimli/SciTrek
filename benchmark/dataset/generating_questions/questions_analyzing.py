# get statistics for the generated questions
import matplotlib.pyplot as plt
import numpy as np
import os
import json
import jsonlines
import random
import sqlite3


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


def statistics_questions(samples_all):
    # lengths of the questions
    lengths_questions = []
    for sample in samples_all:
        lengths_questions.append(len(sample["question"].split()))

    # lengths of the SQLs
    lengths_sqls = []
    for sample in samples_all:
        lengths_sqls.append(len(sample["sql"].split()))

    # numbers of SQL clauses in single SQL query and their distribution among questions
    sql_clauses = []
    with open("../templates_human/clauses.txt", "r") as f:
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
    for number_clause, length_question, length_sql in zip(numbers_clauses, lengths_questions, lengths_sqls):
        combined.append((number_clause, length_question, length_sql))
    combined = sorted(combined, key=lambda item: item[0])
    numbers_clauses_sorted = []
    lengths_questions_sorted = []
    lengths_sqls_sorted = []
    for item in combined:
        numbers_clauses_sorted.append(item[0])
        lengths_questions_sorted.append(item[1])
        lengths_sqls_sorted.append(item[2])

    # numbers_clauses_sorted = [x/max(numbers_clauses_sorted) for x in numbers_clauses_sorted]
    # lengths_questions_sorted = [x/max(lengths_questions_sorted) for x in lengths_questions_sorted]
    # lengths_sqls_sorted = [x/max(lengths_sqls_sorted) for x in lengths_sqls_sorted]
    print("numbers_clauses_sorted", np.max(numbers_clauses_sorted), np.min(numbers_clauses_sorted),
          np.mean(numbers_clauses_sorted))

    # plot
    x = range(0, len(numbers_clauses))
    plt.figure(figsize=(9, 5))
    plt.plot(x, lengths_questions_sorted, color='deepskyblue', label="Word Number in Question")
    plt.plot(x, lengths_sqls_sorted, color='darkcyan', label="Word Number in SQL")
    plt.plot(x, numbers_clauses_sorted, color="orange", label="Clause Number in SQL")
    plt.yticks(fontsize=22)
    plt.xticks(fontsize=22)
    plt.xlabel("Question index", fontdict={"size": 22})
    plt.legend(prop={"size": 17})
    plt.subplots_adjust(top=0.97, bottom=0.15, right=0.98, left=0.11)
    # plt.show()
    plt.savefig('statistics.png', dpi=1024)


def check_answers():
    with open("../../article/papers_final.json") as f:
        papers_all = json.load(f)
    samples_64k = []
    with jsonlines.open("../samples/gpt41/64k_samples_target.jsonl") as reader:
        for line in reader:
            samples_64k.append(line)
    samples_all = samples_64k

    # check the answers
    failures_sql = set([])
    for sample in samples_all:
        if sample["answer"] == "" and sample["question"] == "":
            failures_sql.add(sample["template"])
        if sample["answer"] == "None" and sample["question"] != "":
            sample_sql = sample["sql"]
            cluster_papers = []
            for paper_id in sample["articles"]:
                paper = papers_all[paper_id]
                paper["article_id"] = paper_id
                cluster_papers.append(paper)
            con = constructing_db(cluster_papers)
            cur = con.cursor()
            result = []
            execution = cur.execute(sample_sql).fetchall()
            print(execution)
            if execution != None:
                for row in execution:
                    x = [str(y) for y in row]
                    if len(x) > 0:
                        result.append(",".join(x))
            answer = ",".join(result) if len(result) > 0 else ""
            print(answer, sample["answer"])
    print(len(failures_sql))
    for failure in failures_sql:
        print(failure)

    for template in failures_sql:
        print("Failure", template)
        for sample in samples_all:
            sample_template = sample["template"]
            sample_question = sample["question"]
            sample_answer = sample["answer"]
            if sample_template == template:
                if sample_question != "" and sample_answer != "":
                    print(sample)


def check_failures():
    failure_templates_all = set([])
    failure_sqls_all = set([])
    failure_samples_all = []
    samples_all = []
    failure_sql_types_all = set([])
    samples_all = []
    # for prefix in ["64k", "128k", "512k", "1024k", "single"]:
    #     if prefix in ["64k", "128k", "single"]:
    #         target_labels = ["training", "dev", "test"]
    #     else:
    #         target_labels = ["test"]
    for prefix in ["64k", "128k", "512k", "1024k"]:
        target_labels = ["training", "dev", "test"]

        save_file = f"../samples/other/{prefix}_samples_target.jsonl"

        samples_done = []
        with jsonlines.open(save_file) as reader:
            for line in reader:
                if line["label"] in target_labels:
                    samples_done.append(line)
        samples_all.extend(samples_done)
        print(f"{prefix}", len(samples_done))

        failure_samples = []
        failure_templates = set([])
        failure_sqls = set([])
        failure_sql_types = set([])
        for sample in samples_done:
            samples_all.append(sample)
            if sample["question"] == "" or "database" in sample["question"]:
                failure_samples.append(sample)
                failure_templates.add(sample["template"])
                failure_sqls.add(sample["sql"])
                failure_sql_types.add(sample["sql_type"])
        print("failure samples: ", len(failure_samples))
        print("failure sqls: ", len(failure_sqls))
        print("failure templates: ", len(failure_templates))
        print("failure sql types: ", len(failure_sql_types))
        failure_samples_all.extend(failure_samples)
        failure_sqls_all.update(failure_sqls)
        failure_templates_all.update(failure_templates)
        failure_sql_types_all.update(failure_sql_types)

    print("failure samples all: ", len(failure_samples_all))
    print("failure sqls all: ", len(failure_sqls_all))
    print("failure templates all: ", len(failure_templates_all))
    print("failure sql types all: ", len(failure_sql_types_all))
    print(failure_sql_types_all)
    # for failure_sql in failure_sqls_all:
    #     print(failure_sql)

    detailed_counts = {}
    template_counts = {}
    for sample in samples_all:
        if sample["question"] != "":
            if "database" not in sample["question"]:
                info = sample["sql_type"]
                detailed_counts[info] = detailed_counts.get(info, 0) + 1

                if sample["label"] == "test":
                    template = sample["template"]
                    template_counts[template] = template_counts.get(template, 0) + 1
    print("samples", sum(list(detailed_counts.values())), "SQL categories", len(detailed_counts))
    for info, count in detailed_counts.items():
        templates = set([])
        for sample in samples_all:
            if sample["sql_type"] == info and sample["question"] != "":
                template = sample["template"]
                templates.add(template)
        print(info, "samples:", count, "templates:", len(templates))


def check_naturalness():
    samples_all = []
    non_natural = []
    for prefix in ["64k", "128k", "512k", "1024k", "single"]:
        if prefix in ["64k", "128k", "single"]:
            target_labels = ["training", "dev", "test"]
        else:
            target_labels = ["test"]

        save_file = f"../samples/qwen25/{prefix}_samples_target.jsonl"

        samples_prefix = []
        with jsonlines.open(save_file) as reader:
            for line in reader:
                if line["label"] in target_labels:
                    samples_prefix.append(line)
        samples_all.extend(samples_prefix)

        for sample in samples_prefix:
            question = sample["question"]
            if "database" in question:
                non_natural.append(sample)
                print(question)

    print(len(samples_all), len(non_natural))


def check_diversity():
    questions_all = []
    sqls_all = []
    for prefix in ["64k", "128k", "512k", "1024k", "single"]:
        if prefix in ["64k", "128k", "single"]:
            target_labels = ["training", "dev", "test"]
        else:
            target_labels = ["test"]

        save_file = f"../samples/llama33/{prefix}_samples_target.jsonl"

        with jsonlines.open(save_file) as reader:
            for line in reader:
                if line["label"] in target_labels:
                    if "database" not in line["question"] and line["question"] != "":
                        questions_all.append(line["question"])
                        sqls_all.append(line["sql"])

    print(len(set(sqls_all)), len(set(questions_all)))



if __name__ == "__main__":
    check_failures()



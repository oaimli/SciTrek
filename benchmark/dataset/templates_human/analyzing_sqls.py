# get statistics for the generated questions
import json
import numpy as np
import os
import sqlite3
import jsonlines
import random


def constructing_db(cluster_papers):
    db_name = "../tmp.db"
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
    return con


def sql_validation(sql, db_con):
    execution = 1
    cur = db_con.cursor()
    try:
        cur.execute(sql)
        db_con.rollback()
    except Exception as err:
        print("SQL execution error", err)
        execution = 0

    return execution


if __name__ == "__main__":
    with open("sqls_multi_simple.json", "r") as f:
        sqls_multi_simple = json.load(f)
    with open("sqls_multi_ran_aggregating.json", "r") as f:
        sqls_multi_ran_aggregating = json.load(f)
    with open("sqls_multi_ran_organizing.json", "r") as f:
        sqls_multi_ran_organizing = json.load(f)
    with open("sqls_multi_ran_filtering_ofo.json", "r") as f:
        sqls_multi_ran_filtering_ofo = json.load(f)
    with open("sqls_multi_ran_filtering_foo.json", "r") as f:
        sqls_multi_ran_filtering_foo = json.load(f)
    with open("sqls_multi_ran_filtering_foa.json", "r") as f:
        sqls_multi_ran_filtering_foa = json.load(f)
    with open("sqls_multi_graph_filtering.json", "r") as f:
        sqls_multi_graph_filtering = json.load(f)

    print("sqls_multi_simple", len(sqls_multi_simple))
    print("sqls_multi_ran_aggregating", len(sqls_multi_ran_aggregating))
    print("sqls_multi_ran_organizing", len(sqls_multi_ran_organizing))
    print("sqls_multi_ran_filtering_foa", len(sqls_multi_ran_filtering_foa))
    print("sqls_multi_ran_filtering_foo", len(sqls_multi_ran_filtering_foo))
    print("sqls_multi_ran_filtering_ofo", len(sqls_multi_ran_filtering_ofo))
    print("sqls_multi_graph_filtering", len(sqls_multi_graph_filtering))

    sqls_all = sqls_multi_simple + sqls_multi_ran_organizing + sqls_multi_ran_aggregating + sqls_multi_ran_filtering_foa + sqls_multi_ran_filtering_foo + sqls_multi_ran_filtering_ofo + sqls_multi_graph_filtering
    print("sqls_all", len(sqls_all))

    # executable
    with open("../../article/papers_final.json") as f:
        papers_all = json.load(f)
    clusters_multi_ran = []
    clusters_multi_graph = []
    clusters_single = []
    # the SQLs can be easily adapted to longer contexts
    with jsonlines.open("../clusters/64k_clusters_all.jsonl") as reader:
        for line in reader:
            if line["level"] == "multi_bfs_64":
                clusters_multi_graph.append(line)
            if line["level"] == "multi_dfs_64":
                clusters_multi_graph.append(line)
            if line["level"] == "multi_ran_64":
                clusters_multi_ran.append(line)
    clusters_single = []
    with jsonlines.open("../clusters/single_clusters_all.jsonl") as reader:
        for line in reader:
            clusters_single.append(line)

    for item in sqls_all:
        sql = item["sql"]
        type = item["type"]

        # print(sql)
        sql = sql.replace("{title-word-count}", str(random.choice(range(5, 20))))
        sql = sql.replace("{article-title-fragment}", "\'%Survey%\'")
        sql = sql.replace("{reference-count}", str(random.choice(range(10, 50))))
        sql = sql.replace("{author-position}", str(random.choice(range(0, 20))))
        sql = sql.replace("{author-name}", "\'Ivan\'")
        sql = sql.replace("{author-count}", str(random.choice(range(1, 20))))
        # print(sql)

        if type.startswith("multi_simple"):
            cluster_papers = []
            for paper_id in random.choice(clusters_single)["papers"]:
                paper = papers_all[paper_id]
                paper["article_id"] = paper_id
                cluster_papers.append(paper)
            con_single = constructing_db(cluster_papers)
            execution = sql_validation(sql, con_single)
            if execution != 1:
                print(item)

            cluster_papers = []
            for paper_id in random.choice(clusters_multi_ran)["papers"]:
                paper = papers_all[paper_id]
                paper["article_id"] = paper_id
                cluster_papers.append(paper)
            con_single = constructing_db(cluster_papers)
            execution = sql_validation(sql, con_single)
            if execution != 1:
                print(item)

        if type.startswith("multi_ran"):
            # SQLs for a random multi-article-random cluster
            cluster_papers = []
            for paper_id in random.choice(clusters_multi_ran)["papers"]:
                paper = papers_all[paper_id]
                paper["article_id"] = paper_id
                cluster_papers.append(paper)
            con_multi_ran = constructing_db(cluster_papers)
            execution = sql_validation(sql, con_multi_ran)
            if execution != 1:
                print(item)

        if type.startswith("multi_graph"):
            # SQLs for a random multi-article-graph cluster
            cluster_papers = []
            for paper_id in random.choice(clusters_multi_graph)["papers"]:
                paper = papers_all[paper_id]
                paper["article_id"] = paper_id
                cluster_papers.append(paper)
            con_multi_graph = constructing_db(cluster_papers)
            execution = sql_validation(sql, con_multi_graph)
            if execution != 1:
                print(item)


    # lengths of the SQLs
    lengths_sqls = []
    for question in sqls_all:
        lengths_sqls.append(len(question["sql"].split()))

    # numbers of SQL clauses in single SQL query and their distribution
    sql_clauses = []
    with open("clauses.txt", "r") as f:
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
    for question in sqls_all:
        sql = " ".join(question["sql"].strip().split())
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
    assert len(numbers_clauses) == len(lengths_sqls)

    combined = []
    for number_clause, length_sql in zip(numbers_clauses, lengths_sqls):
        combined.append((number_clause, length_sql))
    combined = sorted(combined, key=lambda item: item[0])
    numbers_clauses_sorted = []
    lengths_sqls_sorted = []
    for item in combined:
        numbers_clauses_sorted.append(item[0])
        lengths_sqls_sorted.append(item[1])

    print("numbers_clauses_sorted", np.max(numbers_clauses_sorted), np.min(numbers_clauses_sorted),
          np.mean(numbers_clauses_sorted))

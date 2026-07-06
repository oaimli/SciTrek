import os
import json
import jsonlines
import random
import sqlite3


def constructing_db(cluster_papers):
    db_name = "reusing_tmp.db"
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

if __name__ == "__main__":
    with open("../../article/papers_final.json") as f:
        papers_all = json.load(f)

    gpt4_samples_single = []
    with jsonlines.open("../samples/qwen25/single_samples_target.jsonl") as reader:
        for line in reader:
            gpt4_samples_single.append(line)
    gpt4_samples_64k = []
    with jsonlines.open("../samples/qwen25/64k_samples_target.jsonl") as reader:
        for line in reader:
            gpt4_samples_64k.append(line)
    gpt4_samples_128k = []
    with jsonlines.open("../samples/qwen25/128k_samples_target.jsonl") as reader:
        for line in reader:
            gpt4_samples_128k.append(line)
    gpt4_samples_512k = []
    with jsonlines.open("../samples/other/512k_samples_target.jsonl") as reader:
        for line in reader:
            gpt4_samples_512k.append(line)
    gpt4_samples_1024k = []
    with jsonlines.open("../samples/other/1024k_samples_target.jsonl") as reader:
        for line in reader:
            gpt4_samples_1024k.append(line)

    for prefix in ["512k", "1024k"]:
        if prefix == "512k":
            for sample_x_index, sample_x in enumerate(gpt4_samples_512k):
                sample_x_sql = sample_x["sql"]
                questions_done = set([])
                for sample_y in gpt4_samples_single + gpt4_samples_64k + gpt4_samples_128k + gpt4_samples_512k + gpt4_samples_1024k:
                    sample_y_sql = sample_y["sql"]
                    if sample_y_sql == sample_x_sql and sample_y["question"] != "":
                        questions_done.add(sample_y["question"])
                if len(questions_done) > 0:
                    sample_x["question"] = random.choice(list(questions_done))

                    cluster_papers = []
                    for paper_id in sample_x["articles"]:
                        paper = papers_all[paper_id]
                        paper["article_id"] = paper_id
                        cluster_papers.append(paper)
                    con = constructing_db(cluster_papers)
                    cur = con.cursor()
                    original_result = []
                    original_execution = cur.execute(sample_x_sql).fetchall()
                    if original_execution != None:
                        for row in original_execution:
                            x = [str(y) for y in row]
                            if len(x) > 0:
                                original_result.append(", ".join(x))
                    sample_x["answer"] = ", ".join(original_result) if len(original_result) > 0 else ""

                    gpt4_samples_512k[sample_x_index] = sample_x

            with jsonlines.open("../samples/qwen25/512k_samples_target.jsonl", "w") as writer:
                writer.write_all(gpt4_samples_512k)
        if prefix == "1024k":
            for sample_x_index, sample_x in enumerate(gpt4_samples_1024k):
                sample_x_sql = sample_x["sql"]
                questions_done = set([])
                for sample_y in gpt4_samples_single + gpt4_samples_64k + gpt4_samples_128k + gpt4_samples_512k + gpt4_samples_1024k:
                    sample_y_sql = sample_y["sql"]
                    if sample_y_sql == sample_x_sql and sample_y["question"] != "":
                        questions_done.add(sample_y["question"])
                if len(questions_done) > 0:
                    sample_x["question"] = random.choice(list(questions_done))

                    cluster_papers = []
                    for paper_id in sample_x["articles"]:
                        paper = papers_all[paper_id]
                        paper["article_id"] = paper_id
                        cluster_papers.append(paper)
                    con = constructing_db(cluster_papers)
                    cur = con.cursor()
                    original_result = []
                    original_execution = cur.execute(sample_x_sql).fetchall()
                    if original_execution != None:
                        for row in original_execution:
                            x = [str(y) for y in row]
                            if len(x) > 0:
                                original_result.append(", ".join(x))
                    sample_x["answer"] = ", ".join(original_result) if len(original_result) > 0 else ""

                    gpt4_samples_1024k[sample_x_index] = sample_x

            with jsonlines.open("../samples/qwen25/1024k_samples_target.jsonl", "w") as writer:
                writer.write_all(gpt4_samples_1024k)
import os
import json
import jsonlines
import random
import sqlite3


def constructing_db(cluster_papers):
    db_name = "correcting_tmp.db"
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

    for prefix in ["single", "64k", "128k", "512k", "1024k"]:
        save_file = f"../samples/llama33/{prefix}_samples_target.jsonl"
        qwen_samples = []
        with jsonlines.open(save_file) as reader:
            for line in reader:
                qwen_samples.append(line)

        for sample_x_index, sample_x in enumerate(qwen_samples):
            if sample_x["question"] != "":
                cluster_papers = []
                for paper_id in sample_x["articles"]:
                    paper = papers_all[paper_id]
                    paper["article_id"] = paper_id
                    cluster_papers.append(paper)
                con = constructing_db(cluster_papers)
                cur = con.cursor()
                original_result = []
                original_execution = cur.execute(sample_x["sql"]).fetchall()
                if original_execution != None:
                    for row in original_execution:
                        x = [str(y) for y in row]
                        if len(x) > 0:
                            original_result.append(", ".join(x))
                sample_x["answer"] = ", ".join(original_result) if len(original_result) > 0 else ""

                if sample_x["answer"] == "" or sample_x["answer"] == "None":
                    sample_x["answer"] = "NULL"

                qwen_samples[sample_x_index] = sample_x

        with jsonlines.open(save_file, "w") as writer:
            writer.write_all(qwen_samples)
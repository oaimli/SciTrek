import random
import json
import jsonlines
import time
from openai import OpenAI
import os
import sqlite3
from tqdm import tqdm


def constructing_db(cluster_papers):
    db_name = "tmp_other.db"
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


def validating_sql(sql, db_con):
    execution = 1
    cur = db_con.cursor()
    try:
        cur.execute(sql)
        db_con.rollback()
    except Exception as err:
        print("SQL execution error", err)
        execution = 0
    cur.close()
    return execution


def llm_prompting_sql2nl(sql, sample):
    # load details of all articles
    with open("../../article/papers_final.json") as f:
        papers_all = json.load(f)
    # print("papers_all", len(papers_all))

    # load cluster of articles
    cluster_papers = []
    for paper_id in sample["articles"]:
        paper = papers_all[paper_id]
        paper["article_id"] = paper_id
        cluster_papers.append(paper)
    con = constructing_db(cluster_papers)

    # load the prompt
    prompt_content = open("prompt_sql2nl.txt").read().strip()
    prompt_content = prompt_content.replace("<SQL_QUERY>", sql)

    openai_api_key = "EMPTY"
    openai_api_base = "http://localhost:8000/v1"
    client = OpenAI(
        api_key=openai_api_key,
        base_url=openai_api_base,
        )
    trials = 0
    while True:
        try:
            output_dict = client.chat.completions.create(
                model="Qwen/Qwen2.5-Coder-32B-Instruct",
                messages=[
                    {"role": "system",
                     "content": "You are requested to carefully understand the instruction about SQL and give the response following the required format."},
                    {"role": "user",
                     "content": prompt_content}
                    ],
                n=1,
                temperature=0.97,
                )
            output_raw = output_dict.choices[0].message.content
            print(output_raw)
            # parse the question and sql
            trials += 1
            try:
                output_json = json.loads(output_raw)
                if isinstance(output_json, dict):
                    if "question" in output_json.keys():
                        output_original, output_inverse = comparing_sqls(sql, output_json["question"], con)
                        if output_original == output_inverse:
                            question = output_json["question"]
                            answer = output_original
                            break
            except json.JSONDecodeError as err:
                print("JSON parsing error,", err)

            if trials == 10:
                question = ""
                answer = ""
                break
        except Exception as e:
            print(e)
            if "limit" in str(e):
                time.sleep(1)
    con.close()

    return question, answer


def llm_prompting_nl2sql(question, db_con):
    prompt_content = open("prompt_nl2sql.txt").read().strip()
    prompt_content = prompt_content.replace("<QUESTION>", question)
    openai_api_key = "EMPTY"
    openai_api_base = "http://localhost:8000/v1"
    client = OpenAI(
        api_key=openai_api_key,
        base_url=openai_api_base,
        )
    trials = 0
    while True:
        try:
            output_dict = client.chat.completions.create(
                model="Qwen/Qwen2.5-Coder-32B-Instruct",
                messages=[
                    {"role": "system",
                     "content": "You are requested to carefully understand the instruction about SQL and give the response following the required format."},
                    {"role": "user",
                     "content": prompt_content}
                    ],
                n=1,
                temperature=0.97,
                )
            output_raw = output_dict.choices[0].message.content
            print(output_raw)
            # parse the generation
            trials += 1
            try:
                output_json = json.loads(output_raw)
                if isinstance(output_json, dict):
                    if "sql" in output_json.keys():
                        inverse_sql = output_json["sql"]
                        if validating_sql(inverse_sql, db_con):
                            break
            except json.JSONDecodeError as err:
                print("JSON parsing error,", err)

            if trials == 5:
                inverse_sql = ""
                break
        except Exception as e:
            print(e)
            if "limit" in str(e):
                time.sleep(1)
    return inverse_sql


def comparing_sqls(original_sql, generated_question, db_con):
    inverse_sql = llm_prompting_nl2sql(generated_question, db_con)
    print("original sql: ", original_sql)
    print("inverse sql: ", inverse_sql)

    executability = 1
    try:
        cur = db_con.cursor()
        cur.execute(original_sql)
        db_con.rollback()
    except Exception as err:
        print("original SQL execution error", err)
        executability = 0
    try:
        cur = db_con.cursor()
        cur.execute(inverse_sql)
        db_con.rollback()
    except Exception as err:
        print("inverse SQL execution error", err)
        executability = 0

    if executability == 1:
        cur = db_con.cursor()
        original_result = []
        original_execution = cur.execute(original_sql).fetchall()
        if original_execution != None:
            for row in original_execution:
                x = [str(y) for y in row]
                if len(x) > 0:
                    original_result.append(",".join(x))
        inverse_result = []
        inverse_execution = cur.execute(inverse_sql).fetchall()
        if inverse_execution != None:
            for row in inverse_execution:
                x = [str(y) for y in row]
                if len(x) > 0:
                    inverse_result.append(",".join(x))
        print("original result: ", ",".join(original_result) if len(original_result) > 0 else "")
        print("inverse result: ", ",".join(inverse_result) if len(inverse_result) > 0 else "")
        cur.close()
        return ",".join(original_result) if len(original_result) > 0 else "", ",".join(inverse_result) if len(
            inverse_result) > 0 else ""
    else:
        print("original result:", "XXXXYYYY")
        print("inverse result:", "YYYYXXXX")
        return "XXXXYYYY", "YYYYXXXX"


if __name__ == "__main__":
    for prefix in ["512k", "1024k"]:
        target_labels = ["test", "dev", "training"]

        init_file = f"../samples/init/{prefix}_samples_all.jsonl"
        output_file = f"../samples/other/{prefix}_samples_target.jsonl"

        samples_all = []
        with jsonlines.open(init_file) as reader:
            for line in reader:
                label = line["label"]
                if label in target_labels:
                    samples_all.append(line)

        samples_done = []
        if os.path.exists(output_file):
            with jsonlines.open(output_file) as reader:
                for line in reader:
                    if line["question"] != "":
                        samples_done.append(line)
        print("samples done", len(samples_done))

        samples_all_final = []
        for sample_x in samples_all:
            sample_x_articles = ",".join(sample_x["articles"])
            sample_x_sql = sample_x["sql"]
            for sample_y in samples_done:
                sample_y_articles = ",".join(sample_y["articles"])
                sample_y_sql = sample_y["sql"]
                if sample_y_articles == sample_x_articles and sample_y_sql == sample_x_sql:
                    if sample_y["question"] != "":
                        sample_x["question"] = sample_y["question"]
                        sample_x["answer"] = sample_y["answer"]
                        break
            samples_all_final.append(sample_x)
        with jsonlines.open(output_file, "w") as writer:
            writer.write_all(samples_all_final)

        failures = 0
        sample_index = 0
        for sample in tqdm(samples_all_final, desc=prefix):
            if sample["question"] == "":
                print(f"#########", sample["sql"])
                question, answer = llm_prompting_sql2nl(sample["sql"], sample)
                if question != "":
                    print(question)
                    sample["question"] = question
                    sample["answer"] = answer
                    samples_all_final[sample_index] = sample
                    print("#########", "DONE")
                    with jsonlines.open(output_file, "w") as writer:
                        writer.write_all(samples_all_final)
                else:
                    failures += 1
                    print("#########", "FAILED", failures)
            sample_index += 1
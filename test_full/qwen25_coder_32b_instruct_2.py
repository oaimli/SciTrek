# Qwen2.5-Coder-32B-Instruct + SQL execution
# Step 1: Database construction based on retrieval with Qwen2.5-Coder-32B-Instruct
# Step 2: Convert the natural language questions to SQL queries
# Step 3: Execute SQL queries to get the answers
import random
from vllm import LLM, SamplingParams
from tqdm import tqdm
from transformers import AutoTokenizer
import json
import jsonlines
import os
import sqlite3
import sys

sys.path.append("../")
from benchmark.dataset.data_loading import load_test, load_articles


def constructing_db_gold(cluster_papers):
    db_name = "tmp_qwen25.db"
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


def extract_title(markdown):
    title = ""
    segment_index = 0
    chunk_size = 16000
    while chunk_size * (segment_index + 1) <= len(markdown):
        segment = markdown[chunk_size * segment_index: chunk_size * (segment_index + 1)]
        trials = 0
        while True:
            prompt_content = open("extraction_prompts/title_extraction.txt").read()
            prompt_content = prompt_content.replace("<MARKDOWN>", segment)
            conversation = [{"role": "user",
                             "content": prompt_content}]
            text = tokenizer.apply_chat_template(
                conversation,
                tokenize=False,
                add_generation_prompt=True
            )
            conversation_outputs = llm.generate([text], sampling_params, use_tqdm=False)
            output_raw = conversation_outputs[0].outputs[0].text
            print(output_raw)
            # parse the generation
            trials += 1
            try:
                output_json = json.loads(output_raw)
                if isinstance(output_json, dict):
                    if "title" in output_json.keys():
                        title = output_json["title"]
                        break
            except json.JSONDecodeError as err:
                print("JSON parsing error,", err)

            if trials == 3:
                title = ""
                break

        if title != "":
            break
        segment_index += 1
    return title


def extract_authors(markdown):
    authors = ""
    segment_index = 0
    chunk_size = 16000
    while chunk_size * (segment_index + 1) <= len(markdown):
        segment = markdown[chunk_size * segment_index: chunk_size * (segment_index + 1)]
        trials = 0
        while True:
            prompt_content = open("extraction_prompts/authors_extraction.txt").read()
            prompt_content = prompt_content.replace("<MARKDOWN>", segment)
            conversation = [{"role": "user",
                             "content": prompt_content}]
            text = tokenizer.apply_chat_template(
                conversation,
                tokenize=False,
                add_generation_prompt=True
            )
            conversation_outputs = llm.generate([text], sampling_params, use_tqdm=False)
            output_raw = conversation_outputs[0].outputs[0].text
            print(output_raw)
            # parse the generation
            trials += 1
            try:
                output_json = json.loads(output_raw)
                if isinstance(output_json, dict):
                    if "authors" in output_json.keys():
                        authors = output_json["authors"]
                        break
            except json.JSONDecodeError as err:
                print("JSON parsing error,", err)

            if trials == 3:
                authors = ""
                break

        if authors != "":
            break
        segment_index += 1
    return authors


def extract_reference_count(markdown):
    reference_count_total = 0
    segment_index = 0
    chunk_size = 16000
    while chunk_size * (segment_index + 1) <= len(markdown):
        segment = markdown[chunk_size * segment_index: chunk_size * (segment_index + 1)]
        trials = 0
        while True:
            prompt_content = open("extraction_prompts/reference_count_extraction.txt").read()
            prompt_content = prompt_content.replace("<MARKDOWN>", segment)
            conversation = [{"role": "user",
                             "content": prompt_content}]
            text = tokenizer.apply_chat_template(
                conversation,
                tokenize=False,
                add_generation_prompt=True
            )
            conversation_outputs = llm.generate([text], sampling_params, use_tqdm=False)
            output_raw = conversation_outputs[0].outputs[0].text
            print(output_raw)
            # parse the generation
            trials += 1
            try:
                output_json = json.loads(output_raw)
                if isinstance(output_json, dict):
                    if "reference_count" in output_json.keys():
                        reference_count = output_json["reference_count"]
                        if reference_count.isdigit():
                            reference_count_total += int(reference_count)
                            break
            except json.JSONDecodeError as err:
                print("JSON parsing error,", err)

            if trials == 3:
                reference_count_total += 0
                break

        segment_index += 1
    return reference_count_total


def extract_cited_references(target_paper, cluster_papers):
    target_title = target_paper["title"]
    references = []
    for cluster_paper in cluster_papers:
        if cluster_paper["article_id"] != target_paper["article_id"]:
            markdown = cluster_paper["markdown"]
            cites = []
            segment_index = 0
            chunk_size = 16000
            while chunk_size * (segment_index + 1) <= len(markdown):
                segment = markdown[chunk_size * segment_index: chunk_size * (segment_index + 1)]
                trials = 0
                while True:
                    prompt_content = open("extraction_prompts/cited_reference_extraction.txt").read()
                    prompt_content = prompt_content.replace("<MARKDOWN>", segment)
                    prompt_content = prompt_content.replace("<TITLE>", target_title)
                    conversation = [{"role": "user",
                                     "content": prompt_content}]
                    text = tokenizer.apply_chat_template(
                        conversation,
                        tokenize=False,
                        add_generation_prompt=True
                    )
                    conversation_outputs = llm.generate([text], sampling_params, use_tqdm=False)
                    output_raw = conversation_outputs[0].outputs[0].text
                    print(output_raw)
                    # parse the generation
                    trials += 1
                    try:
                        output_json = json.loads(output_raw)
                        if isinstance(output_json, dict):
                            if "a_cited_by_b" in output_json.keys():
                                a_cited_by_b = output_json["a_cited_by_b"].lower()
                                if "true" in a_cited_by_b:
                                    cites.append(1)
                                    break
                                if "false" in a_cited_by_b:
                                    cites.append(0)
                                    break
                    except json.JSONDecodeError as err:
                        print("JSON parsing error,", err)

                    if trials == 3:
                        cites.append(0)
                        break

                segment_index += 1
            if sum(cites) > 0:
                references.append(cluster_paper["article_id"])
    return references


def constructing_db_tmp(cluster_papers):
    # element extraction with LLMs
    for paper_index, paper in enumerate(cluster_papers):
        markdown = paper["markdown"]
        # title
        paper["title"] = extract_title(markdown)
        # authors
        paper["authors"] = extract_authors(markdown)
        # reference-count
        paper["referenceCount"] = extract_reference_count(markdown)
        # references
        paper["references"] = extract_cited_references(paper, cluster_papers)
        cluster_papers[paper_index] = paper


    db_name = "tmp_qwen25.db"
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


def llm_prompting_nl2sql(question, db_con):
    prompt_content = open("../test_meta/prompt_nl2sql.txt").read().strip()
    prompt_content = prompt_content.replace("<QUESTION>", question)

    trials = 0
    while True:
        conversation = [{"role": "system",
                         "content": "You are requested to carefully understand the instruction about SQL and give the response following the required format."},
                        {"role": "user",
                         "content": prompt_content}]
        text = tokenizer.apply_chat_template(
            conversation,
            tokenize=False,
            add_generation_prompt=True
        )
        conversation_outputs = llm.generate([text], sampling_params, use_tqdm=False)
        output_raw = conversation_outputs[0].outputs[0].text
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
    return inverse_sql


if __name__ == "__main__":
    random.seed(42)
    model_name_save = "qwen25_coder_32b_instruct"
    target_mode = "test_full"
    # sample_levels = ["64k", "128k", "512k", "1024k"]
    sample_levels = ["512k", "1024k"]

    model_name_official = "Qwen/Qwen2.5-Coder-32B-Instruct"
    vllm_tensor_parallel_size = 4
    vllm_max_model_length = 32768
    llm = LLM(model=model_name_official, max_model_len=vllm_max_model_length,
              tensor_parallel_size=vllm_tensor_parallel_size)
    #  max_tokens is for the maximum length for generation.
    tokenizer = AutoTokenizer.from_pretrained(model_name_official)
    sampling_params = SamplingParams(n=3, temperature=0.7, top_p=0.8, top_k=20, repetition_penalty=1.05,
                                     max_tokens=8192)

    papers_all = load_articles(articles_folder="../bench/article/")

    # testing on different sample levels
    for sample_level in sample_levels:
        save_name = f"../results_test/{sample_level}_{target_mode}_{model_name_save}.jsonl"
        samples_test = load_test(prefix=sample_level, samples_folder="../benchmark/dataset/samples/final/")
        # the process is slow, we sample a subset for each sample_level
        if len(samples_test) > 50:
            samples_test = random.sample(samples_test, 50)
        print("original samples loaded", len(samples_test))

        for sample_index, sample in tqdm(enumerate(samples_test), total=len(samples_test),
                                         desc=f"{model_name_save}_{sample_level}"):
            question = sample["question"]
            # load cluster of articles
            cluster_papers = []
            for paper_id in sample["articles"]:
                paper = papers_all[paper_id]
                paper["article_id"] = paper_id
                cluster_papers.append(paper)
            db_con_gold = constructing_db_gold(cluster_papers)

            sql_query = llm_prompting_nl2sql(question, db_con_gold)

            db_con_tmp = constructing_db_tmp(cluster_papers)

            # execute the sql query
            cur = db_con_tmp.cursor()
            sql_result = []
            sql_execution = cur.execute(sql_query).fetchall()
            if sql_execution != None:
                for row in sql_execution:
                    x = [str(y) for y in row]
                    if len(x) > 0:
                        sql_result.append(",".join(x))
            output = ", ".join(sql_result) if len(sql_result) > 0 else ""
            sample["generations"] = [output, output, output]
            print(sample["answer"], output)

            samples_test[sample_index] = sample

        with jsonlines.open(save_name, "w") as writer:
            writer.write_all(samples_test)


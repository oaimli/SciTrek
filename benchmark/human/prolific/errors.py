import json

import jsonlines

with open("analysis/quality_check_nor.json") as f:
    annotations = json.load(f)

not_aligned = {}
not_agreed = {}
not_both = {}
all_valid = {}
for sample_id, annotation in annotations.items():
    # if annotation["answer"] != "NULL":
    all_valid[sample_id] = annotation
    agreed = annotation["agreed"]
    aligned = annotation["aligned"]
    if agreed == 0:
        not_agreed[sample_id] = annotation
    if aligned < 2:
        not_aligned[sample_id] = annotation
    if agreed == 1 and aligned < 2:
        not_both[sample_id] = annotation

print("not aligned", len(not_aligned), len(all_valid))
print("not agreed", len(not_agreed), len(all_valid))
print("not aligned but agreed", len(not_both), len(all_valid))

with open("../../article/papers_final.json") as f:
    papers_all = json.load(f)

annotation_samples = {}
with jsonlines.open("alignment/data_files/samples_qwen25_21.jsonl") as reader:
    for line in reader:
        annotation_samples[line["id"]] = line["meta"]

content = []
for sample_id, annotation in not_aligned.items():
    sample = annotation_samples[sample_id]
    sql_type = sample["sql_type"]
    question = sample["question"]
    answer = sample["answer"]
    content.append(f"\n############################# Sample ID {sample_id} #################################")
    content.append(f"SQL type: {sql_type}")
    content.append(f"Question: {question}")
    content.append(f"SQL query: {sample['sql']}")
    content.append(f"Answer: {answer}")
    assert annotation["question"] == sample["question"]
    for annotator_id, annotated_answer in annotation["annotations"].items():
        content.append(f"{annotator_id}: {annotated_answer}")
    content.append(f"Aligned: {annotation['aligned']}/3, Agreed: {annotation['agreed']}/1")

    cluster_papers = []
    for paper_id in sample["articles"]:
        paper = papers_all[paper_id]
        paper["article_id"] = paper_id
        cluster_papers.append(paper)

    content.append("\n*******The table of articles*******")
    # articles
    articles = []
    articles.append(["article_id", "article_title", "title_word_count", "author_count", "reference_count"])
    for paper in cluster_papers:
        article_id = paper["article_id"]
        article_title = paper["title"]
        title_word_count = len(article_title.split())
        author_count = len(paper["authors"].split(","))
        reference_count = paper["referenceCount"]
        articles.append([article_id, article_title, title_word_count, author_count, reference_count])
    for row in articles:
        content.append(", ".join([str(x) for x in row]))

    content.append("\n*******The table of article-author relationship*******")
    # article-author
    article_author = []
    article_author.append(["article_id", "author_name", "author_position"])
    for paper in cluster_papers:
        article_id = paper["article_id"]
        paper_authors = [author.strip() for author in paper["authors"].split(",")]
        for order, author in enumerate(paper_authors):
            article_author.append([article_id, author, order])
    for row in article_author:
        content.append(", ".join([str(x) for x in row]))

    content.append("\n*******The table of citation relationship among the articles*******")
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
                citing_cited.append([article_id, paper_reference])
    for row in citing_cited:
        content.append(", ".join([str(x) for x in row]))


    with open("eyeballing.txt", "w") as f:
        f.write("\n".join(content))
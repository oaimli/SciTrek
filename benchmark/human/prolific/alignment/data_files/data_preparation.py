import jsonlines
import random
import json

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

if __name__ == "__main__":
    with open("../../../../article/papers_final.json") as f:
        papers_all = json.load(f)
    # load valid data
    random.seed(42)
    samples_all = []
    for prefix in ["64k", "128k", "512k", "1024k", "single"]:
        save_file = f"../../../../dataset/samples/final/{prefix}_samples_target.jsonl"

        samples_tmp = []
        with jsonlines.open(save_file) as reader:
            for line in reader:
                if line["question"] != "" and "database" not in line["question"]:
                    table_articles, table_article_author, table_citing_cited = get_tables(line, papers_all)
                    line["table_articles"] = table_articles
                    line["table_article_author"] = table_article_author
                    line["table_citing_cited"] = table_citing_cited
                    if len(line["articles"]) <= 10:
                        samples_tmp.append(line)
        samples_all.extend(samples_tmp)
    print("samples all (<10 articles)", len(samples_all))

    detailed_samples = {}
    for sample in samples_all:
        if sample["question"] != "":
            info = sample["sql_type"]
            tmp = detailed_samples.get(info, [])
            tmp.append(sample)
            detailed_samples[info] = tmp
    print("SQL categories", len(detailed_samples))
    sampled_samples = []
    for info, samples_tmp in detailed_samples.items():
        templates = set([])
        for sample in samples_all:
            if sample["sql_type"] == info and sample["question"] != "":
                template = sample["template"]
                templates.add(template)
        print(info, "samples:", len(samples_tmp), "templates:", len(templates))

        sampled_samples.extend(random.sample(samples_tmp, 3))
    random.shuffle(sampled_samples)
    print("sampled samples", len(sampled_samples))

    # quality control
    quality_control_ids = []
    quality_control_ids = random.sample(range(len(sampled_samples)), len(detailed_samples.keys()))
    print("quality_control_ids", quality_control_ids)

    annotation_samples = []
    for index, sample in enumerate(sampled_samples):
        annotation_sample = {}
        if index in quality_control_ids:
            annotation_sample["id"] = f"{index}_testing"
        else:
            annotation_sample["id"] = str(index)
        annotation_sample["meta"] = sample

        text_dict = {}
        text_dict["table_articles"] = sample["table_articles"]
        text_dict["table_article_author"] = sample["table_article_author"]
        text_dict["table_citing_cited"] = sample["table_citing_cited"]
        text_dict["question"] = sample["question"]
        annotation_sample["text"] = text_dict
        print(len(sample["table_articles"]), len(sample["table_article_author"]), len(sample["table_citing_cited"]))
        print(sample["question"])
        annotation_samples.append(annotation_sample)

    with jsonlines.open("samples_qwen25.jsonl", "w") as writer:
        writer.write_all(annotation_samples)
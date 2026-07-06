import json


if __name__ == "__main__":
    with open("sampled_samples.json") as f:
        sampled_samples = json.load(f)

    with open("../../article/papers_final.json") as f:
        papers_all = json.load(f)

    content = []
    for sample_index, sample in enumerate(sampled_samples):
        sql_type = sample["sql_type"]
        question = sample["question"]
        answer = sample["answer"]
        content.append(f"\n############################# Sample {sample_index} #################################")
        content.append(f"SQL type: {sql_type}")
        content.append(f"Question: {question}")
        content.append(f"Answer: {answer}")

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

    with open("textual_samples.txt", "w") as f:
        f.write("\n".join(content))


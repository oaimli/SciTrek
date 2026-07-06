import json


with open("papers_correct.json") as f:
    papers_correct = json.load(f)
papers_annotated_tmp = {}
with open("papers_annotated_tmp.json") as f:
     for paper_id, paper_info in json.load(f).items():
         if paper_info["status"] == "done":
             papers_annotated_tmp[paper_id] = paper_info

papers_annotating = {}
for paper_id, paper_info in papers_correct.items():
    if paper_id in papers_annotated_tmp.keys():
        reference_count = papers_annotated_tmp[paper_id]["referenceCount"]
        authors = []
        for author in paper_info["authors"]:
            authors.append(author["name"])
        papers_annotating[paper_id] = {
            "title": papers_annotated_tmp[paper_id]["title"],
            "referenceCount": reference_count,
            "authors": ", ".join(authors),
            "status": "done"
            }
    else:
        reference_count = paper_info["referenceCount"]
        authors = []
        for author in paper_info["authors"]:
            authors.append(author["name"])
        papers_annotating[paper_id] = {
            "title": paper_info["title"],
            "referenceCount": reference_count,
            "authors": ", ".join(authors),
            "status": "done no"
            }

with open("papers_annotated.json", "w") as f:
    json.dump(papers_annotating, f, indent=4)

import json
import random

with open("papers_correct.json") as f:
    papers_correct = json.load(f)
with open("papers_annotated.json") as f:
    papers_annotated = json.load(f)
with open("papers_gemini.json") as f:
    papers_gemini = json.load(f)

for paper_id, paper_info in papers_correct.items():
    if papers_annotated[paper_id]["status"] == "done":
        # replace the data with human annotation
        papers_correct[paper_id]["title"] = papers_annotated[paper_id]["title"]
        papers_correct[paper_id]["referenceCount"] = papers_annotated[paper_id]["referenceCount"]
        papers_correct[paper_id]["authors"] = papers_annotated[paper_id]["authors"]
    elif papers_annotated[paper_id]["status"] == "done reference":
        # replace the reference count with human annotation
        papers_correct[paper_id]["referenceCount"] = papers_annotated[paper_id]["referenceCount"]
        # replace the authors and title with Gemini annotation
        papers_correct[paper_id]["title"] = papers_gemini[paper_id]["title"]
        papers_correct[paper_id]["authors"] = papers_gemini[paper_id]["authors"]
    else:
        # replace the data with Gemini annotation
        papers_correct[paper_id]["title"] = papers_gemini[paper_id]["title"]
        papers_correct[paper_id]["referenceCount"] = papers_gemini[paper_id]["referenceCount"]
        papers_correct[paper_id]["authors"] = papers_gemini[paper_id]["authors"]

    # replace the Markdown text by Marker with that by Gemini
    with open(f"../md_gemini/{paper_id}.md") as f:
        md_gemini = f.read()
    papers_correct[paper_id]["markdown"] = md_gemini

with open("papers_final.json", "w") as f:
    json.dump(papers_correct, f, indent=4)
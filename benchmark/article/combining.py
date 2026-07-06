# combining the markdown documents into a single file
import json
import os
import random
import sys
sys.path.append("../../")
from utils.tokenizer_llama3.tokenizer import Tokenizer

tokenizer = Tokenizer("../../utils/tokenizer_llama3/tokenizer.model")

# there are all possible papers in graphs for different subtopics
with open("graphs.json") as f:
    graphs = json.load(f)

# only a subset of papers have PDFs
all_papers = {}
for subtopic, graph in graphs.items():
    # print(subtopic)
    papers_detailed = {}
    for paper_id, paper_details in graph.items():
        if os.path.exists(f"../markdown/{paper_id}/{paper_id}.md"):
            paper_details["subtopic"] = subtopic
            with open(f"../markdown/{paper_id}/{paper_id}.md") as f:
                content = f.read()
            paper_details["markdown"] = content
            tokenized = tokenizer.encode(content, bos=True, eos=True)
            print(len(tokenized))
            paper_details["length"] = len(tokenized)
            papers_detailed[paper_id] = paper_details
            # copyfile(f"../pdfs/tmp/{paper_id}.pdf", f"../pdfs/{subtopic}/{paper_id}.pdf")
    all_papers.update(papers_detailed)

    print(subtopic, len(papers_detailed))
print("all papers with markdown:", len(all_papers))

with open("papers.json", "w") as f:
    json.dump(all_papers, f, indent=4)

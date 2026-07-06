import json


# with open("papers_correct.json") as f:
#     papers = json.load(f)
#
# statistics = {}
# for paper_id, paper_info in papers.items():
#     statistics[paper_info["subtopic"]] = statistics.get(paper_info["subtopic"], 0) + 1
# for key, value in statistics.items():
#     print(key, value)
#
# print("all articles", len(papers))

with open("papers_final.json") as f:
    papers = json.load(f)

names = set([])
for paper_id, paper in papers.items():
    authors = paper["authors"].split(",")
    for author in authors:
        names.add(author.strip())
print(len(names))
print(sorted(list(names)))
names_valid = []
for name in sorted(list(names)):
    valid = True
    if len(name) <= 4:
        valid = False
    if name.lower() == "fellow":
        valid = False

    if name.lower().startswith("and "):
        valid = False

    if valid:
        if name.lower().startswith("and "):
            name = " ".join(name.split()[1:])
            names_valid.append(name)
        else:
            names_valid.append(name)
    else:
        print(name)

with open("author_names.json", "w") as f:
    json.dump(names_valid, f, indent=4)
print(len(names_valid))
print(names_valid)

papers_left = {}
for paper_id, paper in papers.items():
    authors = paper["authors"].split(",")
    all_valid = True
    for author in authors:
        if author.strip() not in names_valid:
            all_valid = False
            break
    if not all_valid:
        print(paper_id, paper["authors"], paper["title"])
    if all_valid:
        papers_left[paper_id] = paper
print(len(papers), len(papers_left))
